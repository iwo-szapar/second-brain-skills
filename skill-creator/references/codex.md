# Codex adapter

Codex discovers repository skills through `.agents/skills` and follows the canonical symlink target. Use `agents/openai.yaml` for display metadata, dependencies, and Codex implicit-invocation policy.

For experiments, use a fresh `codex exec` session in an isolated workspace. Record `codex --version`, model, sandbox/approval configuration, raw JSONL, and final message. Test explicit `$skill-name` invocation and implicit matching separately.

Do not assume that a same-named OpenAI system skill and repository skill merge. Make project UI metadata distinct and test the selected path. Do not modify the bundled system skill; it can change with product updates.
