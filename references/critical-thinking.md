# Critical Thinking

A unified reference for logical fallacies, cognitive biases, argument analysis, and evidence evaluation in AI/ML research contexts.

---

## Logical Fallacies

### Causation Fallacies

| Fallacy | Definition | AI/ML Example |
|---------|------------|---------------|
| Post Hoc | Assuming temporal sequence implies causation | "I added dropout and accuracy improved, so dropout caused the improvement" |
| Correlation=Causation | Assuming correlation implies causation | "Models with more parameters correlate with higher accuracy, so more parameters cause better accuracy" |
| Reverse Causation | Wrong direction of causal relationship | Confusing cause and effect in feature importance |

**Detection:** Ask if there is a control condition, check for alternative explanations, look for replication.

### Generalization Fallacies

| Fallacy | Definition | AI/ML Example |
|---------|------------|---------------|
| Hasty Generalization | Broad conclusions from insufficient evidence | "Two studies found an effect, therefore it is robust" |
| Sampling Bias | Generalizing from non-representative samples | WEIRD datasets representing all domains |
| Ecological Fallacy | Group-level findings applied to individuals | Aggregate benchmark results assumed to hold per-instance |

### Relevance Fallacies

| Fallacy | Definition | Detection |
|---------|------------|-----------|
| Ad Hominem | Attacking the person not the argument | Address the argument itself |
| Appeal to Authority | Relying on authority over evidence | Check supporting evidence directly |
| Appeal to Novelty | Assuming new means better | Compare against established baselines |
| Appeal to Tradition | Assuming old means correct | Evaluate on current merits |

### Statistical Fallacies

| Fallacy | Definition | Detection |
|---------|------------|-----------|
| Base Rate Fallacy | Ignoring population prevalence | Apply Bayes' theorem |
| Gambler's Fallacy | Expecting regression in independent events | Verify independence |
| Simpson's Paradox | Trend reverses when groups are combined | Always analyze subgroups |
| Prosecutor's Fallacy | Confusing P(evidence|hypothesis) with P(hypothesis|evidence) | Distinguish conditional probabilities |

### Structural Fallacies

| Fallacy | Definition | Detection |
|---------|------------|-----------|
| False Dichotomy | Only two options when more exist | Look for "either/or" language |
| Straw Man | Misrepresenting an argument | Check if strongest version is addressed |
| Circular Reasoning | Conclusion assumed in premises | Check for self-referential logic |
| Slippery Slope | Small step leads to extreme outcome | Check plausibility of each intermediate step |
| Equivocation | Using a word with multiple meanings | Ensure consistent term definitions |

### AI/ML-Specific Fallacies

- **Overclaiming from Benchmarks**: "SOTA on benchmark X implies true intelligence"
- **Anthropomorphizing Models**: "The model understands language because it generates coherent text"
- **Dataset Bias Generalization**: "Works on ImageNet, therefore works on real-world images"

### Fallacy Detection Checklist

- [ ] **Causation**: Is causal claim supported by experimental evidence?
- [ ] **Sample**: Is the sample size adequate and representative?
- [ ] **Generalization**: Do conclusions match scope of evidence?
- [ ] **Authority**: Is claim supported by evidence, not just authority?
- [ ] **Base rates**: Are prior probabilities considered?
- [ ] **Alternatives**: Are alternative explanations addressed?
- [ ] **Definitions**: Are key terms clearly defined?
- [ ] **Scope**: Is the argument charitable to opposing views?

---

## Cognitive Biases

### Research Phase Susceptibility

| Research Phase | Susceptible Biases |
|---|---|
| Question Formulation | Confirmation Bias, Availability |
| Literature Review | Confirmation Bias, Selection Bias |
| Experimental Design | Bias Blind Spot, Optimism Bias |
| Data Collection | Sampling Bias, Observer Bias |
| Analysis | P-hacking, HARKing, Publication Bias |
| Interpretation | Confirmation Bias, Sunk Cost Fallacy |
| Publication | Publication Bias, Outcome Reporting |

### Key Biases

#### Confirmation Bias

The tendency to search for, interpret, and recall information confirming prior beliefs.

