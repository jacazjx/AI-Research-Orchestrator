---
name: airesearchorchestrator:design-exp
agent: code
description: Design full experiment matrix with hyperparameter ranges, evaluation metrics, and statistical tests. Use when user says "design experiments", "experiment matrix", "设计实验", or needs to plan comprehensive experiments.
argument-hint: [pilot-validation-report-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Design a comprehensive experiment matrix based on pilot results, with proper hyperparameter ranges, baselines, and statistical rigor.

## Workflow

### Step 1: Review Pilot Results

Read `docs/reports/pilot/pilot-validation-report.md` for:
- Validated approach
- Key hyperparameters
- Lessons learned

### Step 2: Define Experiment Categories

Organize experiments:
- Main experiments (core claim validation)
- Ablation studies (component contribution)
- Baseline comparisons (competitive positioning)
- Sensitivity analysis (robustness)

### Step 3: Design Experiment Matrix

For each experiment:
- Independent variables (what to vary)
- Dependent variables (what to measure)
- Control variables (what to keep constant)
- Sample size (number of runs)

### Step 4: Specify Hyperparameters

Define:
- Search space for each hyperparameter
- Sampling strategy (grid, random, Bayesian)
- Number of seeds for statistical validity

### Step 5: Define Evaluation Protocol

Specify:
- Primary metrics
- Secondary metrics
- Statistical tests (t-test, bootstrap, etc.)
- Significance threshold (p < 0.05)

### Step 6: Resource Estimation

Calculate:
- Total GPU hours
- Wall-clock time
- Storage requirements

## Output

Save to `docs/reports/experiments/experiment-spec.md`:

```markdown
# Experiment Specification

## Overview
[Summary of experiment goals and structure]

## Experiment Matrix

### Main Experiments

| Exp ID | Configuration | Purpose | Runs |
|--------|---------------|---------|------|
| M1 | [config] | [purpose] | N seeds |
| M2 | [config] | [purpose] | N seeds |

### Ablation Studies

| Exp ID | Component Removed | Expected Impact | Runs |
|--------|-------------------|-----------------|------|
| A1 | [component] | [expected] | N seeds |

### Baseline Comparisons

| Baseline | Method | Expected Gap | Runs |
|----------|--------|--------------|------|
| B1 | [method] | [expected] | N seeds |

### Sensitivity Analysis

| Parameter | Values to Test | Reason | Runs |
|-----------|----------------|--------|------|
| S1 | [values] | [reason] | N seeds |

## Hyperparameter Ranges

| Parameter | Type | Range/Values | Sampling |
|-----------|------|--------------|----------|
| lr | float | [1e-5, 1e-3] | log-uniform |
| batch_size | int | {16, 32, 64} | grid |
| ... | ... | ... | ... |

## Evaluation Metrics

### Primary Metrics
| Metric | Description | Target | Comparison |
|--------|-------------|--------|------------|
| ...    | ...         | ...    | ...        |

### Secondary Metrics
| Metric | Description | Use Case |
|--------|-------------|----------|
| ...    | ...         | ...      |

## Statistical Analysis

### Significance Tests
- Primary: Paired t-test (alpha = 0.05)
- Multiple comparisons: Bonferroni correction
- Effect size: Cohen's d

### Result Reporting
- Mean ± std across N seeds
- 95% confidence intervals
- p-values for key comparisons

## Resource Requirements

### Compute
- Total experiments: X
- Hours per run: Y
- GPU type: [model]
- **Total GPU hours: Z**

### Timeline
| Phase | Experiments | Duration |
|-------|-------------|----------|
| Main | X | Y days |
| Ablation | X | Y days |
| Baselines | X | Y days |
| Analysis | - | Y days |

## Reproducibility Checklist

- [ ] Fixed random seeds documented
- [ ] Software versions pinned
- [ ] Data splits fixed
- [ ] Config files versioned
- [ ] Checkpointing enabled

## Contingency Plans

| Issue | Detection | Response |
|-------|-----------|----------|
| GPU memory overflow | OOM error | Reduce batch size |
| Slow convergence | No improvement after N steps | Adjust learning rate |
| ... | ... | ... |
```

## Key Rules

- Must include statistical power analysis
- Must have at least 3 seeds per configuration
- Must include both strong and weak baselines
- Resource estimate must include 20% buffer