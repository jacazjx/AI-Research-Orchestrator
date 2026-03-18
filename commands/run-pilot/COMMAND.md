---
name: run-pilot
description: "Run the Pilot phase for preliminary experiment validation"
script: scripts/run_stage_loop.py
triggers:
  - "run pilot"
  - "pilot experiment"
  - "Pilot验证"
  - "小规模实验"
phase: pilot
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
      default: 3
---

# Run Pilot Phase

Executes the Code <-> Adviser loop for pilot analysis:

- `docs/reports/pilot/problem-analysis.md`
- `docs/reports/pilot/pilot-experiment-plan.md`
- `docs/reports/pilot/pilot-results.md`
- `docs/reports/pilot/pilot-validation-report.md`
- `docs/reports/pilot/phase-scorecard.md`

## Process

1. Code does problem analysis and low-cost validation design
2. Adviser judges if pilot supports continue/revise/pivot
3. Loop until ready for Gate 2

## Gate 2 Requirements

- Operational analysis
- Low-cost plan
- Pilot results tied to hypothesis
- Clear recommendation

## ⚠️ CRITICAL: Agent Invocation Required

**You MUST actively invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Step 1: Initialize Phase State

```bash
python3 scripts/run_stage_loop.py --project-root <PROJECT_ROOT> --phase pilot
```

### Step 2: Invoke Code Agent (Primary)

Use the Agent tool to spawn the Code agent:

```
Agent(
  subagent_type="general-purpose",
  name="code",
  prompt="""
You are the Code agent for the research project at <PROJECT_ROOT>.

Your role: Design and execute pilot experiments to validate the core hypothesis.

Tasks:
1. Read docs/reports/survey/research-readiness-report.md for context
2. Analyze the research problem (docs/reports/pilot/problem-analysis.md)
3. Design a minimal pilot experiment (< 24 hours, < 2 GPU hours)
4. Implement and run the pilot experiment
5. Document results in docs/reports/pilot/pilot-results.md
6. Produce pilot-validation-report.md with Go/No-Go recommendation

Constraints:
- Pilot must be low-cost and quick to validate/falsify hypothesis
- Document all code in code/src/
- Log all experiment runs in code/experiments/

Write your work to agents/coder/ and reports to docs/reports/pilot/.
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

Your role: Review pilot design and results, judge if hypothesis is validated.

Tasks:
1. Read docs/reports/pilot/pilot-validation-report.md
2. Assess pilot design validity (can it falsify the hypothesis?)
3. Evaluate results quality and statistical significance
4. Check for failure modes and negative results
5. Produce docs/reports/pilot/phase-scorecard.md with gate score

Decision criteria:
- Go: Pilot supports hypothesis, ready for full experiments
- Revise: Pilot inconclusive, need more work
- Pivot: Pilot falsifies hypothesis, consider alternative direction

Scoring:
- 4.5-5.0: Go (proceed to Experiments)
- 3.5-4.4: Advance with minor fixes
- 2.5-3.4: Revise (redesign pilot)
- <2.5: Pivot recommended

Write your review to agents/adviser/ and the scorecard to docs/reports/pilot/.
"""
)
```

### Step 4: Loop if Needed

If Adviser score < 3.5, iterate:
1. Send Adviser feedback back to Code agent
2. Code revises the pilot
3. Adviser re-reviews
4. Repeat up to `max-loops` times

### Step 5: Present Gate 2 to Human

When the loop completes, summarize:
- Pilot results
- Adviser assessment
- Go/No-Go recommendation
- Gate score

**Wait for human approval before advancing to Experiments phase.**