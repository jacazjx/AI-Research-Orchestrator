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

            reviewed = PIVOT.review_pivot(
                project_root, proposed["pivot_id"], "reject", note="Continue revision"
            )
            self.assertEqual("reject", reviewed["decision"])
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual([], state["pivot_candidates"])
            self.assertEqual("pending", state["phase_reviews"]["survey_critic"])

    def test_approve_pivot_updates_phase(self) -> None:
        """Test that approving a pivot updates the phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "pivot-approve"
            INIT.initialize_research_project(project_root=project_root, topic="Pivot approve")

            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="scope_change",
                rationale="Need to adjust scope based on findings.",
            )
            self.assertEqual("proposed", proposed["status"])

            reviewed = PIVOT.review_pivot(
                project_root, proposed["pivot_id"], "approve", note="Proceed with pivot"
            )
            self.assertEqual("approve", reviewed["decision"])
            self.assertEqual("survey", reviewed["current_phase"])

    def test_downgrade_to_pivot_changes_phase(self) -> None:
        """Test that downgrade_to_pivot pivot changes phase correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "downgrade"
            INIT.initialize_research_project(project_root=project_root, topic="Downgrade test")

            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="downgrade_to_pilot",
                rationale="Need to go back to pilot.",
            )

            reviewed = PIVOT.review_pivot(project_root, proposed["pivot_id"], "approve")
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            # Should be legacy format for downgrade
            self.assertIn("pilot", state["current_phase"])

    def test_archive_branch_sets_complete_gate(self) -> None:
        """Test that archive_branch pivot sets complete gate."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "archive"
            INIT.initialize_research_project(project_root=project_root, topic="Archive test")

            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="archive_branch",
                rationale="Project should be archived.",
            )

            reviewed = PIVOT.review_pivot(project_root, proposed["pivot_id"], "approve")
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("complete", state["current_gate"])

    def test_propose_with_alternative(self) -> None:
        """Test proposing a pivot with alternative."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "alternative"
            INIT.initialize_research_project(project_root=project_root, topic="Alternative test")

            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="methodology_change",
                rationale="Current approach not working.",
                alternative="Try a different algorithm.",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            pivot_entry = json.loads(state["pivot_candidates"][0])
            self.assertEqual("Try a different algorithm.", pivot_entry["alternative"])

    def test_main_propose_command(self) -> None:
        """Test main with propose command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-propose"
            INIT.initialize_research_project(project_root=project_root, topic="Main propose test")

            args = [
                "propose",
                "--project-root",
                str(project_root),
                "--pivot-type",
                "scope_change",
                "--rationale",
                "Testing main propose",
            ]
            with patch("sys.argv", ["pivot_manager.py"] + args):
                with patch("builtins.print") as mock_print:
                    PIVOT.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertEqual("proposed", parsed["status"])

    def test_main_review_command(self) -> None:
        """Test main with review command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-review"
            INIT.initialize_research_project(project_root=project_root, topic="Main review test")

            # First propose a pivot
            proposed = PIVOT.propose_pivot(
                project_root,
                pivot_type="test_pivot",
                rationale="Testing main review",
            )

            args = [
                "review",
                "--project-root",
                str(project_root),
                "--pivot-id",
                proposed["pivot_id"],
                "--decision",
                "reject",
                "--note",
                "Test note",
            ]
            with patch("sys.argv", ["pivot_manager.py"] + args):
                with patch("builtins.print") as mock_print:
                    PIVOT.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertEqual("reject", parsed["decision"])

    def test_main_with_json_flag(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-flag"
            INIT.initialize_research_project(project_root=project_root, topic="JSON flag test")

            args = [
                "--json",
                "propose",
                "--project-root",
                str(project_root),
                "--pivot-type",
                "test",
                "--rationale",
                "JSON test",
            ]
            with patch("sys.argv", ["pivot_manager.py"] + args):
                with patch("builtins.print") as mock_print:
                    PIVOT.main()
                    call_args = mock_print.call_args[0][0]
                    # Should be indented JSON
                    self.assertIn("\n", call_args)
                    parsed = json.loads(call_args)
                    self.assertIn("pivot_id", parsed)

    def test_build_parser_propose_command(self) -> None:
        """Test build_parser with propose command."""
        parser = PIVOT.build_parser()
        args = parser.parse_args(
            [
                "propose",
                "--project-root",
                "/tmp",
                "--pivot-type",
                "test",
                "--rationale",
                "test rationale",
            ]
        )
        self.assertEqual("propose", args.command)
        self.assertEqual("test", args.pivot_type)

    def test_build_parser_review_command(self) -> None:
        """Test build_parser with review command."""
        parser = PIVOT.build_parser()
        args = parser.parse_args(
            [
                "review",
                "--project-root",
                "/tmp",
                "--pivot-id",
                "pivot-1",
                "--decision",
                "approve",
            ]
        )
        self.assertEqual("review", args.command)
        self.assertEqual("pivot-1", args.pivot_id)
        self.assertEqual("approve", args.decision)


if __name__ == "__main__":
    unittest.main()
