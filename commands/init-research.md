---
name: airesearchorchestrator:init-research
description: "Initialize a new AI research project with proper directory structure and state management"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), AskUserQuestion"
---

# Initialize Research Project

Creates the five-phase research workflow structure with:

- `.autoresearch/` - System directory (state, config, dashboard, runtime)
- `agents/` - Per-role work directories
- `paper/` - Paper-related files
- `code/` - Code and experiments
- `docs/` - Documentation and reports

## Interactive Workflow

When invoked, ask the user for the following information using AskUserQuestion:

### Step 1: Project Location

Ask: "Where should the research project be created?"

- Provide current working directory as default option
- Allow user to specify a custom path
- Validate the path exists or can be created

### Step 2: Research Idea

Ask: "What is your research idea or topic?"

- Accept a brief description of the research topic or problem statement
- This will be stored in `.autoresearch/idea-brief.md`

### Step 3: Research Type

Ask: "What type of research is this?"

Options:
- `ml_experiment` - Machine learning experiments (default) — Requires GPU
- `theory` - Theoretical/mathematical research — No GPU needed
- `survey` - Literature survey/review papers — No GPU needed
- `applied` - Applied research with experiments — Requires GPU

### Step 4: GPU Availability (conditional)

If research type is `ml_experiment` or `applied`, ask:

"Do you have GPU access for running experiments?"

Options:
- `yes` - GPU available, configure resource allocation
- `no` - No GPU, consider cloud options or reduce scope

## Execution

After collecting all parameters, invoke:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_research_project.py" \
  --project-root "<collected_path>" \
  --topic "<collected_idea>" \
  --research-type "<collected_type>" \
  --client-type auto
```

## What Happens

1. Creates directory structure
2. Initializes `research-state.yaml`
3. Generates `orchestrator-config.yaml`
4. Creates AGENTS.md or CLAUDE.md (based on client type)
5. Materializes templates from `assets/templates/`

## After Initialization

Inform the user:

1. Project created at `<project-root>`
2. Next step: Run `/run-survey` to begin literature review
3. Or run `/insight` first to clarify research intent