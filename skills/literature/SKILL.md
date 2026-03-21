---
name: airesearchorchestrator:literature
agent: survey
description: Unified literature skill covering quick landscape checks, comprehensive systematic reviews, and research intent clarification. The agent decides depth based on context -- from a rapid 5-paper exploration to a full 7-phase systematic survey with PRISMA flow and mandatory visualizations. Use when user says "literature survey", "find papers", "check literature", "文献调研", "systematic review", "quick literature search", "研究意图澄清", or needs any level of literature exploration.
user-invocable: false
argument-hint: [research-topic-or-question]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent, Skill, AskUserQuestion
---
# Literature

## Overview

A unified literature skill that adapts its depth and approach based on context. The agent chooses from three modes -- quick exploration, standard review, or systematic survey -- based on the research question's maturity, the project phase, and whether gate approval is needed.

## Purpose

- Conduct literature exploration at the appropriate depth for the current need
- Clarify research intent when ideas are vague before committing to a full survey
- Map research landscapes using academic database APIs
- Verify citations for authenticity
- Produce deliverables appropriate for quality gates

## Mode Selection

The agent decides which mode to use based on context. These are not sequential phases; pick one.

| Mode | When to Use | Typical Time | Gate Ready |
|------|-------------|--------------|------------|
| **Quick Exploration** | Fast overview, exploring a new area, finding 5-10 papers | Minutes | No |
| **Standard Review** | Structured search with gap analysis and novelty assessment | Hours | Partial |
| **Systematic Survey** | Formal PRISMA-compliant review, Gate 1 approval required | Hours-Days | Yes |

If the research idea is too vague (clarity < 0.4), run intent clarification first before any mode.

---

## Intent Clarification (Pre-Mode)

Use when the research idea is vague or underspecified. Clarifies the researcher's intent before any literature search begins.

### Clarity Assessment

Evaluate the research idea across five dimensions:

| Dimension | Weight | What to Assess |
|-----------|--------|----------------|
| Problem Definition | 25% | Is the specific problem clearly stated? |
| Solution Direction | 25% | Is there a sense of what approach might work? |
| Contribution Type | 20% | Is the expected contribution type clear? (method/theory/application/benchmark/survey) |
| Constraints | 15% | Are timeline, resources, and venue understood? |
| Novelty Claim | 15% | Is there a hypothesis about what's new? |

**Score interpretation**:
- 0.0-0.3: Very vague -- recommend invoking `ideation` skill for brainstorming
- 0.3-0.4: Unclear -- recommend brainstorming
- 0.4-0.6: Partially clear -- run clarification loop (2-3 targeted questions per round)
- 0.6-0.8: Mostly clear -- minor clarifications needed
- 0.8-1.0: Clear -- proceed to literature search

**Clarification loop**: Maximum 5 rounds. Target clarity >= 0.7. If score remains < 0.4 after 2 rounds, recommend `ideation` skill. Document Q&A in `.autoresearch/research-intent-confirmation.md`. Get explicit researcher confirmation before proceeding.

---

## Mode 1: Quick Exploration

**Goal**: Rapidly map the landscape around a topic -- identify key papers, sub-directions, and open problems.

**Output**: Working notes with 5-10 papers, one-sentence contribution per paper, and a landscape sketch (sub-directions, gaps, recurring limitations).

### Guidance

- Use academic APIs (see API reference below), not web search
- Prefer papers from the last 2-3 years; include seminal papers for context
- Note concurrent work (last 3-6 months)

---

## Mode 2: Standard Review

**Goal**: Produce a structured literature analysis with gap identification and novelty assessment, sufficient for planning but not for gate approval.

**Output**: A literature analysis document covering:
- Structured search results organized by theme/approach
- Gap analysis identifying underexplored areas
- Novelty assessment: how the proposed work differs from existing approaches
- Citation info with verification grades for key papers

### Guidance

- Search across multiple databases with documented queries
- Apply inclusion/exclusion criteria (even if informal)
- Verify key citations via DOI/API checks
- Assess evidence hierarchy (Strong / Moderate / Limited / Insufficient)

---

## Mode 3: Systematic Survey

**Goal**: Produce a comprehensive, PRISMA-compliant literature review that passes Gate 1.

**Output**: A set of artifacts in `docs/survey/`:

| Artifact | Purpose |
|----------|---------|
| `survey-protocol.md` | Research question (PICO framework), search strategy, selection criteria |
| `search-log.md` | Exact queries, filters, result counts, timestamps per database |
| `screening-record.md` | Title/abstract screening decisions with rationale |
| `extraction-database.md` | Per-paper metadata, methodology, findings, limitations |
| `synthesis.md` | Thematic synthesis with evidence hierarchy |
| `citation-verification-report.md` | Verification grades for every citation |
| `research-readiness-report.md` | Final report with executive summary, PRISMA flow, landscape analysis, gaps, novelty assessment, visualizations |
| `figures/` | 1-2 visualizations (landscape map, citation network, PRISMA flow, or timeline) |

### Key Requirements

- Document inclusion/exclusion criteria explicitly
- Verify every citation (target 80%+ Grade A/B)
- Include 1-2 visualizations saved as PDF/PNG in `docs/survey/figures/`
- No fabricated references (zero tolerance)

---

## Academic API Reference

Use these APIs for all literature search and verification. Do NOT use web search for paper discovery.

| API | Use Case | Endpoint |
|-----|----------|----------|
| Semantic Scholar | AI/ML papers, citation graphs | `api.semanticscholar.org/graph/v1/paper/search` |
| arXiv | Preprints (CS, Physics, Math) | `export.arxiv.org/api/query` |
| DBLP | CS bibliography | `dblp.org/search/publ/api` |
| OpenAlex | Multi-disciplinary coverage | `api.openalex.org/works` |
| PubMed | Biomedical | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` |
| CrossRef | DOI verification | `api.crossref.org/works` |

See `references/database_search_strategies.md` for detailed API usage patterns.

## Citation Verification Grading

For the full verification methodology (sources, grades, workflow), see `references/citation-standards.md` (Citation Verification Methodology section).

| Grade | Meaning |
|-------|---------|
| A | DOI-verified via CrossRef |
| B | Confirmed via trusted source (Semantic Scholar, DBLP) |
| C | Preprint only (arXiv/bioRxiv, no formal publication) |
| D | Metadata found but could not fully verify |
| F | Fabrication risk -- not found in any database |

## Exception Handling

- **Insufficient literature**: If fewer than 10 relevant papers found, expand search terms, broaden date range, add related databases, and document the limitation
- **High fabrication risk**: Flag immediately, exclude from final report, report to researcher, search for verified alternatives
- **Vague research intent**: If clarity < 0.4 after 2 rounds, recommend `ideation` skill; do not proceed with systematic survey

## Key Rules

1. **Use academic database APIs, NOT web search** for paper discovery and verification
2. **Verify citations** in standard review and systematic survey modes
3. **Include visualizations** in systematic survey mode (1-2 per report)
4. **Document methodology** -- all search strategies and decisions must be recorded
5. **No fabricated references** -- zero tolerance
6. **Never skip intent clarification** if clarity score < 0.4
7. **Confirm before proceeding** -- get explicit researcher confirmation after clarification

## References

- `references/database_search_strategies.md` - Detailed API usage
- `references/citation-standards.md` - Citation grading criteria and verification standards
- `references/orchestrator-protocol.md` - Intent clarification details (Detailed Intent Clarification section)
