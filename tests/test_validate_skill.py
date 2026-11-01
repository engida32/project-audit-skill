from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skill  # noqa: E402


def write_skill(root: Path, name: str = "project-audit", description: str = "Use when auditing a repository.", body: str = "# Project Audit\n\nBody.\n") -> Path:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n{body}",
        encoding="utf-8",
    )
    return skill


class ValidateSkillTests(unittest.TestCase):
    def test_valid_skill(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = write_skill(Path(raw))
            refs = skill / "references"
            refs.mkdir()
            (refs / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (skill / "SKILL.md").write_text(
                "---\nname: project-audit\ndescription: Use when auditing a repository.\n---\n\n"
                "# Project Audit\n\nSee [guide](references/guide.md).\n",
                encoding="utf-8",
            )
            errors, warnings = validate_skill.validate_skill(skill)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_missing_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = Path(raw) / "project-audit"
            skill.mkdir()
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("missing SKILL.md" in error for error in errors))

    def test_missing_name_and_description(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = Path(raw) / "project-audit"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\n---\n\n# Title\n", encoding="utf-8")
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("missing name" in error for error in errors))
            self.assertTrue(any("missing description" in error for error in errors))

    def test_name_must_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = Path(raw) / "project-audit"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: wrong-name\ndescription: Use when auditing a repository.\n---\n\n# Title\n",
                encoding="utf-8",
            )
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("must match directory name" in error for error in errors))

    def test_description_must_start_with_use_when(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = write_skill(Path(raw), description="Audits a repository.")
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("must start with 'Use when'" in error for error in errors))

    def test_body_line_limit(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = write_skill(Path(raw), body="# Title\n\n" + "line\n" * 510)
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("under 500" in error for error in errors))

    def test_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = write_skill(
                Path(raw),
                body="# Title\n\nSee [missing](references/missing.md).\n",
            )
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("broken link" in error for error in errors))

    def test_absolute_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            body = "# Title\n\nRun " + "/home/" + "alice/project/tool.\n"
            skill = write_skill(Path(raw), body=body)
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("absolute home path" in error for error in errors))

    def test_possible_secret(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            body = "# Title\n\n" + "AKIA" + ("A" * 16) + "\n"
            skill = write_skill(Path(raw), body=body)
            errors, _ = validate_skill.validate_skill(skill)
            self.assertTrue(any("possible secret" in error for error in errors))

    def test_extra_frontmatter_is_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = write_skill(Path(raw))
            (skill / "SKILL.md").write_text(
                "---\nname: project-audit\ndescription: Use when auditing a repository.\n"
                "disable-model-invocation: true\n---\n\n# Title\n",
                encoding="utf-8",
            )
            errors, warnings = validate_skill.validate_skill(skill)
            self.assertEqual(errors, [])
            self.assertTrue(any("extra keys" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
