---
name: airesearchorchestrator:critical-evaluation
agent: critic
description: Apply systematic critical evaluation to research outputs, including methodology critique, bias detection, statistical analysis evaluation, evidence quality assessment, and logical fallacy identification. Use when user says "critically evaluate", "critical review", "批判性评估", "审核质量", or when reviewing Survey Phase outputs.
argument-hint: [target-path] [--focus methodology|bias|statistics|evidence|fallacies|all]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebFetch
---

# Critical Evaluation

## Overview

Apply rigorous, systematic critical evaluation to research outputs across six dimensions: methodology, bias, statistics, evidence quality, logical reasoning, and research design. This skill is the core capability of the Critic Agent for auditing Survey Phase outputs and is also used by Adviser and Reviewer agents.

## Purpose

Ensure research outputs meet scientific standards by identifying weaknesses, biases, and gaps before proceeding to subsequent phases. Prevent propagation of methodological flaws, unsupported claims, or invalid reasoning throughout the research pipeline.

## Workflow

### Step 1: Determine Evaluation Scope

Identify the target of evaluation:

- **Survey outputs**: `docs/reports/survey/` materials
- **Literature review**: Citation lists, summaries, gap analysis
- **Research claims**: Hypotheses, novelty claims, problem definitions
- **Experimental designs**: Methodology, protocols, analysis plans

Use the `--focus` argument to narrow evaluation:

- `methodology` - Focus on methodology critique
- `bias` - Focus on bias detection
- `statistics` - Focus on statistical analysis evaluation
- `evidence` - Focus on evidence quality assessment
- `fallacies` - Focus on logical fallacy identification
- `all` - Comprehensive evaluation (default)

### Step 2: Methodology Critique

Evaluate the research methodology systematically.

#### Study Design Evaluation

Check:

- Is the study design appropriate for the research question?
- Are the experimental and control conditions clearly defined?
- Is the temporal structure appropriate (cross-sectional vs. longitudinal)?
- Are the unit of analysis and level of analysis correct?

Read [references/scientific_method.md](references/scientific_method.md) for study design frameworks.

#### Validity Analysis

Assess three types of validity:

| Validity Type | Key Questions | Red Flags |
|---------------|---------------|-----------|
| Internal | Can we attribute observed effects to the manipulated variables? | Confounding variables, lack of controls, selection bias |
| External | Can results be generalized to other populations/contexts? | Non-representative samples, artificial conditions |
| Construct | Do measurements actually capture the intended constructs? | Poor operationalization, inappropriate proxies |

#### Control and Blinding Assessment

Verify:

- Appropriate control conditions or baseline comparisons
- Randomization procedures documented
- Blinding implemented where feasible (single/double-blind)
- Placebo or sham conditions where applicable

#### Measurement Reliability

Evaluate:

