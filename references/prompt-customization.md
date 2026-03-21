# Prompt Customization Protocol

Use fixed prompt templates for each role, but never launch a role with the raw template alone.

## Rule

- The user-facing orchestrator agent remains the only agent that talks directly to the user.
- Before launching a role, the orchestrator must:
  - inspect the current project state
  - identify the current stage objective
  - choose the right fixed role template
  - inject task-specific constraints, required inputs, and must-read files
- The rendered prompt is a role-specific brief, not a replacement for orchestration.

## Rendering path

- Agent role definitions live in `agents/<role>/AGENT.md`.
- Agent behavior is defined in `agents/<role>/AGENT.md` files.
- The orchestrator may further edit or append to the rendered prompt before using it.

## What the orchestrator should customize

- The exact task summary for the current loop
- The current objective for this invocation
- Which files are mandatory to read before acting
- Which user constraints override defaults
- Which failure mode, risk, or reviewer finding the role must focus on

## What should stay fixed in the template

- Role identity and boundary
- Phase-specific hard rules
- Evidence discipline
- Gate discipline
- AI-Researcher-derived task structure
