# Causal Inference Frameworks

## Overview

Causal inference provides methods to move beyond correlation to causation. This is critical in AI/ML research where we want to understand not just what happens, but why it happens.

## The Fundamental Problem

### Correlation ≠ Causation

$$
Corr(X, Y) \neq P(Y | do(X))
$$

The intervention distribution $P(Y | do(X))$ differs from observational $P(Y | X)$ when confounders exist.

### Counterfactual Framework

**Potential Outcomes (Rubin Causal Model):**

For each unit, there are potential outcomes:
- $Y(1)$: Outcome if treated
- $Y(0)$: Outcome if not treated

**Individual Causal Effect:**
$$
\tau_i = Y_i(1) - Y_i(0)
$$

**Problem:** We can never observe both $Y(1)$ and $Y(0)$ for the same unit.

**Average Treatment Effect (ATE):**
$$
ATE = E[Y(1) - Y(0)]
$$

## Directed Acyclic Graphs (DAGs)

### Basic Concepts

A DAG encodes causal assumptions:

```
    Confounder (C)
       /   \
      v     v
     X ───→ Y
     Treatment → Outcome
```

### Key Relationships

| Relationship | Diagram | Implication |
|--------------|---------|-------------|
| Chain | X → M → Y | X causes Y through M |
| Fork | X ← C → Y | Spurious correlation via C |
| Collider | X → C ← Y | Do NOT condition on C |

### d-Separation

Path is blocked if:
1. Contains a chain (A → B → C) where B is not conditioned on
2. Contains a fork (A ← B → C) where B is conditioned on
3. Contains a collider (A → B ← C) where B IS conditioned on

### Backdoor Criterion

To identify causal effect of X on Y:
1. Block all backdoor paths from X to Y
2. Do not unblock any new paths by conditioning

**Sufficient adjustment set:**
- Variables that block all backdoor paths
- Does not include descendants of X
- Does not include colliders

## Identification Strategies

### Randomization

**Gold standard:** Random assignment breaks all backdoor paths.

$$
E[Y(1) | X=1] = E[Y(1)] = E[Y | X=1]
$$

**In ML context:**
- Random hyperparameter assignment
- A/B testing
- Random data augmentation

### Regression Adjustment

Condition on confounders C:

$$
E[Y | do(X)] = \int E[Y | X, C] P(C) dC
$$

**Assumptions:**
- All confounders measured
- Correct functional form
- No unmeasured confounding

### Propensity Score Methods

**Propensity Score:**
$$
e(X) = P(T=1 | X)
$$

**Methods:**

| Method | Description |
|--------|-------------|
| Matching | Pair treated/control with similar scores |
| Stratification | Group by propensity score quantiles |
| IPW | Weight by $1/e(X)$ or $1/(1-e(X))$ |
| Doubly Robust | Combine outcome model and propensity |

**Inverse Probability Weighting (IPW):**
$$
\hat{ATE}_{IPW} = \frac{1}{n}\sum_{i=1}^{n} \frac{T_i Y_i}{e(X_i)} - \frac{(1-T_i) Y_i}{1-e(X_i)}
$$

### Instrumental Variables

**Instrument Z must:**
1. Affect treatment X (relevance)
2. Not affect Y except through X (exclusion)
3. Not be associated with confounders (independence)

**Two-Stage Least Squares:**

Stage 1: $\hat{X} = \gamma_0 + \gamma_1 Z$
Stage 2: $Y = \beta_0 + \beta_1 \hat{X} + \epsilon$

**Local Average Treatment Effect (LATE):**
$$
LATE = \frac{E[Y | Z=1] - E[Y | Z=0]}{E[X | Z=1] - E[X | Z=0]}
$$

### Regression Discontinuity

Exploit threshold-based treatment assignment:

$$
\tau_{RD} = \lim_{x \downarrow c} E[Y | X=x] - \lim_{x \uparrow c} E[Y | X=x]
$$

**Example in ML:**
- Model deployed above certain accuracy threshold
- Effect of deployment on downstream metrics

### Difference-in-Differences

Compare changes over time between treated and control:

$$
\tau_{DiD} = (Y_{T,post} - Y_{T,pre}) - (Y_{C,post} - Y_{C,pre})
$$

**Parallel trends assumption:**
- Without treatment, both groups would follow same trend

## Pearl's Do-Calculus

### Three Rules

