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


class ProjectConfigTest(unittest.TestCase):
    def test_load_project_config_merges_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "config-demo"
            INIT.initialize_research_project(project_root=project_root, topic="Config demo")

            config_path = project_root / ".autoresearch/config/orchestrator-config.yaml"
            config = COMMON.read_yaml(config_path)
            config["runtime"]["stale_after_minutes"] = 5
            config["loop_limits"]["survey_critic"] = 7
            COMMON.write_yaml(config_path, config)

            loaded = COMMON.load_project_config(project_root)
            state = COMMON.load_state(project_root)

            self.assertEqual(5, loaded["runtime"]["stale_after_minutes"])
            self.assertEqual("enabled", loaded["backends"]["local"])
            self.assertEqual(7, state["loop_limits"]["survey_critic"])


if __name__ == "__main__":
    unittest.main()
