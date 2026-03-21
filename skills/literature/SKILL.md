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

A unified literature skill that adapts its depth and approach based on context. Covers the full spectrum from quick landscape checks (minutes) to comprehensive systematic reviews (hours/days), and includes research intent clarification when the research question is unclear.

## Purpose

- Conduct literature exploration at the appropriate depth for the current need
- Clarify research intent when ideas are vague before committing to a full survey
- Map research landscapes using academic database APIs
- Verify all citations for authenticity
- Produce deliverables appropriate for quality gates

## Mode Selection

The agent decides which mode to use based on context:

| Mode | When to Use | Time | Gate Ready |
|------|-------------|------|------------|
| **Intent Clarification** | Research idea is vague (clarity < 0.4), before survey phase | 10-30 min | No |
| **Quick Exploration** | Need a fast overview, exploring a new area informally, finding 5-10 papers | Minutes | No |
| **Systematic Survey** | Formal research project, Gate 1 approval required, need full verification | Hours-Days | Yes |

---

## Mode 1: Intent Clarification

Use when the research idea is vague or underspecified. This mode clarifies the researcher's intent before any literature search begins.

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
- 0.0-0.3: Very vague, needs brainstorming (recommend invoking `ideation` skill)
- 0.3-0.4: Unclear, recommend brainstorming
- 0.4-0.6: Partially clear, run clarification loop
- 0.6-0.8: Mostly clear, minor clarifications needed
- 0.8-1.0: Clear, proceed to literature search

### First-Principles Question Bank

Select 2-3 questions per round from the weakest-scoring dimensions:

**Problem Dimension**:
- What specific problem are you trying to solve?
- Why is this problem important? What's the impact?
- What happens if this problem isn't solved?

**Solution Dimension**:
- What attempts have been made? Why aren't they good enough?
- What's your intuition about what might work?
- What constraints limit possible solutions?

**Contribution Dimension**:
- What type of contribution do you want to make? (Novel method / Theoretical analysis / Application / Benchmark / Survey)
- What would constitute a successful outcome?

**Context Dimension**:
- What's the target venue and timeline?
- What compute resources and data are available?

**Novelty Dimension**:
- What's your key insight or idea?
- Which assumptions in existing work can be challenged?

### Clarification Loop

- Maximum 5 rounds of questioning
- Target clarity score >= 0.7 before proceeding
- If score remains < 0.4 after 2 rounds, recommend invoking `ideation` skill for brainstorming
- Document all Q&A in `.autoresearch/research-intent-confirmation.md`
- Get explicit researcher confirmation before proceeding

---

## Mode 2: Quick Exploration

A lightweight, rapid literature search for informal landscape mapping.

### Workflow

#### Step 1: Multi-Source Search

Use these academic APIs (NOT web search):

| API | Use Case | Endpoint |
|-----|----------|----------|
| Semantic Scholar | AI/ML papers | `api.semanticscholar.org/graph/v1/paper/search` |
| arXiv | Preprints | `export.arxiv.org/api/query` |
| DBLP | CS bibliography | `dblp.org/search/publ/api` |
| OpenAlex | Comprehensive | `api.openalex.org/works` |

#### Step 2: Build Landscape Map

Organize findings into:
- Sub-directions and approaches
- Key papers (seminal + recent)
- Open problems and gaps
- Recurring limitations

#### Step 3: Output Summary

Save to working notes with:
- Citation info (title, authors, year, venue)
- One-sentence contribution per paper
- Relevance to research direction

### Quick Exploration Rules

- Use academic APIs, NOT web search
- Prefer papers from last 2-3 years
- Include seminal papers for context
- Note concurrent work (last 3-6 months)
- Target 5-10 relevant papers

---

## Mode 3: Systematic Survey (7-Phase Workflow)

A comprehensive, rigorous literature survey for formal research projects. Required for Gate 1 approval.

### Phase 1: Planning

Define the systematic survey protocol before any searching.

#### Research Question Definition

Frame using PICO or similar framework:

| Element | Description |
|---------|-------------|
| **P**opulation | What domain/field? |
| **I**ntervention | What method/approach? |
| **C**omparison | What alternatives? |
| **O**utcome | What metrics/results? |

#### Inclusion/Exclusion Criteria

Document explicit criteria:
- Published in peer-reviewed venues OR reputable preprint servers
- Published within last 3 years (except seminal works)
- Directly addresses the research question
- Empirical or theoretical contribution

#### Protocol Documentation

Create `docs/survey/survey-protocol.md` with research question, search strategy, selection criteria, quality assessment plan, and data extraction fields.

### Phase 2: Search

Execute systematic searches across multiple academic databases.

#### Database Selection

