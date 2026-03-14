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
OVERLAY = load_script_module("apply_overlay")
RENDER = load_script_module("render_agent_prompt")
EXCEPTIONS = load_script_module("exceptions")


class ApplyOverlayTest(unittest.TestCase):
    def test_approved_overlay_is_rendered_in_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-demo"
            INIT.initialize_research_project(project_root=project_root, topic="Overlay demo")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["phase_reviews"]["reflection_curator"] = "approved"
            state["approval_status"]["gate_5"] = "approved"
            COMMON.write_yaml(state_path, state)

            overlay_path = project_root / "paper/overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("Prioritize explicit failure analysis.", encoding="utf-8")

            OVERLAY.activate_overlay(project_root, str(overlay_path), scope_roles=["critic"], scope_phases=["survey"])
            rendered = RENDER.render_agent_prompt(
                project_root=project_root,
                role="critic",
                task_summary="Review the current survey package",
            )

            self.assertIn("Approved Overlays", rendered["prompt"])
            self.assertIn("Prioritize explicit failure analysis.", rendered["prompt"])

            writer_prompt = RENDER.render_agent_prompt(
                project_root=project_root,
                role="paper-writer",
                task_summary="Draft the paper",
            )
            self.assertNotIn("Prioritize explicit failure analysis.", writer_prompt["prompt"])

    def test_rejects_overlay_paths_outside_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-safety"
            INIT.initialize_research_project(project_root=project_root, topic="Overlay safety")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["phase_reviews"]["reflection_curator"] = "approved"
            state["approval_status"]["gate_5"] = "approved"
            COMMON.write_yaml(state_path, state)

            outside_overlay = Path(temp_dir) / "outside.md"
            outside_overlay.write_text("Should not be loadable.", encoding="utf-8")

            with self.assertRaises(Exception) as context:
                OVERLAY.activate_overlay(project_root, "../outside.md")
            self.assertIn("PathSecurityError", type(context.exception).__name__)


if __name__ == "__main__":
    unittest.main()
