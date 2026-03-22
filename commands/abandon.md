---
name: airesearchorchestrator:abandon
description: "Gracefully abandon or archive a research project with proper state cleanup"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), AskUserQuestion"
---

# Abandon / Archive Project

Gracefully exit a research project at any point. Archives current state and deliverables.

## Steps

1. **Read project state** -- load `.autoresearch/state/research-state.yaml`.

2. **Confirm with user** -- show current phase, completion percentage, and deliverables produced. Ask:
   - "Are you sure you want to abandon this project? All deliverables will be preserved but the project will be marked as archived."

3. **Archive deliverables** -- for each completed phase, archive deliverables:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/phase_rollback.py \
     --project-root <project_root> --phase <phase> --reason abandon
   ```

4. **Update state** -- set:
   - `current_phase: "archive"`
   - `progress.next_action: "project-abandoned"`
   - `progress.active_blocker: "none"`
   - Record abandonment reason in `human_decisions` log

5. **Save state** and report summary to user:
   - Phases completed
   - Deliverables archived
   - How to resume if they change their mind (`/configure --starting-phase <phase>` + `/init-research`)

## When to use

- User says "stop", "cancel", "abandon", "archive this project", "I want to quit"
- Project has been stalled and user wants to move on
- Research direction is no longer viable and no pivot makes sense

**This command requires explicit user confirmation before executing.**
