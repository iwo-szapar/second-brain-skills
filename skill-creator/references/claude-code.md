# Claude Code adapter

Use the project skill under `.claude/skills`. Claude-specific frontmatter is permitted only for a Claude-only bundle; do not add it to a shared repository core.

For client experiments, use a fresh non-interactive session, record `claude --version`, model, settings source, and raw JSON/stream output. Keep permissions narrow and run in an isolated temporary workspace. Test explicit invocation and implicit routing separately.

`allowed-tools` is a temporary pre-approval grant, not a tool restriction. Use Claude settings or `disallowed-tools` for restrictions in an intentionally Claude-only skill.

If a workflow has external effects, keep it discoverable unless the user expressly wants explicit-only invocation; require authorization at the actual mutation.
