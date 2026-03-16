# Common Biases

This document catalogs biases that can affect research validity and how to detect them.

## Cognitive Biases (Researcher)

### Confirmation Bias

**Definition**: Tendency to search for, interpret, and recall information in ways that confirm existing beliefs.

**Detection Signs**:
- Selective citation of supporting evidence
- Dismissing contradictory evidence without examination
- Framing results to fit hypotheses
- Ignoring alternative explanations

**Mitigation**:
- Pre-register hypotheses and analysis plans
- Actively seek disconfirming evidence
- Use blind analysis
- Consider alternative explanations explicitly

### Publication Bias

**Definition**: Tendency for positive results to be published more often than negative results.

**Detection Signs**:
- Literature dominated by positive findings
- Missing null results in systematic reviews
- Funnel plot asymmetry in meta-analyses
- Studies with larger samples showing smaller effects

**Mitigation**:
- Pre-registration
- Registered reports
- Search grey literature
- Use trim-and-fill methods in meta-analysis

### Hindsight Bias

**Definition**: Tendency to see past events as having been predictable.

**Detection Signs**:
- Post-hoc explanations presented as predictions
- "We expected this result" after seeing data
- Adapting theory to fit results
- Lack of pre-registration

**Mitigation**:
- Pre-register predictions
- Document predictions before data collection
- Report all pre-registered analyses
- Distinguish confirmatory from exploratory

### Anchoring Bias

**Definition**: Over-reliance on the first piece of information encountered.

**Detection Signs**:
- Persistent effect of initial hypothesis despite new evidence
- Over-weighting early results
- Dismissing subsequent contradictory findings
- Analysis stuck on initial assumptions

**Mitigation**:
- Consider multiple hypotheses
- Update beliefs with new evidence
- Use Bayesian approaches
- Conduct sensitivity analyses

### Availability Bias

**Definition**: Over-weighting information that comes to mind easily.

**Detection Signs**:
- Over-representation of recent or memorable studies
- Missing older or less prominent literature
- Focus on extreme cases
- Neglect of base rates

**Mitigation**:
- Systematic literature search
- Consider all relevant evidence
- Use structured review methods
- Include diverse sources

## Selection Biases

### Sampling Bias

**Definition**: Sample not representative of the target population.

**Types**:

| Type | Description | Example |
|------|-------------|---------|
| Convenience Sampling | Selecting readily available subjects | College student samples |
| Self-Selection Bias | Participants choose to participate | Online surveys |
| Survivorship Bias | Only analyzing "survivors" | Successful companies only |
| Non-Response Bias | Non-responders differ from responders | Survey non-responders |

**Detection Signs**:
- Sample characteristics differ from population
- High non-response rate
- Recruitment from limited sources
- No comparison of responders vs. non-responders

**Mitigation**:
- Random sampling from target population
- Weight adjustments for non-response
- Multiple recruitment strategies
- Report sample demographics vs. population

### Berkson's Bias

**Definition**: Selection based on exposure and outcome creates spurious association.

**Detection Signs**:
- Hospital-based or clinic-based samples
- Selection based on characteristics related to exposure and outcome
- Association present in selected sample but not population

**Mitigation**:
- Population-based sampling
- Understand selection mechanisms
- Adjust for selection factors

### Healthy Worker Effect

**Definition**: Working populations are healthier than general population.

**Detection Signs**:
- Occupational cohort studies
- Lower mortality than general population
- Results may not generalize

**Mitigation**:
- Compare to employed reference population
- Account for health status at entry
- Consider length of employment

## Information Biases

### Recall Bias

**Definition**: Differential accuracy in recall between groups.

**Detection Signs**:
- Retrospective data collection
- Cases more likely to recall exposures
- Long recall periods
- Socially sensitive exposures

**Mitigation**:
- Prospective design
- Shorter recall periods
- Use of records rather than memory
- Blind participants to hypothesis

### Observer Bias

**Definition**: Systematic differences in information collection between groups.

**Detection Signs**:
- Subjective outcome assessment
- Knowledge of exposure/outcome status
- Lack of standardized protocols
- Different measurement procedures for groups

**Mitigation**:
- Blinded assessment
- Standardized protocols
- Objective measures
- Training and calibration

