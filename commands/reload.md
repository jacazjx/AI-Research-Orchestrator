---
description: "Reload project state and configuration to restore research context in a new session"
argument-hint: "[--project-root <path>] [--verbose] [--json]"
allowed-tools: "Read, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Reload Project State

Restores full project context at the start of a new session: reads state, config, GitMem history, and produces a structured status report so the orchestrator can resume exactly where it left off.

**Run this first whenever you open a new Claude Code session on an existing project.**

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/reload_project.py" $ARGUMENTS
```

## Usage

```bash
python3 scripts/reload_project.py --project-root /abs/path/to/project
python3 scripts/reload_project.py --project-root /abs/path/to/project --verbose
python3 scripts/reload_project.py --project-root /abs/path/to/project --json
```

## Use Cases

- Starting a new session on an in-progress project
- Switching between multiple research projects
- Refreshing context after an external state change
- Rebuilding context after an unexpected interruption

## Execution Flow

1. **Locate project root** — find `.autoresearch/` directory
2. **Load project state** — read `research-state.yaml`, `orchestrator-config.yaml`, `status.json`
3. **Run state migration** — call `state_migrator.py` if the state schema version is outdated
4. **Load user config** — read `~/.autoresearch/` user-level settings
5. **Check GitMem history** — read version-tracking log for recent changes
6. **Generate context summary** — project info, phase progress, configuration
7. **Output status report** — formatted summary ready for the orchestrator