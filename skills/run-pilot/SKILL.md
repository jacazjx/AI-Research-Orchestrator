---
name: autoresearch:run-pilot
agent: code
description: Execute pilot experiment and report results. Use when user says "run pilot", "execute pilot", "运行 Pilot", or needs to run the designed pilot experiment.
argument-hint: [pilot-design-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

## Purpose

Execute the pilot experiment, collect results, and determine if the hypothesis is validated.

## Workflow

### Step 1: Prepare Environment

- Verify dependencies installed
- Check GPU availability
- Prepare data

### Step 2: Implement Pilot

Follow pilot design:
- Write minimal code
- Add logging
- Create checkpoints

### Step 3: Execute

Run experiment:
- Monitor progress
- Log key metrics
- Save intermediate results

### Step 4: Collect Results

Gather:
- Training curves
- Final metrics
- Error cases
- Resource usage

### Step 5: Analyze and Report

Interpret results:
- Compare to success criteria
- Identify issues
- Extract lessons learned

## Output

Save to `docs/reports/pilot/pilot-validation-report.md`:

```markdown
# Pilot Validation Report

## Executive Summary
[One paragraph: hypothesis validated or not, key findings]

## Implementation Details

### What Was Implemented
- [Component 1]: [brief description]
- [Component 2]: [brief description]

### Deviations from Design
| Planned | Actual | Reason |
|---------|--------|--------|
| ...     | ...    | ...    |

## Results

### Quantitative Results

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| ...    | ...    | ...      | Pass/Fail |

### Training Curves
[Description or link to figures]

### Qualitative Observations
- [Observation 1]
- [Observation 2]

## Analysis

### What Worked
- [Finding 1]
- [Finding 2]

### What Didn't Work
- [Issue 1]
- [Issue 2]

### Root Cause Analysis
[For any issues encountered]

## Decision

### Hypothesis Status
- [ ] VALIDATED - Proceed to full experiments
- [ ] PARTIALLY VALIDATED - Minor adjustments needed
- [ ] NOT VALIDATED - Major revision required

### Recommendation
[Go/No-Go with rationale]

## Lessons Learned

### Technical Lessons
1. [Lesson 1]
2. [Lesson 2]

### Process Lessons
1. [Lesson 1]
2. [Lesson 2]

## Next Steps
[If Go: prepare for full experiments]
[If No-Go: what needs to change]

## Reproducibility

### Code Location
[Path to pilot code]

### Commands to Reproduce
```bash
[exact commands used]
```

### Random Seeds
[Seeds used for reproducibility]
```

## Key Rules

- Document ALL deviations from design
- Report negative results honestly
- Include reproducibility information
- Make clear Go/No-Go recommendation