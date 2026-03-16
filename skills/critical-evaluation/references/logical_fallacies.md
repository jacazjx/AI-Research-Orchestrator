# Logical Fallacies

This document catalogs logical fallacies commonly encountered in research reasoning.

## Causation Fallacies

### Post Hoc Ergo Propter Hoc

**Definition**: Assuming that because B followed A, A caused B.

**Latin**: "After this, therefore because of this"

**Example**: "The economy improved after the new policy, so the policy caused the improvement."

**Detection**:
- Temporal sequence is only evidence for causation
- No alternative explanations considered
- No control for other factors

**Remedy**:
- Apply Bradford Hill criteria
- Consider alternative explanations
- Look for dose-response relationship
- Seek replication

### Cum Hoc Ergo Propter Hoc

**Definition**: Assuming that correlation implies causation.

**Latin**: "With this, therefore because of this"

**Example**: "Ice cream sales and drowning deaths are correlated, so ice cream causes drowning."

**Detection**:
- Correlation presented as evidence of causation
- No mechanism proposed
- No control for confounders
- Spurious correlations

**Remedy**:
- Consider third variables (confounders)
- Establish temporal sequence
- Look for mechanism
- Conduct controlled experiments

### Reverse Causation

**Definition**: Assuming A causes B when B actually causes A.

**Example**: "People who are depressed have low vitamin D, so low vitamin D causes depression." (Could depression cause lower outdoor activity and thus lower vitamin D?)

**Detection**:
- Cross-sectional data only
- No temporal sequence
- Plausible reverse mechanism
- No longitudinal evidence

**Remedy**:
- Use longitudinal designs
- Consider both causal directions
- Apply cross-lagged analyses
- Use instrumental variables

### Circular Reasoning (Begging the Question)

**Definition**: Conclusion is assumed in the premises.

**Example**: "This treatment is effective because it works."

**Detection**:
- Premise restates conclusion
- No independent evidence
- Definition presented as argument

**Remedy**:
- Identify the premises and conclusion
- Ensure premises provide independent support
- Provide external evidence

### Third Variable Problem

**Definition**: An unmeasured variable causes both observed variables.

**Example**: "Children with larger shoes read better, so big feet help reading." (Age causes both.)

**Detection**:
- Observed association without plausible mechanism
- Potential common causes not measured
- Paradoxical or surprising findings

**Remedy**:
- Identify potential confounders
- Measure and control for confounders
- Use randomization when possible
- Consider alternative explanations

## Generalization Fallacies

### Hasty Generalization

**Definition**: Drawing a general conclusion from insufficient or unrepresentative evidence.

**Example**: "We tested our algorithm on two datasets, so it will work on all datasets."

**Detection**:
- Small sample size
- Non-representative sample
- Broad claims from limited data
- No acknowledgment of limitations

**Remedy**:
- Increase sample size
- Use representative sampling
- Qualify conclusions appropriately
- Test across diverse conditions

### Sampling Bias / Selection Bias

**Definition**: Drawing conclusions from a non-representative sample.

**Example**: "Our survey found that 90% of people love our product" (survey only sent to existing customers).

**Detection**:
- Convenience sampling
- Self-selection into study
- Missing demographic groups
- Sample characteristics don't match population

**Remedy**:
- Use random sampling
- Report sample demographics
- Acknowledge selection effects
- Weight results appropriately

### Ecological Fallacy

**Definition**: Applying group-level findings to individuals.

**Example**: "Countries with higher wine consumption have longer life expectancy, so drinking wine makes you live longer." (Individuals who drink wine may not live longer.)

**Detection**:
- Group-level data used for individual conclusions
- Aggregate associations don't hold at individual level
- No individual-level analysis

**Remedy**:
- Analyze at appropriate level
- Use multilevel modeling
- Acknowledge level of analysis
- Verify with individual-level data

### Exception Fallacy (Converse of Ecological Fallacy)

**Definition**: Applying individual-level findings to groups.

**Example**: "This successful individual came from poverty, so poverty doesn't hinder success."

