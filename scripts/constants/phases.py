"""Phase-related constants for the Research Orchestrator."""

from typing import Dict, Tuple

# Phase sequence (semantic names only)
PHASE_SEQUENCE = (
    "survey",
    "pilot",
    "experiments",
    "paper",
    "reflection",
)

RESEARCH_TYPE_PHASE_SEQUENCE: Dict[str, Tuple[str, ...]] = {
    "ml_experiment": (
        "survey",
        "pilot",
        "experiments",
        "paper",
        "reflection",
    ),
    "theory": (
        "survey",
        "pilot",
        "paper",
        "reflection",
    ),
    "survey": (
        "survey",
        "paper",
        "reflection",
    ),
    "applied": (
        "survey",
        "pilot",
        "experiments",
        "paper",
        "reflection",
    ),
}

# Agent pairs for each phase (primary, reviewer)
PHASE_AGENT_PAIRS: Dict[str, Tuple[str, str]] = {
    # Semantic names only (legacy names are normalized)
    "survey": ("survey", "critic"),
    "pilot": ("code", "adviser"),
    "experiments": ("code", "adviser"),
    "paper": ("writer", "reviewer"),
    "reflection": ("reflector", "curator"),
}

# Phase name mapping (legacy to semantic)
LEGACY_TO_SEMANTIC_PHASE = {
    "01-survey": "survey",
    "02-pilot-analysis": "pilot",
    "03-full-experiments": "experiments",
    "04-paper": "paper",
    "05-reflection-evolution": "reflection",
}

SEMANTIC_TO_LEGACY_PHASE = {v: k for k, v in LEGACY_TO_SEMANTIC_PHASE.items()}

# Phase to gate mapping
PHASE_TO_GATE = {
    "survey": "gate_1",
    "pilot": "gate_2",
    "experiments": "gate_3",
    "paper": "gate_4",
    "reflection": "gate_5",
}

# Handoff requirements between phases
HANDOFF_REQUIREMENTS = {
    "survey-to-pilot": {
        "statuses": (
            ("phase_reviews", "survey_critic"),
            ("approval_status", "gate_1"),
        ),
        "deliverables": ("readiness_report", "survey_scorecard"),
        "next_phase": "pilot",
    },
    "pilot-to-experiments": {
        "statuses": (
            ("phase_reviews", "pilot_adviser"),
            ("approval_status", "gate_2"),
        ),
        "deliverables": (
            "problem_validation_report",
            "problem_analysis",
            "pilot_plan",
            "pilot_results",
            "pilot_adviser_review",
            "pilot_validation_report",
            "pilot_scorecard",
        ),
        "next_phase": "experiments",
    },
    "experiments-to-paper": {
        "statuses": (
            ("phase_reviews", "experiment_adviser"),
            ("approval_status", "gate_3"),
        ),
        "deliverables": (
            "experiment_spec",
            "run_registry",
            "results_summary",
            "checkpoint_index",
            "experiment_adviser_review",
            "evidence_package_index",
            "experiment_scorecard",
        ),
        "next_phase": "paper",
    },
    "paper-to-reflection": {
        "statuses": (
            ("phase_reviews", "paper_reviewer"),
            ("approval_status", "gate_4"),
        ),
        "deliverables": (
            "paper_draft",
            "citation_audit_report",
            "reviewer_report",
            "rebuttal_log",
            "final_acceptance_report",
            "paper_scorecard",
        ),
        "next_phase": "reflection",
    },
    "reflection-closeout": {
        "statuses": (
            ("phase_reviews", "reflection_curator"),
            ("approval_status", "gate_5"),
        ),
        "deliverables": (
            "lessons_learned",
            "overlay_draft",
            "runtime_improvement_report",
            "reflection_scorecard",
            "system_evaluation_report",
        ),
        "next_phase": "handoff-user",
    },
}

# Required deliverables for each phase
# Only CORE gate deliverables listed here.
# Agents decide what additional artifacts to produce.
# HANDOFF_REQUIREMENTS may check additional files for phase transitions.
PHASE_REQUIRED_DELIVERABLES = {
    "survey": ("readiness_report",),
    "pilot": ("pilot_results",),
    "experiments": ("evidence_package_index",),
    "paper": ("paper_draft",),
    "reflection": ("lessons_learned",),
}

