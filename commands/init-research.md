---
name: airesearchorchestrator:init-research
description: "Initialize a new AI research project with proper directory structure and state management"
argument-hint: "[--project-root <path>] [--topic <string>] [--interactive]"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Initialize Research Project

Creates the five-phase research workflow structure with:

- `.autoresearch/` - System directory (state, config, dashboard, runtime)
- `agents/` - Per-role work directories
- `paper/` - Paper-related files
- `code/` - Code-related files
- `docs/` - Documentation and reports

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_research_project.py" $ARGUMENTS
```

## Usage

```bash
# Non-interactive
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/project \
  --topic "Your research idea" \
  --client-type auto

# Interactive wizard
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/project \
  --interactive
```

## What Happens

1. Creates directory structure
2. Initializes `research-state.yaml`
3. Generates `orchestrator-config.yaml`
4. Creates AGENTS.md or CLAUDE.md
5. Materializes templates