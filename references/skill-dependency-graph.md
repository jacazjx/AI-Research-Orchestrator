# Skill Dependency Graph

This document defines the recommended skill invocation order for each agent in the five-phase research workflow.

## Survey Agent

### Workflow 1: Full Ideation to Survey

```
research-intent-clarification → define-idea → theoretical-derivation → literature-survey → novelty-check
```

### Workflow 2: Quick Survey (Well-defined Idea)

```
define-idea → research-lit → novelty-check
```

### Workflow 3: Theory-First Survey

```
define-idea → theoretical-derivation → literature-survey → novelty-check
```

## Critic Agent

### Audit Workflow

```
audit-survey → audit-derivation → audit-citation
```

## Code Agent (Pilot)

### Workflow 1: Pilot Validation

```
validate-problem → analyze-problem → design-pilot → run-pilot → analyze-results
```

### Workflow 2: Quick Pilot

```
design-pilot → run-pilot
```

## Code Agent (Experiments)

### Workflow 1: Full Experiments

```
design-exp → run-experiment → monitor-experiment → analyze-results
```

### Workflow 2: Extended Experiments

```
design-exp → run-experiment → monitor-experiment → run-experiment → analyze-results
```

## Adviser Agent (Pilot/Experiments)

### Audit Workflow

```
audit-design → audit-pilot → audit-exp-design → audit-results
```

## Writer Agent

### Workflow 1: Full Paper Writing

```
paper-plan → paper-write → paper-figure → curate-citation → paper-compile
```

### Workflow 2: Quick Paper Draft

```
paper-plan → paper-write → paper-compile
```

## Reviewer Agent

### Audit Workflow

```
audit-paper → audit-citation → audit-paper-plan
```

## Reflector Agent

### Workflow 1: Full Reflection

```
extract-lessons → propose-overlay
```

## Curator Agent

### Audit Workflow

```
audit-lessons → audit-overlay
```

## Dependencies Between Skills

### Critical Dependencies (Must Follow Order)

| From | To | Reason |
|------|----|--------|
| `define-idea` | `theoretical-derivation` | Need formalized idea before derivation |
| `theoretical-derivation` | `literature-survey` | Need theory scope to search literature |
| `literature-survey` | `novelty-check` | Need literature to verify novelty |
| `validate-problem` | `analyze-problem` | Need problem validation before analysis |
| `analyze-problem` | `design-pilot` | Need problem analysis to design pilot |
| `design-pilot` | `run-pilot` | Need design before execution |
| `design-exp` | `run-experiment` | Need experiment design before running |
| `run-experiment` | `monitor-experiment` | Need running experiments to monitor |
| `paper-plan` | `paper-write` | Need outline before writing |
| `paper-write` | `paper-figure` | Need text to know what figures to create |
| `extract-lessons` | `propose-overlay` | Need lessons before proposing changes |

### Optional Dependencies (Can Skip or Reorder)

| From | To | Condition |
|------|----|-----------|
| `research-intent-clarification` | `define-idea` | Skip if idea is already clear |
| `theoretical-derivation` | `literature-survey` | Skip for applied research |
| `run-pilot` | `analyze-results` | Skip if pilot is simple |
| `paper-figure` | `paper-compile` | Skip if no figures needed |
