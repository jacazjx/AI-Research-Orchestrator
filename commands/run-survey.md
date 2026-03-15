---
name: autoresearch:run-survey
description: "Run the Survey phase with Survey and Critic agents. Use when user says 'run survey', 'start survey', '文献调研', '开始调研'."
triggers:
  - "run survey"
  - "start survey"
  - "文献调研"
  - "开始调研"
  - "literature review"
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