# Scientific Rigor

Experimental design, hypothesis testing, reproducibility, validity, logical fallacies, cognitive biases, argument analysis, and evidence evaluation for AI/ML research.

---

## Experimental Design

### Three Pillars

1. **Randomization**: Distributes confounds randomly across conditions
2. **Replication**: Reduces random error through multiple observations
3. **Control (Blocking)**: Isolates treatment effects from noise

### Design Types

| Design | When to Use in ML |
|--------|-------------------|
| Between-Subjects | Comparing fundamentally different architectures |
| Within-Subjects | Same data processed by different methods |
| Mixed | Model (between) x Dataset (within) |
| Factorial | Optimizer x Learning Rate x Batch Size |

### Baselines

**Required**: random baseline, majority class, previous SOTA (properly cited).

**Baseline Quality Checklist:**
- [ ] Official implementation used when available
- [ ] Same preprocessing applied to all methods
- [ ] Same hyperparameter search budget for all methods
- [ ] Same evaluation protocol for all methods
- [ ] Statistical tests applied to all comparisons

### Common ML Confounders

| Confounder | Control Strategy |
|------------|-----------------|
| Data leakage | Fit preprocessing on train only |
| Compute budget | Equal budget across methods |
| Hyperparameter tuning | Same number of trials |
| Implementation quality | Equal optimization effort |
| Dataset selection | Multiple diverse datasets |

---

## Hypothesis Testing

### Formulating Hypotheses

| Criterion | Example |
|-----------|---------|
| Testable | "Fine-tuning improves accuracy" |
| Specific | "Fine-tuning BERT improves F1 by 5-10%" |
| Falsifiable | NOT: "Model X is always better" |
| Grounded | Prior work suggests benefit |
| Predictive | "We predict improvement on task Y" |

### P-Values: Correct Interpretation

"If H0 were true, there's a p% chance of observing data this extreme or more."

**Common misinterpretations**: p = 0.04 does NOT mean 4% chance H0 is true. p > 0.05 does NOT mean H0 is true. p < 0.05 does NOT mean the effect is large.

### Effect Sizes

P-values tell if an effect exists, not how large. Always report effect sizes.

| Cohen's d | Interpretation |
|-----------|----------------|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |
| 1.2 | Very Large |

### Multiple Comparisons

With alpha = 0.05 and 20 tests: P(at least one false positive) = 64%.

- **Bonferroni**: alpha/m (conservative, controls family-wise error)
- **Benjamini-Hochberg**: Controls false discovery rate (more powerful)

Apply when: multiple primary outcomes, many exploratory tests, testing same data iteratively.

### Test Selection

```
Continuous: 1 sample -> t-test | 2 independent -> t-test (Mann-Whitney if non-normal)
            2 paired -> paired t-test (Wilcoxon) | 3+ -> ANOVA (Kruskal-Wallis)
Categorical: 2 variables -> Chi-square | Paired -> McNemar's
Correlation: Linear -> Pearson's r | Non-linear -> Spearman's rho
```

### Reporting Checklist

- [ ] Descriptive statistics (means, SDs, sample sizes)
- [ ] Test statistic with degrees of freedom
- [ ] Exact p-value (or range)
- [ ] Effect size with confidence interval
- [ ] Direction of effect
- [ ] Practical significance interpretation

---

## Reproducibility

### Reproducibility Hierarchy

| Level | Description |
|-------|-------------|
| 1: Results | Same data + same code = same results |
| 2: Empirical | Same methods + different data = same conclusions |
| 3: Statistical | Same methods + same distribution = same conclusions |
| 4: Conceptual | Different methods + same phenomenon = same conclusions |
| 5: Generalizability | Same phenomenon + different context = same conclusions |

### ML Reproducibility Checklist

**Model**: Architecture, parameter count, initialization, learning rate/schedule, optimizer, loss, regularization, framework version, hardware, random seeds.

**Data**: Dataset name/version/access, preprocessing, train/val/test splits, augmentation, exact metric definitions, number of runs, significance tests, confidence intervals.

**Protocol**: Hyperparameter search procedure, model selection criteria, early stopping, all conditions reported, failed experiments discussed, computational cost.

### Common Reproducibility Failures

| Failure | Solution |
|---------|----------|
| "Works on my machine" | Docker, environment files |
| Vanishing result | Git for code, DVC for data |
| Hyperparameter hunt | Preregistration, experiment logging |
| Dataset drift | Checksums, fixed versions |
| Non-determinism | Global seed setting, deterministic mode |

---

## Validity Types

