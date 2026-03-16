# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Research Orchestrator is a skill that turns a research IDEA into a controlled five-phase project with fixed directories, scored gate checks, visible progress artifacts, and explicit human approval between phases. It is optimized for AI/ML algorithm research that needs literature review, pilot validation, experiments, paper writing, and controlled post-project reflection.

## Key Commands

### Testing

```bash
# Run all tests
python -m pytest tests/ -v --tb=short

# Run specific test file
python -m pytest tests/test_init_research_project.py -v

# Run with coverage
python -m pytest tests/ -v --cov=scripts --cov-report=term-missing
```

### Linting & Formatting

```bash
# Format code
black scripts/ tests/
isort scripts/ tests/

# Check formatting (CI uses these)
black --check scripts/ tests/
isort --check-only --diff scripts/ tests/
flake8 scripts/ tests/ --max-line-length=100 --extend-ignore=E203,W503

# Type checking
mypy scripts/ --ignore-missing-imports
```

### Pre-commit

```bash
# Install hooks
pip install pre-commit && pre-commit install

# Run manually
pre-commit run --all-files
```

## Commands (User-Facing)

The project provides slash commands for each research phase:

| Command | Phase | Trigger Phrases |
|---------|-------|-----------------|
| `/init-research` | Init | "init research", "初始化研究" |
| `/run-survey` | Survey | "run survey", "文献调研" |
| `/run-pilot` | Pilot | "run pilot", "Pilot验证" |
| `/run-experiments` | Experiments | "run experiments", "完整实验" |
| `/write-paper` | Paper | "write paper", "写论文" |
| `/reflect` | Reflection | "reflect", "反思总结" |

Commands are defined in `commands/<name>/COMMAND.md` with frontmatter specifying triggers, scripts, and agents.

### Command Usage

Each command follows this pattern:

```bash
# Direct command invocation
/init-research --project-root /path/to/project --topic "Your idea"

# Equivalent script execution
python3 scripts/init_research_project.py --project-root /path/to/project --topic "Your idea"
```

### Skill Trigger Mechanism

Skills are auto-triggered based on:

1. **Explicit command**: User types `/run-survey`
2. **Trigger phrase**: User says "文献调研" or "start survey"
3. **Phase context**: Current state suggests next phase

**Trigger Flow:**
```
User Input → Command Detection → Skill Loading → Script Execution
     ↓              ↓                ↓                ↓
  "/run-survey"  COMMAND.md    SKILL.md         run_stage_loop.py
```

**Detection Priority:**
1. Exact match: `/init-research`
2. Trigger phrase: "start research project"
3. Phase context: Current state suggests next phase

## Key Scripts

```bash
# Initialize a new research project (non-interactive, default)
python3 scripts/init_research_project.py --project-root /abs/path/to/project --topic "Your idea" --client-type auto

# Initialize with interactive wizard
python3 scripts/init_research_project.py --project-root /abs/path/to/project --interactive

# Initialize with specific research type
python3 scripts/init_research_project.py --project-root /abs/path/to/project --research-type theory

# Materialize templates
python3 scripts/materialize_templates.py --project-root /abs/path/to/project

# Generate dashboard
python3 scripts/generate_dashboard.py --project-root /abs/path/to/project

# Run quality gate check
python3 scripts/quality_gate.py --project-root /abs/path/to/project --phase survey

# Validate handoff between phases
python3 scripts/validate_handoff.py --project-root /abs/path/to/project --target survey-to-pilot

# Render agent prompt
python3 scripts/render_agent_prompt.py --project-root /abs/path/to/project --role survey --task-summary "..." --current-objective "..."

# Analyze existing project (for takeover)
python3 scripts/analyze_project.py --project-root /path/to/existing-project

# Migrate existing project
python3 scripts/migrate_project.py --project-root /path/to/project --topic "Topic"
```

## Initialization System

### Interactive Mode

The initialization wizard provides guided setup:

```bash
python3 scripts/init_research_project.py --project-root /path/to/project --interactive
```

Wizard steps:
1. **Welcome** - Overview of the setup process
2. **Research Idea** - Enter your research topic
3. **Research Type** - Select type (ml_experiment, theory, survey, applied)
4. **Existing Resources** - Handle non-empty directories
5. **Compute Resources** - Configure GPU settings (for GPU-requiring types)
6. **User Profile** - Confirm author information
7. **Confirmation** - Review and approve settings

### Research Types

| Type | Description | GPU Required |
|------|-------------|--------------|
| `ml_experiment` | Machine learning experiments (default) | Yes |
| `theory` | Theoretical/mathematical research | No |
| `survey` | Literature survey/review papers | No |
| `applied` | Applied research with experiments | Yes |

### User Configuration

User preferences are stored in `~/.autoresearch/`:

```
~/.autoresearch/
├── user-config.yaml    # Author info, preferences, defaults
└── gpu-registry.yaml   # GPU device registry
```

User configuration is automatically inherited by new projects.

### Non-Empty Directory Handling

