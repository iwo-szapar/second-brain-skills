# Claude and Codex portability

## Shared core

Repository skills use one canonical `SKILL.md` and the portable field intersection:

```yaml
name: kebab-case-name
description: What it does and when it applies.
license: Optional license identifier
allowed-tools: Optional portable tool declaration
metadata: Optional map for repository tooling
```

Keep the directory name equal to `name`. Require non-empty `name` and `description` even when one host can infer a directory command; this makes the bundle portable and easier to audit.

## Host-specific behavior

| Need | Put it here |
| --- | --- |
| Claude-only invocation, dynamic context, forked agents, or hooks | Claude settings or a documented Claude-only overlay |
| Codex display label, default prompt, dependencies, implicit policy | `agents/openai.yaml` |
| Local repository discovery | `.agents/skills` symlink to canonical source |
| Broader reusable distribution | A plugin, not a copied skill directory |

Do not place `disable-model-invocation`, `argument-hint`, `context`, `agent`, or Claude hooks in a shared core. A shared core with those fields will fail portable validation even if a particular client tolerates it.

## Roots and distribution

`.claude/skills` is canonical in this repository. `.agents/skills` and `.Codex/skills` must resolve to it. A global OpenAI system skill is vendor-managed: do not fork or overwrite it to customize repository behavior.

Use local installation only for personal experimentation. Use a plugin for organization or cross-product distribution. An imported third-party bundle must be staged, inspected, validated, provenance-pinned, and only then enabled.
