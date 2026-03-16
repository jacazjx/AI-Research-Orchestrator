# Reproducibility Standards and Preregistration

A comprehensive guide to reproducibility in AI/ML research, covering standards, best practices, and preregistration protocols that ensure research integrity and enable scientific progress.

## Overview

Reproducibility is the cornerstone of scientific credibility. In AI/ML research, reproducibility faces unique challenges due to computational complexity, data dependencies, and the stochastic nature of training processes.

```
┌─────────────────────────────────────────────────────────────────┐
│              REPRODUCIBILITY HIERARCHY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   LEVEL 1: RESULTS REPRODUCIBILITY                              │
│   ├── Same data + Same code = Same results                      │
│   └── Minimum standard for publication                          │
│                                                                 │
│   LEVEL 2: EMPIRICAL REPRODUCIBILITY                            │
│   ├── Same methods + Different data = Same conclusions         │
│   └── Tests robustness and generalization                       │
│                                                                 │
│   LEVEL 3: STATISTICAL REPRODUCIBILITY                          │
│   ├── Same methods + Same data distribution = Same conclusions  │
│   └── Supports statistical inference                            │
│                                                                 │
│   LEVEL 4: CONCEPTUAL REPRODUCIBILITY                           │
│   ├── Different methods + Same phenomenon = Same conclusions    │
│   └── Tests theoretical validity                                │
│                                                                 │
│   LEVEL 5: GENERALIZABILITY                                     │
│   ├── Same phenomenon + Different context = Same conclusions    │
│   └── Maximum scientific value                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Understanding Reproducibility Terminology

### Key Definitions

| Term | Definition | AI/ML Context |
|------|------------|---------------|
| **Reproducibility** | Same data + same code = same results | Re-running code with same seeds |
| **Replicability** | Same methods + new data = same conclusions | Testing on new datasets |
| **Robustness** | Same methods + variations = same conclusions | Hyperparameter sensitivity |
| **Generalizability** | Same conclusions across different contexts | Cross-domain transfer |
| **Repeatability** | Same experimenter, same setup, same results | Same lab, same runs |

### The Reproducibility Crisis in AI/ML

```
┌─────────────────────────────────────────────────────────────────┐
│              REPRODUCIBILITY CHALLENGES IN AI/ML                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HARDWARE DEPENDENCIES                                          │
│  ├── GPU non-determinism                                        │
│  ├── Floating-point precision differences                       │
│  └── Parallel execution order randomness                        │
│                                                                 │
│  SOFTWARE DEPENDENCIES                                          │
│  ├── Framework version differences (PyTorch, TensorFlow)        │
│  ├── Library version conflicts                                  │
│  └── CUDA/cuDNN version sensitivity                             │
│                                                                 │
│  DATA ISSUES                                                    │
│  ├── Dataset versioning                                         │
│  ├── Data preprocessing variations                              │
│  ├── Train/val/test split differences                           │
│  └── Data availability restrictions                             │
│                                                                 │
│  HYPERPARAMETER SENSITIVITY                                     │
│  ├── Learning rate sensitivity                                  │
│  ├── Initialization randomness                                  │
│  ├── Batch ordering effects                                     │
│  └── Training duration dependence                               │
│                                                                 │
│  REPORTING INADEQUACY                                           │
│  ├── Missing hyperparameters                                    │
│  ├── Undocumented preprocessing                                 │
│  ├── Incomplete architectural details                           │
│  └── Selection of best run without disclosure                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Reproducibility Standards

### ML Reproducibility Checklist

Based on the reproducibility checklist from Pineau et al. and similar initiatives:

