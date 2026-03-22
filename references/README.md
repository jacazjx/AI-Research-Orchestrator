# References Index

Runtime reference documents for the AI Research Orchestrator. Design documents live in `docs/design/`.

## Core Protocol (read first)

| Document | Description |
|----------|-------------|
| `workflow.md` | Five-phase workflow, gate requirements, loop policies, phase execution |
| `system-architecture.md` | Dual-loop runtime architecture (inner_loop, outer_loop) |
| `orchestrator-protocol.md` | Orchestrator coordination, intent alignment, phase control |
| `gate-rubrics.md` | Scoring rubrics for all five quality gates |
| `agent-roles.md` | Agent roles, pairings per phase, communication protocols |
| `deliverable-contracts.md` | Required outputs and canonical paths for each phase |

## Quality and Evidence

| Document | Description |
|----------|-------------|
| `citation-standards.md` | Citation verification, authenticity, formatting, academic API usage |
| `evidence-standards.md` | WHAT to document: traceability, reproducibility, directory structure for experiment artifacts |
| `writing-standards.md` | Academic writing, figures/tables, citation formats, paper quality assurance |
| `scientific-rigor.md` | HOW to design: experimental methodology, hypothesis testing, bias avoidance |
| `statistical-reporting.md` | HOW to report: statistical tests, effect sizes, confidence intervals, APA format |
| `reporting_standards.md` | CONSORT, PRISMA, STROBE, ARRIVE, MIAME reporting standards |
| `venue-requirements.md` | Venue-specific formatting, page limits, checklists, and pre-submission requirements for major ML/AI conferences |

## Operations

| Document | Description |
|----------|-------------|
| `recovery-and-evolution.md` | Pivot policy, rollback, self-healing, controlled self-evolution |
| `project-takeover-protocol.md` | Edge-case guidance for adopting existing projects |
| `database_search_strategies.md` | Academic database search strategies and query construction |

## Design Documents (in `docs/design/`)

| Document | Description |
|----------|-------------|
| `sibyl-inspired-runtime-plan.md` | Future refactor direction inspired by Sibyl Research System |
| `runtime-design-document.md` | Complete runtime design, agent responsibilities, quality gates |
| `integration-guide.md` | Integration with external tools (Codex MCP, Feishu, Zotero) |
