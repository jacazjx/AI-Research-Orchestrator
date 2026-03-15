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
INIT = load_script_module("init_research_project")
VALIDATE = load_script_module("validate_handoff")


class ValidateHandoffTest(unittest.TestCase):
    def test_survey_to_pilot_requires_user_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "retrieval-agent"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Retrieval-augmented multi-agent planning",
            )

            result = VALIDATE.validate_handoff(project_root, "survey-to-pilot")

            self.assertFalse(result["ok"])
            self.assertTrue(any("gate_1 must be approved" in error for error in result["errors"]))

    def test_experiments_to_paper_detects_missing_deliverable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "graph-sparsity"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Graph sparsity learning",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["approval_status"]["gate_3"] = "approved"
            state["phase_reviews"]["experiment_adviser"] = "approved"
            COMMON.write_yaml(state_path, state)
            # Use new paths from DEFAULT_DELIVERABLES
            for relative_path in (
                "code/configs/experiment-spec.md",
                "code/checkpoints/run-registry.md",
                "code/checkpoints/checkpoint-index.md",
                "docs/reports/experiments/evidence-package-index.md",
            ):
                (project_root / relative_path).write_text(
                    f"ready: {relative_path}\n", encoding="utf-8"
                )
            (project_root / "docs/reports/experiments/experiment-adviser-review.md").write_text(
                "# Experiment Adviser Review\n\n- Status: `approved`\n- Recommendation: `approve`\n- Handoff decision: `approve`\n",
                encoding="utf-8",
            )
            (project_root / "docs/reports/experiments/phase-scorecard.md").write_text(
                "# Phase 3 Scorecard\n\n- Gate readiness: `approve`\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )
            # Delete the results-summary to test missing file detection
            results_summary_path = project_root / "docs/reports/experiments/results-summary.md"
            if results_summary_path.exists():
                results_summary_path.unlink()

            result = VALIDATE.validate_handoff(project_root, "experiments-to-paper")

            self.assertFalse(result["ok"])
            # Check for new path in missing_files
            self.assertIn("docs/reports/experiments/results-summary.md", result["missing_files"])

    def test_pilot_to_experiments_requires_phase_review_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "pilot-review"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Pilot review",
            )

            result = VALIDATE.validate_handoff(project_root, "pilot-to-experiments")

            self.assertFalse(result["ok"])
            self.assertTrue(
                any("phase_reviews.pilot_adviser" in error for error in result["errors"])
            )

    def test_handoff_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "safe-paths"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Safe path validation",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["approval_status"]["gate_1"] = "approved"
            state["phase_reviews"]["survey_critic"] = "approved"
            state["deliverables"]["readiness_report"] = "../../escape.md"
            COMMON.write_yaml(state_path, state)

            result = VALIDATE.validate_handoff(project_root, "survey-to-pilot")

            self.assertFalse(result["ok"])
            self.assertTrue(
                any("must stay inside the project root" in error for error in result["errors"])
            )

    def test_survey_loop_escalates_after_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "loop-limit"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Loop escalation policy",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["loop_counts"]["survey_critic"] = 3
            COMMON.write_yaml(state_path, state)

            result = VALIDATE.validate_handoff(project_root, "survey-loop")

            self.assertFalse(result["ok"])
            self.assertEqual("escalate", result["status"])
            self.assertEqual(3, result["limit"])

    def test_survey_loop_passes_when_below_limit(self) -> None:
        """Test that loop passes when count is below limit."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "loop-pass"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Loop pass test",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["loop_counts"]["survey_critic"] = 1
            COMMON.write_yaml(state_path, state)

            result = VALIDATE.validate_handoff(project_root, "survey-loop")

            self.assertTrue(result["ok"])
            self.assertEqual("pass", result["status"])

    def test_paper_to_reflection_handoff(self) -> None:
        """Test paper-to-reflection handoff validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "paper-to-reflection"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Paper to reflection",
            )

            result = VALIDATE.validate_handoff(project_root, "paper-to-reflection")

            self.assertFalse(result["ok"])  # Requires gate_4 approval
            self.assertEqual("reflection", result["next_phase"])

    def test_main_outputs_json_when_requested(self) -> None:
        """Test that main outputs JSON when --json flag is used."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-output"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="JSON output test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--target",
                "survey-to-pilot",
                "--json",
            ]
            with patch("sys.argv", ["validate_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    VALIDATE.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("target", parsed)
                    self.assertEqual("survey-to-pilot", parsed["target"])

    def test_main_outputs_human_readable_for_handoff(self) -> None:
        """Test that main outputs human-readable text for handoff validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "human-output"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Human output test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--target",
                "survey-to-pilot",
            ]
            with patch("sys.argv", ["validate_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    VALIDATE.main()
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("Target", combined)
                    self.assertIn("survey-to-pilot", combined)

    def test_main_outputs_human_readable_for_loop(self) -> None:
        """Test that main outputs human-readable text for loop validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "loop-output"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Loop output test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--target",
                "survey-loop",
            ]
            with patch("sys.argv", ["validate_handoff.py"] + args):
                with patch("builtins.print") as mock_print:
                    VALIDATE.main()
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("Loop", combined)

    def test_main_returns_nonzero_on_failure(self) -> None:
        """Test that main returns non-zero when validation fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "fail-return"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Fail return test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--target",
                "survey-to-pilot",
            ]
            with patch("sys.argv", ["validate_handoff.py"] + args):
                with patch("builtins.print"):
                    result = VALIDATE.main()
                    self.assertNotEqual(0, result)

    def test_main_returns_zero_on_success(self) -> None:
        """Test that main returns zero when validation passes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "success-return"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Success return test",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["loop_counts"]["survey_critic"] = 0
            COMMON.write_yaml(state_path, state)

            args = [
                "--project-root",
                str(project_root),
                "--target",
                "survey-loop",
            ]
            with patch("sys.argv", ["validate_handoff.py"] + args):
                with patch("builtins.print"):
                    result = VALIDATE.main()
                    self.assertEqual(0, result)

    def test_build_parser_accepts_all_targets(self) -> None:
        """Test that parser accepts all valid targets."""
        parser = VALIDATE.build_parser()
        # Test a few valid targets
        for target in ["survey-to-pilot", "pilot-to-experiments", "survey-loop"]:
            args = parser.parse_args(["--project-root", "/tmp", "--target", target])
            self.assertEqual(target, args.target)

    def test_placeholder_file_detection(self) -> None:
        """Test detection of placeholder/template files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "placeholder"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Placeholder test",
            )

            result = VALIDATE.validate_handoff(project_root, "survey-to-pilot")

            self.assertFalse(result["ok"])
            # Template files should be detected as placeholders
            self.assertTrue(len(result["placeholder_files"]) > 0)


if __name__ == "__main__":
    unittest.main()
