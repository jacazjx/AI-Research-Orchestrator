---
name: airesearchorchestrator:experiment-design
agent: coder
description: "Design experiments at pilot or full scale. Scope adapts to current phase: pilot phase produces a minimal validation experiment (< 24hr), experiments phase produces a comprehensive matrix with ablations, baselines, and statistical rigor. Use when user says \"design pilot\", \"design experiments\", \"设计 Pilot\", \"设计实验\"."
user-invocable: false
argument-hint: [problem-analysis-or-pilot-results-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
# Experiment Design

## Purpose

Design experiments at the appropriate scale for the current phase. The agent decides scope, structure, and detail level based on context.

## Mode Selection

| Phase | Mode | Input | Output | Time Budget |
|-------|------|-------|--------|-------------|
| Pilot | Minimal Pilot Design | `docs/pilot/problem-analysis.md` | `docs/pilot/pilot-design.md` | < 24 hours |
| Experiments | Full Matrix Design | `docs/pilot/pilot-validation-report.md` | `docs/experiments/experiment-spec.md` | Days-Weeks |

## Statistical Analysis Guide

Use these standards when designing the evaluation protocol:

### Significance Tests

| Scenario | Recommended Test |
|----------|-----------------|
| Two models, same test set | Paired t-test (alpha = 0.05) |
| Multiple models compared | ANOVA + Bonferroni correction |
| Non-normal distributions | Wilcoxon signed-rank test |
| Multiple hypotheses | Apply Bonferroni or Holm-Bonferroni correction |

### Effect Size

- **Cohen's d** for pairwise comparisons: small (0.2), medium (0.5), large (0.8)
- Report alongside p-values -- statistical significance without practical significance is misleading

### Result Reporting Format

```
Mean +/- std across N seeds (N >= 3)
95% confidence intervals
p-values for key comparisons
Effect size (Cohen's d)
```

### Power Analysis (Full Matrix)

Before committing resources, estimate required sample size:
- Desired power: 0.8 (standard) or 0.9 (for key claims)
- Expected effect size: estimate from pilot results
- Significance level: 0.05

## Key Rules

1. **Pilot must complete in < 24 hours** -- scope ruthlessly
2. **Success criteria must be unambiguous** -- measurable, with clear thresholds
3. **Minimum 3 seeds per configuration** for statistical validity
4. **Must include both strong AND weak baselines** in full matrix
5. **Resource estimates need 20% buffer** minimum
6. **Multiple comparison corrections required** when testing multiple hypotheses
7. **Include rollback plan if pilot fails**
