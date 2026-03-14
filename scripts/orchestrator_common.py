from __future__ import annotations

import json
import logging
import os
import re
import shlex
import tempfile
from pathlib import Path
from typing import Any

import yaml

# Configure module logger
logger = logging.getLogger(__name__)

# System version
SYSTEM_VERSION = "1.12.0"
SYSTEM_VERSION_NAME = "Research Orchestrator"
VERSION_HISTORY = [
    ("1.0.0", "2026-03-01", "Initial release with five-phase workflow"),
    ("1.1.0", "2026-03-05", "Added agent responsibilities and literature verification"),
    ("1.2.0", "2026-03-08", "Added system audit and quality enforcement"),
    ("1.3.0", "2026-03-10", "Added project takeover capability"),
    ("1.4.0", "2026-03-13", "Added starting phase selection"),
    ("1.5.0", "2026-03-13", "Added statusline display and version tracking"),
    ("1.6.0", "2026-03-13", "Switched to PyYAML for full YAML support (comments, complex structures)"),
    ("1.7.0", "2026-03-13", "Fixed KeyError in deliverables, added sub-agent failure recovery protocol"),
    ("1.8.0", "2026-03-13", "Auto-complete missing deliverables on state load for backward compatibility"),
    ("1.9.0", "2026-03-14", "Integrated ralph-loop for phase iteration control with completion promises"),
    ("1.10.0", "2026-03-14", "Added experiment execution best practices (unbuffered output, checkpoint, process management) and document sync rules"),
    ("1.11.0", "2026-03-14", "ARIS integration: cross-model review via Codex MCP, REVIEW_STATE persistence for long-running loops"),
    ("1.12.0", "2026-03-14", "Full ARIS integration: 17 skills, three workflows, IDEA_STATE persistence, GPU protection, AUTO_PROCEED switch"),
]

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_ROOT = SKILL_DIR / "assets" / "templates"


# Legacy phase directories (numbered format) - kept for backward compatibility
PHASE_DIRECTORIES = (
    "00-admin",
    "01-survey",
    "02-pilot-analysis",
    "03-full-experiments",
    "04-paper",
    "05-reflection-evolution",
    "06-archive",
)

# New semantic folder structure (Chunk 1 of folder restructure)
MAIN_DIRECTORIES = (
    "paper",
    "code",
    "docs",
)

AGENT_DIRECTORIES = (
    "agents/survey",
    "agents/critic",
    "agents/coder",
    "agents/adviser",
    "agents/writer",
    "agents/reviewer",
    "agents/reflector",
    "agents/curator",
)

SYSTEM_DIRECTORIES = (
    ".autoresearch/state",
    ".autoresearch/config",
    ".autoresearch/dashboard",
    ".autoresearch/runtime",
    ".autoresearch/reference-papers",
    ".autoresearch/templates",
    ".autoresearch/archive",
)

REQUIRED_DIRECTORIES = MAIN_DIRECTORIES + AGENT_DIRECTORIES + SYSTEM_DIRECTORIES

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
    "readiness_report": "docs/reports/survey/research-readiness-report.md",
    "survey_scorecard": "docs/reports/survey/phase-scorecard.md",
    "problem_analysis": "docs/reports/pilot/problem-analysis.md",
    "pilot_plan": "code/configs/pilot-experiment-plan.md",
    "pilot_results": "docs/reports/pilot/pilot-results.md",
    "pilot_adviser_review": "docs/reports/pilot/pilot-adviser-review.md",
    "pilot_validation_report": "docs/reports/pilot/pilot-validation-report.md",
    "pilot_scorecard": "docs/reports/pilot/phase-scorecard.md",
    "experiment_spec": "code/configs/experiment-spec.md",
    "run_registry": "code/checkpoints/run-registry.md",
    "results_summary": "docs/reports/experiments/results-summary.md",
    "checkpoint_index": "code/checkpoints/checkpoint-index.md",
    "experiment_adviser_review": "docs/reports/experiments/experiment-adviser-review.md",
    "evidence_package_index": "docs/reports/experiments/evidence-package-index.md",
    "experiment_scorecard": "docs/reports/experiments/phase-scorecard.md",
    "paper_draft": "paper/paper-draft.md",
    "citation_audit_report": "paper/citation-audit-report.md",
    "reviewer_report": "paper/reviewer-report.md",
    "rebuttal_log": "paper/rebuttal-log.md",
    "final_acceptance_report": "docs/reports/paper/final-acceptance-report.md",
    "paper_scorecard": "docs/reports/paper/phase-scorecard.md",
    "lessons_learned": "docs/reports/reflection/lessons-learned.md",
    "overlay_draft": "paper/overlay-draft.md",
    "runtime_improvement_report": "docs/reports/reflection/runtime-improvement-report.md",
    "reflection_scorecard": "docs/reports/reflection/phase-scorecard.md",
    "archive_index": ".autoresearch/archive/archive-index.md",
}

DEFAULT_LANGUAGE_POLICY = {
    "process_docs": "zh-CN",
    "paper_docs": "en-US",
}

DEFAULT_LOOP_LIMITS = {
    "survey_critic": 3,
    "pilot_code_adviser": 3,
    "experiment_code_adviser": 3,
    "writer_reviewer": 3,
    "reflector_curator": 2,
}

# ARIS Integration: Cross-model review configuration
# Default reviewer model for Codex MCP integration (GPT-5.4 with xhigh reasoning)
DEFAULT_REVIEWER_CONFIG = {
    "model": "gpt-5.4",
    "reasoning_effort": "xhigh",
    "enabled": False,  # Disabled by default, use local sub-agent
}

