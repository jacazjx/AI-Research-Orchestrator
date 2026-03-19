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
QUALITY = load_script_module("quality_gate")


class QualityGateTest(unittest.TestCase):
    def test_markdown_field_parser_does_not_consume_multiline_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "sample.md"
            sample.write_text(
                "\n".join(
                    [
                        "# Sample",
                        "",
                        "- Plain bullet without ASCII colon",
                        "- Another natural-language bullet：with full-width colon only",
                        "",
                        "## Recommendation",
                        "",
                        "- Recommendation: `approve`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            fields = COMMON.parse_markdown_fields(sample)

            self.assertEqual({"Recommendation": "approve"}, fields)

    def test_returns_revise_for_pending_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quality-revise"
            INIT.initialize_research_project(project_root=project_root, topic="Quality revise")

            # Use new semantic phase name
            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")

            self.assertEqual("revise", result["decision"])
            self.assertIn("phase_review_pending", result["blockers"])
            # When files exist but are templates, we get "deliverables_still_template"
            # When files don't exist, we get "required_deliverables_missing"
            # Since initialize creates template files, we expect deliverables_still_template
            self.assertIn("deliverables_still_template", result["blockers"])
            self.assertIn("structured_gate_signals_invalid", result["blockers"])

    def test_returns_advance_for_approved_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quality-advance"
            INIT.initialize_research_project(project_root=project_root, topic="Quality advance")

            # Use new paths from DEFAULT_DELIVERABLES
            for relative_path in (
                "docs/survey/survey-round-summary.md",
                "docs/survey/critic-round-review.md",
            ):
                (project_root / relative_path).write_text(
                    f"substantive content for {relative_path}\n", encoding="utf-8"
                )
            (project_root / "docs/survey/research-readiness-report.md").write_text(
                "# Research Readiness Report\n\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )
            (project_root / "docs/survey/phase-scorecard.md").write_text(
                "# Phase 1 Scorecard\n\n- Gate readiness: `approve`\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["phase_reviews"]["survey_critic"] = "approved"
            state["approval_status"]["gate_1"] = "approved"
            COMMON.write_yaml(state_path, state)

            # Use new semantic phase name
            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")

            self.assertEqual("advance", result["decision"])
            self.assertEqual(100, result["scores"]["evidence_completeness"])

    def test_returns_pivot_when_review_is_pivot(self) -> None:
        """Test that decision is pivot when review_status is pivot."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quality-pivot"
            INIT.initialize_research_project(project_root=project_root, topic="Quality pivot")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["phase_reviews"]["survey_critic"] = "pivot"
            COMMON.write_yaml(state_path, state)

            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")

            self.assertEqual("pivot", result["decision"])

    def test_returns_pivot_when_pivot_candidates_exist(self) -> None:
        """Test that decision is pivot when pivot_candidates exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quality-pivot-candidate"
            INIT.initialize_research_project(
                project_root=project_root, topic="Quality pivot candidate"
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["pivot_candidates"] = ["alternative-approach"]
            COMMON.write_yaml(state_path, state)

            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")

            self.assertEqual("pivot", result["decision"])
            self.assertEqual(["alternative-approach"], result["pivot_candidates"])

    def test_returns_escalate_when_loop_limit_reached(self) -> None:
        """Test that decision is escalate_to_user when loop limit reached."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quality-escalate"
            INIT.initialize_research_project(project_root=project_root, topic="Quality escalate")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["loop_counts"]["survey_critic"] = 3
            state["loop_limits"]["survey_critic"] = 3
            COMMON.write_yaml(state_path, state)

            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")

            self.assertEqual("escalate_to_user", result["decision"])
            self.assertEqual(3, result["loop_count"])
            self.assertEqual(3, result["loop_limit"])
            self.assertIn("loop_limit_reached", result["blockers"])

    def test_phase_loop_key_mapping(self) -> None:
        """Test PHASE_LOOP_KEY constant returns correct mapping for semantic phase names."""
        from constants.phases import PHASE_LOOP_KEY

        self.assertEqual("survey_critic", PHASE_LOOP_KEY["survey"])
        self.assertEqual("pilot_code_adviser", PHASE_LOOP_KEY["pilot"])
        self.assertEqual("experiment_code_adviser", PHASE_LOOP_KEY["experiments"])
        self.assertEqual("writer_reviewer", PHASE_LOOP_KEY["paper"])
        self.assertEqual("reflector_curator", PHASE_LOOP_KEY["reflection"])

    def test_phase_loop_key_legacy_names(self) -> None:
        """Test PHASE_LOOP_KEY constant covers legacy phase names."""
        from constants.phases import PHASE_LOOP_KEY

        self.assertEqual("survey_critic", PHASE_LOOP_KEY["01-survey"])
        self.assertEqual("pilot_code_adviser", PHASE_LOOP_KEY["02-pilot-analysis"])

    def test_build_parser(self) -> None:
        """Test build_parser creates correct parser."""
        parser = QUALITY.build_parser()

        self.assertIsNotNone(parser)
        # Check that it has the required arguments
        args = parser.parse_args(["--project-root", "/tmp", "--phase", "survey"])
        self.assertEqual("/tmp", args.project_root)
        self.assertEqual("survey", args.phase)
        self.assertFalse(args.json)

    def test_main_with_json_output(self) -> None:
        """Test main function with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            INIT.initialize_research_project(project_root=project_root, topic="Main JSON")

            args = [
                "--project-root",
                str(project_root),
                "--phase",
                "survey",
                "--json",
            ]
            with patch("sys.argv", ["quality_gate.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = QUALITY.main()
                    # Should return non-zero since decision is not "advance"
                    self.assertNotEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("decision", parsed)

    def test_main_human_readable_output(self) -> None:
        """Test main function with human readable output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-human"
            INIT.initialize_research_project(project_root=project_root, topic="Main human")

            args = [
                "--project-root",
                str(project_root),
                "--phase",
                "survey",
            ]
            with patch("sys.argv", ["quality_gate.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = QUALITY.main()
                    self.assertNotEqual(0, result)
                    # Check that human readable output is printed
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("Phase:", combined)
                    self.assertIn("Decision:", combined)

    def test_main_returns_zero_for_advance(self) -> None:
        """Test main returns 0 when decision is advance."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-advance"
            INIT.initialize_research_project(project_root=project_root, topic="Main advance")

            # Set up approved state
            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["phase_reviews"]["survey_critic"] = "approved"
            state["approval_status"]["gate_1"] = "approved"
            COMMON.write_yaml(state_path, state)

            # Create deliverables with proper content
            for relative_path in (
                "docs/survey/survey-round-summary.md",
                "docs/survey/critic-round-review.md",
                "docs/survey/research-readiness-report.md",
                "docs/survey/phase-scorecard.md",
            ):
                file_path = project_root / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(
                    "- Recommendation: `approve`\n- Gate readiness: `approve`\n", encoding="utf-8"
                )

            args = [
                "--project-root",
                str(project_root),
                "--phase",
                "survey",
                "--json",
            ]
            with patch("sys.argv", ["quality_gate.py"] + args):
                with patch("builtins.print"):
                    result = QUALITY.main()
                    self.assertEqual(0, result)

    def test_phase_loop_key_covers_all_semantic_phases(self) -> None:
        """verify PHASE_LOOP_KEY in constants covers all semantic phases."""
        from constants.phases import PHASE_LOOP_KEY, PHASE_SEQUENCE

        for phase in PHASE_SEQUENCE:
            assert phase in PHASE_LOOP_KEY, f"PHASE_LOOP_KEY missing semantic phase '{phase}'"

    def test_evaluate_gate_reads_loop_count_from_correct_key(self) -> None:
        """survey phase loop_count should be read from survey_critic key."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            # initialize minimal project
            INIT.initialize_research_project(
                project_root=project_root,
                topic="test",
                client_type="vscode",
            )
            # manually set loop count
            state = COMMON.load_state(project_root)
            state["loop_counts"]["survey_critic"] = 2
            COMMON.save_state(project_root, state)
            # evaluate
            result = QUALITY.evaluate_quality_gate(project_root, phase="survey")
            assert (
                result["loop_count"] == 2
            ), f"loop_count should be 2 from survey_critic key, got {result['loop_count']}"