```markdown
## ML Reproducibility Checklist

### SECTION A: MODEL AND ALGORITHM DETAILS

#### A1. Model Architecture
- [ ] Exact model architecture described or referenced
- [ ] Number of parameters specified
- [ ] Layer-by-layer configuration documented
- [ ] Activation functions specified
- [ ] Initialization method documented

#### A2. Training Details
- [ ] Exact learning rate(s) specified
- [ ] Learning rate schedule documented
- [ ] Batch size specified
- [ ] Number of training epochs/iterations
- [ ] Optimizer type and hyperparameters
- [ ] Loss function precisely defined
- [ ] Regularization techniques and parameters

#### A3. Implementation Details
- [ ] Framework and version specified (PyTorch, TensorFlow, etc.)
- [ ] Hardware specification (GPU model, memory)
- [ ] Training time reported
- [ ] Random seeds specified
- [ ] Code availability statement

### SECTION B: DATA AND EVALUATION

#### B1. Data Details
- [ ] Dataset name and version
- [ ] Data preprocessing steps documented
- [ ] Train/validation/test split sizes
- [ ] Data augmentation techniques specified
- [ ] Data distribution characteristics
- [ ] Data availability/access instructions

#### B2. Evaluation Details
- [ ] Exact metric definitions
- [ ] Number of evaluation runs
- [ ] Statistical significance tests
- [ ] Confidence intervals reported
- [ ] Baseline comparison methodology

### SECTION C: EXPERIMENTAL PROTOCOL

#### C1. Experiment Setup
- [ ] Hyperparameter search procedure documented
- [ ] Model selection criteria specified
- [ ] Early stopping criteria (if used)
- [ ] Number of random seeds/runs
- [ ] Statistical analysis methodology

#### C2. Results Reporting
- [ ] Mean and standard deviation across runs
- [ ] All experimental conditions reported
- [ ] Failed experiments discussed
- [ ] Negative results reported
- [ ] Computational cost reported
```

### Hardware Reproducibility

```python
# reproducibility_setup.py
"""
Comprehensive reproducibility configuration for PyTorch
"""

import torch
import numpy as np
import random
import os
import json
from datetime import datetime

class ReproducibilityManager:
    """
    Manages all aspects of reproducibility in ML experiments
    """

    def __init__(self, seed=42, deterministic=True, benchmark_mode=False):
        self.seed = seed
        self.deterministic = deterministic
        self.benchmark_mode = benchmark_mode
        self.config = {}

    def set_seed(self):
        """Set all random seeds for reproducibility"""
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed(self.seed)
        torch.cuda.manual_seed_all(self.seed)
        np.random.seed(self.seed)
        random.seed(self.seed)
        os.environ['PYTHONHASHSEED'] = str(self.seed)

        if self.deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        else:
            torch.backends.cudnn.benchmark = self.benchmark_mode

    def get_system_info(self):
        """Collect system information for reproducibility"""
        info = {
            'timestamp': datetime.now().isoformat(),
            'seed': self.seed,
            'deterministic': self.deterministic,
            'python_version': platform.python_version(),
            'torch_version': torch.__version__,
            'cuda_version': torch.version.cuda,
            'cudnn_version': torch.backends.cudnn.version(),
            'gpu_available': torch.cuda.is_available(),
            'gpu_count': torch.cuda.device_count(),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            'gpu_memory': torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,
        }

        if torch.cuda.is_available():
            info['gpu_properties'] = {
                'name': torch.cuda.get_device_name(0),
                'capability': torch.cuda.get_device_capability(0),
                'memory_gb': torch.cuda.get_device_properties(0).total_memory / 1e9
            }

        self.config['system'] = info
        return info

    def save_config(self, filepath):
        """Save reproducibility configuration"""
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)

    def load_config(self, filepath):
        """Load reproducibility configuration"""
        with open(filepath, 'r') as f:
            self.config = json.load(f)
        return self.config

    def verify_reproducibility(self, results1, results2, tolerance=1e-6):
        """Verify that two runs produce identical results"""
        for key in results1:
            if isinstance(results1[key], (int, float)):
                if abs(results1[key] - results2[key]) > tolerance:
                    return False, f"Discrepancy in {key}: {results1[key]} vs {results2[key]}"
            elif isinstance(results1[key], np.ndarray):
                if not np.allclose(results1[key], results2[key], atol=tolerance):
                    return False, f"Array discrepancy in {key}"
            elif results1[key] != results2[key]:
                return False, f"Discrepancy in {key}: {results1[key]} vs {results2[key]}"
        return True, "Results are reproducible"


# Example usage
if __name__ == "__main__":
    repro_manager = ReproducibilityManager(seed=42, deterministic=True)
    repro_manager.set_seed()
    system_info = repro_manager.get_system_info()
    repro_manager.save_config("reproducibility_config.json")
    print(json.dumps(system_info, indent=2))
```

