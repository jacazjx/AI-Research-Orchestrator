---
name: airesearchorchestrator:configure
agent: orchestrator
description: "Configure system parameters, project settings, and user preferences. Use when user says 'configure', '配置', '设置参数', 'setup', 'settings'. Supports interactive and non-interactive modes."
argument-hint: [--project-root /path/to/project] [--action interactive|set|get|list] [--key KEY] [--value VALUE]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Configure Project Settings

Configure project-level settings (in `.autoresearch/config/`) and user-level preferences (in `~/.autoresearch/`). Supports interactive wizard and command-line modes.

## When to Use

- Setting up a new project after initialization
- Adjusting parameters mid-project
- Configuring GPU registry
- Setting user preferences

## Workflow

```
/configure
    │
    ├─→ Interactive mode (default)
    │       ├─→ Show current settings
    │       ├─→ Present configurable options
    │       └─→ Guide through changes
    │
    └─→ Non-interactive mode
            ├─→ --action set: Set a specific key
            ├─→ --action get: Get a specific key
            └─→ --action list: List all settings
```

## Usage

```bash
# Interactive configuration
python3 scripts/configure_project.py --project-root /abs/path/to/project

# Set specific configuration
python3 scripts/configure_project.py --project-root /abs/path/to/project --action set --key max-loops --value 5

# Get specific configuration
python3 scripts/configure_project.py --project-root /abs/path/to/project --action get --key max-loops

# List all configurations
python3 scripts/configure_project.py --project-root /abs/path/to/project --action list
```

## Configurable Settings

### Project-Level (`.autoresearch/config/orchestrator-config.yaml`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `language.process_docs` | string | `zh-CN` | Language for process documentation |
| `language.paper` | string | `en-US` | Language for paper writing |
| `max_loops_per_phase` | int | `3` | Maximum loops before escalation |
| `auto_proceed` | bool | `false` | Auto-advance without human gates |
| `reviewer.enabled` | bool | `true` | Enable external reviewer |
| `reviewer.model` | string | `gpt-5.4` | Reviewer model |

### User-Level (`~/.autoresearch/user-config.yaml`)

| Setting | Type | Description |
|---------|------|-------------|
| `author.name` | string | Author name for papers |
| `author.email` | string | Author email |
| `author.affiliation` | string | Author affiliation |
| `defaults.research_type` | string | Default research type |
| `defaults.venue` | string | Default target venue |

## GPU Registry

Configure available GPU resources in `~/.autoresearch/gpu-registry.yaml`:

```yaml
gpus:
  - id: gpu-001
    name: RTX 4090
    memory: 24GB
    location: local
  - id: gpu-002
    name: A100
    memory: 80GB
    location: remote
    host: gpu-server.example.com
```

## Interactive Wizard Flow

```
┌─────────────────────────────────┐
│  Configuration Wizard           │
├─────────────────────────────────┤
│  1. Language Settings           │
│  2. Loop Limits                 │
│  3. Reviewer Settings           │
│  4. GPU Configuration           │
│  5. User Preferences            │
│                                 │
│  [q] Quit without saving        │
│  [s] Save and exit              │
└─────────────────────────────────┘
```

## Hard Rules

1. **Validate before saving** - Check all inputs for validity
2. **Backup before change** - Create backup of existing config
3. **Show diff** - Display what changed after configuration
4. **Atomic updates** - Either all changes apply or none

## Related Skills

- [init-research](../orchestrator/SKILL.md) — Initialize project with default config
- [reload](./reload/) — Reload project with updated config