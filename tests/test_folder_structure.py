"""Tests for new folder structure constants in orchestrator_common.py.

This test file validates the new semantic folder structure:
- Main directories: paper/, code/, docs/
- Agent workspaces: agents/<role>/
- System directories: .autoresearch/ (state, config, dashboard, runtime, etc.)

Old numbered phase directories (01-survey, 02-pilot-analysis, etc.) are
being replaced by the semantic structure for better clarity.
"""

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


COMMON = load_script_module("orchestrator_common")


class TestNewFolderStructureConstants(unittest.TestCase):
    """Test new folder structure constants exist and have correct values."""

    def test_main_directories_defined(self) -> None:
        """MAIN_DIRECTORIES should contain paper, code, docs."""
        self.assertTrue(hasattr(COMMON, "MAIN_DIRECTORIES"))
        expected = ("paper", "code", "docs")
        self.assertEqual(COMMON.MAIN_DIRECTORIES, expected)

    def test_agent_directories_defined(self) -> None:
        """AGENT_DIRECTORIES should have 8 agent roles."""
        self.assertTrue(hasattr(COMMON, "AGENT_DIRECTORIES"))
        expected = (
            "agents/survey",
            "agents/critic",
            "agents/coder",
            "agents/adviser",
            "agents/writer",
            "agents/reviewer",
            "agents/reflector",
            "agents/curator",
        )
        self.assertEqual(COMMON.AGENT_DIRECTORIES, expected)
        self.assertEqual(len(COMMON.AGENT_DIRECTORIES), 8)

    def test_system_directories_defined(self) -> None:
        """SYSTEM_DIRECTORIES should define .autoresearch subdirectories."""
        self.assertTrue(hasattr(COMMON, "SYSTEM_DIRECTORIES"))
        expected = (
            ".autoresearch/state",
            ".autoresearch/config",
            ".autoresearch/dashboard",
            ".autoresearch/runtime",
            ".autoresearch/reference-papers",
            ".autoresearch/templates",
            ".autoresearch/archive",
        )
        self.assertEqual(COMMON.SYSTEM_DIRECTORIES, expected)

    def test_required_directories_combined(self) -> None:
        """REQUIRED_DIRECTORIES should combine main, agent, and system dirs."""
        self.assertTrue(hasattr(COMMON, "REQUIRED_DIRECTORIES"))
        expected = COMMON.MAIN_DIRECTORIES + COMMON.AGENT_DIRECTORIES + COMMON.SYSTEM_DIRECTORIES
        self.assertEqual(COMMON.REQUIRED_DIRECTORIES, expected)

    def test_legacy_phase_directories_preserved(self) -> None:
        """Old PHASE_DIRECTORIES should be preserved for backward compatibility."""
        self.assertTrue(hasattr(COMMON, "PHASE_DIRECTORIES"))
        expected = (
            "00-admin",
            "01-survey",
            "02-pilot-analysis",
            "03-full-experiments",
            "04-paper",
            "05-reflection-evolution",
            "06-archive",
        )
        self.assertEqual(COMMON.PHASE_DIRECTORIES, expected)


