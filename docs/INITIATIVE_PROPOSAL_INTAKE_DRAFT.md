# Peaceful World — initiative proposal intake (draft, 2026-10-17)

**Decision status:** REVIEW ONLY. This document and accompanying `.github/ISSUE_TEMPLATE/initiative-proposal.yml` are in a draft pull request. Merging the PR would enable a public, GitHub-authenticated issue form. **No approval to activate intake, add site CTAs, recruit, fund or announce a programme has been given.**

## Why this is separate from volunteering

The already active `volunteer.yml` form offers a contribution to a bounded task. The proposed `initiative-proposal.yml` is an idea submitted for evaluation, not a task ready for assignment. Treat the two types differently.

- A person may browse `https://peaceful-world.org/projects` for verified programmes and current products.
- A volunteer can use the already public `volunteer.yml` path for an existing bounded contribution.
- A new idea would use this **proposed** form only after editorial approval and a separate decision to activate it.
- An unvalidated historical Peaceful World idea is **not** automatically a live or recruiting programme.

## Minimum fields

An appropriate proposal includes a purpose, a plain-language concept, one safe/testable next step, a basic ethics and privacy risk assessment, and any relevant public overlap. Potential roles and needed resources are optional.

The issue title, description and checklist are readable in English and Russian. The form does not ask for personal contact details, uploads or a payment. It requires acknowledgement that GitHub issues are public and submission does not imply organizational endorsement.

## Triage lifecycle — future operating model

1. **Submitted (unreviewed):** Public GitHub Issue; no automatic roadmap placement, product status, commitment, recruitment or fund-raising.
2. **Safety/privacy check:** Editorial reviewer considers the issue's personal data, retaliation risks, dehumanization, coercion, vulnerable participants, identity exposure and credibility. A security report must use the published security-policy route. Do not copy sensitive information to the Public Ledger.
3. **Duplicate and provenance check:** Link to a previously documented parent project, public research, suitable existing Issue, or historical idea when relevant. Treat documentation evidence separately from impact evidence.
4. **Decision:** Request clarification, mark as duplicate, decline with a respectful reason, keep as research, or nominate for a separately approved pilot. Triage outcomes are not Public Ledger milestones.
5. **Pilot authorization:** Only a separately approved and adequately owned project receives a lead, scope, safeguards, success/stop criteria, resources and a public build task (where appropriate). The public GitHub Build Board already ignores untriaged Issues without an explicit `<!-- board-status: ... -->` marker.
6. **Public status:** Use the private Peaceful World OS as internal authority; publish only approved `PUBLIC` entries via Public Ledger and the established website review/release route. Opening an Idea Issue alone never changes the official portfolio.

## Publication and safety boundaries

- GitHub is a **public** surface. Never invite sensitive stories, participant information, private third-party accusations, conflict-zone contacts, medical data or documents into a public Issue.
- This issue form has no private submission alternative. **Before linking it from the official site, decide how people without GitHub or with privacy-sensitive submissions can participate safely.** Do not improvise an unreviewed email or public form.
- No automatic fundraising, donation earmarking, project promotion, volunteer recruitment, status changes, notifications to third parties, or tagging of individuals.
- No auto-promotion to the Build Board or to a PUBLIC Ledger row.
- Review capacity, moderation responsibilities, and an escalation/abuse handling path need assignment before activation.
- Preserve nonviolent, dignity-respecting, trauma-informed and non-coercive participation language; avoid impact-washing.

## Release gates before an external CTA

- [ ] Founder approves opening public idea proposals as a service, including expected moderation capacity and acceptable scope.
- [ ] Human reviewer / accountable owner is assigned for triage and reports/abuse.
- [ ] Bilingual form text and issue-template rendering are verified.
- [ ] Consider spam/abuse moderation and privacy-safe non-GitHub alternative.
- [ ] If approved, merge this separate PR; confirm the form actually opens as an Issue in `peaceful-world-org/.github`. Do **not** submit an actual test Issue containing personal data.
- [ ] Only then prepare a **separate** `website-lab` PR adding a clearly worded `Suggest an idea` CTA with appropriate privacy and expectation copy to the staging catalogue.
- [ ] Verify stage and noindex first; production requires the normal owner approval and Release v2 path.

## Source boundaries

- Existing volunteer form: [volunteer.yml](../.github/ISSUE_TEMPLATE/volunteer.yml).
- [Public Work Model](../PUBLIC_WORK_MODEL.md) — public Issues as reviewed work, Board states not private OS states.
- [Volunteer guide](../VOLUNTEER.md) — bounded contributions and review before work is promoted.
- [Public Build Board workflow](../.github/workflows/public-build-board.yml) — untriaged Issues have no board-status marker and are deliberately ignored.
- Current website preview `initiatives-preview/` (source in `peaceful-world-org/website-lab`) is **non-production**, **noindex**, and has no proposal form or intake.
