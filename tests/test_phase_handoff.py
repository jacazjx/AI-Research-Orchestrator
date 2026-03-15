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
HANDOFF = load_script_module("phase_handoff")
INIT = load_script_module("init_research_project")


class PhaseHandoffTest(unittest.TestCase):
    def test_create_handoff_summary_template(self) -> None:
        """Test creating handoff summary template."""
        template = HANDOFF.create_handoff_summary_template("01-survey", "survey")

        self.assertEqual(template["phase"], "01-survey")
        self.assertEqual(template["agent_role"], "survey")
        self.assertIn("key_findings", template)
        self.assertIn("decisions_made", template)
        self.assertIn("open_issues", template)
        self.assertIn("recommendations_for_next_phase", template)

    def test_save_and_load_handoff_summary(self) -> None:
        """Test saving and loading handoff summary."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "handoff-test"

            # Initialize project
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Handoff test",
            )

            # Save handoff summary
            summary = {
                "key_findings": ["Finding 1", "Finding 2"],
                "decisions_made": ["Decision 1"],
                "open_issues": ["Issue 1"],
                "recommendations_for_next_phase": ["Rec 1"],
            }

            result = HANDOFF.save_handoff_summary(project_root, "01-survey", "survey", summary)

            self.assertEqual(result["status"], "saved")
            self.assertEqual(result["phase"], "01-survey")
            self.assertEqual(result["agent_role"], "survey")

            # Load handoff summary
            loaded = HANDOFF.load_handoff_summary(project_root, "01-survey", "survey")

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["key_findings"], ["Finding 1", "Finding 2"])
            self.assertEqual(loaded["decisions_made"], ["Decision 1"])

    def test_list_handoff_summaries(self) -> None:
        """Test listing handoff summaries."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "list-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="List test",
            )

            # Initially empty
            result = HANDOFF.list_all_handoff_summaries(project_root)
            self.assertEqual(result["count"], 0)

            # Save a summary
            HANDOFF.save_handoff_summary(
                project_root, "01-survey", "survey", {"key_findings": ["Test"]}
            )

            # Now should have one
            result = HANDOFF.list_all_handoff_summaries(project_root)
            self.assertEqual(result["count"], 1)

    def test_get_phase_handoff_summaries(self) -> None:
        """Test getting all summaries for a phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "phase-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Phase test",
            )

            # Save summaries for both agents
            HANDOFF.save_handoff_summary(
                project_root, "01-survey", "survey", {"key_findings": ["Survey finding"]}
            )
            HANDOFF.save_handoff_summary(
                project_root, "01-survey", "critic", {"key_findings": ["Critic finding"]}
            )

            # Get phase summaries
            result = HANDOFF.get_phase_handoff_summaries(project_root, "01-survey")

            self.assertEqual(result["phase"], "01-survey")
            self.assertIn("survey", result["available_agents"])
            self.assertIn("critic", result["available_agents"])
            self.assertEqual(len(result["summaries"]), 2)

    def test_format_handoff_report(self) -> None:
        """Test formatting handoff report."""
        handoff_data = {
            "phase": "01-survey",
            "agent_role": "survey",
            "metadata": {"timestamp": "2026-03-13T00:00:00Z"},
            "key_findings": ["Finding 1", "Finding 2"],
            "decisions_made": ["Decision 1"],
            "open_issues": ["Issue 1"],
            "recommendations_for_next_phase": ["Rec 1"],
        }

        report = HANDOFF.format_handoff_report(handoff_data)

        self.assertIn("Phase Handoff Summary", report)
        self.assertIn("01-survey", report)
        self.assertIn("Finding 1", report)
        self.assertIn("Decision 1", report)

    def test_format_handoff_report_with_context(self) -> None:
        """Test formatting handoff report with context for resume."""
        handoff_data = {
            "phase": "02-pilot-analysis",
            "agent_role": "code",
            "metadata": {"timestamp": "2026-03-13T00:00:00Z"},
            "context_for_resume": "Continue from experiment X",
        }

        report = HANDOFF.format_handoff_report(handoff_data)

        self.assertIn("Context for Resume", report)
        self.assertIn("Continue from experiment X", report)

    def test_load_nonexistent_handoff_returns_none(self) -> None:
        """Test loading a nonexistent handoff summary returns None."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-handoff"
            INIT.initialize_research_project(project_root=project_root, topic="No handoff test")

            result = HANDOFF.load_handoff_summary(project_root, "01-survey", "nonexistent")
            self.assertIsNone(result)

    def test_get_phase_handoff_summaries_unknown_phase(self) -> None:
        """Test getting summaries for unknown phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "unknown-phase"
            INIT.initialize_research_project(project_root=project_root, topic="Unknown phase test")

            result = HANDOFF.get_phase_handoff_summaries(project_root, "unknown-phase")
            self.assertEqual(result["phase"], "unknown-phase")
            self.assertEqual(result["summaries"], {})

    def test_main_save_action(self) -> None:
        """Test main with save action."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-save"
            INIT.initialize_research_project(project_root=project_root, topic="Main save test")

            summary_json = json.dumps({"key_findings": ["Test finding"]})
            args = [
                "--project-root",
                str(project_root),
                "--action",
                "save",
                "--phase",
                "01-survey",
                "--agent",
                "survey",
                "--summary",
                summary_json,
            ]
            with patch("sys.argv", ["phase_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = HANDOFF.main()
                    self.assertEqual(0, result)

    def test_main_load_action(self) -> None:
        """Test main with load action."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-load"
            INIT.initialize_research_project(project_root=project_root, topic="Main load test")

            # First save a summary
            HANDOFF.save_handoff_summary(
                project_root, "01-survey", "survey", {"key_findings": ["Test"]}
            )

            args = [
                "--project-root",
                str(project_root),
                "--action",
                "load",
                "--phase",
                "01-survey",
                "--agent",
                "survey",
            ]
            with patch("sys.argv", ["phase_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = HANDOFF.main()
                    self.assertEqual(0, result)

    def test_main_list_action(self) -> None:
        """Test main with list action."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-list"
            INIT.initialize_research_project(project_root=project_root, topic="Main list test")

            args = [
                "--project-root",
                str(project_root),
                "--action",
                "list",
            ]
            with patch("sys.argv", ["phase_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = HANDOFF.main()
                    self.assertEqual(0, result)

    def test_main_template_action(self) -> None:
        """Test main with template action."""
        args = [
            "--project-root",
            "/tmp",
            "--action",
            "template",
            "--phase",
            "01-survey",
            "--agent",
            "survey",
        ]
        with patch("sys.argv", ["phase_handoff.py"] + args):
            with patch("builtins.print") as mock_print:
                result = HANDOFF.main()
                self.assertEqual(0, result)

    def test_main_get_phase_action(self) -> None:
        """Test main with get-phase action."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-get-phase"
            INIT.initialize_research_project(project_root=project_root, topic="Main get phase test")

            # Save a summary
            HANDOFF.save_handoff_summary(
                project_root, "01-survey", "survey", {"key_findings": ["Test"]}
            )

            args = [
                "--project-root",
                str(project_root),
                "--action",
                "get-phase",
                "--phase",
                "01-survey",
            ]
            with patch("sys.argv", ["phase_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = HANDOFF.main()
                    self.assertEqual(0, result)

    def test_main_with_json_output(self) -> None:
        """Test main with --json flag."""
        args = [
            "--project-root",
            "/tmp",
            "--action",
            "template",
            "--phase",
            "01-survey",
            "--agent",
            "survey",
            "--json",
        ]
        with patch("sys.argv", ["phase_handoff.py"] + args):
            with patch("builtins.print") as mock_print:
                result = HANDOFF.main()
                self.assertEqual(0, result)
                # Check that JSON was printed
                call_args = mock_print.call_args[0][0]
                parsed = json.loads(call_args)
                self.assertIn("phase", parsed)


if __name__ == "__main__":
    unittest.main()