# Default deliverables with their paths
DEFAULT_DELIVERABLES = {
    # System/admin files (in .autoresearch/)
    "workspace_manifest": ".autoresearch/workspace-manifest.md",
    "research_state": ".autoresearch/state/research-state.yaml",
    "project_config": ".autoresearch/config/orchestrator-config.yaml",
    "idea_brief": ".autoresearch/idea-brief.md",
    "reference_library_index": ".autoresearch/reference-papers/README.md",
    "dashboard_status": ".autoresearch/dashboard/status.json",
    "dashboard_progress": ".autoresearch/dashboard/progress.md",
    "dashboard_timeline": ".autoresearch/dashboard/timeline.ndjson",
    "job_registry": ".autoresearch/runtime/job-registry.yaml",
    "gpu_registry": ".autoresearch/runtime/gpu-registry.yaml",
    "backend_registry": ".autoresearch/runtime/backend-registry.yaml",
    "sentinel_events": ".autoresearch/runtime/sentinel-events.ndjson",
    # Legacy paths (preserved for backward compatibility)
    "survey_round_log": "agents/survey/survey-round-summary.md",
    "critic_round_log": "agents/critic/critic-round-review.md",
    "readiness_report": "docs/survey/research-readiness-report.md",
    "survey_scorecard": "docs/survey/phase-scorecard.md",
    "problem_validation_report": "docs/pilot/problem-validation-report.md",
    "problem_analysis": "docs/pilot/problem-analysis.md",
    "pilot_plan": "code/configs/pilot-experiment-plan.md",
    "pilot_results": "docs/pilot/pilot-results.md",
    "pilot_adviser_review": "docs/pilot/pilot-adviser-review.md",
    "pilot_validation_report": "docs/pilot/pilot-validation-report.md",
    "pilot_scorecard": "docs/pilot/phase-scorecard.md",
    "experiment_spec": "code/configs/experiment-spec.md",
    "run_registry": "code/checkpoints/run-registry.md",
    "results_summary": "docs/experiments/results-summary.md",
    "checkpoint_index": "code/checkpoints/checkpoint-index.md",
    "experiment_adviser_review": "docs/experiments/experiment-adviser-review.md",
    "evidence_package_index": "docs/experiments/evidence-package-index.md",
    "experiment_scorecard": "docs/experiments/phase-scorecard.md",
    "paper_draft": "paper/paper-draft.md",
    "citation_audit_report": "paper/citation-audit-report.md",
    "reviewer_report": "paper/reviewer-report.md",
    "rebuttal_log": "paper/rebuttal-log.md",
    "final_acceptance_report": "docs/paper/final-acceptance-report.md",
    "paper_scorecard": "docs/paper/phase-scorecard.md",
    "lessons_learned": "docs/reflection/lessons-learned.md",
    "overlay_draft": "paper/overlay-draft.md",
    "runtime_improvement_report": "docs/reflection/runtime-improvement-report.md",
    "reflection_scorecard": "docs/reflection/phase-scorecard.md",
    "system_evaluation_report": "docs/reflection/system-evaluation-report.md",
    "archive_index": ".autoresearch/archive/archive-index.md",
}

# Next phase mapping
NEXT_PHASE = {
    "survey": "pilot",
    "pilot": "experiments",
    "experiments": "paper",
    "paper": "reflection",
    "reflection": "archive",
}

# Phase to review mapping
PHASE_TO_REVIEW = {
    "survey": "survey_critic",
    "pilot": "pilot_adviser",
    "experiments": "experiment_adviser",
    "paper": "paper_reviewer",
    "reflection": "reflection_curator",
}

# Phase loop key mapping
PHASE_LOOP_KEY = {
    "survey": "survey_critic",
    "pilot": "pilot_code_adviser",
    "experiments": "experiment_code_adviser",
    "paper": "writer_reviewer",
    "reflection": "reflector_curator",
}

# Phase completion percentages
PHASE_COMPLETION = {
    "survey": 0,
    "pilot": 20,
    "experiments": 40,
    "paper": 60,
    "reflection": 80,
}

# Default loop limits for each phase
DEFAULT_LOOP_LIMITS = {
    "survey_critic": 3,
    "pilot_code_adviser": 3,
    "experiment_code_adviser": 3,
    "writer_reviewer": 3,
    "reflector_curator": 2,
}

# Loop requirements for each phase
LOOP_REQUIREMENTS = {
    "survey-loop": ("survey_critic", "phase_reviews", "survey_critic"),
    "pilot-loop": ("pilot_code_adviser", "phase_reviews", "pilot_adviser"),
    "experiment-loop": (
        "experiment_code_adviser",
        "phase_reviews",
        "experiment_adviser",
    ),
    "paper-loop": ("writer_reviewer", "phase_reviews", "paper_reviewer"),
    "reflection-loop": ("reflector_curator", "phase_reviews", "reflection_curator"),
}


# Helper functions for phase name conversion
def normalize_phase_name(phase_name: str) -> str:
    """Convert legacy phase name to semantic name."""
    return LEGACY_TO_SEMANTIC_PHASE.get(phase_name, phase_name)


def get_legacy_phase_name(phase_name: str) -> str:
    """Convert semantic phase name to legacy name."""
    return SEMANTIC_TO_LEGACY_PHASE.get(phase_name, phase_name)


def get_all_phase_aliases(phase_name: str) -> list:
    """Get all valid names for a phase (semantic + legacy)."""
    semantic = normalize_phase_name(phase_name)
    legacy = get_legacy_phase_name(semantic)
    if semantic == legacy:
        return [semantic]
    return [semantic, legacy]


def get_phase_agents(phase_name: str) -> Tuple[str, str]:
    """Get the agent pair (primary, reviewer) for a phase.

    Args:
        phase_name: Phase name (semantic or legacy format).

    Returns:
        Tuple of (primary_agent, reviewer_agent).

    Raises:
        ValueError: If phase name is unknown.
    """
    normalized = normalize_phase_name(phase_name)
    if normalized not in PHASE_AGENT_PAIRS:
        raise ValueError(f"Unknown phase: {phase_name}")
    return PHASE_AGENT_PAIRS[normalized]


def get_phase_sequence_for_research_type(research_type: str) -> Tuple[str, ...]:
    """Get phase sequence for a research type."""
    return RESEARCH_TYPE_PHASE_SEQUENCE.get(research_type, PHASE_SEQUENCE)
