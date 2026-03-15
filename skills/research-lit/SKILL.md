---
name: autoresearch:research-lit
description: Literature survey using academic APIs (arXiv, Semantic Scholar, DBLP, OpenAlex). Use when user says "literature survey", "文献调研", "find related work", or needs to map the research landscape.
argument-hint: [research-topic]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent
agent: survey
---

## Purpose

Map the research landscape for a given topic using academic database APIs.

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