**Detection**:
- Individual case generalized to population
- Survivorship bias
- Ignores base rates

**Remedy**:
- Use population-level data
- Consider base rates
- Recognize individual variation

### Anecdotal Evidence

**Definition**: Treating personal experiences or isolated cases as general evidence.

**Example**: "My aunt smoked and lived to 95, so smoking isn't harmful."

**Detection**:
- Stories instead of data
- Individual cases without context
- Ignores quantitative evidence

**Remedy**:
- Seek systematic evidence
- Consider sample size
- Use appropriate study designs

## Authority and Appeal Fallacies

### Appeal to Authority (Argumentum ad Verecundiam)

**Definition**: Accepting a claim because an authority figure said it, without supporting evidence.

**Example**: "Dr. X says this treatment works, so it must be true."

**Detection**:
- Authority cited instead of evidence
- Authority outside their expertise
- No primary evidence provided

**Remedy**:
- Examine the evidence, not the person
- Check if authority is an expert in relevant field
- Look for consensus in the field

### Appeal to Popularity (Argumentum ad Populum)

**Definition**: Accepting a claim because many people believe it.

**Example**: "Everyone uses this method, so it must be the best."

**Detection**:
- "Everyone knows" or "It is well established"
- Popularity as primary argument
- No evidence beyond widespread belief

**Remedy**:
- Examine evidence independently
- Consider historical examples of majority being wrong
- Look for empirical support

### Appeal to Tradition

**Definition**: Accepting a claim because it has been believed for a long time.

**Example**: "This approach has been used for decades, so it must be correct."

**Detection**:
- Tradition cited as evidence
- No current evidence provided
- Resistance to new methods

**Remedy**:
- Examine evidence independently
- Consider that traditions can be wrong
- Look for recent validation

### Appeal to Novelty

**Definition**: Accepting a claim because it is new or innovative.

**Example**: "Our new method is better because it uses deep learning."

**Detection**:
- Novelty as primary selling point
- No comparison to existing methods
- Assumption that newer is better

**Remedy**:
- Require empirical comparison
- Test against established baselines
- Don't assume novelty implies superiority

## Statistical Fallacies

### Gambler's Fallacy

**Definition**: Believing that past random events affect future probabilities.

**Example**: "This coin has landed heads five times, so tails is due."

**Detection**:
- Expectation of "correction" in random sequences
- Misunderstanding of independence
- Predicting random events based on history

**Remedy**:
- Understand independence of random events
- Calculate actual probabilities
- Regression to mean is not a "correction"

### Base Rate Fallacy

**Definition**: Ignoring population prevalence when interpreting probabilities.

**Example**: "The test is 99% accurate, so a positive result means I'm 99% likely to have the disease." (Ignores low base rate.)

**Detection**:
- Test accuracy discussed without prevalence
- Conditional probabilities confused
- No consideration of prior probability

**Remedy**:
- Apply Bayes' theorem
- Consider base rates
- Calculate positive predictive value

### Prosecutor's Fallacy

**Definition**: Confusing P(evidence|innocent) with P(innocent|evidence).

**Example**: "The probability of this DNA match if innocent is 1 in a million, so the probability of innocence is 1 in a million."

**Detection**:
- P(E|H) confused with P(H|E)
- Prior probability ignored
- Bayes' theorem violated

**Remedy**:
- Apply Bayes' theorem
- Consider prior probability
- Calculate posterior probability

### Simpson's Paradox

**Definition**: Trend in groups reverses when groups are combined.

**Example**: Treatment A has higher success rate than Treatment B in each subgroup, but Treatment B has higher overall success rate.

**Detection**:
- Different group sizes
- Confounding between treatment and group
- Aggregate results contradict subgroup results

**Remedy**:
- Analyze by relevant subgroups
- Consider confounding variables
- Use stratified analysis or regression

### Regression Fallacy

**Definition**: Attributing natural regression to the mean to an intervention.

