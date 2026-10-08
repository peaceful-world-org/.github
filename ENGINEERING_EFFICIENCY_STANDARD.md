# Peaceful World — Engineering Efficiency Standard

Status: proposed organization-wide baseline (2026-10-08). This standard complements, and does not override, repository-specific release and safety contracts.

## Scope and accounting

The organization has independent GitHub repositories. A workflow, AGENTS.md rule, or branch configuration in website-lab does **not** automatically apply to another repository or to stale branches that have not incorporated the updated default branch.

Keep two consumption categories separate:
- **GitHub Actions**: runner minutes, artifact storage and workflow runs. Optimize triggers, repeat jobs, preview builds, installation overhead and retention.
- **AI-assisted development**: model requests, premium-model allowances, context and review effort. Optimize task routing, repeated investigations and unnecessary councils.

Do not claim verified account-level billing savings without actual billing/usage access.

## AI / agent model selection

1. Use the lowest-cost model and reasoning effort reliably sufficient for the task.
2. Lightweight models: routine edits, formatting, docs, deterministic preflights.
3. Mid-tier models: bounded implementation, routine review, regression follow-up.
4. Strong engineering models: multi-repository architecture/CI, complex debugging and security/release-sensitive code.
5. Highest-cost models: exceptional architecture or high-risk ambiguity, not routine code edits.
6. After discovery is settled, continue deterministic implementation on a cheaper capable model where practical.
7. Before any new expensive run, inspect current main, prior accepted decisions, existing PR/check results and available evidence. Reuse prior QA rather than rerun it unchanged.
8. Do not launch duplicate high-cost reviews or councils without a distinct decision question. Include the recommended model and reasoning level in Work/Codex instructions.
9. Stay within natural plan limits; do not silently assume extra credit purchases.

The detailed website implementation policy remains in website-lab/docs/AI_MODEL_EFFICIENCY_POLICY.md.

## CI / GitHub Actions default

- Prefer short, deterministic source or contract checks on PRs and **surface-scoped** tests when the touched surface is known.
- Preserve full regression for shared runtimes, build/release infrastructure, security, data/analytics, global routing, unknown diffs or explicit owner request. Unknown scope must fail closed to full.
- Skip heavy checks for verified documentation-only changes, but **preserve required status checks**: if branch protection requires a job, prefer a cheap passing classifier job plus conditional heavy job over making the whole required workflow disappear.
- Cancel superseded PR runs with concurrency/cancel-in-progress; avoid cancelling an already authorized production release.
- Avoid duplicate browser suites in both QA and preview pipelines when a tested exact artifact can safely be reused; preserve reproducibility.
- Add timeout-minutes, minimum necessary permissions, and short artifact retention. Do not add Actions just for a cosmetic check that existing fast QA covers.
- Ignore changes to purely internal instructions/docs in **deployment** workflows when those files do not change deployed bytes.
- Keep branch checks, release controls and proven product-specific QA intact. No forced pushes, secret exposure, or production/publishing bypasses to save minutes.

## Repository-specific boundaries

- **website-lab** is the source and staging for peaceful-world.org. Its chat-native Release v2, exact-artifact gate, scoped/full classification and owner approval apply **only** to the website.
- **peaceful-world.org** is generated-only production. Do not modify its public tree to propagate these instructions.
- **5** is the independent 5 Practice source/PWA/native app. Preserve its own i18n, consent, timers, Android/iOS and Pages checks and release approvals.
- **5-preview** is a preview/deployment surface; avoid production-equivalent checks for docs-only edits.
- **true-cost-of-war** preserves calculation/evidence checks and approved loader/preview routes; its existing Tilda-related paths must not be deleted merely because the primary site has migrated.
- **atlas-of-peace** and **peaceful-garden** should not get large CI suites before they have a concrete, maintained application/test surface.
- **true-cost-of-war-assets** contains release assets; protect immutable/history-sensitive release files.

## Verification and reporting

For each repository, record: existing triggers, expensive suites, concurrency, deploy behavior, what changed, and remaining caveats. Submit changes as small PRs, validate YAML and available status checks, and avoid deploying or merging production-affecting changes without an explicit release decision. Measure savings using Actions usage data if accessible; otherwise describe only expected reductions, not fabricated numbers.
