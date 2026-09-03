---
name: skill-creator
description: Create, improve, evaluate, or align repository skills. Use for a new reusable agent workflow, a quick skill scaffold, an existing SKILL.md that needs repair or evaluation, Claude/Codex skill portability, or duplicate skill-root drift. Do not use to import a third-party skill; use the installer or plugin workflow instead.
license: Apache-2.0
---

# Skill Creator

Own the complete lifecycle of repository skills: quick scaffolding, deliberate authoring, repair, evaluation, and Claude/Codex alignment. The canonical source is `.claude/skills`; `.agents/skills` and `.Codex/skills` are compatibility bridges.

## Choose a mode

| Request | Mode | Read next |
| --- | --- | --- |
| Create a small, clear workflow quickly | `quick` | [authoring](references/authoring.md) |
| Create or substantially redesign a skill | `create` | [authoring](references/authoring.md), then [evaluation contract](references/evaluation-contract.md) when risk warrants it |
| Fix, simplify, or extend an existing bundle | `improve` | [authoring](references/authoring.md) |
| Test routing, outputs, regressions, or cost | `evaluate` | [evaluation contract](references/evaluation-contract.md) |
| Resolve Claude/Codex duplication or portability | `align` | [portability](references/portability.md) |
| Package or distribute beyond this repository | `package` | [portability](references/portability.md) |

Use `quick` by default for a clear, low-risk request. Use `create` when ambiguity, side effects, scripts, customer data, external systems, or a reused team workflow make a design/evidence pass worthwhile.

## Non-negotiable checks

1. Find the existing owner before creating anything. Extend it if it already covers the work.
2. Preserve authorization boundaries. A skill may prepare a mutation, but require approval immediately before a consequential external action.
3. Use one canonical body. Do not create separate Claude and Codex copies.
4. Default shared `SKILL.md` frontmatter to portable fields: `name`, `description`, `license`, `allowed-tools`, and `metadata`. Put Codex UI/policy in `agents/openai.yaml`; use Claude settings for Claude-only visibility. `agents/openai.yaml` is metadata, not a runnable agent. Do not place agent prompts in a skill's `agents/` directory; define and explicitly wire host-specific subagents outside the portable skill only when they have a real execution role.
5. Add scripts only for repeated logic or a meaningful deterministic reliability gain. Add references only when they change decisions in a distinct mode.
6. Validate every changed bundle with:

   ```bash
   python3 path/to/skill-creator/scripts/quick_validate.py <skill-dir> --target portable
   ```

   Run the host repository's own skill-parity check too, when it provides one.

7. Do not report behavior metrics when a client timed out, was unauthenticated, or emitted malformed output. Those are `INFRA_ERROR`, not failures.

## Canonical root and compatibility

Keep one canonical copy in the active repository. A common layout is:

```text
.claude/skills/<name>/       canonical source
.agents/skills/<name>        symlink bridge for Codex discovery
.Codex/skills/<name>         optional legacy compatibility bridge
```

Inspect all files in an existing bundle—scripts, references, assets, evals, and metadata—before changing it. Run the host repository's skill-parity check after changing a bridge, skill, rule, knowledge, or documentation surface.

`skills-generator` is a deprecated compatibility alias. Do not use it for new work; use this skill in `quick` mode.

## Quick workflow

1. Capture the outcome, realistic trigger phrases, non-goals, inputs, output contract, and side effects from the request. Ask only for information that changes the result.
2. Search canonical and global roots for an owner. If an owner exists, improve it instead of creating an overlap.
3. Create the smallest useful bundle. Start with `SKILL.md`; add a script, reference, template, or asset only with a stated use.
4. Write a concise, discriminating description. Front-load the actual task and likely user wording; add exclusions only to prevent likely misrouting.
5. Define a concrete definition of done: observable result, verification command or inspection, failure handling, and stop condition.
6. Validate the bundle and bridge it through the repository parity checker. If it has `evals/evals.json`, parse it and run every deterministic case; structural skill validation alone does not validate eval fixtures.
7. For consequential or complex skills, run the evaluation contract before claiming readiness.

## Improve workflow

1. Baseline the current behavior before changing instructions. Preserve the prior bundle hash and test corpus.
2. Inspect failures for their real category: routing, instruction clarity, missing deterministic helper, unsafe authorization, evaluator weakness, or client infrastructure.
3. Make the narrowest generalizable change. Do not encode one example as a universal rule.
4. Re-run the affected deterministic and behavioral cases. Keep an improvement only if the evidence improves or preserves the relevant outcome.

## Definition of done

A project skill is done when:

- One canonical owner exists and bridges resolve to it.
- Its portable frontmatter and referenced files validate.
- Its description states what it does, when it applies, and a useful boundary.
- Its instructions specify inputs, outcome, verification, and safe failure/stop behavior where relevant.
- Added scripts and evaluators have regression tests.
- Claimed routing or quality gains are backed by completed client runs with recorded client/model/version, corpus hash, and evidence paths.

## Runtime adapters

Read only the adapter for the active client when executing or testing workflows:

- [Claude Code adapter](references/claude-code.md)
- [Codex adapter](references/codex.md)

## Supporting references

- [Authoring](references/authoring.md) — structure, scope, and implementation guidance.
- [Evaluation contract](references/evaluation-contract.md) — real-client experiments, baselines, portable evaluation roles, and reporting.
- [Portability](references/portability.md) — shared core, runtime-specific metadata, plugins, and installation.
- [Security](references/security.md) — safe scripts, untrusted bundles, and viewer constraints.
- [Schemas](references/schemas.md) — artifact contracts for legacy and benchmark tooling.
