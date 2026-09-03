# Second Brain Skills

Portable, privacy-safe skills for AI agents that help people build, maintain,
and use a second brain. Each directory is an independently installable skill
with one canonical `SKILL.md`, optional decision references, and host-specific
metadata only where needed.

The repository deliberately contains no private business data, credentials,
customer information, proprietary URLs, or hard-coded local paths. Configure
those details in the project where a skill is installed.

## Included skills

| Skill | What it does |
| --- | --- |
| [`skill-creator`](./skill-creator/) | Creates, improves, evaluates, and packages reusable agent skills. |
| [`seo`](./seo/) | Makes evidence-backed SEO decisions without publishing or changing a site. |

## Install

Clone this repository, then copy the skill you want into your project's skill root:

```bash
git clone https://github.com/iwo-szapar/second-brain-skills.git
mkdir -p .claude/skills
cp -R second-brain-skills/seo .claude/skills/
```

For Codex discovery in the same project, add a symlink to the installed skill:

```bash
mkdir -p .agents/skills
ln -s ../../.claude/skills/seo .agents/skills/seo
```

Use the same pattern for any other directory in this repository. The latest
packaged archives are available from the [releases page](https://github.com/iwo-szapar/second-brain-skills/releases/latest).

## Use it

Ask your agent to use the relevant skill when its trigger matches the task. For
example, use `skill-creator` to create or evaluate a reusable workflow, or
`seo` to assess a search opportunity, refresh, technical issue, or measurement
window.

## Validate a bundle

The included portable validator uses only the Python standard library:

```bash
python3 skill-creator/scripts/quick_validate.py seo --target portable
```


## Repository layout

```text
skill-creator/             # Skill-authoring workflow and portable tooling
seo/                       # Evidence-backed, read-only SEO decision layer
  SKILL.md                 # Portable entry point
  agents/openai.yaml       # Codex metadata only
  references/              # Decision and evidence contracts
  evals/                   # Regression fixtures
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Created and maintained by [Iwo Szapar](https://github.com/iwo-szapar).
