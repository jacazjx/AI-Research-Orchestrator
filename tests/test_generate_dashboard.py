import importlib.util
import json
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
DASHBOARD = load_script_module("generate_dashboard")


class GenerateDashboardTest(unittest.TestCase):
    def test_generates_runtime_dashboard_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "dashboard-demo"
            INIT.initialize_research_project(project_root=project_root, topic="Dashboard demo")

            result = DASHBOARD.generate_dashboard(project_root)

            status_path = project_root / result["status_path"]
            progress_path = project_root / result["progress_path"]
            timeline_path = project_root / result["timeline_path"]

            self.assertTrue(status_path.exists())
            self.assertTrue(progress_path.exists())
            self.assertTrue(timeline_path.exists())
            payload = json.loads(status_path.read_text(encoding="utf-8"))
            # New semantic phase name
            self.assertEqual("survey", payload["phase"])


if __name__ == "__main__":
    unittest.main()
