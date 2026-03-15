# Commands Directory Structure Design

> **For agentic workers:** This is a design specification. Follow superpowers command pattern.

**Goal:** Design commands/ directory to provide user-facing slash commands for research workflow phases.

**Date:** 2026-03-15

---

## Overview

Commands provide a user-friendly interface to trigger research workflow phases. Each command is a self-contained markdown file that maps to underlying Python scripts and skill definitions.

## Directory Structure

```
AI-Research-Orchestrator/
├── commands/
│   ├── init-research/
│   │   └── COMMAND.md
│   ├── run-survey/
│   │   └── COMMAND.md
│   ├── run-pilot/
│   │   └── COMMAND.md
│   ├── run-experiments/
│   │   └── COMMAND.md
│   ├── write-paper/
│   │   └── COMMAND.md
│   └── reflect/
│       └── COMMAND.md
├── skills/                    # Existing skills
├── scripts/                   # Existing Python scripts
└── SKILL.md                   # Main skill
```

---

## Frontmatter Format

Each `COMMAND.md` follows this frontmatter specification:

```yaml
---
name: command-name
description: Use when [specific triggering conditions]. Triggers: "[trigger words]".
script: scripts/<script_name>.py
arguments:
  required:
    - name: arg_name
      description: Argument description
      type: string | path | enum
  optional:
    - name: optional_arg
      description: Optional argument description
      type: string
      default: default_value
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
phase: survey | pilot | experiments | paper | reflection | init
agents:
  - agent_role_1
  - agent_role_2
---
```

### Field Specifications

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Command identifier (lowercase, hyphens only) |
| `description` | Yes | When to use, max 500 chars |
| `script` | Yes | Python script to execute |
| `arguments` | No | Command arguments definition |
| `triggers` | Yes | Trigger phrases for auto-detection |
| `phase` | Yes | Associated research phase |
| `agents` | Yes | Agents involved in this command |

---

## Command Definitions

### 1. /init-research

```yaml
---
name: init-research
description: Use when starting a new AI/ML research project or taking over an existing research codebase. Creates project structure, initializes state, and prepares workspace. Triggers: "start research", "init project", "new research", "initialize research".
script: scripts/init_research_project.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
    - name: topic
      description: Research topic or idea description
      type: string
  optional:
    - name: client-type
      description: Client initialization type
      type: enum
      values: [auto, codex, openai, claude]
      default: auto
triggers:
  - "start research project"
  - "init research"
  - "new research"
  - "initialize project"
  - "create research workspace"
  - "init-research"
phase: init
agents: []
---
```

**Execution:**
```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/project \
  --topic "Your research idea" \
  --client-type auto
```

---

### 2. /run-survey

```yaml
---
name: run-survey
description: Use when starting the survey phase of a research project. Surveys literature, analyzes related work, and produces research readiness report. Triggers: "run survey", "start survey phase", "literature review".
script: scripts/run_stage_loop.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
  optional:
    - name: max-iterations
      description: Maximum survey iterations
      type: integer
      default: 10
triggers:
  - "run survey"
  - "start survey"
  - "survey phase"
  - "literature review"
  - "run-survey"
phase: survey
agents:
  - survey
  - critic
---
```

**Execution:**
```bash
python3 scripts/run_stage_loop.py \
  --project-root /abs/path/to/project \
  --phase survey \
  --max-iterations 10
```

**Outputs:**
- `docs/reports/survey/research-readiness-report.md`
- `docs/reports/survey/phase-scorecard.md`
- `agents/survey/notes.md`

---

### 3. /run-pilot

```yaml
---
name: run-pilot
description: Use when starting the pilot phase after survey gate approval. Runs pilot experiments to validate research approach. Triggers: "run pilot", "start pilot", "pilot validation".
script: scripts/run_stage_loop.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
  optional:
    - name: max-iterations
      description: Maximum pilot iterations
      type: integer
      default: 10
triggers:
  - "run pilot"
  - "start pilot"
  - "pilot phase"
  - "pilot validation"
  - "run-pilot"
phase: pilot
agents:
  - coder
  - adviser
---
```

**Execution:**
```bash
python3 scripts/run_stage_loop.py \
  --project-root /abs/path/to/project \
  --phase pilot \
  --max-iterations 10
```

**Outputs:**
- `docs/reports/pilot/pilot-validation-report.md`
- `docs/reports/pilot/phase-scorecard.md`
- `code/` (pilot code artifacts)

---

### 4. /run-experiments

```yaml
---
name: run-experiments
description: Use when starting the full experiments phase after pilot gate approval. Runs comprehensive experiments and generates evidence packages. Triggers: "run experiments", "start experiments", "full experiments".
script: scripts/run_stage_loop.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
  optional:
    - name: max-iterations
      description: Maximum experiment iterations
      type: integer
      default: 20
    - name: remote
      description: Run on remote GPU cluster
      type: boolean
      default: false
triggers:
  - "run experiments"
  - "start experiments"
  - "experiments phase"
  - "full experiments"
  - "run-experiments"
phase: experiments
agents:
  - coder
  - adviser
---
```

**Execution:**
```bash
# Local execution
python3 scripts/run_stage_loop.py \
  --project-root /abs/path/to/project \
  --phase experiments \
  --max-iterations 20

# Remote execution
python3 scripts/run_remote_job.py \
  --project-root /abs/path/to/project \
  --config remote-config.yaml
```

