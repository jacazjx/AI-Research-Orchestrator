---
name: airesearchorchestrator:curate-citation
agent: writer
description: Finalize all citations with verification status and ensure authenticity. Use when user says "curate citations", "verify references", "整理引用", or needs to finalize paper citations.
argument-hint: [paper-directory]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Verify all paper citations are authentic, properly formatted, and complete the citation index.

## Workflow

### Step 1: Extract All Citations

Parse the paper:
- Find all \cite{} commands
- Extract references.bib entries
- Identify uncited references

### Step 2: Verify Each Citation

For each citation, verify using academic APIs:
- Semantic Scholar: `api.semanticscholar.org/graph/v1/paper/search`
- CrossRef: `api.crossref.org/works`
- arXiv: `export.arxiv.org/api/query`
- DBLP: `dblp.org/search/publ/api`

Check:
- Paper exists
- Authors are correct
- Year and venue are correct
- DOI is valid

### Step 3: Check Citation Quality

For each citation:
- Is the claim supported?
- Is the context appropriate?
- Is the citation necessary?

### Step 4: Format Consistency

Ensure:
- Consistent citation style
- Complete bibliographic information
- Proper DOI/URL formatting

### Step 5: Create Citation Index

Build index with verification status.

## Output

Save to `paper/citation-index.md`:

```markdown
# Citation Index

## Summary

- Total citations: X
- Verified: Y (Z%)
- Needs attention: N

## Citation Status

### Verified Citations

| Key | Title | Year | Venue | DOI | Verified By |
|-----|-------|------|-------|-----|-------------|
| author2023 | "Paper Title" | 2023 | NeurIPS | 10.xxxx | Semantic Scholar |

### Needs Verification

| Key | Issue | Action Needed |
|-----|-------|---------------|
| unknown2022 | Not found in databases | Verify source or remove |

### Potential Fabrication Flags

| Key | Issue | Severity |
|-----|-------|----------|
| ... | ... | HIGH/MEDIUM/LOW |

## Citation Quality Report

### Well-Supported Claims
- [Claim 1]: Cited by [author2023, other2022]
- [Claim 2]: Cited by [author2021]

### Claims Needing Support
- [Claim]: Currently uncited, suggest adding [author2020]

### Over-Cited Claims
- [Claim]: Multiple citations, consider consolidating

## Recommendations

1. [Recommendation for improving citation quality]
2. [Recommendation for missing citations]

## Verification Log

```
[2024-01-15 10:00] Verified author2023 via Semantic Scholar
[2024-01-15 10:01] Verified other2022 via CrossRef
...
```
```

## Key Rules

- EVERY citation must be verified via academic APIs
- Flag any potential fabrications as HIGH severity
- Use ONLY academic database APIs (NOT web search)
- Cross-check with multiple sources when possible