# ARIS Integration: Review state for long-running loops
# This file survives context compaction and allows loop resumption
REVIEW_STATE_FILENAME = "REVIEW_STATE.json"

# ARIS Integration: Maximum rounds for auto-review-loop
MAX_REVIEW_ROUNDS = 4

# ARIS Integration: Positive assessment threshold
POSITIVE_SCORE_THRESHOLD = 6.0
POSITIVE_VERDICT_KEYWORDS = ("accept", "sufficient", "ready for submission", "almost")

# ARIS Integration: Complete configuration
# Note: GPU protection fields are defined here but enforcement is v1.13.0
DEFAULT_ARIS_CONFIG = {
    "auto_proceed": False,
    "pilot_max_hours": 2,          # v1.13.0: enforcement pending
    "pilot_timeout_hours": 3,       # v1.13.0: enforcement pending
    "max_pilot_ideas": 3,           # v1.13.0: enforcement pending
    "max_total_gpu_hours": 8,       # v1.13.0: enforcement pending
    "reviewer": {
        "enabled": False,
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
    },
    "max_review_rounds": 4,
    "positive_score_threshold": 6.0,
    "feishu": {
        "enabled": False,
        "mode": "off",  # off / push / interactive
    },
}

# ARIS Integration: Idea state filename for idea-discovery pipeline
IDEA_STATE_FILENAME = "IDEA_STATE.json"

DEFAULT_RUNTIME_CONFIG = {
    "languages": dict(DEFAULT_LANGUAGE_POLICY),
    "loop_limits": dict(DEFAULT_LOOP_LIMITS),
    "runtime": {
        "stale_after_minutes": 30,
        "auto_discover_gpu": True,
    },
    "backends": {
        "local": "enabled",
        "ssh": "enabled",
    },
    "reviewer": dict(DEFAULT_REVIEWER_CONFIG),
}

EXPECTED_DELIVERABLE_PREFIXES = {
    "workspace_manifest": ".autoresearch/",
    "research_state": ".autoresearch/",
    "project_config": ".autoresearch/",
    "idea_brief": ".autoresearch/",
    "reference_library_index": ".autoresearch/",
    "dashboard_status": ".autoresearch/",
    "dashboard_progress": ".autoresearch/",
    "dashboard_timeline": ".autoresearch/",
    "job_registry": ".autoresearch/",
    "gpu_registry": ".autoresearch/",
    "backend_registry": ".autoresearch/",
    "sentinel_events": ".autoresearch/",
    "survey_round_log": "agents/",
    "critic_round_log": "agents/",
    "readiness_report": "docs/",
    "survey_scorecard": "agents/",
    "problem_analysis": "docs/",
    "pilot_plan": "code/",
    "pilot_results": "code/",
    "pilot_adviser_review": "agents/",
    "pilot_validation_report": "docs/",
    "pilot_scorecard": "agents/",
    "experiment_spec": "code/",
    "run_registry": "code/",
    "results_summary": "code/",
    "checkpoint_index": "code/",
    "experiment_adviser_review": "agents/",
    "evidence_package_index": "docs/",
    "experiment_scorecard": "agents/",
    "paper_draft": "paper/",
    "citation_audit_report": "paper/",
    "reviewer_report": "paper/",
    "rebuttal_log": "paper/",
    "final_acceptance_report": "paper/",
    "paper_scorecard": "agents/",
    "lessons_learned": "docs/",
    "overlay_draft": "paper/",
    "runtime_improvement_report": ".autoresearch/",
    "reflection_scorecard": "agents/",
    "archive_index": ".autoresearch/",
}

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
        ),
        "next_phase": "handoff-user",
    },
}

LOOP_REQUIREMENTS = {
    "survey-loop": ("survey_critic", "phase_reviews", "survey_critic"),
    "pilot-loop": ("pilot_code_adviser", "phase_reviews", "pilot_adviser"),
    "experiment-loop": ("experiment_code_adviser", "phase_reviews", "experiment_adviser"),
    "paper-loop": ("writer_reviewer", "phase_reviews", "paper_reviewer"),
    "reflection-loop": ("reflector_curator", "phase_reviews", "reflection_curator"),
}

PHASE_TO_GATE = {
    "01-survey": "gate_1",
    "02-pilot-analysis": "gate_2",
    "03-full-experiments": "gate_3",
    "04-paper": "gate_4",
    "05-reflection-evolution": "gate_5",
    # New semantic names
    "survey": "gate_1",
    "pilot": "gate_2",
    "experiments": "gate_3",
    "paper": "gate_4",
    "reflection": "gate_5",
}

PHASE_TO_GATE_LEGACY = {
    "01-survey": "gate_1",
    "02-pilot-analysis": "gate_2",
    "03-full-experiments": "gate_3",
    "04-paper": "gate_4",
    "05-reflection-evolution": "gate_5",
}

NEXT_PHASE = {
    "01-survey": "02-pilot-analysis",
    "02-pilot-analysis": "03-full-experiments",
    "03-full-experiments": "04-paper",
    "04-paper": "05-reflection-evolution",
    "05-reflection-evolution": "06-archive",
    # New semantic names
    "survey": "pilot",
    "pilot": "experiments",
    "experiments": "paper",
    "paper": "reflection",
    "reflection": "archive",
}

