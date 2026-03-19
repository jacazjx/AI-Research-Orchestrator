---
name: airesearchorchestrator:reload
agent: orchestrator
description: "Reload project state and configuration to restore research context in a new session. Use when user says 'reload', '重新加载', '恢复状态', '继续研究', 'reload project'. Run this first whenever you open a new Claude Code session on an existing project."
argument-hint: [--project-root /path/to/project] [--verbose] [--json]
allowed-tools: Read, Bash, Glob, Grep
---

# Reload Project State

Restores full project context at the start of a new session: reads state, config, GitMem history, and produces a structured status report so the orchestrator can resume exactly where it left off.

## When to Use

- Starting a new session on an in-progress project
- Switching between multiple research projects
- Refreshing context after an external state change
- Rebuilding context after an unexpected interruption

## Workflow

```
/reload
    │
    ├─→ 1. Locate project root
    │       └─→ Find .autoresearch/ directory
    │
    ├─→ 2. Load project state
    │       ├─→ research-state.yaml
    │       ├─→ orchestrator-config.yaml
    │       └─→ status.json
    │
    ├─→ 3. Run state migration
    │       └─→ Call state_migrator.py if schema outdated
    │
    ├─→ 4. Load user config
    │       └─→ ~/.autoresearch/ user-level settings
    │
    ├─→ 5. Check GitMem history
    │       └─→ Read version-tracking log
    │
    └─→ 6. Output status report
            ├─→ Project info
            ├─→ Phase progress
            ├─→ Configuration
            └─→ Next actions
```

## Usage

```bash
# Standard reload
python3 scripts/reload_project.py --project-root /abs/path/to/project

# Verbose output
python3 scripts/reload_project.py --project-root /abs/path/to/project --verbose

# JSON output
python3 scripts/reload_project.py --project-root /abs/path/to/project --json
```

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

- **Project not found**: Prompt user to run `/init-research` first
- **Corrupt state file**: Attempt recovery from backup; fall back to re-initialization prompt
- **Incompatible schema version**: Run automatic state migration

## Hard Rules

1. **Always run first** in a new session on an existing project
2. **Never modify state** - this is a read-only operation
3. **Report all errors** - don't silently skip missing files
4. **Suggest next action** based on current phase and gate status

## Related Skills

- [status](./status/) - Quick status check without full reload
- [init-research](../orchestrator/SKILL.md) - Initialize a new project