---
name: airesearchorchestrator:write-paper
description: "Run the Paper phase with Writer and Reviewer agents. Use when user says 'write paper', 'paper writing', '写论文', '论文写作'."
triggers:
  - "write paper"
  - "paper writing"
  - "写论文"
  - "论文写作"
  - "draft paper"
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