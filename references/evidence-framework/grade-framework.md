# GRADE Framework for Evidence Assessment

A comprehensive guide to the Grading of Recommendations Assessment, Development and Evaluation (GRADE) approach, adapted for AI/ML research contexts.

## Overview

The GRADE framework provides a systematic approach for assessing the quality of evidence and strength of recommendations. Originally developed for clinical medicine, it has been adapted here for AI/ML research evaluation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRADE FRAMEWORK OVERVIEW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TWO KEY JUDGMENTS:                                             │
│                                                                 │
│  1. QUALITY OF EVIDENCE                                        │
│     How confident are we in the estimates of effect?            │
│     ├── High: Very confident                                   │
│     ├── Moderate: Moderately confident                         │
│     ├── Low: Limited confidence                                │
│     └── Very Low: Very limited confidence                       │
│                                                                 │
│  2. STRENGTH OF RECOMMENDATION                                 │
│     How strong is the recommendation?                          │
│     ├── Strong: Benefits clearly outweigh harms                 │
│     └── Conditional: Benefits probably outweigh harms           │
│                                                                 │
│  THE PROCESS:                                                   │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐              │
│  │  ASK      │───▶│  ASSESS   │───▶│  RATE     │              │
│  │  Question │    │  Evidence │    │  Quality  │              │
│  └───────────┘    └───────────┘    └───────────┘              │
│        │                │                │                      │
│        ▼                ▼                ▼                      │
│   PICO format      GRADE criteria    4 levels                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. GRADE Quality of Evidence

### Four Levels of Evidence Quality

```
┌─────────────────────────────────────────────────────────────────┐
│              GRADE EVIDENCE QUALITY LEVELS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HIGH (⊕⊕⊕⊕)                                                    │
│  ├── We are very confident that the true effect lies close     │
│  │   to that of the estimate of the effect                     │
│  ├── Starting point for randomized controlled trials           │
│  └── AI/ML: Well-designed experiments with validation          │
│                                                                 │
│  MODERATE (⊕⊕⊕◯)                                               │
│  ├── We are moderately confident in the effect estimate         │
│  ├── The true effect is likely to be close to the estimate     │
│  │   but there is a possibility that it is substantially       │
│  │   different                                                 │
│  └── AI/ML: Studies with some limitations                      │
│                                                                 │
│  LOW (⊕⊕◯◯)                                                    │
│  ├── Our confidence in the effect estimate is limited           │
│  ├── The true effect may be substantially different from       │
│  │   the estimate                                              │
│  └── AI/ML: Observational studies, limited validation          │
│                                                                 │
│  VERY LOW (⊕◯◯◯)                                               │
│  ├── We have very little confidence in the effect estimate     │
│  ├── The true effect is likely to be substantially different   │
│  │   from the estimate                                         │
│  └── AI/ML: Case studies, expert opinion only                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Starting Points by Study Design

```markdown
## GRADE Starting Points (Adapted for AI/ML)

### Randomized Controlled Trials (RCTs) / Controlled Experiments
Initial rating: HIGH (⊕⊕⊕⊕)
Applicable to: A/B tests, controlled algorithm comparisons

### Observational Studies
Initial rating: LOW (⊕⊕◯◯)
Applicable to: Analysis of production logs, natural experiments

### Non-Randomized Controlled Studies
Initial rating: LOW to MODERATE (⊕⊕◯◯ to ⊕⊕⊕◯)
Applicable to: Before-after studies, interrupted time series

### Case Series / Case Reports
Initial rating: VERY LOW (⊕◯◯◯)
Applicable to: Single deployment examples, demonstrations

