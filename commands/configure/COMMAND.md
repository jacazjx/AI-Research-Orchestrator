---
name: airesearchorchestrator:configure
description: "Configure system parameters including research idea, GPU settings, loop limits, and author info"
script: scripts/configure_project.py
triggers:
  - "configure"
  - "配置"
  - "设置参数"
  - "config"
  - "修改配置"
phase: any
agents: []
arguments:
  required:
    - name: project-root
      description: Absolute path to the research project root directory
      type: path
  optional:
    - name: action
      description: Configuration action (show, set, interactive)
      type: enum
      values: [show, set, interactive]
      default: show
    - name: key
      description: Configuration key (e.g. idea, max-loops, gpu)
      type: string
    - name: value
      description: Configuration value
      type: string
    - name: scope
      description: Configuration scope (project, user)
      type: enum
      values: [project, user]
      default: project
---

# Configure System Parameters

Allows users to set or inspect system parameters: research idea, GPU configuration, per-phase loop limits, language settings, and author information.

## Use Cases

- Change the research idea after initialization
- Adjust per-phase maximum loop counts
- Assign GPU resources
- Change language settings
- Update author information

## Usage

```bash
# Show current configuration
python3 scripts/configure_project.py --project-root /abs/path

# Interactive configuration wizard
python3 scripts/configure_project.py --project-root /abs/path --action interactive

# Set a specific key
python3 scripts/configure_project.py --project-root /abs/path --action set --key idea --value "New research idea"
python3 scripts/configure_project.py --project-root /abs/path --action set --key max-loops --value 5

# Assign a GPU
python3 scripts/configure_project.py --project-root /abs/path --action set --key gpu --value "gpu-001"
```

## Configuration Keys

### Project-level (stored in `.autoresearch/config/`)

| Key | Description | Type |
|-----|-------------|------|
| `idea` | Research idea | string |
| `research-type` | Research type | enum: ml_experiment, theory, survey, applied |
| `max-loops` | Maximum loop count per phase | int (1–10) |
| `language` | Language setting | string: "process,lang" |
| `starting-phase` | Starting phase | enum: survey, pilot, experiments, paper, reflection |
| `gpu` | Compute resource GPU ID | string |

### User-level (stored in `~/.autoresearch/`)

| Key | Description | Type |
|-----|-------------|------|
| `author.name` | Author name | string |
| `author.email` | Author email | string |
| `author.institution` | Institution | string |
| `preferences.venue` | Default target venue | string |

## Execution Flow

1. **Parse arguments** — determine action type and target key
2. **Load existing config** — read project and user config files
3. **Execute action**
   - `show`: display current configuration
   - `set`: update the specified key
   - `interactive`: launch interactive wizard
4. **Validate** — check value type and range
5. **Save** — write updated config to disk
6. **Report** — display the updated configuration

## Interactive Wizard

```
⚙️  Configuration Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current configuration:
┌─────────────────────────────────────────┐
│ Project Configuration                   │
├─────────────────────────────────────────┤
│ Idea: Transformer-based time series     │
│ Type: ml_experiment                     │
│ Max loops: 3                            │
│ GPU: RTX 4090 (gpu-001)                 │
│ Language: process/zh-CN, paper/en-US   │
└─────────────────────────────────────────┘

Select what to change:
1. Research idea
2. Research type
3. Max loop count
4. GPU resource
5. Language settings
6. Author information
7. Save and exit
8. Discard changes

Choice [1-8]:
```

## Configuration Priority

Highest to lowest:
1. Command-line arguments (`--max-loops=5`)
2. Project config (`.autoresearch/config/`)
3. User config (`~/.autoresearch/`)
4. System defaults

## Error Handling

- **Unknown key**: lists all valid keys
- **Invalid value**: shows expected type and range
- **Permission denied**: explains required permissions
- **Corrupt config file**: suggests repair or re-initialization
