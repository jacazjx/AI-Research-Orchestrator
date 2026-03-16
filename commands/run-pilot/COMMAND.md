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