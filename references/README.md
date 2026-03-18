# References Documentation Index

This directory contains 28 reference documents that define the protocols, standards, and guidelines for the AI Research Orchestrator.

## Recommended Reading Order

### First-Time Readers

1. `workflow-protocol.md` [Required] - Start here to understand the five-phase workflow
2. `system-architecture.md` [Required] - Understand the dual-loop runtime architecture
3. `orchestrator-protocol.md` [Required] - Learn how the orchestrator coordinates everything
4. `gate-rubrics.md` [Required] - Understand the quality gate scoring system
5. `phase-execution-details.md` [Required] - Dive into specific substeps per phase

### Deep Dive

6. `deliverable-contracts.md` - Learn expected outputs for each phase
7. `role-protocols.md` - Understand each agent's responsibilities
8. `ai-researcher-agent-mapping.md` - See how roles derive from AI-Researcher

### Quality Assurance

9. `citation-authenticity.md` - Citation verification in paper phase
10. `experiment-integrity.md` - Experiment logging and result authenticity
11. `literature-verification.md` - Citation verification in survey phase
12. `paper-quality-assurance.md` - Top-tier submission standards

### Operational

13. `remote-execution.md` - Remote execution abstraction
14. `self-healing.md` - Failure recovery model
15. `self-evolution.md` - Controlled prompt evolution

---

## Document Categories

### Core Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `workflow-protocol.md` | Required | Defines the five-phase order, gate requirements, and loop policies |
| `orchestrator-protocol.md` | Required | Orchestrator responsibilities: intent alignment, phase coordination, quality assurance |
| `system-architecture.md` | Required | Dual-loop runtime design (inner_loop, outer_loop) and directory structure |

### Gate and Scoring

| Document | Status | Description |
|----------|--------|-------------|
| `gate-rubrics.md` | Required | Detailed scoring rubrics for all five gates with thresholds and blocking issues |

### Execution Details

| Document | Status | Description |
|----------|--------|-------------|
| `phase-execution-details.md` | Required | Substeps within each phase, internal progress patterns |
| `deliverable-contracts.md` | Required | Canonical paths and content requirements for each deliverable |

### Quality Assurance

| Document | Status | Description |
|----------|--------|-------------|
| `citation-authenticity.md` | Required | Paper-phase citation handling, verification process, Grade A-F system |
| `experiment-integrity.md` | Required | Experiment logging standards, result verification, fabrication detection |
| `literature-verification.md` | Required | Survey-phase citation verification using academic database APIs |
| `paper-quality-assurance.md` | Required | Top-tier venue standards, review dimensions, citation audit protocol |

### Operations Management

| Document | Status | Description |
|----------|--------|-------------|
| `remote-execution.md` | Optional | Platform-neutral execution abstraction (local, SSH backends) |
| `self-healing.md` | Optional | Bounded recovery model, detection targets, allowed recovery actions |
| `self-evolution.md` | Optional | Controlled evolution through approved overlays |

### Policy Documents

| Document | Status | Description |
|----------|--------|-------------|
| `pivot-policy.md` | Required | Allowed pivot types, approval requirements, no silent pivoting |
| `evidence-rules.md` | Required | Evidence handling for literature, code, datasets, experiments, writing |
| `progress-visualization.md` | Required | Dashboard file requirements (status.json, progress.md, timeline.ndjson) |

### Role and Agent Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `role-protocols.md` | Required | Responsibilities for all eight roles (Survey, Critic, Code, Adviser, Writer, Reviewer, Reflector, Curator) |
| `ai-researcher-agent-mapping.md` | Optional | How roles derive from HKUDS/AI-Researcher source agents |
| `prompt-customization.md` | Required | Fixed template usage, dynamic injection, what stays fixed |

### Clarification Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `intent-clarification-protocol.md` | Required | Process for clarifying research intent before phase work begins |
| `project-takeover-protocol.md` | Optional | Procedures for taking over existing research projects |

### Design and Planning

| Document | Status | Description |
|----------|--------|-------------|
| `runtime-design-document.md` | Optional | Complete runtime design (Chinese), agent responsibilities, quality gates |
| `sibyl-inspired-runtime-plan.md` | Optional | Future refactor direction inspired by Sibyl Research System |
| `reporting_standards.md` | Optional | Summaries of CONSORT, PRISMA, STROBE, ARRIVE, MIAME standards |

### Subdirectories

#### `critical-thinking/`

| Document | Status | Description |
|----------|--------|-------------|
| `argument-analysis.md` | Optional | Comprehensive guide to analyzing research arguments |
| `logical-fallacies.md` | Optional | Catalog of logical fallacies in research contexts |
| `evidence-evaluation.md` | Optional | Framework for evaluating evidence quality and strength |
| `cognitive-biases.md` | Optional | Catalog of cognitive biases affecting research judgment |

#### `evidence-framework/`

| Document | Status | Description |
|----------|--------|-------------|
| `causal-inference.md` | Optional | Causal inference frameworks (Pearl, Rubin, DAGs) |
| `evidence-hierarchy.md` | Optional | Classic evidence pyramid and GRADE framework |
| `grade-framework.md` | Optional | GRADE approach adapted for AI/ML research evaluation |
| `meta-analysis.md` | Optional | Meta-analysis methods for combining study results |

#### `scientific-method/`

| Document | Status | Description |
|----------|--------|-------------|
| `hypothesis-testing.md` | Required | Hypothesis formulation, statistical significance, effect sizes |
| `validity-types.md` | Required | Internal, external, construct, ecological validity |
| `reproducibility.md` | Required | Reproducibility standards, preregistration templates |
| `experimental-design.md` | Required | Randomization, blinding, confounders, sample size |

#### `writing-standards/`

| Document | Status | Description |
|----------|--------|-------------|
| `academic-conventions.md` | Required | Academic writing principles, structure, style |
| `citation-formats.md` | Optional | IEEE, ACM, APA, MLA, BibTeX formats |
| `apa-style.md` | Optional | APA 7th edition specific guidelines |
| `figure-standards.md` | Required | Figure and table standards, formatting conventions |

---

## Quick Reference by Phase

### Survey Phase

- `workflow-protocol.md` - Phase 1 workflow
- `phase-execution-details.md` - Survey substeps
- `literature-verification.md` - Citation verification
- `evidence-rules.md` - Literature evidence rules
- `gate-rubrics.md` - Gate 1 criteria

### Pilot Phase

- `workflow-protocol.md` - Phase 2 workflow
- `phase-execution-details.md` - Pilot substeps
- `pivot-policy.md` - When/how to pivot
- `gate-rubrics.md` - Gate 2 criteria

### Experiments Phase

- `workflow-protocol.md` - Phase 3 workflow
- `phase-execution-details.md` - Experiment substeps
- `experiment-integrity.md` - Logging and verification
- `remote-execution.md` - Job scheduling
- `self-healing.md` - Failure recovery
- `gate-rubrics.md` - Gate 3 criteria

### Paper Phase

- `workflow-protocol.md` - Phase 4 workflow
- `phase-execution-details.md` - Paper substeps
- `citation-authenticity.md` - Citation audit
- `paper-quality-assurance.md` - Quality standards
- `gate-rubrics.md` - Gate 4 criteria

### Reflection Phase

- `workflow-protocol.md` - Phase 5 workflow
- `phase-execution-details.md` - Reflection substeps
- `self-evolution.md` - Overlay system
- `gate-rubrics.md` - Gate 5 criteria

---

## Legend

- **Required**: Must read for understanding the system
- **Optional**: Read when working on specific features or deep-diving