# Evidence Standards

This document defines evidence handling rules, experiment integrity requirements, evidence hierarchy, and frameworks for evaluating evidence quality in AI/ML research.

---

## Evidence Rules

### Literature

- Prefer the last five years for the field snapshot.
- Add older work only when it is seminal or needed for fair comparison.
- Record retrieval dates and source links when available.
- Mark uncertainty when a source could not be verified.

### Code and Datasets

- Treat public repositories and datasets as evidence only after recording their exact URL, branch, commit, tag, or version when available.
- Do not claim compatibility until the implementation or data format has been inspected.
- Keep the user-supplied reference directory intact; add derived notes next to it instead of overwriting raw source files.

### Experimental Results

- Link every result table, figure, or claim to the run log or notebook that produced it.
- Keep failed runs and negative results visible unless the user explicitly archives them.
- Never promote pilot numbers into final evidence without labeling them clearly.

### Writing

- Separate evidence from interpretation.
- Do not cite unsupported claims in the manuscript just because they appear in brainstorm notes.
- Do not state that formal proofs are verified unless an external proof tool actually checked them.

---

## Experiment Integrity Protocol

### Core Principles

#### 1. Traceability

Every result must be traceable to:
- **Source code** (git commit hash)
- **Configuration** (complete parameter set)
- **Execution logs** (timestamped records)
- **Checkpoints** (model states)

#### 2. Reproducibility

All experiments must be reproducible:
- Same code + same config + same seed = same result
- Environment must be documented
- Dependencies must be specified

#### 3. Transparency

All outcomes must be reported:
- Failed runs are documented, not hidden
- Negative results are reported
- Anomalies are explained

### Directory Structure

```
code/experiments/
├── experiment-spec.md           # Experiment specification
├── run-registry.md              # Master run registry
├── results-summary.md           # Aggregated results
docs/experiments/
├── evidence-package-index.md    # Evidence links
code/experiments/
├── checkpoints/
│   └── checkpoint-index.md      # Checkpoint manifest
├── logs/
│   ├── run_001.log
│   └── ...
└── configs/
    ├── config_001.yaml
    └── ...
```

### Log File Format

Each log file must contain:

```
=== RUN METADATA ===
Run ID: [unique identifier]
Timestamp: [ISO 8601 datetime with timezone]
Git Commit: [full hash]
Config File: [relative path]
Random Seed: [integer]
GPU: [device ID and model]
Python Version: [version]
Framework Versions: [list]

=== CONFIGURATION ===
[Complete configuration as YAML or JSON]

=== EXECUTION LOG ===
[Chronological execution output]
[Include all training/validation metrics]
[Include any warnings or errors]

=== RESULTS ===
Start Time: [ISO datetime]
End Time: [ISO datetime]
Duration: [HH:MM:SS]
Status: [completed/failed/crashed]
Final Metrics: [key metrics]
Best Checkpoint: [path and epoch]

=== ARTIFACTS ===
Checkpoints: [list of paths]
Logs: [list of log files]
Visualizations: [list of plots/figures]
```

### Run Registry Format

The `run-registry.md` must contain:

```markdown
# Run Registry

## Summary
- Total runs planned: [N]
- Runs completed: [N]
- Runs failed: [N]
- Runs in progress: [N]

## Run Entries

### Run 001
- **Status**: completed
- **Timestamp**: 2026-03-13T10:30:00Z
- **Duration**: 04:32:15
- **Config**: `configs/config_001.yaml`
- **Seed**: 42
- **GPU**: cuda:0 (RTX 4090)
- **Primary Metric**: accuracy = 95.2% +/- 0.3%
- **Checkpoint**: `checkpoints/run_001_best.pt`
- **Log**: `logs/run_001.log`
- **Notes**: Standard training run
```

---

## Statistical Validity

### Required Statistics

For primary metrics, report:

1. **Central Tendency**: Mean (average across runs), Median (if outliers exist)
2. **Variability**: Standard deviation, Confidence interval (95%)
3. **Significance**: p-values for comparisons, Effect sizes

### Sample Size Guidelines

| Comparison Type | Minimum Runs |
|-----------------|--------------|
| Single method evaluation | 3 |
| Comparing two methods | 5 each |
| Ablation study | 3 per configuration |
| Hyperparameter sensitivity | 3 per setting |

