---
name: reload
description: "Reload project state and configuration to restore research context in a new session"
script: scripts/reload_project.py
triggers:
  - "reload"
  - "重新加载"
  - "恢复状态"
  - "继续研究"
  - "reload project"
phase: any
agents: []
arguments:
  required:
    - name: project-root
      description: Absolute path to the research project root directory
      type: path
  optional:
    - name: verbose
      description: Show detailed output
      type: boolean
      default: false
    - name: json
      description: Output JSON format
      type: boolean
      default: false
---

# Reload Project State

Restores full project context at the start of a new session: reads state, config, GitMem history, and produces a structured status report so the orchestrator can resume exactly where it left off.

**Run this first whenever you open a new Claude Code session on an existing project.**

## Use Cases

- Starting a new session on an in-progress project
- Switching between multiple research projects
- Refreshing context after an external state change
- Rebuilding context after an unexpected interruption

## Usage

```bash
python3 scripts/reload_project.py --project-root /abs/path/to/project
python3 scripts/reload_project.py --project-root /abs/path/to/project --verbose
python3 scripts/reload_project.py --project-root /abs/path/to/project --json
```

## Execution Flow

1. **Locate project root** — find `.autoresearch/` directory
2. **Load project state** — read `research-state.yaml`, `orchestrator-config.yaml`, `status.json`
3. **Run state migration** — call `state_migrator.py` if the state schema version is outdated
4. **Load user config** — read `~/.autoresearch/` user-level settings
5. **Check GitMem history** — read version-tracking log for recent changes
6. **Generate context summary** — project info, phase progress, configuration
7. **Output status report** — formatted summary ready for the orchestrator

## Output Example

```markdown
## Project State Reloaded

### Basic Information
- **Project ID**: my-research-project
- **Topic**: Transformer-based time-series forecasting optimization
- **Research type**: ml_experiment
- **Created**: 2026-03-15

### Current Progress
- **Phase**: pilot (2 of 5)
- **Gate**: gate_2
- **Completion**: 25%

### Completed Work
- Survey phase complete (gate score: 4.2)
- Pilot phase in progress

### Configuration
- **Language**: process docs (zh-CN) / paper (en-US)
- **GPU**: RTX 4090 (ID: gpu-001)
- **Max loops per phase**: 3

### Next Actions
1. Complete pilot experiment design
2. Run pilot validation
3. Await Gate 2 review
```

## Error Handling

- **Project not found**: prompts user to run `/init-research` first
- **Corrupt state file**: attempts recovery from backup; falls back to re-initialization prompt
- **Incompatible schema version**: runs automatic state migration
