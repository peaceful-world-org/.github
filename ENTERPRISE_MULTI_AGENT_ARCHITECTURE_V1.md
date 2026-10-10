# Peaceful World — Enterprise Multi-Agent Architecture v1

**Status: ACTIVE for human-orchestrated, on-demand independent review (owner approved 2026-10-10).** This is an operating standard, not an automatic agent integration. This is not an authorization to change Enterprise settings, install or repermission Apps, enable Copilot, add workflows or secrets, merge product PRs, publish production, or incur AI/API charges.

**Scope:** GitHub Enterprise Cloud governance of the existing `peaceful-world-org` organization; human-orchestrated developer/reviewer collaboration across its *independent* product repositories.

This document specializes the [AI Agent Operating Model](AI_AGENT_OPERATING_MODEL_V1.md), [Engineering Efficiency Standard](ENGINEERING_EFFICIENCY_STANDARD.md), [Enterprise Activation Plan](ENTERPRISE_ACTIVATION_PLAN.md) and [Product Golden Path](PRODUCT_GOLDEN_PATH.md). A repository's current `AGENTS.md`, required checks, release architecture and owner decisions always take precedence.

## 1. Architecture: independent work, independent evidence, human authority

```text
Owner: goal / scope / product acceptance / publication authority
    |
    v
ChatGPT / Codex: coordinator + primary implementer (bounded branch and PR)
    |
    +----> GitHub Actions: deterministic checks on the exact PR head
    |
    +----> Claude Code: independent read-only second opinion when risk warrants
    |         \-> findings with evidence, severity, uncertainty; NO code edits
    |
    +----> Grok / another independent reviewer: OPTIONAL challenge on a
    |         genuinely distinct question; never assumed to have repo access
    |
    v
Coordinator: verify and adjudicate findings against source, CI and citations
    |
    v
Primary implementer: make justified fixes on the same PR
    |
    v
Scoped QA on exact new head; targeted re-review if material P0/P1 changed
    |
    v
Preview + owner product acceptance -> repository-specific approved release
```

These are **functional roles, not GitHub accounts, seats or automatic integrations**. "Different models" is not enough for independent review if one only paraphrases the other's findings. Reviewers must receive the frozen source diff and acceptance criteria, but not the implementer's final verdict or the previous review before their first assessment.

Enterprise provides governance, policies and repository administration. It does **not** by itself supply Claude, Codex, Grok, third-party APIs, or GitHub Copilot/AI credits. GitHub Actions minutes and AI-model usage must be accounted for separately.

### Control and trust planes

| Plane | System of record | Authority boundary |
| --- | --- | --- |
| Product source | Each source repo: e.g. `website-lab`, `5`, `true-cost-of-war` | Codex/developer works on a bounded PR; does not bypass local `AGENTS.md` |
| Evidence | Repository CI runs, exact commit SHA, source citations, review reports | Green tests prove tested invariants, not truth of all assumptions |
| Second opinion | Human-invoked, authenticated Claude Code on the exact PR | Reviewer produces advisory findings; cannot autonomously approve/merge/publish |
| Enterprise governance | Enterprise/organization owners | Only owner authorizes membership, App access, policy, billing and authentication changes |
| Production | Per-repository release mechanism | Human approval + product-specific release gates; no generic enterprise auto-deploy rule |
| Institutional record | GitHub for technical decisions; Google Drive for internal operating records | Never disclose secrets, private donor/member details or unpublished sensitive research in public packets |

**Explicit website distinction:** `website-lab` is source, QA and staging; `peaceful-world.org` is generated-only production delivered by GitHub Pages through website Release Architecture v2. The 2026-10-05 cutover is complete. The website's exact-main chat-native release mechanism is **not** a default for the independent `5` or `true-cost-of-war` repositories. Do not introduce Tilda into current operational release paths.

## 2. What has already been validated

Two human-orchestrated *manual* independent reviews have provided evidence of incremental value:

