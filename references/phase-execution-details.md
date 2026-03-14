# Phase Execution Details

This document expands each phase into concrete substeps, drawing structural inspiration from Sibyl's stage decomposition and AI-Researcher's role-specific task definitions while preserving the two-agent-per-phase rule in this Skill.

## Phase 1: Literature and IDEA Research

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

## Phase 2: Problem Analysis and Pilot Validation

Internal progress pattern:

1. operational problem analysis
2. pilot design
3. low-cost execution
4. pilot interpretation
5. pilot go/no-go recommendation

`Code` substeps:

- translate the approved idea into operational hypotheses
- define minimal data/model/metric setup
- run low-cost validation
- summarize outcomes and anomalies

`Adviser` substeps:

- verify the pilot can actually discriminate the idea from trivial alternatives
- evaluate whether failure conditions were observed and recorded
- recommend full experiment, revision, or pivot

## Phase 3: Full Experiment

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

## Phase 4: Paper Development and Submission-Quality Review

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

## Phase 5: Reflection and Controlled Evolution

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
