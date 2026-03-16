---
name: run-survey
description: "Run the Survey phase for literature review and research gap identification"
script: scripts/run_stage_loop.py
triggers:
  - "run survey"
  - "literature review"
  - "文献调研"
  - "开始调研"
phase: survey
agents:
  - survey
  - critic
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

# Run Survey Phase

Executes the Survey <-> Critic loop to produce:

- `docs/reports/survey/research-readiness-report.md`
- `docs/reports/survey/phase-scorecard.md`

## Process

1. Survey agent expands literature and defines atomic academic definitions
2. Critic reviews novelty, feasibility, theory risk
3. Loop until ready for Gate 1

## Gate 1 Requirements

- Bounded scope
- Atomic definitions
- Literature coverage (recent 5 years + seminal)
- Novelty argument
- Validation route