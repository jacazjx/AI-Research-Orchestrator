---
description: "Run the Paper phase for manuscript writing and review"
argument-hint: "[--project-root <path>] [--max-loops <number>]"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent"
---

# Write Paper Phase

Executes the Writer <-> Reviewer loop for paper development:

- `paper/paper-draft.md`
- `paper/reviewer-report.md`
- `paper/rebuttal-log.md`
- `paper/citation-audit-report.md`
- `paper/final-acceptance-report.md`
- `paper/phase-scorecard.md`

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_stage_loop.py" --phase paper $ARGUMENTS
```

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

## Agent Invocation

**You MUST invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Agent Pair

| Role | Agent |
|------|-------|
| Primary | `writer` |
| Reviewer | `reviewer` |

### Workflow

1. Initialize phase state (script above)
2. Invoke Writer agent with manuscript drafting task
3. Invoke Reviewer agent to review paper
4. Loop if score < 3.5
5. Present Gate 4 to human for approval

**Wait for human approval before advancing to Reflection phase.**