NEXT_PHASE_LEGACY = {
    "01-survey": "02-pilot-analysis",
    "02-pilot-analysis": "03-full-experiments",
    "03-full-experiments": "04-paper",
    "04-paper": "05-reflection-evolution",
    "05-reflection-evolution": "06-archive",
}

# Legacy path to new path mapping for migration
OLD_TO_NEW_PATH_MAPPING = {
    # System files
    "00-admin/workspace-manifest.md": "docs/workspace-manifest.md",
    "00-admin/research-state.yaml": ".autoresearch/state/research-state.yaml",
    "00-admin/orchestrator-config.yaml": ".autoresearch/config/orchestrator-config.yaml",
    "00-admin/idea-brief.md": "docs/idea-brief.md",
    "00-admin/reference-papers/README.md": ".autoresearch/reference-papers/README.md",
    "00-admin/dashboard/status.json": ".autoresearch/dashboard/status.json",
    "00-admin/dashboard/progress.md": ".autoresearch/dashboard/progress.md",
    "00-admin/dashboard/timeline.ndjson": ".autoresearch/dashboard/timeline.ndjson",
    "00-admin/runtime/job-registry.yaml": ".autoresearch/runtime/job-registry.yaml",
    "00-admin/runtime/gpu-registry.yaml": ".autoresearch/runtime/gpu-registry.yaml",
    "00-admin/runtime/backend-registry.yaml": ".autoresearch/runtime/backend-registry.yaml",
    "00-admin/runtime/sentinel-events.ndjson": ".autoresearch/runtime/sentinel-events.ndjson",
    # Phase 01 files
    "01-survey/survey-round-summary.md": "agents/survey/survey-round-summary.md",
    "01-survey/critic-round-review.md": "agents/critic/critic-round-review.md",
    "01-survey/research-readiness-report.md": "docs/research-readiness-report.md",
    "01-survey/phase-scorecard.md": "agents/survey/phase-scorecard.md",
    # Phase 02 files
    "02-pilot-analysis/problem-analysis.md": "docs/problem-analysis.md",
    "02-pilot-analysis/pilot-experiment-plan.md": "code/pilot-experiment-plan.md",
    "02-pilot-analysis/pilot-results.md": "code/pilot-results.md",
    "02-pilot-analysis/pilot-adviser-review.md": "agents/adviser/pilot-adviser-review.md",
    "02-pilot-analysis/pilot-validation-report.md": "docs/pilot-validation-report.md",
    "02-pilot-analysis/phase-scorecard.md": "agents/coder/phase-scorecard.md",
    # Phase 03 files
    "03-full-experiments/experiment-spec.md": "code/experiment-spec.md",
    "03-full-experiments/run-registry.md": "code/run-registry.md",
    "03-full-experiments/results-summary.md": "code/results-summary.md",
    "03-full-experiments/checkpoints/checkpoint-index.md": "code/checkpoints/checkpoint-index.md",
    "03-full-experiments/experiment-adviser-review.md": "agents/adviser/experiment-adviser-review.md",
    "03-full-experiments/evidence-package-index.md": "docs/evidence-package-index.md",
    "03-full-experiments/phase-scorecard.md": "agents/coder/phase-scorecard.md",
    # Phase 04 files
    "04-paper/paper-draft.md": "paper/paper-draft.md",
    "04-paper/citation-audit-report.md": "paper/citation-audit-report.md",
    "04-paper/reviewer-report.md": "agents/reviewer/reviewer-report.md",
    "04-paper/rebuttal-log.md": "paper/rebuttal-log.md",
    "04-paper/final-acceptance-report.md": "paper/final-acceptance-report.md",
    "04-paper/phase-scorecard.md": "agents/reviewer/phase-scorecard.md",
    # Phase 05 files
    "05-reflection-evolution/lessons-learned.md": "docs/lessons-learned.md",
    "05-reflection-evolution/overlay-draft.md": "paper/overlay-draft.md",
    "05-reflection-evolution/runtime-improvement-report.md": ".autoresearch/archive/runtime-improvement-report.md",
    "05-reflection-evolution/phase-scorecard.md": "agents/reflector/phase-scorecard.md",
    # Phase 06 files
    "06-archive/archive-index.md": ".autoresearch/archive/archive-index.md",
}

PHASE_REQUIRED_DELIVERABLES = {
    # Legacy phase names (kept for backward compatibility)
    "01-survey": ("survey_round_log", "critic_round_log", "readiness_report", "survey_scorecard"),
    "02-pilot-analysis": (
        "problem_analysis",
        "pilot_plan",
        "pilot_results",
        "pilot_adviser_review",
        "pilot_validation_report",
        "pilot_scorecard",
    ),
    "03-full-experiments": (
        "experiment_spec",
        "run_registry",
        "results_summary",
        "checkpoint_index",
        "experiment_adviser_review",
        "evidence_package_index",
        "experiment_scorecard",
    ),
    "04-paper": (
        "paper_draft",
        "citation_audit_report",
        "reviewer_report",
        "rebuttal_log",
        "final_acceptance_report",
        "paper_scorecard",
    ),
    "05-reflection-evolution": (
        "lessons_learned",
        "overlay_draft",
        "runtime_improvement_report",
        "reflection_scorecard",
    ),
    # New semantic phase names
    "survey": ("readiness_report", "survey_scorecard"),
    "pilot": ("problem_analysis", "pilot_plan", "pilot_validation_report", "pilot_scorecard"),
    "experiments": ("experiment_spec", "results_summary", "evidence_package_index", "experiment_scorecard"),
    "paper": ("paper_draft", "citation_audit_report", "final_acceptance_report", "paper_scorecard"),
    "reflection": ("lessons_learned", "runtime_improvement_report", "reflection_scorecard"),
}

