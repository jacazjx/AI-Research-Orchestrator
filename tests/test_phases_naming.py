"""Tests for phase-agent naming consistency."""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path so constants package is importable
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))


class TestPhaseAgentNaming:
    """Verify PHASE_AGENT_PAIRS matches actual SKILL.md definitions."""

    def test_paper_phase_agent_names_match_skill_files(self):
        """Paper phase should use 'writer' and 'reviewer' (no hyphens)."""
        from constants.phases import PHASE_AGENT_PAIRS

        primary, reviewer = PHASE_AGENT_PAIRS["paper"]

        # Should match SKILL.md names (without hyphens)
        assert primary == "writer", f"Expected 'writer', got '{primary}'"
        assert reviewer == "reviewer", f"Expected 'reviewer', got '{reviewer}'"

    def test_all_agent_names_exist_as_skills(self):
        """Every agent name in PHASE_AGENT_PAIRS should have a corresponding SKILL.md.

        Note: Some agent names map to different skill directory names:
        - "code" agent -> "coder" skill directory
        """
        from constants.phases import PHASE_AGENT_PAIRS

        skill_dir = Path(__file__).parent.parent / "skills"

        # Mapping from agent name to skill directory name (when they differ)
        agent_to_skill = {
            "code": "coder",  # "code" agent uses "coder" skill
        }

        for phase, (primary, reviewer) in PHASE_AGENT_PAIRS.items():
            primary_skill_name = agent_to_skill.get(primary, primary)
            reviewer_skill_name = agent_to_skill.get(reviewer, reviewer)

            primary_skill = skill_dir / primary_skill_name / "SKILL.md"
            reviewer_skill = skill_dir / reviewer_skill_name / "SKILL.md"

            assert primary_skill.exists(), f"Missing skill for primary agent '{primary}' (looked in '{primary_skill_name}') in phase '{phase}'"
            assert reviewer_skill.exists(), f"Missing skill for reviewer agent '{reviewer}' (looked in '{reviewer_skill_name}') in phase '{phase}'"

    def test_agent_names_no_hyphens(self):
        """Agent names should not contain hyphens for consistency."""
        from constants.phases import PHASE_AGENT_PAIRS

        for phase, (primary, reviewer) in PHASE_AGENT_PAIRS.items():
            assert "-" not in primary, f"Primary agent '{primary}' in phase '{phase}' contains hyphen"
            assert "-" not in reviewer, f"Reviewer agent '{reviewer}' in phase '{phase}' contains hyphen"
