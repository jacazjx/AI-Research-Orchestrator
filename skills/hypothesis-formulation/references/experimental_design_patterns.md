# Experimental Design Patterns

## Table of Contents

- Overview
- Controlled Experiments
- A/B Testing
- Observational Studies
- Simulation Experiments
- Ablation Studies
- Factorial Designs
- Within-Subjects Designs
- Between-Subjects Designs
- Quasi-Experiments
- Design Selection Guide

## Overview

This document provides patterns and templates for designing experiments that test research hypotheses. Each pattern includes when to use it, key components, and example applications.

### Design Selection Criteria

| Factor | Considerations |
|--------|----------------|
| Hypothesis Type | What kind of prediction? |
| Variables | How many IVs and DVs? |
| Resources | Budget, time, participants |
| Control | How much control is possible? |
| Ethics | Are there ethical constraints? |

## Controlled Experiments

### Description

The gold standard for causal inference. Participants/units are randomly assigned to conditions, and the researcher manipulates the independent variable(s) while controlling extraneous variables.

### When to Use

- Testing causal relationships
- Need strong internal validity
- Can randomly assign participants
- Resources allow for control conditions

### Template

```markdown
## Controlled Experiment Design

### Objective
[What causal relationship is being tested]

### Design Type
- [ ] Between-subjects
- [ ] Within-subjects
- [ ] Mixed design

### Independent Variables
| IV | Levels | Manipulation |
|----|--------|--------------|
| IV1 | [level1, level2, ...] | [How manipulated] |
| IV2 | [level1, level2, ...] | [How manipulated] |

### Dependent Variables
| DV | Type | Measurement | Scale |
|----|------|-------------|-------|
| DV1 | Continuous/Categorical | [Method] | [Units] |

### Control Variables
| Variable | Control Method |
|----------|---------------|
| [Variable] | [How controlled] |

### Randomization
- [ ] Random assignment to conditions
- [ ] Random order of trials
- [ ] Counterbalancing: [method]

### Sample
- Size: N = ___
- Power analysis: [effect size, alpha, power]
- Sampling method: [random, convenience, etc.]

### Procedure
1. [Recruitment]
2. [Pre-test measures]
3. [Random assignment]
4. [Intervention]
5. [Post-test measures]
6. [Debriefing]
```

### Example: Testing Learning Rate Effect

```markdown
### Objective
Test whether increasing learning rate reduces convergence time

### Design
Between-subjects controlled experiment

### IV
- Learning rate (0.001, 0.01, 0.1)

### DV
- Convergence time (epochs)

### Controls
- Same architecture
- Same dataset
- Same initialization seed

### Sample
- N = 30 runs per condition
- Power: 0.80 to detect d=0.8
```

## A/B Testing

### Description

Compare two versions (A and B) to determine which performs better on a measured outcome. Common in software development and online experiments.

### When to Use

- Comparing two alternatives
- Large sample available
- Can isolate single variable
- Quick iteration needed

### Template

```markdown
## A/B Test Design

### Objective
[What comparison is being made]

### Variants
| Variant | Description | Change from Control |
|---------|-------------|---------------------|
| A (Control) | [Description] | - |
| B (Treatment) | [Description] | [Specific change] |

### Primary Metric
- Metric: [What is measured]
- Hypothesis: B will [increase/decrease] metric by [X]%

### Secondary Metrics
1. [Metric 1]
2. [Metric 2]

### Sample Size
- Required: N = ___
- Per variant: N = ___
- Calculation based on: [effect size, significance, power]

### Duration
- Start: [Date]
- End: [Date]
- Reason: [traffic, budget, etc.]

### Assignment
- [ ] Random assignment
- [ ] 50/50 split
- [ ] Stratified by: [variables]

### Success Criteria
- Statistical significance: p < ___
- Practical significance: [effect size threshold]
```

### Example: Algorithm Comparison

```markdown
### Objective
Compare Adam vs. SGD optimizer performance

### Variants
- A (Control): SGD with learning rate 0.01
- B (Treatment): Adam with learning rate 0.001

### Primary Metric
- Training loss after 100 epochs

### Sample Size
- N = 100 runs per variant
- Power 0.80, alpha 0.05

### Success Criteria
- p < 0.05
- Effect size > 0.3 (practical significance)
```

## Observational Studies

### Description

Observe and measure variables without manipulation. Useful when experiments are impractical or unethical.

### When to Use

- Cannot manipulate variables
- Natural setting preferred
- Ethical constraints on manipulation
- Exploratory research

### Template

