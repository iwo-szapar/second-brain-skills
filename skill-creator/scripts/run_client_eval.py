#!/usr/bin/env python3
"""Run one skill-evaluation prompt with a real Claude Code or Codex client.

This records execution health separately from quality grading. A successful
client exit means only that the run completed; deterministic assertions and a
separate grader decide whether the output is correct.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath


def command_for(client: str, prompt: str, workspace: Path) -> list[str]:
    if client == "claude":
        return [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "json",
            "--no-session-persistence",
            "--permission-mode",
            "acceptEdits",
        ]
    if client == "codex":
        return [
            "codex",
            "exec",
            "--json",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "-C",
            str(workspace),
            prompt,
        ]
    raise ValueError(f"Unknown client: {client}")


def client_version(client: str) -> str | None:
    try:
        completed = subprocess.run(
            [client, "--version"], text=True, capture_output=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    version = (completed.stdout or completed.stderr).strip()
    return version or None


def prompt_from_eval_file(evals_file: Path, eval_id: int) -> str:
    prompt, _ = eval_case_from_file(evals_file, eval_id)
    return prompt


def eval_case_from_file(
    evals_file: Path, eval_id: int, expected_skill_name: str | None = None
) -> tuple[str, list[str]]:
    data = json.loads(evals_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("eval file must contain a JSON object")
    if expected_skill_name is not None and data.get("skill_name") != expected_skill_name:
        raise ValueError("eval file skill_name must match --skill-directory")
    cases = data.get("evals")
    if not isinstance(cases, list):
        raise ValueError("eval file requires an evals list")
    for case in cases:
        if isinstance(case, dict) and case.get("id") == eval_id:
            prompt = case.get("prompt")
            if isinstance(prompt, str) and prompt.strip():
                files = case.get("files", [])
                if not isinstance(files, list) or not all(
                    isinstance(item, str) for item in files
                ):
                    raise ValueError(f"eval {eval_id} files must be relative paths")
                if any(
                    Path(item).is_absolute()
                    or PureWindowsPath(item).is_absolute()
                    or not item
                    or any(
                        part in {"", ".", ".."}
                        for part in item.replace("\\", "/").split("/")
                    )
                    for item in files
                ):
                    raise ValueError(f"eval {eval_id} files must be relative paths")
                return prompt, files
            raise ValueError(f"eval {eval_id} has no non-empty prompt")
    raise ValueError(f"eval {eval_id} was not found")


def stage_skill(
    skill_directory: Path, workspace: Path, client: str, fixture_paths: list[str]
) -> Path:
    if skill_directory.is_symlink():
        raise ValueError("candidate skill root must not be a symlink")
    if workspace.is_symlink():
        raise ValueError("workspace root must not be a symlink")
    skill_directory = skill_directory.resolve()
    workspace = workspace.resolve()
    if not skill_directory.is_dir():
        raise ValueError(f"skill directory does not exist: {skill_directory}")
    for source_path in skill_directory.rglob("*"):
        if source_path.is_symlink():
            raise ValueError(
                "candidate skill contains a symlink: "
                f"{source_path.relative_to(skill_directory)}"
            )
        if not source_path.is_dir() and not source_path.is_file():
            raise ValueError(
                "candidate skill contains a non-regular path: "
                f"{source_path.relative_to(skill_directory)}"
            )
        try:
            source_path.resolve().relative_to(skill_directory)
        except ValueError as exc:
            raise ValueError(
                "candidate path escapes skill directory: "
                f"{source_path.relative_to(skill_directory)}"
            ) from exc
    host_root = ".claude" if client == "claude" else ".agents"
    host_skills = workspace / host_root / "skills"
    for parent in (workspace / host_root, host_skills):
        if parent.is_symlink():
            raise ValueError(f"workspace staging path must not be a symlink: {parent}")
    destination = host_skills / skill_directory.name
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"skill destination already exists: {destination}")
    host_skills.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        skill_directory,
        destination,
        ignore=shutil.ignore_patterns("evals", "__pycache__", "*.pyc"),
    )

    resolved_skill = skill_directory.resolve()
    resolved_workspace = workspace
    for raw_path in fixture_paths:
        source = (skill_directory / raw_path).resolve()
        try:
            source.relative_to(resolved_skill)
        except ValueError as exc:
            raise ValueError(f"fixture escapes skill directory: {raw_path}") from exc
        if not source.is_file():
            raise ValueError(f"fixture does not exist: {raw_path}")
        fixture_destination = (resolved_workspace / raw_path).resolve()
        try:
            fixture_destination.relative_to(resolved_workspace)
        except ValueError as exc:
            raise ValueError(f"fixture destination escapes workspace: {raw_path}") from exc
        fixture_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, fixture_destination)
    return destination


def write_run_record(
    output_dir: Path,
    client: str,
    version: str | None,
    command: list[str],
    started_at: datetime,
    duration_seconds: float,
    returncode: int | None,
    execution_status: str,
    failure_reason: str | None,
    stdout: str,
    stderr: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "stdout.log").write_text(stdout, encoding="utf-8")
    (output_dir / "stderr.log").write_text(stderr, encoding="utf-8")
    record = {
        "client": client,
        "client_version": version,
        "command": command,
        "started_at": started_at.isoformat(),
        "duration_seconds": round(duration_seconds, 3),
        "returncode": returncode,
        "execution_status": execution_status,
        "failure_reason": failure_reason,
        "stdout": "stdout.log",
        "stderr": "stderr.log",
    }
    (output_dir / "run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("claude", "codex"), required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--evals-file", type=Path)
    parser.add_argument("--eval-id", type=int)
    parser.add_argument("--skill-directory", type=Path)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.prompt is not None and (args.evals_file is not None or args.eval_id is not None):
        parser.error("use --prompt or --evals-file with --eval-id, not both")
    if args.prompt is None and (args.evals_file is None or args.eval_id is None):
        parser.error("provide --prompt or both --evals-file and --eval-id")
    if args.evals_file is not None and args.skill_directory is None:
        parser.error("--evals-file requires --skill-directory")
    fixture_paths: list[str] = []
    if args.prompt is None:
        try:
            prompt, fixture_paths = eval_case_from_file(
                args.evals_file.resolve(),
                args.eval_id,
                args.skill_directory.name,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            parser.error(str(exc))
    else:
        prompt = args.prompt

    if args.workspace.is_symlink():
        parser.error("workspace root must not be a symlink")
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")
    if not shutil.which(args.client):
        parser.error(f"{args.client} is not installed or on PATH")

    if args.skill_directory is not None and not args.dry_run:
        try:
            stage_skill(args.skill_directory, workspace, args.client, fixture_paths)
        except (OSError, ValueError) as exc:
            parser.error(str(exc))

    if fixture_paths:
        prompt += "\n\nInput files are staged in the workspace at: " + ", ".join(
            fixture_paths
        )

    command = command_for(args.client, prompt, workspace)
    if args.dry_run:
        print(json.dumps(command))
        return 0

    started_at = datetime.now(timezone.utc)
    version = client_version(args.client)
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            text=True,
            capture_output=True,
            timeout=args.timeout_seconds,
            check=False,
        )
        duration = time.monotonic() - started
        status = "COMPLETED" if completed.returncode == 0 else "INFRA_ERROR"
        reason = None if status == "COMPLETED" else f"client exited {completed.returncode}"
        write_run_record(
            args.output_dir, args.client, version, command, started_at, duration,
            completed.returncode, status, reason, completed.stdout, completed.stderr,
        )
        print(f"{status}: {args.output_dir / 'run.json'}")
        return 0 if status == "COMPLETED" else 1
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        write_run_record(
            args.output_dir, args.client, version, command, started_at, duration,
            None, "INFRA_ERROR", f"timed out after {args.timeout_seconds}s",
            exc.stdout or "", exc.stderr or "",
        )
        print(f"INFRA_ERROR: {args.output_dir / 'run.json'}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
