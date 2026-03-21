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

A unified citation management skill covering the full lifecycle: discovering gaps, searching for papers, verifying authenticity, ranking candidates, generating BibTeX, and producing a finalized citation index.

## Purpose

- Find and fill citation gaps in LaTeX manuscripts
- Verify all paper citations are authentic and properly attributed
- Rank candidate papers using a repeatable quality formula
- Generate BibTeX with explicit provenance fields
- Replace preprints with formally published versions
- Produce a finalized citation index with verification status

---

## Workflow

### 1. Detect Gaps

Scan documents for citation markers that indicate missing references:
- LaTeX markers: `[cite]`, `[citation needed]`, `\todo{cite}`
- Plain-language notes: "needs citation", "find reference for this"
- Chinese prompts: "需要引用", "找文献支持"
- Cross-reference `\cite{}` commands against `references.bib` entries to find uncited references and undefined keys

### 2. Generate Search Targets

For each citation gap:
- Reduce the paragraph to one verifiable statement
- Extract 3-8 search terms (task, method, population, metric, constraint)
- Generate English keywords even if the draft is in Chinese
- Note the type of evidence needed (benchmark result, survey, causal claim, system design, theory, dataset paper)

### 3. Search & Gather

Query academic APIs in priority order:

| Priority | Source | Use |
|----------|--------|-----|
| 1 | Existing project `.bib` files and verification ledger | Reuse already-verified citations |
| 2 | User-level persistent paper library | Cross-project reuse |
| 3 | Semantic Scholar, OpenAlex | Candidate discovery |
| 4 | CrossRef, DOI resolver | DOI confirmation |
| 5 | DBLP | CS bibliographic records |

**API endpoints**:

| API | Endpoint |
|-----|----------|
| Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/search` |
| CrossRef | `api.crossref.org/works` |
| arXiv | `export.arxiv.org/api/query` |
| DBLP | `dblp.org/search/publ/api` |
| OpenAlex | `api.openalex.org/works` |

For each candidate, collect: title, authors, year, venue, DOI, abstract, citation count, source URL.

**Preprint handling**: Treat arXiv/bioRxiv preprints as discovery hints. If a formally published version exists, cite that instead with its DOI. Keep preprints only when no formal version exists, and label them explicitly.

**Semantic Scholar API key**: Check `--semantic-scholar-api-key`, then `SEMANTIC_SCHOLAR_API_KEY` env var, then persisted local secret. Continue with free shared pool if no key is available. Never write API keys into repo files. Never block workflow solely because a key is missing.

### 4. Verify & Rank

For verification sources, grades, and workflow, see `references/citation-standards.md` (Citation Verification Methodology section).

**Verification** -- for each citation (existing and new):
- Existence: paper found in academic databases
- Metadata accuracy: authors, year, venue, title match
- DOI validity: DOI resolves correctly
- Content alignment: claim accurately reflects cited content
- Attribution: original sources cited (not just reviews)

**Verification by type**:

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

**Ranking** -- score candidates using the rubric from `references/quality-scoring.md`:
- Venue score (CCF A/B, JCR Q1/Q2, high impact factor preferred)
- Freshness score (last 5 years preferred)
- Citation count, impact factor, relevance, evidence type
- Publication bonus (peer-reviewed > preprint)
- Apply a minimum relevance gate. A lower-scoring paper that directly supports the claim can beat a higher-scoring but weakly related paper.

### 5. Output

**BibTeX with provenance fields** -- for each accepted citation:

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

**Citation index** -- save to `paper/citation-index.md` with:
- Summary: total citations, verified count/percentage, needs-attention count, fabrication flags
- Verified citations table (key, title, year, venue, DOI, verified-by, quality score)
- Needs-verification table (key, issue, action needed)
- Fabrication flags table (key, issue, severity) -- HIGH PRIORITY
- Claim-citation mapping (well-supported claims and claims needing support)
- Timestamped verification log

**Sync and persist**: After every run, sync accepted citations into `.citation-curator/verification-ledger.json` and the user-level paper library. If a target `.bib` file was provided, sync the ledger with it. Keep user-edited BibTeX entries intact.

---

## Helper Scripts

See `scripts/` for implementation utilities:

| Script | Purpose |
|--------|---------|
| `scripts/extract_citation_needs.py` | Find citation gaps in `.tex` files |
| `scripts/score_papers.py` | Rank candidates by quality score |
| `scripts/fetch_verified_bibtex.py` | End-to-end verified citation workflow |

## Exception Handling

- **Older papers**: Allow when seminal, standards-defining, or required for classic methods. Label as `seminal exception`.
- **Non-CCF/JCR venues**: Allow for interdisciplinary fields when the paper is otherwise strongly supported.
- **Preprint-only**: If user explicitly allows and no formal version exists, keep outside the final verified bibliography or label as `fallback preprint`.
- **Rate limits**: Use long backoff for shared Semantic Scholar pool. Do not surface failed intermediate attempts in user-facing output.

## Key Rules

1. **Do not invent papers, DOIs, venues, citation counts, or impact factors**
2. **Use ONLY academic database APIs** (not web search) for verification
3. **Every citation should be verified** -- flag any potential fabrications as CRITICAL
4. **Do not keep preprints** when a verified formal publication exists
5. **Do not claim authenticated verification** when no valid API key was used
6. **Do not overwrite user-authored `.bib` entries** -- store extra state in the ledger
7. **Do not guess CCF tier or JCR quartile** -- mark as unknown when unverifiable
8. **Surface disagreements** between DBLP, Crossref, Semantic Scholar, and publisher pages
9. **Cross-verify** with multiple sources when possible

## References

- `references/quality-scoring.md` - Scoring formula and tie-break rules
- `references/source-verification.md` - DOI checks, preprint replacement, BibTeX provenance
- `references/citation-standards.md` - Citation grading criteria and paper phase citation rules
