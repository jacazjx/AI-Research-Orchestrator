# Experimental Design for AI/ML Research

## Overview

Experimental design is the blueprint for scientific inquiry, determining the validity and reliability of research findings. In AI/ML research, proper experimental design distinguishes genuine discoveries from artifacts, confounds, and random noise.

## Table of Contents

1. [Fundamental Principles](#principles)
2. [Control Groups and Baselines](#control-groups)
3. [Randomization](#randomization)
4. [Blinding Procedures](#blinding)
5. [Confounding Variables](#confounders)
6. [Experimental Designs](#designs)
7. [Sample Size and Power](#sample-size)
8. [Validity in Experimental Design](#validity)
9. [AI/ML Specific Considerations](#ai-ml)
10. [Checklists and Templates](#checklists)

---

## 1. Fundamental Principles {#principles}

### The Three Pillars of Experimental Design

```
┌─────────────────────────────────────────────────────────────┐
│                   EXPERIMENTAL DESIGN                        │
├─────────────────┬─────────────────┬─────────────────────────┤
│   RANDOMIZATION  │    REPLICATION  │    CONTROL (BLOCKING)   │
│                 │                 │                         │
│ Distributes     │ Reduces         │ Isolates treatment      │
│ confounds       │ random error    │ effects from noise      │
│ randomly        │                 │                         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### Fisher's Principles

1. **Randomization:** Random assignment to conditions
2. **Replication:** Multiple observations per condition
3. **Blocking:** Group similar experimental units together

### The Scientific Method in Practice

```
1. OBSERVE     → Identify phenomenon or problem
2. HYPOTHESIZE → Formulate testable prediction
3. DESIGN      → Plan experiment with controls
4. PREDICT     → State expected outcomes
5. EXPERIMENT  → Collect data systematically
6. ANALYZE     → Apply statistical methods
7. CONCLUDE    → Draw inferences from data
8. ITERATE     → Refine and repeat
```

### Key Questions in Experimental Design

| Question | Purpose | Consideration |
|----------|---------|---------------|
| What is the independent variable? | Treatment/manipulation | Define precisely, control levels |
| What is the dependent variable? | Outcome measure | Reliable, valid, sensitive |
| Who/what are the subjects? | Experimental units | Representative, appropriate |
| How will groups be formed? | Assignment method | Random vs. self-selected |
| What are the controls? | Comparison standards | Baselines, placebos |
| How many observations? | Sample size | Power analysis |

---

## 2. Control Groups and Baselines {#control-groups}

### Types of Control Groups

| Control Type | Description | Use Case |
|--------------|-------------|----------|
| **Negative Control** | No treatment or placebo | Establish baseline performance |
| **Positive Control** | Known effective treatment | Validate experimental setup |
| **Sham Control** | Mimics procedure without active component | Control for procedure effects |
| **Waitlist Control** | Delayed treatment | Ethical alternative in intervention studies |
| **Historical Control** | Past data comparison | When randomization not possible |

### Baselines in AI/ML Research

```python
class BaselineComparison:
    """
    Framework for establishing baselines in ML experiments.
    """

    def __init__(self):
        self.baselines = {
            "random": self.random_baseline,
            "majority": self.majority_baseline,
            "heuristic": self.heuristic_baseline,
            "previous_sota": self.previous_sota,
            "ablated": self.ablated_baseline
        }

    def random_baseline(self, task_type, num_classes):
        """Random performance as absolute minimum."""
        if task_type == "classification":
            return 1.0 / num_classes  # Random accuracy
        elif task_type == "regression":
            return None  # Depends on metric

    def majority_baseline(self, labels):
        """Majority class performance."""
        from collections import Counter
        most_common = Counter(labels).most_common(1)[0][1]
        return most_common / len(labels)

    def heuristic_baseline(self, data, heuristic_fn):
        """Domain-specific rule-based baseline."""
        predictions = [heuristic_fn(x) for x in data]
        return predictions

    def previous_sota(self, task, dataset):
        """Best previously reported result."""
        # Look up from benchmark tables
        return self.lookup_sota(task, dataset)

    def ablated_baseline(self, model, component):
        """Model without specific component."""
        # Remove component and evaluate
        pass
```

### Baseline Selection Decision Tree

```
START: What are you comparing against?
|
|-- No existing methods? --> Random + Majority baselines (required)
|
|-- Existing methods exist?
|   |-- Direct competitors? --> Include as primary baselines
|   |-- Different paradigm? --> Include for comparison
|   |-- Older methods? --> Include for progress demonstration
|
|-- Claiming novelty?
|   |-- Architectural novelty? --> Ablate each component
|   |-- Training method? --> Compare to standard training
|   |-- Data efficiency? --> Learning curves comparison
|
|-- Multiple datasets?
|   |-- Use same baselines across all datasets for fair comparison
```

### Baseline Quality Checklist

- [ ] Random baseline included (for classification)
- [ ] Majority class baseline included
- [ ] Previous SOTA method included and properly cited
- [ ] Baseline implementations verified for correctness
- [ ] Same preprocessing applied to all methods
- [ ] Same hyperparameter search budget for all methods
- [ ] Same evaluation protocol for all methods
- [ ] Statistical tests applied to all comparisons

---

## 3. Randomization {#randomization}

### Purpose of Randomization

Randomization serves three critical functions:

1. **Eliminates systematic bias** in group assignment
2. **Balances known and unknown confounders** across groups
3. **Provides basis for statistical inference**

### Types of Randomization

#### Simple Randomization

```python
import numpy as np

def simple_randomization(n_subjects, n_groups=2, seed=None):
    """
    Simple random assignment to groups.

    Warning: May result in unbalanced groups, especially for small n.
    """
    if seed is not None:
        np.random.seed(seed)

    assignments = np.random.randint(0, n_groups, size=n_subjects)
    return assignments
```

#### Block Randomization

```python
def block_randomization(n_subjects, n_groups=2, block_size=None, seed=None):
    """
    Block randomization ensures balanced groups.

    Each block contains equal representation of all groups.
    """
    if seed is not None:
        np.random.seed(seed)

    if block_size is None:
        block_size = n_groups  # Minimum block size

    # Verify block_size is valid
    if block_size % n_groups != 0:
        raise ValueError("Block size must be divisible by number of groups")

    # Create blocks
    n_blocks = int(np.ceil(n_subjects / block_size))
    blocks = []

    for _ in range(n_blocks):
        block = []
        for group in range(n_groups):
            block.extend([group] * (block_size // n_groups))
        np.random.shuffle(block)
        blocks.extend(block)

    return np.array(blocks[:n_subjects])
```

#### Stratified Randomization

```python
def stratified_randomization(strata, n_groups=2, seed=None):
    """
    Stratified randomization balances groups within strata.

    Parameters:
    - strata: dict mapping stratum_name -> list of subject_ids
    - n_groups: number of treatment groups
    """
    if seed is not None:
        np.random.seed(seed)

    assignments = {}

    for stratum_name, subjects in strata.items():
        n_in_stratum = len(subjects)

        # Block randomization within each stratum
        stratum_assignments = block_randomization(
            n_in_stratum, n_groups, block_size=n_groups
        )

        for subject_id, group in zip(subjects, stratum_assignments):
            assignments[subject_id] = {
                "stratum": stratum_name,
                "group": group
            }

    return assignments
```

### Randomization in ML Experiments

```python
class MLExperimentRandomizer:
    """
    Proper randomization for ML experiments.
    """

    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed)

    def random_split(self, data, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """Random data split with stratification option."""
        indices = np.arange(len(data))
        np.random.shuffle(indices)

        n_train = int(len(indices) * train_ratio)
        n_val = int(len(indices) * val_ratio)

        train_idx = indices[:n_train]
        val_idx = indices[n_train:n_train + n_val]
        test_idx = indices[n_train + n_val:]

        return train_idx, val_idx, test_idx

    def stratified_split(self, labels, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """Stratified split maintaining class distribution."""
        from sklearn.model_selection import train_test_split

        # First split: train vs rest
        train_idx, rest_idx = train_test_split(
            np.arange(len(labels)),
            train_size=train_ratio,
            stratify=labels,
            random_state=self.seed
        )

        # Second split: val vs test
        val_ratio_adjusted = val_ratio / (val_ratio + test_ratio)
        val_idx, test_idx = train_test_split(
            rest_idx,
            train_size=val_ratio_adjusted,
            stratify=[labels[i] for i in rest_idx],
            random_state=self.seed + 1
        )

        return train_idx, val_idx, test_idx

    def random_hyperparameter_search(self, param_distributions, n_iter=50):
        """Random search for hyperparameters."""
        from sklearn.model_selection import ParameterSampler

        samples = list(ParameterSampler(
            param_distributions,
            n_iter=n_iter,
            random_state=self.seed
        ))
        return samples

    def cross_validation_folds(self, n_samples, n_folds=5):
        """Generate cross-validation fold assignments."""
        indices = np.arange(n_samples)
        np.random.shuffle(indices)

        fold_size = n_samples // n_folds
        folds = []

        for i in range(n_folds):
            start = i * fold_size
            if i == n_folds - 1:
                end = n_samples
            else:
                end = (i + 1) * fold_size

            test_idx = indices[start:end]
            train_idx = np.concatenate([indices[:start], indices[end:]])
            folds.append((train_idx, test_idx))

        return folds
```

### Randomization Verification

After randomization, verify balance:

```python
def verify_randomization_balance(assignments, covariates):
    """
    Check that randomization produced balanced groups.

    Parameters:
    - assignments: Group assignments (0 or 1)
    - covariates: DataFrame of covariates to check

    Returns dictionary of balance statistics.
    """
    from scipy import stats

    balance_report = {}
    group_0 = assignments == 0
    group_1 = assignments == 1

    for col in covariates.columns:
        if covariates[col].dtype in ['float64', 'int64']:
            # Continuous variable: t-test
            t_stat, p_value = stats.ttest_ind(
                covariates.loc[group_0, col],
                covariates.loc[group_1, col]
            )
            mean_diff = covariates.loc[group_1, col].mean() - covariates.loc[group_0, col].mean()
            std_pooled = np.sqrt(
                (covariates.loc[group_0, col].std()**2 +
                 covariates.loc[group_1, col].std()**2) / 2
            )
            standardized_diff = mean_diff / std_pooled

            balance_report[col] = {
                "type": "continuous",
                "mean_group_0": covariates.loc[group_0, col].mean(),
                "mean_group_1": covariates.loc[group_1, col].mean(),
                "std_diff": standardized_diff,
                "p_value": p_value,
                "balanced": abs(standardized_diff) < 0.1  # Common threshold
            }
        else:
            # Categorical variable: chi-square
            contingency = pd.crosstab(assignments, covariates[col])
            chi2, p_value, _, _ = stats.chi2_contingency(contingency)

            balance_report[col] = {
                "type": "categorical",
                "p_value": p_value,
                "balanced": p_value > 0.05
            }

    return balance_report
```

---

## 4. Blinding Procedures {#blinding}

### Types of Blinding

| Type | Who is Blinded | Prevents |
|------|----------------|----------|
| **Single-blind** | Participants | Placebo effects, demand characteristics |
| **Double-blind** | Participants + Experimenters | Experimenter bias, observer effects |
| **Triple-blind** | Participants + Experimenters + Analysts | Analysis bias |
| **Open-label** | No blinding | Used when blinding impossible |

### Blinding in AI/ML Research

While traditional blinding is often impossible in ML (you can see the model architecture), we can implement procedural blinding:

```python
class BlindEvaluation:
    """
    Procedures for blinded evaluation in ML experiments.
    """

    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed)

    def blind_model_names(self, results_dict):
        """
        Replace model names with anonymous identifiers.

        Use this before evaluation to prevent bias.
        """
        names = list(results_dict.keys())
        np.random.shuffle(names)

        blinded_results = {}
        name_mapping = {}

        for i, name in enumerate(names):
            blinded_name = f"Model_{chr(65 + i)}"  # Model_A, Model_B, etc.
            blinded_results[blinded_name] = results_dict[name]
            name_mapping[blinded_name] = name

        # Store mapping for later unblinding
        self.name_mapping = name_mapping
        return blinded_results

    def unblind_results(self, blinded_results):
        """Reveal true model names after evaluation."""
        unblinded = {}
        for blinded_name, results in blinded_results.items():
            true_name = self.name_mapping[blinded_name]
            unblinded[true_name] = results
        return unblinded

    def blind_data_order(self, data, labels):
        """Randomize data order to prevent sequence effects."""
        indices = np.arange(len(data))
        np.random.shuffle(indices)
        return data[indices], labels[indices], indices

    def create_evaluation_protocol(self, models, test_data):
        """
        Create blinded evaluation protocol.

        Steps:
        1. Shuffle test data order
        2. Blind model identities
        3. Run predictions
        4. Collect metrics
        5. Unblind for reporting
        """
        protocol = {
            "test_data_shuffled": True,
            "model_identities_blinded": True,
            "metric_calculation_blinded": True,
            "seed": self.seed
        }
        return protocol
```

### Human Evaluation Blinding

```python
def setup_blinded_human_evaluation(models, test_samples, annotators):
    """
    Setup for blinded human evaluation (e.g., model outputs, generations).

    Returns evaluation packets with no identifying information.
    """
    evaluation_packets = []

    for sample_idx, sample in enumerate(test_samples):
        for model_idx, model in enumerate(models):
            # Generate output (or use pre-generated)
            output = model.generate(sample)

            packet = {
                "packet_id": f"eval_{sample_idx}_{model_idx}",
                "input": sample,
                "output": output,
                # NO model name, NO identifying features
            }
            evaluation_packets.append(packet)

    # Shuffle packets
    np.random.shuffle(evaluation_packets)

    # Assign to annotators
    annotator_assignments = {}
    packets_per_annotator = len(evaluation_packets) // len(annotators)

    for i, annotator in enumerate(annotators):
        start = i * packets_per_annotator
        end = start + packets_per_annotator if i < len(annotators) - 1 else len(evaluation_packets)
        annotator_assignments[annotator] = evaluation_packets[start:end]

    return annotator_assignments
```

### Blinding Checklist

- [ ] Model identities hidden during evaluation
- [ ] Test data order randomized
- [ ] Predictions presented without identifying information
- [ ] Metrics calculated before unblinding
- [ ] Human annotators unaware of hypotheses
- [ ] Analysis scripts treat all conditions identically
- [ ] Results revealed only after all analysis complete

---

## 5. Confounding Variables {#confounders}

### What is a Confounder?

A **confounding variable** is a variable that:

1. Is associated with the independent variable
2. Is associated with the dependent variable
3. Is NOT on the causal pathway between them

```
Without Confounder:       With Confounder:

    IV ────→ DV               IV ←──→ Confounder ────→ DV
                                 ↓
                                 └───→ (spurious association)
```

### Common Confounders in ML Research

| Confounder | Description | Example |
|------------|-------------|---------|
| **Data leakage** | Test data information in training | Preprocessing on full dataset |
| **Compute budget** | More resources for proposed method | 10x GPU hours vs. baseline |
| **Hyperparameter tuning** | Unequal optimization effort | 100 trials vs. 10 trials |
| **Implementation quality** | Better code for proposed method | Optimized vs. naive baseline |
| **Dataset selection** | Cherry-picked datasets | Only datasets where method works |
| **Evaluation protocol** | Different evaluation settings | Different random seeds, folds |
| **Model scale** | Larger model for proposed method | 10x parameters |

### Confounder Control Strategies

```python
class ConfounderControl:
    """
    Strategies for controlling confounders in ML experiments.
    """

    @staticmethod
    def randomization():
        """
        Randomization distributes confounders randomly across conditions.
        """
        return "Use random assignment for all controllable factors"

    @staticmethod
    def matching(confounders, treatment_group):
        """
        Match control units to treatment units on confounders.
        """
        from sklearn.neighbors import NearestNeighbors

        # For each treatment unit, find control unit with similar confounders
        nn = NearestNeighbors(n_neighbors=1)
        nn.fit(confounders[~treatment_group])
        distances, indices = nn.kneighbors(confounders[treatment_group])

        return indices.flatten()

    @staticmethod
    def stratification(confounder, n_strata=5):
        """
        Stratify by confounder and analyze within strata.
        """
        import pandas as pd

        # Create strata based on confounder quantiles
        strata = pd.qcut(confounder, q=n_strata, labels=False)
        return strata

    @staticmethod
    def statistical_control(outcome, treatment, confounders):
        """
        Include confounders as covariates in regression.
        """
        import statsmodels.api as sm

        X = sm.add_constant(np.column_stack([treatment, confounders]))
        model = sm.OLS(outcome, X).fit()

        # Extract treatment effect controlling for confounders
        treatment_effect = model.params[1]
        treatment_se = model.bse[1]

        return treatment_effect, treatment_se

    @staticmethod
    def equalize_compute(models_config):
        """
        Ensure equal computational budget across methods.
        """
        equalized_config = {
            "max_training_time": models_config["max_time"],
            "max_gpu_hours": models_config["max_gpu_hours"],
            "hyperparameter_trials": models_config["n_trials"],  # Same for all
            "max_epochs": models_config["max_epochs"],
            "early_stopping_patience": models_config["patience"]
        }
        return equalized_config
```

### Detecting Confounders

```python
def detect_confounders(iv, dv, potential_confounders):
    """
    Detect if variables are confounders by checking associations.

    A confounder must be:
    1. Associated with IV (treatment)
    2. Associated with DV (outcome)
    3. Not caused by IV
    """
    from scipy import stats

    detected = []

    for name, confounder in potential_confounders.items():
        # Check association with IV
        if isinstance(confounder[0], (int, float)):
            # Continuous confounder
            if len(np.unique(iv)) == 2:
                # Binary IV: t-test
                t, p_iv = stats.ttest_ind(confounder[iv == 0], confounder[iv == 1])
            else:
                # Continuous IV: correlation
                r, p_iv = stats.pearsonr(iv, confounder)
        else:
            # Categorical confounder: chi-square
            contingency = pd.crosstab(iv, confounder)
            chi2, p_iv, _, _ = stats.chi2_contingency(contingency)

        # Check association with DV
        if isinstance(confounder[0], (int, float)):
            r, p_dv = stats.pearsonr(confounder, dv)
        else:
            # Categorical: ANOVA or chi-square
            groups = [dv[confounder == cat] for cat in np.unique(confounder)]
            f, p_dv = stats.f_oneway(*groups)

        # Confounder criteria
        is_confounder = (p_iv < 0.05) and (p_dv < 0.05)

        detected.append({
            "name": name,
            "associated_with_iv": p_iv < 0.05,
            "associated_with_dv": p_dv < 0.05,
            "potential_confounder": is_confounder,
            "p_iv": p_iv,
            "p_dv": p_dv
        })

    return detected
```

---

## 6. Experimental Designs {#designs}

### Between-Subjects Design

Each participant/subject is in only one condition.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Group A   │     │   Group B   │     │   Group C   │
│ Treatment 1 │     │ Treatment 2 │     │ Treatment 3 │
│  n = 30     │     │  n = 30     │     │  n = 30     │
└─────────────┘     └─────────────┘     └─────────────┘

Pros: No carryover effects, simpler analysis
Cons: Requires more subjects, individual differences
```

**When to use in ML:**
- Comparing fundamentally different architectures
- Irreversible training procedures
- One-time evaluations

### Within-Subjects Design

Each participant/subject experiences all conditions.

```
┌─────────────────────────────────────────────┐
│                  Subject 1                   │
│  ──→ Treatment A ──→ Treatment B ──→ ...   │
└─────────────────────────────────────────────┘

Pros: Fewer subjects needed, controls individual differences
Cons: Order effects, carryover effects, practice effects
```

**When to use in ML:**
- Same model evaluated on multiple datasets
- Same data processed by different methods
- Algorithm comparisons on fixed benchmark

### Mixed Design

Combines between-subjects and within-subjects factors.

```
                    Within-Subject Factor
                    (Dataset)
              ┌─────────┬─────────┬─────────┐
              │   A     │   B     │   C     │
    ┌─────────┼─────────┼─────────┼─────────┤
    │ Model 1 │   x     │   x     │   x     │
Between ──────┼─────────┼─────────┼─────────┤
Subject       │ Model 2 │   x     │   x     │   x     │
Factor        └─────────┴─────────┴─────────┴─────────┘
```

### Factorial Design

Multiple independent variables manipulated simultaneously.

```python
def factorial_design(factors):
    """
    Generate full factorial design.

    Parameters:
    - factors: dict of {factor_name: [levels]}

    Returns:
    - List of all condition combinations
    """
    import itertools

    factor_names = list(factors.keys())
    factor_levels = list(factors.values())

    conditions = []
    for combination in itertools.product(*factor_levels):
        condition = dict(zip(factor_names, combination))
        conditions.append(condition)

    return conditions

# Example: 2x3 factorial design
factors = {
    "optimizer": ["adam", "sgd"],
    "learning_rate": [0.001, 0.01, 0.1],
    "batch_size": [32, 64]
}

design = factorial_design(factors)
# Returns 12 conditions (2 x 3 x 2)
```

### Latin Square Design

Controls for order effects in within-subjects designs.

```python
def latin_square(n_conditions):
    """
    Generate balanced Latin square for order counterbalancing.

    Each condition appears once in each position.
    Each condition precedes each other condition equally often.
    """
    def balanced_latin_square(n):
        # For even n
        latin = []
        for i in range(n):
            row = []
            for j in range(n):
                if j % 2 == 0:
                    val = (i + j // 2) % n
                else:
                    val = (n - 1 - i + j // 2) % n
                row.append(val)
            latin.append(row)
        return latin

    # For odd n, need special handling
    if n_conditions % 2 == 1:
        raise NotImplementedError("Odd number of conditions requires doubled Latin square")

    return balanced_latin_square(n_conditions)

# Example: 4 conditions
conditions = ["A", "B", "C", "D"]
orders = latin_square(len(conditions))
# Each row is a presentation order for one subject/replication
```

---

## 7. Sample Size and Power {#sample-size}

### Power Analysis Framework

```python
def power_analysis_for_ml(effect_size, alpha=0.05, power=0.80, test_type="t-test"):
    """
    Calculate required sample size for ML experiments.

    Parameters:
    - effect_size: Expected effect (Cohen's d for t-test, f for ANOVA)
    - alpha: Significance level
    - power: Desired statistical power (1 - beta)
    - test_type: Type of statistical test

    Returns:
    - Required sample size
    """
    from scipy.stats import norm
    import numpy as np

    if test_type == "t-test":
        # Two-sample t-test
        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(power)

        n_per_group = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        return int(np.ceil(n_per_group))

    elif test_type == "paired-t":
        # Paired t-test
        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(power)

        n = ((z_alpha + z_beta) / effect_size) ** 2
        return int(np.ceil(n))

    elif test_type == "anova":
        # One-way ANOVA
        from scipy.stats import f
        # More complex calculation needed
        pass

    else:
        raise ValueError(f"Unknown test type: {test_type}")
```

### Sample Size for Common ML Scenarios

```python
class MLSampleSizeCalculator:
    """
    Sample size calculations for ML experiments.
    """

    def classification_sample_size(self, expected_accuracy, baseline_accuracy,
                                    n_classes, alpha=0.05, power=0.80):
        """
        Sample size for detecting accuracy improvement.
        """
        from scipy.stats import norm

        # Effect size for proportions
        p1, p2 = baseline_accuracy, expected_accuracy
        p_pooled = (p1 + p2) / 2

        effect_size = (p2 - p1) / np.sqrt(p_pooled * (1 - p_pooled))

        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(power)

        n = ((z_alpha + z_beta) / effect_size) ** 2

        return int(np.ceil(n))

    def cross_validation_runs(self, n_folds=10, confidence=0.95):
        """
        Number of cross-validation runs for stable estimates.
        """
        # More folds generally means more stable estimate
        # But also more computation
        return n_folds

    def ab_test_sample_size(self, baseline_rate, expected_lift,
                            alpha=0.05, power=0.80):
        """
        Sample size for A/B testing model improvements.
        """
        from scipy.stats import norm

        p1 = baseline_rate
        p2 = baseline_rate * (1 + expected_lift)

        # Standard error for proportions
        se1 = np.sqrt(p1 * (1 - p1))
        se2 = np.sqrt(p2 * (1 - p2))

        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(power)

        n = ((z_alpha * se1 + z_beta * se2) / (p2 - p1)) ** 2

        return int(np.ceil(n))
```

### Sample Size Guidelines for ML

| Scenario | Minimum Recommended | Preferred | Notes |
|----------|---------------------|-----------|-------|
| Single dataset comparison | 30 samples | 100+ | For stable estimates |
| Cross-validation | 5-fold | 10-fold | More folds = less bias |
| Hyperparameter search | 20 trials | 50+ trials | Depends on dimensionality |
| Ablation study | 5 runs/ablation | 10+ runs | For statistical testing |
| Model comparison | 10 seeds | 30+ seeds | Across random initializations |

---

## 8. Validity in Experimental Design {#validity}

### Types of Validity

```
┌─────────────────────────────────────────────────────────────────┐
│                        VALIDITY TYPES                           │
├───────────────────┬───────────────────┬────────────────────────┤
│ Internal          │ External           │ Construct              │
│                   │                    │                        │
│ "Is the effect    │ "Can results be    │ "Does the measure     │
│ real?"            │ generalized?"      │ capture the concept?" │
│                   │                    │                        │
│ Threats:          │ Threats:           │ Threats:               │
│ • Confounds       │ • Sample bias     │ • Poor operationalization │
│ • Selection bias  │ • Artificial       │ • Construct irrelevance │
│ • History         │   settings         │ • Mono-method bias    │
│ • Maturation      │ • Limited          │ • Method variance     │
│ • Testing effects │   conditions       │                        │
└───────────────────┴───────────────────┴────────────────────────┘
```

### Internal Validity Checklist

- [ ] Random assignment to conditions
- [ ] Equivalent groups at baseline
- [ ] No selection bias
- [ ] No attrition bias (differential dropout)
- [ ] No history effects (external events)
- [ ] No maturation effects (natural change)
- [ ] No testing effects (practice, fatigue)
- [ ] No instrumentation changes
- [ ] No experimenter bias (blinding used)
- [ ] No demand characteristics
- [ ] No placebo effects

### External Validity Checklist

- [ ] Representative sample
- [ ] Multiple datasets tested
- [ ] Realistic experimental conditions
- [ ] Multiple model scales tested
- [ ] Results replicate across seeds
- [ ] Results replicate across implementations
- [ ] Cross-domain generalization tested

### Construct Validity in ML

```python
class ConstructValidityML:
    """
    Assessing construct validity in ML evaluation.
    """

    def __init__(self):
        self.construct_measures = {}

    def evaluate_construct_validity(self, predictions, ground_truth, construct_name):
        """
        Evaluate whether metrics capture intended constructs.
        """
        metrics = {}

        # Accuracy-based constructs
        if construct_name == "overall_performance":
            metrics["accuracy"] = self._accuracy(predictions, ground_truth)
            metrics["balanced_accuracy"] = self._balanced_accuracy(predictions, ground_truth)

        # Fairness constructs
        elif construct_name == "fairness":
            metrics["demographic_parity"] = self._demographic_parity(predictions)
            metrics["equalized_odds"] = self._equalized_odds(predictions, ground_truth)

        # Robustness constructs
        elif construct_name == "robustness":
            metrics["adversarial_accuracy"] = self._adversarial_accuracy(predictions)
            metrics["distribution_shift_performance"] = self._shift_performance()

        return metrics

    def multi_method_validation(self, construct_name, methods):
        """
        Use multiple methods to measure same construct.
        Reduces mono-method bias.
        """
        results = {}
        for method_name, method_fn in methods.items():
            results[method_name] = method_fn()

        # Check convergence
        convergence = self._check_convergence(results)
        return {
            "methods": results,
            "convergence": convergence,
            "valid": convergence > 0.7  # Threshold for validity
        }
```

---

## 9. AI/ML Specific Considerations {#ai-ml}

### The Reproducibility Crisis in ML

```python
class ReproducibilityChecklist:
    """
    Checklist for reproducible ML experiments.
    """

    @staticmethod
    def get_checklist():
        return {
            "code": [
                "[ ] Code publicly available",
                "[ ] Dependencies specified (requirements.txt, environment.yml)",
                "[ ] Random seeds documented and set",
                "[ ] Version control with tagged releases",
                "[ ] README with setup instructions"
            ],
            "data": [
                "[ ] Dataset publicly available or accessible",
                "[ ] Preprocessing steps documented",
                "[ ] Train/val/test splits specified",
                "[ ] Data versioning (DVC, etc.)",
                "[ ] Data statistics reported"
            ],
            "model": [
                "[ ] Architecture specified (config file)",
                "[ ] Hyperparameters documented",
                "[ ] Training procedure described",
                "[ ] Model checkpoints available",
                "[ ] Training curves/logs available"
            ],
            "experiment": [
                "[ ] Compute resources specified",
                "[ ] Training time reported",
                "[ ] Number of runs reported",
                "[ ] Statistical tests applied",
                "[ ] Confidence intervals reported"
            ],
            "evaluation": [
                "[ ] Evaluation metrics defined",
                "[ ] Baselines compared",
                "[ ] Statistical significance tested",
                "[ ] Error analysis provided",
                "[ ] Ablation studies included"
            ]
        }
```

### Common ML Experimental Pitfalls

```python
class MLPitfalls:
    """
    Common pitfalls in ML experiments and how to avoid them.
    """

    @staticmethod
    def data_leakage():
        """Avoid data leakage between train and test."""
        return {
            "pitfall": "Information from test set leaks into training",
            "examples": [
                "Preprocessing on full dataset (normalization, feature selection)",
                "Using test data for early stopping",
                "Including test samples in hyperparameter tuning"
            ],
            "solutions": [
                "Fit preprocessing on train only, apply to test",
                "Use validation set for early stopping",
                "Nested cross-validation for hyperparameter tuning"
            ]
        }

    @staticmethod
    def selection_bias():
        """Avoid selection bias in dataset creation."""
        return {
            "pitfall": "Dataset doesn't represent target population",
            "examples": [
                "Cherry-picking easy examples",
                "Only evaluating on in-domain data",
                "Excluding failure cases from reporting"
            ],
            "solutions": [
                "Use established benchmarks",
                "Report performance across diverse datasets",
                "Include failure analysis"
            ]
        }

    @staticmethod
    def unfair_comparison():
        """Ensure fair comparison between methods."""
        return {
            "pitfall": "Baseline comparison is biased toward proposed method",
            "examples": [
                "Tuning proposed method more than baseline",
                "Using different data preprocessing",
                "Not reporting baseline results honestly",
                "Different model scales"
            ],
            "solutions": [
                "Equal hyperparameter search budget",
                "Same preprocessing pipeline",
                "Report all baseline results",
                "Use same architecture size"
            ]
        }
```

### Proper Comparison Protocol

```python
def fair_comparison_protocol(method_a, method_b, data, config):
    """
    Protocol for fair comparison between ML methods.
    """
    results = {
        "method_a": {},
        "method_b": {}
    }

    # 1. Same data splits
    train_idx, val_idx, test_idx = split_data(data, config["split_seed"])

    # 2. Same preprocessing
    preprocessor = fit_preprocessor(data[train_idx])
    train_data = preprocessor.transform(data[train_idx])
    val_data = preprocessor.transform(data[val_idx])
    test_data = preprocessor.transform(data[test_idx])

    # 3. Equal hyperparameter search budget
    for method, name in [(method_a, "method_a"), (method_b, "method_b")]:
        # Same number of trials
        best_params = hyperparameter_search(
            method, train_data, val_data,
            n_trials=config["n_trials"],
            seed=config["search_seed"]
        )

        # Train with best params
        model = train(method, train_data, val_data, best_params,
                      epochs=config["max_epochs"],
                      seed=config["train_seed"])

        # Evaluate
        results[name]["test_performance"] = evaluate(model, test_data)

    # 4. Multiple runs for statistical significance
    for seed in range(config["n_runs"]):
        # Repeat entire process
        pass

    # 5. Statistical test
    results["statistical_test"] = paired_statistical_test(
        results["method_a"]["runs"],
        results["method_b"]["runs"]
    )

    return results
```

---

## 10. Checklists and Templates {#checklists}

### Pre-Experiment Checklist

```markdown
## Pre-Experiment Checklist

### Research Question
- [ ] Clear, specific research question stated
- [ ] Hypothesis formulated and testable
- [ ] Independent variable(s) defined
- [ ] Dependent variable(s) defined
- [ ] Expected effect size estimated

### Design
- [ ] Experimental design selected (between/within/mixed)
- [ ] Control conditions determined
- [ ] Randomization procedure specified
- [ ] Blinding procedure specified
- [ ] Sample size justified by power analysis

### Data
- [ ] Data source identified
- [ ] Data split procedure determined
- [ ] Preprocessing pipeline defined
- [ ] Data leakage prevention measures in place

### Baselines
- [ ] Appropriate baselines selected
- [ ] Baseline implementations verified
- [ ] Equal comparison conditions ensured

### Analysis
- [ ] Statistical tests planned
- [ ] Multiple comparison correction planned (if needed)
- [ ] Effect size calculation planned
- [ ] Confidence interval calculation planned

### Reproducibility
- [ ] Random seed(s) documented
- [ ] Code version controlled
- [ ] Dependencies documented
- [ ] Compute resources documented
```

### During Experiment Checklist

```markdown
## During Experiment Checklist

### Data Handling
- [ ] Random seed set before any random operation
- [ ] Data splits created with fixed seed
- [ ] No information from test set used in training
- [ ] Preprocessing fit on train only

### Training
- [ ] Training procedure documented
- [ ] Hyperparameters logged
- [ ] Training curves saved
- [ ] Checkpoints saved

### Evaluation
- [ ] Evaluation on held-out test set only
- [ ] Same evaluation procedure for all methods
- [ ] Multiple runs with different seeds
- [ ] All results recorded (not just best)

### Quality Control
- [ ] Check for anomalies in training
- [ ] Verify no data leakage
- [ ] Confirm reproducibility (re-run with same seed)
```

### Post-Experiment Checklist

```markdown
## Post-Experiment Checklist

### Analysis
- [ ] All planned analyses completed
- [ ] Statistical tests applied
- [ ] Effect sizes calculated
- [ ] Confidence intervals reported
- [ ] Multiple comparison correction applied

### Reporting
- [ ] All conditions reported
- [ ] All runs reported (not just best)
- [ ] Failure cases discussed
- [ ] Limitations acknowledged

### Reproducibility
- [ ] Code released
- [ ] Models/checkpoints available
- [ ] Data accessible
- [ ] Results can be reproduced

### Ethics
- [ ] No data misuse
- [ ] No misrepresentation of results
- [ ] No cherry-picking
- [ ] Limitations clearly stated
```

### Experiment Documentation Template

```markdown
# Experiment: [Name]

## Metadata
- Date: [YYYY-MM-DD]
- Researcher: [Name]
- Project: [Project Name]
- Experiment ID: [ID]

## Research Question
[State the specific research question]

## Hypotheses
- H0: [Null hypothesis]
- H1: [Alternative hypothesis]

## Methods

### Design
- Type: [Between/Within/Mixed subjects]
- Variables:
  - IV: [Independent variable(s)]
  - DV: [Dependent variable(s)]
- Controls: [Control conditions]

### Participants/Data
- Sample size: [N]
- Source: [Data source]
- Split: [Train/Val/Test proportions]

### Procedure
1. [Step 1]
2. [Step 2]
...

### Analysis
- Statistical tests: [Tests used]
- Alpha level: [0.05]
- Power: [0.80]

## Results

### Descriptive Statistics
[Means, SDs, etc.]

### Inferential Statistics
[Test statistics, p-values, effect sizes]

## Conclusion
[Interpretation of results]

## Reproducibility
- Code: [URL]
- Data: [URL]
- Seed: [Random seed used]
- Environment: [Dependencies]
```

---

## Summary

Experimental design is the foundation of valid scientific inference. In AI/ML research, proper experimental design ensures that reported improvements are genuine rather than artifacts of poor methodology.

### Key Principles

1. **Control:** Use appropriate control groups and baselines
2. **Randomization:** Randomly assign to conditions to balance confounders
3. **Blinding:** Hide condition identities during evaluation
4. **Replication:** Repeat experiments to establish reliability
5. **Fairness:** Ensure equal treatment of all conditions

### Key Takeaways

- Design experiments BEFORE collecting data
- Report ALL conditions, not just favorable ones
- Use statistical tests appropriately
- Document everything for reproducibility
- Acknowledge limitations honestly

---

## References

1. Campbell, D. T., & Stanley, J. C. (1963). *Experimental and Quasi-Experimental Designs for Research*. Houghton Mifflin.
2. Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin.
3. Henderson, P., et al. (2018). Deep reinforcement learning that matters. *AAAI*.
4. Sculley, D., et al. (2018). The winner's curse? On competition and ML research. *NIPS Critiquing Workshop*.
5. Drummond, C. (2009). Replicability is not reproducibility: Nor is it good science. *Proceedings of the Evaluation Methods for Machine Learning Workshop at ICML*.