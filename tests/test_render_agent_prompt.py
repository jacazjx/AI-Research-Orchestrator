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
RENDER = load_script_module("render_agent_prompt")


class RenderAgentPromptTest(unittest.TestCase):
    def test_renders_prompt_with_orchestrator_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "prompt-demo"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Prompt rendering workflow",
            )

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",
                task_summary="Extract reusable runtime lessons from the completed project",
                current_objective="Prepare the first reflection pass",
                required_inputs=["Experiment evidence package", "Paper acceptance report"],
                extra_instructions=["Separate safe overlays from speculative ideas."],
            )

            prompt = result["prompt"]
            self.assertIn("Extract reusable runtime lessons", prompt)
            self.assertIn("Prepare the first reflection pass", prompt)
            self.assertIn("Experiment evidence package", prompt)
            self.assertIn("Separate safe overlays from speculative ideas.", prompt)
            self.assertIn("05-reflection-evolution/lessons-learned.md", prompt)

    def test_phase_override_updates_gate_in_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "prompt-phase-override"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Prompt rendering workflow",
            )

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="code",
                task_summary="Prepare experiment execution",
                phase_override="03-full-experiments",
            )

            prompt = result["prompt"]
            self.assertIn("Current phase: `03-full-experiments`", prompt)
            self.assertIn("Current gate: `gate_3`", prompt)

    def test_renders_orchestrator_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "orchestrator-demo"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Orchestrator prompt test",
            )

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="orchestrator",
                task_summary="Coordinate research workflow and confirm researcher intent",
                current_objective="Confirm research intent before starting Phase 1",
                extra_instructions=["Ask clarifying questions about target venue."],
            )

            prompt = result["prompt"]
            self.assertIn("Orchestrator", prompt)
            self.assertIn("Coordinate research workflow and confirm researcher intent", prompt)
            self.assertIn("Confirm research intent", prompt)
            self.assertIn("target venue", prompt)
            self.assertIn("research-state.yaml", prompt)
            # Check for key orchestrator responsibilities
            self.assertIn("Intent", prompt)
            self.assertIn("Quality Assurance", prompt)

    def test_orchestrator_has_correct_must_read_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "orchestrator-must-read"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Orchestrator must-read test",
            )

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="orchestrator",
                task_summary="Test must-read files",
            )

            must_read = result["must_read"]
            self.assertIn("00-admin/research-state.yaml", must_read)
            self.assertIn("00-admin/idea-brief.md", must_read)
            self.assertIn("00-admin/dashboard/progress.md", must_read)


if __name__ == "__main__":
    unittest.main()
