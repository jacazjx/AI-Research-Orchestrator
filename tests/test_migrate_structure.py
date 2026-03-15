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
MIGRATE = load_script_module("migrate_structure")


class MigrateStructureTest(unittest.TestCase):
    def test_has_old_structure_detects_old_dirs(self) -> None:
        """Test detection of old numbered structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "old-structure"
            project_root.mkdir()

            # Create old structure directory
            (project_root / "01-survey").mkdir()

            self.assertTrue(MIGRATE.has_old_structure(project_root))

    def test_has_old_structure_new_structure(self) -> None:
        """Test detection returns False for new structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "new-structure"
            project_root.mkdir()

            # Create new structure directories
            (project_root / "paper").mkdir()
            (project_root / "code").mkdir()

            self.assertFalse(MIGRATE.has_old_structure(project_root))

    def test_create_backup(self) -> None:
        """Test backup creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "backup-test"
            project_root.mkdir()

            # Create old directories with content
            (project_root / "01-survey").mkdir()
            (project_root / "01-survey" / "test.txt").write_text("test", encoding="utf-8")

            backup_path = MIGRATE.create_backup(project_root)

            self.assertTrue(backup_path.exists())
            self.assertTrue((backup_path / "01-survey" / "test.txt").exists())

    def test_create_new_structure(self) -> None:
        """Test creating new directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "new-dirs"
            project_root.mkdir()

            created = MIGRATE.create_new_structure(project_root, dry_run=False)

            # Check some expected directories were created
            self.assertTrue((project_root / "paper").exists())
            self.assertTrue((project_root / "code").exists())
            self.assertIsInstance(created, list)

    def test_create_new_structure_dry_run(self) -> None:
        """Test dry run doesn't create directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "dry-run"
            project_root.mkdir()

            created = MIGRATE.create_new_structure(project_root, dry_run=True)

            # Should contain dry run messages
            self.assertTrue(all("[DRY RUN]" in c for c in created))
            # Should not create actual directories
            self.assertFalse((project_root / "paper").exists())

    def test_migrate_files(self) -> None:
        """Test file migration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "migrate-files"
            project_root.mkdir()

            # Create old structure files
            (project_root / "00-admin").mkdir()
            (project_root / "00-admin" / "test.txt").write_text("content", encoding="utf-8")

            results = MIGRATE.migrate_files(project_root, dry_run=False)

            self.assertIn("migrated_files", results)
            self.assertIn("migrated_dirs", results)
            self.assertIn("skipped", results)
            self.assertIn("errors", results)

    def test_migrate_files_dry_run(self) -> None:
        """Test file migration dry run."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "migrate-dry"
            project_root.mkdir()

            # Create old structure
            (project_root / "01-survey").mkdir()
            (project_root / "01-survey" / "report.md").write_text("report", encoding="utf-8")

            results = MIGRATE.migrate_files(project_root, dry_run=True)

            # Should have migration entries but not actually move files
            self.assertIsInstance(results["migrated_files"], list)

    def test_remove_old_directories(self) -> None:
        """Test removal of old directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "remove-old"
            project_root.mkdir()

            # Create old directories
            (project_root / "01-survey").mkdir()
            (project_root / "02-pilot-analysis").mkdir()

            removed = MIGRATE.remove_old_directories(project_root, dry_run=False)

            # Old directories should be removed
            self.assertFalse((project_root / "01-survey").exists())
            self.assertFalse((project_root / "02-pilot-analysis").exists())
            self.assertIn("01-survey", removed)

    def test_remove_old_directories_dry_run(self) -> None:
        """Test dry run doesn't remove directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "remove-dry"
            project_root.mkdir()

            # Create old directory
            (project_root / "01-survey").mkdir()

            removed = MIGRATE.remove_old_directories(project_root, dry_run=True)

            # Directory should still exist
            self.assertTrue((project_root / "01-survey").exists())
            # Dry run message should be present
            self.assertTrue(any("[DRY RUN]" in r for r in removed))

    def test_update_state_file(self) -> None:
        """Test updating state file with new phase names."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "update-state"
            INIT.initialize_research_project(project_root=project_root, topic="Test")

            # Update state to use old phase name
            state = COMMON.load_state(project_root)
            state["current_phase"] = "01-survey"
            state["phase_reviews"] = {"01-survey": {"score": 4.0}}
            COMMON.save_state(project_root, state)

            result = MIGRATE.update_state_file(project_root, dry_run=False)

            # Check state was updated
            updated_state = COMMON.load_state(project_root)
            self.assertEqual(updated_state["current_phase"], "survey")
            self.assertIn("survey", updated_state["phase_reviews"])

    def test_update_state_file_dry_run(self) -> None:
        """Test state update dry run."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "update-dry"
            INIT.initialize_research_project(project_root=project_root, topic="Test")

            result = MIGRATE.update_state_file(project_root, dry_run=True)

            self.assertTrue(result.get("dry_run", False))

    def test_update_state_file_no_state(self) -> None:
        """Test state update when no state file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-state"
            project_root.mkdir()

            result = MIGRATE.update_state_file(project_root, dry_run=False)

            self.assertFalse(result["updated"])

    def test_migrate_project_no_old_structure(self) -> None:
        """Test migration when project has no old structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-old"
            project_root.mkdir()

            # Create new structure
            (project_root / "paper").mkdir()

            result = MIGRATE.migrate_project(project_root, dry_run=False)

            self.assertFalse(result["has_old_structure"])
            self.assertIn("message", result)

    def test_migrate_project_with_old_structure(self) -> None:
        """Test full migration with old structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "full-migrate"
            project_root.mkdir()

            # Create old structure
            (project_root / "01-survey").mkdir()
            (project_root / "01-survey" / "report.md").write_text("report", encoding="utf-8")

            result = MIGRATE.migrate_project(project_root, dry_run=False, backup=True)

            self.assertTrue(result["has_old_structure"])
            self.assertTrue(result["success"])
            self.assertIsNotNone(result["backup_path"])

    def test_migrate_project_dry_run(self) -> None:
        """Test full migration dry run."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "full-dry"
            project_root.mkdir()

            # Create old structure
            (project_root / "01-survey").mkdir()

            result = MIGRATE.migrate_project(project_root, dry_run=True)

            self.assertTrue(result["dry_run"])
            # Old structure should still exist
            self.assertTrue((project_root / "01-survey").exists())

    def test_migrate_project_no_backup(self) -> None:
        """Test migration without backup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-backup"
            project_root.mkdir()

            # Create old structure
            (project_root / "01-survey").mkdir()

            result = MIGRATE.migrate_project(project_root, dry_run=False, backup=False)

            self.assertTrue(result["success"])
            self.assertIsNone(result["backup_path"])

    def test_format_report(self) -> None:
        """Test report formatting."""
        results = {
            "project_root": "/test/project",
            "dry_run": False,
            "success": True,
            "has_old_structure": True,
            "backup_path": "/test/backup",
            "created_directories": ["paper", "code"],
            "migrated_files": [("old/path", "new/path")],
            "migrated_dirs": [],
            "state_updated": {"updated": True, "old_phase": "01-survey", "new_phase": "survey"},
            "removed_directories": ["01-survey"],
            "errors": [],
        }

        report = MIGRATE.format_report(results)

        self.assertIn("Project Structure Migration Report", report)
        self.assertIn("/test/project", report)
        self.assertIn("Created Directories", report)
        self.assertIn("Migrated Files", report)
        self.assertIn("State File Updated", report)

    def test_format_report_dry_run(self) -> None:
        """Test report formatting for dry run."""
        results = {
            "project_root": "/test/project",
            "dry_run": True,
            "success": True,
            "has_old_structure": True,
            "backup_path": None,
            "created_directories": [],
            "migrated_files": [],
            "migrated_dirs": [],
            "state_updated": {},
            "removed_directories": [],
            "errors": [],
        }

        report = MIGRATE.format_report(results)

        self.assertIn("dry run", report.lower())

    def test_format_report_with_errors(self) -> None:
        """Test report formatting with errors."""
        results = {
            "project_root": "/test/project",
            "dry_run": False,
            "success": False,
            "has_old_structure": True,
            "backup_path": None,
            "created_directories": [],
            "migrated_files": [],
            "migrated_dirs": [],
            "state_updated": {},
            "removed_directories": [],
            "errors": ["Test error", ("file.txt", "File not found")],
        }

        report = MIGRATE.format_report(results)

        self.assertIn("Errors", report)
        self.assertIn("Test error", report)

    def test_format_report_no_old_structure(self) -> None:
        """Test report formatting when no old structure."""
        results = {
            "project_root": "/test/project",
            "dry_run": False,
            "success": True,
            "has_old_structure": False,
            "message": "No old structure detected",
            "backup_path": None,
            "created_directories": [],
            "migrated_files": [],
            "migrated_dirs": [],
            "state_updated": {},
            "removed_directories": [],
            "errors": [],
        }

        report = MIGRATE.format_report(results)

        self.assertIn("No old structure detected", report)

    def test_main_with_json_output(self) -> None:
        """Test main function with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--json",
            ]
            with patch("sys.argv", ["migrate_structure.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = MIGRATE.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("project_root", parsed)

    def test_main_with_dry_run(self) -> None:
        """Test main function with --dry-run flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-dry"
            project_root.mkdir()
            (project_root / "01-survey").mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--dry-run",
            ]
            with patch("sys.argv", ["migrate_structure.py"] + args):
                with patch("builtins.print"):
                    result = MIGRATE.main()
                    self.assertEqual(0, result)

    def test_main_with_no_backup(self) -> None:
        """Test main function with --no-backup flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-nobackup"
            project_root.mkdir()
            (project_root / "01-survey").mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--no-backup",
            ]
            with patch("sys.argv", ["migrate_structure.py"] + args):
                with patch("builtins.print"):
                    result = MIGRATE.main()
                    self.assertEqual(0, result)

    def test_main_nonexistent_project(self) -> None:
        """Test main with nonexistent project root."""
        args = [
            "--project-root",
            "/nonexistent/path",
            "--json",
        ]
        with patch("sys.argv", ["migrate_structure.py"] + args):
            result = MIGRATE.main()
            self.assertEqual(1, result)

    def test_phase_name_mapping(self) -> None:
        """Test that phase name mapping is correct."""
        mapping = MIGRATE.PHASE_NAME_MAPPING

        self.assertEqual(mapping["01-survey"], "survey")
        self.assertEqual(mapping["02-pilot-analysis"], "pilot")
        self.assertEqual(mapping["03-full-experiments"], "experiments")
        self.assertEqual(mapping["04-paper"], "paper")
        self.assertEqual(mapping["05-reflection-evolution"], "reflection")

    def test_legacy_phase_directories(self) -> None:
        """Test that legacy phase directories list is correct."""
        legacy_dirs = MIGRATE.LEGACY_PHASE_DIRECTORIES

        self.assertIn("01-survey", legacy_dirs)
        self.assertIn("02-pilot-analysis", legacy_dirs)
        self.assertIn("03-full-experiments", legacy_dirs)
        self.assertIn("04-paper", legacy_dirs)
        self.assertIn("05-reflection-evolution", legacy_dirs)


if __name__ == "__main__":
    unittest.main()