```markdown
## Observational Study Design

### Objective
[What natural relationship is being investigated]

### Study Type
- [ ] Cross-sectional
- [ ] Longitudinal
- [ ] Case-control
- [ ] Cohort

### Variables
| Type | Variable | Measurement |
|------|----------|-------------|
| Predictor | [Variable] | [Method] |
| Outcome | [Variable] | [Method] |
| Confounder | [Variable] | [Method] |

### Sample
- Source: [Where data comes from]
- Size: N = ___
- Selection criteria: [Inclusion/exclusion]

### Data Collection
- Timeframe: [Period]
- Method: [Survey, observation, records]
- Frequency: [Once, repeated]

### Analysis Plan
- Primary analysis: [Statistical method]
- Confounder adjustment: [Method]
- Sensitivity analysis: [Approach]

### Limitations
- Selection bias: [How addressed]
- Confounding: [How addressed]
- Measurement error: [How addressed]
```

### Example: Model Performance Correlation

```markdown
### Objective
Investigate relationship between model size and accuracy

### Study Type
Cross-sectional observational study

### Variables
- Predictor: Model parameter count
- Outcome: Benchmark accuracy
- Confounders: Architecture type, training data

### Sample
- N = 500 models from published papers
- Selection: Papers from 2020-2023

### Analysis
- Regression: accuracy ~ log(params) + architecture
- Control for training data size
```

## Simulation Experiments

### Description

Computational experiments using simulated data or environments. Useful for testing hypotheses about algorithms or systems under controlled conditions.

### When to Use

- Real-world data unavailable
- Need exact control over conditions
- Testing algorithmic hypotheses
- High cost of real experiments

### Template

```markdown
## Simulation Experiment Design

### Objective
[What is being tested through simulation]

### Simulation Environment
- Platform: [Language, framework]
- Model: [What is being simulated]
- Random seed control: [Method]

### Parameters
| Parameter | Values | Purpose |
|-----------|--------|---------|
| [Param1] | [values] | [Why varied] |
| [Param2] | [values] | [Why varied] |

### Conditions
| Condition | Parameters | Replications |
|-----------|------------|--------------|
| [Condition1] | [param values] | N = ___ |
| [Condition2] | [param values] | N = ___ |

### Metrics
| Metric | Calculation | Aggregation |
|--------|-------------|-------------|
| [Metric1] | [Formula] | [Mean, median, etc.] |

### Validation
- Face validity: [Checked by]
- Sensitivity analysis: [Parameters varied]
- Comparison: [Benchmark methods]

### Output
- Raw data: [Location]
- Aggregated results: [Format]
- Visualization: [Types]
```

### Example: Convergence Analysis

```markdown
### Objective
Test convergence under different noise conditions

### Environment
- Python, NumPy
- Simulated gradient descent

### Parameters
- Noise level: [0.0, 0.1, 0.5, 1.0]
- Learning rate: [0.001, 0.01, 0.1]

### Conditions
- 16 conditions (4 noise x 3 LR)
- N = 100 runs per condition

### Metrics
- Convergence rate (1/epochs)
- Final loss value

### Reproducibility
- Seeds: 1-100
- Code version: v1.2.3
```

## Ablation Studies

### Description

Systematically remove components to test their contribution. Essential for understanding which parts of a system are responsible for performance.

### When to Use

- Testing contribution of components
- Understanding mechanism
- Validating design choices
- Model debugging

### Template

```markdown
## Ablation Study Design

### Objective
[What component contribution is being tested]

### Full System Components
1. [Component A]
2. [Component B]
3. [Component C]

### Ablation Conditions
| Condition | Components Removed | Rationale |
|-----------|-------------------|-----------|
| Full | None (baseline) | - |
| -A | [Component A] | [Why test without A] |
| -B | [Component B] | [Why test without B] |
| -A-B | [A and B] | [Why test without both] |

### Metrics
| Metric | Full | -A | -B | -A-B |
|--------|------|----|----|------|
| [Metric1] | ___ | ___ | ___ | ___ |
| [Metric2] | ___ | ___ | ___ | ___ |

### Analysis
- Contribution of A: Full - (-A)
- Contribution of B: Full - (-B)
- Interaction: (Full - (-A-B)) - (Contribution A + Contribution B)

### Sample
- N = ___ runs per condition
- Statistical test: [ANOVA, t-test, etc.]
```

### Example: Architecture Ablation

```markdown
### Objective
Test contribution of attention mechanism

### Full System
- Embedding layer
- Attention layer
- Feed-forward layer
- Output layer

### Conditions
| Condition | Removed | Expected Impact |
|-----------|---------|-----------------|
| Full | None | Best performance |
| -Attention | Attention layer | Lower accuracy |
| -FFN | Feed-forward layer | Lower accuracy |

### Metrics
- Accuracy on test set
- Inference time

### Analysis
- ANOVA across conditions
- Post-hoc pairwise comparisons
```

## Factorial Designs

### Description

Test multiple independent variables simultaneously. Allows examination of main effects and interactions.

### When to Use

- Multiple factors to test
- Interest in interactions
- Efficient use of resources
- Complex causal relationships

### Template