### Theoretical/Computational Analysis
Initial rating: Depends on rigor
- Formal proofs with assumptions tested: MODERATE
- Formal proofs with untested assumptions: LOW
- Theoretical arguments without proof: VERY LOW
```

---

## 2. Factors That Reduce Evidence Quality

### Five GRADE Domains for Downgrading

```
┌─────────────────────────────────────────────────────────────────┐
│          FACTORS THAT REDUCE EVIDENCE QUALITY                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. RISK OF BIAS (Study Limitations)                           │
│     ├── Lack of allocation concealment                         │
│     ├── Lack of blinding                                       │
│     ├── Incomplete outcome data                                │
│     ├── Selective outcome reporting                            │
│     ├── Other biases (e.g., baseline imbalance)                │
│     │                                                          │
│     │  AI/ML Adaptation:                                       │
│     ├── No proper baseline comparison                          │
│     ├── Data leakage between train/test                        │
│     ├── Selective metric reporting                             │
│     ├── Hyperparameter tuning on test set                      │
│     └── Single random seed without uncertainty                 │
│                                                                 │
│  2. INCONSISTENCY                                               │
│     ├── Unexplained heterogeneity of results                   │
│     ├── Wide confidence intervals                              │
│     ├── Different directions of effect                         │
│     │                                                          │
│     │  AI/ML Adaptation:                                       │
│     ├── Results vary across datasets without explanation       │
│     ├── Inconsistent results across runs/seeds                 │
│     ├── Inconsistent results across similar tasks              │
│     └── Large variance in reported results                     │
│                                                                 │
│  3. INDIRECTNESS                                               │
│     ├── Indirect population                                    │
│     ├── Indirect intervention                                  │
│     ├── Indirect comparison                                    │
│     ├── Indirect outcomes                                      │
│     │                                                          │
│     │  AI/ML Adaptation:                                       │
│     ├── Benchmark not representative of target domain          │
│     ├── Proxy metrics instead of real-world outcomes           │
│     ├── Simulation instead of deployment                       │
│     └── Different task than intended application               │
│                                                                 │
│  4. IMPRECISION                                                │
│     ├── Wide confidence intervals                              │
│     ├── Small sample size                                      │
│     ├── Few events                                             │
│     │                                                          │
│     │  AI/ML Adaptation:                                       │
│     ├── Few random seeds/runs                                  │
│     ├── No confidence intervals reported                       │
│     ├── Small test sets                                        │
│     └── High variance in results                               │
│                                                                 │
│  5. PUBLICATION BIAS                                            │
│     ├── Strong suspicion of publication bias                   │
│     ├── Small study effects                                    │
│     │                                                          │
│     │  AI/ML Adaptation:                                       │
│     ├── Selective reporting of results                         │
│     ├── Only positive results published                        │
│     ├── Failed experiments not disclosed                       │
│     └── Cherry-picked baselines or datasets                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Risk of Bias Assessment for AI/ML Studies

```markdown
## Risk of Bias Assessment (AI/ML Adapted)

### Selection Bias
- [ ] Low risk: Random assignment, stratified sampling
- [ ] Unclear: Method not clearly described
- [ ] High risk: Non-random, convenience sampling, no adjustment

### Performance Bias
- [ ] Low risk: Standardized protocols, automated execution
- [ ] Unclear: Protocol deviation unclear
- [ ] High risk: Different protocols across conditions

### Detection Bias
- [ ] Low risk: Automated metrics, blind evaluation
- [ ] Unclear: Evaluation method unclear
- [ ] High risk: Manual evaluation, not blinded, selective metrics

### Attrition Bias
- [ ] Low risk: All data analyzed, no exclusions
- [ ] Unclear: Exclusions not fully explained
- [ ] High risk: Selective exclusion of data

### Reporting Bias
- [ ] Low risk: All pre-specified outcomes reported
- [ ] Unclear: Unclear if all outcomes reported
- [ ] High risk: Selective outcome reporting

### AI/ML-Specific Biases
- [ ] Low risk: Proper train/val/test separation, no leakage
- [ ] Unclear: Data separation not clearly described
- [ ] High risk: Data leakage, test set used for tuning

### Assessment Table

| Bias Type | Judgment | Support for Judgment |
|-----------|----------|----------------------|
| Selection | [L/U/H] | [Explain] |
| Performance | [L/U/H] | [Explain] |
| Detection | [L/U/H] | [Explain] |
| Attrition | [L/U/H] | [Explain] |
| Reporting | [L/U/H] | [Explain] |
| AI/ML Specific | [L/U/H] | [Explain] |
| **Overall** | [L/U/H] | [Explain] |
```

