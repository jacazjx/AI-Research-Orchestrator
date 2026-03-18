---
name: airesearchorchestrator:run-experiments
description: "Run the full Experiments phase for comprehensive evaluation"
script: scripts/run_stage_loop.py
triggers:
  - "run experiments"
  - "full experiments"
  - "完整实验"
  - "大规模实验"
phase: experiments
agents:
  - code
  - adviser
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 5
---

# Run Experiments Phase

Executes the Code <-> Adviser loop for full experiments:

- `docs/reports/experiments/experiment-spec.md`
- `docs/reports/experiments/run-registry.md`
- `docs/reports/experiments/results-summary.md`
- `code/checkpoints/checkpoint-index.md`
- `docs/reports/experiments/evidence-package-index.md`
- `docs/reports/experiments/phase-scorecard.md`

## Process

1. Code finalizes experiment matrix and runs experiments
2. Adviser reviews evidence strength
3. Loop until ready for Gate 3

## Gate 3 Requirements

- Frozen experiment spec
- All runs traceable
- Results match experiment plan
- Checkpoints documented
- Complete evidence package

## ⚠️ CRITICAL: Agent Invocation Required

**You MUST actively invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Step 1: Initialize Phase State

```bash
python3 scripts/run_stage_loop.py --project-root <PROJECT_ROOT> --phase experiments
```

### Step 2: Invoke Code Agent (Primary)

Use the Agent tool to spawn the Code agent:

```
Agent(
  subagent_type="general-purpose",
  name="code",
  prompt="""
You are the Code agent for the research project at <PROJECT_ROOT>.

Your role: Design and execute full experiment matrix to collect evidence.

Tasks:
1. Read docs/reports/pilot/pilot-validation-report.md for context
2. Design full experiment matrix (docs/reports/experiments/experiment-spec.md)
3. Implement experiment code in code/src/
4. Run experiments with proper logging (code/experiments/)
5. Document all checkpoints (code/checkpoints/checkpoint-index.md)
6. Analyze results (docs/reports/experiments/results-summary.md)
7. Build evidence package (docs/reports/experiments/evidence-package-index.md)

Constraints:
- All experiments must be traceable with run IDs
- Log all hyperparameters and random seeds
- Document negative results (do not hide them)
- Statistical analysis required for claims

Write your work to agents/coder/ and reports to docs/reports/experiments/.
"""
)
```

### Step 3: Invoke Adviser Agent (Reviewer)

After Code completes, invoke the Adviser agent:

```
Agent(
  subagent_type="general-purpose",
  name="adviser",
  prompt="""
You are the Adviser agent for the research project at <PROJECT_ROOT>.

Your role: Verify experiment integrity and evidence strength.

Tasks:
1. Read docs/reports/experiments/evidence-package-index.md
2. Verify all runs are traceable (check run IDs in run-registry.md)
3. Assess statistical validity of results
4. Check for hidden negative results
5. Evaluate baseline fairness and completeness
6. Produce docs/reports/experiments/phase-scorecard.md with gate score

Checklist:
- [ ] All experiments have run IDs
- [ ] Checkpoints are valid and accessible
- [ ] Statistical tests are appropriate
- [ ] Negative results are documented
- [ ] Baselines are fair and comprehensive

Scoring:
- 4.5-5.0: Approve (proceed to Paper)
- 3.5-4.4: Advance (minor analysis needed)
- 2.5-3.4: Revise (missing experiments or analysis)
- <2.5: Major issues (untraceable results, hidden negatives)

Write your review to agents/adviser/ and the scorecard to docs/reports/experiments/.
"""
)
```

### Step 4: Loop if Needed

If Adviser score < 3.5, iterate:
1. Send Adviser feedback back to Code agent
2. Code runs additional experiments or analysis
3. Adviser re-reviews
4. Repeat up to `max-loops` times

### Step 5: Present Gate 3 to Human

When the loop completes, summarize:
- Experiment results
- Evidence package
- Adviser assessment
- Gate score

**Wait for human approval before advancing to Paper phase.**