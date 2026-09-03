#!/usr/bin/env python3
"""Validate a skill bundle without confusing structure with behavior quality."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


PORTABLE_FIELDS = {"name", "description", "license", "allowed-tools", "metadata"}
CLAUDE_CODE_FIELDS = PORTABLE_FIELDS | {
    "compatibility", "argument-hint", "disable-model-invocation", "user-invocable",
    "disallowed-tools", "model", "effort", "context", "agent", "background",
    "hooks", "paths", "shell",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
TODO_PATTERN = re.compile(r"\[TODO\]|\[REPLACE\]|\[INSERT\]|\{\{[A-Z_]+\}\}")


class YamlParseError(ValueError):
    """The stdlib-only YAML subset parser found invalid or unsupported input."""


def _yaml_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if value.startswith(("'", '"')):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise YamlParseError(f"invalid quoted scalar: {value}") from exc
    if value.startswith(("[", "{", "|", ">", "&", "*", "!")):
        raise YamlParseError("unsupported YAML scalar; use a plain or quoted value")
    return value


def _yaml_load(text: str) -> dict[str, Any]:
    """Parse the portable skill metadata subset without a PyYAML dependency."""
    lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for index, raw_line in enumerate(lines):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise YamlParseError("tabs are not supported for indentation")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        content = raw_line.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if content.startswith("- "):
            if not isinstance(parent, list):
                raise YamlParseError(f"list item without a list parent on line {index + 1}")
            parent.append(_yaml_scalar(content[2:]))
            continue

        if ":" not in content or not isinstance(parent, dict):
            raise YamlParseError(f"expected a mapping entry on line {index + 1}")
        key, raw_value = content.split(":", 1)
        key = key.strip()
        if not key or key.startswith(("'", '"')):
            raise YamlParseError(f"unsupported mapping key on line {index + 1}")
        if key in parent:
            raise YamlParseError(f"duplicate mapping key '{key}'")
        if raw_value.strip():
            parent[key] = _yaml_scalar(raw_value)
            continue

        child_is_list = False
        for future in lines[index + 1:]:
            if not future.strip() or future.lstrip().startswith("#"):
                continue
            future_indent = len(future) - len(future.lstrip(" "))
            if future_indent <= indent:
                break
            child_is_list = future.strip().startswith("- ")
            break
        child: Any = [] if child_is_list else {}
        parent[key] = child
        stack.append((indent, child))
    return root


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _read_frontmatter(skill_md: Path) -> tuple[dict[str, Any], str]:
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with a closed YAML frontmatter block")
    loaded = _yaml_load(match.group(1))
    if not isinstance(loaded, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return loaded, match.group(2)


def _validate_openai_yaml(skill_root: Path, errors: list[str]) -> None:
    metadata_path = skill_root / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return
    try:
        data = _yaml_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, YamlParseError) as exc:
        errors.append(f"agents/openai.yaml is invalid YAML: {exc}")
        return
    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml requires an interface mapping")
        return
    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"agents/openai.yaml interface.{field} must be a non-empty string")
    policy = data.get("policy")
    if policy is not None and (
        not isinstance(policy, dict)
        or not isinstance(policy.get("allow_implicit_invocation"), bool)
    ):
        errors.append("agents/openai.yaml policy.allow_implicit_invocation must be a boolean")


def _validate_bundle_paths(skill_root: Path, body: str, errors: list[str]) -> None:
    resolved_root = skill_root.resolve()
    for path in skill_root.rglob("*"):
        if path.is_symlink():
            try:
                target = path.resolve(strict=True)
            except FileNotFoundError:
                errors.append(f"broken symlink: {path.relative_to(skill_root)}")
                continue
            if not _inside(resolved_root, target):
                errors.append(f"symlink escapes skill directory: {path.relative_to(skill_root)}")
    for raw_target in MARKDOWN_LINK_PATTERN.findall(body):
        target = raw_target.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "/")):
            continue
        linked = (skill_root / target).resolve()
        if not _inside(resolved_root, linked):
            errors.append(f"relative link escapes skill directory: {raw_target}")
        elif not linked.exists():
            errors.append(f"missing linked file: {raw_target}")


def validate_skill(skill_path: str, target: str = "portable") -> tuple[bool, str]:
    skill_root = Path(skill_path)
    errors: list[str] = []
    if target not in {"portable", "claude-code", "codex"}:
        return False, f"Unknown target: {target}"
    if not skill_root.is_dir():
        return False, f"Not a directory: {skill_path}"
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        return False, f"Missing SKILL.md in {skill_path}"
    try:
        frontmatter, body = _read_frontmatter(skill_md)
    except (OSError, ValueError, YamlParseError) as exc:
        return False, str(exc)

    allowed_fields = CLAUDE_CODE_FIELDS if target == "claude-code" else PORTABLE_FIELDS
    unexpected = sorted(set(frontmatter) - allowed_fields)
    if unexpected:
        errors.append(f"unsupported {target} frontmatter fields: {', '.join(unexpected)}")
    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("missing required frontmatter field: name")
    elif not NAME_PATTERN.fullmatch(name):
        errors.append("name must be lowercase kebab-case")
    elif len(name) > 64:
        errors.append("name must be 64 characters or fewer")
    elif name != skill_root.name:
        errors.append(f"name '{name}' must match directory '{skill_root.name}'")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("missing required frontmatter field: description")
    elif len(description) > 1024:
        errors.append("description must be 1024 characters or fewer")
    elif "<" in description or ">" in description:
        errors.append("description must not contain angle brackets")
    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append("metadata must be a YAML mapping")
    if target == "claude-code":
        for field in ("disable-model-invocation", "user-invocable"):
            if field in frontmatter and not isinstance(frontmatter[field], bool):
                errors.append(f"{field} must be a boolean")
        if frontmatter.get("context") == "fork" and not isinstance(frontmatter.get("agent"), str):
            errors.append("context: fork requires an agent name")
    if TODO_PATTERN.search(_strip_fenced_code(body)):
        errors.append("unresolved template placeholder outside a code block")
    _validate_bundle_paths(skill_root, body, errors)
    if target in {"portable", "codex"}:
        _validate_openai_yaml(skill_root, errors)
    if errors:
        return False, "\n".join(f"- {error}" for error in errors)
    return True, f"Skill is valid for {target}: {skill_root}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("--target", choices=("portable", "claude-code", "codex"), default="portable")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    valid, message = validate_skill(args.skill_directory, target=args.target)
    if args.as_json:
        print(json.dumps({"valid": valid, "target": args.target, "message": message}))
    else:
        print(message)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
