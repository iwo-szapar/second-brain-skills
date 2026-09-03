# Evaluation contract

## Separate four questions

Do not collapse these into one pass rate:

1. **Routing:** Did the client select the skill for the right requests and avoid near-misses?
2. **Behavior:** With the skill loaded, did the completed output satisfy meaningful assertions?
3. **Cost:** What completed-run time, tokens, and tool use did it require?
4. **Infrastructure:** Did the client authenticate, parse output, and finish within bounds?

An infrastructure failure is never a negative behavioral observation. Record `PASS`, `FAIL`, `INFRA_ERROR`, or `NOT_RUN` per run. Exclude the latter two from behavior/cost aggregates and fail the experiment if their rate breaches the declared reliability threshold.

## Before running

Create an immutable corpus in the target skill's `evals/evals.json`, with stable case IDs, positive and negative routing cases, expected observable outcomes, assertion IDs, a corpus hash, and a snapshot/hash of the candidate and baseline. `skill-creator` intentionally has no fixed corpus because it creates and evaluates the corpus for the target skill. Record client, client version, model, command, permissions, timestamp, and run directory.

Use a baseline: no skill for a new capability; the pre-change snapshot for an improvement. Randomize A/B labels before blind qualitative comparison. Never show the grader which version produced an output.

## Evidence thresholds

For a consequential shared skill, run at least three cold repetitions per client and case. Report routing precision/recall, completed-case outcome rate, median and spread for cost, and infrastructure completion rate separately. Do not declare a gain from one run, a changed corpus, unknown model, or a result that only passes superficial assertions.

Use deterministic assertions whenever possible. LLM grading must cite the output evidence, critique weak assertions, and be treated as judgment—not ground truth. Preserve raw outputs and grader inputs beside the summary.

## Apply the evaluation roles

Use these guides only for the evaluation activity at hand. They are portable reference material, not configured subagents: perform the work inline or delegate it through the active host's native subagent mechanism.

- [Evidence grading](evaluation-roles/grading.md) — assess assertions against completed runs and record evidence.
- [Blind comparison](evaluation-roles/blind-comparison.md) — compare candidate and baseline outputs without knowing which is which.
- [Benchmark analysis](evaluation-roles/benchmark-analysis.md) — surface variance, non-discriminating assertions, and cost patterns from completed data.

Do not create a grade, comparison, or benchmark conclusion when the underlying client run is `INFRA_ERROR` or `NOT_RUN`.

## Iteration rule

For each iteration:

1. State the observed failure and the proposed general mechanism.
2. Apply one narrow change.
3. Re-run affected regression cases plus at least one held-out case.
4. Keep, revert, or mark inconclusive based on completed evidence.
5. Stop after the predeclared number of iterations or when an authority/cost boundary is reached.

Do not tune descriptions against the test set. Split routing corpora by case ID, retain a holdout, and never treat a timeout as a non-trigger.

Use `scripts/run_client_eval.py` to capture the actual Claude Code or Codex
command, client exit status, timing, stdout, and stderr in a `run.json`. It
does **not** grade quality: a `COMPLETED` run still needs deterministic
assertions and, where useful, a separate blind grader.
