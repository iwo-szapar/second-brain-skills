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

Use the same pattern for any other directory in this repository. Release pages
list the packaged skill archives actually available for that version. To build
an archive from the current source, run:

```bash
python3 skill-creator/scripts/package_skill.py seo ./dist
```

Packaged archives include bundle files except root `evals/`, `__pycache__/`,
`node_modules/`, `*.pyc`, and `.DS_Store`. Evaluation corpora stay in the
source repository and are intentionally excluded from `.skill` archives.

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

This checks portable metadata, local links, Codex metadata, and the optional
`evals/evals.json` schema. It does not claim that model behavior has been
evaluated; behavioral runs must follow the evaluation contract in
`skill-creator/references/evaluation-contract.md`.

Run a corpus case through an installed client with:

```bash
python3 skill-creator/scripts/run_client_eval.py \
  --client codex \
  --workspace /path/to/empty-isolated-workspace \
  --skill-directory seo \
  --evals-file seo/evals/evals.json \
  --eval-id 1 \
  --output-dir /path/to/run/eval-1
```

## Repository layout

```text
skill-creator/             # Skill-authoring workflow and portable tooling
seo/                       # Evidence-backed, read-only SEO decision layer
  SKILL.md                 # Portable entry point
  agents/openai.yaml       # Codex metadata only
  references/              # Decision and evidence contracts
  evals/                   # Behavior evaluation corpus
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Created and maintained by [Iwo Szapar](https://github.com/iwo-szapar).
