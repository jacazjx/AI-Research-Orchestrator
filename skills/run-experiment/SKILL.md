---
name: airesearchorchestrator:run-experiment
agent: coder
description: "Execute experiments at any scale -- pilot validation or full experiment matrix. Scope is determined by the current phase context: pilot phase runs a minimal validation experiment, experiments phase runs the full matrix. Handles local and remote GPU deployment. Use when user says \"run experiment\", \"run pilot\", \"deploy to server\", \"跑实验\", \"运行 Pilot\", or needs to launch training jobs."
user-invocable: false
argument-hint: [experiment-description]
allowed-tools: Bash(*), Read, Grep, Glob, Edit, Write, Agent
---
## Purpose

Execute experiments on local or remote GPU servers. This skill handles both pilot-scale and full-scale execution -- the scope is determined by the current phase context, not by which skill is invoked.

| Phase | Scope | Goal |
|-------|-------|------|
| Pilot | Minimal, < 24 hours | Validate core hypothesis with minimal resources |
| Experiments | Full matrix | Comprehensive evaluation with ablations, baselines, multiple seeds |

## Workflow

### Step 1: Detect Environment

Read project's CLAUDE.md to determine:
- Local GPU (CUDA/MPS) or Remote server (SSH alias)
- Conda environment
- Code directory

### Step 2: Pre-flight Check

Check GPU availability:
```bash
# Remote
ssh <server> nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader

# Local
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader
```

Free GPU = memory.used < 500 MiB.

### Step 3: Sync Code (Remote Only)

Only sync necessary files:
```bash
rsync -avz --include='*.py' --exclude='*' <local_src>/ <server>:<remote_dst>/
```

### Step 4: Deploy

**Remote (SSH + screen):**
```bash
ssh <server> "screen -dmS <exp_name> bash -c '\
  eval \"\$(<conda_path>/conda shell.bash hook)\" && \
  conda activate <env> && \
  CUDA_VISIBLE_DEVICES=<gpu_id> python <script> <args> 2>&1 | tee <log_file>'"
```

**Local:**
```bash
CUDA_VISIBLE_DEVICES=<gpu_id> python <script> <args> 2>&1 | tee <log_file>
```

### Step 5: Verify Launch

```bash
ssh <server> "screen -ls"  # Remote
ps aux | grep python       # Local
```

### Step 6: Collect Results and Report

Gather results:
- Training curves, final metrics, error cases, resource usage

For pilot phase, additionally:
- Compare results against Go/No-Go criteria from the pilot design
- Make a clear VALIDATED / PARTIALLY VALIDATED / NOT VALIDATED determination
- Include reproducibility information (code location, commands, random seeds)

## Key Rules

- ALWAYS check GPU availability first
- Each experiment gets own screen session + GPU
- Use tee to save logs
- Report: GPU, screen/process, command, estimated time
- Document ALL deviations from the experiment design
- Report negative results honestly