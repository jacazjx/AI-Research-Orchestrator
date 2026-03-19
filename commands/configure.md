---
name: airesearchorchestrator:configure
description: "Configure system parameters including research idea, GPU settings, loop limits, and language preferences"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), AskUserQuestion"
---

# Configure System Parameters

Allows users to set or inspect system parameters: research idea, GPU configuration, per-phase loop limits, language settings, and author information.

## Interactive Workflow

When invoked, ask the user what they want to configure:

### Step 1: Select Configuration Action

Ask: "What would you like to do?"

Options:
- `show` - Display current configuration
- `set` - Modify a specific setting
- `interactive` - Full configuration wizard

### Step 2a: Show Current Configuration

If user selects `show`, read and display:

- `.autoresearch/config/orchestrator-config.yaml` (project-level)
- `~/.autoresearch/user-config.yaml` (user-level, if exists)

Format output as a readable summary, not raw YAML.

### Step 2b: Set Specific Setting

If user selects `set`, ask:

"Which setting would you like to modify?"

Then show available keys grouped by scope:

**Project-level settings:**

| Key | Description | Type |
|-----|-------------|------|
| `idea` | Research idea | string |
| `research-type` | Research type | enum: ml_experiment, theory, survey, applied |
| `max-loops` | Maximum loop count per phase | int (1–10) |
| `language` | Language setting | string: "process,paper" |
| `starting-phase` | Starting phase | enum: survey, pilot, experiments, paper, reflection |
| `gpu` | Compute resource GPU ID | string |

**User-level settings:**

| Key | Description | Type |
|-----|-------------|------|
| `author.name` | Author name | string |
| `author.email` | Author email | string |
| `author.institution` | Institution | string |
| `preferences.venue` | Default target venue | string |

After selecting a key, ask for the new value, then invoke:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure_project.py" \
  --project-root "<current_project>" \
  --action set \
  --key "<selected_key>" \
  --value "<new_value>"
```

### Step 2c: Interactive Wizard

If user selects `interactive`, guide through each setting:

1. Show current value (if any)
2. Ask if user wants to change it
3. If yes, collect new value
4. Repeat for all configurable items

After collecting all changes, invoke script with all updates.

## Configuration Priority

Highest to lowest:
1. Values set during this session
2. Project config (`.autoresearch/config/`)
3. User config (`~/.autoresearch/`)
4. System defaults