**Example**: "The treatment worked because patients improved after receiving it." (Patients selected because they were at their worst would have improved anyway.)

**Detection**:
- Subjects selected for extreme scores
- No control group
| Improvement following intervention
- Natural variation not considered

**Remedy**:
- Use control groups
- Understand regression to mean
- Consider natural history

### Texas Sharpshooter Fallacy

**Definition**: Defining the target after shooting to make it look like a hit.

**Example**: "Our algorithm performs well on these specific tasks" (tasks chosen because algorithm performs well on them).

**Detection**:
- Outcomes defined after seeing data
| Subgroups chosen post-hoc
- Results not pre-registered
- Moving goalposts

**Remedy**:
- Pre-specify hypotheses and analyses
- Distinguish confirmatory from exploratory
| Report all tests conducted

## Reasoning Fallacies

### False Dilemma (False Dichotomy)

**Definition**: Presenting only two options when more exist.

**Example**: "Either we use this method or we abandon the project."

**Detection**:
- Only two alternatives presented
- Middle ground ignored
- "Either X or Y" framing

**Remedy**:
- Identify additional options
- Consider middle ground
| Challenge binary framing

### Straw Man

**Definition**: Misrepresenting an argument to make it easier to attack.

**Example**: "They want to regulate AI, which means they want to stop all AI development." (Misrepresents position.)

**Detection**:
- Opponent's position simplified or exaggerated
- Argument attacked that wasn't made
- No steel-manning of opposing view

**Remedy**:
- Represent arguments fairly
- Steel-man opposing views
- Address actual arguments made

### Slippery Slope

**Definition**: Claiming a small step will inevitably lead to a chain of related events.

**Example**: "If we allow this, it will lead to complete chaos."

**Detection**:
- Chain of predictions without evidence
- Each step not justified
- Extreme consequences from small changes

**Remedy**:
- Examine each step independently
- Require evidence for each link
| Consider where chain might break

### Ad Hominem

**Definition**: Attacking the person making an argument rather than the argument.

**Example**: "Their research can't be trusted because they have industry funding."

**Detection**:
- Focus on source rather than argument
- Personal attacks
- Funding or affiliation used to dismiss

**Remedy**:
- Evaluate arguments independently
- Consider evidence regardless of source
- Acknowledge biases but evaluate merit

### No True Scotsman

**Definition**: Redefining terms to exclude counterexamples.

**Example**: "No real scientist would question this theory." (Anyone who questions is defined as not a real scientist.)

**Detection**:
- Counterexamples excluded by definition
- Terms redefined when challenged
- Circular definition

**Remedy**:
- Define terms clearly and consistently
- Accept counterexamples as evidence
- Revise claims rather than definitions

## Fallacy Detection Checklist

### For Causal Claims

- [ ] Is temporal sequence established?
- [ ] Are alternative explanations considered?
- [ ] Are confounders controlled?
- [ ] Is the mechanism plausible?
- [ ] Is there dose-response relationship?
- [ ] Are results replicated?

### For Generalizations

- [ ] Is sample size adequate?
- [ ] Is sample representative?
- [ ] Are conclusions appropriately qualified?
- [ ] Is the level of analysis correct?
- [ ] Are individual cases distinguished from population patterns?

### For Appeals

- [ ] Is evidence provided beyond authority?
- [ ] Is authority an expert in the relevant field?
- [ ] Is popularity distinguished from correctness?
- [ ] Is tradition distinguished from evidence?

### For Statistical Claims

- [ ] Are probabilities interpreted correctly?
- [ ] Are base rates considered?
- [ ] Is regression to mean considered?
- [ ] Are subgroup patterns examined?
- [ ] Are outcomes pre-specified?

## Fallacy Severity Assessment

| Severity | Criteria | Action |
|----------|----------|--------|
| Critical | Fallacy invalidates main conclusion | Major revision required |
| Major | Fallacy significantly weakens argument | Address before publication |
| Moderate | Fallacy affects secondary claims | Note and correct |
| Minor | Fallacy in peripheral discussion | Consider correcting |