# Changelog

All notable changes to the AI Research Orchestrator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.20.0] - 2026-03-22

### Added

- `/abandon` command for graceful project exit at any phase with deliverable archival
- `available_commands` field in `/status` output — ranked list of actions based on current state
- Abandon option in escalation choices to prevent all-pivots-rejected deadlock

### Changed

- Strengthened auto-transition safety guard: requires explicit gate approval before advancing

## [1.19.0] - 2026-03-22

### Added

- `agents/orchestrator/AGENT.md` — orchestrator agent definition (referenced by 9 skills)
- Agent shutdown protocol (SendMessage + TeamDelete) in all 5 phase commands
- Project closure validation (reflection-closeout) step in `/reflect` command
- Shared `read_hook_input()` and `get_project_root()` in `hooks/__init__.py`

### Fixed

- Pivot execution now archives deliverables before changing phase direction
- Session reload hook outputs error context instead of failing silently

### Removed

- Dead code: `normalize_signal_value()` from state/validator.py
- Empty stub modules: `scripts/templates/` and `scripts/platform/`

## [1.18.0] - 2026-03-22

### Added

- `/pivot` command for explicit research direction management (propose, review, execute)
- `settings.schema.json` for user-configurable plugin settings via environment variables
- `CONTRIBUTING.md` with skill template and contribution guidelines
- GitHub issue templates (bug report, feature request) and PR template
- Actionable escalation options when `escalate_to_user` is triggered (revise/rollback/pivot/force-advance)
- Environment variable fallbacks (`AUTORESEARCH_*`) for init script defaults
- Exported `RESEARCH_TYPE_PHASE_SEQUENCE` and `get_phase_sequence_for_research_type` from constants

### Removed

- 21 duplicate templates from `assets/templates/docs/reports/` (superseded by `docs/` templates)
- Unused exception classes: `ValidationError`, `CommandExecutionError`, `TemplateError`, `DependencyError`
- Deprecated `.bak` test backup files

### Fixed

- Consolidated duplicate `DEFAULT_LANGUAGE_POLICY` constant (was in both `state/builder.py` and `project/client.py`)
- Description mismatch between `plugin.json` and `marketplace.json`
- Applied consistent `black`/`isort` formatting across codebase

## [1.17.0] - 2026-03-22

### Fixed

- State migration consistency, gate race condition, schema validation
- Pivot validation, GPU error handling, version sync, env var config support

## [1.16.0] - 2026-03-22

### Added

- System evaluation grader for Reflection phase (6-dimension scoring)
- Global registry for cross-project trend tracking
- Curator audit workflow for system evaluation reports

## [1.12.0] - 2026-03-14

### Added

- **ARIS Integration**: Full integration of Auto-Research-In-Sleep capabilities
- Skills for autonomous research workflows (consolidated to 21 skills in v1.18.0)
  - Three main workflows: idea-discovery, auto-review-loop, paper-pipeline
  - Cross-model review via Codex MCP (optional)

- **New Skills**:
  - Workflow 1: `idea-discovery`, `research-lit`, `idea-creator`, `novelty-check`, `research-review`
  - Workflow 2: `auto-review-loop`, `run-experiment`, `monitor-experiment`, `analyze-results`
  - Workflow 3: `paper-pipeline`, `paper-plan`, `paper-figure`, `paper-write`, `paper-compile`, `auto-paper-improvement-loop`
  - Utilities: `research-pipeline`, `feishu-notify`

- **Configuration Extensions**:
  - `aris.auto_proceed`: Toggle between human gates and full autonomy
  - `aris.reviewer`: Cross-model review settings
  - `aris.max_review_rounds`: Loop control (default: 4)
  - GPU protection: `pilot_max_hours`, `max_total_gpu_hours`

- **State Management**:
  - `IDEA_STATE.json`: Idea discovery pipeline persistence
  - `REVIEW_STATE.json`: Auto-review-loop persistence (already existed)
  - Cross-context survival for long-running workflows

- **Codex MCP Detection**:
  - Auto-detect Codex MCP availability on project init
  - Setup suggestions when not configured

### Changed

- `orchestrator-config.yaml` template now includes ARIS section
- `init_research_project.py` checks for Codex MCP and suggests setup

### Migration

No breaking changes. All existing functionality preserved.

To enable new ARIS features:
1. Add `aris:` section to existing `orchestrator-config.yaml` (see template)
2. Configure Codex MCP for cross-model review (optional)
3. Invoke new skills: `/idea-discovery`, `/auto-review-loop`, `/paper-pipeline`, `/research-pipeline`

## [1.0.0] - 2024-01-XX

### Added
- Initial release of AI Research Orchestrator
- Five-phase research workflow (Survey, Pilot, Experiments, Paper, Reflection)
- Quality gate system with scored evaluations
- State machine with `research-state.yaml` as single source of truth
- Template system for workspace documents
- Agent prompt rendering with role templates
- Runtime dashboard generation
- Job scheduling with GPU allocation
- Citation audit integration with latex-citation-curator
- Pivot management and approval workflow
- Sentinel and recovery mechanisms
- Overlay activation for self-evolution

### Security
- Removed `shell=True` from subprocess calls to prevent command injection
- Added path traversal validation for working directories
- Replaced hardcoded paths with environment variable configuration
- Added timeout controls for external command execution

### Documentation
- Comprehensive README with quick start guide
- SKILL.md for skill activation and usage
- Reference documentation in `references/` directory
- Code architecture documentation in CLAUDE.md