1. **Research Catalog pilot:** [website-lab issue #871](https://github.com/peaceful-world-org/website-lab/issues/871), [PR #862](https://github.com/peaceful-world-org/website-lab/pull/862). Authenticated Claude Code reviewed a frozen head without editing code. It identified CI/test-maintenance risks beyond initial coordination. Codex addressed accepted findings, and measured preview browser QA improved from 118.4s to 45.8s; screenshot fallbacks fell from 5 to 0. This is a documented *pilot result*, not a guaranteed future speedup.
2. **Research/data pilot:** [true-cost-of-war PR #209](https://github.com/peaceful-world-org/true-cost-of-war/pull/209), independently reviewed by Claude Code. The reviewer flagged missing primary-source validation, misleading wording, hard-coded figures, self-referential test assertions and failure-case coverage. The coordinator separately assessed source evidence and implemented bounded corrections. The historical product outcome does **not** grant blanket review or publication rights.

Neither pilot establishes that GitHub's automatic Claude or Copilot reviewers were enabled. Grok did not complete an equivalent independent review in the Research pilot; do not count a requested review or a guest prompt as a result.

**Adopted owner preference (2026-10-10):** use authenticated existing-subscription Claude Code **on demand**, orchestrated by a human. Defer unattended Claude reviews, new Copilot purchases, additional model/API spend and GitHub App permission changes. The results can justify a future proposal, not silently change this decision.

## 3. Minimum useful review policy

| Class | Examples | Deterministic gate | Second opinion |
| --- | --- | --- | --- |
| R0 — routine | Docs, a typo, isolated trivial cosmetic adjustment with no runtime consequence | Cheapest appropriate checks | **Skip** Claude; avoid review theatre |
| R1 — bounded product | Isolated UI, component logic, local UX or copy with clear test coverage | Product/surface-scoped QA, preview as appropriate | Claude **optional**, especially when assumptions, accessibility or browser behavior are uncertain |
| R2 — material risk | Authentication, secret/data handling, GitHub Actions/release workflows, production routing, donations/financial interfaces, research figures, consequential EN/RU meaning changes, shared architecture | Relevant exact-head checks, source/contract verification; full regression when required by repo policy | **Independent Claude review required before routine promotion**, or explicitly record reviewer unavailability / owner-approved alternative |
| R3 — systemic or urgent | Cross-repo release/infrastructure changes, permissions/security incident, privacy exposure, high-impact public claim | Fail-closed safety checks, isolation/rollback and human incident decision | Claude + specialized/human review where appropriate; no automated approval or production bypass |

A passed review is **not** GitHub branch-protection approval. Do not configure Claude as a required reviewer/status check or treat its "READY" text as a substitute for repo checks, source validation, owner consent or legal/editorial judgment.

On R2/R3, missing reviewer access, stale SHA, unverified external claims, CI failure or inconclusive evidence is explicitly **INCONCLUSIVE / BLOCKED**, not "passed." Emergency intervention remains an owner decision under the existing incident and release procedures.

## 4. Single-package manual review workflow

1. **Freeze:** coordinator reads current target repo `main`, existing PR head/base SHA, diff, `AGENTS.md`, current checks, release boundary and approved acceptance criteria. Confirm which test runs actually cover the head; do not reuse stale runs as current.
2. **Prepare once:** on command **«ПОДГОТОВЬ К CLAUDE-РЕВЬЮ»**, produce a bounded review packet in the PR or the repo's existing `qa/council/current/00_REVIEW.md` location *if that repo uses the convention and the material may safely be stored there*. No public dumping of private diffs or credentials. The packet links to one frozen head and supplies the actual diff/context to an authorized reviewer.
3. **Independent first pass:** owner invokes their existing authenticated Claude Code; reviewer sees code, constraints and CI evidence, **not the developer/coordinator's own verdict**. Explicitly read-only. If authenticated repository access is absent, stop instead of pretending a pasted URL provides access.
4. **Report:** paths/line locations, test steps, severity P0/P1/P2/nit, evidence, alternative hypothesis, source provenance, what was *not* checked, and "no changes made." If source URLs were blocked, claim **not independently verified**.
5. **Adjudicate:** coordinator verifies each concrete finding. Label it `ACCEPT`, `REJECT (reason)` or `DEFER (risk + owner)`; separate a confirmed defect from a hypothesis and a pre-existing baseline failure from PR regression. Preserve original Claude report.
6. **Repair and gate:** implementation agent fixes accepted problems on the *same* PR/branch where safe, runs relevant CI on the **new** SHA, and requests **targeted** re-review only for material changes or unresolved P0/P1. Do not repeat unchanged costly full councils.
7. **Release:** owner accepts actual preview/product result, then invokes the *product's* release mechanism separately. No agent infers approval from a green PR or from the phrase "looks good" outside the product-release context.

Canonical practical instructions and reviewer prompt: [Claude Independent Review SOP](CLAUDE_INDEPENDENT_REVIEW_SOP_V1.md).

## 5. Access and permissions: intended vs. verified

**Design target for an independent reviewer (not a claim about current installations):**

- Repository access: **selected source repositories only**, and only for the duration/scope genuinely needed where the provider allows it.
- GitHub App permissions: repository metadata/read; contents/read; pull requests/read; Actions/read only where logs are necessary. PR/Issue **write for comments** is an optional, separately approved capability, not a prerequisite for doing manual review.
- No contents/write, Workflows/write, Administration, organization owner authority, production credentials, DNS, billing or unrestricted repository membership for a review-only service.
- **Installation repository selection and the App's own permission categories are distinct constraints.** A narrow repository list does not make broad `Contents: write` harmless. A prompt saying "read-only" is a behavioral instruction, **not** GitHub-enforced least privilege.
- The existing Claude/Grok installed permission matrices and pending Claude permission update are **not fully verified** because elevated GitHub authentication is required. Do **not** auto-approve, revoke or modify these installations as a side effect of adopting the SOP.
- The website's `pw-release-publisher` is a **separate publishing principal**, not a reviewer or coding identity. Its receiver-only write capability and Release v2 preflight must remain isolated.

Official GitHub references: [Choosing App permissions](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app) · [Review installed Apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps).

## 6. Cost, timing and anti-duplication guardrails

- Default to **one** review on one frozen head when risk warrants. Don't re-run the same broad model review after a small copy fix; do a precise delta review if needed.
- R0: deterministic checks only. R1: targeted CI, then optional second opinion. R2/R3: a stronger independent reviewer on the narrowest meaningful problem; prefer ordinary capable models for routine work and stronger reasoning only for complex security/architecture or evidence-heavy claims.
- Coordinator/Work model suggestion: **GPT-6 Medium** for normal scoped coordination, **GPT-6 High** for cross-repository release/security architecture. Claude Code: choose the least expensive available model/reasoning setting that can responsibly review the change; reserve its strongest setting for genuinely difficult work. This is guidance, not automatic model configuration.
- Record manual time, source SHA, review token/plan cost **if observable**, real bugs found, false positives, acceptance decisions and avoided reruns. Do not invent savings or equate GitHub Actions' monthly minutes with vendor AI allowances.
- No unattended paid review service, Copilot code-review policy, API secret, auto-reload, webhook, or new GitHub Actions step without **separate owner permission**, exact entitlement verification, permission audit, budget and a limited test repository.

GitHub Copilot code review and third-party partner agents are **different products** from an owner's manually authenticated Claude Code session. GitHub documents possible AI-credit charges and distinct policy/entitlement gates: [Copilot code review and billing](https://docs.github.com/en/copilot/concepts/agents/code-review). Enterprise Cloud alone does not make these reviews free.

## 7. Adoption and rollout checklist

- [x] Existing actual pilot evidence read and recorded; manual second opinion is useful under selected conditions.
- [x] The default operational path is **manual review with existing subscriptions**, no new infrastructure required.
- [x] **Owner approved** this manual architecture and SOP as an active internal operating standard on 2026-10-10. No Enterprise policy or App permission change is implied.
- [ ] Run one R1 and one R2 ordinary PR with a frozen packet, record reviewer time, accepted/falsified findings, CI delta and decision quality in each PR (without creating artificial work).
- [ ] Later, in a **separate security session**, verify Claude/Grok and publisher App permissions after the necessary authenticated owner access; consider reducing rights *only with a tested migration plan*.
- [ ] Consider auto-review **only if** evidence shows repeat workload and owner separately approves the costs, secrets, access and repository-specific rollout.

**Explicit non-goals of adopting this standard:** no Enterprise/GitHub setting changes, no rulesets, no branch-protection edits, no production receiver writes, no publication, no new model purchase, no new generic CI workflows, and no changes to product source files.
