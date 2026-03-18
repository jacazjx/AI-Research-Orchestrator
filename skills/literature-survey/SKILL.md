---
name: airesearchorchestrator:literature-survey
description: Systematic literature survey following 7-phase workflow (Planning, Search, Screening, Extraction, Synthesis, Citation Verification, Document Generation). Creates comprehensive research landscape maps with AI-generated visualizations. Use when user says "literature survey", "文献调研", "systematic review", "find related work", or needs comprehensive research landscape mapping.
argument-hint: [research-topic-or-question]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent
---

# Literature Survey

## Overview

A systematic, rigorous literature survey skill that follows a 7-phase workflow to comprehensively map the research landscape. This skill emphasizes citation authenticity, AI-generated visualizations, and reproducible methodology.

## Purpose

Conduct systematic literature surveys that:
- Define clear research questions and inclusion/exclusion criteria
- Search multiple academic databases comprehensively
- Screen and extract key information systematically
- Synthesize findings with proper evidence hierarchy
- Verify all citations for authenticity
- Generate reports with mandatory AI-generated visualizations

## Key Rules

1. **Use academic database APIs, NOT web search** - See [references/database_search_strategies.md](references/database_search_strategies.md)
2. **Every citation must be verified** - See [references/citation_standards.md](references/citation_standards.md)
3. **Mandatory AI-generated visualizations** - Every survey report must include 1-2 visualizations
4. **Document methodology** - All search strategies and decisions must be recorded
5. **No fabricated references** - Zero tolerance for invented citations

---

## Workflow

### Phase 1: Planning

Define the systematic survey protocol before any searching begins.

#### 1.1 Research Question Definition

Frame the research question using PICO or similar framework:

| Element | Description | Example |
|---------|-------------|---------|
| **P**opulation | What domain/field? | Machine learning for code generation |
| **I**ntervention | What method/approach? | Large language models |
| **C**omparison | What alternatives? | Traditional NLP methods, rule-based systems |
| **O**utcome | What metrics/results? | Code quality, correctness, efficiency |

#### 1.2 Inclusion/Exclusion Criteria

Document explicit criteria:

```markdown
## Inclusion Criteria
- [ ] Published in peer-reviewed venues OR reputable preprint servers
- [ ] Published within last 3 years (except seminal works)
- [ ] Directly addresses the research question
- [ ] Empirical or theoretical contribution

## Exclusion Criteria
- [ ] Non-academic sources (blogs, news articles)
- [ ] Papers without methodology details
- [ ] Duplicate publications
- [ ] Non-English papers (unless seminal)
```

#### 1.3 Protocol Documentation

Create survey protocol at `docs/reports/survey/survey-protocol.md`:

```markdown
# Survey Protocol

## Research Question
[Primary research question]

## Search Strategy
- Databases: [list]
- Date range: [start] to [end]
- Language: English
- Search terms: [primary terms and variations]

## Selection Criteria
### Inclusion
- [List inclusion criteria]

### Exclusion
- [List exclusion criteria]

## Quality Assessment
- Citation verification standards
- Source quality grading

## Data Extraction
- [Fields to extract from each paper]
```

**Deliverable:** `docs/reports/survey/survey-protocol.md`

---

### Phase 2: Search

Execute systematic searches across multiple academic databases.

#### 2.1 Database Selection

Select databases based on research domain:

| Database | Best For | API Endpoint |
|----------|----------|--------------|
| **Semantic Scholar** | AI/ML, Computer Science | `api.semanticscholar.org/graph/v1/paper/search` |
| **arXiv** | Preprints (CS, Physics, Math, Stats) | `export.arxiv.org/api/query` |
| **DBLP** | Computer Science bibliography | `dblp.org/search/publ/api` |
| **OpenAlex** | Comprehensive multi-disciplinary | `api.openalex.org/works` |
| **PubMed** | Biomedical, Life Sciences | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` |
| **CrossRef** | DOI verification, cross-disciplinary | `api.crossref.org/works` |

See [references/database_search_strategies.md](references/database_search_strategies.md) for detailed API usage.

#### 2.2 Search Execution

For each database:

```bash
# Semantic Scholar example
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=YOUR_QUERY&limit=50&year=2023-2026&fields=title,authors,year,venue,citationCount,abstract"

# arXiv example
curl "https://export.arxiv.org/api/query?search_query=all:YOUR_QUERY&start=0&max_results=50"

# OpenAlex example
curl "https://api.openalex.org/works?search=YOUR_QUERY&filter=publication_year:2023-2026&per_page=50"

# DBLP example
curl "https://dblp.org/search/publ/api?q=YOUR_QUERY&format=json&h=50"
```

#### 2.3 Search Logging

Record all searches in `docs/reports/survey/search-log.md`:

```markdown
# Search Log

## Search Session: [Date]

### Semantic Scholar
- Query: `[exact query string]`
- Filters: `year=2023-2026, venue=...`
- Results: [count]
- Timestamp: [ISO 8601]

