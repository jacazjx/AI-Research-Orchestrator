"""State builder: build_state and helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from constants import (
    DEFAULT_DELIVERABLES,
    DEFAULT_LOOP_LIMITS,
    PHASE_COMPLETION,
    PHASE_TO_GATE,
    SYSTEM_VERSION,
)
from project.client import DEFAULT_LANGUAGE_POLICY


def build_state(
    project_id: str,
    topic: str,
    init_source: str,
    init_paths: list[str],
    client_profile: str,
    client_instruction_file: str,
    process_language: str = DEFAULT_LANGUAGE_POLICY["process_docs"],
    paper_language: str = DEFAULT_LANGUAGE_POLICY["paper_docs"],
    starting_phase: str = "survey",
) -> dict[str, Any]:
    """Build a new project state dictionary.

    Args:
        project_id: Unique project identifier.
        topic: Research topic string.
        init_source: Source of initialization.
        init_paths: List of detected init artifact paths.
        client_profile: Client profile name.
        client_instruction_file: Client instruction filename.
        process_language: Language for process documents.
        paper_language: Language for paper documents.
        starting_phase: Starting phase name.

    Returns:
        Complete project state dictionary.
    """
    starting_gate = PHASE_TO_GATE.get(starting_phase, "gate_1")
    created_at = datetime.now(timezone.utc).isoformat()

    return {
        "project_id": project_id,
        "topic": topic,
        "platform": client_profile,
        "client_profile": client_profile,
        "client_instruction_file": client_instruction_file,
        "phase": starting_phase,
        "subphase": "entry",
        "current_phase": starting_phase,
        "current_gate": starting_gate,
        "system_version": SYSTEM_VERSION,
        "created_at": created_at,
        "last_modified": created_at,
        "approval_status": {
            "gate_1": "pending",
            "gate_2": "pending",
            "gate_3": "pending",
            "gate_4": "pending",
            "gate_5": "pending",
        },
        "phase_reviews": {
            "survey_critic": "pending",
            "pilot_adviser": "pending",
            "experiment_adviser": "pending",
            "paper_reviewer": "pending",
            "reflection_curator": "pending",
        },
        "current_substep": None,
        "substep_status": _build_default_substep_status(),
        "language_policy": {
            "process_docs": process_language,
            "paper_docs": paper_language,
        },
        # inner_loops: Per-phase iteration counter that resets when a phase is
        # re-entered (e.g., after a rollback/pivot). Tracks iterations within
        # the current attempt at a phase.
        "inner_loops": {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        },
        # loop_counts: Cumulative per-phase iteration counter that never resets.
        # Tracks total iterations across all attempts.
        "loop_counts": {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        },
        "outer_loop": 0,
        "loop_limits": dict(DEFAULT_LOOP_LIMITS),
        "gate_scores": {
            "gate_1": 0,
            "gate_2": 0,
            "gate_3": 0,
            "gate_4": 0,
            "gate_5": 0,
        },
        "gate_history": [],
        "pivot_candidates": [],
        "human_decisions": [],
        "overlay_stack": [],
        "active_jobs": [],
        "recovery_status": "idle",
        "init_artifacts": {
            "source": init_source,
            "detected_paths": init_paths,
        },
        "dashboard_paths": {
            "status": DEFAULT_DELIVERABLES["dashboard_status"],
            "progress": DEFAULT_DELIVERABLES["dashboard_progress"],
            "timeline": DEFAULT_DELIVERABLES["dashboard_timeline"],
        },
        "runtime": {
            "job_registry": DEFAULT_DELIVERABLES["job_registry"],
            "gpu_registry": DEFAULT_DELIVERABLES["gpu_registry"],
            "backend_registry": DEFAULT_DELIVERABLES["backend_registry"],
            "sentinel_events": DEFAULT_DELIVERABLES["sentinel_events"],
        },
        "progress": {
            "completion_percent": PHASE_COMPLETION.get(starting_phase, 0),
            "current_agent": "orchestrator",
            "last_gate_result": "not_started",
            "active_blocker": "none",
            "next_action": f"prepare-phase-{starting_phase}",
            "active_backend": "local",
            "active_gpu": "unassigned",
            "allowed_return_phases": [],
            "suggested_return_phase": starting_phase,
        },
        "deliverables": dict(DEFAULT_DELIVERABLES),
        "starting_phase": starting_phase,
        "state_version": "2.0.0",
        "research_type": "ml_experiment",
        "user_config_inherited": {},
        "gpu_usage_history": [],
    }


def _build_default_substep_status() -> dict[str, Any]:
    """Build the default substep status structure."""
    return {
        "survey": {
            "literature_survey": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "idea_definition": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "research_plan": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "pilot": {
            "problem_validation": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "problem_analysis": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "pilot_design": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "pilot_execution": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "experiments": {
            "experiment_design": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "experiment_execution": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "results_analysis": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "paper": {
            "paper_planning": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "paper_writing": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "citation_curation": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "reflection": {
            "lessons_extraction": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "overlay_proposal": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "system_evaluation": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
    }
