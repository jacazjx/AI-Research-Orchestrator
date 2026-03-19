"""Path-related constants for the Research Orchestrator."""

from pathlib import Path

# Base directories (computed at import time)
SCRIPT_DIR = Path(__file__).resolve().parent.parent
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

AGENT_WORKSPACE_SUBDIRS = (
    "workspace",
    "battle",
    "output",
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

# Expected deliverable prefixes for validation
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
    "problem_validation_report": "docs/",
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
    "03-full-experiments/experiment-adviser-review.md": (
        "agents/adviser/experiment-adviser-review.md"
    ),
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
    "05-reflection-evolution/runtime-improvement-report.md": (
        ".autoresearch/archive/runtime-improvement-report.md"
    ),
    "05-reflection-evolution/phase-scorecard.md": "agents/reflector/phase-scorecard.md",
    # Phase 06 files
    "06-archive/archive-index.md": ".autoresearch/archive/archive-index.md",
}
