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
ANALYZE = load_script_module("analyze_project")
INIT = load_script_module("init_research_project")


class AnalyzeProjectTest(unittest.TestCase):
    def test_detect_file_patterns(self) -> None:
        """Test file pattern detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-patterns"
            project_root.mkdir()
            (project_root / "train.py").write_text("# training script", encoding="utf-8")
            (project_root / "README.md").write_text("# README", encoding="utf-8")
            (project_root / "config.yaml").write_text("key: value", encoding="utf-8")

            result = ANALYZE.detect_file_patterns(project_root)

            self.assertIn("experiment_code", result)
            self.assertIn("readme", result)
            self.assertIn("config_files", result)

    def test_detect_file_patterns_excludes_hidden(self) -> None:
        """Test that hidden directories are excluded."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-hidden"
            project_root.mkdir()
            (project_root / ".hidden").mkdir()
            (project_root / ".hidden" / "secret.py").write_text("secret", encoding="utf-8")
            (project_root / "public.py").write_text("public", encoding="utf-8")

            result = ANALYZE.detect_file_patterns(project_root)

            # Should not include files in hidden directories
            all_matches = []
            for category in result.values():
                all_matches.extend(category)
            self.assertNotIn(".hidden/secret.py", all_matches)

    def test_detect_directory_structure(self) -> None:
        """Test directory structure detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-structure"
            project_root.mkdir()
            (project_root / "code").mkdir()
            (project_root / "paper").mkdir()
            (project_root / "custom_dir").mkdir()

            result = ANALYZE.detect_directory_structure(project_root)

            self.assertIn("code", result["top_level_dirs"])
            self.assertIn("paper", result["top_level_dirs"])
            self.assertIn("custom_dir", result["custom_dirs"])
            self.assertGreater(result["total_dirs"], 0)

    def test_detect_existing_deliverables(self) -> None:
        """Test deliverable detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-deliverables"
            INIT.initialize_research_project(project_root=project_root, topic="Test")

            result = ANALYZE.detect_existing_deliverables(project_root)

            # Check that research_state deliverable is detected
            self.assertIn("research_state", result)
            self.assertTrue(result["research_state"]["exists"])
            self.assertGreater(result["research_state"]["line_count"], 0)

    def test_detect_research_state_exists(self) -> None:
        """Test research state detection when exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-state"
            INIT.initialize_research_project(project_root=project_root, topic="Test")

            result = ANALYZE.detect_research_state(project_root)

            self.assertTrue(result["exists"])
            self.assertTrue(result["valid"])
            self.assertIsNotNone(result["current_phase"])

    def test_detect_research_state_missing(self) -> None:
        """Test research state detection when missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-state"
            project_root.mkdir()

            result = ANALYZE.detect_research_state(project_root)

            self.assertFalse(result["exists"])

    def test_detect_experiment_evidence(self) -> None:
        """Test experiment evidence detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-experiments"
            project_root.mkdir()
            (project_root / "experiments").mkdir()
            (project_root / "experiments" / "train.log").write_text("log", encoding="utf-8")

            result = ANALYZE.detect_experiment_evidence(project_root)

            self.assertIn("experiments", result["experiment_dirs"])
            self.assertTrue(len(result["log_files"]) > 0)

    def test_detect_literature_evidence(self) -> None:
        """Test literature evidence detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "analyze-literature"
            project_root.mkdir()
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")

            result = ANALYZE.detect_literature_evidence(project_root)

            self.assertIn("refs.bib", result["bib_files"])

    def test_analyze_project_returns_complete_structure(self) -> None:
        """Test that analyze_project returns complete structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "full-analyze"
            INIT.initialize_research_project(project_root=project_root, topic="Full analyze")

            result = ANALYZE.analyze_project(project_root)

            self.assertIn("project_root", result)
            self.assertIn("directory_structure", result)
            self.assertIn("file_patterns", result)
            self.assertIn("existing_deliverables", result)
            self.assertIn("research_state", result)

    def test_main_outputs_json(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            INIT.initialize_research_project(project_root=project_root, topic="Main JSON")

            args = [
                "--project-root",
                str(project_root),
                "--json",
            ]
            with patch("sys.argv", ["analyze_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    ANALYZE.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("project_root", parsed)

    def test_estimate_phase_with_paper_draft(self) -> None:
        """Test phase estimation with paper draft."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "paper-draft"
            project_root.mkdir()
            (project_root / "paper").mkdir()
            (project_root / "paper" / "paper-draft.md").write_text("# Paper", encoding="utf-8")

            result = ANALYZE.estimate_project_phase(project_root)

            self.assertIn("paper", result["estimated_phase"])

    def test_estimate_phase_with_experiment_files(self) -> None:
        """Test phase estimation with experiment code."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "experiment-code"
            project_root.mkdir()
            (project_root / "train.py").write_text("# training", encoding="utf-8")
            (project_root / "results.csv").write_text("col1,col2", encoding="utf-8")

            result = ANALYZE.estimate_project_phase(project_root)

            # Should detect some form of experiments
            self.assertIsNotNone(result["estimated_phase"])

    def test_format_report(self) -> None:
        """Test report formatting."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "format-report"
            INIT.initialize_research_project(project_root=project_root, topic="Format report")

            analysis = ANALYZE.analyze_project(project_root)
            report = ANALYZE.format_report(analysis)

            self.assertIn("Project Analysis Report", report)
            self.assertIn("Summary", report)
            self.assertIn("Directory Structure", report)

    def test_main_quiet_mode(self) -> None:
        """Test main with --quiet flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "quiet-mode"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--quiet",
            ]
            with patch("sys.argv", ["analyze_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    ANALYZE.main()
                    # Should print just the phase
                    mock_print.assert_called()

    def test_main_nonexistent_project(self) -> None:
        """Test main with nonexistent project root."""
        args = [
            "--project-root",
            "/nonexistent/path",
            "--json",
        ]
        with patch("sys.argv", ["analyze_project.py"] + args):
            result = ANALYZE.main()
            self.assertEqual(1, result)

    def test_detect_file_patterns_with_bib(self) -> None:
        """Test detection of bibliography files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "bib-test"
            project_root.mkdir()
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")

            result = ANALYZE.detect_file_patterns(project_root)

            self.assertTrue(len(result["bibliography"]) > 0)

    def test_detect_file_patterns_with_notebook(self) -> None:
        """Test detection of Jupyter notebooks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "notebook-test"
            project_root.mkdir()
            (project_root / "analysis.ipynb").write_text("{}", encoding="utf-8")

            result = ANALYZE.detect_file_patterns(project_root)

            self.assertTrue(len(result["notebooks"]) > 0)

    def test_detect_experiment_evidence_checkpoints(self) -> None:
        """Test detection of checkpoint files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "checkpoint-test"
            project_root.mkdir()
            (project_root / "model.pt").write_text("model", encoding="utf-8")

            result = ANALYZE.detect_experiment_evidence(project_root)

            self.assertTrue(len(result["checkpoint_files"]) > 0)


if __name__ == "__main__":
    unittest.main()
