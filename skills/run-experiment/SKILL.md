---
name: run-experiment
description: Deploy and run ML experiments on local or remote GPU servers. Use when user says "run experiment", "deploy to server", "跑实验", or needs to launch training jobs.
argument-hint: [experiment-description]
allowed-tools: Bash(*), Read, Grep, Glob, Edit, Write, Agent
---

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

## Key Rules

- ALWAYS check GPU availability first
- Each experiment gets own screen session + GPU
- Use tee to save logs
- Report: GPU, screen/process, command, estimated time