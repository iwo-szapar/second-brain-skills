# Blind comparison

Use this when deciding whether a changed skill beats its baseline. Blindness prevents the evaluator from favoring the new version by default.

## Inputs

- Candidate and baseline outputs from the same prompt and input files
- The original task and predefined assertions
- A randomized mapping between the outputs and labels `A` and `B`

## Procedure

1. Verify both runs completed. Exclude any `INFRA_ERROR` or `NOT_RUN` pair rather than treating it as a loss.
2. Hide the mapping from the evaluator. Give it only labels `A` and `B`, the task, and the assertions.
3. Score task-relevant quality dimensions such as correctness, completeness, and usability. Define dimensions before looking for a winner.
4. Treat deterministic assertion results as evidence, not as the only decision rule. A broader qualitative judgment must cite the observable output difference.
5. Select `A`, `B`, or `TIE`. Reveal the mapping only after the result is recorded.
6. Preserve the labels, rubric, evidence, result, and mapping in the experiment record.

## Guardrails

- Do not compare outputs produced from different prompts, inputs, models, or permissions.
- Do not use a single subjective comparison as evidence of a general improvement.
- Do not claim a win when the comparison lacks sufficient evidence to distinguish the outputs.
