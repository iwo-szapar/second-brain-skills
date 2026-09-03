# Evidence grading

Use this after a client run has completed. It converts assertions into an auditable pass or fail record; it does not decide whether a client run itself was healthy.

## Inputs

- The target skill's assertions and expected outcome
- The completed client's `run.json`, transcript, and output directory
- Any deterministic checker supplied by the target skill

## Procedure

1. Read `run.json`. If `execution_status` is not `COMPLETED`, record `INFRA_ERROR` or `NOT_RUN` and stop. Do not turn a timeout, authentication failure, malformed output, or missing client into a behavioral failure.
2. Inspect the relevant output files. Do not accept a transcript claim as proof when the output can be checked directly.
3. Run the target skill's deterministic checker when one exists. Prefer its result over a subjective interpretation.
4. Evaluate every assertion independently. Mark `PASS` only when the output supplies specific, substantive evidence. A correctly named but empty file is not a pass.
5. Record the assertion text, verdict, and a concise evidence citation. Separate unverified output claims from verified facts.
6. Identify one missing or weak assertion only when it would materially improve the corpus. Do not invent new requirements after seeing an output.

## Output

Write `grading.json` beside the evaluated run using the schema in [schemas](../schemas.md). Include an overall pass rate only for completed runs.

## Stop condition

Stop when every predefined assertion has a verdict with evidence, or report the exact missing artifact that prevents grading.
