# Peaceful World — Product Golden Path v1

This document defines the default path for new Peaceful World web products and major website changes.

The goal is not to add process. The goal is to remove repeated manual decisions and make safe releases cheap.

## The default flow

```text
idea
  ↓
issue / brief
  ↓
branch
  ↓
pull request
  ↓
automated web check
  ↓
preview
  ↓
human / council review when useful
  ↓
merge
  ↓
production deployment
  ↓
live monitoring
  ↓
analytics → next iteration
```

## Core principles

1. **GitHub is the technical source of truth.**
   Product code, reusable standards, QA, releases and automation belong in GitHub.

2. **Google Drive is the institutional memory layer.**
   Research, grants, operating records and human-readable canonical documents remain in Drive unless they are product runtime inputs.

3. **One source of truth per concern.**
   Do not duplicate GitHub with GitLab, Monday with Asana/Jira, or MailerLite with another mailing system without a concrete reason.

4. **Preview before production.**
   Material product or website changes should be inspectable before they reach production.

5. **Automate repeated checks.**
   A machine should catch predictable mistakes before a person has to.

6. **Systemic fixes beat page-specific fixes.**
   Repeated visual, copy, accessibility or metadata problems should become Design System, Copy System or QA rules.

7. **Keep CI cheap.**
   Use path filters, short jobs, cancellation of superseded runs, small artifacts and dependency-free checks where possible.

## Golden Path v1 components

### 1. Shared web PR check

Organization workflow:

`.github/workflows/reusable-web-pr-check.yml`

It provides:

- a dependency-free HTML audit;
- duplicate ID detection;
- missing relative asset/link detection;
- optional metadata requirements;
- a GitHub job summary;
- an optional short-lived preview artifact.

Modes:

- `advisory` — report problems without blocking the PR;
- `baseline` — block on structural errors, metadata remains advisory;
- `strict` — block on structural errors and warnings.

Repositories should begin in `advisory`, then move to `baseline` once existing debt is understood.

### 2. Preview policy

Golden Path v1 uploads a short-lived preview artifact from the same runner as QA so it does not create a second CI job.

A stable live URL per pull request is the next infrastructure step. We should add it only after selecting the production/preview host (for example an edge host connected to GitHub), rather than creating a fragile second Pages system.

Until then:

- existing repository-specific previews remain valid;
- preview artifacts give reviewers a reproducible build/surface;
- GitHub Pages main deployments remain unchanged.

### 3. Production policy

Do not replace a working production path merely to make the architecture look cleaner.

Migration should be incremental:

1. build the GitHub-first replacement;
2. verify previews and QA;
3. run it in parallel where practical;
4. switch traffic only when rollback is clear;
5. remove the legacy layer later.

This is especially important for Tilda-backed public pages that are already indexed.

## Recommended caller workflow

A static repository can opt in with a small caller file:

```yaml
name: Peaceful World web PR check

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  web:
    uses: peaceful-world-org/.github/.github/workflows/reusable-web-pr-check.yml@main
    with:
      scan_root: "."
      mode: advisory
      changed_only: true
      require_metadata: false
      upload_preview: true
```

After the repository is clean enough:

```yaml
      mode: baseline
```

Public, citation-oriented surfaces can later use:

```yaml
      mode: strict
      require_metadata: true
```

## Repository-specific QA still belongs in the repository

The shared workflow is a baseline, not a replacement for product tests.

Examples:

- **5 Practice:** Android/iOS smoke tests, localization checks, PWA behavior;
- **True Cost of War:** calculation tests, source/data validation, research consistency;
- **website-lab:** design-system audit, content/model checks and release-specific QA.

The shared gate catches common web failures. Product repositories keep domain-specific checks.

## Pilot order

1. `website-lab`
2. `true-cost-of-war`
3. `5`
4. all new web products begin on the Golden Path by default

We start with `website-lab` because it is the safest place to learn. The live products should inherit the pattern after it proves useful.

## Next versions

Golden Path v1.1 adds lightweight accessibility and discoverability hygiene without adding another dependency or CI job. It still intentionally does **not** solve everything.

Planned layers:

- stable live URL for every PR preview;
- accessibility and Lighthouse budgets;
- machine-readable Design System checks;
- machine-readable Copy System checks;
- SEO / AI-discoverability checks;
- production observability and synthetic checks;
- release/rollback conventions;
- disaster-recovery checks.

Add these only when they reduce real work or real risk.