### arXiv
- Query: `[exact query string]`
- Categories: `[cs.LG, cs.CL, ...]`
- Results: [count]
- Timestamp: [ISO 8601]

[Repeat for each database]

## Deduplication
- Total unique papers: [count]
- Duplicates removed: [count]
```

**Deliverable:** `docs/reports/survey/search-log.md` with raw results

---

### Phase 3: Screening

Filter papers based on inclusion/exclusion criteria.

#### 3.1 Title/Abstract Screening

Screen based on titles and abstracts:

1. Read title and abstract of each paper
2. Apply inclusion/exclusion criteria
3. Record decision with rationale

Create screening record at `docs/reports/survey/screening-record.md`:

```markdown
# Screening Record

## Summary
- Papers identified: [N]
- Duplicates removed: [N]
- Title/abstract screened: [N]
- Full-text assessed: [N]
- Final included: [N]

## Decision Log

| Paper ID | Title | Decision | Rationale |
|----------|-------|----------|-----------|
| S2-12345 | [Title] | INCLUDE | Directly addresses RQ1 |
| arXiv-2401 | [Title] | EXCLUDE | Not peer-reviewed, lacks methodology |
| DBLP-67890 | [Title] | UNDECIDED | Need full-text review |

## PRISMA Flow
[Include PRISMA-style flow diagram]
```

#### 3.2 Full-Text Review

For papers passing initial screening:

1. Retrieve full text
2. Assess against all criteria
3. Record detailed exclusion reasons

**Deliverable:** `docs/reports/survey/screening-record.md`

---

### Phase 4: Extraction

Extract key information from included papers systematically.

#### 4.1 Extraction Template

For each included paper, extract:

```markdown
## Paper: [Citation Key]

### Metadata
- **Title**: [Full title]
- **Authors**: [First author et al.]
- **Year**: [Publication year]
- **Venue**: [Conference/Journal]
- **DOI**: [DOI if available]
- **Source**: [Database where found]
- **Verification Status**: [A/B/C/D/F grade]

### Content
- **Research Question**: [What did they investigate?]
- **Methodology**: [What approach did they use?]
- **Key Findings**: [Main results]
- **Limitations**: [Acknowledged limitations]
- **Future Work**: [Suggested directions]

### Relevance
- **Addresses RQ**: [Which research question(s)]
- **Contribution Type**: [methodology/empirical/theoretical/survey]
- **Key Insight**: [One-sentence key contribution]
```

#### 4.2 Extraction Database

Compile extractions into `docs/reports/survey/extraction-database.md`:

| Field | Description |
|-------|-------------|
| Citation Key | Unique identifier |
| Authors | Author list |
| Year | Publication year |
| Venue | Publication venue |
| DOI | Verified DOI |
| Methodology | Approach used |
| Key Findings | Main results |
| Relevance Score | 1-10 relevance to RQ |
| Verification Grade | A-F citation grade |

**Deliverable:** `docs/reports/survey/extraction-database.md`

---

### Phase 5: Synthesis

Synthesize findings into coherent narrative.

#### 5.1 Thematic Organization

Organize papers by themes/approaches:

```markdown
# Synthesis

## Theme 1: [Approach Category A]

### Overview
[Brief description of this approach category]

### Key Papers
1. **[Author Year]**: [Key contribution]
2. **[Author Year]**: [Key contribution]

### Common Findings
- [Finding 1]
- [Finding 2]

### Limitations
- [Limitation 1]
- [Limitation 2]

## Theme 2: [Approach Category B]
[Repeat structure]

## Research Gaps Identified
1. [Gap 1 with supporting evidence]
2. [Gap 2 with supporting evidence]

## Open Problems
1. [Problem 1]
2. [Problem 2]
```

#### 5.2 Evidence Hierarchy

Rate evidence strength:

| Level | Description |
|-------|-------------|
| **Strong** | Multiple studies with consistent results, high-quality venues |
| **Moderate** | Some studies with generally consistent results |
| **Limited** | Few studies, inconsistent results, or low-quality venues |
| **Insufficient** | Not enough evidence to draw conclusions |

**Deliverable:** `docs/reports/survey/synthesis.md`

---

### Phase 6: Citation Verification

Verify authenticity of every citation.

#### 6.1 Verification Process

For each citation, perform:

1. **DOI Verification**: Resolve DOI via CrossRef
2. **Source Check**: Verify via Semantic Scholar/DBLP
3. **Metadata Cross-check**: Confirm title, authors, year, venue
4. **Grade Assignment**: Assign A-F grade

See [references/citation_standards.md](references/citation_standards.md) for grading criteria.

#### 6.2 Verification Report

Create `docs/reports/survey/citation-verification-report.md`:

```markdown
# Citation Verification Report

## Summary
- Total citations: [N]
- Grade A (DOI-verified): [N] ([%])
- Grade B (Trusted source): [N] ([%])
- Grade C (Preprint): [N] ([%])
- Grade D (Unverified): [N] ([%])
- Grade F (Fabrication risk): [N] ([%])

