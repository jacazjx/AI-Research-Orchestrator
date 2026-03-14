# Folder Restructure Design

> **For agentic workers:** This is a design specification. Use superpowers:writing-plans to create implementation plan.

**Goal:** Restructure project folders to remove numbered naming, create per-agent directories, and establish clear main work directories.

**Date:** 2026-03-14

---

## Overview

The current folder structure uses numbered phase directories (01-survey, 02-pilot-analysis, etc.) which mixes agent outputs with phase artifacts. This design proposes a cleaner separation:

- Main work directories for user-facing outputs: `paper/`, `code/`, `docs/`
- Agent-specific directories for agent intermediate work: `agents/<role>/`
- System management in hidden directory: `.autoresearch/`

## Current Structure

```
project/
├── 00-admin/           # Admin and config
├── 01-survey/          # Survey phase outputs
├── 02-pilot-analysis/  # Pilot phase outputs
├── 03-full-experiments/# Experiment phase outputs
├── 04-paper/           # Paper phase outputs
├── 05-reflection-evolution/
└── 06-archive/         # Archive
```

## New Structure

```
project/
├── paper/                    # Main: Paper outputs
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── references.bib
│
├── code/                     # Main: Code repository
│   ├── src/
│   ├── experiments/
│   ├── configs/
│   └── checkpoints/
│
├── docs/                     # Main: Documents and reports
│   ├── reports/
│   └── figures/
│
├── agents/                   # Agent workspaces
│   ├── survey/
│   ├── critic/
│   ├── coder/
│   ├── adviser/
│   ├── writer/
│   ├── reviewer/
│   ├── reflector/
│   └── curator/
│
└── .autoresearch/            # System management (hidden)
    ├── state/
    ├── config/
    ├── dashboard/
    ├── runtime/
    ├── reference-papers/
    ├── templates/
    └── archive/
```

## Directory Mapping

### From Old to New

| Old Path | New Path |
|----------|----------|
| `00-admin/research-state.yaml` | `.autoresearch/state/research-state.yaml` |
| `00-admin/orchestrator-config.yaml` | `.autoresearch/config/orchestrator-config.yaml` |
| `00-admin/dashboard/*` | `.autoresearch/dashboard/*` |
| `00-admin/runtime/*` | `.autoresearch/runtime/*` |
| `00-admin/reference-papers/` | `.autoresearch/reference-papers/` |
| `00-admin/idea-brief.md` | `.autoresearch/idea-brief.md` |
| `00-admin/workspace-manifest.md` | `.autoresearch/workspace-manifest.md` |
| `01-survey/*` | `agents/survey/` + `docs/reports/survey/` |
| `02-pilot-analysis/*` | `agents/coder/` + `docs/reports/pilot/` |
| `03-full-experiments/*` | `code/` + `agents/coder/` + `docs/reports/experiments/` |
| `04-paper/*` | `paper/` + `agents/writer/` + `agents/reviewer/` |
| `05-reflection-evolution/*` | `agents/reflector/` + `docs/reports/reflection/` |
| `06-archive/` | `.autoresearch/archive/` |

### Agent Directory Contents

Each agent directory contains:
- `notes.md` - Agent's working notes
- `history/` - Historical records (optional)
- `outputs/` - Agent-specific outputs (optional)

### Main Work Directories

**`paper/`** - Paper production workspace:
- LaTeX source files
- Figures for paper
- Bibliography files
- PDF output

**`code/`** - Code repository:
- Source code
- Experiment scripts
- Configuration files
- Model checkpoints

**`docs/`** - Documentation:
- Phase reports
- Evidence packages
- Analysis summaries

### System Directory (`.autoresearch/`)

| Subdirectory | Contents |
|--------------|----------|
| `state/` | `research-state.yaml`, `REVIEW_STATE.json`, `IDEA_STATE.json` |
| `config/` | `orchestrator-config.yaml` |
| `dashboard/` | `status.json`, `progress.md`, `timeline.ndjson` |
| `runtime/` | `job-registry.yaml`, `gpu-registry.yaml`, `sentinel-events.ndjson` |
| `reference-papers/` | Reference paper storage |
| `templates/` | Rendered template cache |
| `archive/` | Archived items from all phases |

## Agent Role Mapping

| Agent | Primary Workspace | Output Location |
|-------|-------------------|-----------------|
| Survey | `agents/survey/` | `docs/reports/survey/` |
| Critic | `agents/critic/` | `agents/critic/reviews/` |
| Code | `code/` | `code/` |
| Adviser | `agents/adviser/` | `agents/adviser/advice/` |
| Paper Writer | `agents/writer/` | `paper/` |
| Reviewer | `agents/reviewer/` | `agents/reviewer/reviews/` |
| Reflector | `agents/reflector/` | `docs/reports/reflection/` |
| Curator | `agents/curator/` | `.autoresearch/archive/` |

## Initialization Check

