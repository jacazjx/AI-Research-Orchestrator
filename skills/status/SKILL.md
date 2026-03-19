---
name: airesearchorchestrator:status
agent: orchestrator
description: "Show live research project status: phase progress, gate scores, blockers, and next-action recommendation. Use when user says 'status', '查看状态', '项目状态', 'show status', 'current status'. Safe to run at any time without changing state."
argument-hint: [--project-root /path/to/project] [--verbose] [--json]
allowed-tools: Read, Bash, Glob, Grep
---

# Show Project Status

Displays a live snapshot of the current research project without changing any state. Safe to run at any time.

## When to Use

- Opening a session and wanting a quick orientation before running `/reload`
- After a phase completes, to confirm gate readiness before requesting advancement
- When unsure what to do next
- Checking progress mid-session

## Workflow

```
/status
    │
    ├─→ 1. Locate project root
    │       └─→ Find .autoresearch/ directory
    │
    ├─→ 2. Read current state
    │       ├─→ status.json
    │       ├─→ research-state.yaml
    │       └─→ phase deliverables
    │
    ├─→ 3. Calculate gate scores
    │       ├─→ Evidence completeness
    │       ├─→ Review readiness
    │       └─→ Human gate status
    │
    ├─→ 4. Identify blockers
    │       └─→ Missing deliverables, pending reviews
    │
    └─→ 5. Output status report
            ├─→ Phase progress
            ├─→ Gate scores
            ├─→ Blockers
            └─→ Next actions
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

## Hard Rules

1. **Read-only operation** - Never modify project state
2. **Show actionable info** - Always include next actions
3. **Highlight blockers** - Make impediments visible
4. **Gate score accuracy** - Calculate from actual deliverables

## Related Skills

- [reload](./reload/) — Restores full session context at session start
- [orchestrator](../orchestrator/SKILL.md) — Main orchestration skill