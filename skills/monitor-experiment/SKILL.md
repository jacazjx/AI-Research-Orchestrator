---
name: airesearchorchestrator:monitor-experiment
agent: code
description: Monitor running experiments, check progress, collect results. Use when user says "check results", "is it done", "monitor", or wants experiment output.
argument-hint: [server-alias or screen-name]
allowed-tools: Bash(ssh *), Bash(echo *), Read, Write, Edit
---

## Workflow

### Step 1: Check What's Running

```bash
ssh <server> "screen -ls"
```

### Step 2: Collect Output

```bash
ssh <server> "screen -S <name> -X hardcopy /tmp/screen_<name>.txt && tail -50 /tmp/screen_<name>.txt"
```

### Step 3: Check JSON Results

```bash
ssh <server> "ls -lt <results_dir>/*.json 2>/dev/null | head -20"
```

### Step 4: Summarize

Present results in comparison table:
| Experiment | Metric | Delta vs Baseline | Status |

### Step 5: Interpret

- Compare against known baselines
- Flag unexpected results
- Suggest next steps

## Key Rules

1. Check running status via SSH and screen
2. Report resource usage (GPU, memory, time)
3. Flag anomalies and unexpected results

## Output

- Console output with status table and resource metrics