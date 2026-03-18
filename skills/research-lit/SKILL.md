---
name: airesearchorchestrator:research-lit
description: Quick literature landscape check using academic APIs. A lightweight alternative to literature-survey for rapid exploration. Use when user says "quick literature search", "check literature", "find papers", or needs fast paper discovery without full systematic review.
user-invocable: false
argument-hint: [research-topic]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent
---
## Purpose

Map the research landscape for a given topic using academic database APIs. This is a **lightweight, rapid** literature exploration skill.

## When to Use This Skill

**Use `research-lit` when:**
- You need a quick overview of the literature landscape
- Exploring a new research area informally
- Looking for recent papers on a topic
- Need to find 5-10 relevant papers quickly

**Use `literature-survey` instead when:**
- You need a systematic, comprehensive literature survey
- Preparing for a formal research project
- Gate 1 approval is required
- You need full verification reports and visualizations

| Aspect | `research-lit` (This Skill) | `literature-survey` |
|--------|----------------------------|---------------------|
| **Scope** | Quick exploration | Systematic review |
| **Output** | Working notes | Full survey report |
| **Verification** | Basic | Comprehensive (Grade A-F) |
| **Visualizations** | None | Mandatory |
| **Time** | Minutes | Hours to days |
| **Gate Ready** | No | Yes (Gate 1) |

## Workflow

### Step 1: Multi-source Search

Use these APIs (NOT web search):

| API | Use Case | Endpoint |
|-----|----------|----------|
| Semantic Scholar | AI/ML papers | `api.semanticscholar.org/graph/v1/paper/search` |
| arXiv | Preprints | `export.arxiv.org/api/query` |
| DBLP | CS bibliography | `dblp.org/search/publ/api` |
| OpenAlex | Comprehensive | `api.openalex.org/works` |

### Step 2: Build Landscape Map

Organize findings into:
- Sub-directions and approaches
- Key papers (seminal + recent)
- Open problems and gaps
- Recurring limitations

### Step 3: Output Summary

Save to working notes with:
- Citation info (title, authors, year, venue)
- One-sentence contribution
- Relevance to research direction

## Key Rules

- Use academic APIs, NOT web search
- Prefer papers from last 2-3 years
- Include seminal papers for context
- Note concurrent work (last 3-6 months)