### Software Environment Reproducibility

```yaml
# environment.yml - Conda environment specification
name: research_env
channels:
  - pytorch
  - conda-forge
  - defaults
dependencies:
  - python=3.10.12
  - pytorch=2.0.1
  - torchvision=0.15.2
  - torchaudio=2.0.2
  - pytorch-cuda=11.8
  - numpy=1.24.3
  - pandas=2.0.2
  - scikit-learn=1.2.2
  - matplotlib=3.7.1
  - seaborn=0.12.2
  - jupyter=1.0.0
  - pip:
    - wandb==0.15.4
    - tensorboard==2.13.0
    - huggingface-hub==0.15.1
    - transformers==4.30.2
    - datasets==2.13.0
```

```txt
# requirements.txt - Pip requirements with exact versions
torch==2.0.1+cu118
torchvision==0.15.2+cu118
torchaudio==2.0.2+cu118
numpy==1.24.3
pandas==2.0.2
scikit-learn==1.2.2
matplotlib==3.7.1
seaborn==0.12.2
wandb==0.15.4
tensorboard==2.13.0
transformers==4.30.2
datasets==2.13.0
```

```python
# requirements.py - Version checking utility
"""
Utility to verify and record exact package versions
"""

import pkg_resources
import json
from datetime import datetime

def get_exact_versions(packages=None):
    """Get exact versions of installed packages"""
    if packages is None:
        packages = [
            'torch', 'torchvision', 'torchaudio', 'numpy', 'pandas',
            'scikit-learn', 'matplotlib', 'seaborn', 'wandb',
            'tensorboard', 'transformers', 'datasets', 'huggingface-hub'
        ]

    versions = {}
    for package in packages:
        try:
            dist = pkg_resources.get_distribution(package)
            versions[package] = {
                'version': dist.version,
                'location': dist.location
            }
        except pkg_resources.DistributionNotFound:
            versions[package] = 'NOT INSTALLED'

    versions['_timestamp'] = datetime.now().isoformat()
    return versions

def save_versions(filepath='exact_versions.json'):
    """Save exact versions to file"""
    versions = get_exact_versions()
    with open(filepath, 'w') as f:
        json.dump(versions, f, indent=2)
    return versions

def compare_versions(filepath1, filepath2):
    """Compare two version files"""
    with open(filepath1) as f:
        v1 = json.load(f)
    with open(filepath2) as f:
        v2 = json.load(f)

    differences = {}
    for pkg in v1:
        if pkg.startswith('_'):
            continue
        if pkg in v2:
            if v1[pkg]['version'] != v2[pkg]['version']:
                differences[pkg] = {
                    'v1': v1[pkg]['version'],
                    'v2': v2[pkg]['version']
                }
    return differences
```

---

## 3. Data Reproducibility

### Data Versioning

```python
# data_versioning.py
"""
Data versioning and integrity verification
"""

import hashlib
import json
import os
from pathlib import Path

class DataVersionManager:
    """
    Manages dataset versions and integrity
    """

    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.manifest_path = self.data_dir / 'manifest.json'

    def compute_hash(self, filepath, algorithm='sha256'):
        """Compute hash of a file"""
        h = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                h.update(chunk)
        return h.hexdigest()

    def create_manifest(self, data_files=None):
        """Create manifest of data files"""
        if data_files is None:
            data_files = list(self.data_dir.glob('**/*'))
            data_files = [f for f in data_files if f.is_file() and f.name != 'manifest.json']

        manifest = {
            'version': datetime.now().isoformat(),
            'files': {}
        }

        for filepath in data_files:
            rel_path = filepath.relative_to(self.data_dir)
            manifest['files'][str(rel_path)] = {
                'sha256': self.compute_hash(filepath),
                'size': filepath.stat().st_size,
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            }

        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def verify_integrity(self):
        """Verify data integrity against manifest"""
        with open(self.manifest_path) as f:
            manifest = json.load(f)

        issues = []
        for rel_path, info in manifest['files'].items():
            filepath = self.data_dir / rel_path
            if not filepath.exists():
                issues.append(f"Missing file: {rel_path}")
                continue

            current_hash = self.compute_hash(filepath)
            if current_hash != info['sha256']:
                issues.append(f"Hash mismatch for {rel_path}")

        return len(issues) == 0, issues

    def get_split_info(self, train_file, val_file, test_file):
        """Document data splits"""
        split_info = {
            'train': {
                'file': str(train_file),
                'hash': self.compute_hash(train_file),
                'samples': self._count_samples(train_file)
            },
            'validation': {
                'file': str(val_file),
                'hash': self.compute_hash(val_file),
                'samples': self._count_samples(val_file)
            },
            'test': {
                'file': str(test_file),
                'hash': self.compute_hash(test_file),
                'samples': self._count_samples(test_file)
            }
        }
        return split_info
```

