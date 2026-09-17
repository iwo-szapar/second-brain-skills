---
name: writing-blank-brief
description: Test a confirmed writing System Card on a comparable new brief. Use after an owner has confirmed standards and wants a traceable draft; do not use to extract standards, publish, or fill missing facts with guesses.
license: Apache-2.0
---

# Writing Blank Brief

Test a confirmed System Card against new work. The outcome is a reviewable
draft plus proof of how it followed the Card.

## Inputs

Require:

1. A confirmed System Card, including approved sources, checks, and boundaries.
2. A comparable new brief of two to four sentences.
3. Any facts or claims that need source support.

If the Card is still a proposal, missing its owner confirmation, or lacks a
reader and decision, stop and send the owner back to `writing-draft-contract`.

## Procedure

1. Restate the requested artifact, reader, decision, allowed facts, and known
   gaps before drafting.
2. Draft only from the new brief and the Card's approved source set.
3. Mark missing information and assumptions clearly rather than smoothing them
   into plausible detail.
4. Add the [Output-to-Card map](references/output-to-card-map.md) after the
   draft.

## Boundaries

- Do not publish, send, schedule, or claim an outcome happened.
- Do not use facts outside the brief or approved source set.
- Do not silently change a confirmed Card while drafting.
- Do not pretend a pass/fail check passed when evidence is missing.

## Definition of done

The requested draft is present, material claims can be traced, the Card's
checks have an explicit pass/fail status, and the owner can see the next
decision needed before use.

Send the result to `writing-quality-check` before changing the Card again.