---

## 3. Factors That Increase Evidence Quality

### Three Domains for Upgrading

```
┌─────────────────────────────────────────────────────────────────┐
│          FACTORS THAT INCREASE EVIDENCE QUALITY                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. LARGE EFFECT SIZE                                           │
│     └── Very large effect (e.g., RR > 2 or RR < 0.5)           │
│                                                                 │
│     AI/ML Adaptation:                                           │
│     ├── Effect size >> typical improvements                     │
│     ├── Cohen's d > 0.8 (large effect)                         │
│     ├── Performance far exceeds baselines                       │
│     └── Practical significance clearly demonstrated             │
│                                                                 │
│  2. DOSE-RESPONSE GRADIENT                                      │
│     └── Consistent dose-response relationship                  │
│                                                                 │
│     AI/ML Adaptation:                                           │
│     ├── Performance scales with model size as predicted         │
│     ├── Performance scales with data size as predicted          │
│     ├── Clear relationship between intervention and outcome     │
│     └── Ablation shows component importance                     │
│                                                                 │
│  3. CONFOUNDING MINIMIZES EFFECT                                │
│     └── Plausible confounding would reduce effect              │
│                                                                 │
│     AI/ML Adaptation:                                           │
│     ├── Residual confounding would favor the alternative       │
│     ├── Conservative analysis still shows effect                │
│     └── Lower bound still practically significant               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Applying Upgrading Factors

```markdown
## When to Upgrade Evidence Quality