```markdown
## Factorial Design

### Design
- [Factor A] x [Factor B] factorial
- [ ] Between-subjects
- [ ] Within-subjects
- [ ] Mixed

### Factors and Levels
| Factor | Levels | Type |
|--------|--------|------|
| A | [a1, a2] | [Between/Within] |
| B | [b1, b2] | [Between/Within] |

### Conditions
| Condition | Factor A | Factor B | N |
|-----------|----------|----------|---|
| 1 | a1 | b1 | ___ |
| 2 | a1 | b2 | ___ |
| 3 | a2 | b1 | ___ |
| 4 | a2 | b2 | ___ |

### Analysis
- Main effect of A: [Test]
- Main effect of B: [Test]
- Interaction A x B: [Test]

### Expected Outcomes
- Effect of A: [Prediction]
- Effect of B: [Prediction]
- Interaction: [Prediction]
```

## Within-Subjects Designs

### Description

Each participant experiences all conditions. Increases statistical power but requires counterbalancing.

### When to Use

- Limited participants
- Interest in individual differences
- Carryover effects minimal
- High power needed

### Template

```markdown
## Within-Subjects Design

### Conditions
1. [Condition 1]
2. [Condition 2]
...

### Counterbalancing
- [ ] Latin square
- [ ] Random order
- [ ] ABBA
- [ ] Complete counterbalancing

### Order Effects
| Order | Condition Sequence |
|-------|-------------------|
| 1 | [1, 2, 3] |
| 2 | [2, 3, 1] |
| 3 | [3, 1, 2] |

### Washout
- Between conditions: [Time/procedure]

### Analysis
- Repeated measures ANOVA
- Mixed-effects model
```

## Between-Subjects Designs

### Description

Each participant experiences only one condition. Avoids carryover effects but requires more participants.

### When to Use

- Carryover effects likely
- Simple logistics
- Irreversible interventions
- Learning effects possible

### Template

```markdown
## Between-Subjects Design

### Conditions
| Condition | Description | N |
|-----------|-------------|---|
| 1 | [Description] | ___ |
| 2 | [Description] | ___ |

### Assignment
- [ ] Random assignment
- [ ] Matched groups
- Matching variables: [list]

### Equivalence Check
- Pre-test on: [variables]
- Expected: No significant differences

### Analysis
- Independent samples t-test (2 conditions)
- One-way ANOVA (3+ conditions)
```

## Quasi-Experiments

### Description

Lack random assignment but attempt to establish causality. Used when randomization is impossible.

### When to Use

- Random assignment impossible
- Natural groups
- Policy evaluation
- Field research

### Template

```markdown
## Quasi-Experiment Design

### Design Type
- [ ] Non-equivalent groups
- [ ] Interrupted time series
- [ ] Regression discontinuity
- [ ] Difference-in-differences

### Groups
| Group | Selection | N |
|-------|-----------|---|
| Treatment | [How selected] | ___ |
| Comparison | [How selected] | ___ |

### Threats to Internal Validity
| Threat | Risk Level | Mitigation |
|--------|------------|------------|
| Selection | High/Med/Low | [Strategy] |
| Maturation | High/Med/Low | [Strategy] |
| History | High/Med/Low | [Strategy] |

### Analysis
- Propensity score matching
- ANCOVA with covariates
- Regression adjustment
```

## Design Selection Guide

### Decision Tree

```
Can you randomly assign?
├── Yes
│   ├── One or multiple IVs?
│   │   ├── One → Controlled experiment (simple)
│   │   └── Multiple → Factorial design
│   └── Can participants experience all conditions?
│       ├── Yes → Within-subjects
│       └── No → Between-subjects
└── No
    ├── Can you manipulate the IV?
    │   ├── Yes → Quasi-experiment
    │   └── No → Observational study
```

### Quick Reference Table

| Design | Internal Validity | External Validity | Resources | Complexity |
|--------|-------------------|-------------------|-----------|------------|
| Controlled Experiment | High | Medium | High | Medium |
| A/B Test | High | High | Medium | Low |
| Observational | Low | High | Low | Medium |
| Simulation | High | Variable | Medium | Medium |
| Ablation | High | Medium | Medium | Low |
| Factorial | High | Medium | Medium | High |
| Within-Subjects | High | Medium | Low | Medium |
| Between-Subjects | High | Medium | High | Low |
| Quasi-Experiment | Medium | High | Medium | Medium |

### Design Checklist

Before finalizing a design:

- [ ] Does it directly test the hypothesis?
- [ ] Are IVs properly manipulated?
- [ ] Are DVs valid and reliable?
- [ ] Is sample size adequate for power?
- [ ] Are controls appropriate?
- [ ] Are confounds addressed?
- [ ] Is randomization possible/appropriate?
- [ ] Are ethical considerations addressed?
- [ ] Is analysis plan pre-specified?
- [ ] Are results reproducible?