from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"
SOURCE = ROOT / "skills" / "project-audit" / "SKILL.md"


def run_install(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["sh", str(INSTALL), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class InstallScriptTests(unittest.TestCase):
    def test_default_install(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "skills with space"
            result = run_install(str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = target / "project-audit" / "SKILL.md"
            self.assertTrue(installed.is_file())
            self.assertEqual(installed.read_text(encoding="utf-8"), SOURCE.read_text(encoding="utf-8"))

    def test_second_run_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "skills"
            self.assertEqual(run_install(str(target)).returncode, 0)
            result = run_install(str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)

    def test_force_backs_up_and_replaces(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "skills"
            self.assertEqual(run_install(str(target)).returncode, 0)
            installed = target / "project-audit" / "SKILL.md"
            installed.write_text("local edit\n", encoding="utf-8")

            result = run_install("--force", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(installed.read_text(encoding="utf-8"), SOURCE.read_text(encoding="utf-8"))

            backups = sorted(target.glob("project-audit.bak.*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "SKILL.md").read_text(encoding="utf-8"), "local edit\n")

    def test_uninstall_refuses_without_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "skills"
            stray = target / "project-audit"
            stray.mkdir(parents=True)
            (stray / "notes.txt").write_text("keep me\n", encoding="utf-8")

            result = run_install("--uninstall", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to remove", result.stderr)
            self.assertTrue(stray.is_dir())

    def test_uninstall_removes_a_real_install(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "skills"
            self.assertEqual(run_install(str(target)).returncode, 0)
            result = run_install("--uninstall", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / "project-audit").exists())

    def test_help(self) -> None:
        result = run_install("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)

    def test_unknown_option(self) -> None:
        result = run_install("--bogus")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown option", result.stderr)


if __name__ == "__main__":
    unittest.main()
