---
name: writing-save-correction
description: Turn one owner-approved writing correction into a testable System Card rule, then revise only after approval. Use after a Card-based quality check; do not use to silently rewrite permanent instructions or save unapproved preferences.
license: Apache-2.0
---

# Writing Save Correction

Preserve one useful correction without letting an AI silently change the
writing system. This skill has two runs: propose, then apply after explicit
owner approval.

## Inputs

Require a confirmed System Card, an exact correction, and the quality-check
evidence that motivated it. Run 2 additionally requires the original draft
and the exact fresh brief or approved fact list used for that draft. If the
correction is broad (“make it better”), ask for the exact behavior, evidence,
or failed sentence before proposing a rule.

## Run 1 — propose a change

1. Identify the one Card field affected by the correction.
2. Return the [correction proposal](references/correction-proposal.md): old
   rule, proposed new rule, pass test, failure test, and the evidence for the
   change.
3. State that the proposed rule is **not active** until the owner explicitly
   approves it.
4. Stop. Do not revise the draft or modify the Card in this run.

## Run 2 — apply an approved change

Only after the owner clearly approves the named proposed rule:

1. Replace only the approved Card field.
2. If the original draft and its fresh brief or approved fact list are present,
   revise the draft using the approved Card and approved source set. If they
   are absent, return only: `Card field changed: [field]. Draft revision: not
   performed. Missing: [brief or fact list].` Then stop; do not guess a
   revision or call it recheck-pending.
3. When a revision was made, return a short change map: `correction → changed
   sentence → remaining uncertainty`.
4. Mark a revised draft `recheck pending`. A change map is not an
   independent quality result; send the revision through `writing-quality-check`
   before calling it a pass.

## Boundaries

- Never treat silence, a request for options, or a generic “looks good” as
  approval.
- Never change unrelated Card fields.
- Do not publish, send, schedule, or claim the revised draft was used.
- Preserve known unknowns; do not resolve them with invented details.
- Do not call a revised draft a pass based only on its change map.

## Definition of done

Run 1 ends with one narrow, reviewable proposal and an explicit approval gate.
Run 2 ends with exactly one approved Card change. If its original evidence is
available, it also ends with a revised draft and a map of what changed and
remains uncertain; that revision remains recheck-pending until a separate
quality check is complete. Without original evidence, it ends with the required
no-revision stop instead.
