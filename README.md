# Skill Creator

A practical workflow for creating, improving, evaluating, and packaging AI agent skills.

Skills are reusable operating guides for an AI agent. They become useful when they define a real job, clear boundaries, an observable result, and a way to verify it. This repository contains the workflow I use to design those guides for Claude Code and Codex.

## What it helps with

- Starting a small, focused skill without building a framework around it
- Improving an existing skill by finding the actual failure mode first
- Keeping Claude Code and Codex on one portable skill definition
- Testing routing, output quality, and cost without mistaking infrastructure errors for failures
- Packaging a skill for reuse outside one repository

The skill keeps the work intentionally small. Add scripts when they create a real reliability gain. Add references when they change a decision. Keep one canonical `SKILL.md` instead of maintaining separate copies for each agent host.

## Install

Clone this repository, then place the `skill-creator` directory in your project's Claude skill root:

```bash
git clone https://github.com/iwo-szapar/skill-creator.git
mkdir -p .claude/skills
cp -R skill-creator/skill-creator .claude/skills/
```

For Codex discovery in the same project, add a symlink:

```bash
mkdir -p .agents/skills
ln -s ../../.claude/skills/skill-creator .agents/skills/skill-creator
```

The latest packaged archive is available from the [releases page](https://github.com/iwo-szapar/skill-creator/releases/latest).

## Use it

Ask your agent to use `skill-creator` when you want to create a reusable workflow, repair a `SKILL.md`, evaluate a skill, align Claude and Codex copies, or package a skill for sharing.

The entry point chooses one of six modes: `quick`, `create`, `improve`, `evaluate`, `align`, or `package`. It then points to the smallest supporting reference needed for that job.

## Validate a bundle

The portable validator uses only the Python standard library:

```bash
python3 skill-creator/scripts/quick_validate.py skill-creator
```

For consequential skills, use the evaluation contract before claiming a quality or routing improvement. It separates completed behavior from authentication, timeout, and parser failures so the resulting evidence remains useful.

## Repository layout

```text
skill-creator/
  SKILL.md                 # Entry point and workflow
  agents/openai.yaml       # Codex metadata only, not a runnable agent
  references/              # Authoring, portability, safety, and evaluation guidance
  scripts/                 # Validation, packaging, and evaluation helpers
  assets/                  # Review-page template
  eval-viewer/             # Local results viewer
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Created and maintained by [Iwo Szapar](https://github.com/iwo-szapar).