### Reporting Template

```markdown
### Primary Results

| Method | Accuracy (%) | F1 Score |
|--------|--------------|----------|
| Ours | 95.2 +/- 0.3 | 0.943 +/- 0.005 |
| Baseline A | 91.5 +/- 0.4 | 0.901 +/- 0.008 |

**Statistical Significance:**
- Ours vs Baseline A: p < 0.001 (paired t-test)

**Confidence Intervals (95%):**
- Ours Accuracy: [94.8%, 95.6%]
```

---

## Baseline Fairness

### Fair Comparison Requirements

1. **Same Data**: All methods use identical train/val/test splits, same preprocessing
2. **Same Conditions**: Same compute budget, same number of parameters (or controlled), same training duration or convergence criteria
3. **Honest Reporting**: Report best baseline results (not worst), include baseline hyperparameter tuning effort, acknowledge any baseline advantages

### Baseline Implementation Checklist

- [ ] Official implementation used when available
- [ ] Hyperparameters from original paper
- [ ] Same evaluation protocol
- [ ] Multiple runs for variance
- [ ] Results match published baselines (within variance)

---

## Negative Result Handling

### Documentation Requirements

1. **Failed Runs**
   ```markdown
   ### Run 015 (Failed)
   - **Status**: failed
   - **Error**: CUDA out of memory
   - **Recovery**: Reduced batch size to 32
   - **Follow-up**: Run 016 with reduced batch size
   ```

2. **Null Results**
   ```markdown
   ### Ablation: Attention Mechanism
   - **Hypothesis**: Attention is critical for performance
   - **Result**: Removing attention reduced accuracy by only 0.5%
   - **Conclusion**: Attention provides minor improvement
   ```

3. **Anomalies**
   ```markdown
   ### Run 008 Anomaly
   - **Expected**: 93-95% accuracy
   - **Actual**: 78% accuracy
   - **Investigation**: Learning rate was 10x higher than intended
   - **Resolution**: Fixed config, re-ran as Run 009
   ```

---

## Result Verification

### Automatic Verification Checks

1. **Log Existence Check** - Verify log file exists for each run
2. **Checkpoint Integrity Check** - Verify checkpoint loads correctly
3. **Metric Extraction Check** - Extract final metrics from log

### Manual Verification Checklist

- [ ] Run IDs in registry match log file names
- [ ] Timestamps are reasonable (no time travel)
- [ ] Durations match experiment complexity
- [ ] Metrics match between logs and summary
- [ ] Seeds are documented for all runs

### Fabrication Detection Red Flags

| Red Flag | What to Check |
|----------|---------------|
| Perfect results | Unusually high/consistent scores |
| Round numbers | Metrics like exactly 95.0% or 99.0% |
| No failures | All runs completed successfully |
| Instant results | Training time too short for model size |
| Missing logs | Results claimed without logs |
| Inconsistent seeds | Same seed produces different results |

---

## Provenance Records

### Git Integration

```bash
git rev-parse HEAD > .git-commit
git diff > .git-diff
git status > .git-status
```

### Environment Recording

```bash
pip freeze > requirements.txt
nvidia-smi > gpu-info.txt
uname -a > system-info.txt
```

### Data Provenance

```yaml
dataset:
  name: ImageNet
  version: ILSVRC2012
  source: https://image-net.org/
  download_date: 2026-03-01
  hash: sha256:abc123...
  train_samples: 1281167
  val_samples: 50000
  test_samples: 100000
```

---

## Evidence Hierarchy for AI/ML Research

### ML-Specific Hierarchy

| Level | Evidence Type | Example |
|-------|---------------|---------|
| 1 | Reproducible benchmarks with code | Papers with code, multiple datasets |
| 2 | Ablation studies | Component contribution analysis |
| 3 | Cross-validation results | k-fold CV with proper splits |
| 4 | Single train/test split | Hold-out validation |
| 5 | Theoretical analysis | Complexity bounds, convergence proofs |
| 6 | Expert intuition | "We believe this should work" |

### Red Flags in ML Evidence

