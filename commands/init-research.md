---
name: autoresearch:init-research
description: "Initialize a new five-phase AI research project. Use when user says 'init research', 'start research project', '初始化研究', '新建研究项目'."
triggers:
  - "init research"
  - "start research project"
  - "初始化研究"
  - "新建研究项目"
  - "research init"
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