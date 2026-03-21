# Rollback Policy

This document defines how deliverables are handled when a Gate rejection causes a rollback to an earlier phase.

## Overview

When a Gate is rejected and the researcher chooses to roll back to an earlier phase, the system must handle the deliverables created during the current and intermediate phases.

## Default Policy

| Action | Behavior |
|--------|----------|
| Archive | Deliverables are copied to `.autoresearch/archive/<phase>-<timestamp>/` |
| Delete | Original files are preserved (not deleted) |
| State Reset | `research-state.yaml` is reset by `reset_state_for_phase()` |

## Rollback Scenarios

### Scenario 1: Same-Phase Revision (REVISE)

When Gate rejects with "revise" decision:
- No phase change
- No file archival needed
- Continue iterating with feedback

### Scenario 2: Rollback to Earlier Phase (ROLLBACK)

When rolling back from phase N to phase M (M < N):

1. **Archive intermediate deliverables**
   - All deliverables from phases M+1 through N are archived
   - Timestamp and reason recorded in `archive-metadata.json`

2. **State reset**
   - `reset_state_for_phase()` resets gate approvals and review status
   - Loop counters for affected phases are reset

3. **File preservation**
   - Original files remain in place
   - Researchers can reference or restore from archive

### Scenario 3: Pivot (PIVOT)

When choosing a fundamentally different direction:
- Archive all current phase deliverables
- Reset to survey phase for new direction
- Previous work remains in archive for reference

## Archive Structure

```
.autoresearch/archive/
├── experiments-20260320-143000/
│   ├── results-summary.md
│   ├── evidence-package-index.md
│   └── archive-metadata.json
├── paper-20260321-100000/
│   ├── paper-draft.md
│   └── archive-metadata.json
└── archive-index.md
```

## Archive Metadata Format

```json
{
  "phase": "experiments",
  "reason": "gate_rejection",
  "timestamp": "2026-03-20T14:30:00Z",
  "files": [
    {
      "original": "docs/experiments/results-summary.md",
      "archived": ".autoresearch/archive/experiments-20260320-143000/results-summary.md"
    }
  ]
}
```

## Integration with reset_state_for_phase()

The `reset_state_for_phase()` function handles state reset.
The `archive_phase_deliverables()` function handles file archival.

Call sequence on rollback:

```python
from orchestrator_common import reset_state_for_phase
from phase_rollback import archive_phase_deliverables

# 1. Archive deliverables from phases being rolled back
for phase in phases_to_archive:
    archive_phase_deliverables(project_root, phase)

# 2. Reset state
reset_state_for_phase(state, target_phase)
```

## Configuration

Rollback policy can be customized in `orchestrator-config.yaml`:

```yaml
rollback:
  default_policy:
    archive: true
    delete: false
  phase_overrides:
    paper:
      archive: true
      delete: false  # Never auto-delete paper drafts
```