- [ ] No statistical significance testing
- [ ] Single random seed
- [ ] Cherry-picked examples
- [ ] Unfair comparison (different compute, data)
- [ ] No baselines or weak baselines
- [ ] Test data leaked into training
- [ ] Hyperparameter tuning on test set

### Best Practices for ML Evidence

1. Multiple random seeds (report mean +/- std)
2. Statistical significance testing
3. Proper train/validation/test splits
4. Ablation studies
5. Comparison to strong baselines
6. Released code and data
7. Compute budget reported
8. Hyperparameter search details

---

## Audit Protocol

### Self-Audit Checklist

Before submitting for Gate 3:

- [ ] All runs have corresponding log files
- [ ] All metrics in summary match log files
- [ ] All checkpoints are loadable
- [ ] All configurations are complete
- [ ] All random seeds are documented
- [ ] Failed runs are documented
- [ ] Negative results are reported
- [ ] Statistical tests are appropriate
- [ ] Baselines are fairly compared
- [ ] Environment is fully specified

### Adviser Audit Process

1. Spot-check 10-20% of runs
2. Verify metrics from logs
3. Load random checkpoints
4. Check statistical calculations
5. Review baseline implementations
6. Look for red flags

---

## Experiment Reproducibility Requirements

This section specifies concrete, actionable requirements that every experiment run MUST satisfy. These rules apply to all phases that produce experimental results (pilot and experiments).

### Random Seed Management

```python
# Mandatory seed setting for ML experiments
import random
import numpy as np
import torch

def set_global_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

- All experiments MUST set seeds at the start
- Seed value MUST be recorded in run metadata
- Multi-GPU: use `torch.cuda.manual_seed_all()`
- For JAX: `jax.random.PRNGKey(seed)`
- Document any operations that are inherently non-deterministic (e.g., atomicAdd in CUDA)

### Configuration Tracking

- Every experiment run MUST save its full configuration as YAML/JSON alongside results
- Use Hydra, OmegaConf, or equivalent for structured configs
- Config diffs between runs MUST be explicitly documented
- Command-line overrides MUST be logged
- Template:

```yaml
# run-config.yaml
experiment:
  name: "ablation-lr"
  seed: 42
  timestamp: "2026-03-22T10:00:00Z"
model:
  architecture: "transformer"
  hidden_size: 768
  num_layers: 12
training:
  learning_rate: 1e-4
  batch_size: 32
  epochs: 100
  optimizer: "adamw"
  weight_decay: 0.01
data:
  dataset: "dataset-v2"
  split_seed: 42
  train_ratio: 0.8
```

### Environment Documentation

- Every first run MUST capture:
  - `pip freeze > requirements-frozen.txt`
  - `python --version`
  - `nvidia-smi` output (GPU model, driver, CUDA version)
  - `uname -a` (OS info)
  - Git commit hash of code
- Store in `.autoresearch/runtime/environment-snapshot.txt`

### Checkpoint Preservation

- Checkpoints MUST include: model weights, optimizer state, scheduler state, epoch/step number, best metric, full config
- Naming: `checkpoint-{epoch:04d}-{metric:.4f}.pt`
- Keep at minimum: best checkpoint + last checkpoint
- Record checkpoint metadata in `code/checkpoints/checkpoint-index.md`

### Dataset Versioning

- Record SHA-256 hash of each data file used
- If using DVC: commit `.dvc` files alongside code
- If using HuggingFace datasets: pin exact revision/commit
- Document any preprocessing steps as executable scripts, not prose
- Template for `code/data/dataset-manifest.yaml`:

```yaml
datasets:
  - name: "training-data"
    source: "huggingface/dataset-name"
    revision: "abc123"
    sha256: "..."
    preprocessing: "scripts/preprocess.py"
  - name: "eval-data"
    source: "local"
    path: "data/eval.jsonl"
    sha256: "..."
    rows: 5000
```

### Run Registry Standards

Every experiment run in `docs/experiments/run-registry.md` MUST include:

- Run ID (auto-generated UUID or sequential)
- Timestamp (ISO 8601)
- Config file path
- Git commit hash
- Seed
- Key hyperparameters (inline)
- Result metrics
- Status (running/completed/failed/killed)
- GPU hours consumed
- Notes
