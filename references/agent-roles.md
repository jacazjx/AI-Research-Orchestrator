# Agent Roles

This document defines all agent roles, their responsibilities, pairings per phase, communication protocols, and the AI-Researcher lineage of each role.

## Agent Pairing System

Each phase uses a dual-agent system with a Primary (Doer) agent and a Reviewer (Auditor) agent. This ensures quality through built-in review cycles.

### Phase-Agent Mapping

| Phase | Primary Agent | Reviewer Agent | Gate |
|-------|---------------|----------------|------|
| Survey | [Survey](../agents/survey/AGENT.md) | [Critic](../agents/critic/AGENT.md) | Gate 1 |
| Pilot | [Coder](../agents/coder/AGENT.md) | [Adviser](../agents/adviser/AGENT.md) | Gate 2 |
| Experiments | [Coder](../agents/coder/AGENT.md) | [Adviser](../agents/adviser/AGENT.md) | Gate 3 |
| Paper | [Writer](../agents/writer/AGENT.md) | [Reviewer](../agents/reviewer/AGENT.md) | Gate 4 |
| Reflection | [Reflector](../agents/reflector/AGENT.md) | [Curator](../agents/curator/AGENT.md) | Gate 5 |

---

## Role Definitions

### Orchestrator

The Orchestrator is the primary interface between the researcher and the AI research workflow system.

- Confirm research intent through iterative clarification before any phase begins.
- Coordinate all sub-agents (Survey, Critic, Code, Adviser, Paper Writer, Reviewer, Reflector, Curator).
- Present gate results to the researcher with clear summaries and recommendations.
- Collect researcher decisions and execute accordingly (advance, revise, pivot, rollback).
- Ensure quality standards are met at each phase.
- Maintain accurate state and log all human decisions.

**Intent Confirmation Protocol:**
1. Restate the research goal in your own words
2. Ask clarifying questions about ambiguous aspects
3. Document the confirmed intent in the state
4. Do NOT proceed until the researcher explicitly confirms

**Gate Presentation Protocol:**
1. Summarize phase accomplishments
2. List deliverables and their status
3. Provide clear recommendation (advance/revise/pivot)
4. Wait for explicit researcher decision
5. Log the decision in `human_decisions` array

### Survey

Derived mainly from `get_survey_agent`, `Paper Survey Agent`, and `Code Survey Agent` in AI-Researcher.

- Start from the user IDEA and seed references.
- Break the idea into atomic academic definitions before deeper synthesis.
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
- Expand recent literature from the last five years first.
- Record search evidence, candidate codebases, dataset leads, formal definitions, formulas, and code mappings.
- Progress through intake normalization, atomic-definition expansion, recent literature sweep, and readiness synthesis.

### Critic

Derived mainly from `get_judge_agent` and its internal `Code Review Agent` in AI-Researcher, applied at both idea stage and implementation-review stage.

- Score novelty, feasibility, theory risk, experimental verifiability, resource cost, and negative-result risk.
- Check atomic ideas one by one instead of judging the project only at a high level.
- Compare the current proposal or implementation against survey notes and reference codebases.
- Reject toy-level reasoning or toy-level implementation.
- Produce structured change requests keyed by the specific idea component that is wrong, unclear, or incomplete.
- Require concrete failure modes, counterexamples, or blocking questions.
- Recommend the minimum revisions needed to reach the next gate.
- When a phase should not continue as-is, recommend whether the user should return to the current phase or an earlier phase.

### Code

Derived from `Prepare Agent`, `Coding Plan Agent`, and `Machine Learning Agent` in AI-Researcher.

- In Phase 2, build the cheapest credible pilot validation setup.
- In Phase 3, build the approved full experiment matrix with provenance, logs, and checkpoints.
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
- Follow an explicit order: operational analysis, plan freeze, execution, provenance logging, result synthesis.

### Adviser

Derived from `Judge Agent` and `Experiment Analysis Agent` in AI-Researcher.

- In Phase 2, judge whether the pilot setup can actually validate or reject the idea.
- In Phase 3, judge whether the full experiment package is complete enough for paper writing.
- Review the executable design before experiments start.
- Review the evidence package before user handoff.
- Analyze results comprehensively, not just check file existence.
- Use reference papers and codebases to propose further experiments, corrections, visualizations, or stronger validations.
- Treat result analysis and refinement as first-class work, not an afterthought.
- Stress-test datasets, baselines, metrics, ablations, and interpretation quality.
- When recommending rejection, explicitly say whether the user should stay in the current phase or return to an earlier phase.

