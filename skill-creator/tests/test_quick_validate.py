from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from quick_validate import validate_skill


class EvalValidationTest(unittest.TestCase):
    def make_skill(self, eval_data: object | None = None) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        skill_root = Path(temporary.name) / "example-skill"
        skill_root.mkdir()
        (skill_root / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Example skill.\n---\n",
            encoding="utf-8",
        )
        if eval_data is not None:
            evals_dir = skill_root / "evals"
            evals_dir.mkdir()
            (evals_dir / "evals.json").write_text(
                json.dumps(eval_data), encoding="utf-8"
            )
        return skill_root

    def test_accepts_documented_eval_schema(self) -> None:
        skill_root = self.make_skill({
            "skill_name": "example-skill",
            "evals": [{
                "id": 1,
                "prompt": "Do the example task.",
                "expected_output": "A completed example.",
                "expectations": ["The output is complete."],
            }],
        })

        valid, message = validate_skill(str(skill_root), target="portable")

        self.assertTrue(valid, message)

    def test_rejects_legacy_fixture_shape(self) -> None:
        skill_root = self.make_skill({"fixtures": [{"id": "old-shape"}]})

        valid, message = validate_skill(str(skill_root), target="portable")

        self.assertFalse(valid)
        self.assertIn("skill_name must match", message)
        self.assertIn("requires a non-empty evals list", message)

    def test_rejects_duplicate_ids_and_escaping_files(self) -> None:
        skill_root = self.make_skill({
            "skill_name": "example-skill",
            "evals": [
                {
                    "id": 1,
                    "prompt": "First case.",
                    "expected_output": "First result.",
                    "expectations": ["First assertion."],
                },
                {
                    "id": 1,
                    "prompt": "Second case.",
                    "expected_output": "Second result.",
                    "expectations": ["Second assertion."],
                    "files": ["../private.txt"],
                },
            ],
        })

        valid, message = validate_skill(str(skill_root), target="portable")

        self.assertFalse(valid)
        self.assertIn("id must be unique", message)
        self.assertIn("path must be relative", message)

    def test_rejects_absolute_fixture_path(self) -> None:
        skill_root = self.make_skill({
            "skill_name": "example-skill",
            "evals": [{
                "id": 1,
                "prompt": "Run a case.",
                "expected_output": "A result.",
                "expectations": ["The result is present."],
                "files": ["/tmp/input.txt"],
            }],
        })

        valid, message = validate_skill(str(skill_root), target="portable")

        self.assertFalse(valid)
        self.assertIn("path must be relative", message)

    def test_rejects_current_directory_fixture_segment(self) -> None:
        skill_root = self.make_skill({
            "skill_name": "example-skill",
            "evals": [{
                "id": 1,
                "prompt": "Run a case.",
                "expected_output": "A result.",
                "expectations": ["The result is present."],
                "files": ["evals/./input.txt"],
            }],
        })

        valid, message = validate_skill(str(skill_root), target="portable")

        self.assertFalse(valid)
        self.assertIn("path must be relative", message)


if __name__ == "__main__":
    unittest.main()
