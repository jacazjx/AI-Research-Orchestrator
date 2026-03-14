"""Tests for ARIS state management functions."""

import tempfile
from pathlib import Path
import unittest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from orchestrator_common import (
    build_idea_state,
    save_idea_state,
    load_idea_state,
    clear_idea_state,
    IDEA_STATE_FILENAME,
    load_aris_config,
    is_auto_proceed,
    DEFAULT_ARIS_CONFIG,
)


class TestIdeaState(unittest.TestCase):
    """Test IDEA_STATE management functions."""

    def test_build_idea_state_defaults(self):
        """Test building idea state with defaults."""
        state = build_idea_state(direction="test direction")
        self.assertEqual(state["direction"], "test direction")
        self.assertEqual(state["phase"], "literature-survey")
        self.assertEqual(state["ideas_generated"], 0)
        self.assertIsNone(state["top_idea_id"])
        self.assertIn("timestamp", state)

    def test_build_idea_state_full(self):
        """Test building idea state with all fields."""
        state = build_idea_state(
            direction="transformer efficiency",
            phase="pilot",
            ideas_generated=8,
            ideas_filtered=3,
            pilots_run=2,
            pilots_positive=1,
            top_idea_id="idea_003",
        )
        self.assertEqual(state["direction"], "transformer efficiency")
        self.assertEqual(state["phase"], "pilot")
        self.assertEqual(state["ideas_generated"], 8)
        self.assertEqual(state["ideas_filtered"], 3)
        self.assertEqual(state["pilots_run"], 2)
        self.assertEqual(state["pilots_positive"], 1)
        self.assertEqual(state["top_idea_id"], "idea_003")

    def test_save_and_load_idea_state(self):
        """Test saving and loading idea state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            state = build_idea_state(
                direction="test",
                phase="idea-generation",
                ideas_generated=5,
            )
            save_idea_state(project_root, state)

            # Verify file exists
            state_path = project_root / IDEA_STATE_FILENAME
            self.assertTrue(state_path.exists())

            # Load and verify
            loaded = load_idea_state(project_root)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["direction"], "test")
            self.assertEqual(loaded["phase"], "idea-generation")
            self.assertEqual(loaded["ideas_generated"], 5)

    def test_load_idea_state_missing(self):
        """Test loading when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            loaded = load_idea_state(project_root)
            self.assertIsNone(loaded)

    def test_clear_idea_state(self):
        """Test clearing idea state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            state = build_idea_state(direction="test")
            save_idea_state(project_root, state)

            state_path = project_root / IDEA_STATE_FILENAME
            self.assertTrue(state_path.exists())

            clear_idea_state(project_root)
            self.assertFalse(state_path.exists())


class TestArisConfig(unittest.TestCase):
    """Test ARIS configuration functions."""

    def test_default_aris_config_structure(self):
        """Test default ARIS config has all expected keys."""
        self.assertIn("auto_proceed", DEFAULT_ARIS_CONFIG)
        self.assertIn("pilot_max_hours", DEFAULT_ARIS_CONFIG)
        self.assertIn("reviewer", DEFAULT_ARIS_CONFIG)
        self.assertIn("max_review_rounds", DEFAULT_ARIS_CONFIG)
        self.assertIn("feishu", DEFAULT_ARIS_CONFIG)

        # Check defaults
        self.assertFalse(DEFAULT_ARIS_CONFIG["auto_proceed"])
        self.assertEqual(DEFAULT_ARIS_CONFIG["max_review_rounds"], 4)
        self.assertFalse(DEFAULT_ARIS_CONFIG["reviewer"]["enabled"])

    def test_load_aris_config_with_missing_file(self):
        """Test loading ARIS config when config file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            # Create minimal project structure
            (project_root / "00-admin").mkdir(parents=True)

            config = load_aris_config(project_root)
            # Should return defaults
            self.assertEqual(config["auto_proceed"], DEFAULT_ARIS_CONFIG["auto_proceed"])
            self.assertEqual(config["max_review_rounds"], DEFAULT_ARIS_CONFIG["max_review_rounds"])

    def test_is_auto_proceed_default(self):
        """Test is_auto_proceed returns False by default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / "00-admin").mkdir(parents=True)

            result = is_auto_proceed(project_root)
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()