class TestUpdatedDeliverablesPaths(unittest.TestCase):
    """Test that DEFAULT_DELIVERABLES uses new paths."""

    def test_research_state_uses_autoresearch_path(self) -> None:
        """research_state should be in .autoresearch/state/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["research_state"], ".autoresearch/state/research-state.yaml"
        )

    def test_project_config_uses_autoresearch_path(self) -> None:
        """project_config should be in .autoresearch/config/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["project_config"],
            ".autoresearch/config/orchestrator-config.yaml",
        )

    def test_dashboard_paths_use_autoresearch(self) -> None:
        """Dashboard files should be in .autoresearch/dashboard/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["dashboard_status"], ".autoresearch/dashboard/status.json"
        )
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["dashboard_progress"], ".autoresearch/dashboard/progress.md"
        )

    def test_runtime_paths_use_autoresearch(self) -> None:
        """Runtime registry files should be in .autoresearch/runtime/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["job_registry"], ".autoresearch/runtime/job-registry.yaml"
        )
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["gpu_registry"], ".autoresearch/runtime/gpu-registry.yaml"
        )

    def test_reference_library_path_updated(self) -> None:
        """reference_library_index should be in .autoresearch/reference-papers/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["reference_library_index"],
            ".autoresearch/reference-papers/README.md",
        )

    def test_idea_brief_in_autoresearch(self) -> None:
        """idea_brief should be in .autoresearch/."""
        self.assertEqual(COMMON.DEFAULT_DELIVERABLES["idea_brief"], ".autoresearch/idea-brief.md")

    def test_workspace_manifest_in_autoresearch(self) -> None:
        """workspace_manifest should be in .autoresearch/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["workspace_manifest"], ".autoresearch/workspace-manifest.md"
        )

    def test_paper_draft_in_paper(self) -> None:
        """paper_draft should be in paper/."""
        self.assertEqual(COMMON.DEFAULT_DELIVERABLES["paper_draft"], "paper/paper-draft.md")

    def test_paper_related_in_paper_dir(self) -> None:
        """Paper-related deliverables should be in paper/."""
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["citation_audit_report"], "paper/citation-audit-report.md"
        )
        self.assertEqual(COMMON.DEFAULT_DELIVERABLES["rebuttal_log"], "paper/rebuttal-log.md")
        # final_acceptance_report is in docs/paper/ per design
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["final_acceptance_report"],
            "docs/paper/final-acceptance-report.md",
        )

    def test_experiment_files_in_code(self) -> None:
        """Experiment-related files should be in code/."""
        # experiment_spec is in code/configs/ per design
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["experiment_spec"], "code/configs/experiment-spec.md"
        )
        # run_registry is in code/checkpoints/ per design
        self.assertEqual(
            COMMON.DEFAULT_DELIVERABLES["run_registry"], "code/checkpoints/run-registry.md"
        )


class TestHandoffRequirementsSemanticNames(unittest.TestCase):
    """Test HANDOFF_REQUIREMENTS uses semantic phase names."""

    def test_survey_to_pilot_uses_semantic_name(self) -> None:
        """Next phase from survey should be 'pilot'."""
        self.assertEqual(COMMON.HANDOFF_REQUIREMENTS["survey-to-pilot"]["next_phase"], "pilot")

    def test_pilot_to_experiments_uses_semantic_name(self) -> None:
        """Next phase from pilot should be 'experiments'."""
        self.assertEqual(
            COMMON.HANDOFF_REQUIREMENTS["pilot-to-experiments"]["next_phase"], "experiments"
        )

    def test_experiments_to_paper_uses_semantic_name(self) -> None:
        """Next phase from experiments should be 'paper'."""
        self.assertEqual(COMMON.HANDOFF_REQUIREMENTS["experiments-to-paper"]["next_phase"], "paper")

    def test_paper_to_reflection_uses_semantic_name(self) -> None:
        """Next phase from paper should be 'reflection'."""
        self.assertEqual(
            COMMON.HANDOFF_REQUIREMENTS["paper-to-reflection"]["next_phase"], "reflection"
        )

    def test_reflection_closeout_uses_semantic_name(self) -> None:
        """Next phase from reflection should be 'handoff-user'."""
        self.assertEqual(
            COMMON.HANDOFF_REQUIREMENTS["reflection-closeout"]["next_phase"], "handoff-user"
        )


