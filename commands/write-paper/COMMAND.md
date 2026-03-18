---
name: airesearchorchestrator:write-paper
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

## ⚠️ CRITICAL: Agent Invocation Required

**You MUST actively invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Step 1: Initialize Phase State

```bash
python3 scripts/run_stage_loop.py --project-root <PROJECT_ROOT> --phase paper
```

### Step 2: Invoke Writer Agent (Primary)

Use the Agent tool to spawn the Writer agent:

```
Agent(
  subagent_type="general-purpose",
  name="writer",
  prompt="""
You are the Writer agent for the research project at <PROJECT_ROOT>.

Your role: Write manuscript based ONLY on approved evidence.

Tasks:
1. Read docs/reports/experiments/evidence-package-index.md for approved claims
2. Create paper outline (paper/PAPER_PLAN.md)
3. Write each section following the outline
4. Generate figures from experiment data (paper/figures/)
5. Compile LaTeX manuscript (paper/main.tex)
6. Ensure all claims are grounded in approved evidence

Constraints:
- ONLY use evidence from the approved evidence package
- Do NOT invent or hallucinate experiments or results
- All citations must be verified (use academic APIs)
- Follow target venue formatting guidelines

Write your draft to agents/writer/ and final paper to paper/.
"""
)
```

### Step 3: Invoke Reviewer Agent (Reviewer)

After Writer completes, invoke the Reviewer agent:

```
Agent(
  subagent_type="general-purpose",
  name="reviewer",
  prompt="""
You are the Reviewer agent for the research project at <PROJECT_ROOT>.

Your role: Review manuscript against top-tier conference standards (NeurIPS/ICML/ICLR).

Tasks:
1. Read paper/main.tex
2. Check claim-evidence alignment (cross-reference with evidence package)
3. Audit citations (>=90% must be verified via DOI or trusted sources)
4. Assess writing quality and clarity
5. Identify missing sections or weak arguments
6. Produce paper/reviewer-report.md with detailed feedback

Review criteria:
- Novelty: Is the contribution clear and significant?
- Evidence: Are all claims supported by approved evidence?
- Citations: Are all references verifiable and relevant?
- Writing: Is the paper clear and well-organized?
- Reproducibility: Is the method described in sufficient detail?

Scoring:
- 4.5-5.0: Accept (submission ready)
- 3.5-4.4: Minor revision needed
- 2.5-3.4: Major revision needed
- <2.5: Reject (fundamental issues)

Write your review to agents/reviewer/ and the report to paper/.
"""
)
```

### Step 4: Loop if Needed

If Reviewer score < 3.5, iterate:
1. Send Reviewer feedback back to Writer agent
2. Writer revises the manuscript
3. Reviewer re-reviews
4. Repeat up to `max-loops` times

### Step 5: Present Gate 4 to Human

When the loop completes, summarize:
- Paper draft
- Reviewer assessment
- Citation audit results
- Gate score

**Wait for human approval before advancing to Reflection phase.**