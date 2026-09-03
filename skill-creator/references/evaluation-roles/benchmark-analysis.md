# Benchmark analysis

Use this after completed runs have been aggregated. The goal is to explain patterns in the data, not to manufacture a recommendation.

## Inputs

- Completed `grading.json` records and run metadata
- The aggregate benchmark summary
- The target skill's corpus and baseline definition

## Procedure

1. Exclude `INFRA_ERROR` and `NOT_RUN` observations from quality and cost averages. Report their rate separately.
2. Find assertions that pass for both candidate and baseline. Mark them as non-discriminating candidates, not as proof the candidate has no value.
3. Find assertions that fail in every run. Distinguish a broken assertion, an unsupported capability, and a repeated implementation defect only when the evidence supports it.
4. Report variance and outliers in pass rate, elapsed time, token use, and tool calls. Do not hide a wide spread behind a mean.
5. Compare candidate and baseline on the same corpus. State the trade-off when quality, cost, or reliability move in opposite directions.
6. Give only evidence-backed next steps: keep, revert, or run a narrowly defined follow-up test.

## Output

Write concise observations that name the affected case, assertion, or metric. Separate facts from hypotheses and do not report a performance gain from incomplete or incomparable runs.
