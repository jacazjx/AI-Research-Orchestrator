---
name: airesearchorchestrator:reload
description: "Restore project context from saved state at the start of a session"
allowed-tools: "Read, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Reload Project Context

Restores the full project context from `.autoresearch/state/research-state.yaml`. Use this command at the start of a new session to understand where you left off.

## Execution

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/reload_project.py" --project-root "$ARG_PROJECT_ROOT"
```

## What It Does

1. Reads `research-state.yaml` and `orchestrator-config.yaml`
2. Displays current phase, gate status, and blockers
3. Shows what deliverables exist and what's missing
4. Recommends next actions based on current state

## When to Use

- Starting a new Claude Code session on an existing project
- After a long break from the project
- When you're unsure what to do next

## Output

The reload command provides:

- **Current phase** and gate status
- **Progress indicators** (completion percentage, loop counts)
- **Missing deliverables** that need to be created
- **Next recommended action**

## Relationship to Other Commands

- **`/reload`** — restores session context; use at session start
- **`/status`** — shows live gate state; use mid-session to check progress
