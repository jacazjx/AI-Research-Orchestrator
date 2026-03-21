# References Documentation Index

This directory contains reference documents that define the protocols, standards, and guidelines for the AI Research Orchestrator.

## Recommended Reading Order

### First-Time Readers

1. `workflow.md` [Required] - Five-phase workflow, gate requirements, loop policies, and phase execution details
2. `system-architecture.md` [Required] - Dual-loop runtime architecture
3. `orchestrator-protocol.md` [Required] - Orchestrator coordination protocols
4. `gate-rubrics.md` [Required] - Quality gate scoring system
5. `agent-roles.md` [Required] - All agent roles, pairings, and communication protocols

### Deep Dive

6. `deliverable-contracts.md` - Expected outputs for each phase
7. `citation-standards.md` - Citation verification, authenticity, and formatting
8. `evidence-standards.md` - Evidence handling, experiment integrity, and validation

### Quality Assurance

9. `writing-standards.md` - Academic writing, figures/tables, paper quality assurance
10. `scientific-method.md` - Experimental design, hypothesis testing, reproducibility, validity
11. `critical-thinking.md` - Logical fallacies, cognitive biases, argument analysis, evidence evaluation

### Operational

12. `recovery-and-evolution.md` - Pivot policy, rollback, self-healing, self-evolution
13. `remote-execution.md` - Remote execution abstraction

---

## Document Categories

### Core Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `workflow.md` | Required | Five-phase order, gate requirements, loop policies, and phase execution substeps |
| `orchestrator-protocol.md` | Required | Orchestrator responsibilities: intent alignment, phase coordination, quality assurance |
| `system-architecture.md` | Required | Dual-loop runtime design (inner_loop, outer_loop) and directory structure |

### Gate and Scoring

| Document | Status | Description |
|----------|--------|-------------|
| `gate-rubrics.md` | Required | Detailed scoring rubrics for all five gates with thresholds and blocking issues |

### Execution Details

| Document | Status | Description |
|----------|--------|-------------|
| `deliverable-contracts.md` | Required | Canonical paths and content requirements for each deliverable |

### Quality Assurance

| Document | Status | Description |
|----------|--------|-------------|
| `citation-standards.md` | Required | Citation verification, authenticity, formatting, and academic API usage |
| `evidence-standards.md` | Required | Evidence rules, experiment integrity, logging, statistical validity |
| `writing-standards.md` | Required | Academic writing, figures/tables, citation formats, paper quality assurance |

### Operations Management

| Document | Status | Description |
|----------|--------|-------------|
| `remote-execution.md` | Optional | Platform-neutral execution abstraction (local, SSH backends) |
| `recovery-and-evolution.md` | Required | Pivot policy, rollback, self-healing, self-evolution |

### Role and Agent Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `agent-roles.md` | Required | All 8 agent roles, pairings per phase, communication protocols, AI-Researcher mapping |
| `prompt-customization.md` | Required | Fixed template usage, dynamic injection, what stays fixed |

### Clarification Protocols

| Document | Status | Description |
|----------|--------|-------------|
| `intent-clarification-protocol.md` | Required | Process for clarifying research intent before phase work begins |
| `project-takeover-protocol.md` | Optional | Procedures for taking over existing research projects |

### Research Methodology

| Document | Status | Description |
|----------|--------|-------------|
| `scientific-method.md` | Required | Experimental design, hypothesis testing, reproducibility, validity types |
| `critical-thinking.md` | Required | Logical fallacies, cognitive biases, argument analysis, evidence evaluation |

### Design and Planning

| Document | Status | Description |
|----------|--------|-------------|
| `runtime-design-document.md` | Optional | Complete runtime design (Chinese), agent responsibilities, quality gates |
| `sibyl-inspired-runtime-plan.md` | Optional | Future refactor direction inspired by Sibyl Research System |
| `reporting_standards.md` | Optional | Summaries of CONSORT, PRISMA, STROBE, ARRIVE, MIAME standards |

### Other References

| Document | Status | Description |
|----------|--------|-------------|
| `database_search_strategies.md` | Required | Academic database search strategies |
| `integration-guide.md` | Optional | Integration with external tools |
| `progress-visualization.md` | Required | Dashboard file requirements |
| `skill-dependency-graph.md` | Optional | Skill invocation order per agent |

---

## Quick Reference by Phase

### Survey Phase

- `workflow.md` - Phase 1 workflow and substeps
- `citation-standards.md` - Citation verification
- `evidence-standards.md` - Literature evidence rules
- `gate-rubrics.md` - Gate 1 criteria

### Pilot Phase

- `workflow.md` - Phase 2 workflow and substeps
- `recovery-and-evolution.md` - When/how to pivot
- `gate-rubrics.md` - Gate 2 criteria

### Experiments Phase

- `workflow.md` - Phase 3 workflow and substeps
- `evidence-standards.md` - Logging and verification
- `remote-execution.md` - Job scheduling
- `recovery-and-evolution.md` - Failure recovery
- `gate-rubrics.md` - Gate 3 criteria

### Paper Phase

- `workflow.md` - Phase 4 workflow and substeps
- `citation-standards.md` - Citation audit
- `writing-standards.md` - Quality standards and formatting
- `gate-rubrics.md` - Gate 4 criteria

### Reflection Phase

- `workflow.md` - Phase 5 workflow and substeps
- `recovery-and-evolution.md` - Overlay system
- `gate-rubrics.md` - Gate 5 criteria

---

## Legend

- **Required**: Must read for understanding the system
- **Optional**: Read when working on specific features or deep-diving
