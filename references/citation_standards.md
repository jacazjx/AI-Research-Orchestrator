# Citation Standards

This document defines the standards and procedures for verifying citation authenticity in research projects. Every citation must be verified before inclusion in any deliverable.

## Citation Quality Grades

| Grade | Criteria | Verification Method | Acceptable For |
|-------|----------|---------------------|----------------|
| **A** | DOI-verified, peer-reviewed publication | DOI resolution via CrossRef | Primary evidence, novelty claims |
| **B** | Trusted source (DBLP, Semantic Scholar, publisher) | Source database lookup | Supporting evidence, methodology |
| **C** | arXiv or reputable preprint server | URL/ID verification | Emerging work, technical details |
| **D** | Unverified source, needs manual check | Requires human review | Context only, not for claims |
| **F** | Cannot locate or verify | Must be removed or flagged | None - must be excluded |

---

## Verification Requirements

### Minimum Standards for Gate 1 Approval

For Survey phase approval, the citation portfolio must satisfy:

| Requirement | Threshold |
|-------------|-----------|
| Grade A or B citations | ≥ 80% of total |
| Grade F citations | 0 (or explicit justification) |
| Grade D citations | All have manual verification plan |
| Novelty claims | Supported by ≥ 1 Grade A or B citation |

### Phase-Specific Requirements

| Phase | Requirement | Rationale |
|-------|-------------|-----------|
| Survey | 80%+ Grade A/B | Ensures solid foundation |
| Pilot | All cited baselines verified | Fair comparison |
| Experiments | All method references verified | Reproducibility |
| Paper | 90%+ Grade A/B | Publication standards |

---

## Verification Methods

### 1. DOI Verification (Grade A)

```bash
# Check DOI validity
curl -I "https://doi.org/10.48550/arXiv.1706.03762"

# Get metadata via CrossRef
curl "https://api.crossref.org/works/10.48550/arXiv.1706.03762"
```

**Verification Steps:**
1. Extract DOI from citation
2. Resolve via `https://doi.org/[DOI]`
3. Verify title, authors, year match
4. Record resolution status

**Valid Response:** HTTP 302 redirect to publisher URL

### 2. Trusted Source Verification (Grade B)

**Semantic Scholar:**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=PAPER_TITLE&fields=title,authors,year,venue"
```

**DBLP:**
```bash
curl "https://dblp.org/search/publ/api?q=PAPER_TITLE&format=json"
```

**Publisher Databases:**
| Publisher | Search URL |
|-----------|------------|
| ACM DL | `https://dl.acm.org/doSearch?query=[title]` |
| IEEE Xplore | `https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=[title]` |
| Springer | `https://link.springer.com/search?query=[title]` |
| Elsevier | `https://www.sciencedirect.com/search?qs=[title]` |

### 3. arXiv Verification (Grade C)

```bash
# Verify arXiv ID
curl "https://export.arxiv.org/api/query?id_list=2301.07094"

# Check for published version
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=PAPER_TITLE&fields=externalIds,venue"
```

**Verification Steps:**
1. Extract arXiv ID (format: `YYMM.NNNNN` or `arch-ive/YYMMNNN`)
2. Resolve via `https://arxiv.org/abs/[ID]`
3. Check if published version exists (upgrade to Grade A if found)
4. Recommend formal publication citation if available

---

## Citation Metadata Requirements

### Required Fields

Every citation must include:

| Field | Requirement | Example |
|-------|-------------|---------|
| **Title** | Exact title from publication | "Attention Is All You Need" |
| **Authors** | At least first author full name | "Vaswani, Ashish et al." |
| **Year** | Publication year | 2017 |
| **Venue** | Conference, journal, or repository | "NeurIPS" or "arXiv" |

### Recommended Fields

| Field | Purpose |
|-------|---------|
| **DOI** | Permanent identifier |
| **URL** | Direct link to paper |
| **Pages** | Page range for journals/conferences |
| **Volume/Number** | For journals |
| **Publisher** | For books |

### Quality Enhancement Fields

| Field | Purpose |
|-------|---------|
| **Access Date** | When citation was verified |
| **Verification Status** | Grade (A-F) |
| **Verification Source** | Database used for verification |
| **Published Version** | Link to formal publication if citing preprint |

---

## Novelty Claim Verification

### Required Evidence for Novelty Claims

When claiming novelty, provide:

#### 1. Direct Prior Art Search

- Search results for key terms across databases
- Papers with similar titles/abstracts
- Related work sections in similar papers

