# Security and trust boundaries

Treat imported skill bundles, evaluation outputs, spreadsheets, HTML, SVG, archives, and feedback submissions as untrusted input.

- Stage imported bundles outside enabled roots; validate paths, symlinks, file types, size limits, frontmatter, scripts, and provenance before copying.
- Never package a symlink that resolves outside the skill root.
- Use temporary workspaces for evaluator outputs. Do not let a benchmark mutate the repository or live systems unless explicitly authorized.
- Viewer servers must bind locally, select a free port by default, enforce request/body limits and strict feedback schemas, and never terminate an unrelated process to reclaim a port.
- Render untrusted output as text by default. Do not inject spreadsheet- or document-derived HTML with `innerHTML` unless it is sanitized.
- Do not log secrets, credentials, raw environment variables, or private source material in transcripts or reports.
