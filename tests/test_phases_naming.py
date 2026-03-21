"""Tests for phase-agent naming consistency."""

import sys
from pathlib import Path

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

    def test_all_agent_names_exist_as_agent_definitions(self):
        """Every agent name in PHASE_AGENT_PAIRS should have an AGENT.md in agents/.

        Agent role definitions live in agents/<role>/AGENT.md, not in skills/.
        """
        from constants.phases import PHASE_AGENT_PAIRS

        agent_dir = Path(__file__).parent.parent / "agents"

        # Mapping from agent name to agent directory name (when they differ)
        agent_to_dir = {
            "code": "coder",  # "code" agent uses "coder" directory
        }

        for phase, (primary, reviewer) in PHASE_AGENT_PAIRS.items():
            primary_dir_name = agent_to_dir.get(primary, primary)
            reviewer_dir_name = agent_to_dir.get(reviewer, reviewer)

            primary_agent = agent_dir / primary_dir_name / "AGENT.md"
            reviewer_agent = agent_dir / reviewer_dir_name / "AGENT.md"

            assert primary_agent.exists(), (
                f"Missing AGENT.md for primary agent '{primary}'"
                f" (looked in '{primary_dir_name}') in phase '{phase}'"
            )
            assert reviewer_agent.exists(), (
                f"Missing AGENT.md for reviewer agent '{reviewer}'"
                f" (looked in '{reviewer_dir_name}') in phase '{phase}'"
            )

    def test_agent_names_no_hyphens(self):
        """Agent names should not contain hyphens for consistency."""
        from constants.phases import PHASE_AGENT_PAIRS

        for phase, (primary, reviewer) in PHASE_AGENT_PAIRS.items():
            assert (
                "-" not in primary
            ), f"Primary agent '{primary}' in phase '{phase}' contains hyphen"
            assert (
                "-" not in reviewer
            ), f"Reviewer agent '{reviewer}' in phase '{phase}' contains hyphen"
