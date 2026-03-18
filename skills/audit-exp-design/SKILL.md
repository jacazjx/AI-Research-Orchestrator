---
name: airesearchorchestrator:audit-exp-design
description: Audit experiment design for statistical validity, baseline completeness, and resource adequacy. Use when user says "audit experiment design", "review exp design", "审核实验设计", or needs to verify full experiment planning.
user-invocable: false
argument-hint: [experiment-spec-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
## Purpose

Critically review full experiment design for statistical rigor and completeness.

## Workflow

### Step 1: Review Experiment Spec

Read `docs/reports/experiments/experiment-spec.md` for matrix, hyperparameters, and evaluation.

### Step 2: Assess Statistical Validity

Evaluate:
- Sufficient seeds (minimum 3)
- Appropriate statistical tests
- Significance thresholds defined
- Multiple comparison corrections

### Step 3: Evaluate Experiment Matrix

Check:
- Main experiments test core claims
- Ablations cover key components
- Baselines include strong and weak
- Sensitivity analysis appropriate

### Step 4: Review Hyperparameters

Assess:
- Search spaces appropriate
- Sampling strategy sound
- Computational budget feasible

### Step 5: Validate Resource Estimates

Check:
- GPU hours realistic
- Timeline includes buffer
- Storage adequate

## Output

```markdown
# Experiment Design Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Statistical Rigor**: X/10
- **Baseline Completeness**: X/10

## Statistical Validity

| Criterion | Status | Notes |
|-----------|--------|-------|
| Minimum seeds (>=3) | Yes/No | N seeds |
| Statistical tests defined | Yes/No | [Which tests] |
| Significance threshold | Yes/No | alpha = X |
| Multiple comparison correction | Yes/No | [Method] |

**Statistical Issues**:
- [Issue]

## Experiment Matrix Review

### Main Experiments

| Exp ID | Tests Core Claim? | Adequate? | Notes |
|--------|-------------------|-----------|-------|
| M1 | Yes/No | Yes/No | |

### Ablation Studies

| Exp ID | Component Tested | Necessary? | Adequate? |
|--------|------------------|------------|-----------|
| A1 | [Component] | Yes/No | Yes/No |

### Baseline Comparisons

| Baseline | Type | Appropriate? | Missing? |
|----------|------|--------------|----------|
| B1 | Strong/Weak | Yes/No | |

**Missing Baselines**:
- [Baseline that should be included]

## Hyperparameter Review

| Parameter | Range | Sampling | Appropriate? |
|-----------|-------|----------|--------------|
| lr | [range] | [method] | Yes/No |

**Hyperparameter Concerns**:
- [Concern]

## Resource Estimates

| Resource | Estimated | Auditor Estimate | Variance |
|----------|-----------|------------------|----------|
| GPU hours | X | Y | +/-Z |
| Timeline | X days | Y days | |
| Storage | X GB | Y GB | |

**Resource Concerns**:
- [Concern]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Experiment design is rigorous, proceed
- [ ] PASS_WITH_FIXES - Minor issues, address and proceed
- [ ] REVISE - Significant gaps in design
- [ ] BLOCK - Statistical validity compromised
```

## Key Rules

- Less than 3 seeds is a critical issue
- Must include strong baselines
- Must have multiple comparison correction
- Resource estimates need 20% buffer