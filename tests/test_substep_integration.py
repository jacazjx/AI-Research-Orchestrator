"""Integration tests for substep workflow in Agent-Skill Coupling.

These tests verify the complete substep workflow including:
- Primary agent execution to reviewer approval
- GitMem checkpoint creation
- Review-rejection-revision cycles
- Phase transitions with substeps
"""

from __future__ import annotations

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
INIT = load_script_module("init_research_project")
STAGE = load_script_module("run_stage_loop")
VALIDATE = load_script_module("validate_substep")


class TestCompleteSubstepWorkflow(unittest.TestCase):
    """Test the complete substep workflow from start to approval."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "substep-workflow-test"
        INIT.initialize_research_project(
            project_root=self.project_root, topic="Complete substep workflow test"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_complete_substep_workflow(self) -> None:
        """Test complete workflow: Primary -> Reviewer approves -> Checkpoint -> Next substep."""
        # Create required artifact for literature_survey
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Literature Review\n\nA comprehensive review.\n", encoding="utf-8")

        # Run as primary agent (survey)
        result1 = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="Primary agent completed literature survey.",
        )

        # Verify initial state
        self.assertEqual("literature_survey", result1["current_substep"])
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        self.assertEqual("literature_survey", state["current_substep"])
        # Substep should be in_progress
        self.assertEqual(
            "in_progress",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )

        # Run as reviewer with approval
        result2 = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Reviewer approved literature survey.",
        )

        # Verify approval and advancement
        self.assertEqual("idea_definition", result2["current_substep"])
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # Previous substep should be approved
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["review_result"],
        )
        # New substep should be in_progress
        self.assertEqual(
            "in_progress",
            state["substep_status"]["survey"]["idea_definition"]["status"],
        )

        # Verify GitMem checkpoint was created
        tags = COMMON.gitmem_list_tags(self.project_root)
        self.assertIn("survey-literature_survey-approved", tags)

    def test_substep_checkpoint_created_on_approval(self) -> None:
        """Test that GitMem checkpoint is created when substep is approved."""
        # Create required artifact
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Literature Review\n", encoding="utf-8")

        # Approve the substep
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved",
        )

        # Verify checkpoint
        tags = COMMON.gitmem_list_tags(self.project_root)
        self.assertIn("survey-literature_survey-approved", tags)


class TestSubstepRevisionCycle(unittest.TestCase):
    """Test the revision cycle when reviewer rejects substep."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "substep-revision-test"
        INIT.initialize_research_project(
            project_root=self.project_root, topic="Substep revision test"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_substep_revision_cycle(self) -> None:
        """Test: Primary agent -> Reviewer rejects -> Revision -> Approval."""
        # Create artifact
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Literature Review\n\nInitial version.\n", encoding="utf-8")

        # Primary agent completes work
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="Primary agent completed work.",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        initial_attempts = state["substep_status"]["survey"]["literature_survey"].get("attempts", 1)

        # Reviewer rejects
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Reviewer requests revision.",
        )

        # Verify revision state
        self.assertEqual("revise", result["decision"])
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # Substep should still be in_progress
        self.assertEqual(
            "in_progress",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )
        # Attempts should be incremented
        self.assertEqual(
            initial_attempts + 1,
            state["substep_status"]["survey"]["literature_survey"]["attempts"],
        )
        # Should switch back to primary agent
        self.assertEqual("survey", state["progress"]["current_agent"])

        # Simulate revision - update artifact
        artifact.write_text(
            "# Literature Review\n\nRevised version with improvements.\n",
            encoding="utf-8",
        )

        # Primary agent resubmits
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="Primary agent submitted revision.",
        )

        # Reviewer approves
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Reviewer approved revision.",
        )

        # Verify final approval
        self.assertEqual("idea_definition", result["current_substep"])
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )

    def test_multiple_revisions_before_approval(self) -> None:
        """Test multiple revision cycles before approval."""
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)

        # Initial submission
        artifact.write_text("# V1\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="V1",
        )

        # First rejection - attempts goes from 0 (or unset) to 1
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Needs revision 1",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # After first revise, attempts = 1 (0 + 1)
        self.assertEqual(1, state["substep_status"]["survey"]["literature_survey"]["attempts"])

        # Second rejection
        artifact.write_text("# V2\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="V2",
        )
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Needs revision 2",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # After second revise, attempts = 2 (1 + 1)
        self.assertEqual(2, state["substep_status"]["survey"]["literature_survey"]["attempts"])

        # Final approval
        artifact.write_text("# V3 - Final\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="survey",
            note="V3",
        )
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved",
        )

        self.assertEqual("idea_definition", result["current_substep"])