**Self-Assessment:**
- [ ] Have I considered alternative hypotheses equally?
- [ ] Am I testing against the strongest baselines?
- [ ] Would I accept negative results as meaningful?
- [ ] Have I sought out contradictory evidence?

**Mitigation:** Adversarial testing, devil's advocate analysis, blind analysis.

#### Publication Bias

Preferential publication of positive or novel results.

**Impact:** Overstated performance, wasted research effort, distorted progress perception.

**Mitigation:** Preregister studies, publish null/negative results, report all conditions.

#### HARKing (Hypothesizing After Results Known)

Presenting post-hoc hypotheses as if they were a priori.

**Red Flags:**
- Hypothesis perfectly matches results
- No mention of alternative approaches tried
- No negative or null results reported
- Hyperparameters seem "magically" optimal

**Mitigation:** Preregistration, clearly distinguish exploratory from confirmatory analyses.

#### P-hacking and Multiple Comparisons

Analyzing data in multiple ways to find statistically significant results.

**Common Practices in AI/ML:**
- Try many metrics, report only significant ones
- Run many experiments, report only successes
- Select favorable random seeds
- Compare to weak baselines

**Correction Methods:**
- **Bonferroni**: Divide alpha by number of tests (conservative)
- **Benjamini-Hochberg**: Controls false discovery rate (less conservative)

**Prevention Checklist:**
- [ ] Preregister primary hypotheses and analysis plan
- [ ] Specify primary outcome metric in advance
- [ ] Apply multiple comparison correction
- [ ] Report all tests conducted
- [ ] Distinguish exploratory from confirmatory

#### Sunk Cost Fallacy

Continuing an endeavor due to prior investment despite poor prospects.

**Fresh Start Test:** "If starting today with no prior investment, would I choose this project?"

**Forward-Looking Costs (Consider These):**
- Time remaining to completion
- Compute remaining needed
- Alternative uses of resources
- Value of expected outcomes

**Sunk Costs (Ignore These):**
- Time already invested
- Compute already used
- Code already written

#### Other Important Biases

| Bias | Definition | Primary Mitigation |
|------|------------|-------------------|
| Anchoring | Over-relying on first information | Use multiple starting points |
| Availability | Over-weighting available/recent info | Systematic review |
| Selection | Non-representative samples | Representative sampling |
| Optimism | Overestimating success probability | Pre-mortem analysis, reference class forecasting |
| Bias Blind Spot | Believing you are less biased than others | Assume you are biased, seek external review |

---

## Argument Analysis

### Argument Components

Every argument consists of:
- **Premises (P)**: Starting points, assumptions, or evidence
- **Inference (arrow)**: Logical movement from premises to conclusion (deductive, inductive, or abductive)
- **Conclusion (C)**: The claim being supported

### Argument Types

| Type | Direction | Certainty | AI/ML Example |
|------|-----------|-----------|---------------|
| Deductive | General to specific | Certain (if valid) | Theorem proving, algorithm correctness |
| Inductive | Specific to general | Probabilistic | Empirical results, generalization |
| Abductive | Inference to best explanation | Plausible | Model debugging, hypothesis formation |

### Evaluation Criteria

1. **Truth of Premises**: Are premises factually correct with adequate evidence?
2. **Relevance of Premises**: Do premises actually support the conclusion?
3. **Sufficiency of Support**: Is support strong enough for the conclusion?
4. **Handling of Counter-Arguments**: Are objections addressed?
5. **Clarity and Coherence**: Is the argument clearly expressed?

### Toulmin Model

| Element | Description |
|---------|-------------|
| Claim (C) | The conclusion being argued for |
| Data (D) | Facts or evidence supporting the claim |
| Warrant (W) | Reasoning connecting data to claim |
| Backing (B) | Support for the warrant |
| Qualifier (Q) | Degree of certainty |
| Rebuttal (R) | Conditions under which the claim does not hold |

### Analysis Workflow

1. **Extraction**: Identify conclusion, list premises (explicit and implicit), note inference type
2. **Evaluation**: Evaluate each premise for truth, check inference validity, check for fallacies
3. **Critical Response**: Identify weaknesses, generate counter-arguments, suggest improvements

