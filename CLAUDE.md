# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Research Orchestrator is a Claude Code skill that turns a research IDEA into a controlled five-phase project with scored gate checks, visible progress artifacts, and explicit human approval between phases. Optimized for AI/ML algorithm research requiring literature review, pilot validation, experiments, paper writing, and reflection.

## Development Commands

```bash
# On Debian/Ubuntu, create a venv first (pip install is blocked system-wide):
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run all tests
python -m pytest tests/ -v --tb=short

# Run specific test
python -m pytest tests/test_init_research_project.py -v

# Run with coverage
python -m pytest tests/ -v --cov=scripts --cov-report=term-missing

# Format code
black scripts/ tests/ && isort scripts/ tests/

# Lint (CI checks)
black --check scripts/ tests/
isort --check-only --diff scripts/ tests/
flake8 scripts/ tests/ --max-line-length=100 --extend-ignore=E203,W503
mypy scripts/ --ignore-missing-imports

# Pre-commit
pre-commit run --all-files
```

## User-Facing Commands

| Command | Phase | Trigger Phrases |
|---------|-------|-----------------|
| `/init-research` | Init | "init research", "初始化研究" |
| `/reload` | Any | "reload", "重新加载", "恢复状态" |
| `/configure` | Any | "configure", "配置", "设置参数" |
| `/insight` | Init | "insight", "澄清意图", "明确想法" |
| `/run-survey` | Survey | "run survey", "文献调研" |
| `/run-pilot` | Pilot | "run pilot", "Pilot验证" |
| `/run-experiments` | Experiments | "run experiments", "完整实验" |
| `/write-paper` | Paper | "write paper", "写论文" |
| `/reflect` | Reflection | "reflect", "反思总结" |
| `/status` | Any | "status", "查看状态", "项目状态" |

Commands are defined in `commands/<name>/COMMAND.md`. Trigger flow: User Input → COMMAND.md → SKILL.md → Script execution.

## Key Scripts

```bash
# Initialize project (non-interactive)
python3 scripts/init_research_project.py --project-root /abs/path --topic "Idea" --client-type auto

# Initialize with interactive wizard
python3 scripts/init_research_project.py --project-root /abs/path --interactive

# Show live project status (gate scores, phase progress, blockers)
python3 scripts/run_status.py --project-root /abs/path

# Reload project state (restore context)
python3 scripts/reload_project.py --project-root /abs/path

# Reload with verbose output
python3 scripts/reload_project.py --project-root /abs/path --verbose

# Configure project settings
python3 scripts/configure_project.py --project-root /abs/path

# Interactive configuration
python3 scripts/configure_project.py --project-root /abs/path --action interactive

# Set specific configuration
python3 scripts/configure_project.py --project-root /abs/path --action set --key max-loops --value 5

# Clarify research intent
python3 scripts/run_insight.py --idea "Your research idea"

# Non-interactive intent assessment
python3 scripts/run_insight.py --idea "Your idea" --interactive false --json

# Materialize templates
python3 scripts/materialize_templates.py --project-root /abs/path

# Generate dashboard
python3 scripts/generate_dashboard.py --project-root /abs/path

# Run quality gate
python3 scripts/quality_gate.py --project-root /abs/path --phase survey

# Validate phase handoff
python3 scripts/validate_handoff.py --project-root /abs/path --target survey-to-pilot

# Render agent prompt
python3 scripts/render_agent_prompt.py --project-root /abs/path --role survey --task-summary "..." --current-objective "..."

# Analyze existing project (for takeover)
python3 scripts/analyze_project.py --project-root /path/to/existing-project

# Migrate project
python3 scripts/migrate_project.py --project-root /path/to/project --topic "Topic"
```

## Architecture

### Five Phases

| Phase | Agents | Key Deliverable |
|-------|--------|-----------------|
| `survey` | Survey ↔ Critic | `docs/survey/research-readiness-report.md` |
| `pilot` | Code ↔ Adviser | `docs/pilot/pilot-validation-report.md` |
| `experiments` | Code ↔ Adviser | `docs/experiments/evidence-package-index.md` |
| `paper` | Writer ↔ Reviewer | `paper/final-acceptance-report.md` |
| `reflection` | Reflector ↔ Curator | `docs/reflection/runtime-improvement-report.md` |

### Dual-Loop Runtime

- **inner_loop**: Phase-local iteration between two agents (e.g., Survey ↔ Critic)
- **outer_loop**: Orchestrator control over phase transitions, gate evaluation, pivot proposals, recovery, and human approvals

### Project Directory Structure

