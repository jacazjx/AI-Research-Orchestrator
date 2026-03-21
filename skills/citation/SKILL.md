---
name: airesearchorchestrator:citation
agent: writer
description: Unified citation skill covering discovery, verification, ranking, BibTeX generation, and finalization. Finds citation gaps in LaTeX drafts, retrieves real candidate papers, verifies via academic APIs, ranks with a quality formula, and produces provenance-aware BibTeX. Use when user says "curate citations", "verify references", "find citations", "整理引用", "验证引用", or needs citation management for paper writing.
user-invocable: false
argument-hint: [paper-directory-or-tex-file]
allowed-tools: Bash(curl, python), Read, Write, Edit, Grep, Glob, WebFetch
---
# Citation

## Overview

A unified citation management skill that covers the full lifecycle: discovering citation gaps, searching for supporting papers, verifying authenticity via academic APIs, ranking candidates by quality, generating DOI-verified BibTeX, and finalizing the citation index.

## Purpose

- Find and fill citation gaps in LaTeX manuscripts
- Verify all paper citations are authentic and properly attributed
- Rank candidate papers using a repeatable quality formula
- Generate BibTeX with explicit provenance fields
- Replace preprints with formally published versions
- Produce a finalized citation index with verification status

---

## Workflow

### Step 1: Locate Citation Gaps

Inspect the draft for markers:
- `[cite]`, `[citation needed]`, `\todo{cite}`
- Plain-language notes: "needs citation", "find reference for this"
- Chinese prompts: "我想找一篇论文来支撑论点", "需要引用", "找文献支持"

Use `scripts/extract_citation_needs.py` when a local `.tex` file is available:
```bash
python3 scripts/extract_citation_needs.py draft.tex --json
```

### Step 2: Extract and Cross-Reference Existing Citations

Parse the paper:
- Find all `\cite{}` commands
- Extract all `references.bib` entries
- Cross-reference used vs. defined citations
- Identify uncited references

### Step 3: Rewrite Gaps into Search Targets

For each citation gap:
- Reduce the paragraph to one verifiable statement
- Extract 3-8 search terms (task, method, population, metric, constraint)
- Generate English keywords even if the draft is in Chinese
- Note what kind of evidence is needed (benchmark result, survey, causal claim, system design, theory, dataset paper)

### Step 4: Gather Real Candidates from Academic Sources

**Source priority order**:
1. Existing project `.bib` files and project-local verification ledger
2. User-level persistent paper library (cache directory)
3. Semantic Scholar API and OpenAlex for candidate discovery
4. Crossref and DOI resolver for final DOI confirmation
5. DBLP for computer-science bibliographic records
6. Google Scholar only as a manual hint fallback (not for automated metadata)

**For each candidate, collect**: title, authors, year, venue, DOI, abstract, citation count, source URL, BibTeX source URL.

