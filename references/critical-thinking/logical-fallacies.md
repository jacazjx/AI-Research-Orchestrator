# Logical Fallacies

## Overview

Logical fallacies are errors in reasoning that undermine the validity of arguments. Recognizing these fallacies is essential for critical evaluation of research claims and scientific literature.

## Classification

### Formal vs. Informal Fallacies

| Type | Description | Example |
|------|-------------|---------|
| Formal | Invalid logical structure | All A are B; All B are C; Therefore all C are A |
| Informal | Content-based errors | Ad hominem, straw man |

## Causation Fallacies

### Post Hoc Ergo Propter Hoc

"After this, therefore because of this"

**Definition:** Assuming temporal sequence implies causation.

**Example:**
```
"I took vitamin C and my cold went away.
Therefore, vitamin C cured my cold."
```

**Detection:**
- Ask: Is there a control condition?
- Check for alternative explanations
- Look for replication across studies

**Correction:**
- Require controlled experiments
- Consider confounding variables
- Apply Bradford Hill criteria

### Cum Hoc Ergo Propter Hoc

"With this, therefore because of this" (Correlation implies causation)

**Definition:** Assuming correlation implies causation.

**Example:**
```
"Ice cream sales correlate with drowning deaths.
Therefore, ice cream causes drowning."
```

**Detection:**
- Look for third variables (temperature in example)
- Check for temporal precedence
- Examine dose-response relationship

### Reverse Causation

**Definition:** Assuming wrong direction of causal relationship.

**Example:**
```
"Depressed people have lower serotonin.
Therefore, low serotonin causes depression."

(Alternative: Depression may cause lower serotonin)
```

**Detection:**
- Consider bidirectional relationships
- Look for longitudinal data
- Apply theoretical understanding

## Generalization Fallacies

### Hasty Generalization

**Definition:** Drawing broad conclusions from insufficient evidence.

**Example:**
```
"Two studies found an effect.
Therefore, the effect is robust."
```

**Detection:**
- Check sample sizes
- Look for meta-analyses
- Verify representativeness

### Sampling Bias

**Definition:** Generalizing from non-representative samples.

**Example:**
```
"WEIRD samples (Western, Educated, Industrialized,
Rich, Democratic) represent human psychology."
```

**Detection:**
- Check recruitment methods
- Examine demographic characteristics
- Consider generalizability explicitly

### Ecological Fallacy

**Definition:** Applying group-level findings to individuals.

**Example:**
```
"Countries with higher chocolate consumption have
more Nobel laureates. Therefore, eating chocolate
makes you smarter."
```

**Detection:**
- Distinguish aggregate vs. individual data
- Consider within-group variation
- Apply multilevel modeling

## Relevance Fallacies

### Ad Hominem

**Definition:** Attacking the person instead of the argument.

**Types:**
- Abusive: Direct attack on character
- Circumstantial: Attack on circumstances
- Tu quoque: "You do it too"

**Example:**
```
"Dr. Smith's research is flawed because he has
a conflict of interest."
```

**Response:**
- Address the argument itself
- Consider evidence independently
- Note: Conflicts of interest are relevant but don't invalidate findings

### Appeal to Authority

**Definition:** Relying on authority rather than evidence.

**Example:**
```
"Einstein said quantum mechanics is incomplete,
so it must be wrong."
```

**Detection:**
- Check if authority is expert in relevant field
- Look for supporting evidence
- Consider consensus among experts

### Appeal to Novelty

**Definition:** Assuming new means better.

**Example:**
```
"This new algorithm must be superior because it
uses the latest deep learning techniques."
```

**Detection:**
- Compare against established baselines
- Require empirical validation
- Check for proper ablation studies

### Appeal to Tradition

**Definition:** Assuming old means correct.

**Example:**
```
"We've always done it this way, so it must be
the right approach."
```

## Ambiguity Fallacies

### Equivocation

**Definition:** Using a word with multiple meanings.

**Example:**
```
"Evolution is just a theory. Therefore, it's not
proven." (Confusing scientific theory with guess)
```

**Detection:**
- Check for term definitions
- Ensure consistent usage
- Clarify meanings explicitly

### Amphiboly

**Definition:** Ambiguous sentence structure leads to misinterpretation.