### Large Effect Size
Upgrade by 1 level if:
- Relative risk > 2 or < 0.5 (observational studies)
- Effect size (Cohen's d) > 0.8
- Performance improvement >> typical improvements in field

Upgrade by 2 levels if:
- Relative risk > 5 or < 0.2
- Effect size > 1.3
- Performance improvement is transformative

Caveats:
- Effect must be precisely estimated
- No serious risk of bias
- Effect is not due to data leakage or overfitting

### Dose-Response Gradient
Upgrade by 1 level if:
- Clear, consistent dose-response relationship
- Multiple dose levels tested
- Relationship predicted by theory

AI/ML Examples:
- Model performance scales predictably with parameters
- Training performance scales with data
- Component ablation shows clear contribution

### All Plausible Confounders Would Reduce Effect
Upgrade by 1 level if:
- Confounding would work against the observed effect
- Conservative analysis still shows meaningful effect
- Residual confounding explanations are implausible
```

---

## 4. GRADE Evidence Profiles

### Evidence Profile Structure

```markdown
## GRADE Evidence Profile Template

### Question: [PICO formatted question]

| Certainty | Study Design | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Effect Size | Overall Certainty |
|-----------|--------------|--------------|---------------|--------------|-------------|------------------|-------------|-------------------|
| [Initial] | [Design]     | [↓/none]     | [↓/none]      | [↓/none]     | [↓/none]    | [↓/none]         | [↑/none]    | [Final]           |

### Footnotes:
- [Explain each downgrade/upgrade]

### Summary of Findings:
[Plain language summary of the evidence]
```

### Example Evidence Profile (AI/ML Study)

```markdown
## Evidence Profile: Transfer Learning vs. Training from Scratch

### Question:
For image classification tasks with limited labeled data (P), does
transfer learning from ImageNet (I) compared to training from scratch (C)
improve classification accuracy (O)?

| Certainty Assessment | No. of Studies | Study Design | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Large Effect |
|---------------------|----------------|--------------|--------------|---------------|--------------|-------------|------------------|--------------|
|                     | 8 RCTs         | RCTs ⊕⊕⊕⊕    | Serious ↓    | Not serious   | Not serious  | Serious ↓   | Suspected ↓      | Large ↑      |
| **Final Certainty** |                |              |              |               |              |             |                  |              |
| **⊕⊕◯◯ LOW**        |                |              |              |               |              |             |                  |              |

### Effect:
Mean accuracy difference: +15.2% (95% CI: 12.1% to 18.3%)
Favors: Transfer learning

### Explanations:
1. **Risk of Bias (Serious ↓)**: Several studies did not properly tune
   baseline models; some used single random seeds
2. **Imprecision (Serious ↓)**: Wide confidence intervals in some studies;
   few studies reported uncertainty
3. **Publication Bias (Suspected ↓)**: Positive results more likely to be
   published; negative results may be underreported
4. **Large Effect (↑)**: Effect size > 0.8 (Cohen's d = 1.2), indicating
   large practical improvement

### Summary:
Transfer learning probably improves accuracy substantially compared to
training from scratch for image classification with limited data, but
confidence is limited by methodological issues and potential publication
bias. The effect is large enough that it likely holds despite these
concerns.
```

---

## 5. GRADE Recommendations

### Strength of Recommendations

```
┌─────────────────────────────────────────────────────────────────┐
│              STRENGTH OF RECOMMENDATIONS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STRONG RECOMMENDATION                                          │
│  ─────────────────────                                          │
│  Phrasing: "We recommend..." / "Should..."                      │
│                                                                 │
│  For users: Most would want the intervention                    │
│  For developers: The intervention should be implemented         │
│  Confidence: Benefits clearly outweigh harms                    │
│                                                                 │
│  CONDITIONS FOR STRONG:                                         │
│  ├── High or moderate certainty in estimates                    │
│  ├── Large effect size                                          │
│  ├── Consistent results across studies                          │
│  ├── Clear benefits with minimal harms                          │
│  └── Values and preferences align with recommendation           │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  CONDITIONAL RECOMMENDATION                                     │
│  ───────────────────────────                                    │
│  Phrasing: "We suggest..." / "Consider..."                      │
│                                                                 │
│  For users: Most would want the intervention, but many would not│
│  For developers: Need to consider context and user preferences  │
│  Confidence: Benefits probably outweigh harms                   │
│                                                                 │
│  CONDITIONS FOR CONDITIONAL:                                    │
│  ├── Low or very low certainty in estimates                     │
│  ├── Small or uncertain effect size                             │
│  ├── Inconsistent results                                       │
│  ├── Balance of benefits and harms is close                     │
│  └── Values and preferences vary significantly                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Factors Affecting Recommendation Strength

```markdown
## Factors Determining Recommendation Strength

### 1. Certainty of Evidence
Higher certainty → Stronger recommendation
- High certainty: Strong recommendation possible
- Moderate certainty: Strong or conditional
- Low certainty: Usually conditional
- Very low certainty: Conditional or no recommendation

### 2. Balance of Benefits and Harms
Clear benefit → Stronger recommendation
- Large net benefit: Strong recommendation
- Moderate net benefit: Strong or conditional
- Small net benefit: Conditional
- Uncertain balance: Conditional or no recommendation

### 3. Values and Preferences
Uniform values → Stronger recommendation
- Similar values across population: Strong recommendation possible
- Important variation in values: Conditional recommendation

### 4. Resource Implications
Reasonable cost → Stronger recommendation
- Negligible or acceptable cost: Strong recommendation possible
- Significant resource implications: May warrant conditional

### 5. Equity Considerations
Promotes equity → Stronger recommendation
- Improves equity: Supports strong recommendation
- Worsens equity: May warrant conditional or against

### 6. Feasibility
Highly feasible → Stronger recommendation
- Easily implemented: Strong recommendation possible
- Significant barriers: May warrant conditional
```

### Recommendation Framework

```python
# grade_recommendation.py

class GRADERecommendation:
    """
    Framework for developing GRADE-based recommendations
    """

    def __init__(self, question):
        self.question = question
        self.evidence_quality = None
        self.benefits = []
        self.harms = []
        self.values = None
        self.resources = None
        self.recommendation = None

    def set_evidence_quality(self, quality):
        """
        Set evidence quality (High, Moderate, Low, Very Low)
        """
        self.evidence_quality = quality

    def add_benefit(self, benefit, magnitude, certainty):
        """
        Add a benefit of the intervention
        """
        self.benefits.append({
            'benefit': benefit,
            'magnitude': magnitude,  # Large, Moderate, Small
            'certainty': certainty
        })

    def add_harm(self, harm, magnitude, certainty):
        """
        Add a harm/risk of the intervention
        """
        self.harms.append({
            'harm': harm,
            'magnitude': magnitude,
            'certainty': certainty
        })

    def assess_balance(self):
        """
        Assess balance of benefits and harms
        """
        benefit_score = self._calculate_score(self.benefits, 'benefit')
        harm_score = self._calculate_score(self.harms, 'harm')
        net_benefit = benefit_score - harm_score

        if net_benefit > 2:
            return "Clear net benefit"
        elif net_benefit > 0:
            return "Probable net benefit"
        elif net_benefit > -2:
            return "Balance uncertain"
        else:
            return "Net harm likely"

    def determine_recommendation_strength(self):
        """
        Determine recommendation strength
        """
        balance = self.assess_balance()

        if self.evidence_quality in ['High', 'Moderate']:
            if "Clear net benefit" in balance:
                return "Strong"
            elif "Probable net benefit" in balance:
                return "Strong" if self._values_aligned() else "Conditional"
            else:
                return "Conditional"
        else:  # Low or Very Low certainty
            if "Clear net benefit" in balance:
                return "Conditional"
            else:
                return "Conditional"

    def generate_recommendation(self):
        """
        Generate recommendation statement
        """
        strength = self.determine_recommendation_strength()
        balance = self.assess_balance()

        if strength == "Strong":
            phrase = "We recommend"
        else:
            phrase = "We suggest"

        # Generate recommendation text
        recommendation = f"""
## GRADE Recommendation

### Question
{self.question}

### Evidence Quality
{self.evidence_quality}

### Balance of Benefits and Harms
{balance}

### Benefits
"""
        for b in self.benefits:
            recommendation += f"- {b['benefit']} (Magnitude: {b['magnitude']})\n"

        recommendation += "\n### Harms/Risks\n"
        for h in self.harms:
            recommendation += f"- {h['harm']} (Magnitude: {h['magnitude']})\n"

        recommendation += f"""
### Recommendation Strength
{strength}

### Recommendation Statement
{phrase} [intervention] for [population] because [reasoning].

### Key Uncertainties
- [List remaining uncertainties]

### Implementation Considerations
- [Context-specific considerations]
"""
        return recommendation

    def _calculate_score(self, items, item_type):
        """Calculate weighted score for benefits or harms"""
        scores = {'Large': 3, 'Moderate': 2, 'Small': 1}
        return sum(scores.get(item['magnitude'], 1) for item in items)

    def _values_aligned(self):
        """Check if values and preferences align"""
        return self.values is None or self.values.get('aligned', True)
```

---

## 6. GRADE for AI/ML: Adapted Domains

### AI/ML-Specific Considerations

```markdown
## GRADE Adaptations for AI/ML Research

### Risk of Bias (AI/ML Specific)

#### Data-Related Bias
- Training/test contamination
- Distribution shift between training and deployment
- Selection bias in data collection
- Label noise and annotation bias

#### Methodological Bias
- Inappropriate baseline comparison
- Hyperparameter tuning on test data
- Selective metric reporting
- Single random seed (no uncertainty)

#### Reporting Bias
- Cherry-picked results
- Unreported failures
- Incomplete methodology description

### Inconsistency (AI/ML Specific)

#### Cross-Dataset Variation
- Performance varies across datasets
- Domain transfer issues
- Distribution mismatch

#### Implementation Variation
- Results depend on implementation
- Framework differences
- Hardware dependencies

#### Seed Sensitivity
- High variance across random seeds
- Sensitivity to initialization
- Training instability

### Indirectness (AI/ML Specific)

#### Benchmark Indirectness
- Benchmarks don't represent target domain
- Synthetic vs. real data
- Simplified task assumptions

#### Metric Indirectness
- Proxy metrics (accuracy vs. real-world success)
- Missing important metrics (fairness, robustness)
- Task-specific vs. general capability

#### Evaluation Indirectness
- Offline vs. online evaluation
- Simulation vs. deployment
- Short-term vs. long-term effects

### Imprecision (AI/ML Specific)

#### Statistical Imprecision
- Few experimental runs
- Small test sets
- No confidence intervals

#### Practical Imprecision
- Unclear computational requirements
- Unknown deployment characteristics
- Uncertain maintenance burden
```

---

## 7. GRADE Assessment Worksheet

### Complete Assessment Template

```markdown
## GRADE Evidence Assessment Worksheet

### SECTION A: QUESTION FORMULATION

**P**opulation:
[Who/what is the target?]

**I**ntervention:
[What is being evaluated?]

**C**omparator:
[What is it being compared to?]

**O**utcome:
[What outcomes are being measured?]

### SECTION B: EVIDENCE IDENTIFICATION

Studies included:
| # | Citation | Design | Sample Size |
|---|----------|--------|-------------|
| 1 | | | |
| 2 | | | |

### SECTION C: QUALITY ASSESSMENT

#### Initial Quality
[ ] High (RCTs) [ ] Low (Observational)

#### Risk of Bias
| Domain | Judgment | Support |
|--------|----------|---------|
| Selection | [L/U/H] | |
| Performance | [L/U/H] | |
| Detection | [L/U/H] | |
| Attrition | [L/U/H] | |
| Reporting | [L/U/H] | |
| AI/ML Specific | [L/U/H] | |

Overall Risk of Bias: [ ] Not serious [ ] Serious [ ] Very serious
Downgrade: [ ] None [ ] -1 [ ] -2

#### Inconsistency
[ ] Not serious [ ] Serious [ ] Very serious
Explanation:
Downgrade: [ ] None [ ] -1 [ ] -2

#### Indirectness
[ ] Not serious [ ] Serious [ ] Very serious
Explanation:
Downgrade: [ ] None [ ] -1 [ ] -2

#### Imprecision
[ ] Not serious [ ] Serious [ ] Very serious
Explanation:
Downgrade: [ ] None [ ] -1 [ ] -2

#### Publication Bias
[ ] Undetected [ ] Suspected
Explanation:
Downgrade: [ ] None [ ] -1

### SECTION D: FACTORS INCREASING QUALITY

#### Large Effect Size
[ ] No [ ] Yes, large [ ] Yes, very large
Upgrade: [ ] None [ ] +1 [ ] +2

#### Dose-Response
[ ] No [ ] Yes
Upgrade: [ ] None [ ] +1

#### Confounding Minimizes Effect
[ ] No [ ] Yes
Upgrade: [ ] None [ ] +1

### SECTION E: FINAL QUALITY

Starting Quality: [High/Moderate/Low/Very Low]
Downgrades: _____
Upgrades: _____
Final Quality: [High/Moderate/Low/Very Low]

### SECTION F: SUMMARY OF FINDINGS

Effect estimate:
Confidence interval:
Plain language summary:
```

---

## 8. Practical Applications

### Example 1: Evaluating a New Algorithm

```markdown
## GRADE Assessment: Transformer vs. LSTM for Sequence Modeling

### Question (PICO)
- **P**: Long sequence modeling tasks
- **I**: Transformer architecture
- **C**: LSTM architecture
- **O**: Task accuracy, training efficiency

### Evidence Quality Assessment

| Factor | Assessment | Action |
|--------|------------|--------|
| Starting quality | RCTs (controlled experiments) | High ⊕⊕⊕⊕ |
| Risk of bias | Some studies use weak LSTM baselines | Downgrade -1 |
| Inconsistency | Results consistent across tasks | No downgrade |
| Indirectness | Benchmarks may not represent all tasks | Downgrade -1 |
| Imprecision | Some studies few seeds, no CI | Downgrade -1 |
| Publication bias | Positive results more likely published | Suspected -1 |
| Large effect | Yes, substantial improvement | Upgrade +1 |

**Final Quality**: Moderate (⊕⊕⊕◯)

### Recommendation
"We suggest transformers over LSTMs for sequence modeling tasks,
particularly for long sequences. The improvement is substantial, but
the recommendation is conditional due to methodological limitations
in some studies and potential publication bias. Users should validate
on their specific task and consider computational constraints."

### Key Uncertainties
- Optimal for tasks with limited data
- Computational cost trade-offs
- Performance on very specific domains
```

### Example 2: Evaluating a Model Deployment

```markdown
## GRADE Assessment: Deploying ML Model in Production

### Question (PICO)
- **P**: Production environment for [specific application]
- **I**: Deploy ML model with continuous monitoring
- **C**: Continue with rule-based system
- **O**: System accuracy, user satisfaction, maintenance burden

### Evidence Quality Assessment

| Factor | Assessment | Action |
|--------|------------|--------|
| Starting quality | Observational (deployment data) | Low ⊕⊕◯◯ |
| Risk of bias | Non-randomized, before-after design | Serious -1 |
| Inconsistency | Results vary by deployment context | Serious -1 |
| Indirectness | Test environment vs. production | Not serious |
| Imprecision | Limited deployment duration | Serious -1 |
| Publication bias | Limited by internal nature | Not suspected |
| Large effect | Yes, significant improvement | Upgrade +1 |
| Dose-response | N/A | No upgrade |

**Final Quality**: Very Low (⊕◯◯◯)

### Recommendation
"We suggest piloting the ML model in a limited production environment
with careful monitoring before full deployment. The evidence for
improvement is suggestive but limited by study design and context
variability. This is a conditional recommendation requiring local
validation."

### Implementation Guidance
1. Start with A/B test in subset of traffic
2. Define clear success metrics before deployment
3. Establish rollback procedures
4. Monitor for distribution shift
5. Collect data for future evidence strengthening
```

---

## Summary: GRADE Quick Reference

### GRADE Process Flow

```
1. ASK → Formulate PICO question
2. SEARCH → Identify relevant evidence
3. ASSESS → Evaluate quality (5 downgrading factors)
4. CONSIDER → Apply upgrading factors
5. RATE → Determine final quality
6. DECIDE → Develop recommendation
7. COMMUNICATE → Present clearly
```

### Quality Rating Summary

| Starting Point | Possible Range | Typical After Assessment |
|----------------|----------------|--------------------------|
| RCTs | High to Very Low | High or Moderate |
| Observational | Low to High | Low or Moderate |
| Case Series | Very Low to Low | Very Low |

### Recommendation Language

| Strength | Language | Certainty Needed |
|----------|----------|------------------|
| Strong | "We recommend" / "Should" | Moderate-High |
| Conditional | "We suggest" / "Consider" | Any |
| Against | "We recommend against" | Moderate-High |

---

## References

1. Guyatt, G., et al. (2011). GRADE guidelines: A new series of articles. *J Clin Epidemiol*.
2. Balshem, H., et al. (2011). GRADE guidelines: Rating quality of evidence. *J Clin Epidemiol*.
3. Andrews, J., et al. (2013). GRADE guidelines: Going from evidence to recommendations. *BMJ*.
4. Schunemann, H., et al. (2013). GRADE handbook.
5. GRADE Working Group: http://www.gradeworkinggroup.org/