When initializing into an existing directory:
- **Preserve mode** (default in non-interactive): Keep existing files
- **Migrate mode**: Move unrecognized files to `.autoresearch/legacy/{timestamp}/`
- Analysis detects recognized patterns (paper drafts, code, data, etc.)

### State Version Migration

State files are automatically migrated to the current version on load:
- Current version: `2.0.0`
- Migration chain: `1.0.0` → `1.1.0` → `1.12.0` → `2.0.0`

New fields in v2.0.0:
- `research_type`: Type of research project
- `user_config_inherited`: Inherited user configuration
- `gpu_usage_history`: Track GPU usage over time

## Architecture

### Dual-Loop Runtime

- **inner_loop**: Phase-local iteration between two agents (e.g., Survey ↔ Critic)
- **outer_loop**: Orchestrator-level control over phase transitions, gate evaluation, pivot proposals, recovery, and human approvals

### Five Phases (Semantic Names)

| Phase | Agents | Key Deliverable |
|-------|--------|-----------------|
| `survey` | Survey ↔ Critic | `docs/reports/survey/research-readiness-report.md` |
| `pilot` | Code ↔ Adviser | `docs/reports/pilot/pilot-validation-report.md` |
| `experiments` | Code ↔ Adviser | `docs/reports/experiments/evidence-package-index.md` |
| `paper` | Writer ↔ Reviewer | `paper/final-acceptance-report.md` |
| `reflection` | Reflector ↔ Curator | `docs/reports/reflection/runtime-improvement-report.md` |

> Legacy numbered names (`01-survey`, `02-pilot-analysis`, etc.) are supported but deprecated.

### Directory Structure

**Project Structure (per-research-project):**
```
project/
├── .autoresearch/           # System directory
│   ├── state/research-state.yaml    # Single source of truth
│   ├── config/orchestrator-config.yaml
│   ├── dashboard/
│   ├── runtime/             # job, GPU, backend registries
│   └── archive/
├── agents/                  # Per-role work directories
├── paper/
├── code/
└── docs/reports/            # Phase deliverables
```

**Skill Structure (this repository):**
```
AI-Research-Orchestrator/
├── SKILL.md                 # Main skill definition
├── commands/                # User-facing commands (6)
│   ├── init-research/COMMAND.md
│   ├── run-survey/COMMAND.md
│   ├── run-pilot/COMMAND.md
│   ├── run-experiments/COMMAND.md
│   ├── write-paper/COMMAND.md
│   └── reflect/COMMAND.md
├── skills/                  # Sub-skills (17)
│   ├── idea-discovery/SKILL.md
│   ├── research-lit/SKILL.md
│   ├── paper-pipeline/SKILL.md
│   └── ... (14 more)
├── scripts/                 # Python scripts (29)
│   ├── orchestrator_common.py
│   ├── init_research_project.py
│   ├── user_config.py       # User configuration management
│   ├── gpu_manager.py       # GPU registry management
│   ├── legacy_handler.py    # Non-empty directory handling
│   ├── state_migrator.py    # State version migration
│   ├── init_wizard.py       # Interactive initialization wizard
│   ├── prompts.py           # Interactive prompt utilities
│   └── ... (21 more)
├── agents/                  # Agent configurations
├── assets/                  # Templates and prompts
│   ├── prompts/
│   └── templates/
└── references/              # Documentation (17)
```

### Hard Rules

1. **Each phase has EXACTLY 2 agents** (primary + reviewer). Do NOT spawn explore agents or helpers.
2. **Use academic database APIs for literature** (Semantic Scholar, arXiv, CrossRef, DBLP, OpenAlex), NOT web search.
3. **Do not advance phases** when `validate_handoff.py` or `quality_gate.py` reports failure.
4. **Human gates are mandatory** between phases - no automatic rollback without user decision.
5. **Save handoff summaries** when dismissing agents; read them when resuming.
6. **Orchestrator is the only agent** that talks directly to the researcher.

### Gate Score Thresholds

| Score | Decision | Action |
|-------|----------|--------|
| 4.5-5.0 | Approve | Proceed |
| 3.5-4.4 | Advance | Minor fixes, proceed |
| 2.5-3.4 | Revise | Significant revision |
| 1.5-2.4 | Major Revise | Return to earlier phase |
| 0.0-1.4 | Pivot | Consider alternative |

## Key Reference Documents

- `references/workflow-protocol.md` - Phase order and gate requirements
- `references/system-architecture.md` - Inner/outer loop design
- `references/gate-rubrics.md` - Detailed scoring rubrics per gate
- `references/orchestrator-protocol.md` - Orchestrator interaction protocols
- `references/literature-verification.md` - Citation verification standards
- `references/phase-execution-details.md` - Substeps within each phase
- `references/citation-authenticity.md` - Paper phase citation rules
- `references/experiment-integrity.md` - Experiment logging standards

## Python Requirements

- Python >= 3.9
- No external runtime dependencies (scripts use stdlib only)
- Dev dependencies: pytest, black, isort, flake8, mypy, bandit