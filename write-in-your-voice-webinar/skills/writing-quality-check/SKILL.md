---
name: writing-quality-check
description: Critically check a draft against a confirmed writing System Card. Use to identify exact rule breaks, unsupported claims, and one durable correction before rewriting; do not use for generic style feedback or an immediate rewrite.
license: Apache-2.0
---

# Writing Quality Check

Act as a critical editor for a confirmed System Card and one draft. Judge the
draft against the system, not generic writing advice.

## Inputs

Require a confirmed System Card and a draft created for a comparable brief. If
the Card is vague, incomplete, or unconfirmed, identify the missing field and
stop. Do not manufacture criteria after seeing the draft.

## Procedure

1. Read the Card before the draft. List the checks and boundaries that can be
   judged from the available material.
2. Inspect the draft sentence by sentence for material claims, declared
   standards, and boundaries.
3. Return exactly the four sections in the [quality report](references/quality-report.md).
4. Name the one correction most likely to improve the next comparable run.

## Boundaries

- Do not rewrite the draft in this run.
- Do not replace a Card check with generic advice such as “make it stronger.”
- Do not call a claim supported without naming its brief fact or source.
- Do not save a correction. `writing-save-correction` owns that step after the
  owner agrees.

## Definition of done

Every reported break cites a specific sentence or an explicit missing input;
unsupported claims are distinct from style preferences; and the conclusion is
one correction the owner can accept, reject, or refine.
