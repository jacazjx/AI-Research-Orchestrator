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


if __name__ == "__main__":
    unittest.main()
