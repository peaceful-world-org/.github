# Peaceful World — Enterprise activation plan

Status: **PROPOSED / awaiting owner review**  
Date: 2026-10-10  
Scope: GitHub Enterprise Cloud governing the existing `peaceful-world-org` organization.

## Objective

Use Enterprise as a shared governance and capacity layer for Peaceful World digital products, while preserving established production releases and avoiding unnecessary administration. The initial human user is the founder/director. **Subscription confirmation in Billing & Licensing is a separate verification step, not established by this document.**

## Existing architecture — preserve it

- `peaceful-world-org/website-lab`: source, scoped QA and staging for the website.
- `peaceful-world-org/peaceful-world.org`: generated-only public website release/Pages repository.
- `peaceful-world-org/5`: independent 5 Practice code, PWA and mobile release checks.
- Other products retain their own repositories, tests and release authority.
- The primary website's post-cutover Release Architecture v2 remains authoritative. Do **not** change the production domain, DNS, GitHub Pages routing, GitHub App publisher permissions or Release v2 signal branches as a side effect of Enterprise onboarding.
- The existing `website-lab` repository ruleset `Protect main` is active. Do not overwrite it with a generic enterprise-wide rule.

References: [Product Golden Path](PRODUCT_GOLDEN_PATH.md) · [Engineering Efficiency Standard](ENGINEERING_EFFICIENCY_STANDARD.md) · [AI Agent Operating Model](AI_AGENT_OPERATING_MODEL_V1.md) · [Public Work Model](PUBLIC_WORK_MODEL.md).

## Day-1 verification checklist (read-only first)

- [ ] **Enterprise ownership:** in Enterprise → Organizations confirm `peaceful-world-org` is the selected organization, retaining its existing repositories and permissions.
- [ ] **Seats:** in Billing & Licensing verify the actual paid seat count; reconcile external collaborators, automation accounts and any license-consuming principals before adding users.
- [ ] **Nonprofit terms:** verify the redeemed nonprofit discount, active paid plan, next invoice, tax treatment and renewal terms in the Enterprise billing UI; do not assume the coupon screen proves final invoice state.
- [ ] **Actions allowance:** verify the Enterprise Actions quota and usage period in Billing & Licensing; standard GitHub-hosted runners are counted separately from AI model/API consumption.
- [ ] **Budget continuity:** inspect all inherited Enterprise/organization/repository Actions budgets, especially the previous small Actions budget. Determine whether `Stop usage when budget limit is reached` is enabled before considering any update. Preserve an alerting budget without surprising stoppage.
- [ ] **Actions baseline:** inspect current workflow permissions and existing GitHub Apps; do not broaden default `GITHUB_TOKEN` permissions.
- [ ] **Current protection:** compare existing repository rulesets and environments before applying policies from the Enterprise level. Pilot, then roll out to additional repos.
- [ ] **Security/access:** review membership and two-factor-authentication policies; do not force a new SSO/SCIM setting or change authentication without a separately approved migration and lockout plan.
- [ ] **Member README:** publish a concise Enterprise README in the Enterprise Overview. The source draft is [here](ENTERPRISE_README_DRAFT.md); the Enterprise UI README is visible to members, while this public source contains no secrets.
- [ ] **Baseline record:** record verified owner, date, scope and screenshots/links in a private operating record; never publish invoice details, secret names/values or personal data in a public issue.

## Guardrails for the production approval pilot

`website-lab/.github/workflows/release-production-v2.yml` currently attaches `environment: production` to its `release-candidate` job **for every invocation mode**, including dry-run.

Do **not** simply add an Enterprise required reviewer to that environment: doing so would block non-publishing validation as well.

Pilot plan (separate architecture PR and explicit owner decision):

1. Inspect the current Release v2 workflows, environment rules and required checks.
2. Ensure non-publishing `dry-run` and `test-publish` paths remain unblocked and unchanged.
3. Test a protected production-only approval gate on an isolated, non-publishing validation path.
4. For a single human owner, ensure self-review is permitted **if** GitHub permits the intended approval flow; otherwise keep the existing one-action chat-native gate.
5. Confirm exactly one meaningful approval, immutable artifact, publisher app, live verification and fallback; only then roll out to the real environment.
6. Do not introduce two independent approvals or a bypass that weakens authorization.

Until successfully validated, keep Release Architecture v2 unchanged.

## Agent adoption without extra license assumptions

Start with humans orchestrating existing connected assistants. GitHub Enterprise does **not** automatically provide API allowances or GitHub Copilot licenses for Codex, Claude, Gemini or Grok.

Phase 1: Codex prepares small PRs; Claude reviews relevant implementation and reasoning; Gemini assists translations with factual verification; Grok can act as an optional adversarial reviewer. Verify all conclusions independently and in CI.

Phase 2: once the owner explicitly authorizes external model/API use, test low-privilege read-only automated review on **one** non-sensitive repository and a single PR. Measure latency, model cost, failure modes, and data access.

Phase 3: only after a successful pilot, integrate reusable checks into other products and add an agent work queue, while retaining owner control for releases, money, identity, public outreach and sensitive content.

## Done means

A verified enterprise billing and license baseline; a healthy, unchanged production pipeline; a documented approval pilot (not an unreviewed gate change); a concise Enterprise README; and a useful, reviewable multi-agent operating model. Creating the enterprise account alone does not satisfy these checks.