- Inter-rater reliability for subjective measures
- Test-retest reliability for repeated measures
- Internal consistency (Cronbach's alpha, etc.)
- Calibration and validation of instruments

### Step 3: Bias Detection

Identify potential biases that could compromise validity.

#### Cognitive Biases

Check for researcher cognitive biases:

| Bias | Description | Detection |
|------|-------------|-----------|
| Confirmation bias | Seeking evidence that supports hypotheses | Cherry-picked results, ignored contradictory evidence |
| Publication bias | Favoring positive results | Missing negative results, selective reporting |
| Hindsight bias | "We knew it all along" | Over-interpretation after seeing results |
| Anchoring bias | Over-relying on initial information | Ignoring subsequent evidence |

Read [references/common_biases.md](references/common_biases.md) for a comprehensive bias catalog.

#### Selection Bias

Evaluate:

- Is the sample representative of the target population?
- Are inclusion/exclusion criteria appropriate?
- Is there survivorship bias in longitudinal studies?
- Are comparison groups balanced?

#### Measurement Bias

Check:

- Are measurement instruments valid and reliable?
- Is there systematic error in data collection?
- Are there differential measurement effects across groups?
- Is recall bias present in retrospective studies?

#### Analysis Bias

Identify:

- P-hacking and data dredging
- Stopping rules and optional stopping
- Selective reporting of outcomes
- Inappropriate subgroup analyses

#### Confounding Factors

Assess:

- Are potential confounders identified?
- Are confounders measured and controlled?
- Is residual confounding possible?
- Are mediator vs. confounder relationships correct?

### Step 4: Statistical Analysis Evaluation

Critically assess the statistical approach.

#### Sample Size Adequacy

Check:

- Was a power analysis conducted?
- Is the sample size justified?
- Are effect sizes realistic?
- Is the study adequately powered for the primary outcomes?

#### Test Selection Appropriateness

Verify:

- Are statistical tests appropriate for the data type?
- Are distributional assumptions checked?
- Are non-parametric alternatives used when needed?
- Are corrections for multiple comparisons applied?

#### Multiple Comparisons Handling

Evaluate:

- Are multiple testing corrections applied (Bonferroni, FDR, etc.)?
- Is the family-wise error rate controlled?
- Are pre-registered analyses distinguished from exploratory?
- Are correction methods appropriate for the dependency structure?

#### P-value Interpretation

Assess:

- Are p-values interpreted correctly (not as probability of hypothesis)?
- Is statistical vs. practical significance distinguished?
- Are confidence intervals reported alongside p-values?
- Is the "p < 0.05" threshold applied appropriately?

#### Effect Size Assessment

Check:

- Are effect sizes reported with confidence intervals?
- Is the effect size measure appropriate for the context?
- Are effect sizes interpreted in practical terms?
- Is the precision of estimates discussed?

Read [references/statistical_pitfalls.md](references/statistical_pitfalls.md) for common statistical errors.

### Step 5: Evidence Quality Assessment

Evaluate the quality and strength of evidence.

#### Study Hierarchy

Apply the evidence hierarchy:

| Level | Study Type | Strength |
|-------|------------|----------|
| 1 | Systematic reviews, meta-analyses | Strongest |
| 2 | Randomized controlled trials (RCTs) | Strong |
| 3 | Quasi-experimental studies | Moderate |
| 4 | Observational studies (cohort, case-control) | Moderate-Weak |
| 5 | Case series, case reports | Weak |
| 6 | Expert opinion, editorials | Weakest |

Read [references/evidence_hierarchy.md](references/evidence_hierarchy.md) for detailed grading criteria.

#### GRADE Framework

Apply GRADE criteria for evidence quality:

- **Risk of bias**: Methodological limitations
- **Inconsistency**: Heterogeneity across studies
- **Indirectness**: Applicability to the question
- **Imprecision**: Wide confidence intervals, small samples
- **Publication bias**: Likely underreporting

Rate evidence as: High, Moderate, Low, or Very Low quality.

#### Convergence of Evidence

Assess:

- Do multiple lines of evidence converge?
- Are findings replicated across studies?
- Is there evidence from different methodological approaches?
- Are theoretical and empirical evidence aligned?

### Step 6: Logical Fallacy Identification

Identify reasoning errors in arguments.

#### Causation Fallacies

Check for:

| Fallacy | Description | Example |
|---------|-------------|---------|
| Post hoc ergo propter hoc | After this, therefore because of this | "X happened after Y, so Y caused X" |
| Cum hoc ergo propter hoc | Correlation implies causation | "X and Y are correlated, so X causes Y" |
| Reverse causation | Wrong causal direction | Assuming A causes B when B causes A |

#### Generalization Fallacies

Identify:

| Fallacy | Description | Detection |
|---------|-------------|-----------|
| Hasty generalization | Drawing conclusions from insufficient sample | Small n, non-representative sample |
| Sampling bias | Non-representative sample | Selection issues, convenience sampling |
| Ecological fallacy | Applying group-level findings to individuals | Aggregate data used for individual claims |

#### Authority Fallacies

Check:

- Appeal to authority without evidence
- Expertise in one area applied to another
- Citations used as argument from authority
- "Everyone knows" or "it is well established" without support

#### Statistical Fallacies

Identify:

| Fallacy | Description |
|---------|-------------|
| Gambler's fallacy | Expecting regression to mean in independent events |
| Base rate fallacy | Ignoring population prevalence |
| Prosecutor's fallacy | Confusing P(evidence|innocent) with P(innocent|evidence) |
| Simpson's paradox | Trend reversed when groups combined |

Read [references/logical_fallacies.md](references/logical_fallacies.md) for a comprehensive catalog.

### Step 7: Research Design Guidance

Provide constructive recommendations.

#### Question Refinement

If research questions are unclear:

- Suggest more specific, testable formulations
- Recommend scope narrowing if too broad
- Propose operational definitions
- Identify falsifiable hypotheses

#### Transparency and Rigor Standards

Recommend:

- Pre-registration of hypotheses and analyses
- Complete reporting of all conditions and measures
- Data and code sharing practices
- Replication study design

## Output

Generate a Critical Evaluation Report:

```markdown
# Critical Evaluation Report

## Summary
- **Target**: [What was evaluated]
- **Evaluation Focus**: [methodology/bias/statistics/evidence/fallacies/all]
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION / BLOCKED
- **Confidence Level**: HIGH / MEDIUM / LOW

---

## 1. Methodology Critique

### Study Design
- **Design Type**: [Experimental/Quasi-experimental/Observational/...]
- **Appropriateness**: [Assessment]
- **Issues Identified**:
  - [Issue 1]
  - [Issue 2]

### Validity Assessment

| Validity Type | Score | Issues |
|---------------|-------|--------|
| Internal | X/10 | [Issues] |
| External | X/10 | [Issues] |
| Construct | X/10 | [Issues] |

### Control and Blinding
- [Assessment of controls]
- [Assessment of blinding]

### Measurement Reliability
- [Assessment of reliability measures]

---

## 2. Bias Detection

### Cognitive Biases Detected
| Bias Type | Evidence | Severity |
|-----------|----------|----------|
| [Bias] | [Evidence] | HIGH/MEDIUM/LOW |

### Selection Bias
- [Assessment]

### Measurement Bias
- [Assessment]

### Analysis Bias
- [Assessment]

### Confounding Factors
- **Identified Confounders**: [List]
- **Controlled**: [Yes/Partially/No]
- **Residual Confounding Risk**: HIGH/MEDIUM/LOW

---

## 3. Statistical Analysis Evaluation

### Sample Size
- **Power Analysis**: Present/Absent
- **Adequacy**: Adequate/Marginal/Inadequate
- **Effect Size Assumptions**: [Assessment]

### Statistical Tests
- **Appropriateness**: Correct/Questionable/Incorrect
- **Assumptions Verified**: Yes/No/Partial
- **Alternative Tests Considered**: [List]

### Multiple Comparisons
- **Number of Comparisons**: X
- **Correction Method**: [Method or None]
- **Family-wise Error Rate**: Controlled/Uncontrolled

### P-value and Effect Sizes
- **P-value Interpretation**: Correct/Misleading/Incorrect
- **Effect Sizes Reported**: Yes/No/Partial
- **Confidence Intervals**: Reported/Not Reported

---

## 4. Evidence Quality Assessment

### Study Types Included

| Study Type | Count | Quality |
|------------|-------|---------|
| Meta-analyses | X | [Quality] |
| RCTs | X | [Quality] |
| Observational | X | [Quality] |
| Case studies | X | [Quality] |

### GRADE Assessment
- **Risk of Bias**: [Assessment]
- **Inconsistency**: [Assessment]
- **Indirectness**: [Assessment]
- **Imprecision**: [Assessment]
- **Publication Bias**: [Assessment]
- **Overall Quality**: High/Moderate/Low/Very Low

### Evidence Convergence
- **Lines of Evidence**: [Number]
- **Replication Status**: [Assessment]
- **Consistency**: Consistent/Mixed/Inconsistent

---

## 5. Logical Fallacy Identification

### Fallacies Detected

| Fallacy | Location | Severity | Recommendation |
|---------|----------|----------|----------------|
| [Fallacy] | [Section/Page] | HIGH/MEDIUM/LOW | [Fix] |

### Reasoning Quality
- **Causal Claims**: Justified/Partially Justified/Unjustified
- **Generalizations**: Appropriate/Overreaching
- **Appeals to Authority**: Appropriate/Misplaced

---

## 6. Recommendations

### Critical Issues (Must Fix)
1. [Issue with specific fix recommendation]
2. [Issue with specific fix recommendation]

### Moderate Issues (Should Fix)
1. [Issue with specific fix recommendation]
2. [Issue with specific fix recommendation]

### Minor Issues (Consider Fixing)
1. [Issue with specific fix recommendation]
2. [Issue with specific fix recommendation]

### Strengths
- [Strength 1]
- [Strength 2]

---

## Gate Decision

- [ ] **PASS** - No critical issues, proceed to next phase
- [ ] **PASS_WITH_FIXES** - Minor/moderate issues, fix and proceed
- [ ] **REVISE** - Significant issues requiring revision
- [ ] **MAJOR_REVISION** - Fundamental problems, return for major work
- [ ] **BLOCK** - Critical issues blocking further progress

### Rationale
[Explanation of gate decision]

### Required Actions Before Proceeding
1. [Action item]
2. [Action item]
```

## Key Rules

1. **Be systematic**: Follow the full evaluation workflow; do not skip sections
2. **Be constructive**: Identify issues AND provide specific recommendations
3. **Be evidence-based**: Support all assessments with specific evidence from the material
4. **Be proportionate**: Focus depth of evaluation on high-risk areas
5. **Distinguish severity**: Clearly separate critical, moderate, and minor issues
6. **Use references**: Consult reference documents for detailed criteria
7. **Gate strictly**: Block advancement when critical issues exist

## References

- [Scientific Method](references/scientific_method.md) - Study design frameworks and validity criteria
- [Common Biases](references/common_biases.md) - Comprehensive bias catalog
- [Statistical Pitfalls](references/statistical_pitfalls.md) - Common statistical errors
- [Evidence Hierarchy](references/evidence_hierarchy.md) - Study type ranking and GRADE criteria
- [Logical Fallacies](references/logical_fallacies.md) - Reasoning error catalog