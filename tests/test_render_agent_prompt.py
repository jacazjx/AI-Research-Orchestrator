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

    def test_render_with_overlay_stack(self) -> None:
        """Test rendering with overlay stack."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-test"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overlay test",
            )

            # Add overlay to state
            overlay_path = project_root / "paper" / "overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("## Overlay Content\n\nThis is an overlay.", encoding="utf-8")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["overlay_stack"] = ["paper/overlay-draft.md"]
            COMMON.write_yaml(state_path, state)

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",
                task_summary="Test overlay",
            )

            self.assertEqual(1, result["overlay_count"])
            self.assertIn("Approved Overlays", result["prompt"])
            self.assertIn("overlay-draft.md", result["prompt"])

    def test_render_with_overlay_filtered_by_role(self) -> None:
        """Test that overlay is filtered by role."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-role"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overlay role test",
            )

            # Add overlay with role restriction
            overlay_path = project_root / "paper" / "overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("## Overlay Content\n\nThis is an overlay.", encoding="utf-8")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            # Overlay only for survey role
            state["overlay_stack"] = [
                json.dumps({"path": "paper/overlay-draft.md", "roles": ["survey"], "phases": []})
            ]
            COMMON.write_yaml(state_path, state)

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",  # Different role
                task_summary="Test overlay filtering",
            )

            # Overlay should not appear because role doesn't match
            self.assertNotIn("Approved Overlays", result["prompt"])

    def test_render_with_overlay_filtered_by_phase(self) -> None:
        """Test that overlay is filtered by phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-phase"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overlay phase test",
            )

            # Add overlay with phase restriction
            overlay_path = project_root / "paper" / "overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("## Overlay Content\n\nThis is an overlay.", encoding="utf-8")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            # Overlay only for paper phase
            state["overlay_stack"] = [
                json.dumps({"path": "paper/overlay-draft.md", "roles": [], "phases": ["paper"]})
            ]
            COMMON.write_yaml(state_path, state)

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",
                task_summary="Test overlay phase filtering",
            )

            # Overlay should not appear because phase is survey, not paper
            self.assertNotIn("Approved Overlays", result["prompt"])

    def test_render_with_missing_overlay_file(self) -> None:
        """Test that missing overlay file is skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-missing"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overlay missing test",
            )

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["overlay_stack"] = ["paper/nonexistent.md"]
            COMMON.write_yaml(state_path, state)

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",
                task_summary="Test missing overlay",
            )

            # No overlay should appear
            self.assertNotIn("Approved Overlays", result["prompt"])

    def test_render_with_empty_overlay_file(self) -> None:
        """Test that empty overlay file is skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overlay-empty"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Overlay empty test",
            )

            # Create empty overlay
            overlay_path = project_root / "paper" / "overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("", encoding="utf-8")

            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["overlay_stack"] = ["paper/overlay-draft.md"]
            COMMON.write_yaml(state_path, state)

            result = RENDER.render_agent_prompt(
                project_root=project_root,
                role="reflector",
                task_summary="Test empty overlay",
            )

            # No overlay should appear
            self.assertNotIn("Approved Overlays", result["prompt"])

    def test_parse_overlay_entry_string(self) -> None:
        """Test parsing string overlay entry."""
        result = RENDER._parse_overlay_entry("path/to/overlay.md")
        self.assertEqual("path/to/overlay.md", result["path"])
        self.assertEqual([], result["roles"])
        self.assertEqual([], result["phases"])

    def test_parse_overlay_entry_json(self) -> None:
        """Test parsing JSON overlay entry."""
        entry = json.dumps(
            {"path": "path/to/overlay.md", "roles": ["survey"], "phases": ["survey"]}
        )
        result = RENDER._parse_overlay_entry(entry)
        self.assertEqual("path/to/overlay.md", result["path"])
        self.assertEqual(["survey"], result["roles"])
        self.assertEqual(["survey"], result["phases"])

    def test_build_parser(self) -> None:
        """Test build_parser creates correct parser."""
        parser = RENDER.build_parser()

        args = parser.parse_args(
            [
                "--project-root",
                "/tmp",
                "--role",
                "survey",
                "--task-summary",
                "Test task",
            ]
        )
        self.assertEqual("/tmp", args.project_root)
        self.assertEqual("survey", args.role)
        self.assertEqual("Test task", args.task_summary)
        self.assertFalse(args.json)

    def test_main_with_json_output(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Main JSON test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--role",
                "survey",
                "--task-summary",
                "Test task",
                "--json",
            ]
            with patch("sys.argv", ["render_agent_prompt.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RENDER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("prompt", parsed)
                    self.assertEqual("survey", parsed["role"])

    def test_main_human_readable_output(self) -> None:
        """Test main with human readable output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-human"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Main human test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--role",
                "survey",
                "--task-summary",
                "Test task",
            ]
            with patch("sys.argv", ["render_agent_prompt.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RENDER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    # Should output the prompt directly
                    self.assertIn("Survey", call_args)

    def test_main_with_all_options(self) -> None:
        """Test main with all options."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-all"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Main all test",
            )

            args = [
                "--project-root",
                str(project_root),
                "--role",
                "survey",
                "--task-summary",
                "Test task",
                "--current-objective",
                "Test objective",
                "--phase-override",
                "survey",
                "--loop-label",
                "loop-1",
                "--required-input",
                "Input 1",
                "--must-read",
                "file1.md",
                "--extra-instruction",
                "Extra instruction",
                "--json",
            ]
            with patch("sys.argv", ["render_agent_prompt.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RENDER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    # Check that required inputs and extra instructions are passed
                    self.assertEqual(["Input 1"], parsed["required_inputs"])
                    self.assertEqual(["file1.md"], parsed["must_read"])
                    self.assertEqual(["Extra instruction"], parsed["extra_instructions"])


if __name__ == "__main__":
    unittest.main()
