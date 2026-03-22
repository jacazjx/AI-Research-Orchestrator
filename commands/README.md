# AI Research Orchestrator Commands

This directory contains user-facing commands for the five-phase research workflow.

## Directory Structure

```
commands/
├── init-research.md    # Initialize a new research project
├── configure.md        # Configure system parameters
├── insight.md          # Interactive intent clarification
├── status.md           # Show live project status
├── pivot.md            # Manage research direction pivots
├── run-survey.md       # Literature survey and readiness assessment
├── run-pilot.md        # Pilot validation and feasibility check
├── run-experiments.md  # Full experiments and evidence collection
├── write-paper.md      # Paper writing and submission preparation
├── reflect.md          # Lessons learned and project evolution
├── abandon.md          # Gracefully archive and exit a project
├── post-submission.md  # Post-submission: self-review, rebuttal, post-acceptance
└── README.md           # This file
```

## Available Commands

| Command | Phase | Agents | Trigger Phrases |
|---------|-------|--------|-----------------|
| `/init-research` | Init | - | "init research", "初始化研究" |
| `/configure` | Any | - | "configure", "配置", "设置参数" |
| `/insight` | Init | - | "insight", "澄清意图", "明确想法" |
| `/status` | Any | - | "status", "查看状态", "项目状态" |
| `/pivot` | Any | - | "pivot", "转向", "换方向" |
| `/run-survey` | Survey | Survey, Critic | "run survey", "文献调研" |
| `/run-pilot` | Pilot | Code, Adviser | "run pilot", "Pilot验证" |
| `/run-experiments` | Experiments | Code, Adviser | "run experiments", "完整实验" |
| `/write-paper` | Paper | Writer, Reviewer | "write paper", "写论文" |
| `/reflect` | Reflection | Reflector, Curator | "reflect", "反思总结" |
| `/abandon` | Any | - | "abandon", "stop project", "archive project" |
| `/post-submission` | Post-Paper | Writer | "self review", "write rebuttal", "post acceptance", "投稿自查", "写rebuttal" |

## Workflow Order

```
/init-research → /run-survey → /run-pilot → /run-experiments → /write-paper → /reflect
     Setup          Phase 1       Phase 2          Phase 3              Phase 4        Phase 5
```

## Utility Commands

These commands can be used at any point in the workflow:

- **`/configure`** - Modify project or user settings
- **`/insight`** - Clarify research intent before or during a project
- **`/status`** - Show live project status with gate scores and blockers
- **`/pivot`** - Propose, review, or execute a research direction pivot
- **`/abandon`** - Gracefully archive and exit a project at any phase
- **`/post-submission`** - Post-submission workflow: self-review, rebuttal, post-acceptance materials

> **Note**: Project state is automatically reloaded on session start via the `SessionStart` hook.

## COMMAND.md Frontmatter Schema

Each `COMMAND.md` file contains the following frontmatter fields:

```yaml
---
name: <command-name>
description: "<description>"
allowed-tools: "Read, Write, Edit, ..."
---
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Namespaced command identifier (e.g., `airesearchorchestrator:run-survey`) |
| `description` | Yes | Brief description of the command |
| `allowed-tools` | Yes | Comma-separated list of tools the command can use |

## Quick Start

### Start a New Project

```bash
/init-research --project-root /path/to/project --topic "Your research idea"
```

### Run Full Pipeline

```bash
/run-survey --project-root /path/to/project
/run-pilot --project-root /path/to/project
/run-experiments --project-root /path/to/project
/write-paper --project-root /path/to/project
/reflect --project-root /path/to/project
```

## Gate Requirements

Each phase transition requires:

1. **Gate 0 → 1**: Project initialization complete
2. **Gate 1 → 2**: `research-readiness-report.md` approved
3. **Gate 2 → 3**: `pilot-validation-report.md` approved
4. **Gate 3 → 4**: `evidence-package-index.md` approved
5. **Gate 4 → 5**: `final-acceptance-report.md` approved
6. **Gate 5**: Project completion decision

## Related Skills

The commands delegate to these skills:

- `skills/ideation/` - Research ideation: generate, filter, verify novelty
- `skills/literature/` - Literature search and survey
- `skills/run-experiment/` - Experiment execution (pilot and full scale)
- `skills/paper-write/` - Paper planning and LaTeX writing
- `skills/external-review/` - External review via Codex MCP (single-shot or multi-round)
- `skills/self-review/` - Pre-submission self-review checklist
- `skills/rebuttal/` - Structured rebuttal writing for reviewer responses
- `skills/post-acceptance/` - Post-acceptance dissemination materials

## Configuration

Commands respect settings in `.autoresearch/config/orchestrator-config.yaml`:

```yaml
aris:
  auto_proceed: false  # Require manual gate approval
  reviewer:
    enabled: true
    model: gpt-5.4
```