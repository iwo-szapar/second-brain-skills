---
name: writing-quality-check
description: Critically check a draft against a confirmed writing System Card. Use to identify exact rule breaks, unsupported claims, and one durable correction before rewriting; do not use for generic style feedback or an immediate rewrite.
license: Apache-2.0
---

# Writing Quality Check

Act as a critical editor for a confirmed System Card and one draft. Judge the
draft against the system, not generic writing advice.

## Inputs

Require all of the following:

1. A confirmed System Card.
2. A draft created for a comparable brief.
3. The exact fresh brief, or an approved fact list that was used to create the
   draft.

If the Card is vague, incomplete, or unconfirmed, identify the missing field
and stop. If the fresh brief or approved facts are absent, stop: the checker
cannot verify a material claim from the draft alone. Do not manufacture
criteria after seeing the draft.

### Required-input stop

When any required input is absent, return only this short stop response:

```text
Cannot run the Card-based quality check yet.
Missing: [named Card field, fresh brief, or approved fact list].
Needed next: [exact file or owner decision].
```

Do not return the four-section report, a pass/fail judgment about the draft,
a correction, or a rewrite. The report format applies only after all required
inputs are present.

## Procedure

1. Gate the required inputs. Use the required-input stop if any are missing.
2. Read the Card and fresh brief before the draft. List the checks and
   boundaries that can be judged from the available material.
3. Inspect the draft sentence by sentence for material claims, declared
   standards, and boundaries. Compare every claimed fact with the brief or an
   approved Card source.
4. Return exactly the four sections in the [quality report](references/quality-report.md).
5. Name the one correction most likely to improve the next comparable run.

## Boundaries

- Do not rewrite the draft in this run.
- Do not replace a Card check with generic advice such as “make it stronger.”
- Do not call a claim supported without naming its exact brief fact or source.
- Do not save a correction. `writing-save-correction` owns that step after the
  owner agrees.

## Definition of done

Every reported break cites a specific sentence or an explicit missing input;
unsupported claims are distinct from style preferences; and the conclusion is
one correction the owner can accept, reject, or refine.