**API endpoints**:
| API | Endpoint |
|-----|----------|
| Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/search` |
| CrossRef | `api.crossref.org/works` |
| arXiv | `export.arxiv.org/api/query` |
| DBLP | `dblp.org/search/publ/api` |
| OpenAlex | `api.openalex.org/works` |

**Semantic Scholar API key handling**:
- Check `--semantic-scholar-api-key`, then `SEMANTIC_SCHOLAR_API_KEY` env var, then persisted local secret
- If user has a key: use authenticated mode, persist after first successful run
- If user lacks a key: continue with free shared pool, use long backoff for rate limits
- Never write API keys into repo, `.tex`, `.bib`, or report files
- Never block workflow solely because user lacks a key

### Step 5: Replace Preprints with Published Versions

Treat arXiv or other preprints as discovery hints, not final citations:
- If a preprint has a formally published version: cite the formal version with its DOI
- If the formal version has no DOI: fetch BibTeX from DBLP and mark for manual second checking
- If no formal version exists: say so explicitly
- Keep preprints only as search breadcrumbs, not in the final bibliography

### Step 6: Rank Candidates

Use the scoring rubric from `references/quality-scoring.md`:

**Scoring dimensions**:
- Venue score (CCF A/B, JCR Q1/Q2, high impact factor preferred)
- Freshness score (last 5 years preferred)
- Citation count score
- Impact factor score
- Relevance score
- Evidence score
- Publication bonus (peer-reviewed > preprint)

Apply a minimum relevance gate before delivery. A lower-scoring paper that directly supports the claim can beat a higher-scoring but weakly related paper.

Use `scripts/score_papers.py` for consistent ranking:
```bash
python3 scripts/score_papers.py candidates.json --format tsv
```

### Step 7: Verify Each Citation

For each citation (existing and new):
- **Existence**: Paper exists in academic databases
- **Metadata accuracy**: Authors, year, venue, title match
- **DOI validity**: DOI resolves correctly
- **Content alignment**: Claim accurately reflects cited content
- **Attribution**: Original sources cited (not just reviews), primary sources for methods

**Verification standards by citation type**:

| Citation Type | Required Verification |
|---------------|----------------------|
| Journal article | DOI verification via CrossRef |
| arXiv preprint | arXiv ID verification |
| Conference paper | DBLP/Semantic Scholar verification |
| Book | ISBN verification |
| Website | URL accessibility check |

**Severity levels**:

| Issue | Severity |
|-------|----------|
| Fabricated citation (not in any database) | CRITICAL |
| Wrong claims attributed to source | HIGH |
| Retracted source cited | HIGH |
| Preprint without version number | MEDIUM |
| Incomplete bibliographic info | LOW |

### Step 8: Generate Verified BibTeX

For each accepted citation, produce BibTeX with provenance fields:

```bibtex
@article{author2024method,
  title     = {Exact Title},
  author    = {Last, First and Last, First},
  year      = {2024},
  journal   = {Venue Name},
  doi       = {10.xxxx/yyyy},
  url       = {https://doi.org/10.xxxx/yyyy},
  x-bib-source       = {crossref},
  x-bib-source-url   = {https://api.crossref.org/works/10.xxxx/yyyy},
  x-verified-with    = {semantic-scholar, crossref},
  x-verified-at      = {2026-03-21},
  x-quality-score    = {85},
  x-verification-status = {verified},
}
```

Do not fabricate missing BibTeX fields. If the source record is incomplete, note what is missing.

### Step 9: Check Citation Quality and Context

For each citation:
- Is the claim supported by the cited paper?
- Is the context appropriate?
- Is the citation necessary (avoid padding)?
- Is the attribution to the original source (not a secondary review)?

### Step 10: Produce Citation Index

Save finalized index to `paper/citation-index.md`:

```markdown
# Citation Index

## Summary
- Total citations: X
- Verified: Y (Z%)
- Needs attention: N
- Fabrication flags: M

## Verified Citations

| Key | Title | Year | Venue | DOI | Verified By | Quality Score |
|-----|-------|------|-------|-----|-------------|---------------|
| author2024 | "Title" | 2024 | NeurIPS | 10.xxx | Semantic Scholar, CrossRef | 85 |

## Needs Verification

| Key | Issue | Action Needed |
|-----|-------|---------------|
| unknown2022 | Not found in databases | Verify source or remove |

## Fabrication Flags (HIGH PRIORITY)

| Key | Issue | Severity |
|-----|-------|----------|
| suspicious2021 | Not in any database | CRITICAL |

## Citation Quality Report

### Well-Supported Claims
- [Claim]: Cited by [key1, key2]

### Claims Needing Support
- [Claim]: Currently uncited, suggest adding [author2020]

## Verification Log
[Timestamped log of all verification actions]
```

### Step 11: Sync and Persist

After every run:
- Sync accepted citations into `.citation-curator/verification-ledger.json`
- Sync into user-level paper library for cross-project reuse
- If a target `.bib` file was provided, sync the ledger with that file
- Keep user-edited BibTeX entries intact; store extra verification state in the ledger

---

## Local Helper Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/extract_citation_needs.py` | Find citation gaps in `.tex` files | `python3 scripts/extract_citation_needs.py draft.tex --json` |
| `scripts/score_papers.py` | Rank candidates by quality | `python3 scripts/score_papers.py candidates.json --format tsv` |
| `scripts/fetch_verified_bibtex.py` | End-to-end verified citation workflow | See below |

### fetch_verified_bibtex.py Usage

```bash
# Basic usage
python3 scripts/fetch_verified_bibtex.py \
  --query "claim to support" \
  --existing-bib refs.bib \
  --write-json report.json \
  --write-bib verified.bib

# Batch mode from extracted claims
python3 scripts/extract_citation_needs.py draft.tex --json > claims.json
python3 scripts/fetch_verified_bibtex.py \
  --claims-json claims.json \
  --existing-bib refs.bib \
  --no-key-prompt \
  --append-bib refs.bib
```

---

## Exception Handling

- **Older papers**: Allow when seminal, standards-defining, or required for classic methods. Label as `seminal exception`.
- **Non-CCF/JCR venues**: Allow for interdisciplinary fields when the paper is otherwise strongly supported.
- **Preprint-only**: If user explicitly allows and no formal version exists, keep outside the final verified bibliography or label as `fallback preprint`.
- **Rate limits**: Use long backoff for shared Semantic Scholar pool. Do not surface failed intermediate attempts in user-facing output.

## Key Rules

1. **Do not invent papers, DOIs, venues, citation counts, or impact factors**
2. **Use ONLY academic database APIs** (NOT web search) for verification
3. **Every citation must be verified** -- flag any potential fabrications as CRITICAL
4. **Do not keep preprints** when a verified formal publication exists
5. **Do not claim authenticated verification** when no valid API key was used
6. **Do not overwrite user-authored `.bib` entries** -- store extra state in the ledger
7. **Do not guess CCF tier or JCR quartile** -- mark as unknown when unverifiable
8. **Surface disagreements** between DBLP, Crossref, Semantic Scholar, and publisher pages
9. **Cross-verify** with multiple sources when possible

## References

- `references/quality-scoring.md` - Scoring formula and tie-break rules
- `references/source-verification.md` - DOI checks, preprint replacement, BibTeX provenance
- `references/citation-standards.md` - Paper phase citation rules
- `references/citation-standards.md` - Citation grading criteria