### Data Split Reproducibility

```python
# data_splits.py
"""
Reproducible data splitting utilities
"""

import numpy as np
from sklearn.model_selection import train_test_split
import json

class ReproducibleDataSplitter:
    """
    Ensures reproducible data splits
    """

    def __init__(self, seed=42):
        self.seed = seed
        self.split_info = {}

    def stratified_split(self, X, y, test_size=0.2, val_size=0.1):
        """
        Create reproducible stratified splits
        """
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=test_size,
            stratify=y,
            random_state=self.seed
        )

        # Second split: train vs val
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=val_ratio,
            stratify=y_temp,
            random_state=self.seed
        )

        # Document splits
        self.split_info = {
            'seed': self.seed,
            'test_size': test_size,
            'val_size': val_size,
            'n_train': len(X_train),
            'n_val': len(X_val),
            'n_test': len(X_test),
            'train_class_dist': self._get_distribution(y_train),
            'val_class_dist': self._get_distribution(y_val),
            'test_class_dist': self._get_distribution(y_test),
            'indices': {
                'train': list(range(len(X_train))),
                'val': list(range(len(X_val))),
                'test': list(range(len(X_test)))
            }
        }

        return X_train, X_val, X_test, y_train, y_val, y_test

    def save_split_info(self, filepath):
        """Save split information"""
        with open(filepath, 'w') as f:
            json.dump(self.split_info, f, indent=2)

    def load_split_info(self, filepath):
        """Load split information"""
        with open(filepath) as f:
            self.split_info = json.load(f)
        return self.split_info

    def _get_distribution(self, y):
        """Get class distribution"""
        unique, counts = np.unique(y, return_counts=True)
        return dict(zip(unique.tolist(), counts.tolist()))
```

---

## 4. Experiment Tracking

### Comprehensive Experiment Logger