## Verification Details

| Citation | DOI | Source | Grade | Notes |
|----------|-----|--------|-------|-------|
| author2024 | 10.xxxx/xxx | Semantic Scholar | A | Verified |
| author2023 | arXiv:2301.xxxxx | arXiv | C | Preprint, check for published version |

## Fabrication Risk Assessment
- **Overall Risk**: LOW / MEDIUM / HIGH
- **Flagged Citations**: [List any suspicious citations]

## Recommendations
- [Any citations needing manual verification]
```

**Deliverable:** `docs/reports/survey/citation-verification-report.md`

---

### Phase 7: Document Generation

Generate final survey report with mandatory visualizations.

#### 7.1 Report Structure

Create `docs/reports/survey/research-readiness-report.md`:

```markdown
# Literature Survey Report

## Executive Summary
[2-3 paragraph overview of findings]

## 1. Introduction
- Research question
- Scope and methodology
- Protocol summary

## 2. Search Strategy
- Databases searched
- Search terms and queries
- Results overview (PRISMA flow)

## 3. Landscape Analysis
### 3.1 Research Landscape Visualization
[MANDATORY: Include research landscape/concept map]

### 3.2 Key Themes
[Thematic synthesis from Phase 5]

### 3.3 Citation Network
[MANDATORY: Include citation relationship diagram]

## 4. Key Findings
[Synthesized findings organized by theme]

## 5. Research Gaps
[Identified gaps with supporting evidence]

## 6. Novelty Assessment
[How proposed research addresses gaps]

## 7. Conclusion
[Summary and next steps]

## References
[Complete reference list with verification grades]

## Appendix
- Search log
- Screening record
- Extraction database
```

#### 7.2 Mandatory Visualizations

**Every survey report MUST include 1-2 AI-generated visualizations:**

##### Visualization Types

1. **Research Landscape/Concept Map**
   - Shows research themes and their relationships
   - Nodes = research topics/approaches
   - Edges = relationships (extends, contrasts, combines)

2. **Citation Relationship Diagram**
   - Shows how key papers relate to each other
   - Temporal flow or influence network
   - Grouped by approach/theme

3. **PRISMA Flow Diagram**
   - Shows screening process
   - Papers identified → screened → included

4. **Timeline Visualization**
   - Shows evolution of research over time
   - Key papers marked at their publication date

##### Generation Process

Use AI image generation or create visualizations programmatically:

```bash
# Option 1: Generate via Agent
# Describe the visualization to an AI agent for generation

# Option 2: Create using Python
# Use matplotlib, graphviz, or similar for structured diagrams
```

##### Visualization Requirements

- Clear labeling and legend
- Professional appearance suitable for academic reports
- Include source data/methodology notes
- Save as PDF or PNG in `docs/reports/survey/figures/`

#### 7.3 Quality Checklist

Before finalizing report:

- [ ] All 7 phases completed
- [ ] Every citation verified (80%+ Grade A/B)
- [ ] Mandatory visualizations included (1-2)
- [ ] Research gaps clearly identified
- [ ] Methodology fully documented
- [ ] No fabricated references

**Deliverable:** `docs/reports/survey/research-readiness-report.md` with visualizations

---

## Output Artifacts

| Artifact | Location | Phase |
|----------|----------|-------|
| Survey Protocol | `docs/reports/survey/survey-protocol.md` | Phase 1 |
| Search Log | `docs/reports/survey/search-log.md` | Phase 2 |
| Screening Record | `docs/reports/survey/screening-record.md` | Phase 3 |
| Extraction Database | `docs/reports/survey/extraction-database.md` | Phase 4 |
| Synthesis | `docs/reports/survey/synthesis.md` | Phase 5 |
| Citation Verification | `docs/reports/survey/citation-verification-report.md` | Phase 6 |
| Final Report | `docs/reports/survey/research-readiness-report.md` | Phase 7 |
| Visualizations | `docs/reports/survey/figures/` | Phase 7 |

---

## Integration with Other Skills

- **audit-survey**: Reviews this survey for completeness and citation authenticity
- **latex-citation-curator**: Provides verified BibTeX for paper writing phase
- **research-lit**: Lighter-weight literature search for quick landscape checks
- **novelty-check**: Uses survey findings to assess novelty claims

---

## Exception Handling

### Insufficient Literature

If search yields fewer than 10 relevant papers:
1. Expand search terms
2. Expand date range
3. Add related databases
4. Document limitation in report

### High Fabrication Risk

If citation verification reveals potential fabrications:
1. Flag immediately
2. Do not include in final report
3. Report to researcher
4. Re-run search for verified alternatives

### Visualization Failure

If AI visualization generation fails:
1. Use programmatic generation (matplotlib, graphviz)
2. Create simple text-based diagrams
3. Document limitation
4. Must still include at least 1 visualization

---

## References

- [Database Search Strategies](references/database_search_strategies.md)
- [Citation Standards](references/citation_standards.md)