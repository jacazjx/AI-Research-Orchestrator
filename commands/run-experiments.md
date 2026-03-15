---
name: autoresearch:run-experiments
description: "Run the full Experiments phase with Code and Adviser agents. Use when user says 'run experiments', 'full experiments', '完整实验', '大规模实验'."
triggers:
  - "run experiments"
  - "full experiments"
  - "完整实验"
  - "大规模实验"
  - "experiment phase"
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