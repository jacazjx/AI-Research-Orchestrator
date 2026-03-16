"""Tests for the state_migrator module."""

import importlib.util
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    """Dynamically load a script module for testing."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


STATE_MIGRATOR = load_script_module("state_migrator")


class TestGetStateVersion(unittest.TestCase):
    """Tests for get_state_version function."""

    def test_returns_version_when_present(self) -> None:
        """Test that version is returned when present."""
        state = {"state_version": "1.1.0", "topic": "test"}
        self.assertEqual(STATE_MIGRATOR.get_state_version(state), "1.1.0")

    def test_returns_default_when_missing(self) -> None:
        """Test that default version is returned when missing."""
        state = {"topic": "test"}
        self.assertEqual(STATE_MIGRATOR.get_state_version(state), "1.0.0")

    def test_returns_default_when_none(self) -> None:
        """Test that default version is returned when version is None."""
        state = {"state_version": None, "topic": "test"}
        self.assertEqual(STATE_MIGRATOR.get_state_version(state), "1.0.0")


class TestNeedsMigration(unittest.TestCase):
    """Tests for needs_migration function."""

    def test_returns_false_for_current_version(self) -> None:
        """Test that no migration needed for current version."""
        state = {"state_version": STATE_MIGRATOR.CURRENT_STATE_VERSION}
        self.assertFalse(STATE_MIGRATOR.needs_migration(state))

    def test_returns_true_for_older_version(self) -> None:
        """Test that migration needed for older version."""
        state = {"state_version": "1.0.0"}
        self.assertTrue(STATE_MIGRATOR.needs_migration(state))

    def test_returns_true_for_missing_version(self) -> None:
        """Test that migration needed when version missing."""
        state = {"topic": "test"}
        self.assertTrue(STATE_MIGRATOR.needs_migration(state))


class TestMigrationPath(unittest.TestCase):
    """Tests for get_migration_path function."""

    def test_path_from_1_0_to_current(self) -> None:
        """Test migration path from 1.0.0 to current."""
        path = STATE_MIGRATOR.get_migration_path("1.0.0", STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], ("1.0.0", "1.1.0"))
        self.assertEqual(path[1], ("1.1.0", "1.12.0"))
        self.assertEqual(path[2], ("1.12.0", "2.0.0"))

    def test_path_from_1_1_to_2_0(self) -> None:
        """Test migration path from 1.1.0 to 2.0.0."""
        path = STATE_MIGRATOR.get_migration_path("1.1.0", "2.0.0")
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], ("1.1.0", "1.12.0"))
        self.assertEqual(path[1], ("1.12.0", "2.0.0"))

    def test_no_path_for_same_version(self) -> None:
        """Test empty path for same version."""
        path = STATE_MIGRATOR.get_migration_path("1.1.0", "1.1.0")
        self.assertEqual(len(path), 0)

    def test_error_for_unknown_version(self) -> None:
        """Test error for unknown version."""
        with self.assertRaises(ValueError):
            STATE_MIGRATOR.get_migration_path("0.0.0", "2.0.0")

    def test_error_for_backward_migration(self) -> None:
        """Test error for backward migration."""
        with self.assertRaises(ValueError):
            STATE_MIGRATOR.get_migration_path("2.0.0", "1.0.0")


class TestMigrate1_0To1_1(unittest.TestCase):
    """Tests for migrate_1_0_to_1_1 function."""

    def test_adds_substep_status(self) -> None:
        """Test that substep_status is added."""
        state = {"topic": "test", "state_version": "1.0.0"}
        migrated, log = STATE_MIGRATOR.migrate_1_0_to_1_1(state)

        self.assertIn("substep_status", migrated)
        self.assertIn("survey", migrated["substep_status"])
        self.assertIn("pilot", migrated["substep_status"])
        self.assertEqual(migrated["state_version"], "1.1.0")
        self.assertIn("substep_status", log)

    def test_preserves_existing_fields(self) -> None:
        """Test that existing fields are preserved."""
        state = {
            "topic": "test topic",
            "project_id": "proj-123",
            "current_phase": "survey",
            "state_version": "1.0.0",
        }
        migrated, _ = STATE_MIGRATOR.migrate_1_0_to_1_1(state)

        self.assertEqual(migrated["topic"], "test topic")
        self.assertEqual(migrated["project_id"], "proj-123")
        self.assertEqual(migrated["current_phase"], "survey")

    def test_does_not_modify_original(self) -> None:
        """Test that original state is not modified."""
        state = {"topic": "test", "state_version": "1.0.0"}
        migrated, _ = STATE_MIGRATOR.migrate_1_0_to_1_1(state)

        self.assertNotIn("substep_status", state)
        self.assertIn("substep_status", migrated)


class TestMigrate1_1To1_12(unittest.TestCase):
    """Tests for migrate_1_1_to_1_12 function."""

    def test_adds_aris_fields(self) -> None:
        """Test that ARIS fields are added."""
        state = {
            "topic": "test",
            "state_version": "1.1.0",
            "substep_status": {"survey": {}},
        }
        migrated, log = STATE_MIGRATOR.migrate_1_1_to_1_12(state)

        self.assertIn("system_version", migrated)
        self.assertIn("inner_loops", migrated)
        self.assertIn("loop_counts", migrated)
        self.assertIn("outer_loop", migrated)
        self.assertIn("loop_limits", migrated)
        self.assertIn("recovery_status", migrated)
        self.assertIn("active_jobs", migrated)
        self.assertEqual(migrated["state_version"], "1.12.0")

    def test_preserves_existing_fields(self) -> None:
        """Test that existing fields are preserved."""
        state = {
            "topic": "test topic",
            "substep_status": {"survey": {"literature_survey": {"status": "completed"}}},
            "state_version": "1.1.0",
        }
        migrated, _ = STATE_MIGRATOR.migrate_1_1_to_1_12(state)

        self.assertEqual(
            migrated["substep_status"]["survey"]["literature_survey"]["status"],
            "completed"
        )


class TestMigrate1_12To2_0(unittest.TestCase):
    """Tests for migrate_1_12_to_2_0 function."""

    def test_adds_v2_fields(self) -> None:
        """Test that version 2.0.0 fields are added."""
        state = {"topic": "test", "state_version": "1.12.0"}
        migrated, log = STATE_MIGRATOR.migrate_1_12_to_2_0(state)

        self.assertIn("research_type", migrated)
        self.assertEqual(migrated["research_type"], "ml_experiment")
        self.assertIn("user_config_inherited", migrated)
        self.assertEqual(migrated["user_config_inherited"], {})
        self.assertIn("gpu_usage_history", migrated)
        self.assertEqual(migrated["gpu_usage_history"], [])
        self.assertEqual(migrated["state_version"], "2.0.0")

    def test_preserves_existing_fields(self) -> None:
        """Test that existing fields are preserved."""
        state = {
            "topic": "test topic",
            "project_id": "proj-456",
            "system_version": "1.12.0",
            "state_version": "1.12.0",
        }
        migrated, _ = STATE_MIGRATOR.migrate_1_12_to_2_0(state)

        self.assertEqual(migrated["topic"], "test topic")
        self.assertEqual(migrated["project_id"], "proj-456")


class TestMigrateState(unittest.TestCase):
    """Tests for migrate_state function."""

    def test_no_migration_needed_for_current(self) -> None:
        """Test no changes for current version."""
        state = {"state_version": STATE_MIGRATOR.CURRENT_STATE_VERSION, "topic": "test"}
        migrated, logs = STATE_MIGRATOR.migrate_state(state)

        self.assertIs(migrated, state)
        self.assertEqual(len(logs), 0)

    def test_full_migration_from_1_0(self) -> None:
        """Test full migration from 1.0.0."""
        state = {"topic": "test", "project_id": "proj-123"}
        migrated, logs = STATE_MIGRATOR.migrate_state(state)

        self.assertEqual(migrated["state_version"], STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertEqual(len(logs), 3)
        self.assertIn("substep_status", migrated)
        self.assertIn("research_type", migrated)
        self.assertIn("user_config_inherited", migrated)
        self.assertIn("gpu_usage_history", migrated)

    def test_migration_from_1_1(self) -> None:
        """Test migration from 1.1.0."""
        state = {
            "topic": "test",
            "state_version": "1.1.0",
            "substep_status": {"survey": {}},
        }
        migrated, logs = STATE_MIGRATOR.migrate_state(state)

        self.assertEqual(migrated["state_version"], STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertEqual(len(logs), 2)

    def test_migration_from_1_12(self) -> None:
        """Test migration from 1.12.0."""
        state = {
            "topic": "test",
            "state_version": "1.12.0",
            "inner_loops": {"survey_critic": 2},
        }
        migrated, logs = STATE_MIGRATOR.migrate_state(state)

        self.assertEqual(migrated["state_version"], STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertEqual(len(logs), 1)
        self.assertEqual(migrated["inner_loops"]["survey_critic"], 2)

    def test_migration_preserves_all_data(self) -> None:
        """Test that migration preserves all original data."""
        state = {
            "topic": "important research",
            "project_id": "proj-789",
            "current_phase": "pilot",
            "current_gate": "gate_2",
            "approval_status": {"gate_1": "approved"},
            "gate_scores": {"gate_1": 4.5, "gate_2": 0},
        }
        migrated, _ = STATE_MIGRATOR.migrate_state(state)

        self.assertEqual(migrated["topic"], "important research")
        self.assertEqual(migrated["project_id"], "proj-789")
        self.assertEqual(migrated["current_phase"], "pilot")
        self.assertEqual(migrated["current_gate"], "gate_2")
        self.assertEqual(migrated["approval_status"]["gate_1"], "approved")
        self.assertEqual(migrated["gate_scores"]["gate_1"], 4.5)


class TestValidateStateVersion(unittest.TestCase):
    """Tests for validate_state_version function."""

    def test_valid_version(self) -> None:
        """Test that known versions are valid."""
        for version in STATE_MIGRATOR.VERSION_ORDER:
            state = {"state_version": version}
            self.assertTrue(STATE_MIGRATOR.validate_state_version(state))

    def test_invalid_version(self) -> None:
        """Test that unknown versions are invalid."""
        state = {"state_version": "99.0.0"}
        self.assertFalse(STATE_MIGRATOR.validate_state_version(state))


class TestGetMigrationInfo(unittest.TestCase):
    """Tests for get_migration_info function."""

    def test_info_for_current_version(self) -> None:
        """Test info for current version."""
        state = {"state_version": STATE_MIGRATOR.CURRENT_STATE_VERSION}
        info = STATE_MIGRATOR.get_migration_info(state)

        self.assertEqual(info["current_version"], STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertEqual(info["target_version"], STATE_MIGRATOR.CURRENT_STATE_VERSION)
        self.assertFalse(info["needs_migration"])
        self.assertEqual(info["migration_steps"], 0)
        self.assertTrue(info["is_valid_version"])

    def test_info_for_older_version(self) -> None:
        """Test info for older version."""
        state = {"state_version": "1.0.0"}
        info = STATE_MIGRATOR.get_migration_info(state)

        self.assertEqual(info["current_version"], "1.0.0")
        self.assertTrue(info["needs_migration"])
        self.assertEqual(info["migration_steps"], 3)
        self.assertTrue(info["is_valid_version"])
        self.assertEqual(len(info["migration_path"]), 3)

    def test_info_for_unknown_version(self) -> None:
        """Test info for unknown version."""
        state = {"state_version": "99.0.0"}
        info = STATE_MIGRATOR.get_migration_info(state)

        self.assertFalse(info["is_valid_version"])
        self.assertIn("error", info)


class TestStateVersions(unittest.TestCase):
    """Tests for STATE_VERSIONS constant."""

    def test_all_versions_have_descriptions(self) -> None:
        """Test that all versions have descriptions."""
        for version in STATE_MIGRATOR.VERSION_ORDER:
            self.assertIn(version, STATE_MIGRATOR.STATE_VERSIONS)

    def test_current_version_is_last(self) -> None:
        """Test that current version is the last in order."""
        self.assertEqual(
            STATE_MIGRATOR.VERSION_ORDER[-1],
            STATE_MIGRATOR.CURRENT_STATE_VERSION
        )

    def test_migrations_cover_all_steps(self) -> None:
        """Test that migrations cover all version steps."""
        for i in range(len(STATE_MIGRATOR.VERSION_ORDER) - 1):
            from_ver = STATE_MIGRATOR.VERSION_ORDER[i]
            to_ver = STATE_MIGRATOR.VERSION_ORDER[i + 1]
            key = (from_ver, to_ver)
            self.assertIn(key, STATE_MIGRATOR.MIGRATIONS)


if __name__ == "__main__":
    unittest.main()