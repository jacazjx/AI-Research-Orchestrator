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

    def test_create_phase_directories(self) -> None:
        """Test create_phase_directories function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "phase-dirs"
            project_root.mkdir()

            result = MIGRATE.create_phase_directories(project_root)

            self.assertIsInstance(result, dict)
            self.assertTrue((project_root / "paper").exists())

    def test_create_admin_structure(self) -> None:
        """Test create_admin_structure function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "admin-structure"
            project_root.mkdir()

            result = MIGRATE.create_admin_structure(project_root, "Test topic")

            self.assertIn("created", result)
            self.assertTrue((project_root / ".autoresearch").exists())

    def test_main_outputs_json(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "JSON test",
                "--json",
            ]
            with patch("sys.argv", ["migrate_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    MIGRATE.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("project_root", parsed)

    def test_main_with_dry_run(self) -> None:
        """Test main with --dry-run flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-dry-run"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Dry run test",
                "--dry-run",
            ]
            with patch("sys.argv", ["migrate_project.py"] + args):
                with patch("builtins.print"):
                    result = MIGRATE.main()
                    self.assertEqual(0, result)

    def test_migrate_with_project_id(self) -> None:
        """Test migrate with explicit project_id."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project-id-test"
            project_root.mkdir()

            result = MIGRATE.migrate_project(
                project_root,
                topic="Project ID test",
                project_id="custom-id-123",
                dry_run=False,
            )

            # Check that migration succeeded
            self.assertTrue(result["success"])

            # Verify project_id was stored in the state file
            import yaml

            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            self.assertTrue(state_path.exists())
            with open(state_path) as f:
                state = yaml.safe_load(f)

            self.assertEqual("custom-id-123", state["project_id"])

    def test_create_config(self) -> None:
        """Test create_config function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "config-test"
            project_root.mkdir()

            result = MIGRATE.create_config(project_root)

            self.assertTrue(result["created"])
            config_path = project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
            self.assertTrue(config_path.exists())

    def test_create_config_already_exists(self) -> None:
        """Test create_config when config already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "config-exists"
            project_root.mkdir()

            # Create existing config
            config_path = project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
            config_path.parent.mkdir(parents=True)
            config_path.write_text("existing: config")

            result = MIGRATE.create_config(project_root)

            self.assertTrue(result["existed"])
            self.assertFalse(result["created"])

    def test_create_workspace_manifest(self) -> None:
        """Test create_workspace_manifest function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "manifest-test"
            project_root.mkdir()

            result = MIGRATE.create_workspace_manifest(project_root, "Test topic")

            self.assertTrue(result["created"])
            manifest_path = project_root / ".autoresearch" / "workspace-manifest.md"
            self.assertTrue(manifest_path.exists())

    def test_create_workspace_manifest_already_exists(self) -> None:
        """Test create_workspace_manifest when it already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "manifest-exists"
            project_root.mkdir()

            # Create existing manifest
            manifest_path = project_root / ".autoresearch" / "workspace-manifest.md"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text("existing manifest")

            result = MIGRATE.create_workspace_manifest(project_root, "Test topic")

            self.assertTrue(result["existed"])
            self.assertFalse(result["created"])

    def test_create_idea_brief_already_exists(self) -> None:
        """Test create_idea_brief when it already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "idea-exists"
            project_root.mkdir()

            # Create existing idea brief
            idea_path = project_root / ".autoresearch" / "idea-brief.md"
            idea_path.parent.mkdir(parents=True)
            idea_path.write_text("existing idea")

            result = MIGRATE.create_idea_brief(project_root, "Test topic")

            self.assertTrue(result["existed"])
            self.assertFalse(result["created"])

    def test_import_existing_files_bib(self) -> None:
        """Test import_existing_files with bib files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "import-bib"
            project_root.mkdir()

            # Create bib file
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")

            # Create analysis result
            analysis = {
                "literature_evidence": {
                    "bib_files": ["refs.bib"],
                    "reference_papers": [],
                }
            }

            result = MIGRATE.import_existing_files(project_root, analysis, dry_run=False)

            self.assertTrue(len(result["imported"]) > 0)
            # Check file was copied
            self.assertTrue(
                (project_root / ".autoresearch" / "reference-papers" / "refs.bib").exists()
            )

    def test_import_existing_files_pdf(self) -> None:
        """Test import_existing_files with PDF files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "import-pdf"
            project_root.mkdir()

            # Create PDF file
            (project_root / "paper.pdf").write_text("PDF content", encoding="utf-8")

            # Create analysis result
            analysis = {
                "literature_evidence": {
                    "bib_files": [],
                    "reference_papers": ["paper.pdf"],
                }
            }

            result = MIGRATE.import_existing_files(project_root, analysis, dry_run=False)

            self.assertTrue(len(result["imported"]) > 0)
            # Check file was copied
            self.assertTrue(
                (project_root / ".autoresearch" / "reference-papers" / "paper.pdf").exists()
            )

    def test_import_existing_files_dry_run(self) -> None:
        """Test import_existing_files in dry run mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "import-dry"
            project_root.mkdir()

            # Create bib file
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")

            analysis = {
                "literature_evidence": {
                    "bib_files": ["refs.bib"],
                    "reference_papers": [],
                }
            }

            result = MIGRATE.import_existing_files(project_root, analysis, dry_run=True)

            # Should have dry run message
            self.assertTrue(any("[DRY RUN]" in item for item in result["imported"]))
            # File should not be copied
            self.assertFalse(
                (project_root / ".autoresearch" / "reference-papers" / "refs.bib").exists()
            )

    def test_migrate_with_existing_files(self) -> None:
        """Test migration with existing literature files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "existing-files"
            project_root.mkdir()

            # Create existing files
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")
            (project_root / "paper.pdf").write_text("PDF", encoding="utf-8")

            result = MIGRATE.migrate_project(
                project_root,
                topic="Existing files test",
                dry_run=False,
            )

            self.assertTrue(result["success"])
            # Check import step completed
            self.assertIn("import_files", result["steps"])

    def test_format_report(self) -> None:
        """Test format_report function."""
        results = {
            "migration_time": "2024-01-01T00:00:00",
            "project_root": "/test/project",
            "dry_run": False,
            "success": True,
            "steps": {
                "analysis": {"status": "completed"},
                "create_directories": {"status": "completed", "created": ["paper", "code"]},
            },
        }

        report = MIGRATE.format_report(results)

        self.assertIn("Project Migration Report", report)
        self.assertIn("/test/project", report)
        self.assertIn("Success", report)

    def test_format_report_dry_run(self) -> None:
        """Test format_report for dry run."""
        results = {
            "migration_time": "2024-01-01T00:00:00",
            "project_root": "/test/project",
            "dry_run": True,
            "success": True,
            "steps": {},
        }

        report = MIGRATE.format_report(results)

        self.assertIn("dry run", report.lower())

    def test_create_research_state_auto_project_id(self) -> None:
        """Test create_research_state with auto-generated project_id."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "auto-id"
            project_root.mkdir()

            result = MIGRATE.create_research_state(project_root, topic="Auto ID test")

            self.assertTrue(result["created"])
            # Check state file
            state = COMMON.read_yaml(
                project_root / ".autoresearch" / "state" / "research-state.yaml"
            )
            self.assertIsNotNone(state.get("project_id"))

    def test_create_research_state_already_exists(self) -> None:
        """Test create_research_state when state already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "state-exists"
            project_root.mkdir()

            # Create existing state
            state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
            state_path.parent.mkdir(parents=True)
            state_path.write_text("existing: state")

            result = MIGRATE.create_research_state(project_root, topic="Test")

            self.assertTrue(result["existed"])
            self.assertFalse(result["created"])

    def test_main_with_starting_phase(self) -> None:
        """Test main with --starting-phase flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "starting-phase"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Starting phase test",
                "--starting-phase",
                "pilot",
                "--json",
            ]
            with patch("sys.argv", ["migrate_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = MIGRATE.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertTrue(parsed["success"])


if __name__ == "__main__":
    unittest.main()