class TestPhaseTransitionWithSubsteps(unittest.TestCase):
    """Test phase transitions when all substeps are completed."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "phase-transition-test"
        INIT.initialize_research_project(
            project_root=self.project_root, topic="Phase transition test"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_phase_transition_with_substeps(self) -> None:
        """Test complete all substeps -> Phase gate -> Next phase."""
        # Create all survey artifacts
        artifacts = {
            "docs/survey/literature-review.md": "# Literature Review\n",
            "docs/survey/idea-definition.md": "# Idea Definition\n",
            "docs/survey/research-readiness-report.md": (
                "# Research Readiness\n- Recommendation: `approve`\n"
            ),
            "docs/survey/survey-round-summary.md": "# Summary\n",
            "docs/survey/critic-round-review.md": "# Review\n",
            "docs/survey/phase-scorecard.md": "# Scorecard\n- Gate readiness: `approve`\n",
        }

        for path, content in artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Complete all three survey substeps sequentially
        # Substep 1: literature_survey
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved literature_survey",
        )

        # Substep 2: idea_definition
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved idea_definition",
        )

        # Substep 3: research_plan - this is the last one
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved research_plan",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")

        # All survey substeps should be approved
        for substep in ["literature_survey", "idea_definition", "research_plan"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["survey"][substep]["status"],
            )

        # Now transition to pilot with gate approval
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            gate_status="approved",
            increment_loop=True,
            auto_transition=True,
            note="Survey complete, transitioning to pilot.",
        )

        self.assertEqual("advance", result["decision"])
        self.assertEqual("pilot", result["transitioned_to"])

        # Verify pilot substep initialized
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        self.assertEqual("pilot", state["current_phase"])

        # Run pilot to initialize substep
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="code",
            note="Starting pilot phase",
        )

        self.assertEqual("problem_validation", result["current_substep"])

    def test_substep_resets_on_phase_transition(self) -> None:
        """Test that current_substep resets when transitioning phases."""
        # Set up for transition
        artifacts = {
            "docs/survey/literature-review.md": "# Lit Review\n",
            "docs/survey/idea-definition.md": "# Idea\n",
            "docs/survey/research-readiness-report.md": (
                "# Readiness\n- Recommendation: `approve`\n"
            ),
            "docs/survey/survey-round-summary.md": "# Summary\n",
            "docs/survey/critic-round-review.md": "# Review\n",
            "docs/survey/phase-scorecard.md": "# Scorecard\n- Gate readiness: `approve`\n",
        }

        for path, content in artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Complete survey and transition
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            gate_status="approved",
            auto_transition=True,
            note="Transition",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")

        # current_substep should be None after transition (reset)
        self.assertIsNone(state.get("current_substep"))

        # Start pilot - substep should initialize
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="code",
            note="Start pilot",
        )

        self.assertEqual("problem_validation", result["current_substep"])


class TestGitMemCheckpointsThroughWorkflow(unittest.TestCase):
    """Test GitMem checkpoints are created correctly throughout the workflow."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "checkpoint-test"
        INIT.initialize_research_project(project_root=self.project_root, topic="Checkpoint test")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_gitmem_checkpoints_through_workflow(self) -> None:
        """Verify checkpoints are created correctly throughout workflow."""
        # Create artifact
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)

        tags_before = COMMON.gitmem_list_tags(self.project_root)
        self.assertEqual(0, len(tags_before))

        # Complete first substep
        artifact.write_text("# Literature Review\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved lit survey",
        )

        tags_after_first = COMMON.gitmem_list_tags(self.project_root)
        self.assertIn("survey-literature_survey-approved", tags_after_first)

        # Complete second substep
        artifact2 = self.project_root / "docs/survey/idea-definition.md"
        artifact2.write_text("# Idea Definition\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved idea definition",
        )

        tags_after_second = COMMON.gitmem_list_tags(self.project_root)
        self.assertIn("survey-literature_survey-approved", tags_after_second)
        self.assertIn("survey-idea_definition-approved", tags_after_second)

    def test_gate_checkpoint_distinct_from_substep(self) -> None:
        """Test that gate checkpoints are distinct from substep checkpoints."""
        # Set up for gate approval
        artifacts = {
            "docs/survey/literature-review.md": "# Lit\n",
            "docs/survey/idea-definition.md": "# Idea\n",
            "docs/survey/research-readiness-report.md": (
                "# Ready\n- Recommendation: `approve`\n"
            ),
            "docs/survey/survey-round-summary.md": "# Summary\n",
            "docs/survey/critic-round-review.md": "# Review\n",
            "docs/survey/phase-scorecard.md": "# Scorecard\n- Gate readiness: `approve`\n",
        }

        for path, content in artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Complete all substeps first
        # Substep 1: literature_survey
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved literature_survey",
        )

        # Substep 2: idea_definition
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved idea_definition",
        )

        # Substep 3: research_plan - last substep
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved research_plan",
        )

        # Now approve the gate
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            gate_status="approved",
            increment_loop=True,
            note="Gate approved",
        )

        tags = COMMON.gitmem_list_tags(self.project_root)

        # Should have substep checkpoints for all three
        self.assertIn("survey-literature_survey-approved", tags)
        self.assertIn("survey-idea_definition-approved", tags)
        self.assertIn("survey-research_plan-approved", tags)
        # Should have gate checkpoint
        self.assertIn("phase-gate-survey-approved", tags)

    def test_checkpoint_not_created_on_revision(self) -> None:
        """Test that checkpoint is not created when review is revise."""
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Lit Review\n", encoding="utf-8")

        tags_before = COMMON.gitmem_list_tags(self.project_root)

        # Request revision
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Needs revision",
        )

        tags_after = COMMON.gitmem_list_tags(self.project_root)

        # No new checkpoint should be created
        self.assertEqual(len(tags_before), len(tags_after))


