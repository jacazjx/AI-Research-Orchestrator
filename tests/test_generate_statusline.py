import importlib.util
import json
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
STATUSLINE = load_script_module("generate_statusline")
INIT = load_script_module("init_research_project")


class GenerateStatuslineTest(unittest.TestCase):
    def test_generate_statusline_basic(self) -> None:
        """Test basic statusline generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"

            # Initialize a project
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Test research topic",
            )

            # Generate statusline
            statusline = STATUSLINE.generate_statusline(project_root, use_color=False)

            # Check that statusline contains expected elements
            self.assertIn("Phase:", statusline)
            self.assertIn("Gate:", statusline)
            self.assertIn("Survey", statusline)
            self.assertIn("Agents:", statusline)

    def test_statusline_shows_current_phase(self) -> None:
        """Test that statusline shows correct current phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "phase-test"

            # Initialize project at experiment phase (use new semantic name)
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Phase test topic",
                starting_phase="experiments",
            )

            statusline = STATUSLINE.generate_statusline(project_root, use_color=False)

            # Should show Experiments phase
            self.assertIn("Experiments", statusline)
            self.assertIn("gate_3", statusline.lower())

    def test_statusline_compact_mode(self) -> None:
        """Test compact single-line statusline."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "compact-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Compact test",
            )

            statusline = STATUSLINE.generate_statusline(project_root, use_color=False, compact=True)

            # Should be a single line (no newlines)
            lines = statusline.strip().split("\n")
            self.assertEqual(len(lines), 1)
            # Check for "survey" (lowercase in compact mode) or "Survey" (title case)
            self.assertIn("survey", statusline.lower())

    def test_json_output(self) -> None:
        """Test JSON status output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="JSON test topic",
                starting_phase="pilot",  # Use new semantic name
            )

            status = STATUSLINE.generate_json_status(project_root)

            # Check JSON structure
            self.assertEqual(status["current_phase"], "pilot")  # New semantic name
            self.assertEqual(status["current_gate"], "gate_2")
            self.assertIn("agents", status)
            self.assertEqual(len(status["agents"]), 5)  # 5 phases

            # Check agent status
            for agent_status in status["agents"]:
                self.assertIn("phase", agent_status)
                self.assertIn("primary_agent", agent_status)
                self.assertIn("secondary_agent", agent_status)
                self.assertIn("primary_status", agent_status)
                self.assertIn("secondary_status", agent_status)

    def test_agent_status_determination(self) -> None:
        """Test agent status determination logic."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "status-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Status test",
            )

            state = COMMON.load_state(project_root)

            # Test current phase (survey - new semantic name)
            status = STATUSLINE.get_agent_status(state, "survey", "primary")
            self.assertEqual(status, "active")

            # Test future phase (pilot - new semantic name)
            status = STATUSLINE.get_agent_status(state, "pilot", "primary")
            self.assertEqual(status, "pending")

    def test_progress_bar_generation(self) -> None:
        """Test progress bar generation."""
        # Test different completion percentages (using new semantic names)
        bar_0 = STATUSLINE.generate_progress_bar("survey", 0, width=10, use_color=False)
        self.assertEqual(bar_0, "░░░░░░░░░░")

        bar_50 = STATUSLINE.generate_progress_bar("experiments", 50, width=10, use_color=False)
        self.assertEqual(bar_50, "█████░░░░░")

        bar_100 = STATUSLINE.generate_progress_bar("reflection", 100, width=10, use_color=False)
        self.assertEqual(bar_100, "██████████")

    def test_colorization(self) -> None:
        """Test colorization function."""
        # With color disabled
        text = STATUSLINE.colorize("test", "green", use_color=False)
        self.assertEqual(text, "test")

        # With color enabled
        text = STATUSLINE.colorize("test", "green", use_color=True)
        self.assertIn("test", text)
        self.assertNotEqual(text, "test")  # Should have ANSI codes

    def test_status_icons(self) -> None:
        """Test status icon generation."""
        # Active status
        icon = STATUSLINE.get_status_icon("active", use_color=False)
        self.assertEqual(icon, "●")

        # Reviewing status
        icon = STATUSLINE.get_status_icon("reviewing", use_color=False)
        self.assertEqual(icon, "●")

        # Completed status
        icon = STATUSLINE.get_status_icon("completed", use_color=False)
        self.assertEqual(icon, "✓")

        # Pending status
        icon = STATUSLINE.get_status_icon("pending", use_color=False)
        self.assertEqual(icon, "○")


if __name__ == "__main__":
    unittest.main()