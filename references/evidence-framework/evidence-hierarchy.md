# Evidence Hierarchy

## Overview

Not all evidence is created equal. Evidence hierarchies rank study designs by their ability to minimize bias and establish causal relationships. Understanding these hierarchies is essential for critical evaluation of research.

## Classic Evidence Pyramid

```
                    ┌─────────────────┐
                    │  Systematic     │
                    │  Reviews &      │
                    │  Meta-analyses  │
                    └────────┬────────┘
                             │
                   ┌─────────┴─────────┐
                   │  Randomized       │
                   │  Controlled       │
                   │  Trials (RCTs)    │
                   └────────┬──────────┘
                            │
            ┌───────────────┴───────────────┐
            │  Cohort Studies               │
            │  (Prospective observational)  │
            └───────────────┬───────────────┘
                            │
            ┌───────────────┴───────────────┐
            │  Case-Control Studies         │
            │  (Retrospective observational)│
            └───────────────┬───────────────┘
                            │
    ┌───────────────────────┴───────────────────────┐
    │  Case Series, Case Reports, Expert Opinion   │
    └───────────────────────────────────────────────┘
```

## Study Types Ranked by Evidence Strength

### Level 1: Systematic Reviews and Meta-analyses

**Definition:** Comprehensive synthesis of all relevant studies on a topic.

**Strengths:**
- Highest level of evidence
- Combines results across studies
- Increases statistical power
- Identifies patterns and inconsistencies

**Limitations:**
- Garbage in, garbage out
- Publication bias
- Heterogeneity across studies

**Quality Indicators:**
- [ ] Pre-registered protocol (PROSPERO)
- [ ] Clear inclusion/exclusion criteria
- [ ] Multiple database searches
- [ ] Risk of bias assessment
- [ ] Heterogeneity analysis (I²)
- [ ] Publication bias assessment (funnel plot)

### Level 2: Randomized Controlled Trials (RCTs)

**Definition:** Participants randomly assigned to intervention or control groups.

**Strengths:**
- Gold standard for causation
- Controls for confounders through randomization
- Can be blinded

**Limitations:**
- May not reflect real-world conditions
- Expensive and time-consuming
- Ethical constraints on randomization

**Quality Indicators:**
- [ ] Random sequence generation
- [ ] Allocation concealment
- [ ] Blinding of participants and personnel
- [ ] Blinding of outcome assessment
- [ ] Complete outcome data
- [ ] Selective reporting avoided

### Level 3: Cohort Studies

**Definition:** Follow groups over time to compare outcomes.

**Strengths:**
- Can establish temporal sequence
- Good for rare exposures
- Multiple outcomes can be studied

**Limitations:**
- Confounding is major concern
- Expensive for long follow-up
- Loss to follow-up

**Quality Indicators:**
- [ ] Representative sample
- [ ] Prospective design (vs. retrospective)
- [ ] Adequate follow-up duration
- [ ] Control for confounders
- [ ] Blinded outcome assessment

### Level 4: Case-Control Studies

**Definition:** Compare cases (with outcome) to controls (without outcome).

**Strengths:**
- Good for rare outcomes
- Relatively inexpensive
- Quick to conduct

**Limitations:**
- Recall bias
- Selection bias
- Cannot establish temporal sequence

**Quality Indicators:**
- [ ] Appropriate control selection
- [ ] Matching on confounders
- [ ] Blinded exposure assessment
- [ ] Adequate sample size

### Level 5: Case Series and Case Reports

**Definition:** Description of individual cases or series of cases.

**Strengths:**
- First line of evidence for new phenomena
- Good for rare conditions
- Generate hypotheses

**Limitations:**
- No control group
- High risk of bias
- Cannot establish causation

### Level 6: Expert Opinion

**Definition:** Opinions of authorities in the field.

**Strengths:**
- Useful when no other evidence exists
- Synthesizes experience

**Limitations:**
- Subject to bias
- Not systematic
- May reflect tradition rather than evidence

## GRADE Framework

### Overview

The Grading of Recommendations Assessment, Development and Evaluation (GRADE) system provides a structured approach to rating evidence quality.

### Evidence Quality Levels

