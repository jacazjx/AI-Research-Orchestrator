"""Tests for legacy_handler.py module.

Tests cover:
- Directory analysis and pattern detection
- Legacy backup creation
- Content extraction from legacy files
- Migration handling modes
- Report generation
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import exceptions first, then legacy_handler to ensure consistent module references
import exceptions as EXCEPTIONS  # noqa: E402
import legacy_handler as LEGACY  # noqa: E402


class DirectoryAnalysisTest(unittest.TestCase):
    """Tests for DirectoryAnalysis dataclass."""

    def test_dataclass_creation(self) -> None:
        """Test DirectoryAnalysis can be created with default values."""
        analysis = LEGACY.DirectoryAnalysis(
            is_empty=True,
            total_files=0,
        )

        self.assertTrue(analysis.is_empty)
        self.assertEqual(analysis.total_files, 0)
        self.assertEqual(analysis.recognized_patterns, {})
        self.assertEqual(analysis.orphan_files, [])
        self.assertEqual(analysis.recommended_actions, [])

    def test_dataclass_with_values(self) -> None:
        """Test DirectoryAnalysis with populated values."""
        analysis = LEGACY.DirectoryAnalysis(
            is_empty=False,
            total_files=10,
            recognized_patterns={"code": ["main.py"]},
            orphan_files=["unknown.xyz"],
            recommended_actions=[{"action": "migrate"}],
        )

        self.assertFalse(analysis.is_empty)
        self.assertEqual(analysis.total_files, 10)
        self.assertIn("code", analysis.recognized_patterns)


class MigrationResultTest(unittest.TestCase):
    """Tests for MigrationResult dataclass."""

    def test_dataclass_creation(self) -> None:
        """Test MigrationResult can be created with default values."""
        result = LEGACY.MigrationResult(success=True)

        self.assertTrue(result.success)
        self.assertIsNone(result.legacy_path)
        self.assertEqual(result.migrated_files, [])
        self.assertEqual(result.extracted_content, {})
        self.assertEqual(result.report, "")

    def test_dataclass_with_values(self) -> None:
        """Test MigrationResult with populated values."""
        result = LEGACY.MigrationResult(
            success=True,
            legacy_path="/path/to/legacy",
            migrated_files=["file1.txt", "file2.txt"],
            extracted_content={"paper_titles": ["Test Paper"]},
            report="Migration completed",
        )

        self.assertTrue(result.success)
        self.assertEqual(result.legacy_path, "/path/to/legacy")
        self.assertEqual(len(result.migrated_files), 2)


class AnalyzeDirectoryContentsTest(unittest.TestCase):
    """Tests for analyze_directory_contents function."""

    def test_empty_directory(self) -> None:
        """Test analysis of an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "empty-project"
            project_root.mkdir()

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertTrue(analysis.is_empty)
            self.assertEqual(analysis.total_files, 0)

    def test_nonexistent_directory(self) -> None:
        """Test analysis raises error for nonexistent directory."""
        with self.assertRaises(LEGACY.LegacyHandlerError):
            LEGACY.analyze_directory_contents(Path("/nonexistent/path"))

    def test_file_not_directory(self) -> None:
        """Test analysis raises error when path is a file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "notadir.txt"
            file_path.write_text("content", encoding="utf-8")

            with self.assertRaises(LEGACY.LegacyHandlerError):
                LEGACY.analyze_directory_contents(file_path)

    def test_recognizes_paper_draft_files(self) -> None:
        """Test recognition of paper draft files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "paper-project"
            project_root.mkdir()
            (project_root / "draft.tex").write_text("\\title{Test}", encoding="utf-8")
            (project_root / "notes.md").write_text("# Notes", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertIn("paper_draft", analysis.recognized_patterns)

    def test_recognizes_code_files(self) -> None:
        """Test recognition of code files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "code-project"
            project_root.mkdir()
            (project_root / "main.py").write_text("print('hello')", encoding="utf-8")
            (project_root / "analysis.ipynb").write_text("{}", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertIn("code", analysis.recognized_patterns)

    def test_recognizes_data_files(self) -> None:
        """Test recognition of data files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "data-project"
            project_root.mkdir()
            (project_root / "data.csv").write_text("col1,col2", encoding="utf-8")
            (project_root / "results.json").write_text("{}", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertIn("data", analysis.recognized_patterns)

    def test_recognizes_reference_files(self) -> None:
        """Test recognition of reference files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "ref-project"
            project_root.mkdir()
            (project_root / "refs.bib").write_text("@article{test}", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertIn("references", analysis.recognized_patterns)

    def test_identifies_orphan_files(self) -> None:
        """Test identification of files not matching patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "orphan-project"
            project_root.mkdir()
            (project_root / "weird.xyz").write_text("unknown format", encoding="utf-8")
            (project_root / "random.dat").write_text("data", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertEqual(len(analysis.orphan_files), 2)

    def test_skips_hidden_directories(self) -> None:
        """Test that hidden directories are excluded from analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "hidden-project"
            project_root.mkdir()
            (project_root / ".git").mkdir()
            (project_root / ".git" / "config").write_text("config", encoding="utf-8")
            (project_root / "public.py").write_text("public", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            # Should not count hidden files
            all_files = []
            for files in analysis.recognized_patterns.values():
                all_files.extend(files)
            all_files.extend(analysis.orphan_files)

            self.assertNotIn(".git/config", all_files)

    def test_skips_node_modules_and_pycache(self) -> None:
        """Test that node_modules and __pycache__ are excluded."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "exclude-project"
            project_root.mkdir()
            (project_root / "node_modules").mkdir()
            (project_root / "node_modules" / "package.js").write_text("js", encoding="utf-8")
            (project_root / "__pycache__").mkdir()
            (project_root / "__pycache__" / "module.pyc").write_text("pyc", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            all_files = []
            for files in analysis.recognized_patterns.values():
                all_files.extend(files)
            all_files.extend(analysis.orphan_files)

            self.assertNotIn("node_modules/package.js", all_files)
            self.assertNotIn("__pycache__/module.pyc", all_files)

    def test_skips_orchestrator_directories(self) -> None:
        """Test that orchestrator structure directories are skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "orch-project"
            project_root.mkdir()
            (project_root / "paper").mkdir()
            (project_root / "paper" / "draft.md").write_text("# Draft", encoding="utf-8")
            (project_root / "code").mkdir()
            (project_root / "code" / "main.py").write_text("print()", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            # Files in orchestrator dirs should not be counted as orphans
            self.assertEqual(len(analysis.orphan_files), 0)

    def test_generates_recommendations(self) -> None:
        """Test that recommendations are generated for large file counts."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "recommend-project"
            project_root.mkdir()

            # Create many orphan files
            for i in range(15):
                (project_root / f"file{i}.xyz").write_text("data", encoding="utf-8")

            analysis = LEGACY.analyze_directory_contents(project_root)

            self.assertTrue(len(analysis.recommended_actions) > 0)


class CreateLegacyBackupTest(unittest.TestCase):
    """Tests for create_legacy_backup function."""

    def test_creates_backup_directory(self) -> None:
        """Test that backup directory is created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "backup-test"
            project_root.mkdir()
            (project_root / "orphan.xyz").write_text("content", encoding="utf-8")

            legacy_path = LEGACY.create_legacy_backup(project_root, ["orphan.xyz"])

            self.assertTrue(legacy_path.exists())
            self.assertTrue(legacy_path.name.isdigit() or "_" in legacy_path.name)

    def test_moves_files_to_backup(self) -> None:
        """Test that files are moved to backup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "move-test"
            project_root.mkdir()
            (project_root / "file1.xyz").write_text("content1", encoding="utf-8")
            (project_root / "file2.xyz").write_text("content2", encoding="utf-8")

            legacy_path = LEGACY.create_legacy_backup(project_root, ["file1.xyz", "file2.xyz"])

            # Original files should be gone
            self.assertFalse((project_root / "file1.xyz").exists())
            self.assertFalse((project_root / "file2.xyz").exists())

            # Files should be in backup
            self.assertTrue((legacy_path / "file1.xyz").exists())
            self.assertTrue((legacy_path / "file2.xyz").exists())

    def test_creates_manifest(self) -> None:
        """Test that manifest.json is created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "manifest-test"
            project_root.mkdir()
            (project_root / "file.xyz").write_text("content", encoding="utf-8")

            legacy_path = LEGACY.create_legacy_backup(project_root, ["file.xyz"])

            manifest_path = legacy_path / "manifest.json"
            self.assertTrue(manifest_path.exists())

            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)

            self.assertEqual(manifest["total_files"], 1)
            self.assertEqual(manifest["migrated_count"], 1)

    def test_handles_nested_files(self) -> None:
        """Test that nested files are properly moved."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "nested-test"
            project_root.mkdir()
            (project_root / "subdir").mkdir()
            (project_root / "subdir" / "nested.xyz").write_text("nested", encoding="utf-8")

            legacy_path = LEGACY.create_legacy_backup(project_root, ["subdir/nested.xyz"])

            self.assertTrue((legacy_path / "subdir" / "nested.xyz").exists())

    def test_raises_error_for_no_files(self) -> None:
        """Test that error is raised when no files provided."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-files"
            project_root.mkdir()

            with self.assertRaises(LEGACY.LegacyHandlerError):
                LEGACY.create_legacy_backup(project_root, [])

    def test_handles_missing_source_files(self) -> None:
        """Test that missing source files are recorded in manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "missing-test"
            project_root.mkdir()

            # Create one file, but try to migrate two
            (project_root / "exists.xyz").write_text("content", encoding="utf-8")

            legacy_path = LEGACY.create_legacy_backup(project_root, ["exists.xyz", "missing.xyz"])

            manifest_path = legacy_path / "manifest.json"
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)

            # Should have one error for missing file
            self.assertEqual(len(manifest["errors"]), 1)


class ExtractValuableContentTest(unittest.TestCase):
    """Tests for extract_valuable_content function."""

    def test_extracts_from_markdown(self) -> None:
        """Test extraction from markdown files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            legacy_path = Path(temp_dir) / "extract-md"
            legacy_path.mkdir()
            (legacy_path / "notes.md").write_text(
                "# My Research Paper Title\n\nContent here.", encoding="utf-8"
            )

            extracted = LEGACY.extract_valuable_content(legacy_path)

            self.assertIn("My Research Paper Title", extracted["paper_titles"])

    def test_extracts_from_bibtex(self) -> None:
        """Test extraction from BibTeX files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            legacy_path = Path(temp_dir) / "extract-bib"
            legacy_path.mkdir()
            (legacy_path / "refs.bib").write_text(
                "@article{smith2023, title={Test}}\n@inproceedings{jones2022, title={Other}}",
                encoding="utf-8",
            )

            extracted = LEGACY.extract_valuable_content(legacy_path)

            self.assertIn("smith2023", extracted["references"])
            self.assertIn("jones2022", extracted["references"])

    def test_extracts_from_python(self) -> None:
        """Test extraction from Python files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            legacy_path = Path(temp_dir) / "extract-py"
            legacy_path.mkdir()
            (legacy_path / "module.py").write_text(
                "class Model:\n    pass\n\ndef train():\n    pass\ndef evaluate():\n    pass",
                encoding="utf-8",
            )

            extracted = LEGACY.extract_valuable_content(legacy_path)

            self.assertEqual(len(extracted["code_modules"]), 1)
            self.assertIn("Model", extracted["code_modules"][0]["classes"])

    def test_records_data_files(self) -> None:
        """Test recording of data files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            legacy_path = Path(temp_dir) / "extract-data"
            legacy_path.mkdir()
            (legacy_path / "data.csv").write_text("col1,col2\n1,2", encoding="utf-8")
            (legacy_path / "model.pt").write_text("binary", encoding="utf-8")

            extracted = LEGACY.extract_valuable_content(legacy_path)

            self.assertEqual(len(extracted["data_files"]), 2)

    def test_handles_nonexistent_path(self) -> None:
        """Test error handling for nonexistent path."""
        with self.assertRaises(LEGACY.LegacyHandlerError):
            LEGACY.extract_valuable_content(Path("/nonexistent/path"))

    def test_skips_manifest_file(self) -> None:
        """Test that manifest.json is skipped during extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            legacy_path = Path(temp_dir) / "extract-manifest"
            legacy_path.mkdir()
            (legacy_path / "manifest.json").write_text('{"test": true}', encoding="utf-8")

            extracted = LEGACY.extract_valuable_content(legacy_path)

            self.assertEqual(extracted["metadata"]["files_analyzed"], 0)


class HandleNonEmptyDirectoryTest(unittest.TestCase):
    """Tests for handle_non_empty_directory function."""

    def test_migrate_mode(self) -> None:
        """Test migrate mode moves orphan files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "migrate-test"
            project_root.mkdir()
            (project_root / "orphan.xyz").write_text("content", encoding="utf-8")

            result = LEGACY.handle_non_empty_directory(project_root, "migrate")

            self.assertTrue(result.success)
            self.assertIsNotNone(result.legacy_path)
            self.assertIn("orphan.xyz", result.migrated_files)

    def test_preserve_mode(self) -> None:
        """Test preserve mode keeps files in place."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "preserve-test"
            project_root.mkdir()
            (project_root / "file.xyz").write_text("content", encoding="utf-8")

            result = LEGACY.handle_non_empty_directory(project_root, "preserve")

            self.assertTrue(result.success)
            self.assertIsNone(result.legacy_path)
            # File should still exist
            self.assertTrue((project_root / "file.xyz").exists())

    def test_cancel_mode(self) -> None:
        """Test cancel mode returns empty result."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "cancel-test"
            project_root.mkdir()

            result = LEGACY.handle_non_empty_directory(project_root, "cancel")

            self.assertTrue(result.success)
            self.assertIsNone(result.legacy_path)
            self.assertEqual(len(result.migrated_files), 0)
            self.assertIn("cancelled", result.report.lower())

    def test_invalid_mode(self) -> None:
        """Test that invalid mode raises ValidationError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "invalid-test"
            project_root.mkdir()

            with self.assertRaises(LEGACY.ValidationError):
                LEGACY.handle_non_empty_directory(project_root, "invalid")

    def test_no_orphans_to_migrate(self) -> None:
        """Test handling when no orphan files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-orphans"
            project_root.mkdir()
            (project_root / "code").mkdir()
            (project_root / "code" / "main.py").write_text("print()", encoding="utf-8")

            result = LEGACY.handle_non_empty_directory(project_root, "migrate")

            self.assertTrue(result.success)
            self.assertIsNone(result.legacy_path)  # No legacy path created

    def test_custom_files_to_migrate(self) -> None:
        """Test migrating specific files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "custom-test"
            project_root.mkdir()
            (project_root / "file1.xyz").write_text("content1", encoding="utf-8")
            (project_root / "file2.xyz").write_text("content2", encoding="utf-8")

            result = LEGACY.handle_non_empty_directory(
                project_root, "migrate", files_to_migrate=["file1.xyz"]
            )

            self.assertTrue(result.success)
            self.assertEqual(len(result.migrated_files), 1)
            self.assertIn("file1.xyz", result.migrated_files)


class GenerateMigrationReportTest(unittest.TestCase):
    """Tests for generate_migration_report function."""

    def test_generates_report(self) -> None:
        """Test report generation."""
        analysis = LEGACY.DirectoryAnalysis(
            is_empty=False,
            total_files=5,
            recognized_patterns={"code": ["main.py"]},
            orphan_files=["orphan.xyz"],
            recommended_actions=[],
        )
        result = LEGACY.MigrationResult(
            success=True,
            legacy_path="/path/to/legacy",
            migrated_files=["orphan.xyz"],
        )

        report = LEGACY.generate_migration_report(analysis, result)

        self.assertIn("Directory Migration Report", report)
        self.assertIn("Total Files Analyzed", report)
        self.assertIn("Orphan Files", report)
        self.assertIn("Recognized File Patterns", report)

    def test_includes_extracted_content(self) -> None:
        """Test report includes extracted content."""
        analysis = LEGACY.DirectoryAnalysis(
            is_empty=False,
            total_files=1,
            orphan_files=["paper.md"],
        )
        result = LEGACY.MigrationResult(
            success=True,
            legacy_path="/path/to/legacy",
            extracted_content={"paper_titles": ["My Paper"]},
        )

        report = LEGACY.generate_migration_report(analysis, result)

        self.assertIn("Extracted Content", report)
        self.assertIn("My Paper", report)


class FormatAnalysisSummaryTest(unittest.TestCase):
    """Tests for format_analysis_summary function."""

    def test_empty_directory_summary(self) -> None:
        """Test summary for empty directory."""
        analysis = LEGACY.DirectoryAnalysis(is_empty=True, total_files=0)

        summary = LEGACY.format_analysis_summary(analysis)

        self.assertIn("empty", summary.lower())

    def test_non_empty_summary(self) -> None:
        """Test summary for non-empty directory."""
        analysis = LEGACY.DirectoryAnalysis(
            is_empty=False,
            total_files=10,
            recognized_patterns={"code": ["main.py", "utils.py"]},
            orphan_files=["unknown.xyz"],
        )

        summary = LEGACY.format_analysis_summary(analysis)

        self.assertIn("10 files", summary)
        self.assertIn("code", summary)
        self.assertIn("Orphan", summary)


class MainFunctionTest(unittest.TestCase):
    """Tests for main() function."""

    def test_analyze_mode_json(self) -> None:
        """Test analyze mode with JSON output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-analyze"
            project_root.mkdir()

            args = [
                "--project-root",
                str(project_root),
                "--mode",
                "analyze",
                "--json",
            ]
            with patch("sys.argv", ["legacy_handler.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = LEGACY.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("total_files", parsed)

    def test_migrate_mode_quiet(self) -> None:
        """Test migrate mode with quiet output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-migrate"
            project_root.mkdir()
            (project_root / "orphan.xyz").write_text("content", encoding="utf-8")

            args = [
                "--project-root",
                str(project_root),
                "--mode",
                "migrate",
                "--quiet",
            ]
            with patch("sys.argv", ["legacy_handler.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = LEGACY.main()
                    self.assertEqual(0, result)
                    mock_print.assert_called()

    def test_nonexistent_project(self) -> None:
        """Test with nonexistent project root."""
        args = [
            "--project-root",
            "/nonexistent/path",
            "--mode",
            "analyze",
        ]
        with patch("sys.argv", ["legacy_handler.py"] + args):
            result = LEGACY.main()
            self.assertEqual(1, result)


class PatternMatchingTest(unittest.TestCase):
    """Tests for pattern matching functions."""

    def test_match_pattern_glob(self) -> None:
        """Test glob pattern matching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            file_path = base_path / "test.py"

            self.assertTrue(LEGACY._match_pattern(file_path, "*.py", base_path))
            self.assertFalse(LEGACY._match_pattern(file_path, "*.txt", base_path))

    def test_match_pattern_directory(self) -> None:
        """Test directory pattern matching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            (base_path / "paper").mkdir()
            file_path = base_path / "paper" / "draft.md"

            self.assertTrue(LEGACY._match_pattern(file_path, "paper/**", base_path))
            self.assertFalse(LEGACY._match_pattern(file_path, "code/**", base_path))

    def test_get_file_category(self) -> None:
        """Test file category detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)

            py_file = base_path / "main.py"
            self.assertEqual(LEGACY._get_file_category(py_file, base_path), "code")

            bib_file = base_path / "refs.bib"
            self.assertEqual(LEGACY._get_file_category(bib_file, base_path), "references")

            unknown_file = base_path / "weird.xyz"
            self.assertIsNone(LEGACY._get_file_category(unknown_file, base_path))


class LegacyHandlerErrorTest(unittest.TestCase):
    """Tests for LegacyHandlerError exception."""

    def test_error_creation(self) -> None:
        """Test error can be created with all attributes."""
        error = LEGACY.LegacyHandlerError(
            "Test error",
            path="/test/path",
            operation="test",
        )

        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.path, "/test/path")
        self.assertEqual(error.operation, "test")

    def test_error_inheritance(self) -> None:
        """Test error inherits from OrchestratorError."""
        error = LEGACY.LegacyHandlerError("Test")
        self.assertIsInstance(error, EXCEPTIONS.OrchestratorError)


if __name__ == "__main__":
    unittest.main()
