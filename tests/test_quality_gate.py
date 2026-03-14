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
                "docs/reports/survey/survey-round-summary.md",
                "docs/reports/survey/critic-round-review.md",
            ):
                (project_root / relative_path).write_text(f"substantive content for {relative_path}\n", encoding="utf-8")
            (project_root / "docs/reports/survey/research-readiness-report.md").write_text(
                "# Research Readiness Report\n\n- Recommendation: `approve`\n",
                encoding="utf-8",
            )
            (project_root / "docs/reports/survey/phase-scorecard.md").write_text(
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


if __name__ == "__main__":
    unittest.main()
