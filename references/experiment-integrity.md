# Experiment Integrity Protocol

This document defines the standards and procedures for ensuring experimental integrity, proper logging, and result authenticity.

## Core Principles

### 1. Traceability

Every result must be traceable to:
- **Source code** (git commit hash)
- **Configuration** (complete parameter set)
- **Execution logs** (timestamped records)
- **Checkpoints** (model states)

### 2. Reproducibility

All experiments must be reproducible:
- Same code + same config + same seed = same result
- Environment must be documented
- Dependencies must be specified

### 3. Transparency

All outcomes must be reported:
- Failed runs are documented, not hidden
- Negative results are reported
- Anomalies are explained

## Logging Standards

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
│   ├── run_002.log
│   └── ...
└── configs/
    ├── config_001.yaml
    ├── config_002.yaml
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
- **Primary Metric**: accuracy = 95.2% ± 0.3%
- **Checkpoint**: `checkpoints/run_001_best.pt`
- **Log**: `logs/run_001.log`
- **Notes**: Standard training run

### Run 002
...
```

## Result Verification

### Automatic Verification Checks

1. **Log Existence Check**
   ```bash
   # Verify log file exists for each run
   for run_id in $(grep -oP 'Run \K\d+' run-registry.md); do
     test -f logs/run_${run_id}.log || echo "Missing log: run_${run_id}"
   done
   ```

2. **Checkpoint Integrity Check**
   ```python
   # Verify checkpoint loads correctly
   import torch
   checkpoint = torch.load('checkpoints/run_001_best.pt')
   assert 'model_state_dict' in checkpoint
   assert 'optimizer_state_dict' in checkpoint
   ```

3. **Metric Extraction Check**
   ```bash
   # Extract final metrics from log
   grep "Final Metrics:" logs/run_001.log
   ```

### Manual Verification Checklist

- [ ] Run IDs in registry match log file names
- [ ] Timestamps are reasonable (no time travel)
- [ ] Durations match experiment complexity
- [ ] Metrics match between logs and summary
- [ ] Seeds are documented for all runs

## Fabrication Detection

### Red Flags

| Red Flag | What to Check |
|----------|---------------|
| Perfect results | Unusually high/consistent scores |
| Round numbers | Metrics like exactly 95.0% or 99.0% |
| No failures | All runs completed successfully |
| Instant results | Training time too short for model size |
| Missing logs | Results claimed without logs |
| Inconsistent seeds | Same seed produces different results |

### Verification Steps

1. **Cross-Check Metrics**
   ```
   Log file metric: 95.23%
   Summary metric: 95.2%
   Registry metric: 95.23%
   → Consistent ✓
   ```

2. **Verify Timing**
   ```
   Model parameters: 10M
   Dataset size: 100K samples
   Epochs: 100
   Expected time: ~4-8 hours on RTX 4090
   Claimed time: 4.5 hours
   → Plausible ✓
   ```

3. **Check Reproducibility**
   ```
   Run with same config and seed
   Compare results
   Variance within expected range
   → Reproducible ✓
   ```

## Statistical Validity

### Required Statistics

For primary metrics, report:

1. **Central Tendency**
   - Mean (average across runs)
   - Median (if outliers exist)

2. **Variability**
   - Standard deviation
   - Confidence interval (95%)

3. **Significance**
   - p-values for comparisons
   - Effect sizes

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
| Ours | 95.2 ± 0.3 | 0.943 ± 0.005 |
| Baseline A | 91.5 ± 0.4 | 0.901 ± 0.008 |
| Baseline B | 89.8 ± 0.5 | 0.885 ± 0.010 |

**Statistical Significance:**
- Ours vs Baseline A: p < 0.001 (paired t-test)
- Ours vs Baseline B: p < 0.001 (paired t-test)

**Confidence Intervals (95%):**
- Ours Accuracy: [94.8%, 95.6%]
```

## Baseline Fairness

### Fair Comparison Requirements

1. **Same Data**
   - All methods use identical train/val/test splits
   - Same preprocessing applied

2. **Same Conditions**
   - Same compute budget
   - Same number of parameters (or controlled)
   - Same training duration or convergence criteria

3. **Honest Reporting**
   - Report best baseline results (not worst)
   - Include baseline hyperparameter tuning effort
   - Acknowledge any baseline advantages

### Baseline Implementation Checklist

- [ ] Official implementation used when available
- [ ] Hyperparameters from original paper
- [ ] Same evaluation protocol
- [ ] Multiple runs for variance
- [ ] Results match published baselines (within variance)

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
   - **Impact**: May not be essential component
   ```

3. **Anomalies**
   ```markdown
   ### Run 008 Anomaly
   - **Expected**: 93-95% accuracy
   - **Actual**: 78% accuracy
   - **Investigation**: Learning rate was 10x higher than intended
   - **Resolution**: Fixed config, re-ran as Run 009
   ```

## Provenance Records

### Git Integration

```bash
# Record git state
git rev-parse HEAD > .git-commit
git diff > .git-diff
git status > .git-status
```

### Environment Recording

```bash
# Python environment
pip freeze > requirements.txt

# CUDA version
nvidia-smi > gpu-info.txt

# System info
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