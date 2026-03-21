---
name: airesearchorchestrator:experiment-design
agent: coder
description: Unified experiment design skill covering both pilot (minimal, <24hr) and full experiment matrix design. The agent decides scope based on current phase -- pilot phase produces a minimal validation experiment, experiments phase produces a comprehensive matrix with ablations, baselines, and statistical rigor. Use when user says "design pilot", "design experiments", "pilot experiment", "experiment matrix", "设计 Pilot", "设计实验", or needs to plan experiments at any scale.
user-invocable: false
argument-hint: [problem-analysis-or-pilot-results-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
# Experiment Design

## Overview

A unified experiment design skill that adapts its scope based on the current phase. During the pilot phase, it produces a minimal experiment to validate the core hypothesis quickly (< 24 hours). During the experiments phase, it produces a comprehensive experiment matrix with ablations, baselines, hyperparameter ranges, and full statistical rigor.

## Purpose

- Design experiments at the appropriate scale for the current phase
- Ensure statistical validity and reproducibility from the start
- Define clear success criteria and Go/No-Go thresholds
- Produce resource estimates with appropriate buffers
- Create specifications that support quality gate evaluation

## Mode Selection

| Phase | Mode | Input | Output | Time Budget |
|-------|------|-------|--------|-------------|
| Pilot | Minimal Pilot Design | `docs/pilot/problem-analysis.md` | `docs/pilot/pilot-design.md` | < 24 hours |
| Experiments | Full Matrix Design | `docs/pilot/pilot-validation-report.md` | `docs/experiments/experiment-spec.md` | Days-Weeks |

---

## Pilot Design Mode

Design a minimal, fast experiment that validates the core hypothesis with minimal resources.

### Step 1: Review Problem Analysis

Read `docs/pilot/problem-analysis.md` for core challenge, solution approach, and success metrics.

### Step 2: Define Pilot Scope

Minimize scope while preserving validity:
- Smallest dataset that demonstrates the concept
- Simplified model/architecture
- Key hyperparameters to test
- Quick evaluation metrics

### Step 3: Design Implementation

Specify:
- **Code structure**: File organization and key modules
- **Data pipeline**: Dataset, preprocessing, train/val/test splits
- **Training procedure**: Framework, optimizer, learning rate, batch size, training steps
- **Evaluation protocol**: Metrics, how to compute, success thresholds

### Step 4: Define Success Criteria

Set clear, unambiguous criteria:

**Go Criteria**:
- [Criterion]: Must achieve X
- [Criterion]: Must show Y pattern

**No-Go Criteria**:
- [Criterion]: Would indicate fundamental issue

**Early stopping conditions**: When to terminate early.

### Step 5: Resource Planning

| Task | Duration | Notes |
|------|----------|-------|
| Data prep | X hours | |
| Implementation | X hours | |
| Debugging | X hours | Buffer |
| Training | X hours | |
| Analysis | X hours | |
| **Total** | **< 24 hours** | |

### Step 6: Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Implementation issues | [Fallback plan] |
| Poor initial results | [Debugging steps] |
| Resource constraints | [Reduced scope option] |

### Pilot Design Output

Save to `docs/pilot/pilot-design.md`:

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
| ... | ... | ... |

## Success Criteria

### Go Criteria
- [Criterion 1]: Must achieve X
- [Criterion 2]: Must show Y pattern

### No-Go Criteria
- [Criterion]: Would indicate fundamental issue

## Timeline

| Task | Duration | Notes |
|------|----------|-------|
| Total | < 24 hours | |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| ... | ... |

## Code Outline
[Pseudo-code or file structure]
```

---

## Full Matrix Design Mode

Design a comprehensive experiment matrix based on pilot results.

### Step 1: Review Pilot Results

Read `docs/pilot/pilot-validation-report.md` for validated approach, key hyperparameters, and lessons learned.

### Step 2: Define Experiment Categories

| Category | Purpose | Examples |
|----------|---------|---------|
| Main experiments | Core claim validation | Full-scale training, main comparisons |
| Ablation studies | Component contribution | Remove/replace key components |
| Baseline comparisons | Competitive positioning | Strong and weak baselines |
| Sensitivity analysis | Robustness | Vary key parameters |

### Step 3: Design Experiment Matrix

For each experiment:
- **Independent variables**: What to vary
- **Dependent variables**: What to measure
- **Control variables**: What to keep constant
- **Sample size**: Number of runs (minimum 3 seeds)

### Step 4: Specify Hyperparameters

| Parameter | Type | Range/Values | Sampling |
|-----------|------|--------------|----------|
| lr | float | [1e-5, 1e-3] | log-uniform |
| batch_size | int | {16, 32, 64} | grid |
| ... | ... | ... | ... |

### Step 5: Define Evaluation Protocol

#### Primary Metrics

| Metric | Description | Target | Comparison |
|--------|-------------|--------|------------|
| ... | ... | ... | ... |

#### Statistical Analysis

- **Significance tests**: Paired t-test (alpha = 0.05)
- **Multiple comparison correction**: Bonferroni correction
- **Effect size**: Cohen's d
- **Result reporting**: Mean +/- std across N seeds, 95% CI, p-values

### Step 6: Resource Estimation

| Resource | Estimated | With 20% Buffer |
|----------|-----------|-----------------|
| Total experiments | X | |
| Hours per run | Y | |
| GPU type | [model] | |
| Total GPU hours | Z | Z * 1.2 |
| Storage | X GB | X * 1.2 GB |

### Full Matrix Output

Save to `docs/experiments/experiment-spec.md`:

```markdown
# Experiment Specification

## Overview
[Summary of goals and structure]

## Experiment Matrix

### Main Experiments
| Exp ID | Configuration | Purpose | Runs |
|--------|---------------|---------|------|
| M1 | [config] | [purpose] | N seeds |

### Ablation Studies
| Exp ID | Component Removed | Expected Impact | Runs |
|--------|-------------------|-----------------|------|
| A1 | [component] | [expected] | N seeds |

### Baseline Comparisons
| Baseline | Method | Expected Gap | Runs |
|----------|--------|--------------|------|
| B1 | [method] | [expected] | N seeds |

### Sensitivity Analysis
| Parameter | Values | Reason | Runs |
|-----------|--------|--------|------|
| S1 | [values] | [reason] | N seeds |

## Hyperparameter Ranges

| Parameter | Type | Range/Values | Sampling |
|-----------|------|--------------|----------|
| ... | ... | ... | ... |

## Evaluation Metrics

### Primary Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| ... | ... | ... |

### Secondary Metrics
| Metric | Description |
|--------|-------------|
| ... | ... |

## Statistical Analysis

### Significance Tests
- Primary: Paired t-test (alpha = 0.05)
- Multiple comparisons: Bonferroni correction
- Effect size: Cohen's d

### Result Reporting
- Mean +/- std across N seeds
- 95% confidence intervals
- p-values for key comparisons

## Resource Requirements

### Compute
- Total experiments: X
- Hours per run: Y
- GPU type: [model]
- Total GPU hours: Z (with 20% buffer: Z')

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
```

---

## Key Rules

1. **Pilot must complete in < 24 hours** -- scope ruthlessly
2. **Must test core hypothesis directly** -- no tangential experiments in pilot
3. **Success criteria must be unambiguous** -- measurable, with clear thresholds
4. **Include rollback plan if pilot fails**
5. **Must include statistical power analysis** for full matrix
6. **Minimum 3 seeds per configuration** for statistical validity
7. **Must include both strong AND weak baselines** in full matrix
8. **Resource estimates need 20% buffer** minimum
9. **Hyperparameter search spaces must be appropriate** -- not too narrow or too wide
10. **Multiple comparison corrections required** when testing multiple hypotheses
