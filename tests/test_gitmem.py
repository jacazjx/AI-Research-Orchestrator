"""Tests for GitMem integration in orchestrator_common.py."""

import importlib.util
import subprocess
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


class GitMemInitTest(unittest.TestCase):
    """Tests for gitmem_init function."""

    def test_init_creates_gitmem_directory(self) -> None:
        """Test that gitmem_init creates .gitmem directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            gitmem_path = project_root / ".gitmem"
            self.assertTrue(gitmem_path.exists())
            self.assertTrue((gitmem_path / ".gitignore").exists())

    def test_init_creates_git_repo(self) -> None:
        """Test that gitmem_init initializes a git repo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            # Check that git repo is initialized
            result = subprocess.run(
                ["git", "-C", str(project_root / ".gitmem"), "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)

    def test_init_updates_gitignore(self) -> None:
        """Test that gitmem_init updates main project's .gitignore."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            gitignore = project_root / ".gitignore"
            self.assertTrue(gitignore.exists())
            content = gitignore.read_text(encoding="utf-8")
            self.assertIn(".gitmem", content)

    def test_init_idempotent(self) -> None:
        """Test that calling gitmem_init twice doesn't fail."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)
            COMMON.gitmem_init(project_root)  # Should not raise

            self.assertTrue(COMMON.gitmem_is_initialized(project_root))

    def test_init_during_project_initialization(self) -> None:
        """Test that init_research_project calls gitmem_init."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "gitmem-init-test"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="GitMem init test",
            )

            # Check that .gitmem was created
            gitmem_path = project_root / ".gitmem"
            self.assertTrue(gitmem_path.exists(), ".gitmem directory should be created")


class GitMemCommitTest(unittest.TestCase):
    """Tests for gitmem_commit function."""

    def setUp(self) -> None:
        """Set up a test project with GitMem initialized."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        # Initialize GitMem
        COMMON.gitmem_init(self.project_root)

        # Create a test file in a tracked directory
        test_file = self.project_root / "docs/reports/test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Test content\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_commit_returns_hash(self) -> None:
        """Test that gitmem_commit returns a commit hash."""
        commit_hash = COMMON.gitmem_commit(
            self.project_root,
            "docs/reports/test.md",
            "Initial commit",
        )

        self.assertIsInstance(commit_hash, str)
        self.assertEqual(len(commit_hash), 40)  # SHA-1 hash length

    def test_commit_creates_new_revision(self) -> None:
        """Test that multiple commits create different revisions."""
        hash1 = COMMON.gitmem_commit(
            self.project_root,
            "docs/reports/test.md",
            "First commit",
        )

        # Modify file
        test_file = self.project_root / "docs/reports/test.md"
        test_file.write_text("# Modified content\n", encoding="utf-8")

        hash2 = COMMON.gitmem_commit(
            self.project_root,
            "docs/reports/test.md",
            "Second commit",
        )

        self.assertNotEqual(hash1, hash2)

    def test_commit_nonexistent_file_raises(self) -> None:
        """Test that committing nonexistent file raises error."""
        with self.assertRaises(ValueError):
            COMMON.gitmem_commit(
                self.project_root,
                "docs/reports/nonexistent.md",
                "Should fail",
            )


class GitMemCheckpointTest(unittest.TestCase):
    """Tests for gitmem_checkpoint function."""

    def setUp(self) -> None:
        """Set up a test project with GitMem and commits."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        COMMON.gitmem_init(self.project_root)

        # Create and commit a test file
        test_file = self.project_root / "docs/reports/checkpoint-test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Checkpoint test\n", encoding="utf-8")

        COMMON.gitmem_commit(
            self.project_root,
            "docs/reports/checkpoint-test.md",
            "Initial commit",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_checkpoint_creates_tag(self) -> None:
        """Test that gitmem_checkpoint creates a git tag."""
        COMMON.gitmem_checkpoint(self.project_root, "test-checkpoint")

        # Check that tag exists
        result = subprocess.run(
            ["git", "-C", str(self.project_root / ".gitmem"), "tag", "-l"],
            capture_output=True,
            text=True,
        )
        self.assertIn("test-checkpoint", result.stdout)

    def test_multiple_checkpoints(self) -> None:
        """Test that multiple checkpoints can be created."""
        COMMON.gitmem_checkpoint(self.project_root, "checkpoint-1")

        # Modify and commit
        test_file = self.project_root / "docs/reports/checkpoint-test.md"
        test_file.write_text("# Modified\n", encoding="utf-8")
        COMMON.gitmem_commit(self.project_root, "docs/reports/checkpoint-test.md", "Update")

        COMMON.gitmem_checkpoint(self.project_root, "checkpoint-2")

        result = subprocess.run(
            ["git", "-C", str(self.project_root / ".gitmem"), "tag", "-l"],
            capture_output=True,
            text=True,
        )
        self.assertIn("checkpoint-1", result.stdout)
        self.assertIn("checkpoint-2", result.stdout)


class GitMemCheckLoopTest(unittest.TestCase):
    """Tests for gitmem_check_loop function."""

    def setUp(self) -> None:
        """Set up a test project with GitMem."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        COMMON.gitmem_init(self.project_root)

        # Create a test file
        test_file = self.project_root / "docs/reports/loop-test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Loop test\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_no_loop_initially(self) -> None:
        """Test that there's no loop initially."""
        in_loop = COMMON.gitmem_check_loop(self.project_root, "docs/reports/loop-test.md")
        self.assertFalse(in_loop)

    def test_loop_detected_after_threshold(self) -> None:
        """Test that loop is detected after threshold commits."""
        # Create commits up to and past threshold
        for i in range(COMMON.GITMEM_LOOP_THRESHOLD + 1):
            test_file = self.project_root / "docs/reports/loop-test.md"
            test_file.write_text(f"# Loop test revision {i}\n", encoding="utf-8")
            COMMON.gitmem_commit(
                self.project_root,
                "docs/reports/loop-test.md",
                f"Revision {i}",
            )

        in_loop = COMMON.gitmem_check_loop(self.project_root, "docs/reports/loop-test.md")
        self.assertTrue(in_loop)

    def test_no_loop_after_checkpoint(self) -> None:
        """Test that loop is reset after checkpoint."""
        # Create commits past threshold
        for i in range(COMMON.GITMEM_LOOP_THRESHOLD + 1):
            test_file = self.project_root / "docs/reports/loop-test.md"
            test_file.write_text(f"# Loop test revision {i}\n", encoding="utf-8")
            COMMON.gitmem_commit(
                self.project_root,
                "docs/reports/loop-test.md",
                f"Revision {i}",
            )

        # Create checkpoint
        COMMON.gitmem_checkpoint(self.project_root, "stable-state")

        # No loop should be detected after checkpoint
        in_loop = COMMON.gitmem_check_loop(self.project_root, "docs/reports/loop-test.md")
        self.assertFalse(in_loop)

    def test_get_loop_info(self) -> None:
        """Test gitmem_get_loop_info returns correct info."""
        # Make 3 commits
        for i in range(3):
            test_file = self.project_root / "docs/reports/loop-test.md"
            test_file.write_text(f"# Revision {i}\n", encoding="utf-8")
            COMMON.gitmem_commit(
                self.project_root,
                "docs/reports/loop-test.md",
                f"Revision {i}",
            )

        info = COMMON.gitmem_get_loop_info(self.project_root, "docs/reports/loop-test.md")

        self.assertFalse(info["in_loop"])  # 3 < 5
        self.assertEqual(info["change_count"], 3)
        self.assertIsNone(info["last_checkpoint"])


class GitMemHistoryTest(unittest.TestCase):
    """Tests for gitmem_history function."""

    def setUp(self) -> None:
        """Set up a test project with multiple commits."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        COMMON.gitmem_init(self.project_root)

        # Create multiple commits
        test_file = self.project_root / "docs/reports/history-test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)

        for i in range(3):
            test_file.write_text(f"# Version {i}\n", encoding="utf-8")
            COMMON.gitmem_commit(
                self.project_root,
                "docs/reports/history-test.md",
                f"Version {i}",
            )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_history_returns_list(self) -> None:
        """Test that gitmem_history returns a list of commits."""
        history = COMMON.gitmem_history(self.project_root, "docs/reports/history-test.md")

        self.assertIsInstance(history, list)
        self.assertEqual(len(history), 3)

    def test_history_contains_required_fields(self) -> None:
        """Test that history entries have required fields."""
        history = COMMON.gitmem_history(self.project_root, "docs/reports/history-test.md")

        for entry in history:
            self.assertIn("hash", entry)
            self.assertIn("date", entry)
            self.assertIn("message", entry)

    def test_history_respects_limit(self) -> None:
        """Test that history respects limit parameter."""
        history = COMMON.gitmem_history(self.project_root, "docs/reports/history-test.md", limit=2)

        self.assertEqual(len(history), 2)


class GitMemDiffTest(unittest.TestCase):
    """Tests for gitmem_diff function."""

    def setUp(self) -> None:
        """Set up a test project with multiple commits."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        COMMON.gitmem_init(self.project_root)

        test_file = self.project_root / "docs/reports/diff-test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Original\n", encoding="utf-8")
        COMMON.gitmem_commit(self.project_root, "docs/reports/diff-test.md", "Original")

        test_file.write_text("# Modified\nNew content\n", encoding="utf-8")
        COMMON.gitmem_commit(self.project_root, "docs/reports/diff-test.md", "Modified")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_diff_returns_string(self) -> None:
        """Test that gitmem_diff returns a string."""
        diff = COMMON.gitmem_diff(self.project_root, "docs/reports/diff-test.md")

        self.assertIsInstance(diff, str)
        self.assertIn("Original", diff)
        self.assertIn("Modified", diff)


class GitMemRollbackTest(unittest.TestCase):
    """Tests for gitmem_rollback function."""

    def setUp(self) -> None:
        """Set up a test project with multiple commits."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()

        COMMON.gitmem_init(self.project_root)

        test_file = self.project_root / "docs/reports/rollback-test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Version 1\n", encoding="utf-8")
        COMMON.gitmem_commit(self.project_root, "docs/reports/rollback-test.md", "V1")

        test_file.write_text("# Version 2\n", encoding="utf-8")
        COMMON.gitmem_commit(self.project_root, "docs/reports/rollback-test.md", "V2")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_rollback_restores_content(self) -> None:
        """Test that rollback restores previous content."""
        result = COMMON.gitmem_rollback(self.project_root, "docs/reports/rollback-test.md")

        self.assertTrue(result)
        test_file = self.project_root / "docs/reports/rollback-test.md"
        content = test_file.read_text(encoding="utf-8")
        self.assertIn("Version 1", content)

    def test_rollback_creates_new_commit(self) -> None:
        """Test that rollback creates a new commit (doesn't rewrite history)."""
        COMMON.gitmem_rollback(self.project_root, "docs/reports/rollback-test.md")

        # Check that there's a rollback commit
        history = COMMON.gitmem_history(self.project_root, "docs/reports/rollback-test.md")
        self.assertTrue(any("Rollback" in entry["message"] for entry in history))


class GitMemIsInitializedTest(unittest.TestCase):
    """Tests for gitmem_is_initialized function."""

    def test_returns_false_when_not_initialized(self) -> None:
        """Test that gitmem_is_initialized returns False when .gitmem doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            self.assertFalse(COMMON.gitmem_is_initialized(project_root))

    def test_returns_false_when_gitmem_exists_but_no_git(self) -> None:
        """Test that gitmem_is_initialized returns False when .gitmem exists but .git doesn't."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            # Create .gitmem without .git
            gitmem_path = project_root / ".gitmem"
            gitmem_path.mkdir()

            self.assertFalse(COMMON.gitmem_is_initialized(project_root))

    def test_returns_true_after_init(self) -> None:
        """Test that gitmem_is_initialized returns True after init."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            self.assertTrue(COMMON.gitmem_is_initialized(project_root))


class GitMemListTagsTest(unittest.TestCase):
    """Tests for gitmem_list_tags function."""

    def test_returns_empty_list_when_not_initialized(self) -> None:
        """Test that gitmem_list_tags returns empty list when not initialized."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            tags = COMMON.gitmem_list_tags(project_root)
            self.assertEqual([], tags)

    def test_returns_tags_after_checkpoint(self) -> None:
        """Test that gitmem_list_tags returns tags after checkpoints are created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            # Create a test file and commit
            test_file = project_root / "docs/reports/test.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("content\n", encoding="utf-8")
            COMMON.gitmem_commit(project_root, "docs/reports/test.md", "Initial")

            # Create checkpoint
            COMMON.gitmem_checkpoint(project_root, "test-checkpoint")

            tags = COMMON.gitmem_list_tags(project_root)
            self.assertIn("test-checkpoint", tags)

    def test_returns_multiple_tags(self) -> None:
        """Test that gitmem_list_tags returns all tags."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()

            COMMON.gitmem_init(project_root)

            test_file = project_root / "docs/reports/test.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("content\n", encoding="utf-8")
            COMMON.gitmem_commit(project_root, "docs/reports/test.md", "Initial")

            COMMON.gitmem_checkpoint(project_root, "checkpoint-1")
            COMMON.gitmem_checkpoint(project_root, "checkpoint-2")

            tags = COMMON.gitmem_list_tags(project_root)
            self.assertIn("checkpoint-1", tags)
            self.assertIn("checkpoint-2", tags)


class GitMemCommitEdgeCasesTest(unittest.TestCase):
    """Edge case tests for gitmem_commit function."""

    def setUp(self) -> None:
        """Set up a test project with GitMem initialized."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "test-project"
        self.project_root.mkdir()
        COMMON.gitmem_init(self.project_root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_commit_file_outside_tracked_directories(self) -> None:
        """Test committing a file outside tracked directories (should still work but log warning)."""
        # Create file outside tracked directories
        test_file = self.project_root / "other/file.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content\n", encoding="utf-8")

        # This should not raise an error, just log a warning
        commit_hash = COMMON.gitmem_commit(self.project_root, "other/file.md", "Commit outside tracked")
        self.assertIsInstance(commit_hash, str)

    def test_commit_with_no_changes(self) -> None:
        """Test committing with no changes returns current HEAD."""
        test_file = self.project_root / "docs/reports/test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content\n", encoding="utf-8")

        hash1 = COMMON.gitmem_commit(self.project_root, "docs/reports/test.md", "First commit")

        # Commit again without changes
        hash2 = COMMON.gitmem_commit(self.project_root, "docs/reports/test.md", "No changes")

        # Should return the same hash
        self.assertEqual(hash1, hash2)

    def test_commit_without_init_raises(self) -> None:
        """Test that committing without init raises ValueError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-init-project"
            project_root.mkdir()

            test_file = project_root / "docs/reports/test.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("content\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                COMMON.gitmem_commit(project_root, "docs/reports/test.md", "Should fail")

            self.assertIn("not initialized", str(context.exception).lower())


class GitMemRollbackEdgeCasesTest(unittest.TestCase):
    """Edge case tests for gitmem_rollback function."""

    def test_rollback_without_init_returns_false(self) -> None:
        """Test that rollback without init returns False."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-init-project"
            project_root.mkdir()

            result = COMMON.gitmem_rollback(project_root, "docs/reports/test.md")
            self.assertFalse(result)

    def test_rollback_to_nonexistent_revision_returns_false(self) -> None:
        """Test that rollback to nonexistent revision returns False."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()
            COMMON.gitmem_init(project_root)

            test_file = project_root / "docs/reports/test.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("content\n", encoding="utf-8")
            COMMON.gitmem_commit(project_root, "docs/reports/test.md", "Initial")

            result = COMMON.gitmem_rollback(project_root, "docs/reports/test.md", to_rev="nonexistent")
            self.assertFalse(result)


class GitMemHistoryEdgeCasesTest(unittest.TestCase):
    """Edge case tests for gitmem_history function."""

    def test_history_without_init_returns_empty_list(self) -> None:
        """Test that history without init returns empty list."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-init-project"
            project_root.mkdir()

            history = COMMON.gitmem_history(project_root, "docs/reports/test.md")
            self.assertEqual([], history)

    def test_history_for_nonexistent_file_returns_empty_list(self) -> None:
        """Test that history for nonexistent file returns empty list."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_root.mkdir()
            COMMON.gitmem_init(project_root)

            history = COMMON.gitmem_history(project_root, "docs/reports/nonexistent.md")
            self.assertEqual([], history)


class GitMemDiffEdgeCasesTest(unittest.TestCase):
    """Edge case tests for gitmem_diff function."""

    def test_diff_without_init_returns_message(self) -> None:
        """Test that diff without init returns appropriate message."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "no-init-project"
            project_root.mkdir()

            diff = COMMON.gitmem_diff(project_root, "docs/reports/test.md")
            self.assertIn("not initialized", diff.lower())


if __name__ == "__main__":
    unittest.main()
