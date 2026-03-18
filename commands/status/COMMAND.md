---
name: status
description: "Show live research project status: phase progress, gate scores, blockers, and next-action recommendation"
script: scripts/run_status.py
triggers:
  - "status"
  - "查看状态"
  - "项目状态"
  - "show status"
  - "current status"
phase: any
agents: []
arguments:
  required:
    - name: project-root
      description: Absolute path to the research project root directory
      type: path
  optional:
    - name: verbose
      description: Include missing/existing deliverable lists
      type: boolean
      default: false
    - name: json
      description: Output JSON format
      type: boolean
      default: false
---

# Show Project Status

Displays a live snapshot of the current research project without changing any state. Safe to run at any time.

## When to Use

- Opening a session and wanting a quick orientation before running `/reload`
- After a phase completes, to confirm gate readiness before requesting advancement
- When unsure what to do next

## Usage

```bash
# Standard status snapshot
python3 scripts/run_status.py --project-root /abs/path/to/project

# Verbose (includes deliverable lists)
python3 scripts/run_status.py --project-root /abs/path/to/project --verbose

# JSON output (for scripting)
python3 scripts/run_status.py --project-root /abs/path/to/project --json
```

## Output Example

```
## Research Project Status

**Phase:** Pilot  |  **Gate:** gate_2  |  **Loops:** 1/3

**Progress:** Survey → [Pilot] → Experiments → Paper → Reflection

### Gate Scores
  Evidence completeness :  40%
  Review readiness      :   0%
  Human gate            :   0%

**Decision:** 🔄 Revise — complete missing work before advancing

### Blockers
  • Required deliverables are missing
  • Phase review status: pending

### Next Actions
1. Complete pilot experiment design
2. Request Adviser review
3. Await Gate 2 human approval
```

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