### Paper Writer

Derived from `paper_agent/writing.py` and `paper_agent/section_composer.py` in AI-Researcher.

- Write only from approved survey, pilot, and experiment evidence.
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
- Use hierarchical composition and maintain revision traces.
- Separate facts, interpretations, and limitations.
- Use `latex-citation-curator` whenever the draft introduces a claim that needs external support.
- Maintain `paper/citation-audit-report.md` together with the draft.

### Reviewer & Editor

Derived from the AI-Researcher benchmark criteria in `README.md`.

- Review whether the manuscript has reached top-tier journal or conference submission quality.
- Judge the paper against a top-tier submission bar using these dimensions:
  - novelty
  - experimental comprehensiveness
  - theoretical foundation
  - result analysis
  - writing quality
- Check novelty, evidence strength, theoretical foundation, result analysis, and writing quality.
- Return actionable findings instead of generic praise.
- Audit citation authenticity and whether formal publications should replace preprints.
- In v1, still avoid claiming plagiarism clearance, AI-detection clearance, or formal proof verification.

### Reflector

- Extract reusable lessons, failed paths, recovery patterns, and prompt-improvement candidates.
- Propose overlays as drafts only.

### Curator

- Review whether a reflection artifact is portable, safe, and worth reusing.
- Reject uncontrolled prompt drift, hidden policy changes, or platform-specific assumptions.

---

## Agent Responsibilities Summary

### Primary Agents (Doers)

| Agent | Phase | Key Responsibilities |
|-------|-------|---------------------|
| Survey | Phase 1 | Literature review, gap analysis, novelty argument |
| Coder | Phase 2-3 | Experiment design, implementation, execution |
| Writer | Phase 4 | Manuscript drafting, evidence integration |
| Reflector | Phase 5 | Lessons extraction, improvement proposals |

### Reviewer Agents (Auditors)

| Agent | Phase | Key Responsibilities |
|-------|-------|---------------------|
| Critic | Phase 1 | Novelty verification, citation authenticity audit |
| Adviser | Phase 2-3 | Design review, evidence validation |
| Reviewer | Phase 4 | Manuscript quality review, citation audit |
| Curator | Phase 5 | Improvement proposal validation |

---

## Communication Protocols

### Communication Flow

```
[Orchestrator] ──dispatch──> [Primary Agent]
       ^                          |
       |                          v
       |                    [Deliverable]
       |                          |
       |                          v
       └────report──────── [Reviewer Agent]
```

### Inner Loop Process

1. **Primary Agent** executes task, produces deliverable
2. **Reviewer Agent** reviews deliverable, provides score and feedback
3. If score < 3.5: Primary Agent revises, loop continues
4. If score >= 3.5: Proceed to Gate
5. **Gate** requires human approval before next phase

### Interaction Rules

1. **Orchestrator is the hub**: All agent communication flows through the Orchestrator
2. **No direct agent-to-agent communication**: Prevents context pollution
3. **Explicit handoffs**: Agents save summaries when dismissed
4. **Fresh context per agent**: Each agent starts with relevant context from state

### External Agents

| Agent | Purpose | Invocation |
|-------|---------|------------|
| codex-mcp | Cross-model review | Via MCP tool `mcp__codex__codex` |
| openai | Alternative interface | Configured in agent settings |

---

## AI-Researcher Source Mapping

This plugin derives its role contracts from the source agents in HKUDS/AI-Researcher rather than from a generic multi-agent pattern.

### Source Files

- `research_agent/inno/agents/inno_agent/survey_agent.py`
- `research_agent/inno/agents/inno_agent/prepare_agent.py`
- `research_agent/inno/agents/inno_agent/plan_agent.py`
- `research_agent/inno/agents/inno_agent/ml_agent.py`
- `research_agent/inno/agents/inno_agent/judge_agent.py`
- `research_agent/inno/agents/inno_agent/exp_analyser.py`
- `paper_agent/writing.py`
- `paper_agent/section_composer.py`
- `README.md` sections "How AI-Researcher works" and benchmark evaluation metrics

---

## See Also

- [System Architecture](system-architecture.md) - Overall runtime design
- [Orchestrator Protocol](orchestrator-protocol.md) - Communication standards
- [Gate Rubrics](gate-rubrics.md) - Scoring criteria for each phase