**Example:**
```
"Research shows that the method works."
(Which research? What method? Works for what?)
```

## Statistical Fallacies

### Gambler's Fallacy

**Definition:** Expecting regression to mean in independent events.

**Example:**
```
"We've had 10 coin flips landing heads.
The next one must be tails."
```

### Base Rate Fallacy

**Definition:** Ignoring population prevalence.

**Example:**
```
"A test is 99% accurate. You tested positive.
Therefore, you have a 99% chance of having the disease."
(Ignores base rate of disease in population)
```

**Detection:**
- Apply Bayes' theorem
- Consider prior probabilities
- Calculate positive predictive value

```python
def positive_predictive_value(sensitivity, specificity, prevalence):
    """
    Calculate PPV considering base rate.
    """
    p_pos_given_disease = sensitivity
    p_pos_given_healthy = 1 - specificity

    p_pos = (prevalence * p_pos_given_disease +
             (1 - prevalence) * p_pos_given_healthy)

    ppv = (prevalence * p_pos_given_disease) / p_pos
    return ppv

# Example: 99% accurate test, 1% prevalence
ppv = positive_predictive_value(0.99, 0.99, 0.01)
print(f"PPV = {ppv:.1%}")  # Only ~50%!
```

### Prosecutor's Fallacy

**Definition:** Confusing P(evidence|innocent) with P(innocent|evidence).

**Example:**
```
"The DNA match probability is 1 in a million.
Therefore, there's a 99.9999% chance the defendant
is guilty."
```

### Simpson's Paradox

**Definition:** Trend reverses when groups are combined.

**Example:**
```
Treatment A has higher success rate in both
mild and severe cases. But when combined,
Treatment B appears better (due to case mix).
```

**Detection:**
- Always analyze subgroups
- Consider confounding variables
- Use stratified analysis

## Begging the Question

### Circular Reasoning

**Definition:** Conclusion is assumed in premises.

**Example:**
```
"The model is accurate because it makes correct
predictions, and we know the predictions are correct
because the model is accurate."
```

### Loaded Question

**Definition:** Question contains unjustified assumption.

**Example:**
```
"Have you stopped using the flawed methodology?"
(Assumes methodology was flawed)
```

## False Dichotomy

**Definition:** Presenting only two options when more exist.

**Example:**
```
"Either this finding replicates or the original
study was fraudulent."
(Ignores: different population, methodology, etc.)
```

**Detection:**
- Look for "either/or" language
- Consider middle positions
- Check for continuum of possibilities

## Straw Man

**Definition:** Misrepresenting an argument to make it easier to attack.

**Example:**
```
Original: "We should be cautious about this finding."
Straw man: "They claim the finding is worthless."
```

**Detection:**
- Check if strongest version is addressed
- Look for charitable interpretation
- Verify original claim

## Slippery Slope

**Definition:** Assuming small step leads to extreme outcome.

**Example:**
```
"If we accept this minor assumption, we'll end up
rejecting all established science."
```

**Detection:**
- Look for intermediate steps
- Check plausibility of each step
- Consider mitigation mechanisms

## Fallacies in AI/ML Research

### Overclaiming from Benchmarks

**Example:**
```
"Our model achieves SOTA on benchmark X.
Therefore, it represents true intelligence."
```

### Anthropomorphizing Models

**Example:**
```
"The model understands language because it
generates coherent text."
```

### Dataset Bias Generalization

**Example:**
```
"Our model works well on ImageNet.
Therefore, it will work on real-world images."
```

## Detection Checklist

When evaluating arguments, check for:

- [ ] **Causation**: Is causal claim supported by experimental evidence?
- [ ] **Sample**: Is the sample size adequate and representative?
- [ ] **Generalization**: Do conclusions match scope of evidence?
- [ ] **Authority**: Is claim supported by evidence, not just authority?
- [ ] **Base rates**: Are prior probabilities considered?
- [ ] **Alternatives**: Are alternative explanations addressed?
- [ ] **Definitions**: Are key terms clearly defined?
- [ ] **Scope**: Is the argument charitable to opposing views?

## References

- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty
- Nisbett, R. E., & Ross, L. (1980). Human inference
- Baron, J. (2008). Thinking and deciding