#### 2. Differentiation Evidence

- Specific differences with closest prior work
- Technical novelty (not just application novelty)
- Theoretical novelty (if applicable)

#### 3. Coverage Analysis

- Survey papers in the area
- Recent workshops/tutorials
- Benchmark papers

### Novelty Statement Template

```
Our approach differs from [Prior Work A] in that we [specific difference].
Unlike [Prior Work B], our method [specific difference].
While [Prior Work C] addresses [their focus], we focus on [our focus].
```

---

## Red Flags and Resolution

### Red Flag: "To the best of our knowledge, no work has..."

**Required Evidence:**
- Documented search across multiple databases
- Query terms used
- Date range searched
- Explanation of why existing works don't address the claimed gap

### Red Flag: Citation from obscure source

**Required Action:**
1. Verify the source exists
2. Check if cited correctly
3. Consider if a more mainstream source exists
4. Document verification effort

### Red Flag: Many citations from same author/group

**Required Check:**
- Expand search to other groups
- Include competing approaches
- Ensure balanced perspective

### Red Flag: All citations are preprints

**Required Action:**
- Check if published versions exist
- Update to formal publications where available
- Acknowledge preprint status in document

---

## Verification Report Format

Create verification report at `docs/survey/citation-verification-report.md`:

```markdown
# Citation Verification Report

## Summary
- Total citations: 45
- Grade A (DOI-verified): 28 (62%)
- Grade B (Trusted source): 12 (27%)
- Grade C (Preprint): 4 (9%)
- Grade D (Unverified): 1 (2%)
- Grade F (Fabrication risk): 0 (0%)

## Portfolio Quality
- A+B percentage: 89% ✓ (meets 80% threshold)
- F citations: 0 ✓ (meets 0 threshold)

## Verification Details

| Citation | DOI | Source | Grade | Notes |
|----------|-----|--------|-------|-------|
| vaswani2017 | 10.48550/arXiv.1706.03762 | Semantic Scholar | A | NeurIPS 2017 |
| dosovitskiy2021 | 10.1007/978-3-030-58452-8_14 | CrossRef | A | ICLR 2021 |
| brown2020 | arXiv:2005.14165 | arXiv | C | Preprint, no published version |

## Recommendations
- Grade D citation "smith2023" needs manual verification
- Consider finding Grade A alternatives for Grade C citations
```

---

## Verification Checklist

Before submitting any deliverable:

- [ ] All citations have at least Grade C verification
- [ ] At least 80% (Survey) / 90% (Paper) are Grade A or B
- [ ] All DOI citations resolve correctly
- [ ] All arXiv citations checked for published versions
- [ ] Novelty claims have documented prior art search
- [ ] No "to our knowledge" claims without search evidence
- [ ] All references include access dates
- [ ] Competing approaches are represented

---

## Automation Support

### Scripts

```bash
# Check DOI validity
python3 scripts/verify_citations.py --project-root /path/to/project --check-doi

# Check arXiv for published versions
python3 scripts/verify_citations.py --project-root /path/to/project --check-arxiv

# Full verification report
python3 scripts/verify_citations.py --project-root /path/to/project --full-report
```

### Integration with latex-citation-curator

For Paper phase, use the `latex-citation-curator` skill for:
- Finding verified BibTeX entries
- Checking DOI authenticity
- Semantic Scholar integration

---

## Exceptions

### Acceptable Exceptions to Grade Requirements

| Exception | Justification |
|-----------|---------------|
| Very recent work (last 3 months) | Preprint acceptable, note "forthcoming" |
| Unpublished seminal work | Document why unpublished is appropriate |
| Dataset/software citations | Cite repository, not paper |
| Historical context | Older seminal work may lack DOI |

### Handling Exceptions

1. Document the exception reason
2. Provide alternative verification if possible
3. Note in verification report
4. Researcher approval required

---

## Manual Review Process

When automated verification fails:

1. **Document the citation exactly as found**
2. **Search manually in multiple databases**
3. **Record search terms and results**
4. **If found, update metadata and re-grade**
5. **If not found, flag for researcher review**

### Manual Review Request Format

```markdown
## Manual Review Request

**Citation:** [Author, Title, Year]
**Issue:** [Cannot verify / Source unclear / Metadata mismatch]
**Attempted:**
- Semantic Scholar search: No results
- CrossRef search: No results
- arXiv search: No results

**Requested Action:** [Remove / Find alternative / Researcher decision needed]
```