---
name: airesearchorchestrator:init-research
description: "Initialize a new AI research project with proper directory structure and state management"
script: scripts/init_research_project.py
triggers:
  - "init research"
  - "start research project"
  - "初始化研究"
  - "新建研究项目"
phase: init
agents: []
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
    - name: topic
      description: Research topic or idea description
      type: string
  optional:
    - name: client-type
      description: Client type for agent execution
      type: enum
      values: [auto, codex, openai, claude]
      default: auto
---

# Initialize Research Project

Creates the five-phase research workflow structure with:

- `.autoresearch/` - System directory (state, config, dashboard, runtime)
- `agents/` - Per-role work directories
- `paper/` - Paper-related files
- `code/` - Code-related files
- `docs/` - Documentation and reports

## Usage

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/project \
  --topic "Your research idea" \
  --client-type auto
```

## What Happens

1. Creates directory structure
2. Initializes `research-state.yaml`
3. Generates `orchestrator-config.yaml`
4. Creates AGENTS.md or CLAUDE.md
5. Materializes templates