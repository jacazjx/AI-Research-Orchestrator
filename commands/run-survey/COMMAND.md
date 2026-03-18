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

## ⚠️ CRITICAL: Agent Invocation Required

**You MUST actively invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Step 1: Initialize Phase State

```bash
python3 scripts/run_stage_loop.py --project-root <PROJECT_ROOT> --phase survey
```

### Step 2: Invoke Survey Agent (Primary)

Use the Agent tool to spawn the Survey agent:

```
Agent(
  subagent_type="general-purpose",
  name="survey",
  prompt="""
You are the Survey agent for the research project at <PROJECT_ROOT>.

Your role: Conduct literature review and define atomic academic definitions.

Tasks:
1. Read the idea brief at .autoresearch/idea-brief.md
2. Search academic APIs (Semantic Scholar, arXiv, DBLP, OpenAlex) for related work
3. Define atomic academic definitions for key concepts
4. Identify research gaps and novelty opportunities
5. Produce docs/reports/survey/research-readiness-report.md

Constraints:
- Use ONLY academic APIs for literature search (NO web search)
- Cite at least 10 recent papers (last 5 years)
- Ensure all citations are verifiable via DOI or trusted sources

Write your findings to agents/survey/ and the final report to docs/reports/survey/.
"""
)
```

### Step 3: Invoke Critic Agent (Reviewer)

After Survey completes, invoke the Critic agent:

```
Agent(
  subagent_type="general-purpose",
  name="critic",
  prompt="""
You are the Critic agent for the research project at <PROJECT_ROOT>.

Your role: Audit the Survey work for quality and novelty.

Tasks:
1. Read docs/reports/survey/research-readiness-report.md
2. Verify citation authenticity (check DOIs, Semantic Scholar)
3. Assess novelty argument strength
4. Identify theory risks and feasibility concerns
5. Produce docs/reports/survey/phase-scorecard.md with gate score

Scoring:
- 4.5-5.0: Approve (proceed to Gate 1)
- 3.5-4.4: Advance (minor fixes needed)
- 2.5-3.4: Revise (significant revision required)
- <2.5: Major issues (return to Survey)

Write your review to agents/critic/ and the scorecard to docs/reports/survey/.
"""
)
```

### Step 4: Loop if Needed

If Critic score < 3.5, iterate:
1. Send Critic feedback back to Survey agent
2. Survey revises the report
3. Critic re-reviews
4. Repeat up to `max-loops` times

### Step 5: Present Gate 1 to Human

When the loop completes, summarize:
- Survey findings
- Critic assessment
- Gate score
- Recommendation

**Wait for human approval before advancing to Pilot phase.**