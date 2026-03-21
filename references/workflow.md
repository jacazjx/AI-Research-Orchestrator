# Workflow

Use this skill as a gated five-phase research runtime for one project at a time.

---

## Phase Order

The project uses semantic phase names:

1. `.autoresearch/`: initialize workspace, state, config, dashboard, runtime registries, idea brief, and reference drop zone.
2. `survey`: run `Survey <-> Critic` until the research-readiness package is strong enough for human review.
3. `pilot`: run `Pilot Code <-> Pilot Adviser` on problem analysis and low-cost validation before full experiments.
4. `experiments`: run `Experiment Code <-> Experiment Adviser` on the full matrix, execution provenance, and evidence package.
5. `paper`: run `Paper Writer <-> Reviewer & Editor` until the manuscript reaches top-tier submission readiness.
6. `reflection`: run `Reflector <-> Curator` to produce lessons learned, overlay drafts, and runtime improvement proposals.
7. `.autoresearch/archive/`: store superseded drafts, rejected pivots, and retired overlays without polluting live deliverables.

> **Backward Compatibility**: Legacy numbered phase names (`01-survey`, `02-pilot-analysis`, etc.) are still supported, but semantic names are recommended.

---

## Required Human Gates

- Gate 1: approve `docs/survey/research-readiness-report.md` before pilot analysis.
- Gate 2: approve `docs/pilot/pilot-validation-report.md` before full experiments.
- Gate 3: approve `docs/experiments/evidence-package-index.md` before paper writing.
- Gate 4: approve `paper/final-acceptance-report.md` before reflection or final handoff.
- Gate 5: approve `docs/reflection/runtime-improvement-report.md` before any overlay or runtime policy change becomes active.

When a human gate rejects the current phase:

- the orchestrator must present the allowed return phases
- the orchestrator may recommend a return phase based on the current blockers
- the user decides whether to stay in the same phase or roll back to an earlier phase
- no automatic rollback is allowed without that human decision

---

## Loop Policy

- `Survey` and `Critic` may iterate up to the configured `survey_critic` loop limit.
- `Code` and `Adviser` may iterate in pilot analysis up to `pilot_code_adviser`.
- `Code` and `Adviser` may iterate in full experiments up to `experiment_code_adviser`.
- `Paper Writer` and `Reviewer & Editor` may iterate up to `writer_reviewer`.
- `Reflector` and `Curator` may iterate up to `reflector_curator`.
- Once a loop reaches its limit without approval, escalate to the user instead of continuing autonomously.

---

## Runtime Rules

- `.autoresearch/state/research-state.yaml` is the only machine-readable truth.
- `.autoresearch/config/orchestrator-config.yaml` is the project-level runtime configuration.
- `.autoresearch/dashboard/` is the canonical place for visible progress artifacts.
- Every deliverable path referenced in the state must remain project-relative.
- Pivots may be proposed automatically, but never executed without explicit human approval.
- Paper writing must include a citation-authenticity pass before Gate 4.

**Agent Teams Update:** At the start of each phase, the Orchestrator creates a team with `TeamCreate`. When the phase ends, the Orchestrator sends a `shutdown_request` to each agent via `SendMessage`, then calls `TeamDelete` to disband the team.

---

## Phase Execution Details

This section expands each phase into concrete substeps, drawing structural inspiration from Sibyl's stage decomposition and AI-Researcher's role-specific task definitions while preserving the two-agent-per-phase rule.

**Agent Teams Update:** Within each phase, Primary and Reviewer iterate directly via `SendMessage` without the Orchestrator relaying their exchanges. When a substep is blocked and cannot be resolved internally, the Primary agent signals the Orchestrator by calling `TaskUpdate(status="blocked")`, which triggers Orchestrator escalation handling.

### Phase 1: Literature and IDEA Research

Internal progress pattern:

1. intake normalization
2. atomic definition expansion
3. recent literature sweep
4. seminal backfill only where needed
5. novelty and risk attack
6. readiness synthesis

`Survey` substeps:

- normalize IDEA into problem statement, target claim, constraints, and evaluation target
- produce atomic academic definitions
- map theory to candidate implementation obligations
- build codebase and dataset candidate shortlist

`Critic` substeps:

- attack novelty and scope assumptions
- identify theory gaps and likely failure modes
- identify what pilot validation must prove or falsify
- recommend same-phase revision or fallback to an earlier framing

### Phase 2: Problem Validation and Pilot Analysis

Internal progress pattern:

1. problem validation
2. operational problem analysis
3. pilot design
4. low-cost execution
5. pilot interpretation
6. pilot go/no-go recommendation

#### Substep: Problem Validation

Before committing resources to problem analysis, validate that:

- **Problem Exists**: Evidence from literature, data, or practical sources
- **Problem Matters**: Academic, practical, or social significance
- **Problem Is Unsolved**: Gap analysis shows room for contribution

`Code` substeps (problem_validation):

- gather evidence that the problem actually exists
- assess significance across academic/practical/timeliness/feasibility
- identify what would be lost if this problem is not addressed
- produce validation verdict: Validated/Reformulate/Defer/Pivot

`Adviser` substeps (audit-validation):

- verify evidence quality and source credibility
- challenge significance assessment
- ensure verdict follows logically from evidence

#### Substep: Problem Analysis

`Code` substeps (problem_analysis):

- translate the validated problem into operational hypotheses
- define minimal data/model/metric setup
- identify technical challenges and solution approaches
- summarize feasibility assessment

`Adviser` substeps (audit-analysis):

- verify the problem decomposition is complete
- challenge solution approach assumptions
- ensure feasibility assessment is honest

#### Substep: Pilot Design & Execution

`Code` substeps:

- design minimal experiment that validates core hypothesis
- run low-cost validation
- summarize outcomes and anomalies

`Adviser` substeps:

- verify the pilot can actually discriminate the idea from trivial alternatives
- evaluate whether failure conditions were observed and recorded
- recommend full experiment, revision, or pivot

### Phase 3: Full Experiment

Internal progress pattern:

1. freeze experiment matrix
2. schedule and execute runs
3. collect logs and checkpoints
4. aggregate results
5. adviser evidence review
6. final evidence-pack synthesis

`Code` substeps:

- freeze dataset/baseline/metric/ablation plan
- manage run registry, checkpoints, and result tables
- keep provenance and reproducibility evidence current

`Adviser` substeps:

- audit baseline and ablation completeness
- audit negative-result handling
- determine whether the evidence is strong enough for paper writing

### Phase 4: Paper Development and Submission-Quality Review

Internal progress pattern:

1. outline and section planning
2. draft section composition
3. citation authenticity audit
4. structured review
5. rebuttal and revision
6. submission-readiness judgment

`Paper Writer` substeps:

- compose section hierarchy
- draft the manuscript from approved evidence only
- run citation-gap discovery and citation verification
- update the citation audit report
- revise according to reviewer findings

`Reviewer & Editor` substeps:

- check novelty, theory, experiments, and writing quality
- audit citation authenticity and support quality
- distinguish structural blockers from editorial polish
- determine whether the draft is at top-tier submission level

### Phase 5: Reflection and Controlled Evolution

Internal progress pattern:

1. lessons extraction
2. runtime and prompt reflection
3. overlay drafting
4. curator review
5. opt-in recommendation package

`Reflector` substeps:

- identify reusable success patterns
- identify expensive dead ends and recovery patterns
- draft overlay and runtime change proposals

`Curator` substeps:

- review portability and safety
- reject uncontrolled prompt drift
- separate approved-for-consideration changes from archival notes
