# Evidence Hierarchy

This document defines the hierarchy of evidence quality and the GRADE framework for assessing evidence strength.

## Study Design Hierarchy

### Levels of Evidence

| Level | Study Type | Strength | Typical Use |
|-------|------------|----------|-------------|
| 1a | Systematic review of RCTs with homogeneity | Strongest | Synthesis of multiple high-quality trials |
| 1b | Individual RCT with narrow confidence interval | Very Strong | Single definitive trial |
| 1c | All-or-none case series | Strong | Dramatic treatment effects |
| 2a | Systematic review of cohort studies | Strong | Synthesis of observational evidence |
| 2b | Individual cohort study | Moderate-Strong | Prospective observational |
| 2c | Outcomes research, ecological studies | Moderate | Population-level evidence |
| 3a | Systematic review of case-control studies | Moderate | Synthesis of retrospective evidence |
| 3b | Individual case-control study | Moderate-Weak | Retrospective comparison |
| 4 | Case series, poor-quality cohort/case-control | Weak | Descriptive evidence |
| 5 | Expert opinion, editorials, bench research | Weakest | Indirect evidence |

### Oxford Centre for Evidence-Based Medicine (OCEBM) Levels

| Level | Therapy/Prevention | Prognosis | Diagnosis | Economic Analysis |
|-------|-------------------|-----------|-----------|-------------------|
| 1 | SR of RCTs | SR of inception cohorts | SR of validated studies | SR of economic evaluations |
| 2 | RCT | Inception cohort | Validated study | Economic evaluation |
| 3 | Non-randomized controlled trial | Cohort study | Exploratory study | Limited economic analysis |
| 4 | Case series | Case series | Case series | Case series |
| 5 | Expert opinion | Expert opinion | Expert opinion | Expert opinion |

## Study Type Details

### Systematic Reviews and Meta-Analyses

**Definition**: Structured synthesis of multiple studies on a research question.

**Strengths**:
- Combines evidence from multiple sources
- Increases statistical power
- Identifies patterns across studies
- Provides quantitative effect estimates

**Quality Indicators**:
- Pre-registered protocol
- Comprehensive search strategy
- Explicit inclusion/exclusion criteria
- Risk of bias assessment
- Heterogeneity assessment
- Publication bias assessment

**Limitations**:
- Garbage in, garbage out
- Heterogeneity may limit synthesis
- Publication bias
- Dependent on primary study quality

### Randomized Controlled Trials (RCTs)

**Definition**: Participants randomly assigned to intervention or control groups.

**Strengths**:
- Gold standard for causation
- Controls for confounding through randomization
- Allows blinding
- Clear temporal sequence

**Quality Indicators**:
- Adequate randomization sequence generation
- Allocation concealment
- Blinding of participants and personnel
- Blinding of outcome assessment
- Complete outcome data
- Selective reporting avoided

**Limitations**:
- May not reflect real-world conditions
- Ethical constraints
- Expensive and time-consuming
- May have limited generalizability

### Quasi-Experimental Studies

**Definition**: Studies with intervention but without random assignment.

**Types**:
- Non-randomized controlled trials
- Regression discontinuity designs
- Interrupted time series
- Controlled before-after studies

**Strengths**:
- Can assess interventions when RCT not feasible
- May have better external validity
- Often more practical

**Limitations**:
- Selection bias
- Confounding
- Weaker causal inference

### Cohort Studies

**Definition**: Follow groups (cohorts) over time to compare outcomes.

**Types**:
- Prospective: Groups identified at start and followed forward
- Retrospective: Groups identified from historical records

**Strengths**:
- Good for rare exposures
- Can examine multiple outcomes
- Establishes temporal sequence
- Good for studying natural history

**Quality Indicators**:
- Representative sample
- Clear exposure definition
- Adequate follow-up duration
- High follow-up rate
- Blinded outcome assessment
- Control for confounders

**Limitations**:
- Inefficient for rare outcomes
- Loss to follow-up
- Confounding
- Long duration for prospective

### Case-Control Studies

**Definition**: Compare cases (with outcome) to controls (without outcome) on past exposures.

**Strengths**:
- Efficient for rare outcomes
- Relatively quick and inexpensive
- Can examine multiple exposures
- Good for diseases with long latency

**Quality Indicators**:
- Incident rather than prevalent cases
- Representative cases
- Appropriate control selection
- Comparable exposure assessment
- Blinded exposure assessment

**Limitations**:
- Recall bias
- Selection bias
- Cannot calculate incidence
- Confounding
- Temporal sequence may be unclear

### Cross-Sectional Studies

**Definition**: Assess exposure and outcome at one point in time.

**Strengths**:
- Quick and inexpensive
- Good for prevalence estimation
- Useful for hypothesis generation
- Can examine multiple associations

**Limitations**:
- Cannot establish temporal sequence
- Prevalence-incidence bias
- Not suitable for rare conditions
- Subject to survivorship bias

### Case Series and Case Reports

**Definition**: Description of one or more cases without comparison group.

**Strengths**:
- Hypothesis generation
- Documentation of new conditions
- Rare condition reporting
- Adverse event reporting

**Limitations**:
- No comparison group
- Cannot estimate effects
- Subject to selection bias
- Not generalizable