```python
# experiment_logger.py
"""
Comprehensive experiment logging for reproducibility
"""

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib

class ExperimentLogger:
    """
    Logs all aspects of an experiment for reproducibility
    """

    def __init__(self, experiment_name, log_dir='experiments'):
        self.experiment_name = experiment_name
        self.log_dir = Path(log_dir) / experiment_name
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.log = {
            'experiment_name': experiment_name,
            'start_time': datetime.now().isoformat(),
            'git_info': self._get_git_info(),
            'system_info': self._get_system_info(),
            'config': {},
            'hyperparameters': {},
            'data_info': {},
            'training_log': [],
            'results': {},
            'artifacts': []
        }

    def log_config(self, config):
        """Log experiment configuration"""
        self.log['config'] = config

    def log_hyperparameters(self, hparams):
        """Log hyperparameters"""
        self.log['hyperparameters'] = hparams

    def log_data_info(self, data_info):
        """Log data information"""
        self.log['data_info'] = data_info

    def log_training_step(self, step, metrics):
        """Log a training step"""
        entry = {
            'step': step,
            'timestamp': datetime.now().isoformat(),
            **metrics
        }
        self.log['training_log'].append(entry)

    def log_results(self, results):
        """Log final results"""
        self.log['results'] = results
        self.log['end_time'] = datetime.now().isoformat()

    def log_artifact(self, artifact_path, artifact_type):
        """Log an artifact (model, plot, etc.)"""
        artifact_info = {
            'path': str(artifact_path),
            'type': artifact_type,
            'hash': self._compute_hash(artifact_path),
            'timestamp': datetime.now().isoformat()
        }
        self.log['artifacts'].append(artifact_info)

    def save(self):
        """Save experiment log"""
        log_path = self.log_dir / 'experiment_log.json'
        with open(log_path, 'w') as f:
            json.dump(self.log, f, indent=2)
        return log_path

    def load(self, experiment_name):
        """Load an existing experiment log"""
        log_path = self.log_dir / 'experiment_log.json'
        with open(log_path) as f:
            self.log = json.load(f)
        return self.log

    def generate_report(self):
        """Generate a reproducibility report"""
        report = f"""
# Experiment Reproducibility Report

## Experiment: {self.log['experiment_name']}

### System Information
- Start Time: {self.log['start_time']}
- Python: {self.log['system_info']['python']}
- PyTorch: {self.log['system_info']['torch']}
- CUDA: {self.log['system_info']['cuda']}
- GPU: {self.log['system_info']['gpu']}

### Git Information
- Commit: {self.log['git_info']['commit']}
- Branch: {self.log['git_info']['branch']}
- Dirty: {self.log['git_info']['dirty']}

### Hyperparameters
```json
{json.dumps(self.log['hyperparameters'], indent=2)}
```

### Data Information
- Train samples: {self.log['data_info'].get('n_train', 'N/A')}
- Validation samples: {self.log['data_info'].get('n_val', 'N/A')}
- Test samples: {self.log['data_info'].get('n_test', 'N/A')}

### Results
```json
{json.dumps(self.log['results'], indent=2)}
```

### Artifacts
"""
        for artifact in self.log['artifacts']:
            report += f"- {artifact['type']}: {artifact['path']} (hash: {artifact['hash'][:8]}...)\n"

        return report
```

---

## 5. Preregistration

### What is Preregistration?

Preregistration is the practice of documenting research hypotheses, methods, and analysis plans before conducting research. This prevents hypothesizing after results are known (HARKing) and reduces publication bias.

```
┌─────────────────────────────────────────────────────────────────┐
│                PREREGISTRATION WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TRADITIONAL RESEARCH (NOT PREREGISTERED)                       │
│  ─────────────────────────────────────                          │
│  Data Collection → Analysis → Results → Hypothesis              │
│  (HARKing risk)                                                 │
│                                                                 │
│  PREREGISTERED RESEARCH                                         │
│  ────────────────────────                                       │
│  Hypothesis → Preregistration → Data Collection → Analysis      │
│  (Prevents HARKing)                                             │
│                                                                 │
│  AI/ML PREREGISTRATION TIMELINE                                 │
│  ─────────────────────────────                                  │
│  1. Define research question                                    │
│  2. Specify hypotheses (before any experiments)                │
│  3. Document experimental design                               │
│  4. Specify analysis plan                                       │
│  5. Define success criteria                                     │
│  6. Register protocol                                           │
│  7. Conduct experiments                                         │
│  8. Report all results (including null/negative)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### AI/ML Preregistration Template

```markdown
# AI/ML Research Preregistration Template

## 1. STUDY INFORMATION

### 1.1 Title
[Descriptive title of the research]

### 1.2 Authors
[List all authors and affiliations]

### 1.3 Registration Date
[Date of preregistration]

### 1.4 Version
[Version number if updating]

---

## 2. RESEARCH QUESTIONS AND HYPOTHESES

### 2.1 Primary Research Question
[State the main question this research addresses]

### 2.2 Primary Hypothesis
[State the specific hypothesis being tested]

**Directionality:**
- [ ] Directional (one-tailed): [specify direction]
- [ ] Non-directional (two-tailed)

**Example:**
"Hypothesis: Model X will achieve higher accuracy than Model Y on
dataset Z (one-tailed)."

### 2.3 Secondary Hypotheses
[List any secondary hypotheses, clearly labeled as exploratory if
applicable]

### 2.4 Exploratory Analyses
[Describe any planned exploratory analyses that are not hypothesis-driven]

---

## 3. METHODOLOGY