Every script must call `ensure_project_structure()` at startup:

```python
def ensure_project_structure(project_root: Path) -> bool:
    """
    Ensure project directory structure is valid.

    1. Check required directories exist
    2. Auto-create missing directories
    3. Verify state file is valid
    4. Return True if valid, False if needs initialization
    """
```

Required directories:
- `paper/`, `code/`, `docs/`
- `agents/survey/`, `agents/critic/`, `agents/coder/`, `agents/adviser/`
- `agents/writer/`, `agents/reviewer/`, `agents/reflector/`, `agents/curator/`
- `.autoresearch/state/`, `.autoresearch/config/`, `.autoresearch/dashboard/`
- `.autoresearch/runtime/`, `.autoresearch/reference-papers/`, `.autoresearch/archive/`

## Constants Update

### PHASE_DIRECTORIES → PROJECT_DIRECTORIES

```python
# Main work directories
MAIN_DIRECTORIES = ("paper", "code", "docs")

# Agent directories
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

# System directories (hidden)
SYSTEM_DIRECTORIES = (
    ".autoresearch/state",
    ".autoresearch/config",
    ".autoresearch/dashboard",
    ".autoresearch/runtime",
    ".autoresearch/reference-papers",
    ".autoresearch/templates",
    ".autoresearch/archive",
)

# All required directories
REQUIRED_DIRECTORIES = MAIN_DIRECTORIES + AGENT_DIRECTORIES + SYSTEM_DIRECTORIES
```

### DEFAULT_DELIVERABLES Update

All paths need to be updated to new locations:

```python
DEFAULT_DELIVERABLES = {
    # State files
    "research_state": ".autoresearch/state/research-state.yaml",
    "review_state": ".autoresearch/state/REVIEW_STATE.json",
    "idea_state": ".autoresearch/state/IDEA_STATE.json",

    # Config
    "project_config": ".autoresearch/config/orchestrator-config.yaml",

    # Dashboard
    "dashboard_status": ".autoresearch/dashboard/status.json",
    "dashboard_progress": ".autoresearch/dashboard/progress.md",
    "dashboard_timeline": ".autoresearch/dashboard/timeline.ndjson",

    # Runtime
    "job_registry": ".autoresearch/runtime/job-registry.yaml",
    "gpu_registry": ".autoresearch/runtime/gpu-registry.yaml",
    "sentinel_events": ".autoresearch/runtime/sentinel-events.ndjson",

    # Reference papers
    "reference_library_index": ".autoresearch/reference-papers/README.md",

    # Idea brief
    "idea_brief": ".autoresearch/idea-brief.md",
    "workspace_manifest": ".autoresearch/workspace-manifest.md",

    # Survey outputs
    "survey_notes": "agents/survey/notes.md",
    "readiness_report": "docs/reports/survey/research-readiness-report.md",
    "survey_scorecard": "docs/reports/survey/phase-scorecard.md",

    # Pilot outputs
    "problem_analysis": "docs/reports/pilot/problem-analysis.md",
    "pilot_validation_report": "docs/reports/pilot/pilot-validation-report.md",
    "pilot_scorecard": "docs/reports/pilot/phase-scorecard.md",

    # Experiment outputs
    "experiment_spec": "code/configs/experiment-spec.yaml",
    "results_summary": "docs/reports/experiments/results-summary.md",
    "evidence_package_index": "docs/reports/experiments/evidence-package-index.md",
    "experiment_scorecard": "docs/reports/experiments/phase-scorecard.md",

    # Paper outputs
    "paper_draft": "paper/main.tex",
    "citation_audit_report": "paper/citation-audit-report.md",
    "reviewer_report": "agents/reviewer/reviews/reviewer-report.md",
    "final_acceptance_report": "docs/reports/paper/final-acceptance-report.md",
    "paper_scorecard": "docs/reports/paper/phase-scorecard.md",

    # Reflection outputs
    "lessons_learned": "docs/reports/reflection/lessons-learned.md",
    "runtime_improvement_report": "docs/reports/reflection/runtime-improvement-report.md",
    "reflection_scorecard": "docs/reports/reflection/phase-scorecard.md",

    # Archive
    "archive_index": ".autoresearch/archive/archive-index.md",
}
```

## Migration Path

For existing projects:

1. `migrate_project.py --restructure` - Convert old structure to new
2. Backup old directories before migration
3. Update all path references in state files
4. Verify migration with `verify_system.py`

## Benefits

1. **Semantic clarity**: No more numbered directories
2. **Clear ownership**: Each agent has its own workspace
3. **User-friendly**: Main work directories (`paper/`, `code/`, `docs/`) are prominent
4. **Clean separation**: System files hidden in `.autoresearch/`
5. **Better organization**: Related files grouped by purpose, not phase

## Backward Compatibility

- Migration script provided for existing projects
- State file version bumped to 2.0.0
- Old paths are recognized during migration only