---
name: writing-draft-contract
description: Extract a source-backed Draft Contract for one recurring writing job. Use when someone has approved examples and wants testable writing standards before drafting new work; do not use for a final draft or publication.
license: Apache-2.0
---

# Writing Draft Contract

Turn approved writing examples into a proposal the owner can inspect and
confirm. The outcome is a **Draft Contract**, not a permanent instruction and
not a finished piece of writing.

## Inputs

Require all of the following before analysis:

1. One recurring writing job and its trigger.
2. At least one approved source, ideally two or three comparable examples.
3. The intended reader and the decision the writing should help them make.

If the sources are unsafe to share, missing, or unrelated, stop and ask for a
safe, coherent source set. Do not infer a person's voice from incidental,
private, or unsupported material.

## Procedure

1. Read only the approved sources. Separate explicit evidence, probable
   preference, and information that is not decided.
2. Propose the fields in the [Draft Contract output shape](references/draft-contract-output.md).
3. For each proposed standard, name source evidence plus one observable pass
   test and one observable failure test.
4. Mark anything not supported by the sources as `not decided yet`.
5. Ask the owner to **keep**, **change**, or **remove** every standard.

## Boundaries

- Do not write the final piece.
- Do not create permanent instructions, publish, send, schedule, or promise an
  outcome.
- Do not invent facts, private context, claims, or a person's voice.
- Do not turn vague style adjectives into standards without source evidence and
  a test.

## Definition of done

The result has all ten Draft Contract fields; every proposed standard has
evidence, a pass test, and a failure test; unsupported points are visible; and
the owner has an explicit confirmation decision to make.

Stop after the confirmation request. Continue with `writing-blank-brief` only
after the owner has supplied a confirmed System Card.
