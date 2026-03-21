"""Tests for phase rollback file handling."""

import sys
from pathlib import Path

# Add scripts directory to path
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

import tempfile

from phase_rollback import archive_phase_deliverables, get_deliverables_for_phase


class TestPhaseRollback:
    """Test rollback file handling strategies."""

    def test_archive_deliverables_on_rollback(self):
        """When rolling back, deliverables should be archived."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            docs_dir = project_root / "docs" / "experiments"
            docs_dir.mkdir(parents=True)
            (docs_dir / "results-summary.md").write_text("Experiment results")

            archive_dir = project_root / ".autoresearch" / "archive"
            archive_dir.mkdir(parents=True)

            archived = archive_phase_deliverables(project_root, "experiments")

            assert len(archived) == 1
            assert "results-summary.md" in archived[0]

    def test_archive_preserves_original_files(self):
        """Archiving should preserve original files, not delete them."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            docs_dir = project_root / "docs" / "experiments"
            docs_dir.mkdir(parents=True)
            results_file = docs_dir / "results-summary.md"
            results_file.write_text("Experiment results")

            archive_dir = project_root / ".autoresearch" / "archive"
            archive_dir.mkdir(parents=True)

            archive_phase_deliverables(project_root, "experiments")

            assert results_file.exists()

    def test_get_deliverables_for_phase(self):
        """Should return list of deliverable paths for a phase."""
        survey_deliverables = get_deliverables_for_phase("survey")

        assert isinstance(survey_deliverables, list)
        assert len(survey_deliverables) > 0
        assert any("research-readiness-report" in d for d in survey_deliverables)
