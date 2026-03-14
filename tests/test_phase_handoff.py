import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


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

            result = HANDOFF.save_handoff_summary(
                project_root, "01-survey", "survey", summary
            )

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


if __name__ == "__main__":
    unittest.main()