### 3.1 Data

#### 3.1.1 Dataset(s)
- Dataset name:
- Version:
- Source:
- License:
- Size (number of samples):
- Features/dimensions:
- Class distribution:

#### 3.1.2 Data Splits
- Training set size:
- Validation set size:
- Test set size:
- Split methodology:
- Random seed for splitting:

#### 3.1.3 Preprocessing
[Describe all preprocessing steps]

### 3.2 Models/Algorithms

#### 3.2.1 Primary Model(s)
- Model architecture:
- Number of parameters:
- Key hyperparameters:

#### 3.2.2 Baseline(s)
- Baseline model(s):
- Justification for baseline selection:

#### 3.2.3 Implementation Details
- Framework and version:
- Hardware specifications:
- Training duration:

### 3.3 Experimental Design

#### 3.3.1 Design Type
- [ ] Within-subjects (same data, different models)
- [ ] Between-subjects (different data splits)
- [ ] Factorial design: [describe]

#### 3.3.2 Randomization
[Describe randomization procedures]

#### 3.3.3 Blinding
[Describe any blinding procedures, e.g., anonymous evaluation]

---

## 4. ANALYSIS PLAN

### 4.1 Primary Outcome Measures

| Measure | Definition | Implementation |
|---------|------------|----------------|
| [Measure 1] | [Definition] | [How computed] |
| [Measure 2] | [Definition] | [How computed] |

### 4.2 Secondary Outcome Measures
[List secondary measures]

### 4.3 Statistical Analyses

#### 4.3.1 Primary Analysis
- Statistical test:
- Alpha level:
- Correction for multiple comparisons:

#### 4.3.2 Sample Size / Number of Runs
- Number of random seeds:
- Number of runs per seed:
- Justification:

#### 4.3.3 Power Analysis (if applicable)
[Describe power analysis or justification for sample size]

### 4.4 Exclusion Criteria
[Define criteria for excluding runs or data]

### 4.5 Outlier Handling
[Define how outliers will be identified and handled]

---

## 5. SUCCESS CRITERIA

### 5.1 Primary Success Criterion
[Define what constitutes a successful outcome]

### 5.2 Minimum Effect Size of Interest
[Define the smallest effect size considered meaningful]

### 5.3 Stopping Rules
[Define when to stop experiments, e.g., early stopping criteria]

---

## 6. DEVIATIONS

### 6.1 Planned Deviations
[None at registration - to be completed after data collection]

### 6.2 Justification for Deviations
[To be completed if deviations occur]

---

## 7. DATA AVAILABILITY

- [ ] Data will be made publicly available
- [ ] Data cannot be shared (explain why)
- [ ] Data available upon request

## 8. CODE AVAILABILITY

- [ ] Code will be made publicly available
- [ ] Repository URL: [if known]
- [ ] License:

## 9. CONFLICTS OF INTEREST

[Declare any conflicts of interest]

---

## 10. TIMELINE

| Phase | Estimated Start | Estimated End |
|-------|-----------------|---------------|
| Data preparation | | |
| Implementation | | |
| Experiments | | |
| Analysis | | |
| Writing | | |

---

Registration completed: [Date]
Registry: [e.g., OSF, AsPredicted, or institutional registry]
URL: [Registration URL]
```

### Preregistration Decision Tree

```
START: Should I Preregister?
│
├── Is this confirmatory research (testing specific hypotheses)?
│   ├── NO → Exploratory research
│   │   ├── Preregistration optional
│   │   └── Clearly label as exploratory
│   └── YES → Continue
│
├── Are you testing a novel hypothesis (not derived from prior analysis)?
│   ├── NO → Already have some results
│   │   ├── Cannot preregister (would be misleading)
│   │   └── Be transparent about exploratory nature
│   └── YES → Continue
│
├── Will you conduct new experiments?
│   ├── NO → Using existing data
│   │   ├── Can preregister analysis plan
│   │   └── Acknowledge data familiarity
│   └── YES → Continue
│
├── Can you commit to reporting all results?
│   ├── NO → Preregistration not appropriate
│   └── YES → PREREGISTER
│       ├── Document hypotheses
│       ├── Specify analysis plan
│       ├── Define success criteria
│       └── Commit to full reporting
```

---

## 6. Reproducibility Assessment Framework

### Reproducibility Scoring

```markdown
## Reproducibility Assessment Score (RAS)

