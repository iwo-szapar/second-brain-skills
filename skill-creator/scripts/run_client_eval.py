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
from pathlib import Path


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
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")
    if not shutil.which(args.client):
        parser.error(f"{args.client} is not installed or on PATH")

    command = command_for(args.client, args.prompt, workspace)
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
