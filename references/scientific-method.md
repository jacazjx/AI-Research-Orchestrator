# Scientific Method

A unified reference for experimental design, hypothesis testing, reproducibility standards, and validity types in AI/ML research.

---

## Experimental Design

### Three Pillars

1. **Randomization**: Distributes confounds randomly across conditions
2. **Replication**: Reduces random error through multiple observations
3. **Control (Blocking)**: Isolates treatment effects from noise

### Key Design Questions

| Question | Purpose |
|----------|---------|
| What is the independent variable? | Treatment/manipulation to define precisely |
| What is the dependent variable? | Outcome measure (reliable, valid, sensitive) |
| How will groups be formed? | Random vs. self-selected assignment |
| What are the controls? | Baselines, placebos, comparison standards |
| How many observations? | Power analysis for sample size |

### Design Types

| Design | Description | When to Use in ML |
|--------|-------------|-------------------|
| Between-Subjects | Each subject in one condition | Comparing fundamentally different architectures |
| Within-Subjects | Each subject experiences all conditions | Same data processed by different methods |
| Mixed | Combines between and within factors | Model (between) x Dataset (within) |
| Factorial | Multiple IVs simultaneously | Optimizer x Learning Rate x Batch Size |

### Baselines in ML Research

**Required baselines:**
- Random baseline (for classification)
- Majority class baseline
- Previous SOTA method (properly cited)

**Baseline Quality Checklist:**
- [ ] Official implementation used when available
- [ ] Same preprocessing applied to all methods
- [ ] Same hyperparameter search budget for all methods
- [ ] Same evaluation protocol for all methods
- [ ] Statistical tests applied to all comparisons

### Blinding in ML Experiments

While traditional blinding is often impossible in ML, implement procedural blinding:
- Replace model names with anonymous identifiers before evaluation
- Randomize test data order to prevent sequence effects
- Calculate metrics before unblinding
- Run analysis scripts treating all conditions identically

### Common ML Confounders

| Confounder | Example | Control Strategy |
|------------|---------|-----------------|
| Data leakage | Preprocessing on full dataset | Fit on train only |
| Compute budget | 10x GPU hours for proposed method | Equal budget |
| Hyperparameter tuning | 100 trials vs. 10 for baseline | Same number of trials |
| Implementation quality | Optimized vs. naive baseline | Equal optimization effort |
| Dataset selection | Only favorable datasets | Multiple diverse datasets |

---

## Hypothesis Testing

### Formulating Good Hypotheses

| Criterion | Description | Example |
|-----------|-------------|---------|
| Testable | Can be empirically verified | "Fine-tuning improves accuracy" |
| Specific | Defines variables and relationships | "Fine-tuning BERT improves F1 by 5-10%" |
| Falsifiable | Possible to prove wrong | NOT: "Model X is always better" |
| Grounded | Based on theory or prior evidence | Prior work suggests benefit |
| Predictive | Makes clear outcome predictions | "We predict improvement on task Y" |

### Null and Alternative Hypotheses

| Type | H0 | H1 | When to Use |
|------|----|----|-------------|
| Two-tailed | mu = mu0 | mu != mu0 | Exploratory research |
| One-tailed | mu <= mu0 | mu > mu0 | Strong prior for direction |

### Understanding P-Values

**Correct interpretation:** "If H0 were true, there's a p% chance of observing data this extreme or more."

**Common misinterpretations:**
- p = 0.04 does NOT mean 4% chance H0 is true
- p > 0.05 does NOT mean H0 is true (just insufficient evidence to reject)
- p < 0.05 does NOT mean the effect is large (statistical != practical significance)

### Type I and Type II Errors

| | H0 True | H0 False |
|---|---------|----------|
| **Reject H0** | Type I Error (alpha) - False Positive | Correct (Power = 1-beta) |
| **Fail to Reject** | Correct (1-alpha) | Type II Error (beta) - False Negative |

### Statistical Power

Power = 1 - beta = P(reject H0 | H0 is false)

**Four factors:** Effect size (larger = more power), Sample size (larger = more power), Significance level (stricter = less power), Variability (less = more power)

### Sample Size Guidelines for ML