class TestSubstepValidationIntegration(unittest.TestCase):
    """Integration tests for substep validation."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "validation-test"
        INIT.initialize_research_project(project_root=self.project_root, topic="Validation test")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cannot_skip_substeps(self) -> None:
        """Test that substeps cannot be skipped."""
        # Try to validate idea_definition without completing literature_survey
        result = VALIDATE.validate_substep(self.project_root, "survey", "idea_definition")

        self.assertFalse(result["can_proceed"])
        self.assertFalse(result["previous_substeps_complete"])
        self.assertTrue(len(result["errors"]) > 0)

    def test_can_proceed_after_previous_approved(self) -> None:
        """Test that substep can proceed after previous is approved."""
        # Create artifact
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Lit Review\n", encoding="utf-8")

        # Approve first substep
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved",
        )

        # Now validate second substep
        result = VALIDATE.validate_substep(self.project_root, "survey", "idea_definition")

        self.assertTrue(result["can_proceed"])
        self.assertTrue(result["previous_substeps_complete"])


class TestSubstepStatePersistence(unittest.TestCase):
    """Test substep state persistence across operations."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "persistence-test"
        INIT.initialize_research_project(project_root=self.project_root, topic="Persistence test")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_substep_status_persists_across_reloads(self) -> None:
        """Test that substep status persists across state reloads."""
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Content\n", encoding="utf-8")

        # Approve substep
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved",
        )

        # Reload state
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")

        # Verify substep status persisted
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["review_result"],
        )

    def test_attempts_count_persists(self) -> None:
        """Test that attempts count persists across operations."""
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# V1\n", encoding="utf-8")

        # First revision - attempts goes from 0 (or unset) to 1
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Revise",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # After first revise, attempts = 1 (0 + 1)
        self.assertEqual(1, state["substep_status"]["survey"]["literature_survey"]["attempts"])

        # Second revision - attempts goes from 1 to 2
        artifact.write_text("# V2\n", encoding="utf-8")
        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="revise",
            note="Revise again",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")
        # After second revise, attempts = 2 (1 + 1)
        self.assertEqual(2, state["substep_status"]["survey"]["literature_survey"]["attempts"])