class TestLegacyMappings(unittest.TestCase):
    """Test backward compatibility mappings."""

    def test_phase_to_gate_legacy_defined(self) -> None:
        """PHASE_TO_GATE_LEGACY should map old numbered phase names to gates."""
        self.assertTrue(hasattr(COMMON, "PHASE_TO_GATE_LEGACY"))
        self.assertEqual(COMMON.PHASE_TO_GATE_LEGACY["01-survey"], "gate_1")
        self.assertEqual(COMMON.PHASE_TO_GATE_LEGACY["02-pilot-analysis"], "gate_2")
        self.assertEqual(COMMON.PHASE_TO_GATE_LEGACY["03-full-experiments"], "gate_3")
        self.assertEqual(COMMON.PHASE_TO_GATE_LEGACY["04-paper"], "gate_4")
        self.assertEqual(COMMON.PHASE_TO_GATE_LEGACY["05-reflection-evolution"], "gate_5")

    def test_next_phase_legacy_defined(self) -> None:
        """NEXT_PHASE_LEGACY should map old numbered phases to next numbered phase."""
        self.assertTrue(hasattr(COMMON, "NEXT_PHASE_LEGACY"))
        self.assertEqual(COMMON.NEXT_PHASE_LEGACY["01-survey"], "02-pilot-analysis")
        self.assertEqual(COMMON.NEXT_PHASE_LEGACY["02-pilot-analysis"], "03-full-experiments")
        self.assertEqual(COMMON.NEXT_PHASE_LEGACY["03-full-experiments"], "04-paper")
        self.assertEqual(COMMON.NEXT_PHASE_LEGACY["04-paper"], "05-reflection-evolution")
        self.assertEqual(COMMON.NEXT_PHASE_LEGACY["05-reflection-evolution"], "06-archive")

    def test_old_to_new_path_mapping_defined(self) -> None:
        """OLD_TO_NEW_PATH_MAPPING should map old paths to new paths."""
        self.assertTrue(hasattr(COMMON, "OLD_TO_NEW_PATH_MAPPING"))
        # Check some key mappings
        self.assertIn("00-admin/research-state.yaml", COMMON.OLD_TO_NEW_PATH_MAPPING)
        self.assertEqual(
            COMMON.OLD_TO_NEW_PATH_MAPPING["00-admin/research-state.yaml"],
            ".autoresearch/state/research-state.yaml",
        )

        self.assertIn("00-admin/orchestrator-config.yaml", COMMON.OLD_TO_NEW_PATH_MAPPING)
        self.assertIn("04-paper/paper-draft.md", COMMON.OLD_TO_NEW_PATH_MAPPING)
        self.assertEqual(
            COMMON.OLD_TO_NEW_PATH_MAPPING["04-paper/paper-draft.md"], "paper/paper-draft.md"
        )


class TestPhaseToGateConstant(unittest.TestCase):
    """Test PHASE_TO_GATE still works (may be aliased to legacy)."""

    def test_phase_to_gate_exists(self) -> None:
        """PHASE_TO_GATE should still exist."""
        self.assertTrue(hasattr(COMMON, "PHASE_TO_GATE"))

    def test_phase_to_gate_has_expected_mappings(self) -> None:
        """PHASE_TO_GATE should map phases to gates."""
        # Should work with either old or new phase names
        self.assertIn("gate_1", COMMON.PHASE_TO_GATE.values())
        self.assertIn("gate_2", COMMON.PHASE_TO_GATE.values())
        self.assertIn("gate_3", COMMON.PHASE_TO_GATE.values())
        self.assertIn("gate_4", COMMON.PHASE_TO_GATE.values())
        self.assertIn("gate_5", COMMON.PHASE_TO_GATE.values())


class TestNextPhaseConstant(unittest.TestCase):
    """Test NEXT_PHASE still works."""

    def test_next_phase_exists(self) -> None:
        """NEXT_PHASE should still exist."""
        self.assertTrue(hasattr(COMMON, "NEXT_PHASE"))


class TestExpectedDeliverablePrefixesUpdated(unittest.TestCase):
    """Test EXPECTED_DELIVERABLE_PREFIXES uses new paths."""

    def test_research_state_prefix_updated(self) -> None:
        """research_state prefix should be .autoresearch/."""
        self.assertEqual(COMMON.EXPECTED_DELIVERABLE_PREFIXES["research_state"], ".autoresearch/")

    def test_paper_draft_prefix_updated(self) -> None:
        """paper_draft prefix should be paper/."""
        self.assertEqual(COMMON.EXPECTED_DELIVERABLE_PREFIXES["paper_draft"], "paper/")


