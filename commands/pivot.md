---
name: airesearchorchestrator:pivot
description: "Propose, review, or execute a research direction pivot when the current approach is not viable"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), AskUserQuestion"
---

# Manage Research Pivots

Propose, review, and execute research direction pivots. Use when the current research direction is not viable, a dead end is reached, or evidence suggests a different approach.

## Interactive Workflow

### Step 1: Select Action

Ask: "What pivot action do you want to take?"

Options:
- `propose` — Create a new pivot proposal
- `review` — Review and decide on a pending pivot
- `list` — Show all pending pivot proposals

### Step 2a: Propose a Pivot

If user selects `propose`, collect:

1. **Pivot type** — Ask: "What kind of pivot?"
   - `downgrade_to_pilot` — Restart from Pilot phase with adjusted hypothesis
   - `restart_phase` — Restart current phase with new direction
   - `archive_branch` — Archive this branch and start fresh
   - `scope_change` — Narrow or expand research scope

2. **Rationale** — Ask: "Why is a pivot needed? What evidence supports this?"

3. **Alternative direction** — Ask: "What alternative approach do you propose?"

Then invoke:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/pivot_manager.py" propose \
  --project-root "<current_project>" \
  --pivot-type "<type>" \
  --rationale "<rationale>" \
  --alternative "<alternative>" \
  --affected-phase "<current_phase>"
```

Present the result and confirm: "Pivot proposal created. It requires your explicit approval before execution."

### Step 2b: Review a Pivot

If user selects `review`:

1. Read `.autoresearch/state/research-state.yaml` and list all entries in `pivot_candidates`
2. If no pending pivots: inform user "No pending pivot proposals."
3. If pivots exist: present each with ID, type, rationale, and alternative
4. Ask: "Do you approve or reject this pivot?"

Then invoke:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/pivot_manager.py" review \
  --project-root "<current_project>" \
  --pivot-id "<id>" \
  --decision "<approve|reject>" \
  --note "<user_note>"
```

### Step 2c: List Pivots

Read state and show all entries in `pivot_candidates` and related entries in `human_decisions`.

## Pivot Safety Rules

1. **Human approval is mandatory** — No pivot executes without explicit user consent
2. **State is preserved** — Pivots update phase pointers but do not delete artifacts
3. **Artifacts archived** — Before a pivot executes, existing phase artifacts remain in place
4. **Logged permanently** — All pivot proposals and decisions are recorded in `human_decisions`

## When Pivots Are Triggered

Pivots may be proposed by:
- The orchestrator, when gate evaluation consistently fails
- An agent (Survey, Code), when evidence contradicts the hypothesis
- The user, when they want to change direction

## Relationship to Other Commands

- **`/status`** — Shows if a pivot is pending in the `active_blocker` field
- **`/configure`** — Adjust settings without changing research direction
- **Phase commands** — Resume normal flow after pivot approval/rejection
