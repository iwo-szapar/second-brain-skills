# Write in Your Voice webinar pack

This is a build-along pack for turning a small set of trusted writing into a
testable system for one recurring job. It is intentionally small: one job,
one source set, one fresh brief, and one approved correction.

## Install

Install all four skills in the order below, or install only the next skill you
need. Each skill is self-contained and can be copied to a project skill root.

```bash
cp -R write-in-your-voice-webinar/skills/* .claude/skills/
```

For Codex discovery, create the usual project-local `.agents/skills` symlinks
to the installed directories.

## The build order

1. [`writing-draft-contract`](./skills/writing-draft-contract/) turns approved
   examples into a Draft Contract. It does not write the final piece.
2. [`writing-blank-brief`](./skills/writing-blank-brief/) tests a confirmed
   System Card on a comparable new brief.
3. [`writing-quality-check`](./skills/writing-quality-check/) identifies exact
   passes, breaks, unsupported claims, and one high-value correction.
4. [`writing-save-correction`](./skills/writing-save-correction/) proposes a
   single durable rule change, waits for approval, then revises from the
   approved Card.

## Shared workshop references

- [System Card template](./system-card-template.md)
- [Fictional starter source pack](./starter-source-pack.md)

These examples are deliberately harmless and fictional. Use only material you
are permitted to keep in the AI account or local folder you choose. Do not add
credentials, client contracts, regulated data, or private company documents to
the workshop.

## What this pack does not do

It does not publish, send, schedule, connect a CRM, make a commercial promise,
or treat an AI-proposed rule as permanent. The owner confirms the System Card
and approves any correction.

After three comparable manual runs, use the repository's
[`skill-creator`](../skill-creator/) to decide whether the proven workflow
should become a more specialized skill.
