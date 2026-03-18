---
name: airesearchorchestrator:status
description: "Show live research project status: phase progress, gate scores, blockers, and next-action recommendation"
argument-hint: "[--project-root <path>] [--verbose] [--json]"
allowed-tools: "Read, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Show Project Status

Displays a live snapshot of the current research project without changing any state. Safe to run at any time.

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_status.py" $ARGUMENTS
```

## Usage

```bash
# Standard status snapshot
python3 scripts/run_status.py --project-root /abs/path/to/project

# Verbose (includes deliverable lists)
python3 scripts/run_status.py --project-root /abs/path/to/project --verbose

# JSON output (for scripting)
python3 scripts/run_status.py --project-root /abs/path/to/project --json
```

## When to Use

- Opening a session and wanting a quick orientation before running `/reload`
- After a phase completes, to confirm gate readiness before requesting advancement
- When unsure what to do next

## Gate Score Interpretation

| Evidence | Review | Human Gate | Decision |
|----------|--------|------------|----------|
| 100% | 100% | 100% | ✅ Advance |
| 100% | 100% | 0% | 🔄 Revise (awaiting your approval) |
| < 100% | any | any | 🔄 Revise (deliverables incomplete) |
| any | pivot | any | ⚠️ Pivot |
| any | any | any (loop maxed) | 🔔 Escalate |

## Relationship to Other Commands

- **`/reload`** — restores full session context; use at the start of a new session
- **`/status`** — shows live gate state; use mid-session to check progress