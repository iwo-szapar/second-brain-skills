# Authoring skills

## Start from the decision, not a template

Capture five things before writing: the user outcome, realistic trigger language, non-goals, inputs and output contract, and authority boundary. A reusable skill must describe a procedure that is more reliable or efficient than ad-hoc prompting. Do not create one for generic advice or a one-off task.

Search the canonical root and global skill roots before authoring. Extend an owner skill when its scope already covers the work. If scopes differ, document the boundary in both descriptions rather than inventing a catch-all.

## Bundle shape

Start with `SKILL.md`. Add a resource only when it has a concrete job:

| Resource | Add when | Verify |
| --- | --- | --- |
| `scripts/` | repeated logic or deterministic checks materially improve reliability | executable test with representative and failing input |
| `references/` | a distinct mode needs detailed policy, schema, or procedure | entrypoint says exactly when to read it |
| `assets/` | output needs a source template, icon, font, or document | asset path and license/provenance are known |
| `agents/openai.yaml` | Codex/ChatGPT UI, dependencies, or policy need metadata | YAML matches the shared skill scope |

Avoid READMEs, change logs, copied manuals, placeholder directories, generic examples, and nested reference chains that do not alter execution.

## Write the entrypoint

Use imperative instructions. State the outcome, critical inputs, ordered decisions, verification, and recovery/stop condition only where they matter. Explain a non-obvious constraint rather than repeating generic cautions.

Keep descriptions short enough to survive skill-list truncation. Include the task, likely trigger words, and an exclusion only when it prevents a recurrent false positive. Put detailed procedure in the body because descriptions are discovery metadata, not an API catalogue.

For a shared skill, use portable frontmatter. Keep Claude-only fields out of `SKILL.md`; configure visibility in Claude settings. Keep Codex display/policy/dependencies in `agents/openai.yaml`.

## Definition of done

Every authored skill needs:

1. A named owner and canonical root.
2. An observable output or state transition.
3. A verification method that is harder to satisfy accidentally than the desired outcome.
4. Clear behavior for missing inputs, failed dependencies, and external authorization.
5. A regression case when it contains a script, evaluator, safety rule, or past failure repair.

For an `evals/evals.json` fixture, also prove that it parses, every case has a
stable ID and expected observable result, and each deterministic case is run
against the helper it claims to test. A skill-bundle validator cannot infer
whether an eval file is valid JSON or whether its examples actually exercise
the validator.