### Instructions
Score each item from 0-2:
- 0 = Not addressed
- 1 = Partially addressed
- 2 = Fully addressed

### Categories

#### 1. Code Availability (0-10 points)
- [ ] Code publicly available in repository
- [ ] Clear documentation/README
- [ ] Installation instructions
- [ ] Usage examples
- [ ] All dependencies specified

#### 2. Data Availability (0-10 points)
- [ ] Dataset publicly available
- [ ] Data preprocessing code included
- [ ] Data splits documented
- [ ] Data versioning information
- [ ] Privacy/ethical considerations addressed

#### 3. Methodological Details (0-14 points)
- [ ] Model architecture fully specified
- [ ] All hyperparameters listed
- [ ] Training procedure documented
- [ ] Random seeds specified
- [ ] Hardware specifications
- [ ] Software versions documented
- [ ] Evaluation methodology clear

#### 4. Results Reporting (0-10 points)
- [ ] All experimental conditions reported
- [ ] Statistical significance tests
- [ ] Confidence intervals
- [ ] Multiple runs/seeds
- [ ] Negative/null results reported

#### 5. Reproducibility Artifacts (0-6 points)
- [ ] Docker/container available
- [ ] Environment specification file
- [ ] Reproducibility checklist completed
- [ ] Pretrained models available
- [ ] Experiment logs available
- [ ] Clear reproduction instructions

### Scoring Interpretation
- 45-50: Excellent reproducibility
- 35-44: Good reproducibility
- 25-34: Moderate reproducibility
- 15-24: Limited reproducibility
- 0-14: Poor reproducibility
```

### Self-Assessment Checklist

```markdown
## Pre-Publication Reproducibility Self-Assessment

### BEFORE SUBMISSION

#### Can Someone Reproduce Your Results?

□ Code Repository
  □ All code uploaded
  □ README with setup instructions
  □ Requirements.txt or environment.yml
  □ Sample data or data acquisition instructions
  □ Run scripts for all experiments

□ Hyperparameters
  □ All hyperparameters in config file or code
  □ Default values clearly marked
  □ Hyperparameter search procedure documented
  □ Final hyperparameters highlighted

□ Data
  □ Dataset download instructions
  □ Preprocessing code included
  □ Data splits provided or seed specified
  □ Data checksums provided

□ Computation
  □ Hardware requirements specified
  □ Estimated training time
  □ GPU memory requirements
  □ Random seeds specified

□ Results
  □ Raw results data provided
  □ Analysis scripts included
  □ Plot generation scripts included
  □ Tables can be regenerated

#### Internal Verification

□ Ran experiments multiple times
□ Verified with different random seeds
□ Tested on clean environment
□ Another team member reproduced
□ Docker/container tested (if provided)
```

---

## 7. Common Reproducibility Failures and Solutions

### Failure Modes

```
┌─────────────────────────────────────────────────────────────────┐
│              COMMON REPRODUCIBILITY FAILURES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FAILURE MODE 1: THE "WORKS ON MY MACHINE" PROBLEM              │
│  ├── Cause: Undocumented environment dependencies               │
│  ├── Solution: Docker containers, environment files             │
│  └── Prevention: Test on clean environment before submission    │
│                                                                 │
│  FAILURE MODE 2: THE VANISHING RESULT                           │
│  ├── Cause: No version control for code/data                   │
│  ├── Solution: Git for code, DVC for data                      │
│  └── Prevention: Commit before every experiment                │
│                                                                 │
│  FAILURE MODE 3: THE HYPERPARAMETER HUNT                        │
│  ├── Cause: Selecting best result without disclosure            │
│  ├── Solution: Report all experiments, use validation set      │
│  └── Prevention: Preregistration, experiment logging           │
│                                                                 │
│  FAILURE MODE 4: THE DATASET DRIFT                              │
│  ├── Cause: Dataset updated without versioning                  │
│  ├── Solution: Dataset versioning, checksums                    │
│  └── Prevention: Dataset manifest, fixed URLs                   │
│                                                                 │
│  FAILURE MODE 5: THE NON-DETERMINISTIC NIGHTMARE                │
│  ├── Cause: Not controlling random seeds                        │
│  ├── Solution: Global seed setting, deterministic mode          │
│  └── Prevention: Verify reproducibility before submitting       │
│                                                                 │
│  FAILURE MODE 6: THE INVISIBLE BASELINE                         │
│  ├── Cause: Baseline code/parameters not released               │
│  ├── Solution: Release all baseline code and configs            │
│  └── Prevention: Same standards for baselines as new methods    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Troubleshooting Guide