**Rule 1 (Insertion/deletion of observations):**
$$
P(Y | do(X), Z, W) = P(Y | do(X), W)
$$
if $Y \perp Z | X, W$ in $G_{\overline{X}}$

**Rule 2 (Action/observation exchange):**
$$
P(Y | do(X), do(Z), W) = P(Y | do(X), Z, W)
$$
if $Y \perp Z | X, W$ in $G_{\overline{X}\underline{Z}}$

**Rule 3 (Insertion/deletion of actions):**
$$
P(Y | do(X), do(Z), W) = P(Y | do(X), W)
$$
if $Y \perp Z | X, W$ in $G_{\overline{X}, \overline{Z(W)}}$

### Identification Algorithm

```
1. Check if backdoor criterion satisfied
2. If not, apply do-calculus rules
3. Transform do-expression to observational
4. If unsuccessful, effect is not identifiable
```

## Sensitivity Analysis

### For Unmeasured Confounding

**E-value:** Minimum strength of association that unmeasured confounder would need with both treatment and outcome to explain away effect.

$$
E\text{-value} = RR + \sqrt{RR(RR-1)}
$$

**For effect estimate $\hat{\tau}$:**
1. How strong would confounder-treatment association need to be?
2. How strong would confounder-outcome association need to be?
3. Is this plausible given domain knowledge?

### Rosenbaum Bounds

For propensity score matching:
- How much would hidden bias need to change significance?
- Report sensitivity parameter $\Gamma$

## Causal Inference in Machine Learning

### Causal ML Applications

| Application | Causal Question |
|-------------|-----------------|
| Treatment effect estimation | What is HTE? |
| Feature importance | Does X cause Y? |
| Model interpretability | Counterfactual explanations |
| Fairness | Is prediction causally fair? |
| Domain adaptation | What invariances exist? |

### Causal Discovery

Learn causal structure from data:

| Method | Assumption | Approach |
|--------|------------|----------|
| PC algorithm | Faithfulness | Conditional independence tests |
| GES | Faithfulness | Score-based search |
| LiNGAM | Non-Gaussian | Independent component analysis |
| NOTEARS | DAG constraint | Continuous optimization |

### Counterfactual Explanations

**Question:** "What would need to change for the prediction to be different?"

$$
x^{CF} = \arg\min_{x'} d(x, x') \text{ s.t. } f(x') \neq f(x)
$$

### Heterogeneous Treatment Effects

**CATE (Conditional Average Treatment Effect):**
$$
\tau(x) = E[Y(1) - Y(0) | X=x]
$$

**Meta-learners:**

| Learner | Approach |
|---------|----------|
| S-learner | Include T as feature |
| T-learner | Separate models for T=0, T=1 |
| X-learner | Enhanced two-stage |
| R-learner | Robinson (1988) decomposition |

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Conditioning on collider | Opens spurious paths | Do not condition on colliders |
| Bad controls | Conditioning on post-treatment | Only adjust for pre-treatment vars |
| Overadjustment | Blocking causal paths | Do not adjust for mediators |
| Selection bias | Conditioning on outcome | Model selection process |
| Measurement error | Attenuation bias | Use latent variable models |

## Reporting Standards

### Causal Analysis Checklist

- [ ] State causal question clearly
- [ ] Draw DAG with assumptions
- [ ] Identify adjustment set
- [ ] Discuss unmeasured confounders
- [ ] Report sensitivity analysis
- [ ] Discuss identification assumptions
- [ ] Compare methods if possible

### DAG Documentation

```markdown
## Causal Assumptions

### Variables
- X: Treatment (algorithm A vs B)
- Y: Outcome (model accuracy)
- C1: Dataset size (confounder)
- C2: Hyperparameters (confounder)
- M: Training time (mediator)

### Assumed Causal Structure
C1 → X (larger datasets → choice of algorithm)
C2 → X (hyperparameters → algorithm choice)
C1 → Y (dataset size → accuracy)
C2 → Y (hyperparameters → accuracy)
X → M → Y (algorithm → training time → accuracy)
X → Y (direct effect)

### Adjustment Set
{C1, C2} blocks all backdoor paths
```

## References

- Pearl, J. (2009). Causality: Models, Reasoning, and Inference
- Imbens, G. W., & Rubin, D. B. (2015). Causal Inference for Statistics
- Hernán, M. A., & Robins, J. M. (2020). Causal Inference: What If
- Peters, J., et al. (2017). Elements of Causal Inference