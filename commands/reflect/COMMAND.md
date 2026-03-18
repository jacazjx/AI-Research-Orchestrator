---
name: airesearchorchestrator:reflect
description: "Run the Reflection phase for lessons learned and system improvement"
script: scripts/run_stage_loop.py
triggers:
  - "reflect"
  - "lessons learned"
  - "反思"
  - "总结"
phase: reflection
agents:
  - reflector
  - curator
arguments:
  required:
    - name: project-root
      description: Absolute path to the project directory
      type: path
  optional:
    - name: max-loops
      description: Maximum iteration loops between agents
      type: integer
      default: 2
---

# Reflection Phase

Executes the Reflector <-> Curator loop for project closure:

- `docs/reports/reflection/lessons-learned.md`
- `docs/reports/reflection/overlay-draft.md`
- `docs/reports/reflection/runtime-improvement-report.md`
- `docs/reports/reflection/phase-scorecard.md`
- `.autoresearch/archive/archive-index.md`

## Process

1. Reflector extracts lessons and improvement suggestions
2. Curator judges which suggestions are reusable
3. User decides on overlay activation

## Gate 5 Requirements

- Lessons documented and transferable
- Overlay drafts marked as drafts
- All changes documented
- Opt-in list for changes requiring approval

## Final Decisions

- Overlay activation (yes/no)
- If yes: `python3 scripts/apply_overlay.py --project-root <path>`
- Project status set to `completed`

## ⚠️ CRITICAL: Agent Invocation Required

**You MUST actively invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Step 1: Initialize Phase State

```bash
python3 scripts/run_stage_loop.py --project-root <PROJECT_ROOT> --phase reflection
```

### Step 2: Invoke Reflector Agent (Primary)

Use the Agent tool to spawn the Reflector agent:

```
Agent(
  subagent_type="general-purpose",
  name="reflector",
  prompt="""
You are the Reflector agent for the research project at <PROJECT_ROOT>.

Your role: Extract lessons learned and propose system improvements.

Tasks:
1. Review all phase reports (survey, pilot, experiments, paper)
2. Identify what worked well and what didn't
3. Extract transferable lessons for future projects
4. Propose system improvements (overlays) for the orchestrator
5. Document in docs/reports/reflection/lessons-learned.md
6. Create overlay drafts in docs/reports/reflection/overlay-draft.md

Categories for lessons:
- Methodology: What research approaches worked?
- Tools: What tools or techniques were effective?
- Process: What workflow improvements would help?
- Pitfalls: What mistakes should be avoided?

Overlay proposals:
- Must be opt-in (require explicit human approval)
- Must include safety rationale
- Must be backward compatible
- Must have rollback plan

Write your findings to agents/reflector/ and reports to docs/reports/reflection/.
"""
)
```

### Step 3: Invoke Curator Agent (Reviewer)

After Reflector completes, invoke the Curator agent:

```
Agent(
  subagent_type="general-purpose",
  name="curator",
  prompt="""
You are the Curator agent for the research project at <PROJECT_ROOT>.

Your role: Judge which lessons and overlays are reusable and safe.

Tasks:
1. Read docs/reports/reflection/lessons-learned.md
2. Assess transferability of each lesson
3. Read docs/reports/reflection/overlay-draft.md
4. Evaluate overlay safety and compatibility
5. Produce docs/reports/reflection/runtime-improvement-report.md
6. Create docs/reports/reflection/phase-scorecard.md

Evaluation criteria for overlays:
- Safety: Does it have a rollback plan?
- Compatibility: Is it backward compatible?
- Opt-in: Does it require explicit approval?
- Documentation: Is the change fully documented?

Scoring:
- 4.5-5.0: All lessons actionable, overlays ready for activation
- 3.5-4.4: Minor refinement needed
- 2.5-3.4: Some lessons not transferable, overlays need revision
- <2.5: Fundamental issues with lessons or unsafe overlays

Write your review to agents/curator/ and reports to docs/reports/reflection/.
"""
)
```

### Step 4: Present Gate 5 to Human

When the reflection is complete, summarize:
- Key lessons learned
- Proposed overlays
- Curator assessment
- Gate score

**Ask the human:**
1. Approve the final report?
2. Activate any overlays? (requires explicit opt-in)

### Step 5: Archive and Close

If approved:
```bash
# Archive the project
python3 scripts/archive_project.py --project-root <PROJECT_ROOT>

# Apply overlays if approved
python3 scripts/apply_overlay.py --project-root <PROJECT_ROOT> --overlay <OVERLAY_NAME>
```

**Update project status to `completed`.**