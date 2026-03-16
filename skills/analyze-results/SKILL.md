---
name: airesearchorchestrator:analyze-results
description: Analyze ML experiment results, compute statistics, generate comparison tables and insights. Use when user says "analyze results", "compare", or needs to interpret experimental data.
argument-hint: [results-path-or-description]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent
agent: code
---

## Workflow

### Step 1: Locate Results

Find JSON/CSV result files in `figures/`, `results/`, or output directories.

### Step 2: Build Comparison Table

Organize by:
- Independent variables
- Dependent variables
- Delta vs baseline

### Step 3: Statistical Analysis

- Report mean ± std for multiple seeds
- Identify parameter trends
- Flag outliers

### Step 4: Generate Insights

Structure as:
- Observation
- Interpretation
- Implication
- Next step

### Step 5: Update Documentation

Draft finding statements for project notes.