### Misclassification Bias

**Definition**: Errors in classifying exposure or outcome status.

**Types**:

| Type | Description | Effect |
|------|-------------|--------|
| Non-differential | Same error rate in all groups | Bias toward null |
| Differential | Different error rates between groups | Bias in either direction |

**Detection Signs**:
- Imprecise measurement
- Single measurement of variable
- Self-report without validation
- Variable definitions changed

**Mitigation**:
- Validate measurement instruments
- Multiple measurements
- Use established definitions
- Sensitivity analysis

## Analysis Biases

### P-Hacking

**Definition**: Selectively reporting analyses that achieve statistical significance.

**Forms**:

| Form | Description |
|------|-------------|
| Data Dredging | Running many analyses, reporting significant ones |
| Outcome Switching | Changing primary outcome based on results |
| Subgroup Fishing | Analyzing many subgroups, reporting significant ones |
| Optional Stopping | Stopping data collection when significance reached |

**Detection Signs**:
- Many analyses reported, few significant
- Unusual analysis choices
- Multiple primary outcomes
- No pre-registration
| Subgroup analyses not pre-specified |

**Mitigation**:
- Pre-register analysis plan
- Report all analyses conducted
- Correct for multiple comparisons
- Separate confirmatory from exploratory

### Citation Bias

**Definition**: Selective citation of studies supporting a position.

**Types**:

| Type | Description |
|------|-------------|
| Positive Citation Bias | Citing supportive studies |
| Language Bias | Citing only English-language studies |
| Familiarity Bias | Citing known authors/journals |

**Detection Signs**:
- Missing contradictory studies in citations
- All citations support one view
- Disproportionate self-citation
- Ignoring recent contradictory evidence

**Mitigation**:
- Systematic search
- Include contradictory evidence
- Discuss limitations of supporting evidence
- Cite across journals and authors

## Confounding

### Definition

A confounder is a variable that:
1. Is associated with the exposure
2. Causes the outcome
3. Is not on the causal pathway

### Types of Confounding

| Type | Description | Example |
|------|-------------|---------|
| Confounding by Indication | Treatment depends on prognosis | Sicker patients get treatment |
| Time-Varying Confounding | Confounder changes over time | Lifestyle changes during study |
| Confounding by Severity | Severity affects both exposure and outcome | More severe disease leads to more treatment |

### Detection Signs**

- Known confounders not measured
- Known confounders not controlled
- Large differences between unadjusted and adjusted estimates
- Imbalance in potential confounders between groups

**Mitigation**:
- Identify potential confounders a priori
- Measure known confounders
- Use appropriate control methods (matching, stratification, regression, propensity scores)
- Consider residual confounding
- Sensitivity analysis for unmeasured confounding

## Bias Assessment Tools

### For Observational Studies

- **Newcastle-Ottawa Scale**: For case-control and cohort studies
- **ROBINS-I**: Risk of Bias in Non-randomized Studies of Interventions

### For Randomized Trials

- **Cochrane Risk of Bias Tool**: Randomization, deviations, missing data, measurement, selection

### For Systematic Reviews

- **ROBIS**: Risk of Bias in Systematic Reviews
- **AMSTAR**: Assessing Methodological Quality of Systematic Reviews

## Bias Direction Summary

| Bias Type | Typical Direction |
|-----------|-------------------|
| Selection bias | Either direction |
| Information bias (non-differential) | Toward null |
| Information bias (differential) | Either direction |
| Confounding | Either direction |
| Publication bias | Away from null |
| P-hacking | Away from null |

## Evaluating Bias Risk

### Key Questions

1. **Selection**: How were participants selected? Is the sample representative?
2. **Information**: How were exposures/outcomes measured? Is measurement comparable across groups?
3. **Confounding**: Were potential confounders identified and controlled?
4. **Analysis**: Were analyses pre-specified? Were all results reported?
5. **Reporting**: Were results selectively reported?

### Overall Risk Assessment

| Rating | Criteria |
|--------|----------|
| Low | All domains at low risk |
| Moderate | Some domains at moderate risk, none at high |
| High | One or more domains at high risk |
| Critical | Fundamental flaws that invalidate results |