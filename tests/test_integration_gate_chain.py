"""Integration tests: init → quality_gate pipeline."""
from __future__ import annotations

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
QUALITY = _load("quality_gate")


class IntegrationGateChainTest(unittest.TestCase):
    """End-to-end tests: initialize project then evaluate quality gate."""

    def _init_project(self, tmp_dir: str, phase: str = "survey") -> Path:
        project_root = Path(tmp_dir)
        INIT.initialize_research_project(
            project_root=project_root,
            topic="Integration test topic",
            client_type="vscode",
            starting_phase=phase,
        )
        return project_root

    def test_fresh_project_gate_returns_revise(self) -> None:
        """A newly initialized project should have decision=revise (no filled deliverables)."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")
            self.assertEqual(
                "revise", result["decision"],
                f"Fresh project should need revisions.\nDecision: {result['decision']}\n"
                f"Blockers: {result['blockers']}"
            )
            # A fresh project materializes template files; they exist but contain placeholders.
            # The gate therefore reports deliverables_still_template (not missing).
            blocker_set = set(result["blockers"])
            has_deliverable_blocker = bool(
                blocker_set & {"required_deliverables_missing", "deliverables_still_template"}
            )
            self.assertTrue(
                has_deliverable_blocker,
                f"Expected a deliverable blocker but got: {result['blockers']}"
            )

    def test_fresh_project_has_correct_current_phase(self) -> None:
        """After init, state.current_phase should be the starting phase."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            state = COMMON.load_state(project_root)
            self.assertEqual("survey", state["current_phase"])

    def test_quality_gate_phase_matches_state(self) -> None:
        """evaluate_quality_gate with no phase arg should use state.current_phase."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            result = QUALITY.evaluate_quality_gate(project_root)
            self.assertEqual("survey", result["phase"])

    def test_approved_gate_removes_gate_blocker(self) -> None:
        """Setting gate_status=approved should remove user_gate blocker."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            # Check initial state has gate blocker
            result_before = QUALITY.evaluate_quality_gate(project_root, phase="survey")
            self.assertIn("user_gate_pending", result_before["blockers"])
            # Approve the gate
            state = COMMON.load_state(project_root)
            state["approval_status"]["gate_1"] = "approved"
            COMMON.save_state(project_root, state)
            # Gate blocker should be gone
            result_after = QUALITY.evaluate_quality_gate(project_root, phase="survey")
            self.assertNotIn("user_gate_pending", result_after["blockers"],
                            f"Gate blocker should be removed after approval. "
                            f"Remaining blockers: {result_after['blockers']}")

    def test_warn_prerequisites_invoked_for_non_survey_start(self) -> None:
        """warn_starting_phase_prerequisites should return warnings for non-survey start."""
        warnings = COMMON.warn_starting_phase_prerequisites("experiments")
        self.assertGreater(len(warnings), 0)
        combined = " ".join(warnings).lower()
        self.assertIn("survey", combined)
        self.assertIn("pilot", combined)

    def test_state_schema_error_on_corrupt_state(self) -> None:
        """load_state should raise StateSchemaError on corrupt state file."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".autoresearch" / "state"
            state_dir.mkdir(parents=True)
            config_dir = project_root / ".autoresearch" / "config"
            config_dir.mkdir(parents=True)
            # Write corrupt state (missing required fields)
            (state_dir / "research-state.yaml").write_text("current_phase: survey\n")
            (config_dir / "orchestrator-config.yaml").write_text("{}\n")
            from exceptions import StateSchemaError  # type: ignore
            with self.assertRaises(StateSchemaError):
                COMMON.load_state(project_root)


if __name__ == "__main__":
    unittest.main()
