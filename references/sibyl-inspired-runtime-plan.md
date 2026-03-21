# Sibyl-Inspired Runtime Refactor Plan

## Purpose

This document captures the next major refactor direction for `ai-research-orchestrator`.

The goal is to borrow the runtime strengths of [Sibyl Research System](https://github.com/Sibyl-Research-Team/sibyl-research-system) while preserving the current product positioning:

- remain a portable Skill rather than a single-platform research OS
- support Codex, Claude Code, Openclaw, and similar agent shells
- keep exactly two agents per phase
- keep explicit human approval at every phase transition
- make in-phase progress visible instead of running as a black box

This is a system redesign plan, not a promise that every capability will be implemented in one step.

## Design Goals

- Borrow Sibyl's system capabilities except its many-agent phase topology.
- Preserve the current Skill-oriented packaging and cross-platform compatibility.
- Replace the current three-stage pipeline with a five-phase gated runtime.
- Keep every phase as a two-agent loop under a user-facing orchestrator.
- Introduce a system-level closed loop with reflection and controlled prompt evolution.
- Add runtime-level visibility, recovery, and execution management.

## Non-Goals

- Do not clone Sibyl's exact agent roster.
- Do not remove human decisions from phase transitions.
- Do not silently auto-pivot, auto-submit, or auto-modify prompts without approval.
- Do not tie the runtime to Claude Code-only assumptions.

## Core Principles

### 1. Skill First

The system remains a Skill package with templates, scripts, references, and state files. Advanced runtime features must be exposed through scripts and protocol files that can run in different agent clients.

### 2. Two Agents Per Phase

Each phase uses exactly two role prompts. Complex work is decomposed into iterative substeps inside that pair rather than expanded into many concurrent agents.

### 3. Human-Controlled Phase Gates

Each phase transition requires explicit human approval. Automatic loops are allowed only inside a phase.

### 4. Evidence Before Advancement

Phase advancement depends on scored evidence, not just file existence.

### 5. Visible Progress

Every phase must emit live-readable progress artifacts so the researcher can inspect current status, blockers, and recent decisions.

## Target Architecture

The refactor introduces two nested loops:

- `inner_loop`: phase-local iteration between the two agents
- `outer_loop`: orchestrator-level phase control, gate decisions, pivot proposals, recovery, and human approvals

The user-facing orchestrator remains the only role that talks directly to the user. All sub-agent prompts are rendered from fixed templates and then adjusted for the current task by the orchestrator.

## Five-Phase Workflow

### Phase 1: Literature and IDEA Research

Roles:

- `Survey`
- `Critic`

Purpose:

- expand the user IDEA into atomic academic definitions
- survey the recent field and necessary seminal work
- identify novelty gap, known baselines, likely failure modes, and research scope

Borrowed from Sibyl:

- stronger research planning discipline
- explicit quality checks before downstream execution
- structured phase scorecards

Primary outputs:

- `docs/survey/survey-round-summary.md`
- `docs/survey/critic-round-review.md`
- `docs/survey/research-readiness-report.md`
- `docs/survey/phase-scorecard.md`

Gate decision:

- human approval required before entering Phase 2

### Phase 2: Problem Analysis and Pilot Validation

Roles:

- `Pilot Code`
- `Pilot Adviser`

Purpose:

- convert the approved research direction into small-scale analytical validation
- test assumptions using toy settings, reduced data, reduced models, or low-cost sanity experiments
- reject fragile ideas before full experiments consume large compute budgets

Borrowed from Sibyl:

- pilot-first discipline
- early reality checks before large experiment cycles
- structured analysis of whether a direction deserves full execution

Primary outputs:

- `docs/pilot/problem-analysis.md`
- `code/configs/pilot-experiment-plan.md`
- `docs/pilot/pilot-results.md`
- `docs/pilot/pilot-adviser-review.md`
- `docs/pilot/pilot-validation-report.md`
- `docs/pilot/phase-scorecard.md`

Gate decision:

- human approval required before entering Phase 3

### Phase 3: Full Experiment

Roles:

- `Experiment Code`
- `Experiment Adviser`

Purpose:

- run the full experimental program
- execute baselines, ablations, robustness checks, and result analysis
- produce a complete experiment evidence package

Borrowed from Sibyl:

- managed execution loops
- runtime-level job control
- recovery from interrupted or failed runs
- quality gates around result completeness and reproducibility evidence

Primary outputs:

- `code/experiments/experiment-spec.md`
- `code/experiments/run-registry.md`
- `code/experiments/results-summary.md`
- `code/experiments/checkpoint-index.md`
- `docs/experiments/experiment-adviser-review.md`
- `docs/experiments/evidence-package-index.md`
- `docs/experiments/phase-scorecard.md`

Gate decision:

- human approval required before entering Phase 4

### Phase 4: Paper Development and Submission-Quality Review

Roles:

- `Paper Writer`
- `Reviewer & Editor`

Purpose:

- write the paper from approved evidence only
- iterate until the manuscript reaches top-tier submission readiness

Borrowed from AI-Researcher:

- structured academic writing workflow
- research-to-paper transformation discipline

Borrowed from Sibyl:

- runtime-level quality gate logic
- critique-driven iteration records

Primary outputs:

- `paper/paper-draft.md`
- `paper/reviewer-report.md`
- `paper/rebuttal-log.md`
- `paper/final-acceptance-report.md`
- `paper/phase-scorecard.md`

Gate decision:

- human approval required before entering Phase 5 or final handoff

### Phase 5: Reflection and Controlled Evolution

Roles:

- `Reflector`
- `Curator`

Purpose:

- turn project experience into reusable system improvements
- create lessons learned, prompt overlays, recovery heuristics, and gate-tuning suggestions
- preserve a system-level closed loop without allowing uncontrolled prompt drift

Borrowed from Sibyl:

- self-evolution
- system-level feedback loop
- long-horizon improvement from prior runs

Primary outputs:

- `docs/reflection/lessons-learned.md`
- `docs/reflection/overlay-draft.md`
- `docs/reflection/runtime-improvement-report.md`
- `docs/reflection/phase-scorecard.md`

Gate decision:

- human approval required before any overlay or runtime policy change becomes active

## Phase-Level Agent Logic

Every phase follows the same shape:

1. the orchestrator prepares the phase objective, required inputs, and constraints
2. Agent A produces the primary artifact
3. Agent B critiques, scores, or comments on the artifact
4. the orchestrator records progress and evaluates the phase gate
5. the phase either:
   - advances
   - loops for revision
   - proposes a pivot
   - escalates to the user

This preserves the current "main agent + two role agents" model while absorbing Sibyl's stronger runtime discipline.

## Automatic Quality Gates

The current validation flow must evolve from file checks into scored decisions.

Each phase gate should output one of:

- `advance`
- `revise`
- `pivot`
- `escalate_to_user`

Each gate must include:

- required deliverables
- evidence completeness checks
- phase-specific scoring rubric
- hard blockers
- pivot triggers
- escalation rules

Gate scorecards should be written to disk and summarized in the dashboard.

## PIVOT Mechanism

The runtime must support structured pivots rather than binary success/failure.

Allowed pivot types:

- narrow the research question
- replace the theoretical framing
- change datasets or baselines
- downgrade from full experiment back to pilot validation
- archive the current direction and start a new branch

Rules:

- only the orchestrator proposes pivots
- every pivot must include rationale, affected artifacts, and the cheapest viable alternative
- every pivot requires explicit human approval
- no silent pivoting is allowed

## GPU Scheduling and Remote Execution

The runtime should borrow Sibyl's operational strengths without becoming platform-specific.

### Execution Backends

Introduce a backend abstraction with support for:

- local shell execution
- SSH remote execution
- Docker container execution
- future extension to Slurm, RunPod, or Kubernetes

### GPU Scheduler

The scheduler should track:

- available devices
- current job ownership
- job heartbeats
- recovery eligibility
- release on failure or completion

### Runtime Records

Execution state should be written into project artifacts so progress remains visible to the researcher.

Proposed files:

- `.autoresearch/runtime/job-registry.yaml`
- `.autoresearch/runtime/gpu-registry.yaml`
- `.autoresearch/runtime/backend-registry.yaml`

## Self-Healing

Borrow Sibyl's failure recovery ideas, but keep actions controlled and inspectable.

The runtime should detect:

- interrupted long-running jobs
- missing expected artifacts
- stale heartbeats
- broken checkpoint chains
- failed phase gate prerequisites

Allowed recovery actions:

- retry
- resume
- regenerate non-experimental metadata
- escalate to user

The runtime must never silently skip failed work.

## Self-Evolution

The system should learn from completed runs, but changes must remain reviewable.

### Safe Evolution Model

Completed projects may produce:

- prompt overlay drafts
- gate tuning proposals
- recovery heuristics
- workflow refinements

### Explicit Constraint

Base prompts and base workflow rules must not be rewritten automatically.

Instead:

- overlays are generated as proposals
- the orchestrator may recommend adoption
- the user must approve activation

This preserves the closed-loop benefit without turning the runtime into an opaque, self-modifying system.

## Progress Visualization

Each phase must expose visible progress artifacts.

Required dashboard outputs:

- `.autoresearch/dashboard/status.json`
- `.autoresearch/dashboard/progress.md`
- `.autoresearch/dashboard/timeline.ndjson`

Each dashboard update should include:

- current phase
- current inner loop count
- current outer loop count
- current agent turn
- last gate result
- phase completion estimate
- active blockers
- active jobs
- remote backend status
- GPU allocation status
- next orchestrator action

## State Model Upgrade

The current `research-state.yaml` should be upgraded to include runtime fields beyond basic phase tracking.

Proposed fields:

- `project_id`
- `topic`
- `platform`
- `phase`
- `subphase`
- `inner_loop`
- `outer_loop`
- `gate_scores`
- `gate_history`
- `pivot_candidates`
- `human_decisions`
- `job_registry`
- `gpu_allocations`
- `remote_backends`
- `recovery_status`
- `overlay_stack`
- `progress`
- `deliverable_index`

`research-state.yaml` remains the only machine-readable source of truth.

## Prompt System Upgrade

The prompt system should be extended from "fixed template + dynamic task injection" to a three-layer composition model:

1. base role template
2. approved overlay layer
3. orchestrator dynamic injection layer

New prompt artifacts should include:

- orchestrator runtime prompt
- phase-specific role prompts
- gate review prompts
- reflection/evolution prompts

The orchestrator is still responsible for the final task-specific adjustment before a role is used.

## File and Directory Refactor

The current directory model has been refactored to use semantic names and a cleaner structure:

- `.autoresearch/` (system directory, hidden)
  - `state/` (state files)
  - `config/` (configuration)
  - `dashboard/` (runtime dashboard)
  - `runtime/` (job, GPU, backend registries)
  - `reference-papers/`
  - `templates/`
  - `archive/`
- `agents/` (per-role work directories)
  - `survey/`, `critic/`, `coder/`, `adviser/`, `writer/`, `reviewer/`, `reflector/`, `curator/`
- `paper/` (paper-related files)
- `code/` (code-related files)
  - `pilot/`, `experiments/`, `configs/`
- `docs/` (documentation and reports)
  - `reports/survey/`, `reports/pilot/`, `reports/experiments/`, `reports/reflection/`

Phase names are now semantic: `survey`, `pilot`, `experiments`, `paper`, `reflection`.
Legacy numbered names (`01-survey`, `02-pilot-analysis`, etc.) are still supported for backward compatibility.

## Planned Script Additions

New scripts should be added to support the runtime:

- `scripts/run_stage_loop.py`
- `scripts/quality_gate.py`
- `scripts/pivot_manager.py`
- `scripts/schedule_jobs.py`
- `scripts/run_remote_job.py`
- `scripts/sentinel.py`
- `scripts/recover_stage.py`
- `scripts/generate_dashboard.py`
- `scripts/apply_overlay.py`

## Planned Reference Additions

New references should document the runtime contract:

- `references/system-architecture.md`
- `references/recovery-and-evolution.md` (includes pivot policy, self-healing, self-evolution)
- `references/progress-visualization.md`
- `references/remote-execution.md`

## Implementation Milestones

### Milestone 1: Five-Phase State Machine

- upgrade the state schema
- redesign workflow and directory structure
- add phase and loop tracking
- preserve existing initialization compatibility

### Milestone 2: Quality Gates and Pivot Decisions

- implement scoring-based phase gates
- add scorecards and gate history
- add explicit pivot proposals and approval records

### Milestone 3: Pilot and Full Experiment Split

- separate lightweight validation from full-scale experiments
- redefine Code and Adviser responsibilities for both phases
- enforce low-cost early validation before large compute use

### Milestone 4: Runtime Operations

- add backend abstraction
- add GPU and remote execution state
- add heartbeat, sentinel, and recovery logic
- expose execution progress in dashboards

### Milestone 5: Reflection and Controlled Evolution

- add the fifth phase
- emit lessons learned and overlay drafts
- require approval before any overlay becomes active

## Acceptance Criteria

The refactor is complete only if all of the following are true:

- every phase uses exactly two agents
- every phase transition requires explicit human approval
- every phase produces visible progress artifacts
- the runtime can recommend `advance`, `revise`, `pivot`, or `escalate_to_user`
- pilot validation and full experiments are distinct phases
- remote execution and GPU usage are represented through a platform-neutral abstraction
- recovery logic exists and never hides failure
- self-evolution exists only through reviewable overlays
- the Skill remains usable from Codex, Claude Code, and Openclaw-style environments

## Risks and Mitigations

### Risk: runtime complexity grows too quickly

Mitigation:

- implement state machine, gates, and dashboards first
- delay advanced remote execution features until the core runtime is stable

### Risk: the system becomes too heavy for a Skill

Mitigation:

- keep advanced features behind configuration flags
- preserve graceful local-only execution

### Risk: human gates slow down the workflow

Mitigation:

- keep iteration automatic within a phase
- require approval only at phase boundaries and for pivots

### Risk: uncontrolled prompt drift

Mitigation:

- never auto-rewrite base prompts
- restrict evolution to explicit overlay proposals

## Immediate Next Step

The first implementation wave should focus on:

- five-phase state model
- scored quality gates
- pivot decision model
- progress dashboard

That is the smallest change set that meaningfully brings the Skill closer to Sibyl's system strengths while preserving human control and cross-platform portability.
