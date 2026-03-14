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
INIT = load_script_module("init_research_project")
STAGE = load_script_module("run_stage_loop")
EXCEPTIONS = load_script_module("exceptions")


class RunStageLoopTest(unittest.TestCase):
    def test_stage_revise_continues_internal_iteration_with_next_agent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "stage-iterate-pending-review"
            INIT.initialize_research_project(project_root=project_root, topic="Stage iterate pending review")

            # Use new paths
            problem_analysis = project_root / "docs/reports/pilot/problem-analysis.md"
            problem_analysis.parent.mkdir(parents=True, exist_ok=True)
            problem_analysis.write_text(
                "# Problem Analysis\n\n- runtime finding: real pilot still blocked\n",
                encoding="utf-8",
            )
            result = STAGE.run_stage_loop(
                project_root,
                phase="pilot",  # Use new semantic name
                actor="code",
                note="Code agent updated the pilot analysis and is waiting for adviser review.",
            )

            self.assertEqual("revise", result["decision"])
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("adviser", state["progress"]["current_agent"])
            self.assertEqual("run-adviser", state["progress"]["next_action"])

    def test_revise_review_increments_loop_and_switches_back_to_authoring_agent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "stage-iterate-revise"
            INIT.initialize_research_project(project_root=project_root, topic="Stage iterate revise")

            # Use new paths
            paper_draft = project_root / "paper/paper-draft.md"
            paper_draft.parent.mkdir(parents=True, exist_ok=True)
            paper_draft.write_text(
                "# Paper Draft\n\nA draft that still needs major revision.\n",
                encoding="utf-8",
            )
            result = STAGE.run_stage_loop(
                project_root,
                phase="paper",  # Use new semantic name
                actor="reviewer-editor",
                review_status="revise",
                note="Reviewer requests another manuscript revision inside the same phase.",
            )

            self.assertEqual("revise", result["decision"])
            self.assertEqual(1, result["loop_count"])
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("paper-writer", state["progress"]["current_agent"])
            self.assertEqual("run-paper-writer", state["progress"]["next_action"])
            self.assertEqual("iteration-1", state["subphase"])

    def test_auto_transition_after_approved_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "stage-transition"
            INIT.initialize_research_project(project_root=project_root, topic="Stage transition")

            # Use new paths
            for relative_path in (
                "docs/reports/survey/survey-round-summary.md",
                "docs/reports/survey/critic-round-review.md",
            ):
                file_path = project_root / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(f"ready: {relative_path}\n", encoding="utf-8")
            readiness_report = project_root / "docs/reports/survey/research-readiness-report.md"
            readiness_report.write_text(
                "# Research Readiness Report\n\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )
            phase_scorecard = project_root / "docs/reports/survey/phase-scorecard.md"
            phase_scorecard.write_text(
                "# Phase 1 Scorecard\n\n- Gate readiness: `approve`\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )

            result = STAGE.run_stage_loop(
                project_root,
                phase="survey",  # Use new semantic name
                actor="critic",
                review_status="approved",
                gate_status="approved",
                increment_loop=True,
                auto_transition=True,
                note="Survey package approved.",
            )

            self.assertEqual("advance", result["decision"])
            self.assertEqual("pilot", result["transitioned_to"])
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("pilot", state["current_phase"])
            self.assertEqual(1, state["loop_counts"]["survey_critic"])

    def test_rejected_gate_requires_and_applies_return_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "stage-return"
            INIT.initialize_research_project(project_root=project_root, topic="Stage return")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["current_phase"] = "experiments"  # Use new semantic name
            state["phase"] = "experiments"
            state["current_gate"] = "gate_3"
            state["phase_reviews"]["experiment_adviser"] = "approved"
            state["approval_status"]["gate_3"] = "rejected"
            COMMON.write_yaml(state_path, state)

            result = STAGE.run_stage_loop(
                project_root,
                phase="experiments",  # Use new semantic name
                actor="orchestrator",
                gate_status="rejected",
                return_phase="pilot",  # Use new semantic name
                note="Return to pilot for stronger validation.",
            )

            self.assertEqual("pilot", result["returned_to"])
            state = COMMON.read_yaml(state_path)
            self.assertEqual("pilot", state["current_phase"])
            self.assertEqual("pending", state["approval_status"]["gate_2"])
            self.assertIn("pilot", state["progress"]["allowed_return_phases"])

    def test_rejected_gate_rejects_future_return_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "stage-invalid-return"
            INIT.initialize_research_project(project_root=project_root, topic="Stage invalid return")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["current_phase"] = "experiments"  # Use new semantic name
            state["phase"] = "experiments"
            state["current_gate"] = "gate_3"
            state["phase_reviews"]["experiment_adviser"] = "approved"
            state["approval_status"]["gate_3"] = "rejected"
            COMMON.write_yaml(state_path, state)

            with self.assertRaises(Exception) as context:
                STAGE.run_stage_loop(
                    project_root,
                    phase="experiments",  # Use new semantic name
                    actor="orchestrator",
                    gate_status="rejected",
                    return_phase="paper",  # Use new semantic name - this is a future phase, should be rejected
                    note="Invalid future phase jump should be blocked.",
                )
            self.assertIn("PhaseTransitionError", type(context.exception).__name__)


if __name__ == "__main__":
    unittest.main()