## GRADE Framework

### Overview

The Grading of Recommendations Assessment, Development and Evaluation (GRADE) approach provides a system for rating quality of evidence.

### GRADE Evidence Quality

| Rating | Definition |
|--------|------------|
| High | Further research very unlikely to change confidence in estimate |
| Moderate | Further research likely to have important impact on confidence |
| Low | Further research very likely to have important impact on confidence |
| Very Low | Any estimate of effect is very uncertain |

### Starting Point by Study Design

| Study Design | Initial Quality |
|--------------|-----------------|
| RCTs | High |
| Observational studies | Low |

### Factors That Decrease Quality

| Factor | Description | Downgrade |
|--------|-------------|-----------|
| Risk of Bias | Methodological limitations | -1 or -2 |
| Inconsistency | Unexplained heterogeneity across studies | -1 or -2 |
| Indirectness | Evidence not directly applicable | -1 or -2 |
| Imprecision | Wide confidence intervals, small sample | -1 or -2 |
| Publication Bias | Likely underreporting | -1 or -2 |

### Risk of Bias Assessment

**For RCTs**:

| Domain | Questions |
|--------|-----------|
| Randomization | Was sequence generation adequate? Was allocation concealed? |
| Deviations | Were participants and personnel blinded? Were deviations from intervention addressed? |
| Missing data | Were outcome data complete? Was missing data addressed? |
| Measurement | Was outcome assessment blinded? |
| Selection | Were groups analyzed as randomized? Were results selectively reported? |

**For Observational Studies**:

| Domain | Questions |
|--------|-----------|
| Confounding | Were confounders measured and controlled? |
| Selection | Was selection into study related to exposure and outcome? |
| Classification | Were exposures and outcomes measured appropriately? |
| Missing data | Was missing data addressed appropriately? |
| Measurement | Was outcome assessment blinded? |
| Selection | Were results selectively reported? |

### Inconsistency Assessment

**Indicators of Inconsistency**:

- Point estimates vary widely across studies
- Confidence intervals show little or no overlap
- Statistical heterogeneity (I² > 50%)
- Different directions of effect
- Unexplained differences in effect estimates

**Assessment**:

| I² Value | Interpretation |
|----------|----------------|
| 0-40% | Might not be important |
| 30-60% | May represent moderate heterogeneity |
| 50-90% | May represent substantial heterogeneity |
| 75-100% | Considerable heterogeneity |

### Indirectness Assessment

**Types of Indirectness**:

| Type | Description |
|------|-------------|
| Population | Study population differs from target |
| Intervention | Intervention differs from target |
| Comparator | Comparator differs from target |
| Outcome | Surrogate outcomes, short follow-up |
| Indirect comparison | No head-to-head comparison |

### Imprecision Assessment

**Indicators**:

- Wide confidence intervals
- Small sample size
- Low event numbers
- Confidence interval crosses decision threshold

**Optimal Information Size (OIS)**: Minimum sample size needed for adequate power.

### Factors That Increase Quality

| Factor | Description | Upgrade |
|--------|-------------|---------|
| Large Effect | Effect size large (RR > 2 or < 0.5) | +1 |
| Very Large Effect | Effect size very large (RR > 5 or < 0.2) | +2 |
| Dose-Response | Evidence of dose-response relationship | +1 |
| Residual Confounding | Would bias toward null if present | +1 |

## Convergence of Evidence

### Definition

Multiple independent lines of evidence supporting the same conclusion.

### Types of Convergence

| Type | Description |
|------|-------------|
| Methodological | Different methods yield similar results |
| Population | Results replicated across populations |
| Setting | Results replicated across settings |
| Temporal | Results replicated over time |
| Theoretical | Empirical results align with theory |

### Assessing Convergence

1. **Identify lines of evidence**: What different approaches have been used?
2. **Evaluate each line**: Assess quality of each line
3. **Compare conclusions**: Do lines point in same direction?
4. **Explain discrepancies**: If divergent, why?
5. **Synthesize**: What does overall pattern suggest?

### Convergence Matrix

| Evidence Quality | High Convergence | Moderate Convergence | Low Convergence |
|------------------|------------------|---------------------|-----------------|
| High | Very Strong Evidence | Strong Evidence | Moderate Evidence |
| Moderate | Strong Evidence | Moderate Evidence | Weak Evidence |
| Low | Moderate Evidence | Weak Evidence | Very Weak Evidence |

## Evidence Quality Summary Checklist

### Systematic Reviews

- [ ] Protocol pre-registered
- [ ] Comprehensive search
- [ ] Explicit selection criteria
- [ ] Risk of bias assessed
- [ ] Heterogeneity assessed
- [ ] Publication bias assessed
- [ ] GRADE applied

### Primary Studies

- [ ] Appropriate design for question
- [ ] Adequate sample size
- [ ] Appropriate controls/comparisons
- [ ] Valid and reliable measures
- [ ] Complete reporting
- [ ] Biases addressed

### Overall Assessment

- [ ] Multiple lines of evidence considered
- [ ] Convergence of evidence evaluated
- [ ] Quality across studies synthesized
- [ ] Confidence in estimates expressed
- [ ] Limitations acknowledged