| Effect Size | Cohen's d | Min n (per group) | Context |
|-------------|-----------|-------------------|---------|
| Small | 0.2 | ~394 | Subtle model improvements |
| Medium | 0.5 | ~64 | Moderate improvements |
| Large | 0.8 | ~26 | Major architecture changes |

### Effect Sizes

P-values only tell if an effect exists, not how large. Always report effect sizes.

**Cohen's d interpretation:**

| d | Interpretation | % Overlap |
|---|----------------|-----------|
| 0.2 | Small | 85% |
| 0.5 | Medium | 67% |
| 0.8 | Large | 53% |
| 1.2 | Very Large | 38% |

### Multiple Comparisons Problem

With alpha = 0.05 and m = 20 tests: P(at least one false positive) = 64%

**Correction Methods:**
- **Bonferroni**: alpha_adjusted = alpha / m (conservative, controls family-wise error)
- **Benjamini-Hochberg**: Controls false discovery rate (more powerful)

**When to apply:** Multiple primary outcomes, many exploratory tests, testing same data iteratively. NOT needed for: single pre-planned primary hypothesis, independent experiments.

### Test Selection Decision Tree

```
Continuous Data:
  One sample -> One-sample t-test
  Two samples:
    Independent -> Independent t-test (or Mann-Whitney U if non-normal)
    Paired -> Paired t-test (or Wilcoxon if non-normal)
  3+ groups:
    Independent -> One-way ANOVA (or Kruskal-Wallis)
    Repeated -> Repeated measures ANOVA

Categorical Data:
  Two variables -> Chi-square test
  Paired -> McNemar's test

Correlation:
  Linear -> Pearson's r
  Non-linear -> Spearman's rho
```

### Reporting Checklist

- [ ] Descriptive statistics (means, standard deviations, sample sizes)
- [ ] Test statistic with degrees of freedom
- [ ] Exact p-value (or range)
- [ ] Effect size with confidence interval
- [ ] Assumption checks
- [ ] Direction of effect
- [ ] Practical significance interpretation

### Avoiding Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| P-hacking | Pre-register analyses; correct for multiple comparisons |
| HARKing | Pre-register hypotheses; distinguish exploratory from confirmatory |
| Cherry-picking | Report all planned analyses |
| Small sample bias | Conduct power analysis; increase sample size |

---

## Reproducibility Standards

### Reproducibility Hierarchy

| Level | Description | Example |
|-------|-------------|---------|
| 1: Results | Same data + same code = same results | Re-running with same seeds |
| 2: Empirical | Same methods + different data = same conclusions | Testing on new datasets |
| 3: Statistical | Same methods + same distribution = same conclusions | Different random samples |
| 4: Conceptual | Different methods + same phenomenon = same conclusions | Independent validation |
| 5: Generalizability | Same phenomenon + different context = same conclusions | Cross-domain transfer |

### ML Reproducibility Checklist

**Model and Algorithm:**
- [ ] Exact architecture described or referenced
- [ ] Number of parameters specified
- [ ] Initialization method documented
- [ ] Exact learning rate(s) and schedule
- [ ] Optimizer type and hyperparameters
- [ ] Loss function defined
- [ ] Regularization documented
- [ ] Framework and version specified
- [ ] Hardware specification
- [ ] Random seeds specified

**Data and Evaluation:**
- [ ] Dataset name, version, and access instructions
- [ ] Preprocessing steps documented
- [ ] Train/val/test split sizes and method
- [ ] Data augmentation specified
- [ ] Exact metric definitions
- [ ] Number of evaluation runs
- [ ] Statistical significance tests
- [ ] Confidence intervals reported

**Experimental Protocol:**
- [ ] Hyperparameter search procedure documented
- [ ] Model selection criteria specified
- [ ] Early stopping criteria
- [ ] All experimental conditions reported
- [ ] Failed experiments discussed
- [ ] Computational cost reported

### Reproducibility Setup (PyTorch)