| Rating | Description | Interpretation |
|--------|-------------|----------------|
| **High** | We are very confident | True effect lies close to estimate |
| **Moderate** | We are moderately confident | True effect likely close to estimate |
| **Low** | Our confidence is limited | True effect may be substantially different |
| **Very Low** | We have very little confidence | True effect likely substantially different |

### Factors That Lower Evidence Quality

| Factor | Description | Example |
|--------|-------------|---------|
| **Risk of bias** | Methodological flaws | Lack of blinding, incomplete data |
| **Inconsistency** | Heterogeneous results | I² > 50%, opposite directions |
| **Indirectness** | Indirect evidence | Animal studies, surrogate outcomes |
| **Imprecision** | Wide confidence intervals | Small sample, few events |
| **Publication bias** | Selective publication | Funnel plot asymmetry |

### Factors That Increase Evidence Quality

| Factor | Description | Example |
|--------|-------------|---------|
| **Large effect size** | Magnitude of effect | RR > 2 or RR < 0.5 |
| **Dose-response** | Gradient relationship | Linear trend across doses |
| **Plausible confounding** | Confounding would reduce effect | Effect persists despite bias |

### GRADE Assessment Workflow

```markdown
1. Start with study design
   - RCTs → High
   - Observational → Low

2. Lower quality for:
   - Risk of bias (-1 or -2)
   - Inconsistency (-1 or -2)
   - Indirectness (-1 or -2)
   - Imprecision (-1 or -2)
   - Publication bias (-1 or -2)

3. Raise quality for:
   - Large effect (+1 or +2)
   - Dose-response (+1)
   - Plausible confounding (+1)

4. Final rating: High, Moderate, Low, or Very Low
```

## Evidence in Machine Learning Research

### ML-Specific Hierarchy

| Level | Evidence Type | Example |
|-------|---------------|---------|
| 1 | Reproducible benchmarks with code | Papers with code, multiple datasets |
| 2 | Ablation studies | Component contribution analysis |
| 3 | Cross-validation results | k-fold CV with proper splits |
| 4 | Single train/test split | Hold-out validation |
| 5 | Theoretical analysis | Complexity bounds, convergence proofs |
| 6 | Expert intuition | "We believe this should work" |

### Red Flags in ML Evidence

- [ ] No statistical significance testing
- [ ] Single random seed
- [ ] Cherry-picked examples
- [ ] Unfair comparison (different compute, data)
- [ ] No baselines or weak baselines
- [ ] Test data leaked into training
- [ ] Hyperparameter tuning on test set

### Best Practices for ML Evidence

```markdown
1. Multiple random seeds (report mean ± std)
2. Statistical significance testing
3. Proper train/validation/test splits
4. Ablation studies
5. Comparison to strong baselines
6. Released code and data
7. Compute budget reported
8. Hyperparameter search details
```

## Applying Evidence Hierarchies

### For Literature Review

1. Start with systematic reviews
2. Include high-quality RCTs
3. Add observational studies if necessary
4. Note limitations of lower-quality evidence

### For Clinical/Policy Decisions

1. What is the quality of evidence?
2. What is the magnitude of effect?
3. What are the risks and costs?
4. What are patient preferences?

### For Research Design

1. Match design to question
2. Aim for highest feasible evidence level
3. Document limitations
4. Consider feasibility and ethics

## Evidence Quality Checklist

### For RCTs

- [ ] Randomization method described
- [ ] Allocation concealed
- [ ] Groups comparable at baseline
- [ ] Participants blinded (if possible)
- [ ] Outcome assessors blinded
- [ ] Intention-to-treat analysis
- [ ] All outcomes reported
- [ ] Sample size justified

### For Observational Studies

- [ ] Representative sample
- [ ] Exposure measured before outcome
- [ ] Valid and reliable measures
- [ ] Confounders measured and controlled
- [ ] Complete follow-up
- [ ] Sensitivity analyses conducted

### For Systematic Reviews

- [ ] Protocol pre-registered
- [ ] Comprehensive search strategy
- [ ] Clear eligibility criteria
- [ ] Risk of bias assessment
- [ ] Appropriate synthesis method
- [ ] Heterogeneity explored
- [ ] Publication bias assessed

## References

- GRADE Working Group (2004). Grading quality of evidence
- Murad, M. H., et al. (2016). How to read a systematic review
- Concato, J., et al. (2000). Randomized, controlled trials, observational studies