| Database | Best For | API Endpoint |
|----------|----------|--------------|
| Semantic Scholar | AI/ML, CS | `api.semanticscholar.org/graph/v1/paper/search` |
| arXiv | Preprints (CS, Physics, Math) | `export.arxiv.org/api/query` |
| DBLP | CS bibliography | `dblp.org/search/publ/api` |
| OpenAlex | Multi-disciplinary | `api.openalex.org/works` |
| PubMed | Biomedical | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` |
| CrossRef | DOI verification | `api.crossref.org/works` |

See `references/database_search_strategies.md` for detailed API usage.

#### Search Logging

Record all searches in `docs/survey/search-log.md` with exact queries, filters, result counts, and timestamps.

### Phase 3: Screening

Filter papers based on inclusion/exclusion criteria.

- Title/abstract screening with decision rationale
- Full-text review for papers passing initial screening
- PRISMA-style flow documentation
- Save screening record to `docs/survey/screening-record.md`

### Phase 4: Extraction

Extract key information from included papers systematically.

For each paper: metadata (title, authors, year, venue, DOI, verification grade), content (research question, methodology, key findings, limitations), and relevance assessment.

Save to `docs/survey/extraction-database.md`.

### Phase 5: Synthesis

Synthesize findings into coherent narrative.

- Organize by themes/approaches
- Apply evidence hierarchy (Strong / Moderate / Limited / Insufficient)
- Identify research gaps with supporting evidence
- Save to `docs/survey/synthesis.md`

### Phase 6: Citation Verification

Verify authenticity of every citation.

- DOI verification via CrossRef
- Source check via Semantic Scholar/DBLP
- Metadata cross-check (title, authors, year, venue)
- Grade assignment (A: DOI-verified, B: Trusted source, C: Preprint, D: Unverified, F: Fabrication risk)
- Save to `docs/survey/citation-verification-report.md`

### Phase 7: Document Generation

Generate final survey report with mandatory visualizations.

#### Report Structure

Create `docs/survey/research-readiness-report.md` with:
- Executive summary
- Search strategy and PRISMA flow
- Landscape analysis with mandatory visualizations (1-2)
- Key findings by theme
- Research gaps with evidence
- Novelty assessment
- References with verification grades

#### Mandatory Visualizations

Every systematic survey MUST include 1-2 AI-generated visualizations:
1. Research Landscape/Concept Map (themes and relationships)
2. Citation Relationship Diagram (paper influence network)
3. PRISMA Flow Diagram (screening process)
4. Timeline Visualization (research evolution)

Save as PDF or PNG in `docs/survey/figures/`.

#### Quality Checklist

- [ ] All 7 phases completed
- [ ] Every citation verified (80%+ Grade A/B)
- [ ] Mandatory visualizations included (1-2)
- [ ] Research gaps clearly identified
- [ ] Methodology fully documented
- [ ] No fabricated references

---

## Output Artifacts

### Intent Clarification Mode
- `.autoresearch/research-intent-confirmation.md`

### Quick Exploration Mode
- Working notes with landscape map

### Systematic Survey Mode

| Artifact | Location | Phase |
|----------|----------|-------|
| Survey Protocol | `docs/survey/survey-protocol.md` | 1 |
| Search Log | `docs/survey/search-log.md` | 2 |
| Screening Record | `docs/survey/screening-record.md` | 3 |
| Extraction Database | `docs/survey/extraction-database.md` | 4 |
| Synthesis | `docs/survey/synthesis.md` | 5 |
| Citation Verification | `docs/survey/citation-verification-report.md` | 6 |
| Final Report | `docs/survey/research-readiness-report.md` | 7 |
| Visualizations | `docs/survey/figures/` | 7 |

---

## Exception Handling

### Insufficient Literature
If search yields fewer than 10 relevant papers: expand search terms, expand date range, add related databases, document limitation in report.

### High Fabrication Risk
If citation verification reveals potential fabrications: flag immediately, do not include in final report, report to researcher, re-run search for verified alternatives.

### Vague Research Intent
If clarity score remains < 0.4 after 2 clarification rounds: recommend brainstorming via `ideation` skill, do not proceed with systematic survey until intent is clarified.

## Key Rules

1. **Use academic database APIs, NOT web search** (Semantic Scholar, arXiv, DBLP, OpenAlex, CrossRef)
2. **Every citation must be verified** in systematic survey mode
3. **Mandatory visualizations** in systematic survey mode (1-2 per report)
4. **Document methodology** -- all search strategies and decisions must be recorded
5. **No fabricated references** -- zero tolerance
6. **Never skip intent clarification** if clarity score < 0.4
7. **Max 5 clarification rounds** -- escalate if still unclear
8. **Confirm before proceeding** -- get explicit researcher confirmation after clarification

## References

- `references/database_search_strategies.md` - Detailed API usage
- `references/citation_standards.md` - Citation grading criteria
- `references/literature-verification.md` - Verification standards
- `references/intent-clarification-protocol.md` - Intent clarification details