### Research Claim Template

```markdown
### The Claim
[State central claim clearly]

### The Evidence
1. [Primary evidence] - Source: [...] - Strength: [...]

### The Reasoning
[How evidence supports the claim]

### Qualifications
[Limitations, conditions, uncertainties]

### Counter-Arguments Addressed
1. [Objection] - Response: [...]

### Conclusion (Qualified)
[Restate with appropriate qualifications]
```

### Dialectical Reasoning

```
THESIS -> Initial position
  |
ANTITHESIS -> Counter-position
  |
SYNTHESIS -> Resolution incorporating insights from both
```

---

## Evidence Evaluation

### Evidence Types for AI/ML

| Type | Examples |
|------|---------|
| Experimental | Controlled experiments, A/B tests, laboratory studies |
| Observational | Cohort studies, cross-sectional studies, natural experiments |
| Theoretical | Mathematical proofs, complexity analysis, formal verification |
| Computational | Benchmark results, simulation studies, ablation studies |
| Expert | Expert consensus, peer review, community knowledge |

### Evidence Hierarchy (AI/ML Adapted)

| Level | Evidence Type |
|-------|--------------|
| 1 (Strongest) | Theoretical proofs with empirical validation, large-scale RCTs, systematic reviews with meta-analyses |
| 2 (Strong) | Controlled experiments with proper baselines, multi-dataset studies, peer-reviewed with code |
| 3 (Moderate) | Single dataset experiments, observational studies, conference publications |
| 4 (Weak) | Case studies, expert opinion without data, preprints without peer review |
| 5 (Weakest) | Anecdotal evidence, marketing materials, claims without data |

### Quality Assessment Dimensions

| Dimension | Key Questions |
|-----------|---------------|
| Internal Validity | Does the design support causal claims? |
| External Validity | Can findings be generalized? |
| Construct Validity | Does it measure what it claims? |
| Statistical Validity | Are statistical conclusions sound? |
| Reliability | Can others replicate results? Are results stable? |
| Transparency | Are methods, data, and analysis fully described? |

### Evidence Strength Factors

| Factor | Key Question |
|--------|-------------|
| Effect Size | How large is the effect? Is it practically meaningful? |
| Precision | How wide are confidence intervals? |
| Consistency | Do results replicate across studies? |
| Directness | Does evidence directly address the question? |
| Dose-Response | Is there a dose-response relationship? |
| Plausibility | Is there a plausible mechanism? |

### Evidence Synthesis

| Pattern | Description | Action |
|---------|-------------|--------|
| Convergent | Multiple sources point to same conclusion | Strengthens confidence |
| Divergent | Sources point to different conclusions | Requires reconciliation |
| Complementary | Different aspects of the same question | Builds complete picture |
| Conflicting | Directly contradictory results | Requires investigation |

### Handling Conflicting Evidence

1. **Examine quality**: Higher quality evidence should weigh more
2. **Look for moderators**: What conditions affect outcomes?
3. **Consider effect sizes**: Are differences practically meaningful?
4. **Investigate methods**: Are there methodological explanations?
5. **Seek additional evidence**: Can new data resolve the conflict?

### Common Evidence Evaluation Errors

| Error | Correction |
|-------|-----------|
| Cherry-Picking | Systematically search for all relevant evidence |
| Equating All Evidence | Weight by quality and relevance |
| Overvaluing Recent Evidence | Consider recency but weight by quality |
| Undervaluing Negative Results | Give appropriate weight to all well-conducted studies |
| Authority Bias | Evaluate evidence on merits, not source prestige |
| Confirmatory Bias | Actively seek disconfirming evidence |
| Single-Study Syndrome | Seek convergent evidence from multiple sources |

### Self-Assessment Checklist

- [ ] Have I searched systematically for relevant evidence?
- [ ] Have I included evidence that contradicts my hypothesis?
- [ ] Have I assessed the quality of each piece of evidence?
- [ ] Have I weighted evidence appropriately?
- [ ] Have I considered alternative interpretations?
- [ ] Have I acknowledged limitations and uncertainties?
- [ ] Would someone with opposite views agree with my assessment?
