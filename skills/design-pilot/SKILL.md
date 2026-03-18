---
name: airesearchorchestrator:design-pilot
description: Design minimal pilot experiment to validate core hypothesis. Use when user says "design pilot", "pilot experiment", "设计 Pilot", or needs to create a small-scale validation experiment.
user-invocable: false
argument-hint: [problem-analysis-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
## Purpose

Design a minimal, fast pilot experiment that validates the core hypothesis with minimal resources.

## Workflow

### Step 1: Review Problem Analysis

Read `docs/reports/pilot/problem-analysis.md` for:
- Core challenge
- Solution approach
- Success metrics

### Step 2: Define Pilot Scope

Minimize scope while preserving validity:
- Smallest dataset that demonstrates concept
- Simplified model/architecture
- Key hyperparameters to test
- Quick evaluation metrics

### Step 3: Design Implementation

Specify:
- Code structure
- Data pipeline
- Training procedure
- Evaluation protocol

### Step 4: Define Success Criteria

Set clear criteria:
- Minimum acceptable performance
- Key metrics to observe
- Go/No-Go thresholds
- Early stopping conditions

### Step 5: Resource Planning

Estimate:
- Compute time (should be < 24 hours)
- Data preparation time
- Debugging buffer

## Output

Save to `docs/reports/pilot/pilot-design.md`:

```markdown
# Pilot Design

## Objective
[What this pilot validates and why it's sufficient]

## Minimal Implementation

### Data
- Dataset: [name, size, subset]
- Preprocessing: [minimal steps]
- Splits: [train/val/test]

### Model/Method
- Architecture: [simplified version]
- Key components: [essential parts only]
- Hyperparameters: [initial values]

### Training
- Framework: [PyTorch/TensorFlow/etc.]
- Optimizer: [type, learning rate]
- Batch size: [value]
- Training steps/epochs: [minimal for validation]

## Evaluation Protocol

| Metric | How to Compute | Success Threshold |
|--------|----------------|-------------------|
| ...    | ...            | ...               |

## Success Criteria

### Go Criteria
- [Criterion 1]: Must achieve X
- [Criterion 2]: Must show Y pattern

### No-Go Criteria
- [Criterion]: Would indicate fundamental issue

## Timeline

| Task | Duration | Notes |
|------|----------|-------|
| Data prep | X hours | ... |
| Implementation | X hours | ... |
| Debugging | X hours | ... |
| Training | X hours | ... |
| Analysis | X hours | ... |
| **Total** | **X hours** | |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Implementation issues | [Plan] |
| Poor initial results | [Debugging steps] |

## Code Outline

```
[pseudo-code or file structure]
```
```

## Key Rules

- Pilot must complete in < 24 hours
- Must test core hypothesis directly
- Success criteria must be unambiguous
- Include rollback plan if pilot fails