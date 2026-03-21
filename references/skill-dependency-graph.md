# Skill Dependency Graph

This document defines the recommended skill invocation order for each agent in the five-phase research workflow.

## Survey Agent

### Workflow 1: Full Ideation to Survey

```
insight → problem-analysis → theoretical-derivation → literature → ideation
```

### Workflow 2: Quick Survey (Well-defined Idea)

```
problem-analysis → literature → ideation
```

### Workflow 3: Theory-First Survey

```
problem-analysis → theoretical-derivation → literature → ideation
```

## Critic Agent

### Audit Workflow

```
audit (survey scope) → audit (derivation scope) → audit (citation scope)
```

## Code Agent (Pilot)

### Workflow 1: Pilot Validation

```
problem-analysis → experiment-design → run-pilot → analyze-results
```

### Workflow 2: Quick Pilot

```
experiment-design → run-pilot
```

## Code Agent (Experiments)

### Workflow 1: Full Experiments

```
experiment-design → run-experiment → monitor-experiment → analyze-results
```

### Workflow 2: Extended Experiments

```
experiment-design → run-experiment → monitor-experiment → run-experiment → analyze-results
```

## Adviser Agent (Pilot/Experiments)

### Audit Workflow

```
audit (design scope) → audit (pilot scope) → audit (experiment-design scope) → audit (results scope)
```

## Writer Agent

### Workflow 1: Full Paper Writing

```
paper-plan → paper-write → paper-figure → citation → paper-compile
```

### Workflow 2: Quick Paper Draft

```
paper-plan → paper-write → paper-compile
```

## Reviewer Agent

### Audit Workflow

```
audit (paper scope) → audit (citation scope) → audit (paper-plan scope)
```

## Reflector Agent

### Workflow 1: Full Reflection

```
extract-lessons → propose-overlay
```

## Curator Agent

### Audit Workflow

```
audit (lessons scope) → audit (overlay scope)
```

## Dependencies Between Skills

### Critical Dependencies (Must Follow Order)

| From | To | Reason |
|------|----|--------|
| `problem-analysis` | `theoretical-derivation` | Need formalized idea before derivation |
| `theoretical-derivation` | `literature` | Need theory scope to search literature |
| `literature` | `ideation` | Need literature to verify novelty |
| `problem-analysis` | `experiment-design` | Need problem analysis to design experiments |
| `experiment-design` | `run-pilot` | Need design before execution |
| `experiment-design` | `run-experiment` | Need experiment design before running |
| `run-experiment` | `monitor-experiment` | Need running experiments to monitor |
| `paper-plan` | `paper-write` | Need outline before writing |
| `paper-write` | `paper-figure` | Need text to know what figures to create |
| `extract-lessons` | `propose-overlay` | Need lessons before proposing changes |

### Optional Dependencies (Can Skip or Reorder)

| From | To | Condition |
|------|----|-----------|
| `insight` | `problem-analysis` | Skip if idea is already clear |
| `theoretical-derivation` | `literature` | Skip for applied research |
| `run-pilot` | `analyze-results` | Skip if pilot is simple |
| `paper-figure` | `paper-compile` | Skip if no figures needed |
