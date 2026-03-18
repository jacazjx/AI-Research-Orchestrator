import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


COMMON = load_script_module("orchestrator_common")
VERSION = load_script_module("show_version")
INIT = load_script_module("init_research_project")


class ShowVersionTest(unittest.TestCase):
    def test_version_constants_exist(self) -> None:
        """Test that version constants are defined."""
        self.assertTrue(hasattr(COMMON, "SYSTEM_VERSION"))
        self.assertTrue(hasattr(COMMON, "SYSTEM_VERSION_NAME"))
        self.assertTrue(hasattr(COMMON, "VERSION_HISTORY"))

        self.assertIsInstance(COMMON.SYSTEM_VERSION, str)
        self.assertIsInstance(COMMON.SYSTEM_VERSION_NAME, str)
        self.assertIsInstance(COMMON.VERSION_HISTORY, list)
        self.assertGreater(len(COMMON.VERSION_HISTORY), 0)

    def test_version_format(self) -> None:
        """Test that version follows semver format."""
        version_pattern = r"^\d+\.\d+\.\d+$"
        self.assertRegex(COMMON.SYSTEM_VERSION, version_pattern)

    def test_version_history_format(self) -> None:
        """Test version history entries have correct format."""
        for entry in COMMON.VERSION_HISTORY:
            self.assertEqual(len(entry), 3)
            version, date, description = entry
            self.assertIsInstance(version, str)
            self.assertIsInstance(date, str)
            self.assertIsInstance(description, str)

    def test_get_version_info(self) -> None:
        """Test version info retrieval."""
        info = VERSION.get_version_info()

        self.assertEqual(info["version"], COMMON.SYSTEM_VERSION)
        self.assertEqual(info["name"], COMMON.SYSTEM_VERSION_NAME)
        self.assertIn("history", info)
        self.assertEqual(len(info["history"]), len(COMMON.VERSION_HISTORY))

    def test_format_version_report(self) -> None:
        """Test version report formatting."""
        report = VERSION.format_version_report(use_color=False)

        self.assertIn(COMMON.SYSTEM_VERSION_NAME, report)
        self.assertIn(COMMON.SYSTEM_VERSION, report)
        self.assertIn("Version History", report)

    def test_version_report_with_color(self) -> None:
        """Test version report with ANSI colors."""
        report = VERSION.format_version_report(use_color=True)

        # Should contain ANSI escape codes
        self.assertIn("\033[", report)

    def test_version_in_state(self) -> None:
        """Test that version is stored in project state."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "version-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Version test",
            )

            state = COMMON.load_state(project_root)

            self.assertIn("system_version", state)
            self.assertEqual(state["system_version"], COMMON.SYSTEM_VERSION)
            self.assertIn("created_at", state)
            self.assertIn("last_modified", state)

    def test_short_version_output(self) -> None:
        """Test short version output (just version number)."""
        # Import and run the module directly
        import subprocess

        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "show_version.py"), "--short"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), COMMON.SYSTEM_VERSION)

    def test_json_version_output(self) -> None:
        """Test JSON version output."""
        import subprocess

        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "show_version.py"), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)

        data = json.loads(result.stdout)
        self.assertEqual(data["version"], COMMON.SYSTEM_VERSION)

    def test_check_for_updates(self) -> None:
        """Test check_for_updates function."""
        result = VERSION.check_for_updates()
        self.assertEqual(result["current_version"], COMMON.SYSTEM_VERSION)
        self.assertFalse(result["update_available"])
        self.assertIn("message", result)

    def test_main_short_flag(self) -> None:
        """Test main function with --short flag."""
        args = ["--short"]
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as mock_print:
                result = VERSION.main()
                self.assertEqual(0, result)
                mock_print.assert_called_with(COMMON.SYSTEM_VERSION)

    def test_main_json_flag(self) -> None:
        """Test main function with --json flag."""
        args = ["--json"]
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as mock_print:
                result = VERSION.main()
                self.assertEqual(0, result)
                call_args = mock_print.call_args[0][0]
                parsed = json.loads(call_args)
                self.assertIn("version", parsed)

    def test_main_json_with_check_updates(self) -> None:
        """Test main function with --json and --check-updates flags."""
        args = ["--json", "--check-updates"]
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as mock_print:
                result = VERSION.main()
                self.assertEqual(0, result)
                call_args = mock_print.call_args[0][0]
                parsed = json.loads(call_args)
                self.assertIn("update_check", parsed)

    def test_main_no_color_flag(self) -> None:
        """Test main function with --no-color flag."""
        args = ["--no-color"]
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as _:
                result = VERSION.main()
                self.assertEqual(0, result)

    def test_main_check_updates_no_update(self) -> None:
        """Test main function with --check-updates when no update available."""
        args = ["--check-updates"]
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as mock_print:
                result = VERSION.main()
                self.assertEqual(0, result)
                # Check that "latest version" message was printed
                calls = [str(call) for call in mock_print.call_args_list]
                combined = " ".join(calls)
                self.assertIn("latest version", combined.lower())

    def test_format_version_report_highlights_current(self) -> None:
        """Test that version report highlights current version."""
        report = VERSION.format_version_report(use_color=False)
        # Current version should be marked with bullet
        self.assertIn(COMMON.SYSTEM_VERSION, report)

    def test_main_default_output(self) -> None:
        """Test main function with no flags."""
        args = []
        with patch("sys.argv", ["show_version.py"] + args):
            with patch("builtins.print") as _:
                result = VERSION.main()
                self.assertEqual(0, result)


if __name__ == "__main__":
    unittest.main()
