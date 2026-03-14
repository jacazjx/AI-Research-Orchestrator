# Changelog

All notable changes to the AI Research Orchestrator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.12.0] - 2026-03-14

### Added

- **ARIS Integration**: Full integration of Auto-Research-In-Sleep capabilities
  - 17 new skills for autonomous research workflows
  - Three main workflows: idea-discovery, auto-review-loop, paper-writing
  - Cross-model review via Codex MCP (optional)

- **New Skills**:
  - Workflow 1: `idea-discovery`, `research-lit`, `idea-creator`, `novelty-check`, `research-review`
  - Workflow 2: `auto-review-loop`, `run-experiment`, `monitor-experiment`, `analyze-results`
  - Workflow 3: `paper-writing`, `paper-plan`, `paper-figure`, `paper-write`, `paper-compile`, `auto-paper-improvement-loop`
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
3. Invoke new skills: `/idea-discovery`, `/auto-review-loop`, `/paper-writing`, `/research-pipeline`

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