PHASE_TO_REVIEW = {
    # Legacy phase names
    "01-survey": "survey_critic",
    "02-pilot-analysis": "pilot_adviser",
    "03-full-experiments": "experiment_adviser",
    "04-paper": "paper_reviewer",
    "05-reflection-evolution": "reflection_curator",
    # New semantic phase names
    "survey": "survey_critic",
    "pilot": "pilot_adviser",
    "experiments": "experiment_adviser",
    "paper": "paper_reviewer",
    "reflection": "reflection_curator",
}

PHASE_LOOP_KEY = {
    # Legacy phase names
    "01-survey": "survey_critic",
    "02-pilot-analysis": "pilot_code_adviser",
    "03-full-experiments": "experiment_code_adviser",
    "04-paper": "writer_reviewer",
    "05-reflection-evolution": "reflector_curator",
    # New semantic phase names
    "survey": "survey_critic",
    "pilot": "pilot_code_adviser",
    "experiments": "experiment_code_adviser",
    "paper": "writer_reviewer",
    "reflection": "reflector_curator",
}

PHASE_SEQUENCE = (
    "survey",
    "pilot",
    "experiments",
    "paper",
    "reflection",
)

MARKDOWN_FIELD_RE = re.compile(r"^- ([^:\n]+):\s*(.+)$", re.MULTILINE)

STRUCTURED_SIGNAL_REQUIREMENTS = {
    "survey": {
        "survey_scorecard": {"Gate readiness": {"approve", "advance"}},
        "readiness_report": {"Recommendation": {"approve"}},
    },
    "pilot": {
        "pilot_scorecard": {"Gate readiness": {"approve", "advance"}},
        "pilot_adviser_review": {"Status": {"approved"}, "Recommendation": {"approve", "advance"}},
        "pilot_validation_report": {"Continue to full experiments": {"yes", "approved", "true"}},
    },
    "experiments": {
        "experiment_scorecard": {"Gate readiness": {"approve", "advance"}},
        "experiment_adviser_review": {
            "Status": {"approved"},
            "Recommendation": {"approve", "advance"},
            "Handoff decision": {"approve", "advance"},
        },
    },
    "paper": {
        "paper_scorecard": {"Gate readiness": {"approve", "advance"}},
        "citation_audit_report": {"Citation authenticity status": {"approved", "verified"}},
        "reviewer_report": {
            "Submission bar": {"top-tier journal/conference ready"},
            "Verdict": {"accept", "minor revision"},
        },
        "final_acceptance_report": {
            "Meets top-tier venue bar": {"yes", "approved", "true"},
            "Recommendation": {"approve"},
        },
    },
    "reflection": {
        "reflection_scorecard": {"Gate readiness": {"approve", "advance"}},
        "runtime_improvement_report": {"Recommendation": {"approve", "approved-for-consideration"}},
    },
}


def slugify(value: str) -> str:
    collapsed = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    collapsed = collapsed.strip("-")
    return collapsed or "research-project"


def yaml_dump(value: Any, indent: int = 0) -> str:
    """Dump a Python object to a YAML string using PyYAML.

    Args:
        value: Python object to serialize.
        indent: Ignored (kept for backward compatibility).

    Returns:
        YAML string representation.
    """
    return yaml.dump(value, allow_unicode=True, default_flow_style=False, sort_keys=False)


def yaml_load(text: str) -> Any:
    """Parse a YAML document string into a Python object using PyYAML.

    Supports all standard YAML features including:
    - Comments (preserved in round-trip but stripped in output)
    - Complex nested structures
    - Multi-line strings
    - All scalar types

    Args:
        text: YAML document string to parse.

    Returns:
        Parsed Python object (dict, list, or scalar).
    """
    return yaml.safe_load(text)


