---
description: "Run the Survey phase for literature review and research gap identification"
argument-hint: "[--project-root <path>] [--max-loops <number>]"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent"
---

# Run Survey Phase

Executes the Survey <-> Critic loop to produce:

- `docs/reports/survey/research-readiness-report.md`
- `docs/reports/survey/phase-scorecard.md`

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_stage_loop.py" --phase survey $ARGUMENTS
```

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

## Agent Invocation

**You MUST invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Agent Pair

| Role | Agent |
|------|-------|
| Primary | `survey` |
| Reviewer | `critic` |

### Workflow

1. Initialize phase state (script above)
2. Invoke Survey agent with literature review task
3. Invoke Critic agent to audit work
4. Loop if score < 3.5
5. Present Gate 1 to human for approval

**Wait for human approval before advancing to Pilot phase.**