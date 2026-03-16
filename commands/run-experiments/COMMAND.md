---
name: run-experiments
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