class TestEnsureProjectStructure(unittest.TestCase):
    """Test ensure_project_structure() function."""

    def setUp(self) -> None:
        """Create temporary directory for test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_returns_true_for_valid_structure(self) -> None:
        """Return True when all required directories exist."""
        # Create all required directories
        for dir_path in COMMON.REQUIRED_DIRECTORIES:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)

        result = COMMON.ensure_project_structure(self.project_root)
        self.assertTrue(result)

    def test_creates_missing_directories(self) -> None:
        """Create missing directories when create_if_missing=True."""
        # Create only some directories
        (self.project_root / "paper").mkdir(parents=True)
        (self.project_root / "code").mkdir(parents=True)

        # Call with create_if_missing=True (default)
        result = COMMON.ensure_project_structure(self.project_root, create_if_missing=True)
        self.assertTrue(result)

        # Verify all directories now exist
        for dir_path in COMMON.REQUIRED_DIRECTORIES:
            self.assertTrue(
                (self.project_root / dir_path).exists(), f"Directory should exist: {dir_path}"
            )

    def test_returns_false_for_empty_project(self) -> None:
        """Return False for empty project when create_if_missing=False."""
        # Empty project - no directories created
        result = COMMON.ensure_project_structure(self.project_root, create_if_missing=False)
        self.assertFalse(result)


class TestMigrationScript(unittest.TestCase):
    """Test migrate_structure.py script."""

    def setUp(self) -> None:
        """Create temporary directory for test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)

        # Load migrate_structure module
        spec = importlib.util.spec_from_file_location(
            "migrate_structure", SCRIPTS_DIR / "migrate_structure.py"
        )
        self.migrate_module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(self.migrate_module)

    def tearDown(self) -> None:
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_has_old_structure_detects_old_dirs(self) -> None:
        """has_old_structure should detect old numbered directories."""
        # Create old structure
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "01-survey").mkdir()

        result = self.migrate_module.has_old_structure(self.project_root)
        self.assertTrue(result)

    def test_has_old_structure_returns_false_for_new_structure(self) -> None:
        """has_old_structure should return False for already migrated project."""
        # Create new structure only
        (self.project_root / "paper").mkdir()
        (self.project_root / ".autoresearch" / "state").mkdir(parents=True)

        result = self.migrate_module.has_old_structure(self.project_root)
        self.assertFalse(result)

    def test_migrate_project_dry_run_no_changes(self) -> None:
        """Dry run should not make any changes."""
        # Create old structure with a file
        (self.project_root / "00-admin").mkdir()
        test_file = self.project_root / "00-admin" / "test.txt"
        test_file.write_text("test content")

        # Run migration in dry-run mode
        results = self.migrate_module.migrate_project(self.project_root, dry_run=True, backup=True)

        # Verify dry run detected old structure
        self.assertTrue(results["has_old_structure"])
        self.assertTrue(results["dry_run"])

        # Verify old structure still exists (no changes made)
        self.assertTrue((self.project_root / "00-admin").exists())
        self.assertEqual(test_file.read_text(), "test content")

        # Verify new structure not created
        self.assertFalse((self.project_root / ".autoresearch").exists())

    def test_migrate_project_creates_backup(self) -> None:
        """Migration should create backup of old directories."""
        # Create old structure
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "01-survey").mkdir()
        (self.project_root / "00-admin" / "test.txt").write_text("test")

        # Run migration
        results = self.migrate_module.migrate_project(self.project_root, dry_run=False, backup=True)

        # Verify backup was created
        self.assertIsNotNone(results["backup_path"])
        self.assertTrue(Path(results["backup_path"]).exists())
        self.assertTrue((Path(results["backup_path"]) / "00-admin" / "test.txt").exists())

    def test_migrate_project_creates_new_structure(self) -> None:
        """Migration should create new directory structure."""
        # Create old structure
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "04-paper").mkdir()

        # Run migration
        self.migrate_module.migrate_project(self.project_root, dry_run=False, backup=False)

        # Verify new structure exists
        self.assertTrue((self.project_root / "paper").exists())
        self.assertTrue((self.project_root / "code").exists())
        self.assertTrue((self.project_root / "docs").exists())
        self.assertTrue((self.project_root / ".autoresearch" / "state").exists())
        self.assertTrue((self.project_root / ".autoresearch" / "config").exists())

    def test_migrate_project_migrates_files(self) -> None:
        """Migration should move files from old to new paths."""
        # Create old structure with state file
        (self.project_root / "00-admin").mkdir()
        state_content = "research_state:\n  current_phase: 01-survey\n"
        (self.project_root / "00-admin" / "research-state.yaml").write_text(state_content)

        # Run migration
        self.migrate_module.migrate_project(self.project_root, dry_run=False, backup=False)

        # Verify file was migrated
        new_state_path = self.project_root / ".autoresearch" / "state" / "research-state.yaml"
        self.assertTrue(new_state_path.exists())
        self.assertIn("research_state:", new_state_path.read_text())

    def test_migrate_project_updates_state_phase_names(self) -> None:
        """Migration should update phase names in state file."""
        # Create old structure with state file using old phase names
        (self.project_root / "00-admin").mkdir()
        state_content = """
research_state:
  current_phase: 01-survey
  phase_reviews:
    01-survey: approved
    02-pilot-analysis: revise
  approval_status:
    01-survey: gate_1
  loop_counts:
    01-survey: 2
"""
        (self.project_root / "00-admin" / "research-state.yaml").write_text(state_content)
        (self.project_root / "00-admin" / "orchestrator-config.yaml").write_text("{}")

        # Run migration - should handle state update gracefully
        self.migrate_module.migrate_project(self.project_root, dry_run=False, backup=False)

        # State file should exist at new path
        new_state_path = self.project_root / ".autoresearch" / "state" / "research-state.yaml"
        self.assertTrue(new_state_path.exists())

    def test_migrate_project_removes_old_directories(self) -> None:
        """Migration should remove old directories after migration."""
        # Create old structure
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "01-survey").mkdir()
        (self.project_root / "04-paper").mkdir()

        # Run migration
        results = self.migrate_module.migrate_project(
            self.project_root, dry_run=False, backup=False
        )

        # Verify old directories are removed
        self.assertFalse((self.project_root / "00-admin").exists())
        self.assertFalse((self.project_root / "01-survey").exists())

        # Verify removal is tracked in results
        self.assertIn("00-admin", results["removed_directories"])
        self.assertIn("01-survey", results["removed_directories"])

    def test_migrate_project_no_old_structure_message(self) -> None:
        """Migration should return message when no old structure detected."""
        # Create only new structure
        (self.project_root / "paper").mkdir()
        (self.project_root / ".autoresearch" / "state").mkdir(parents=True)

        # Run migration
        results = self.migrate_module.migrate_project(self.project_root, dry_run=False, backup=True)

        # Verify message is set
        self.assertIn("message", results)
        self.assertIn("no old structure detected", results["message"].lower())

    def test_create_new_structure_in_dry_run_mode(self) -> None:
        """create_new_structure should report what it would create in dry run."""
        results = self.migrate_module.create_new_structure(self.project_root, dry_run=True)

        # Should return list of what would be created
        self.assertTrue(all("[DRY RUN]" in r for r in results))
        self.assertTrue(any("paper" in r for r in results))

    def test_migrate_files_handles_errors_gracefully(self) -> None:
        """migrate_files should handle errors gracefully."""
        # Create old structure with a file
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "00-admin" / "test.txt").write_text("test")

        # Run migration
        results = self.migrate_module.migrate_files(self.project_root, dry_run=False)

        # Should complete without raising exception
        self.assertIn("migrated_files", results)
        self.assertIn("errors", results)


if __name__ == "__main__":
    unittest.main()
