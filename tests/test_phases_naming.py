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

    def test_research_type_phase_sequences(self):
        """Each research type should have a valid phase subsequence."""
        from constants.phases import (
            PHASE_SEQUENCE,
            RESEARCH_TYPE_PHASE_SEQUENCE,
            get_phase_sequence_for_research_type,
        )

        for rt, seq in RESEARCH_TYPE_PHASE_SEQUENCE.items():
            assert len(seq) >= 2, f"Research type '{rt}' has fewer than 2 phases"
            for phase in seq:
                assert (
                    phase in PHASE_SEQUENCE
                ), f"Phase '{phase}' in research type '{rt}' is not in PHASE_SEQUENCE"
            # Verify order is consistent with PHASE_SEQUENCE
            indices = [PHASE_SEQUENCE.index(p) for p in seq]
            assert indices == sorted(
                indices
            ), f"Phase order for '{rt}' is not consistent with PHASE_SEQUENCE"

        # get_phase_sequence_for_research_type fallback
        assert get_phase_sequence_for_research_type("unknown") == PHASE_SEQUENCE

    def test_get_next_phase_for_state_default(self):
        """get_next_phase_for_state falls back to NEXT_PHASE without phase_sequence."""
        from constants.phases import NEXT_PHASE, get_next_phase_for_state

        state = {"current_phase": "survey"}
        assert get_next_phase_for_state(state) == NEXT_PHASE["survey"]

    def test_get_next_phase_for_state_theory(self):
        """Theory research type skips experiments phase."""
        from constants.phases import get_next_phase_for_state

        state = {
            "current_phase": "pilot",
            "phase_sequence": ["survey", "pilot", "paper", "reflection"],
        }
        assert get_next_phase_for_state(state) == "paper"

    def test_get_next_phase_for_state_survey_type(self):
        """Survey research type goes directly from survey to paper."""
        from constants.phases import get_next_phase_for_state

        state = {
            "current_phase": "survey",
            "phase_sequence": ["survey", "paper", "reflection"],
        }
        assert get_next_phase_for_state(state) == "paper"

    def test_get_next_phase_for_state_final(self):
        """Final phase returns archive."""
        from constants.phases import get_next_phase_for_state

        state = {
            "current_phase": "reflection",
            "phase_sequence": ["survey", "paper", "reflection"],
        }
        assert get_next_phase_for_state(state) == "archive"
