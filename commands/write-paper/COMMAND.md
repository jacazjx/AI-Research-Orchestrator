---
name: write-paper
description: "Run the Paper phase for manuscript writing and review"
script: scripts/run_stage_loop.py
triggers:
  - "write paper"
  - "draft paper"
  - "写论文"
  - "论文写作"
phase: paper
agents:
  - writer
  - reviewer
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

# Write Paper Phase

Executes the Writer <-> Reviewer loop for paper development:

- `paper/paper-draft.md`
- `paper/reviewer-report.md`
- `paper/rebuttal-log.md`
- `paper/citation-audit-report.md`
- `paper/final-acceptance-report.md`
- `paper/phase-scorecard.md`

## Process

1. Writer drafts based on approved evidence only
2. Reviewer gives structured review per top-tier standards
3. Loop until submission-ready

## Gate 4 Requirements

- Evidence-grounded draft
- Citation audit (>=90% verified)
- Reviewer report with scores
- Revision log
- Top-tier bar met