class TestFullResearchProjectWorkflow(unittest.TestCase):
    """End-to-end test simulating a complete research project workflow."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "full-workflow-test"
        INIT.initialize_research_project(
            project_root=self.project_root, topic="Full research project workflow test"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_full_research_project_workflow(self) -> None:
        """
        End-to-end test simulating a complete research project:
        - Survey phase: complete all 3 substeps
        - Pilot phase: complete all 3 substeps
        - Experiments phase: complete all 3 substeps
        - Paper phase: complete all 3 substeps
        - Reflection phase: complete all 2 substeps

        Verify:
        - GitMem checkpoints are created at each substep approval
        - Phase gates trigger correctly
        - State is correctly tracked throughout
        """
        all_checkpoints = []

        # ==================== SURVEY PHASE ====================
        # Create survey artifacts
        survey_artifacts = {
            "docs/survey/literature-review.md": (
                "# Literature Review\n\nComprehensive review of related work.\n"
            ),
            "docs/survey/idea-definition.md": (
                "# Idea Definition\n\nNovel research contribution.\n"
            ),
            "docs/survey/research-readiness-report.md": (
                "# Research Readiness Report\n\n- Recommendation: `approve`\n"
            ),
            "docs/survey/survey-round-summary.md": "# Survey Round Summary\n",
            "docs/survey/critic-round-review.md": "# Critic Round Review\n",
            "docs/survey/phase-scorecard.md": (
                "# Phase Scorecard\n\n- Gate readiness: `approve`\n"
            ),
        }
        for path, content in survey_artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Survey substep 1: literature_survey
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved literature_survey",
        )
        self.assertEqual("idea_definition", result["current_substep"])
        all_checkpoints.append("survey-literature_survey-approved")

        # Survey substep 2: idea_definition
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved idea_definition",
        )
        self.assertEqual("research_plan", result["current_substep"])
        all_checkpoints.append("survey-idea_definition-approved")

        # Survey substep 3: research_plan (last substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved research_plan",
        )
        all_checkpoints.append("survey-research_plan-approved")

        # Survey gate approval and transition to pilot
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            gate_status="approved",
            increment_loop=True,
            auto_transition=True,
            note="Survey complete, transitioning to pilot.",
        )
        self.assertEqual("advance", result["decision"])
        self.assertEqual("pilot", result["transitioned_to"])
        all_checkpoints.append("phase-gate-survey-approved")

        # ==================== PILOT PHASE ====================
        # Create pilot artifacts for both substep advancement and quality gate
        # Substep artifacts: problem-validation-report.md, problem-analysis.md,
        #   pilot-design.md, pilot-validation-report.md
        # Phase deliverables: problem_validation_report, problem_analysis, pilot_plan,
        #   pilot_validation_report, pilot_scorecard, pilot_adviser_review
        pilot_artifacts = {
            # Substep artifacts
            "docs/pilot/problem-validation-report.md": (
                "# Problem Validation Report\n\n- Validation verdict: `validated`\n"
            ),
            "docs/pilot/problem-analysis.md": (
                "# Problem Analysis\n\nDetailed problem breakdown.\n"
            ),
            "docs/pilot/pilot-design.md": (
                "# Pilot Design\n\nExperimental design for pilot.\n"
            ),
            "docs/pilot/pilot-validation-report.md": (
                "# Pilot Validation Report\n\n- Continue to full experiments: `yes`\n"
            ),
            # Additional phase deliverables for quality gate
            "code/configs/pilot-experiment-plan.md": (
                "# Pilot Experiment Plan\n\nPlan for pilot experiments.\n"
            ),
            "docs/pilot/pilot-adviser-review.md": (
                "# Pilot Adviser Review\n\n- Status: `approved`\n- Recommendation: `approve`\n"
            ),
            # Other artifacts
            "docs/pilot/pilot-round-summary.md": "# Pilot Round Summary\n",
            "docs/pilot/adviser-round-review.md": "# Adviser Round Review\n",
            "docs/pilot/phase-scorecard.md": (
                "# Phase Scorecard\n\n- Gate readiness: `approve`\n"
            ),
        }
        for path, content in pilot_artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Initialize pilot phase
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="code",
            note="Starting pilot phase",
        )
        self.assertEqual("problem_validation", result["current_substep"])

        # Pilot substep 0: problem_validation (NEW - first substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="adviser",
            review_status="approved",
            note="Approved problem_validation",
        )
        self.assertEqual("problem_analysis", result["current_substep"])
        all_checkpoints.append("pilot-problem_validation-approved")

        # Pilot substep 1: problem_analysis
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="adviser",
            review_status="approved",
            note="Approved problem_analysis",
        )
        self.assertEqual("pilot_design", result["current_substep"])
        all_checkpoints.append("pilot-problem_analysis-approved")

        # Pilot substep 3: pilot_design
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="adviser",
            review_status="approved",
            note="Approved pilot_design",
        )
        self.assertEqual("pilot_execution", result["current_substep"])
        all_checkpoints.append("pilot-pilot_design-approved")

        # Pilot substep 4: pilot_execution (last substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="adviser",
            review_status="approved",
            note="Approved pilot_execution",
        )
        all_checkpoints.append("pilot-pilot_execution-approved")

        # Pilot gate approval and transition to experiments
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="pilot",
            actor="adviser",
            gate_status="approved",
            increment_loop=True,
            auto_transition=True,
            note="Pilot complete, transitioning to experiments.",
        )
        self.assertEqual("advance", result["decision"])
        self.assertEqual("experiments", result["transitioned_to"])
        all_checkpoints.append("phase-gate-pilot-approved")

        # ==================== EXPERIMENTS PHASE ====================
        # Create experiments artifacts for both substep advancement and quality gate
        # Substep artifacts: experiment-spec.md, run-registry.md, evidence-package-index.md
        # Phase deliverables: experiment_spec, results_summary, evidence_package_index,
        #   experiment_scorecard, experiment_adviser_review
        experiments_artifacts = {
            # Substep artifacts
            "docs/experiments/experiment-spec.md": (
                "# Experiment Specification\n\nDetailed experiment design.\n"
            ),
            "docs/experiments/run-registry.md": (
                "# Run Registry\n\nExperiment run logs.\n"
            ),
            "docs/experiments/evidence-package-index.md": (
                "# Evidence Package Index\n\n- Results: `positive`\n"
            ),
            # Additional phase deliverables for quality gate
            "code/configs/experiment-spec.md": (
                "# Experiment Specification\n\nDetailed experiment design.\n"
            ),
            "docs/experiments/results-summary.md": (
                "# Results Summary\n\nSummary of experiment results.\n"
            ),
            "docs/experiments/experiment-adviser-review.md": (
                "# Experiment Adviser Review\n\n"
                "- Status: `approved`\n"
                "- Recommendation: `approve`\n"
                "- Handoff decision: `approve`\n"
            ),
            # Other artifacts
            "docs/experiments/experiments-round-summary.md": (
                "# Experiments Round Summary\n"
            ),
            "docs/experiments/adviser-round-review.md": "# Adviser Round Review\n",
            "docs/experiments/phase-scorecard.md": (
                "# Phase Scorecard\n\n- Gate readiness: `approve`\n"
            ),
        }
        for path, content in experiments_artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Initialize experiments phase
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="experiments",
            actor="code",
            note="Starting experiments phase",
        )
        self.assertEqual("experiment_design", result["current_substep"])

        # Experiments substep 1: experiment_design
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="experiments",
            actor="adviser",
            review_status="approved",
            note="Approved experiment_design",
        )
        self.assertEqual("experiment_execution", result["current_substep"])
        all_checkpoints.append("experiments-experiment_design-approved")

        # Experiments substep 2: experiment_execution
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="experiments",
            actor="adviser",
            review_status="approved",
            note="Approved experiment_execution",
        )
        self.assertEqual("results_analysis", result["current_substep"])
        all_checkpoints.append("experiments-experiment_execution-approved")

        # Experiments substep 3: results_analysis (last substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="experiments",
            actor="adviser",
            review_status="approved",
            note="Approved results_analysis",
        )
        all_checkpoints.append("experiments-results_analysis-approved")

        # Experiments gate approval and transition to paper
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="experiments",
            actor="adviser",
            gate_status="approved",
            increment_loop=True,
            auto_transition=True,
            note="Experiments complete, transitioning to paper.",
        )
        self.assertEqual("advance", result["decision"])
        self.assertEqual("paper", result["transitioned_to"])
        all_checkpoints.append("phase-gate-experiments-approved")

        # ==================== PAPER PHASE ====================
        # Create paper artifacts with correct structured signals for quality gate
        # Substep artifacts: paper-outline.md, paper-draft.md, citation-audit-report.md
        # Phase deliverables: paper_draft, citation_audit_report, final_acceptance_report,
        #   paper_scorecard, reviewer_report
        paper_artifacts = {
            # Substep artifacts
            "paper/paper-outline.md": "# Paper Outline\n\nStructure of the paper.\n",
            "paper/paper-draft.md": "# Paper Draft\n\nFull paper draft.\n",
            "paper/citation-audit-report.md": (
                "# Citation Audit Report\n\n- Citation authenticity status: `verified`\n"
            ),
            # Additional phase deliverables for quality gate
            "paper/reviewer-report.md": (
                "# Reviewer Report\n\n"
                "- Submission bar: `top-tier journal/conference ready`\n"
                "- Verdict: `accept`\n"
            ),
            "docs/paper/final-acceptance-report.md": (
                "# Final Acceptance Report\n\n"
                "- Meets top-tier venue bar: `yes`\n"
                "- Recommendation: `approve`\n"
            ),
            "docs/paper/phase-scorecard.md": (
                "# Phase Scorecard\n\n- Gate readiness: `approve`\n"
            ),
            # Other artifacts
            "paper/paper-round-summary.md": "# Paper Round Summary\n",
            "paper/reviewer-round-review.md": "# Reviewer Round Review\n",
        }
        for path, content in paper_artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Initialize paper phase
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="paper",
            actor="writer",
            note="Starting paper phase",
        )
        self.assertEqual("paper_planning", result["current_substep"])

        # Paper substep 1: paper_planning
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="paper",
            actor="reviewer",
            review_status="approved",
            note="Approved paper_planning",
        )
        self.assertEqual("paper_writing", result["current_substep"])
        all_checkpoints.append("paper-paper_planning-approved")

        # Paper substep 2: paper_writing
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="paper",
            actor="reviewer",
            review_status="approved",
            note="Approved paper_writing",
        )
        self.assertEqual("citation_curation", result["current_substep"])
        all_checkpoints.append("paper-paper_writing-approved")

        # Paper substep 3: citation_curation (last substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="paper",
            actor="reviewer",
            review_status="approved",
            note="Approved citation_curation",
        )
        all_checkpoints.append("paper-citation_curation-approved")

        # Paper gate approval and transition to reflection
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="paper",
            actor="reviewer",
            gate_status="approved",
            increment_loop=True,
            auto_transition=True,
            note="Paper complete, transitioning to reflection.",
        )
        self.assertEqual("advance", result["decision"])
        self.assertEqual("reflection", result["transitioned_to"])
        all_checkpoints.append("phase-gate-paper-approved")

        # ==================== REFLECTION PHASE ====================
        # Create reflection artifacts
        # Note: runtime_improvement_report needs 'Recommendation: approve' for gate signal
        reflection_artifacts = {
            "docs/reflection/lessons-learned.md": (
                "# Lessons Learned\n\nKey takeaways from the project.\n"
            ),
            "docs/reflection/runtime-improvement-report.md": (
                "# Runtime Improvement Report\n\n- Recommendation: `approve`\n"
            ),
            "docs/reflection/reflection-round-summary.md": ("# Reflection Round Summary\n"),
            "docs/reflection/curator-round-review.md": "# Curator Round Review\n",
            "docs/reflection/phase-scorecard.md": (
                "# Phase Scorecard\n\n- Gate readiness: `approve`\n"
            ),
        }
        for path, content in reflection_artifacts.items():
            file_path = self.project_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        # Initialize reflection phase
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="reflection",
            actor="reflector",
            note="Starting reflection phase",
        )
        self.assertEqual("lessons_extraction", result["current_substep"])

        # Reflection substep 1: lessons_extraction
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="reflection",
            actor="curator",
            review_status="approved",
            note="Approved lessons_extraction",
        )
        self.assertEqual("overlay_proposal", result["current_substep"])
        all_checkpoints.append("reflection-lessons_extraction-approved")

        # Reflection substep 2: overlay_proposal (last substep)
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="reflection",
            actor="curator",
            review_status="approved",
            note="Approved overlay_proposal",
        )
        all_checkpoints.append("reflection-overlay_proposal-approved")

        # Reflection gate approval (project complete)
        # Note: Do NOT use auto_transition=True because "archive" is not in PHASE_SEQUENCE
        result = STAGE.run_stage_loop(
            self.project_root,
            phase="reflection",
            actor="curator",
            gate_status="approved",
            increment_loop=True,
            auto_transition=False,
            note="Reflection complete, project finished.",
        )
        # Gate should advance, but transitioned_to is None because we don't auto-transition
        self.assertEqual("advance", result["decision"])
        self.assertIsNone(
            result["transitioned_to"]
        )  # No transition since archive not in PHASE_SEQUENCE
        all_checkpoints.append("phase-gate-reflection-approved")

        # ==================== FINAL VERIFICATION ====================
        # Verify all GitMem checkpoints were created
        tags = COMMON.gitmem_list_tags(self.project_root)
        for checkpoint in all_checkpoints:
            self.assertIn(checkpoint, tags, f"Missing checkpoint: {checkpoint}")

        # Verify final state
        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")

        # Verify all phases completed
        self.assertEqual("reflection", state["current_phase"])

        # Verify all survey substeps are approved
        for substep in ["literature_survey", "idea_definition", "research_plan"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["survey"][substep]["status"],
                f"Survey substep {substep} not approved",
            )

        # Verify all pilot substeps are approved
        for substep in ["problem_analysis", "pilot_design", "pilot_execution"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["pilot"][substep]["status"],
                f"Pilot substep {substep} not approved",
            )

        # Verify all experiments substeps are approved
        for substep in ["experiment_design", "experiment_execution", "results_analysis"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["experiments"][substep]["status"],
                f"Experiments substep {substep} not approved",
            )

        # Verify all paper substeps are approved
        for substep in ["paper_planning", "paper_writing", "citation_curation"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["paper"][substep]["status"],
                f"Paper substep {substep} not approved",
            )

        # Verify all reflection substeps are approved
        for substep in ["lessons_extraction", "overlay_proposal"]:
            self.assertEqual(
                "approved",
                state["substep_status"]["reflection"][substep]["status"],
                f"Reflection substep {substep} not approved",
            )

        # Verify checkpoint count: 15 substeps + 5 phase gates = 20 checkpoints
        self.assertEqual(20, len(tags), f"Expected 20 checkpoints, got {len(tags)}: {tags}")


class TestMultiPhaseSubstepWorkflow(unittest.TestCase):
    """Test substep workflow across multiple phases."""

    def setUp(self) -> None:
        """Set up a test project."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "multi-phase-test"
        INIT.initialize_research_project(project_root=self.project_root, topic="Multi-phase test")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_substep_status_isolated_between_phases(self) -> None:
        """Test that substep status is isolated between phases."""
        # Complete survey substeps
        artifact = self.project_root / "docs/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Survey\n", encoding="utf-8")

        STAGE.run_stage_loop(
            self.project_root,
            phase="survey",
            actor="critic",
            review_status="approved",
            note="Approved survey",
        )

        state = COMMON.read_yaml(self.project_root / ".autoresearch/state/research-state.yaml")

        # Survey substep should be approved
        self.assertEqual(
            "approved",
            state["substep_status"]["survey"]["literature_survey"]["status"],
        )

        # After approval of literature_survey, idea_definition should be in_progress
        self.assertEqual(
            "in_progress",
            state["substep_status"]["survey"]["idea_definition"]["status"],
        )

        # Pilot substeps should all be pending (not yet started)
        for substep in ["problem_analysis", "pilot_design", "pilot_execution"]:
            self.assertEqual(
                "pending",
                state["substep_status"]["pilot"][substep]["status"],
            )


if __name__ == "__main__":
    unittest.main()
