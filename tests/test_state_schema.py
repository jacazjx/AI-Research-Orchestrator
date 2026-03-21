"""Tests for state schema validation."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SKILL_DIR / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


COMMON = _load("orchestrator_common")
INIT = _load("init_research_project")


class StateSchemaValidationTest(unittest.TestCase):
    REQUIRED_KEYS = [
        "current_phase",
        "deliverables",
        "approval_status",
        "phase_reviews",
        "loop_counts",
    ]

    def _valid_state(self) -> dict:
        return {
            "current_phase": "survey",
            "deliverables": {},
            "approval_status": {"gate_1": "pending"},
            "phase_reviews": {"survey_critic": "pending"},
            "loop_counts": {},
        }

    def test_validate_accepts_valid_state(self) -> None:
        errors = COMMON.validate_state_schema(self._valid_state())
        self.assertEqual([], errors, f"Valid state should have no errors: {errors}")

    def test_validate_reports_missing_current_phase(self) -> None:
        state = self._valid_state()
        del state["current_phase"]
        errors = COMMON.validate_state_schema(state)
        self.assertTrue(
            any("current_phase" in e for e in errors),
            f"Should error on missing current_phase: {errors}",
        )

    def test_validate_reports_missing_deliverables(self) -> None:
        state = self._valid_state()
        del state["deliverables"]
        errors = COMMON.validate_state_schema(state)
        self.assertTrue(
            any("deliverables" in e for e in errors),
            f"Should error on missing deliverables: {errors}",
        )

    def test_validate_reports_missing_approval_status(self) -> None:
        state = self._valid_state()
        del state["approval_status"]
        errors = COMMON.validate_state_schema(state)
        self.assertTrue(any("approval_status" in e for e in errors))

    def test_validate_reports_missing_phase_reviews(self) -> None:
        state = self._valid_state()
        del state["phase_reviews"]
        errors = COMMON.validate_state_schema(state)
        self.assertTrue(any("phase_reviews" in e for e in errors))

    def test_validate_reports_unknown_current_phase(self) -> None:
        state = self._valid_state()
        state["current_phase"] = "nonexistent_phase"
        errors = COMMON.validate_state_schema(state)
        self.assertTrue(
            any("current_phase" in e or "nonexistent_phase" in e for e in errors),
            f"Should error on unknown phase: {errors}",
        )

    def test_validate_accepts_archive_phase(self) -> None:
        """archive / 06-archive are valid terminal phases."""
        state = self._valid_state()
        state["current_phase"] = "archive"
        errors = COMMON.validate_state_schema(state)
        self.assertEqual([], errors)

    def test_load_state_raises_state_schema_error_on_corrupt_yaml(self) -> None:
        """load_state raises StateSchemaError when required fields are missing."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            state_path.parent.mkdir(parents=True)
            # Write state with only current_phase (missing other required fields)
            state_path.write_text("current_phase: survey\n", encoding="utf-8")
            config_path = project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
            config_path.parent.mkdir(parents=True)
            config_path.write_text("{}\n", encoding="utf-8")
            from exceptions import StateSchemaError  # type: ignore

            with self.assertRaises(StateSchemaError):
                COMMON.load_state(project_root)


class TestSubstepStatus(unittest.TestCase):
    """Test substep status structure matches phase-execution-details.md."""

    def test_pilot_phase_has_problem_validation_substep(self):
        """Pilot phase should include problem_validation substep."""
        from orchestrator_common import _build_default_substep_status

        substep_status = _build_default_substep_status()

        assert "pilot" in substep_status, "Missing pilot phase in substep_status"
        assert (
            "problem_validation" in substep_status["pilot"]
        ), "Missing problem_validation substep in pilot phase"

    def test_all_substeps_have_required_fields(self):
        """Each substep should have status, review_result, attempts, last_agent."""
        from orchestrator_common import _build_default_substep_status

        substep_status = _build_default_substep_status()
        required_fields = {"status", "review_result", "attempts", "last_agent"}

        for phase, substeps in substep_status.items():
            for substep_name, substep_data in substeps.items():
                missing = required_fields - set(substep_data.keys())
                assert not missing, f"Substep {phase}/{substep_name} missing fields: {missing}"


if __name__ == "__main__":
    unittest.main()