```
project/
├── .autoresearch/           # System directory
│   ├── state/research-state.yaml    # Single source of truth
│   ├── config/orchestrator-config.yaml
│   ├── dashboard/           # Visual progress tracking
│   ├── runtime/             # Job/GPU/Backend registries
│   └── archive/             # Superseded artifacts
├── agents/                  # Per-role work directories
├── paper/                   # Manuscript and related files
├── code/                    # Code and experiments
└── docs/                    # Phase deliverables
```

### Skill Repository Structure

```
AI-Research-Orchestrator/
├── SKILL.md                 # Main skill definition
├── commands/                # User-facing commands (10)
├── skills/                  # Sub-skills (52+)
├── scripts/                 # Python scripts (38)
├── agents/                  # Agent configurations
├── assets/templates/        # Project templates
├── assets/prompts/          # Agent prompt templates
└── references/              # Protocol documentation
```

## Hard Rules

1. **EXACTLY 2 agents per phase** (primary + reviewer). Do NOT spawn explore agents or helpers.
2. **Use academic APIs for literature** (Semantic Scholar, arXiv, CrossRef, DBLP, OpenAlex), NOT web search.
3. **Do not advance phases** when `validate_handoff.py` or `quality_gate.py` reports failure.
4. **Human gates are mandatory** between phases - no automatic phase transitions.
5. **Save handoff summaries** when dismissing agents; read them when resuming.
6. **Orchestrator is the only agent** that talks directly to the researcher.

## Gate Score Thresholds

| Score | Decision | Action |
|-------|----------|--------|
| 4.5-5.0 | Approve | Proceed immediately |
| 3.5-4.4 | Advance | Minor fixes, then proceed |
| 2.5-3.4 | Revise | Significant revision required |
| 1.5-2.4 | Major Revise | Return to earlier phase |
| 0.0-1.4 | Pivot | Consider alternative or termination |

## Orchestrator Communication

### With Researcher

- Use clear, non-technical language
- Provide context for technical terms
- Summarize complex outputs
- Ask before assuming

### With Sub-Agents

- Provide explicit task summaries
- Set clear success criteria
- Give phase-specific context
- Collect and synthesize outputs

## Initialization System

### Research Types

| Type | Description | GPU Required |
|------|-------------|--------------|
| `ml_experiment` | Machine learning experiments (default) | Yes |
| `theory` | Theoretical/mathematical research | No |
| `survey` | Literature survey/review papers | No |
| `applied` | Applied research with experiments | Yes |

### User Configuration

User preferences stored in `~/.autoresearch/`:
- `user-config.yaml` - Author info, preferences, defaults
- `gpu-registry.yaml` - GPU device registry

### State Version

- Current version: `2.0.0`
- Migration chain: `1.0.0` → `1.1.0` → `1.12.0` → `2.0.0`
- State files are automatically migrated on load

## Key Reference Documents

| Document | Purpose |
|----------|---------|
| `references/workflow-protocol.md` | Phase order and gate requirements |
| `references/system-architecture.md` | Inner/outer loop design |
| `references/gate-rubrics.md` | Detailed scoring rubrics |
| `references/orchestrator-protocol.md` | Orchestrator interaction protocols |
| `references/literature-verification.md` | Citation verification standards |
| `references/phase-execution-details.md` | Substeps within each phase |
| `references/citation-authenticity.md` | Paper phase citation rules |
| `references/experiment-integrity.md` | Experiment logging standards |

## Agent Teams Architecture

This plugin uses the Claude Code Agent Teams feature for inter-agent communication.

### Required Environment Variable

Set before using phase commands:
```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### Agent Teams Tools Available

When Agent Teams is enabled, the following tools become available:
- `TeamCreate` - Create a named team of agents for a phase
- `TeamDelete` - Disband team when phase completes
- `TaskCreate` - Create trackable tasks with dependencies
- `TaskUpdate` - Update task status/owner
- `TaskGet`/`TaskList` - Monitor task progress
- `SendMessage` - Direct agent-to-agent communication

### Team Lifecycle per Phase

1. Orchestrator: `TeamCreate(team_name="research-<phase>", description="...")`
2. Orchestrator: Creates tasks with `TaskCreate` and dependency chains
3. Orchestrator: Spawns Primary Agent with `Agent(subagent_type=..., name=..., team_name=...)`
4. Orchestrator: Spawns Reviewer Agent with `Agent(subagent_type=..., name=..., team_name=...)`
5. Agents communicate directly via `SendMessage`
6. Orchestrator: `TeamDelete()` when phase complete

## Python Requirements

- Python >= 3.9
- Runtime dependencies:
  - PyYAML (for YAML configuration files)
- Dev dependencies: pytest, black, isort, flake8, mypy