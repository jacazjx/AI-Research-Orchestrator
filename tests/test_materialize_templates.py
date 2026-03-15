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


INIT = load_script_module("init_research_project")
MATERIALIZE = load_script_module("materialize_templates")


class MaterializeTemplatesTest(unittest.TestCase):
    def test_recreates_missing_template_without_overwriting_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "pilot-validation"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Pilot validation",
            )

            # Use new paths
            pilot_plan = project_root / "code/configs/pilot-experiment-plan.md"
            reviewer_report = project_root / "paper/reviewer-report.md"
            pilot_plan.parent.mkdir(parents=True, exist_ok=True)
            pilot_plan.write_text("custom pilot plan\n", encoding="utf-8")
            if reviewer_report.exists():
                reviewer_report.unlink()

            result = MATERIALIZE.materialize_project_templates(project_root, overwrite=False)

            self.assertEqual("custom pilot plan\n", pilot_plan.read_text(encoding="utf-8"))
            self.assertTrue(reviewer_report.exists())
            # Check for new paths in rendered_files
            self.assertIn("paper/reviewer-report.md", result["rendered_files"])
            self.assertNotIn("code/configs/pilot-experiment-plan.md", result["rendered_files"])

    def test_overwrite_true_replaces_existing_files(self) -> None:
        """Test that overwrite=True replaces existing files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overwrite-test"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overwrite test",
            )

            # Modify a template file (not the state file)
            idea_brief = project_root / ".autoresearch/idea-brief.md"
            original_content = idea_brief.read_text(encoding="utf-8")
            idea_brief.write_text("modified content\n", encoding="utf-8")

            result = MATERIALIZE.materialize_project_templates(project_root, overwrite=True)

            # File should be replaced (not the modified content)
            self.assertNotEqual("modified content\n", idea_brief.read_text(encoding="utf-8"))
            self.assertTrue(result["overwrite"])

    def test_materialize_returns_rendered_files_list(self) -> None:
        """Test that materialize returns list of rendered files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "rendered-files"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Rendered files test",
            )

            result = MATERIALIZE.materialize_project_templates(project_root, overwrite=False)

            self.assertIn("project_root", result)
            self.assertIn("state_path", result)
            self.assertIn("overwrite", result)
            self.assertIn("rendered_files", result)
            self.assertIsInstance(result["rendered_files"], list)

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
                "--json",
            ]
            with patch("sys.argv", ["materialize_templates.py"] + args):
                with patch("builtins.print") as mock_print:
                    MATERIALIZE.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("project_root", parsed)
                    self.assertIn("rendered_files", parsed)

    def test_main_outputs_human_readable_by_default(self) -> None:
        """Test that main outputs human-readable text by default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "human-output"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Human output test",
            )

            args = [
                "--project-root",
                str(project_root),
            ]
            with patch("sys.argv", ["materialize_templates.py"] + args):
                with patch("builtins.print") as mock_print:
                    MATERIALIZE.main()
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("Project root", combined)

    def test_main_with_overwrite_flag(self) -> None:
        """Test that --overwrite flag is passed correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overwrite-flag"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overwrite flag test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--overwrite",
            ]
            with patch("sys.argv", ["materialize_templates.py"] + args):
                with patch("builtins.print") as mock_print:
                    MATERIALIZE.main()
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("True", combined)

    def test_build_parser_accepts_all_arguments(self) -> None:
        """Test that parser accepts all expected arguments."""
        parser = MATERIALIZE.build_parser()
        args = parser.parse_args(
            [
                "--project-root",
                "/tmp/test",
                "--overwrite",
                "--json",
            ]
        )
        self.assertEqual("/tmp/test", args.project_root)
        self.assertTrue(args.overwrite)
        self.assertTrue(args.json)


if __name__ == "__main__":
    unittest.main()
