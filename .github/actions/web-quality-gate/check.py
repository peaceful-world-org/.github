#!/usr/bin/env python3
"""Peaceful World dependency-free static web quality audit."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


TRUTHY = {"1", "true", "yes", "on"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.title_parts: list[str] = []
        self.in_title = False
        self.description = ""
        self.canonical = ""
        self.viewport = ""
        self.robots = ""
        self.ids: list[str] = []
        self.refs: list[tuple[str, str, str]] = []
        self.main_count = 0
        self.h1_count = 0
        self.images_missing_alt: list[str] = []
        self.iframes_missing_title: list[str] = []
        self.has_hreflang = False
        self.multilingual_signal = False
        self.in_jsonld = False
        self.jsonld_buffer: list[str] = []
        self.jsonld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()

        if tag == "html":
            self.html_lang = data.get("lang", "").strip()
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = data.get("name", "").lower()
            if name == "description":
                self.description = data.get("content", "").strip()
            elif name == "viewport":
                self.viewport = data.get("content", "").strip()
            elif name == "robots":
                self.robots = data.get("content", "").strip()
        elif tag == "link":
            rel = data.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = data.get("href", "").strip()
            if "alternate" in rel and data.get("hreflang", "").strip():
                self.has_hreflang = True
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            if "alt" not in data:
                self.images_missing_alt.append(data.get("src", "(inline image)"))
        elif tag == "iframe":
            if not data.get("title", "").strip():
                self.iframes_missing_title.append(data.get("src", data.get("data-src", "(iframe)")))
        elif tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.jsonld_buffer = []

        if any(key in data for key in ("data-en", "data-ru", "data-pw-lang")):
            self.multilingual_signal = True

        element_id = data.get("id", "").strip()
        if element_id:
            self.ids.append(element_id)

        for attr in ("href", "src"):
            value = data.get(attr, "").strip()
            if value:
                self.refs.append((tag, attr, value))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_jsonld:
            self.jsonld_blocks.append("".join(self.jsonld_buffer).strip())
            self.jsonld_buffer = []
            self.in_jsonld = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_jsonld:
            self.jsonld_buffer.append(data)

    @property
    def title(self) -> str:
        return " ".join(part.strip() for part in self.title_parts if part.strip()).strip()

    @property
    def indexable(self) -> bool:
        return "noindex" not in self.robots.lower()


def bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUTHY


def changed_html(root: Path) -> list[Path] | None:
    if not bool_env("PW_CHANGED_ONLY", True):
        return None

    base_ref = os.getenv("GITHUB_BASE_REF", "").strip()
    if not base_ref:
        return None

    try:
        subprocess.run(
            ["git", "fetch", "--no-tags", "--depth=1", "origin", base_ref],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", f"origin/{base_ref}...HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    cwd = Path.cwd().resolve()
    files: list[Path] = []
    for raw in result.stdout.splitlines():
        candidate = (cwd / raw).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if candidate.suffix.lower() in {".html", ".htm"} and candidate.is_file():
            files.append(candidate)
    return sorted(set(files))


def all_html(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".htm"}
        and ".git" not in path.parts
    )


def is_external_or_ignored(ref: str) -> bool:
    value = ref.strip()
    if not value or value.startswith(("#", "/", "//", "{", "<%")):
        return True
    lowered = value.lower()
    if lowered.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:")):
        return True
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc)


def resolve_local_ref(page: Path, ref: str) -> Path | None:
    if is_external_or_ignored(ref):
        return None

    parsed = urlparse(ref)
    raw_path = unquote(parsed.path)
    if not raw_path:
        return None

    target = (page.parent / raw_path).resolve()
    if target.exists():
        return target

    if raw_path.endswith("/"):
        index = target / "index.html"
        return index if index.exists() else target

    if target.suffix == "":
        index = target / "index.html"
        if index.exists():
            return index
        html_variant = target.with_suffix(".html")
        if html_variant.exists():
            return html_variant

    return target


def audit_page(page: Path, root: Path, require_metadata: bool) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    try:
        text = page.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append("not valid UTF-8")
        return errors, warnings, notes

    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:
        errors.append(f"HTML parser error: {exc}")
        return errors, warnings, notes

    duplicate_ids = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
    if duplicate_ids:
        preview = ", ".join(duplicate_ids[:8])
        suffix = "..." if len(duplicate_ids) > 8 else ""
        errors.append(f"duplicate element IDs: {preview}{suffix}")

    core_metadata = [
        ("html[lang]", parser.html_lang),
        ("title", parser.title),
        ("meta description", parser.description),
    ]
    for label, value in core_metadata:
        if not value:
            message = f"missing {label}"
            if require_metadata:
                errors.append(message)
            else:
                warnings.append(message)

    if not parser.viewport:
        warnings.append("missing viewport meta")

    if parser.main_count == 0:
        warnings.append("missing <main> landmark")
    elif parser.main_count > 1:
        warnings.append(f"multiple <main> landmarks ({parser.main_count})")

    if parser.h1_count == 0:
        warnings.append("missing <h1>")

    if parser.images_missing_alt:
        shown = ", ".join(parser.images_missing_alt[:8])
        suffix = "..." if len(parser.images_missing_alt) > 8 else ""
        warnings.append(f"images without alt attribute: {shown}{suffix}")

    if parser.iframes_missing_title:
        shown = ", ".join(parser.iframes_missing_title[:8])
        suffix = "..." if len(parser.iframes_missing_title) > 8 else ""
        errors.append(f"iframes without title: {shown}{suffix}")

    missing_refs: list[str] = []
    for tag, attr, ref in parser.refs:
        target = resolve_local_ref(page, ref)
        if target is None:
            continue
        try:
            target.relative_to(root)
        except ValueError:
            continue
        if not target.exists():
            missing_refs.append(f"{tag}[{attr}]={ref}")

    if missing_refs:
        shown = ", ".join(missing_refs[:8])
        suffix = "..." if len(missing_refs) > 8 else ""
        errors.append(f"missing relative references: {shown}{suffix}")

    for block in parser.jsonld_blocks:
        if not block:
            warnings.append("empty JSON-LD block")
            continue
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            warnings.append(f"invalid JSON-LD: {exc.msg}")

    if parser.indexable:
        if not parser.canonical:
            warnings.append("indexable page has no canonical URL")
        if not parser.jsonld_blocks:
            warnings.append("indexable page has no structured data (JSON-LD)")
        if parser.multilingual_signal and not parser.has_hreflang:
            warnings.append("multilingual page has no hreflang alternates")
    else:
        notes.append("page is noindex; canonical/schema/hreflang discoverability checks were relaxed")

    return errors, warnings, notes


def main() -> int:
    repo_root = Path.cwd().resolve()
    scan_root = (repo_root / os.getenv("PW_SCAN_ROOT", ".")).resolve()
    mode = os.getenv("PW_MODE", "baseline").strip().lower()
    require_metadata = bool_env("PW_REQUIRE_METADATA", False)

    if mode not in {"advisory", "baseline", "strict"}:
        print(f"::error::Unsupported PW_MODE: {mode}")
        return 2

    try:
        scan_root.relative_to(repo_root)
    except ValueError:
        print("::error::scan_root must stay inside the checked-out repository")
        return 2

    if not scan_root.exists():
        print(f"::error::scan_root does not exist: {scan_root}")
        return 2

    candidates = changed_html(scan_root)
    selection = "changed HTML files"
    if candidates is None:
        candidates = all_html(scan_root)
        selection = "all HTML files"

    errors: list[tuple[Path, str]] = []
    warnings: list[tuple[Path, str]] = []
    notes: list[tuple[Path, str]] = []

    for page in candidates:
        page_errors, page_warnings, page_notes = audit_page(page, scan_root, require_metadata)
        relative = page.relative_to(repo_root)
        errors.extend((relative, message) for message in page_errors)
        warnings.extend((relative, message) for message in page_warnings)
        notes.extend((relative, message) for message in page_notes)

    summary_lines = [
        "## Peaceful World web quality gate",
        "",
        f"- Mode: **{mode}**",
        f"- Scan root: `{scan_root.relative_to(repo_root)}`",
        f"- Selection: {selection}",
        f"- HTML files audited: **{len(candidates)}**",
        f"- Errors: **{len(errors)}**",
        f"- Warnings: **{len(warnings)}**",
        f"- Notes: **{len(notes)}**",
        "",
        "Checks include structural integrity, basic accessibility signals, and search/AI discoverability hygiene.",
        "",
    ]

    if errors:
        summary_lines += ["### Errors", ""]
        summary_lines += [f"- `{path}`: {message}" for path, message in errors[:50]]
        if len(errors) > 50:
            summary_lines.append(f"- ...and {len(errors) - 50} more")
        summary_lines.append("")

    if warnings:
        summary_lines += ["### Warnings", ""]
        summary_lines += [f"- `{path}`: {message}" for path, message in warnings[:50]]
        if len(warnings) > 50:
            summary_lines.append(f"- ...and {len(warnings) - 50} more")
        summary_lines.append("")

    if notes:
        summary_lines += ["### Notes", ""]
        summary_lines += [f"- `{path}`: {message}" for path, message in notes[:30]]
        if len(notes) > 30:
            summary_lines.append(f"- ...and {len(notes) - 30} more")
        summary_lines.append("")

    if not candidates:
        summary_lines += [
            "No HTML files matched this run. This is normal for documentation-only changes.",
            "",
        ]

    step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write("\n".join(summary_lines) + "\n")

    for path, message in errors:
        print(f"::error file={path}::{message}")
    for path, message in warnings:
        print(f"::warning file={path}::{message}")
    for path, message in notes:
        print(f"::notice file={path}::{message}")

    if mode == "advisory":
        return 0
    if errors:
        return 1
    if mode == "strict" and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