| Type | Core Question | Key Threats |
|------|---------------|-------------|
| Internal | Is the causal relationship valid? | Confounds, bias, selection, data leakage |
| External | Can findings be generalized? | Distribution shift, benchmark overfitting |
| Construct | Are we measuring the right thing? | Proxy inadequacy, narrow metrics |
| Ecological | Do findings apply in real settings? | Simplified tasks, clean data |

### Key Checklists

**Internal**: Random seeds fixed, data splits stratified, no data leakage, multiple runs (n >= 3), confidence intervals.

**External**: Multiple benchmarks, out-of-distribution testing, hardware requirements specified, dataset demographics documented.

**Construct**: Measures cover all aspects, convergent and discriminant validity checked, proxy limitations documented.

---

## Logical Fallacies

### Causation Fallacies

| Fallacy | AI/ML Example |
|---------|---------------|
| Post Hoc | "Added dropout and accuracy improved, so dropout caused improvement" |
| Correlation=Causation | "More parameters correlate with higher accuracy, so more parameters cause better accuracy" |

**Detection**: Check for control conditions, alternative explanations, replication.

### Generalization Fallacies

| Fallacy | AI/ML Example |
|---------|---------------|
| Hasty Generalization | "Two studies found effect, therefore robust" |
| Sampling Bias | WEIRD datasets representing all domains |
| Ecological Fallacy | Aggregate benchmark results assumed per-instance |

### Statistical Fallacies

| Fallacy | Detection |
|---------|-----------|
| Base Rate Fallacy | Apply Bayes' theorem |
| Simpson's Paradox | Always analyze subgroups |
| Prosecutor's Fallacy | Distinguish P(E|H) from P(H|E) |

### AI/ML-Specific Fallacies

- **Overclaiming from Benchmarks**: "SOTA on benchmark X implies true intelligence"
- **Anthropomorphizing Models**: "The model understands language"
- **Dataset Bias Generalization**: "Works on ImageNet, therefore works on real-world images"

---

## Cognitive Biases in Research

### Phase Susceptibility

| Research Phase | Susceptible Biases |
|----------------|-------------------|
| Question Formulation | Confirmation Bias, Availability |
| Literature Review | Confirmation Bias, Selection Bias |
| Experimental Design | Bias Blind Spot, Optimism Bias |
| Analysis | P-hacking, HARKing, Publication Bias |
| Interpretation | Confirmation Bias, Sunk Cost Fallacy |

### Key Biases and Mitigations

| Bias | Mitigation |
|------|------------|
| Confirmation Bias | Adversarial testing, seek contradictory evidence, devil's advocate |
| Publication Bias | Preregister, publish null results, report all conditions |
| HARKing | Preregistration, distinguish exploratory from confirmatory |
| P-hacking | Pre-register analyses, correct for multiple comparisons, report all tests |
| Sunk Cost Fallacy | Fresh start test: "If starting today with no prior investment, would I choose this?" |
| Anchoring | Use multiple starting points |
| Optimism Bias | Pre-mortem analysis, reference class forecasting |

---

## Argument Analysis

### Argument Components

- **Premises**: Starting points, assumptions, evidence
- **Inference**: Logical movement (deductive, inductive, or abductive)
- **Conclusion**: The claim being supported

### Evaluation Criteria

1. **Truth of Premises**: Factually correct with adequate evidence?
2. **Relevance**: Do premises actually support the conclusion?
3. **Sufficiency**: Strong enough for the claimed conclusion?
4. **Counter-Arguments**: Are objections addressed?
5. **Clarity**: Is the argument clearly expressed?

---

## Evidence Evaluation

### Evidence Hierarchy (AI/ML)

| Level | Evidence Type |
|-------|--------------|
| 1 (Strongest) | Theoretical proofs with empirical validation, systematic reviews with meta-analyses |
| 2 (Strong) | Controlled experiments with proper baselines, multi-dataset studies, peer-reviewed with code |
| 3 (Moderate) | Single dataset experiments, observational studies, conference publications |
| 4 (Weak) | Case studies, expert opinion without data, preprints without review |
| 5 (Weakest) | Anecdotal evidence, claims without data |

### Evidence Synthesis Patterns

| Pattern | Action |
|---------|--------|
| Convergent (multiple sources, same conclusion) | Strengthens confidence |
| Divergent (different conclusions) | Requires reconciliation |
| Conflicting (contradictory) | Examine quality, look for moderators, investigate methods |

### Common Evaluation Errors

| Error | Correction |
|-------|-----------|
| Cherry-Picking | Systematically search all relevant evidence |
| Equating All Evidence | Weight by quality and relevance |
| Single-Study Syndrome | Seek convergent evidence from multiple sources |
| Authority Bias | Evaluate on merits, not source prestige |
