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

            OVERLAY.activate_overlay(
                project_root, str(overlay_path), scope_roles=["critic"], scope_phases=["survey"]
            )
            rendered = RENDER.render_agent_prompt(
                project_root=project_root,
                role="critic",
                task_summary="Review the current survey package",
            )

            self.assertIn("Approved Overlays", rendered["prompt"])
            self.assertIn("Prioritize explicit failure analysis.", rendered["prompt"])

            writer_prompt = RENDER.render_agent_prompt(
                project_root=project_root,
                role="writer",
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

    def test_activate_overlay_without_gate_check(self) -> None:
        """Test activating overlay without gate approval check."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-gate-check"
            INIT.initialize_research_project(project_root=project_root, topic="No gate check")

            overlay_path = project_root / "paper/overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("Test overlay content.", encoding="utf-8")

            result = OVERLAY.activate_overlay(project_root, str(overlay_path), require_gate=False)
            self.assertEqual("active", result["status"])

    def test_activate_overlay_raises_for_missing_file(self) -> None:
        """Test that activating missing overlay raises FileNotFoundError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "missing-overlay"
            INIT.initialize_research_project(project_root=project_root, topic="Missing overlay")

            with self.assertRaises(FileNotFoundError):
                OVERLAY.activate_overlay(project_root, "nonexistent.md", require_gate=False)

    def test_activate_overlay_raises_without_gate_approval(self) -> None:
        """Test that activating overlay without gate approval raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-approval"
            INIT.initialize_research_project(project_root=project_root, topic="No approval")

            overlay_path = project_root / "paper/overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("Test overlay.", encoding="utf-8")

            with self.assertRaises(Exception):
                OVERLAY.activate_overlay(project_root, str(overlay_path), require_gate=True)

    def test_main_with_json_output(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-output"
            INIT.initialize_research_project(project_root=project_root, topic="JSON output")

            overlay_path = project_root / "paper/overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("Test overlay.", encoding="utf-8")

            args = [
                "--project-root",
                str(project_root),
                "--overlay-path",
                str(overlay_path),
                "--skip-approval-check",
                "--json",
            ]
            with patch("sys.argv", ["apply_overlay.py"] + args):
                with patch("builtins.print") as mock_print:
                    OVERLAY.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertEqual("active", parsed["status"])

    def test_main_with_scope_options(self) -> None:
        """Test main with scope role and phase options."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "scope-options"
            INIT.initialize_research_project(project_root=project_root, topic="Scope options")

            overlay_path = project_root / "paper/overlay-draft.md"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("Scoped overlay.", encoding="utf-8")

            args = [
                "--project-root",
                str(project_root),
                "--overlay-path",
                str(overlay_path),
                "--skip-approval-check",
                "--scope-role",
                "critic",
                "--scope-phase",
                "survey",
            ]
            with patch("sys.argv", ["apply_overlay.py"] + args):
                result = OVERLAY.main()
                self.assertEqual(0, result)

    def test_build_parser_accepts_all_options(self) -> None:
        """Test that parser accepts all options."""
        parser = OVERLAY.build_parser()
        args = parser.parse_args(
            [
                "--project-root",
                "/tmp",
                "--overlay-path",
                "/tmp/overlay.md",
                "--note",
                "Test note",
                "--scope-role",
                "critic",
                "--scope-phase",
                "survey",
                "--skip-approval-check",
                "--json",
            ]
        )
        self.assertEqual("/tmp", args.project_root)
        self.assertEqual("Test note", args.note)
        self.assertTrue(args.skip_approval_check)


if __name__ == "__main__":
    unittest.main()
