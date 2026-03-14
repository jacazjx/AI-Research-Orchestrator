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
PIVOT = load_script_module("pivot_manager")


class PivotManagerTest(unittest.TestCase):
    def test_propose_and_review_pivot_updates_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "pivot-demo"
            INIT.initialize_research_project(project_root=project_root, topic="Pivot demo")

            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="narrow_scope",
                rationale="The original scope is too broad for pilot validation.",
            )
            self.assertEqual("proposed", proposed["status"])

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("pivot", state["phase_reviews"]["survey_critic"])
            self.assertEqual(1, len(state["pivot_candidates"]))

            reviewed = PIVOT.review_pivot(project_root, proposed["pivot_id"], "reject", note="Continue revision")
            self.assertEqual("reject", reviewed["decision"])
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual([], state["pivot_candidates"])
            self.assertEqual("pending", state["phase_reviews"]["survey_critic"])


if __name__ == "__main__":
    unittest.main()
