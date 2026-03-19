---
name: airesearchorchestrator:reflect
description: "Run the Reflection phase for lessons learned and system improvement"
argument-hint: "[--project-root <path>] [--max-loops <number>]"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent"
---

# Reflection Phase

Executes the Reflector <-> Curator loop for project closure:

- `docs/reflection/lessons-learned.md`
- `docs/reflection/overlay-draft.md`
- `docs/reflection/runtime-improvement-report.md`
- `docs/reflection/phase-scorecard.md`
- `.autoresearch/archive/archive-index.md`

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_stage_loop.py" --phase reflection $ARGUMENTS
```

## Process

1. Reflector extracts lessons and improvement suggestions
2. Curator judges which suggestions are reusable
3. User decides on overlay activation

## Gate 5 Requirements

- Lessons documented and transferable
- Overlay drafts marked as drafts
- All changes documented
- Opt-in list for changes requiring approval

## Agent Invocation

**You MUST invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Agent Pair

| Role | Agent |
|------|-------|
| Primary | `reflector` |
| Reviewer | `curator` |

### Workflow

1. Initialize phase state (script above)
2. Invoke Reflector agent with lesson extraction task
3. Invoke Curator agent to judge reusability
4. Present Gate 5 to human

### Final Decisions

- Approve final report?
- Activate any overlays? (requires explicit opt-in)

If approved:
```bash
# Archive the project
python3 scripts/archive_project.py --project-root <PROJECT_ROOT>

# Apply overlays if approved
python3 scripts/apply_overlay.py --project-root <PROJECT_ROOT> --overlay <OVERLAY_NAME>
```

**Update project status to `completed`.**