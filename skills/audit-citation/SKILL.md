---
name: autoresearch:audit-citation
agent: reviewer
description: Audit citation authenticity with detailed verification of each reference. Use when user says "audit citations", "verify citations", "验证引用", or needs deep citation verification.
argument-hint: [paper-directory]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Deep verification of all citations for authenticity and proper attribution.

## Workflow

### Step 1: Extract All Citations

Parse:
- All \cite{} commands in paper
- All entries in references.bib
- Cross-reference used vs defined

### Step 2: Verify Each Citation

For each citation, check via academic APIs:
- Paper exists (Semantic Scholar, arXiv, CrossRef)
- Authors are correct
- Year and venue match
- DOI/URL is valid
- Title matches

### Step 3: Assess Citation Quality

Evaluate:
- Is citation appropriate for context?
- Is claim accurately attributed?
- Is citation necessary?

### Step 4: Check for Fabrication

Flag:
- Papers not found in any database
- Mismatched details (author, year, venue)
- Suspicious DOI patterns

### Step 5: Verify Attribution

Ensure:
- Original sources cited (not just reviews)
- Primary sources for methods
- Appropriate credit given

## Output

```markdown
# Citation Audit Report

## Summary
- **Total Citations**: X
- **Verified**: Y (Z%)
- **Potential Fabrications**: N
- **Attribution Issues**: M

## Verification Details

### Verified Citations

| Key | Title | Authors | Year | Venue | DOI | Verified Via |
|-----|-------|---------|------|-------|-----|--------------|
| author2023 | [Title] | [Names] | 2023 | NeurIPS | 10.xxx | Semantic Scholar |

### Needs Verification

| Key | Title | Issue | Action |
|-----|-------|-------|--------|
| unknown2022 | [Title] | Not found | Verify source or remove |

### Potential Fabrications (HIGH PRIORITY)

| Key | Title | Issue | Severity |
|-----|-------|-------|----------|
| suspicious2021 | [Title] | Not in any database | HIGH |

### Attribution Issues

| Citation | Issue | Recommendation |
|----------|-------|----------------|
| [Key] | Secondary source cited | Cite original: [Original paper] |

## Verification by Source

| API | Citations Found | Coverage |
|-----|-----------------|----------|
| Semantic Scholar | X | Y% |
| arXiv | X | Y% |
| CrossRef | X | Y% |
| DBLP | X | Y% |
| Not Found | X | Y% |

## Context Appropriateness

| Citation | Context | Appropriate? | Notes |
|----------|---------|--------------|-------|
| [Key] | [Context] | Yes/No | |

## Recommendations

1. [Action for each fabrication]
2. [Action for each attribution issue]

## Gate Decision

- [ ] PASS - All citations verified, no fabrications
- [ ] PASS_WITH_FIXES - Minor issues, fix and proceed
- [ ] REVISE - Citation issues need addressing
- [ ] BLOCK - Fabrications detected, must resolve

## Verification Log

```
[Date Time] Verified author2023 via Semantic Scholar (DOI: 10.xxx)
[Date Time] WARNING: unknown2022 not found in any database
...
```
```

## Key Rules

- Must verify EVERY citation via academic APIs
- Any potential fabrication is HIGH severity
- Use ONLY academic APIs (NOT web search)
- Cross-verify with multiple sources when possible
- Attribution must go to original sources