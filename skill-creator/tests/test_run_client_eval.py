from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_client_eval import (
    command_for,
    eval_case_from_file,
    prompt_from_eval_file,
    stage_skill,
)


class CodexCommandTest(unittest.TestCase):
    def test_temporary_workspace_does_not_require_a_git_repository(self) -> None:
        workspace = Path("/tmp/example-eval-workspace")

        command = command_for("codex", "Run this evaluation.", workspace)

        self.assertIn("--skip-git-repo-check", command)
        self.assertEqual(command[-1], "Run this evaluation.")

    def test_loads_prompt_from_documented_eval_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evals_file = Path(temporary) / "evals.json"
            evals_file.write_text(json.dumps({
                "skill_name": "example-skill",
                "evals": [{
                    "id": 7,
                    "prompt": "Run case seven.",
                    "expected_output": "A result.",
                    "expectations": ["The result is present."],
                }],
            }), encoding="utf-8")

            prompt = prompt_from_eval_file(evals_file, 7)

        self.assertEqual(prompt, "Run case seven.")

    def test_stages_candidate_without_eval_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            (skill / "evals").mkdir()
            (skill / "evals" / "evals.json").write_text("{}", encoding="utf-8")
            (skill / "evals" / "sample.txt").write_text("fixture", encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()

            destination = stage_skill(skill, workspace, "codex", ["evals/sample.txt"])

            self.assertEqual(
                destination,
                workspace.resolve() / ".agents/skills/example-skill",
            )
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertFalse((destination / "evals").exists())
            self.assertEqual(
                (workspace / "evals/sample.txt").read_text(encoding="utf-8"),
                "fixture",
            )

    def test_cli_stages_skill_and_selects_eval_by_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            evals_file = root / "evals.json"
            evals_file.write_text(json.dumps({
                "skill_name": "example-skill",
                "evals": [{
                    "id": 9,
                    "prompt": "Run case nine.",
                    "expected_output": "A result.",
                    "expectations": ["The result is present."],
                }],
            }), encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()
            bin_dir = root / "bin"
            bin_dir.mkdir()
            fake_codex = bin_dir / "codex"
            fake_codex.write_text(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "if '--version' in sys.argv:\n"
                "    print('codex-cli test')\n"
                "else:\n"
                "    print(json.dumps({'type': 'turn.completed'}))\n",
                encoding="utf-8",
            )
            fake_codex.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = str(bin_dir) + os.pathsep + environment["PATH"]

            completed = subprocess.run([
                sys.executable,
                str(SCRIPTS_DIR / "run_client_eval.py"),
                "--client", "codex",
                "--workspace", str(workspace),
                "--skill-directory", str(skill),
                "--evals-file", str(evals_file),
                "--eval-id", "9",
                "--output-dir", str(root / "output"),
            ], text=True, capture_output=True, check=False, env=environment)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(
                (workspace / ".agents/skills/example-skill/SKILL.md").is_file()
            )
            run_record = json.loads(
                (root / "output/run.json").read_text(encoding="utf-8")
            )
            self.assertEqual(run_record["execution_status"], "COMPLETED")
            self.assertEqual(run_record["command"][-1], "Run case nine.")

    def test_rejects_eval_for_a_different_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evals_file = Path(temporary) / "evals.json"
            evals_file.write_text(json.dumps({
                "skill_name": "different-skill",
                "evals": [{
                    "id": 1,
                    "prompt": "Run a case.",
                    "expected_output": "A result.",
                    "expectations": ["The result is present."],
                }],
            }), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "skill_name must match"):
                eval_case_from_file(evals_file, 1, "example-skill")

    def test_cli_rejects_eval_for_a_different_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            evals_file = root / "evals.json"
            evals_file.write_text(json.dumps({
                "skill_name": "different-skill",
                "evals": [{"id": 1, "prompt": "Run a case."}],
            }), encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()

            completed = subprocess.run([
                sys.executable,
                str(SCRIPTS_DIR / "run_client_eval.py"),
                "--client", "codex",
                "--workspace", str(workspace),
                "--skill-directory", str(skill),
                "--evals-file", str(evals_file),
                "--eval-id", "1",
                "--output-dir", str(root / "output"),
                "--dry-run",
            ], text=True, capture_output=True, check=False)

            self.assertEqual(completed.returncode, 2)
            self.assertIn("skill_name must match", completed.stderr)

    def test_cli_rejects_symlinked_workspace_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real_workspace = root / "real-workspace"
            real_workspace.mkdir()
            linked_workspace = root / "linked-workspace"
            linked_workspace.symlink_to(real_workspace, target_is_directory=True)

            completed = subprocess.run([
                sys.executable,
                str(SCRIPTS_DIR / "run_client_eval.py"),
                "--client", "codex",
                "--workspace", str(linked_workspace),
                "--prompt", "Run a case.",
                "--output-dir", str(root / "output"),
                "--dry-run",
            ], text=True, capture_output=True, check=False)

            self.assertEqual(completed.returncode, 2)
            self.assertIn("workspace root must not be a symlink", completed.stderr)

    def test_rejects_current_directory_fixture_segment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evals_file = Path(temporary) / "evals.json"
            evals_file.write_text(json.dumps({
                "skill_name": "example-skill",
                "evals": [{
                    "id": 1,
                    "prompt": "Run a case.",
                    "files": ["evals/./input.txt"],
                }],
            }), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "files must be relative"):
                eval_case_from_file(evals_file, 1, "example-skill")

    def test_rejects_candidate_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            private_file = root / "private.txt"
            private_file.write_text("private", encoding="utf-8")
            (skill / "linked-private.txt").symlink_to(private_file)
            workspace = root / "workspace"
            workspace.mkdir()

            with self.assertRaisesRegex(ValueError, "contains a symlink"):
                stage_skill(skill, workspace, "codex", [])

    def test_rejects_symlinked_candidate_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            linked_skill = root / "linked-skill"
            linked_skill.symlink_to(skill, target_is_directory=True)
            workspace = root / "workspace"
            workspace.mkdir()

            with self.assertRaisesRegex(ValueError, "root must not be a symlink"):
                stage_skill(linked_skill, workspace, "codex", [])

    def test_rejects_fixture_destination_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            (skill / "evals").mkdir(parents=True)
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            (skill / "evals/sample.txt").write_text("fixture", encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()

            with self.assertRaisesRegex(ValueError, "destination escapes workspace"):
                stage_skill(
                    skill,
                    workspace,
                    "codex",
                    ["../example-skill/evals/sample.txt"],
                )

    def test_rejects_symlinked_staging_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()
            outside = root / "outside"
            outside.mkdir()
            (workspace / ".agents").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "staging path must not be a symlink"):
                stage_skill(skill, workspace, "codex", [])


if __name__ == "__main__":
    unittest.main()