```python
import torch, numpy as np, random, os

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

### Common Reproducibility Failures

| Failure | Cause | Solution |
|---------|-------|----------|
| "Works on my machine" | Undocumented dependencies | Docker, environment files |
| Vanishing result | No version control | Git for code, DVC for data |
| Hyperparameter hunt | Selecting best without disclosure | Preregistration, experiment logging |
| Dataset drift | Dataset updated without versioning | Checksums, fixed versions |
| Non-determinism | Uncontrolled random seeds | Global seed setting, deterministic mode |

### Preregistration

Document hypotheses, methods, and analysis plans before conducting research.

**When to preregister:**
- Confirmatory research (testing specific hypotheses)
- Novel hypothesis (not derived from prior analysis)
- New experiments planned
- Willing to commit to reporting all results

**Key elements:**
1. Research question and hypotheses
2. Data description and splits
3. Model/algorithm details
4. Analysis plan with statistical tests
5. Success criteria and minimum effect size of interest
6. Exclusion criteria and outlier handling

---

## Validity Types

### Four Types at a Glance

| Type | Core Question | Key Threats | AI/ML Priority |
|------|---------------|-------------|----------------|
| Internal | Is the causal relationship valid? | Confounds, bias, selection | High |
| External | Can findings be generalized? | Distribution shift, domain gap | High |
| Construct | Are we measuring the right thing? | Proxy inadequacy, narrow metrics | Critical |
| Ecological | Do findings apply in real settings? | Simplified tasks, clean data | High |

### Internal Validity

**Threats:**

| Threat | AI/ML Example |
|--------|---------------|
| Selection Bias | Training on non-representative data splits |
| History Effects | Dataset drift during long training runs |
| Instrumentation | Different evaluation metrics across runs |
| Testing Effects | Overfitting to validation set |
| Confounding | Data preprocessing differences |
| Attrition | Selective removal of hard examples |

**Checklist:**
- [ ] Random seeds documented and fixed
- [ ] Data splits stratified and documented
- [ ] No data leakage between splits
- [ ] Hyperparameters fixed or systematically varied
- [ ] Same evaluation metrics across conditions
- [ ] Multiple runs conducted (n >= 3)
- [ ] Confidence intervals reported

### External Validity

**Threats:**

| Threat | Mitigation |
|--------|-----------|
| Benchmark Overfitting | Multiple diverse benchmarks |
| Distribution Shift | Domain adaptation, robustness testing |
| Dataset Selection Bias | Dataset analysis, bias documentation |
| Hardware Dependencies | Hardware-agnostic metrics |

**Checklist:**
- [ ] Multiple benchmarks used
- [ ] Out-of-distribution testing conducted
- [ ] Hardware requirements specified
- [ ] Cross-framework validation (if applicable)
- [ ] Dataset demographics documented
- [ ] Limitations of training population discussed

### Construct Validity

**Components:**
- **Convergent**: Measures that should be related ARE related
- **Discriminant**: Measures that should NOT be related are NOT
- **Content**: Measure covers all aspects of the construct

**AI/ML Concerns:**

| Construct | Common Proxy | Validity Concern |
|-----------|-------------|-----------------|
| Intelligence | Benchmark performance | Narrow task definition |
| Fairness | Demographic parity | Single metric insufficient |
| Robustness | Adversarial accuracy | May not capture real-world failures |
| Efficiency | FLOPs | Tradeoffs not captured |

### Ecological Validity

**Continuum:**
```
Controlled Lab <-----> Simulated <-----> Real-World Deployment
High Internal          Medium Both       High External Validity
```

**Assessment:**
- [ ] Task reflects real-world application
- [ ] Data source and preprocessing justified
- [ ] Metrics reflect real-world success
- [ ] Failure modes documented
- [ ] Deployment considerations addressed

### Validity Trade-offs

- **Internal vs. External**: Tight control limits generalization; high ecological validity may introduce confounds
- **Construct vs. Practical**: Perfect constructs may be impractical; practical measures may lack validity
- **Statistical vs. Practical Significance**: Large samples detect tiny effects; always report both

### Minimum Validity Standards

- [ ] Define constructs clearly
- [ ] Document operationalizations
- [ ] Control for major confounds
- [ ] Report statistical significance AND effect sizes
- [ ] Test on multiple datasets/domains
- [ ] Acknowledge validity limitations
- [ ] Discuss generalizability constraints
- [ ] Address real-world applicability