def read_yaml(path: Path) -> Any:
    return yaml_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: Any) -> None:
    """Write data to a YAML file with atomic write pattern.

    Uses a temporary file and atomic replace to prevent corruption
    if the process crashes mid-write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = yaml_dump(data) + "\n"

    # Atomic write: write to temp file, then replace
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp"
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        # Atomic replace on POSIX systems
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def detect_client_init_artifacts(project_root: Path) -> list[str]:
    artifacts: list[str] = []
    if not project_root.exists():
        return artifacts
    for candidate in sorted(project_root.glob("*.md")):
        if candidate.name in {"workspace-manifest.md"}:
            continue
        artifacts.append(candidate.relative_to(project_root).as_posix())
    return artifacts


def normalize_relative_path(project_root: Path, path_value: str | Path) -> str:
    path = Path(path_value)
    root = project_root.resolve()
    resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        from exceptions import PathSecurityError
        raise PathSecurityError(
            f"Path must stay inside project root: {path}",
            path=str(path),
            reason="traversal",
        ) from exc


from datetime import datetime, timezone

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
    # Determine the starting gate based on phase
    starting_gate = PHASE_TO_GATE.get(starting_phase, "gate_1")

    # Determine completion percent based on phase
    phase_completion = {
        # Legacy phase names
        "01-survey": 0,
        "02-pilot-analysis": 20,
        "03-full-experiments": 40,
        "04-paper": 60,
        "05-reflection-evolution": 80,
        # New semantic phase names
        "survey": 0,
        "pilot": 20,
        "experiments": 40,
        "paper": 60,
        "reflection": 80,
    }

    # Get current timestamp
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
        "language_policy": {
            "process_docs": process_language,
            "paper_docs": paper_language,
        },
        "inner_loops": {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        },
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
            "completion_percent": phase_completion.get(starting_phase, 0),
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
    }


def build_template_variables(project_root: Path, state: dict[str, Any]) -> dict[str, str]:
    init_paths = state["init_artifacts"]["detected_paths"]
    if init_paths:
        init_paths_section = "\n".join(f"- `{path}`" for path in init_paths)
    else:
        init_paths_section = "- No client `/init` artifact was detected; the skill bootstrap owns the initial project files."

    # Safely get deliverable path, fallback to DEFAULT_DELIVERABLES if missing
    def get_deliverable(key: str) -> str:
        deliverables = state.get("deliverables", {})
        return deliverables.get(key, DEFAULT_DELIVERABLES.get(key, f"MISSING_{key}"))

    return {
        "PROJECT_ID": state["project_id"],
        "TOPIC": state["topic"],
        "PROJECT_ROOT": str(project_root),
        "CLIENT_PROFILE": state.get("client_profile", "codex"),
        "CLIENT_INSTRUCTION_FILE": state.get("client_instruction_file", "AGENTS.md"),
        "PROCESS_LANGUAGE": state.get("language_policy", {}).get("process_docs", "zh-CN"),
        "PAPER_LANGUAGE": state.get("language_policy", {}).get("paper_docs", "en-US"),
        "INIT_SOURCE": state["init_artifacts"]["source"],
        "INIT_PATHS_SECTION": init_paths_section,
        "CURRENT_PHASE": state.get("current_phase", "01-survey"),
        "CURRENT_GATE": state.get("current_gate", "gate_1"),
        "PROJECT_CONFIG_PATH": get_deliverable("project_config"),
        "IDEA_BRIEF_PATH": get_deliverable("idea_brief"),
        "REFERENCE_LIBRARY_INDEX_PATH": get_deliverable("reference_library_index"),
        "DASHBOARD_STATUS_PATH": get_deliverable("dashboard_status"),
        "DASHBOARD_PROGRESS_PATH": get_deliverable("dashboard_progress"),
        "JOB_REGISTRY_PATH": get_deliverable("job_registry"),
        "GPU_REGISTRY_PATH": get_deliverable("gpu_registry"),
        "BACKEND_REGISTRY_PATH": get_deliverable("backend_registry"),
        "GATE_1_REPORT_PATH": get_deliverable("readiness_report"),
        "GATE_2_REPORT_PATH": get_deliverable("pilot_validation_report"),
        "GATE_3_REPORT_PATH": get_deliverable("evidence_package_index"),
        "GATE_4_REPORT_PATH": get_deliverable("final_acceptance_report"),
        "GATE_5_REPORT_PATH": get_deliverable("runtime_improvement_report"),
        "CITATION_AUDIT_REPORT_PATH": get_deliverable("citation_audit_report"),
    }


def build_list_section(items: list[str], empty_message: str) -> str:
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def render_template_string(template_text: str, variables: dict[str, str]) -> str:
    rendered = template_text
    for key, value in variables.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def write_text_if_needed(path: Path, text: str, overwrite: bool = False) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def render_template_tree(
    template_root: Path,
    project_root: Path,
    variables: dict[str, str],
    overwrite: bool = False,
) -> list[Path]:
    created: list[Path] = []
    for template_path in sorted(template_root.rglob("*.tmpl")):
        relative_path = template_path.relative_to(template_root)
        destination = project_root / str(relative_path)[:-5]
        content = render_template_string(template_path.read_text(encoding="utf-8"), variables)
        if write_text_if_needed(destination, content, overwrite=overwrite):
            created.append(destination)
    return created


def detect_client_profile(project_root: Path, init_paths: list[str], client_type: str) -> str:
    if client_type in {"codex", "claude"}:
        return client_type

    candidates = [Path(path).name for path in init_paths]
    if (project_root / "CLAUDE.md").exists() or "CLAUDE.md" in candidates:
        return "claude"
    if (project_root / "AGENTS.md").exists() or "AGENTS.md" in candidates:
        return "codex"
    return "codex"


def build_client_instruction_text(client_profile: str, state: dict[str, Any]) -> str:
    filename = "CLAUDE.md" if client_profile == "claude" else "AGENTS.md"
    return "\n".join(
        [
            f"# {filename}",
            "",
            "This workspace is initialized by the ai-research-orchestrator skill.",
            "",
            "## Core contracts",
            "",
            f"- Machine-readable state: `{DEFAULT_DELIVERABLES['research_state']}`",
            f"- Human-readable manifest: `{DEFAULT_DELIVERABLES['workspace_manifest']}`",
            f"- User IDEA template: `{DEFAULT_DELIVERABLES['idea_brief']}`",
            f"- User reference library: `{DEFAULT_DELIVERABLES['reference_library_index']}`",
            f"- Dashboard status: `{DEFAULT_DELIVERABLES['dashboard_progress']}`",
            "",
            "## Required phases",
            "",
            "- Phase 1: Survey <-> Critic",
            "- Phase 2: Pilot Code <-> Pilot Adviser",
            "- Phase 3: Experiment Code <-> Experiment Adviser",
            "- Phase 4: Paper Writer <-> Reviewer & Editor",
            "- Phase 5: Reflector <-> Curator",
            "",
            "## Required gates",
            "",
            "- Gate 1: research-readiness report approved by the user",
            "- Gate 2: pilot validation pack approved by the user",
            "- Gate 3: experiment evidence package approved by the user",
            "- Gate 4: paper package approved by the user",
            "- Gate 5: reflection/evolution package approved by the user before overlays or policy changes apply",
            "",
            "## Runtime rules",
            "",
            "- Keep every phase as a two-agent loop under the user-facing orchestrator.",
            "- Update dashboard and runtime registries as phase status changes.",
            "- Do not bypass `research-state.yaml`.",
            "- Do not pivot without explicit human approval.",
            "- Do not claim plagiarism clearance, AI-detection clearance, or formal proof verification in v1.",
            "",
            "## Language policy",
            "",
            f"- Process documents: `{state['language_policy']['process_docs']}`",
            f"- Paper-facing documents: `{state['language_policy']['paper_docs']}`",
            "",
        ]
    )


def resolve_deliverable_path(project_root: Path, state: dict[str, Any], key: str) -> Path:
    relative_value = state["deliverables"][key]
    return (project_root / relative_value).resolve()


def validate_deliverable_location(project_root: Path, relative_path: str, key: str) -> list[str]:
    errors: list[str] = []
    relative = Path(relative_path)
    expected_prefix = EXPECTED_DELIVERABLE_PREFIXES[key]
    if relative.is_absolute():
        errors.append(f"{key} must be project-relative, got absolute path: {relative_path}")
        return errors
    if ".." in relative.parts:
        errors.append(f"{key} must stay inside the project root, got: {relative_path}")
        return errors
    normalized = relative.as_posix()
    if not normalized.startswith(expected_prefix):
        errors.append(f"{key} must live under {expected_prefix}, got: {relative_path}")
    return errors


def ensure_complete_deliverables(state: dict[str, Any]) -> dict[str, Any]:
    """Ensure all required deliverables exist in the state.

    This function adds any missing deliverables from DEFAULT_DELIVERABLES
    to the state, ensuring backward compatibility with older project states.

    Args:
        state: The current state dictionary.

    Returns:
        The state with complete deliverables.
    """
    if "deliverables" not in state:
        state["deliverables"] = {}

    # Add any missing deliverables from defaults
    for key, default_path in DEFAULT_DELIVERABLES.items():
        if key not in state["deliverables"]:
            state["deliverables"][key] = default_path
            logger.info(f"Added missing deliverable: {key} = {default_path}")

    return state


def load_state(project_root: Path) -> dict[str, Any]:
    state = read_yaml(project_root / DEFAULT_DELIVERABLES["research_state"])
    config = load_project_config(project_root)
    state["loop_limits"] = dict(config["loop_limits"])
    state["language_policy"] = dict(config["languages"])
    # Ensure all deliverables exist (backward compatibility)
    state = ensure_complete_deliverables(state)
    return state


def save_state(project_root: Path, state: dict[str, Any]) -> None:
    write_yaml(project_root / DEFAULT_DELIVERABLES["research_state"], state)


def load_project_config(project_root: Path) -> dict[str, Any]:
    path = project_root / DEFAULT_DELIVERABLES["project_config"]
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    config = read_yaml(path)
    merged = json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    for key, value in config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def append_state_log(state: dict[str, Any], key: str, entry: dict[str, Any] | str) -> None:
    items = list(state.get(key, []))
    if isinstance(entry, str):
        items.append(entry)
    else:
        items.append(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    state[key] = items


def load_json(path: Path, default: Any) -> Any:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write data to a JSON file with atomic write pattern.

    Uses a temporary file and atomic replace to prevent corruption
    if the process crashes mid-write.

    Args:
        path: Target file path.
        payload: Python object to serialize as JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    # Atomic write: write to temp file, then replace
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp"
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        # Atomic replace on POSIX systems
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


# ============================================================================
# ARIS Integration: Review State Management
# ============================================================================

def build_review_state(
    phase: str,
    round_num: int = 1,
    thread_id: str | None = None,
    status: str = "in_progress",
    last_score: float = 0.0,
    last_verdict: str = "not_started",
    pending_experiments: list[str] | None = None,
) -> dict[str, Any]:
    """Build a new REVIEW_STATE structure for ARIS auto-review-loop.

    Args:
        phase: Current phase name (e.g., "02-pilot-analysis").
        round_num: Current round number (1-based).
        thread_id: Codex MCP conversation thread ID for context continuity.
        status: Loop status ("in_progress", "completed", "stale").
        last_score: Last review score (1-10).
        last_verdict: Last verdict ("ready", "almost", "not_ready").
        pending_experiments: List of experiment IDs still running.

    Returns:
        REVIEW_STATE dictionary.
    """
    return {
        "phase": phase,
        "round": round_num,
        "max_rounds": MAX_REVIEW_ROUNDS,
        "threadId": thread_id,
        "status": status,
        "last_score": last_score,
        "last_verdict": last_verdict,
        "pending_experiments": pending_experiments or [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_review_state(project_root: Path, review_state: dict[str, Any]) -> None:
    """Save REVIEW_STATE.json to project root.

    This file persists loop state across context compaction,
    allowing long-running auto-review-loops to resume.

    Args:
        project_root: Project root directory.
        review_state: Review state dictionary.
    """
    # Update timestamp on every save
    review_state["timestamp"] = datetime.now(timezone.utc).isoformat()
    path = project_root / REVIEW_STATE_FILENAME
    write_json(path, review_state)
    logger.info(f"Saved review state: round {review_state['round']}, status {review_state['status']}")


def load_review_state(project_root: Path) -> dict[str, Any] | None:
    """Load REVIEW_STATE.json from project root.

    Args:
        project_root: Project root directory.

    Returns:
        Review state dictionary if file exists and is valid, None otherwise.
    """
    path = project_root / REVIEW_STATE_FILENAME
    if not path.exists():
        return None

    try:
        state = load_json(path, None)
        if state is None:
            return None

        # Check for stale state (older than 24 hours with in_progress status)
        if state.get("status") == "in_progress":
            timestamp_str = state.get("timestamp", "")
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    age_hours = (datetime.now(timezone.utc) - timestamp).total_seconds() / 3600
                    if age_hours > 24:
                        logger.warning(f"Review state is stale ({age_hours:.1f} hours old), starting fresh")
                        return None
                except Exception as e:
                    logger.warning(f"Failed to parse timestamp: {e}")

        return state
    except Exception as e:
        logger.warning(f"Failed to load review state: {e}")
        return None


def clear_review_state(project_root: Path) -> None:
    """Remove REVIEW_STATE.json (call on completion).

    Args:
        project_root: Project root directory.
    """
    path = project_root / REVIEW_STATE_FILENAME
    if path.exists():
        path.unlink()
        logger.info("Cleared review state file")


def is_positive_assessment(score: float, verdict: str) -> bool:
    """Check if review result meets positive assessment threshold.

    Args:
        score: Review score (1-10).
        verdict: Review verdict string.

    Returns:
        True if assessment is positive (loop can stop).
    """
    if score >= POSITIVE_SCORE_THRESHOLD:
        verdict_lower = verdict.lower()
        if any(kw in verdict_lower for kw in POSITIVE_VERDICT_KEYWORDS):
            return True
    return False


def get_reviewer_config(project_root: Path) -> dict[str, Any]:
    """Get reviewer configuration from project config.

    Args:
        project_root: Project root directory.

    Returns:
        Reviewer configuration dictionary.
    """
    config = load_project_config(project_root)
    return config.get("reviewer", DEFAULT_REVIEWER_CONFIG)


def is_cross_model_review_enabled(project_root: Path) -> bool:
    """Check if cross-model review via Codex MCP is enabled.

    Args:
        project_root: Project root directory.

    Returns:
        True if cross-model review is enabled.
    """
    reviewer_config = get_reviewer_config(project_root)
    return reviewer_config.get("enabled", False)


# ============================================================================
# ARIS Integration: Idea State Management
# ============================================================================

def build_idea_state(
    direction: str,
    phase: str = "literature-survey",
    ideas_generated: int = 0,
    ideas_filtered: int = 0,
    pilots_run: int = 0,
    pilots_positive: int = 0,
    top_idea_id: str | None = None,
) -> dict[str, Any]:
    """Build a new IDEA_STATE structure for idea-discovery pipeline.

    Args:
        direction: Research direction string.
        phase: Current phase (literature-survey, idea-generation, novelty-check, pilot, review).
        ideas_generated: Total ideas generated.
        ideas_filtered: Ideas that passed filtering.
        pilots_run: Number of pilot experiments run.
        pilots_positive: Pilots with positive signal.
        top_idea_id: ID of the top-ranked idea.

    Returns:
        IDEA_STATE dictionary.
    """
    return {
        "direction": direction,
        "phase": phase,
        "ideas_generated": ideas_generated,
        "ideas_filtered": ideas_filtered,
        "pilots_run": pilots_run,
        "pilots_positive": pilots_positive,
        "top_idea_id": top_idea_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_idea_state(project_root: Path, idea_state: dict[str, Any]) -> None:
    """Save IDEA_STATE.json to project root.

    Args:
        project_root: Project root directory.
        idea_state: Idea state dictionary.
    """
    idea_state["timestamp"] = datetime.now(timezone.utc).isoformat()
    path = project_root / IDEA_STATE_FILENAME
    write_json(path, idea_state)
    logger.info(f"Saved idea state: phase {idea_state['phase']}, ideas {idea_state['ideas_generated']}")


def load_idea_state(project_root: Path) -> dict[str, Any] | None:
    """Load IDEA_STATE.json from project root.

    Args:
        project_root: Project root directory.

    Returns:
        Idea state dictionary if file exists and is valid, None otherwise.
    """
    path = project_root / IDEA_STATE_FILENAME
    if not path.exists():
        return None

    try:
        state = load_json(path, None)
        if state is None:
            return None

        # Check for stale state (older than 7 days)
        timestamp_str = state.get("timestamp", "")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                age_days = (datetime.now(timezone.utc) - timestamp).total_seconds() / 86400
                if age_days > 7:
                    logger.warning(f"Idea state is stale ({age_days:.1f} days old), starting fresh")
                    return None
            except Exception as e:
                logger.warning(f"Failed to parse timestamp: {e}")

        return state
    except Exception as e:
        logger.warning(f"Failed to load idea state: {e}")
        return None


def clear_idea_state(project_root: Path) -> None:
    """Remove IDEA_STATE.json (call on completion).

    Args:
        project_root: Project root directory.
    """
    path = project_root / IDEA_STATE_FILENAME
    if path.exists():
        path.unlink()
        logger.info("Cleared idea state file")


def load_aris_config(project_root: Path) -> dict[str, Any]:
    """Load ARIS configuration from project config.

    Args:
        project_root: Project root directory.

    Returns:
        ARIS configuration dictionary.
    """
    config = load_project_config(project_root)
    return config.get("aris", DEFAULT_ARIS_CONFIG)


def is_auto_proceed(project_root: Path) -> bool:
    """Check if auto-proceed mode is enabled.

    Args:
        project_root: Project root directory.

    Returns:
        True if auto-proceed is enabled.
    """
    aris_config = load_aris_config(project_root)
    return aris_config.get("auto_proceed", False)


def is_unmodified_template(project_root: Path, state: dict[str, Any], relative_path: str) -> bool:
    target_path = project_root / relative_path
    if not target_path.exists():
        return False
    template_path = TEMPLATE_ROOT / f"{relative_path}.tmpl"
    if not template_path.exists():
        return False
    variables = build_template_variables(project_root, state)
    expected = render_template_string(template_path.read_text(encoding="utf-8"), variables).strip()
    actual = target_path.read_text(encoding="utf-8").strip()
    return actual == expected


def validate_deliverable_content(project_root: Path, state: dict[str, Any], key: str) -> list[str]:
    relative_path = state["deliverables"][key]
    if is_unmodified_template(project_root, state, relative_path):
        return [f"{relative_path} is still the unedited template and does not satisfy the gate."]
    if not (project_root / relative_path).read_text(encoding="utf-8").strip():
        return [f"{relative_path} is empty and does not satisfy the gate."]
    return []


def parse_markdown_fields(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key, value in MARKDOWN_FIELD_RE.findall(text):
        fields[key.strip()] = value.strip().strip("`")
    return fields


def validate_structured_signals(project_root: Path, state: dict[str, Any], phase_name: str) -> list[str]:
    errors: list[str] = []
    requirements = STRUCTURED_SIGNAL_REQUIREMENTS.get(phase_name, {})
    for deliverable_key, field_requirements in requirements.items():
        relative_path = state["deliverables"][deliverable_key]
        candidate = project_root / relative_path
        if not candidate.exists():
            errors.append(f"{relative_path} is missing; cannot read structured gate signals.")
            continue
        fields = parse_markdown_fields(candidate)
        for field_name, expected_values in field_requirements.items():
            actual = fields.get(field_name)
            normalized = normalize_signal_value(actual)
            if normalized not in expected_values:
                errors.append(
                    f"{relative_path} must set '{field_name}' to one of {sorted(expected_values)}, got {actual!r}."
                )
    return errors


def normalize_signal_value(value: str | None) -> str:
    if value is None:
        return ""
    normalized = value.strip().strip("`").lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def allowed_return_phases(phase_name: str) -> list[str]:
    if phase_name not in PHASE_SEQUENCE:
        return []
    index = PHASE_SEQUENCE.index(phase_name)
    return list(PHASE_SEQUENCE[: index + 1])


def reset_state_for_phase(state: dict[str, Any], phase_name: str) -> None:
    if phase_name not in PHASE_SEQUENCE:
        from exceptions import PhaseTransitionError
        raise PhaseTransitionError(
            f"Unsupported phase: {phase_name}",
            to_phase=phase_name,
            reason="invalid_phase",
        )
    index = PHASE_SEQUENCE.index(phase_name)
    for candidate in PHASE_SEQUENCE[index:]:
        gate = PHASE_TO_GATE[candidate]
        review = PHASE_TO_REVIEW[candidate]
        state["approval_status"][gate] = "pending"
        state["phase_reviews"][review] = "pending"
    state["current_phase"] = phase_name
    state["phase"] = phase_name
    state["current_gate"] = PHASE_TO_GATE[phase_name]
    state["subphase"] = "entry"
    state["progress"]["allowed_return_phases"] = allowed_return_phases(phase_name)
    state["progress"]["suggested_return_phase"] = phase_name


def suggest_return_phase(phase_name: str, blockers: list[str]) -> str:
    if "deliverables_still_template" in blockers or "phase_review_pending" in blockers:
        return phase_name
    options = allowed_return_phases(phase_name)
    if len(options) >= 2:
        return options[-2]
    return phase_name


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    """Configure logging for the orchestrator.

    Args:
        level: Logging level (default: INFO).
        log_file: Optional file path to write logs.
    """
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


def ensure_project_structure(project_root: Path, create_if_missing: bool = True) -> bool:
    """
    Ensure project directory structure is valid.

    This function checks and optionally creates the required directory structure.
    Every script should call this at startup to guarantee consistent structure.

    Args:
        project_root: Path to the project root directory
        create_if_missing: If True, create missing directories automatically

    Returns:
        True if structure is valid (all directories exist)
        False if structure is invalid and create_if_missing is False
    """
    # Resolve and validate project_root path
    project_root = project_root.resolve()
    if not project_root.exists():
        if create_if_missing:
            project_root.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project root: {project_root}")
        else:
            logger.error(f"Project root does not exist: {project_root}")
            return False

    # Track missing directories
    missing_dirs: list[str] = []

    for dir_path in REQUIRED_DIRECTORIES:
        full_path = project_root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)

    # Create missing directories if requested
    if missing_dirs:
        if create_if_missing:
            for dir_path in missing_dirs:
                full_path = project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
        else:
            logger.warning(f"Missing directories: {missing_dirs}")
            return False

    # Check if state file exists (log info if not, but don't fail)
    state_file = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_file.exists():
        logger.info(f"State file not found (expected): {state_file}")

    return True