**Outputs:**
- `docs/reports/experiments/evidence-package-index.md`
- `docs/reports/experiments/results-summary.md`
- `docs/reports/experiments/phase-scorecard.md`
- `code/experiments/`

---

### 5. /write-paper

```yaml
---
name: write-paper
description: Use when starting the paper writing phase after experiments gate approval. Writes LaTeX paper, manages citations, and runs citation audit. Triggers: "write paper", "paper phase", "draft paper".
script: scripts/run_stage_loop.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
  optional:
    - name: max-iterations
      description: Maximum writing iterations
      type: integer
      default: 15
    - name: citation-audit
      description: Run citation authenticity audit
      type: boolean
      default: true
triggers:
  - "write paper"
  - "paper phase"
  - "draft paper"
  - "write-paper"
  - "paper writing"
phase: paper
agents:
  - writer
  - reviewer
---
```

**Execution:**
```bash
python3 scripts/run_stage_loop.py \
  --project-root /abs/path/to/project \
  --phase paper \
  --max-iterations 15

# Citation audit
python3 scripts/run_citation_audit.py \
  --project-root /abs/path/to/project
```

**Outputs:**
- `paper/main.tex`
- `paper/references.bib`
- `paper/citation-audit-report.md`
- `docs/reports/paper/final-acceptance-report.md`

---

### 6. /reflect

```yaml
---
name: reflect
description: Use when starting the reflection phase after paper completion. Generates lessons learned, runtime improvements, and project archive. Triggers: "reflect", "reflection phase", "lessons learned".
script: scripts/run_stage_loop.py
arguments:
  required:
    - name: project-root
      description: Absolute path to project directory
      type: path
  optional:
    - name: activate-overlay
      description: Apply improvements to skill templates
      type: boolean
      default: false
triggers:
  - "reflect"
  - "reflection phase"
  - "lessons learned"
  - "project review"
  - "reflect"
phase: reflection
agents:
  - reflector
  - curator
---
```

**Execution:**
```bash
python3 scripts/run_stage_loop.py \
  --project-root /abs/path/to/project \
  --phase reflection

# Apply overlay improvements
python3 scripts/apply_overlay.py \
  --project-root /abs/path/to/project
```

**Outputs:**
- `docs/reports/reflection/lessons-learned.md`
- `docs/reports/reflection/runtime-improvement-report.md`
- `.autoresearch/archive/archive-index.md`

---

## Command-to-Skill Trigger Relationship

### Trigger Flow

```
User Input → Command Detection → Skill Loading → Script Execution
     ↓              ↓                ↓                ↓
  "/run-survey"  COMMAND.md    SKILL.md         run_stage_loop.py
```

### Detection Priority

1. **Exact match**: User types `/init-research`
2. **Trigger phrase**: User says "start research project"
3. **Phase context**: Current state suggests next phase

### Skill Integration

| Command | Related Skills | State Effect |
|---------|----------------|--------------|
| `/init-research` | `idea-discovery`, `research-init` | Creates `research-state.yaml` |
| `/run-survey` | `research-lit`, `survey` | Sets `phase: survey` |
| `/run-pilot` | `pilot-validation`, `experiment-design` | Sets `phase: pilot` |
| `/run-experiments` | `experiment-runner`, `evidence-packager` | Sets `phase: experiments` |
| `/write-paper` | `paper-writer`, `citation-audit` | Sets `phase: paper` |
| `/reflect` | `reflection`, `archival` | Sets `phase: reflection` |

### Gate Enforcement

Commands respect gate requirements:

```
/init-research → (no gate required)
    ↓
/run-survey → Gate 0 passed (project initialized)
    ↓
/run-pilot → Gate 1 passed (survey score ≥ 3.5)
    ↓
/run-experiments → Gate 2 passed (pilot validated)
    ↓
/write-paper → Gate 3 passed (experiments complete)
    ↓
/reflect → Gate 4 passed (paper accepted)
```

If gate not passed, command returns:
```
ERROR: Gate 2 not passed. Run quality_gate.py to check requirements.
```

---

## Implementation Notes

### Command File Template

```markdown
---
name: <command-name>
description: Use when <trigger conditions>. Triggers: "<trigger words>".
script: scripts/<script>.py
arguments:
  required:
    - name: <arg>
      description: <desc>
      type: <type>
  optional:
    - name: <arg>
      description: <desc>
      type: <type>
      default: <value>
triggers:
  - "<trigger 1>"
  - "<trigger 2>"
phase: <phase>
agents:
  - <agent1>
  - <agent2>
---

# <Command Name>

## Overview
<Brief description of what this command does>

## When to Use
<Specific conditions for using this command>

## Arguments
<Argument documentation>

## Examples
<Usage examples>

## Related Commands
<Links to related commands>
```

### Argument Types

| Type | Description | Validation |
|------|-------------|------------|
| `string` | Text value | Non-empty |
| `path` | File system path | Must exist (for input) |
| `integer` | Whole number | Range check |
| `boolean` | True/false | Flag parsing |
| `enum` | Enumerated values | Must be in values list |

---

## Summary

The commands/ directory provides:

1. **User-friendly interface**: `/command-name` format
2. **Auto-detection**: Trigger phrases enable command discovery
3. **Script integration**: Commands map to existing Python scripts
4. **Gate enforcement**: Commands respect phase gate requirements
5. **Agent coordination**: Each command specifies involved agents

This design follows the superpowers pattern while integrating with the existing AI-Research-Orchestrator infrastructure.