```markdown
## Reproducibility Troubleshooting Guide

### Problem: Results differ between runs

#### Diagnostic Steps
1. Check random seed setting
   ```python
   import torch
   print(torch.initial_seed())
   ```

2. Verify deterministic mode
   ```python
   print(torch.backends.cudnn.deterministic)
   print(torch.backends.cudnn.benchmark)
   ```

3. Check for non-deterministic operations
   - Some operations (e.g., atomicAdd) are non-deterministic
   - Set environment variable: CUBLAS_WORKSPACE_CONFIG=:16:8

4. Verify data loading
   - Check if data loader has shuffle enabled
   - Verify num_workers setting

#### Solutions
- Set all seeds before any imports
- Use deterministic algorithms where possible
- Reduce parallelism during debugging
- Check GPU vs CPU differences

### Problem: Cannot reproduce paper results

#### Diagnostic Steps
1. Check framework versions
   - Paper may use older version
   - Breaking changes between versions

2. Verify hyperparameters
   - Check supplementary materials
   - Check code repository
   - Contact authors

3. Check preprocessing
   - Different normalization
   - Different data augmentation

4. Hardware differences
   - Different GPU architectures
   - Different precision (fp32 vs fp16)

#### Solutions
- Use exact versions from paper
- Check for unofficial implementations
- Try reproducing baseline first
- File issue on paper repository

### Problem: Docker container fails to build

#### Diagnostic Steps
1. Check base image availability
2. Verify all dependencies are still available
3. Check for breaking changes in dependencies
4. Verify network access during build

#### Solutions
- Pin exact versions in Dockerfile
- Use multi-stage builds
- Cache dependencies
- Document build requirements
```

---

## Summary: Reproducibility Quick Reference

### Minimum Reproducibility Standards

```markdown
## Essential Reproducibility Checklist

### For Every Paper
□ Code publicly available
□ README with setup instructions
□ Requirements.txt with versions
□ Dataset access instructions
□ All hyperparameters specified
□ Random seeds provided
□ Hardware specified
□ Results with confidence intervals
□ Statistical tests reported

### For High-Impact Papers (Additional)
□ Docker container available
□ Preregistration (if applicable)
□ Multiple random seeds (n ≥ 3)
□ Ablation studies
□ Sensitivity analyses
□ Negative results reported
□ Experiment logs released
□ Video/walkthrough available
```

### Key Principles

1. **Document Everything**: Code, data, environment, hyperparameters
2. **Version Control**: Track all changes to code and data
3. **Be Deterministic**: Control randomness with seeds
4. **Report Fully**: Include null and negative results
5. **Test Reproducibility**: Have others reproduce before submission
6. **Preregister**: For confirmatory research, preregister hypotheses

---

## References and Resources

### Guidelines and Checklists
- Pineau, J., et al. (2020). Improving reproducibility in machine learning research. *JMLR*.
- Papers With Code reproducibility checklist
- NeurIPS reproducibility checklist

### Preregistration Platforms
- Open Science Framework (osf.io)
- AsPredicted (aspredicted.org)
- ML Preregistration templates

### Tools
- Git for version control
- DVC (Data Version Control)
- Weights & Biases, MLflow for experiment tracking
- Docker for environment reproducibility
- Conda for environment management

### Further Reading
- Gundersen & Kjensmo (2018). State of the art: Reproducibility in AI
- Hutson (2018). Artificial intelligence faces reproducibility crisis
- Drummond (2009). Replicability is not reproducibility