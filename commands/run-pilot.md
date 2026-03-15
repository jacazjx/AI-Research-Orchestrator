---
name: autoresearch:run-pilot
description: "Run the Pilot phase with Code and Adviser agents. Use when user says 'run pilot', 'pilot experiment', 'Pilot验证', '小规模实验'."
triggers:
  - "run pilot"
  - "pilot experiment"
  - "Pilot验证"
  - "小规模实验"
  - "pilot analysis"
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