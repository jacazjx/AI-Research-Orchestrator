---
name: airesearchorchestrator:theoretical-derivation
description: Conduct theoretical derivation and formal analysis for research hypotheses. Includes mathematical formulation, proof sketches, complexity analysis, and theoretical guarantees. Use when user says "theoretical derivation", "理论推导", "formal analysis", "mathematical proof", or after idea formulation before literature survey.
user-invocable: false
argument-hint: [hypothesis-or-idea]
allowed-tools: Bash(python, sympy), Read, Write, Edit, Grep, Glob
---
# Theoretical Derivation

## Overview

Conduct rigorous theoretical derivation and formal analysis for research hypotheses. This skill bridges the gap between informal research ideas and mathematically grounded theories, providing the theoretical foundation needed for sound experimental design.

## Purpose

Transform informal research hypotheses into mathematically rigorous formulations with:
- Formal problem definitions
- Mathematical notation and symbols
- Theoretical analysis and proof sketches
- Complexity analysis where applicable
- Theoretical guarantees or bounds

## When to Use

**Trigger: After `define-idea` but before `research-lit`**

```
Research Idea → Idea Definition → Theoretical Derivation → Literature Survey
                                        ↑
                                   This skill
```

## Workflow

### Stage 1: Formalize the Problem

**Objective**: Transform informal problem statement into rigorous mathematical formulation.

#### Step 1.1: Define Mathematical Objects

For each key concept in the hypothesis:

```markdown
## Mathematical Object Definition

**Object**: [Name]
**Type**: Set / Function / Distribution / Algorithm / ...
**Notation**: [Symbol, e.g., X, f, P]

**Formal Definition**:
[LaTeX-formatted mathematical definition]

**Properties**:
- Property 1: [Statement]
- Property 2: [Statement]
```

#### Step 1.2: Specify Problem Domain

```markdown
## Problem Domain

**Input Space**: $\mathcal{X} = \{x \in \mathbb{R}^d : \text{constraints}\}$

**Output Space**: $\mathcal{Y} = \{y : \text{conditions}\}$

**Function Class**: $\mathcal{F} = \{f: \mathcal{X} \to \mathcal{Y} \mid \text{properties}\}$

**Assumptions**:
1. [Assumption 1 with justification]
2. [Assumption 2 with justification]
```

#### Step 1.3: Formalize Research Question

Transform the research question into mathematical terms:

| Original Question | Formal Formulation |
|-------------------|-------------------|
| "Does method A work better?" | $\exists f_A \in \mathcal{F}_A: \text{Performance}(f_A) > \text{Performance}(f_B)$ |
| "What is the relationship?" | $\forall x \in \mathcal{X}: f(x) = g(h(x))$ |
| "Can we bound the error?" | $\text{Error}(f) \leq O(g(n))$ under conditions C |

### Stage 2: Derive Core Theory

**Objective**: Develop the mathematical foundation of the proposed approach.

#### Step 2.1: Main Theorem Formulation

For each key claim, formulate as a theorem:

```markdown
## Theorem 1: [Name]

**Statement**:
Let $\mathcal{D}$ be a dataset drawn from distribution $P$ over $\mathcal{X} \times \mathcal{Y}$.
Under assumptions A1-Ak, for method M with parameters $\theta$:
$$
\text{[Main claim in formal notation]}
$$

**Significance**: [Why this theorem matters]

**Proof Sketch**:
1. [Key step 1]
2. [Key step 2]
3. [Key step 3]
...

**Full Proof**: [Optional, in appendix]

**Conditions**: [When does this apply?]

**Tightness**: [Is this bound tight? Can it be improved?]
```

#### Step 2.2: Lemma Development

Break down complex proofs into lemmas:

```markdown
## Lemma 1: [Name]

**Statement**: [Formal statement]

**Proof**:
[Proof steps]

**Used in**: Theorem 1, Step 2
```

#### Step 2.3: Corollaries and Extensions

```markdown
## Corollary 1: [Application/Extension]

**From**: Theorem 1

**Statement**: [Derived result]

**Implication**: [Practical significance]
```

### Stage 3: Complexity Analysis

**Objective**: Analyze computational and sample complexity.

#### Step 3.1: Time Complexity

```markdown
## Time Complexity Analysis

**Operation**: [Algorithm/Method name]

**Complexity**:
- Best case: $O(\cdot)$
- Average case: $O(\cdot)$
- Worst case: $O(\cdot)$

**Breakdown**:
| Step | Operation | Complexity |
|------|-----------|------------|
| 1 | [Step 1] | $O(n)$ |
| 2 | [Step 2] | $O(n \log n)$ |

**Comparison to Baselines**:
| Method | Time Complexity |
|--------|-----------------|
| Proposed | $O(\cdot)$ |
| Baseline A | $O(\cdot)$ |
| Baseline B | $O(\cdot)$ |
```

#### Step 3.2: Space Complexity

```markdown
## Space Complexity

**Memory Requirements**:
- Model parameters: $O(\cdot)$
- Intermediate storage: $O(\cdot)$
- Total: $O(\cdot)$

**Memory-Efficient Variants**:
[If applicable, describe trade-offs]
```

#### Step 3.3: Sample Complexity

