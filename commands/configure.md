---
description: "Configure system parameters including research idea, GPU settings, loop limits, and language preferences"
argument-hint: "[--project-root <path>] [--action <show|set|interactive>] [--key <config-key>] [--value <config-value>]"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Configure System Parameters

Allows users to set or inspect system parameters: research idea, GPU configuration, per-phase loop limits, language settings, and author information.

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure_project.py" $ARGUMENTS
```

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

## Configuration Priority

Highest to lowest:
1. Command-line arguments (`--max-loops=5`)
2. Project config (`.autoresearch/config/`)
3. User config (`~/.autoresearch/`)
4. System defaults