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

> **Interactive Mode (no arguments):** When this command is called without arguments, Claude acting
> as Orchestrator MUST NOT run the script immediately. Instead, ask the user interactively for:
>
> 1. **Project location** — where should the project be created? (default: current working directory)
> 2. **Research idea** — a brief description of the research topic or problem statement
> 3. **Research type** — one of: `ml_experiment` (default), `theory`, `survey`, `applied`
> 4. **GPU availability** — does the user have GPU access? (yes/no; affects resource planning)
>
> Once all four parameters are collected, invoke the script with the gathered values:
>
> ```bash
> python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_research_project.py" \
>   --project-root "<collected_path>" \
>   --topic "<collected_idea>" \
>   --client-type auto
> ```
>
> This replaces the previous non-interactive invocation that fails without `--project-root`.

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