```markdown
## Sample Complexity

**Setting**: [Supervised / Unsupervised / RL / ...]

**Bound Type**: PAC / Rademacher / VC-dimension / ...

**Result**:
With probability $1 - \delta$, to achieve error $\epsilon$:
$$
n \geq O\left(\frac{\text{complexity measure}}{\epsilon^2}\right)
$$

**Interpretation**: [Practical implications for data requirements]
```

### Stage 4: Theoretical Guarantees

**Objective**: Establish theoretical properties of the proposed approach.

#### Step 4.1: Convergence Analysis

```markdown
## Convergence Guarantees

**Setting**: [Optimization / Learning / ...]

**Assumptions**:
- A1: [Smoothness / Lipschitz]
- A2: [Convexity / Non-convexity]
- A3: [Stochasticity conditions]

**Main Result**:
$$
\mathbb{E}[f(x_T) - f(x^*)] \leq O\left(\frac{L}{T^\alpha}\right)
$$

**Rate**: Linear / Sublinear / ...

**Comparison**:
| Method | Rate | Assumptions |
|--------|------|-------------|
| Proposed | $O(1/T)$ | [List] |
| Baseline | $O(1/\sqrt{T})$ | [List] |
```

#### Step 4.2: Generalization Bounds

```markdown
## Generalization Bounds

**Framework**: [PAC-Bayes / Rademacher / Margin / ...]

**Bound**:
With probability $1 - \delta$:
$$
R(f) \leq \hat{R}(f) + O\left(\sqrt{\frac{\text{Complexity}}{n}}\right)
$$

**Interpretation**:
[What does this mean for practical deployment?]
```

#### Step 4.3: Robustness Analysis

```markdown
## Robustness Properties

**Type**: Adversarial / Distribution Shift / Noise

**Guarantee**:
For perturbation $\|\Delta\| \leq \epsilon$:
$$
\|f(x + \Delta) - f(x)\| \leq L \cdot \epsilon
$$

**Certification Method**: [If applicable]
```

### Stage 5: Identify Theoretical Gaps

**Objective**: Acknowledge limitations and areas needing further theoretical work.

```markdown
## Theoretical Gaps and Open Questions

### Proven Results
1. [Theorem 1]: [Summary]
2. [Theorem 2]: [Summary]

### Conjectures (Not Proven)
1. **Conjecture**: [Statement]
   - **Intuition**: [Why we believe it's true]
   - **Evidence**: [Empirical or partial theoretical support]
   - **Difficulty**: [Why hard to prove]

### Open Questions
1. [Question 1]
   - **Importance**: [Why this matters]
   - **Approaches Tried**: [What didn't work]

### Limitations
1. [Assumption that may not hold]
2. [Setting not covered by theory]
```

### Stage 6: Map to Experiments

**Objective**: Connect theoretical predictions to experimental validation.

```markdown
## Theory-Experiment Mapping

### Predictions to Validate

| Theoretical Claim | Experimental Test | Metric |
|-------------------|-------------------|--------|
| $O(1/T)$ convergence | Plot loss vs iterations | Loss curve slope |
| Sample complexity bound | Vary training set size | Performance vs n |
| Robustness guarantee | Adversarial attacks | Success rate |

### Critical Experiments

1. **Validation of Assumptions**
   - Assumption: [Statement]
   - Test: [How to verify experimentally]

2. **Boundary Conditions**
   - Theory predicts: [Behavior at boundaries]
   - Test: [Extreme case experiments]

3. **Comparative Predictions**
   - Theory predicts: [How method compares]
   - Test: [Baseline comparisons]
```

## Output

Save to `docs/survey/theoretical-derivation.md`:

```markdown
# Theoretical Derivation Report

## Executive Summary
- Core mathematical formulation
- Main theoretical results
- Key assumptions and limitations

## 1. Problem Formalization
[From Stage 1]

## 2. Core Theory
[From Stage 2]

## 3. Complexity Analysis
[From Stage 3]

## 4. Theoretical Guarantees
[From Stage 4]

## 5. Gaps and Open Questions
[From Stage 5]

## 6. Experiment Mapping
[From Stage 6]

## Appendix A: Full Proofs
[Detailed mathematical proofs]

## Appendix B: Notation Table
| Symbol | Meaning |
|--------|---------|
| $\mathcal{X}$ | Input space |
| $\mathcal{Y}$ | Output space |
| ... | ... |
```

## Quality Checklist

Before completion:

- [ ] All mathematical objects clearly defined
- [ ] Theorem statements are precise and unambiguous
- [ ] Proof sketches cover key steps
- [ ] Complexity analysis addresses all major operations
- [ ] Assumptions are explicit and justified
- [ ] Theoretical gaps are honestly acknowledged
- [ ] Predictions are mapped to experimental validation

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `define-idea` | Takes hypothesis as input |
| `research-lit` | Provides theoretical foundation for literature search |
| `audit-derivation` | Critic reviews the derivation |
| `design-exp` | Uses predictions for experiment design |

## Key Rules

1. **Rigor Over Generality**: Prefer precise results for specific cases over vague general claims
2. **Explicit Assumptions**: Every assumption must be stated and justified
3. **Honest Gaps**: Acknowledge what is not proven
4. **Experimental Connection**: Every theorem should have experimental implications
5. **Notation Consistency**: Define symbols once, use consistently

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Unstated assumptions | List all assumptions explicitly |
| Imprecise theorems | Quantify all terms precisely |
| Missing conditions | Specify when results hold |
| No proof sketch | At minimum, outline key steps |
| Disconnected from experiments | Map each theorem to testable predictions |