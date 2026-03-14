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


ANALYZE = load_script_module("analyze_project")
MIGRATE = load_script_module("migrate_project")


class AnalyzeProjectTest(unittest.TestCase):
    def test_analyze_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "empty-project"
            project_root.mkdir()

            analysis = ANALYZE.analyze_project(project_root)

            self.assertTrue(analysis["project_exists"])
            self.assertEqual(analysis["summary"]["total_files"], 0)
            self.assertEqual(analysis["summary"]["deliverables_found"], 0)
            self.assertFalse(analysis["research_state"]["exists"])

    def test_analyze_detects_python_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "python-project"
            project_root.mkdir()

            # Create some Python files
            (project_root / "train.py").write_text("# training script")
            (project_root / "eval.py").write_text("# eval script")

            analysis = ANALYZE.analyze_project(project_root)

            self.assertIn("experiment_code", analysis["file_patterns"])
            self.assertTrue(len(analysis["file_patterns"]["experiment_code"]) >= 2)

    def test_estimate_phase_for_empty_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "empty-project"
            project_root.mkdir()

            estimate = ANALYZE.estimate_project_phase(project_root)

            # Should return 'survey' for empty project (new semantic name)
            self.assertEqual(estimate["estimated_phase"], "survey")
            self.assertEqual(estimate["confidence"], "low")

    def test_detect_file_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "patterns-project"
            project_root.mkdir()

            # Create files with different patterns
            (project_root / "paper.md").write_text("# Paper")
            (project_root / "refs.bib").write_text("@article{test}")
            (project_root / "data.csv").write_text("col1,col2")

            patterns = ANALYZE.detect_file_patterns(project_root)

            self.assertTrue(len(patterns["paper_draft"]) > 0)
            self.assertTrue(len(patterns["bibliography"]) > 0)
            self.assertTrue(len(patterns["data_files"]) > 0)


class MigrateProjectTest(unittest.TestCase):
    def test_migrate_creates_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "migrate-test"
            project_root.mkdir()

            results = MIGRATE.migrate_project(
                project_root,
                topic="Test migration",
                dry_run=False,
            )

            # Check new structure directories were created
            self.assertTrue((project_root / "paper").exists())
            self.assertTrue((project_root / "code").exists())
            self.assertTrue((project_root / "docs").exists())
            self.assertTrue((project_root / "agents").exists())
            self.assertTrue((project_root / ".autoresearch").exists())

    def test_migrate_creates_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "state-test"
            project_root.mkdir()

            results = MIGRATE.migrate_project(
                project_root,
                topic="State test",
                project_id="test-project-001",
                dry_run=False,
            )

            # Check state file was created in new location
            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            self.assertTrue(state_path.exists())

    def test_migrate_creates_idea_brief(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "idea-test"
            project_root.mkdir()

            results = MIGRATE.migrate_project(
                project_root,
                topic="Idea test topic",
                dry_run=False,
            )

            # Check idea brief was created in new location
            idea_path = project_root / ".autoresearch" / "idea-brief.md"
            self.assertTrue(idea_path.exists())

            content = idea_path.read_text()
            self.assertIn("Idea test topic", content)

    def test_migrate_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "dry-run-test"
            project_root.mkdir()

            results = MIGRATE.migrate_project(
                project_root,
                topic="Dry run test",
                dry_run=True,
            )

            self.assertTrue(results["dry_run"])
            # Check that directories were NOT created
            self.assertFalse((project_root / ".autoresearch").exists())

    def test_migrate_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-overwrite"
            project_root.mkdir()

            # Create existing state file in new location
            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            state_path.parent.mkdir(parents=True)
            state_path.write_text("existing: content")

            results = MIGRATE.migrate_project(
                project_root,
                topic="No overwrite test",
                dry_run=False,
            )

            # State should not be overwritten
            self.assertEqual(results["steps"]["create_state"]["status"], "skipped")

    def test_migrate_with_explicit_starting_phase(self) -> None:
        """Test that explicit starting_phase overrides auto-detected phase."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "explicit-phase"
            project_root.mkdir()

            # Create a paper draft (would normally auto-detect as paper)
            (project_root / "draft.md").write_text("# Paper Draft\n\n## Abstract\n...")

            results = MIGRATE.migrate_project(
                project_root,
                topic="Explicit phase test",
                starting_phase="pilot",  # Use new semantic name
                dry_run=False,
            )

            # Should use explicit phase, not auto-detected
            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            self.assertTrue(state_path.exists())

            import yaml
            with open(state_path) as f:
                state = yaml.safe_load(f)

            # Should use new semantic name
            self.assertEqual(state["current_phase"], "pilot")
            self.assertEqual(state["current_gate"], "gate_2")

    def test_migrate_auto_detect_phase(self) -> None:
        """Test that phase is auto-detected when not specified."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "auto-phase"
            project_root.mkdir()

            # Create experiment files
            (project_root / "experiment.py").write_text("# experiment")
            (project_root / "results.csv").write_text("col1,col2")

            results = MIGRATE.migrate_project(
                project_root,
                topic="Auto phase test",
                dry_run=False,
            )

            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            self.assertTrue(state_path.exists())

            import yaml
            with open(state_path) as f:
                state = yaml.safe_load(f)

            # Should detect experiments and set appropriate phase (using new semantic names)
            self.assertIn(state["current_phase"], ["pilot", "experiments"])


if __name__ == "__main__":
    unittest.main()