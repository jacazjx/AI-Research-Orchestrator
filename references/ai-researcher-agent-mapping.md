# AI-Researcher Agent Mapping

This skill derives its role contracts from the source agents in HKUDS/AI-Researcher rather than from a generic multi-agent pattern.

## Source files

- `research_agent/inno/agents/inno_agent/survey_agent.py`
- `research_agent/inno/agents/inno_agent/prepare_agent.py`
- `research_agent/inno/agents/inno_agent/plan_agent.py`
- `research_agent/inno/agents/inno_agent/ml_agent.py`
- `research_agent/inno/agents/inno_agent/judge_agent.py`
- `research_agent/inno/agents/inno_agent/exp_analyser.py`
- `paper_agent/writing.py`
- `paper_agent/section_composer.py`
- `README.md` sections "How AI-Researcher works" and benchmark evaluation metrics

## Local role mapping

### Survey

Derived mainly from `get_survey_agent`, `Paper Survey Agent`, and `Code Survey Agent`.

- Break the user idea into atomic academic definitions before doing any synthesis.
- Require each atomic definition to be:
  - single and self-contained
  - mathematically grounded
  - implementable in code
  - traceable to specific papers
- Read papers thoroughly and extract:
  - formal definitions
  - mathematical formulas
  - key theoretical components
- Inspect codebases and extract:
  - corresponding implementations
  - implementation details
  - key functions and classes
- Merge theory and implementation notes only after all required atomic definitions have been covered.

### Critic

Derived mainly from `get_judge_agent` and its internal `Code Review Agent`, but applied in this skill at both idea stage and implementation-review stage.

- Check atomic ideas one by one instead of judging the project only at a high level.
- Compare the current proposal or implementation against survey notes and reference codebases.
- Reject toy-level reasoning or toy-level implementation.
- Produce structured change requests keyed by the specific idea component that is wrong, unclear, or incomplete.

### Code

Derived from `Prepare Agent`, `Coding Plan Agent`, and `Machine Learning Agent`.

- Select a small set of reference repositories after actual inspection, not by name only.
- Prefer repositories that are:
  - highly relevant
  - reasonably recent
  - well documented
  - structurally readable
  - Python-first and preferably PyTorch-based
  - runnable in the local environment
- Build a concrete plan that includes:
  - dataset plan
  - model plan
  - training plan
  - testing plan
- Implement a self-contained project:
  - keep all code inside the project workspace
  - do not import directly from reference repositories
  - adapt and rewrite code into one coherent codebase
  - document the origin and modification of adapted logic
- Implement every atomic academic definition from the survey notes.
- Avoid toy data and shortcuts unless explicitly approved.

### Adviser

Derived from `Judge Agent` and `Experiment Analysis Agent`.

- Review the executable design before experiments start.
- Review the evidence package before user handoff.
- Analyze results comprehensively, not just check file existence.
- Use reference papers and codebases to propose further experiments, corrections, visualizations, or stronger validations.
- Treat result analysis and refinement as first-class work, not an afterthought.

### Paper Writer

Derived from `paper_agent/writing.py` and `paper_agent/section_composer.py`.

- Use a hierarchical writing workflow:
  - methodology
  - related work
  - experiments
  - introduction
  - conclusion
  - abstract
- Preserve section content carefully when fusing subsections into a full draft.
- Maintain checkpoints for intermediate writing artifacts.
- Keep citations, equations, and technical content stable during section fusion and cleanup.

### Reviewer & Editor

Derived from the AI-Researcher benchmark criteria in `README.md`.

- Judge the paper against a top-tier submission bar using these dimensions:
  - novelty
  - experimental comprehensiveness
  - theoretical foundation
  - result analysis
  - writing quality
- Return actionable revision requests, not generic praise.
- In v1, still avoid claiming plagiarism clearance, AI-detection clearance, or formal proof verification.
