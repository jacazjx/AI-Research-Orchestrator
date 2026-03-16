# Citation Standards

This document defines the standards for citation verification and quality assessment in literature surveys.

## Core Principles

1. **Zero Tolerance for Fabrication** - Never invent or fabricate citations
2. **Verification Required** - Every citation must be verified through academic APIs
3. **Transparency** - Document verification status for all citations
4. **Quality Over Quantity** - Prefer fewer high-quality citations over many low-quality ones

---

## Citation Quality Grades

### Grade Definitions

| Grade | Criteria | Verification Method | Acceptable? |
|-------|----------|---------------------|-------------|
| **A** | DOI-verified, peer-reviewed publication | DOI resolution + CrossRef/Semantic Scholar | Yes |
| **B** | Trusted source (DBLP, Semantic Scholar, publisher) | Source lookup with metadata confirmation | Yes |
| **C** | arXiv or other preprint server | URL verification + metadata check | Conditional |
| **D** | Unverified source, needs manual check | Requires human review | No (pending) |
| **F** | Cannot locate or verify | Must be removed or flagged | No |

### Grade A Requirements

A citation receives Grade A when ALL of the following are true:

- [ ] Has a valid DOI
- [ ] DOI resolves correctly (HTTP 302 redirect)
- [ ] Title matches across sources
- [ ] Authors match (at least first author)
- [ ] Year matches
- [ ] Venue is a peer-reviewed publication

```bash
# Verify DOI
curl -I "https://doi.org/10.1234/example"
# Should return HTTP 302

# Verify via CrossRef
curl "https://api.crossref.org/works/10.1234/example"
# Should return valid JSON with matching metadata
```

### Grade B Requirements

A citation receives Grade B when:

- [ ] No DOI available, OR DOI verification failed but source is trusted
- [ ] Found in DBLP, Semantic Scholar, or publisher database
- [ ] Title, authors, year, venue confirmed
- [ ] Publication is peer-reviewed

```bash
# Verify via Semantic Scholar
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=TITLE&fields=title,authors,year,venue"

# Verify via DBLP
curl "https://dblp.org/search/publ/api?q=TITLE&format=json"
```

### Grade C Requirements

A citation receives Grade C when:

- [ ] arXiv or other preprint server
- [ ] No peer-reviewed version found
- [ ] Metadata verified on preprint server

**Important**: Always check if a published version exists:

```bash
# Check arXiv for published version
curl "https://export.arxiv.org/api/query?id_list=2301.00001"
# Look for DOI in the response

# Search Semantic Scholar for published version
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=TITLE&fields=title,year,venue,externalIds"
```

### Grade D (Needs Manual Check)

A citation receives Grade D when:

- [ ] Cannot verify through automated means
- [ ] Source is unclear or potentially unreliable
- [ ] Metadata is incomplete or inconsistent

**Action Required**: Manual verification by researcher before inclusion.

### Grade F (Fabrication Risk)

A citation receives Grade F when:

- [ ] Cannot be found in any academic database
- [ ] DOI does not resolve
- [ ] Metadata is inconsistent across sources
- [ ] Signs of potential fabrication

**Action Required**: Remove from survey, flag for investigation.

---

## Minimum Acceptable Standards

### For Survey Approval

| Metric | Minimum Requirement |
|--------|---------------------|
| Grade A + B combined | >= 80% of citations |
| Grade F citations | 0 (zero tolerance) |
| Grade D citations | Must have manual verification plan |
| Novelty claims | Supported by at least one Grade A or B citation |

### Citation Count Guidelines

| Survey Type | Minimum Citations | Recommended |
|-------------|-------------------|-------------|
| Quick landscape | 10-15 | 20-30 |
| Standard survey | 20-30 | 40-60 |
| Comprehensive review | 50+ | 100+ |

---

## Verification Workflow

### Step 1: Extract Citation Information

From each paper, extract:
- Title (exact)
- Authors (at least first author)
- Year
- Venue
- DOI (if available)

### Step 2: DOI Verification (if DOI exists)

```bash
# Method 1: Direct DOI resolution
curl -I "https://doi.org/[DOI]"

# Method 2: CrossRef API
curl "https://api.crossref.org/works/[DOI]"
```

**Success Criteria:**
- HTTP 302 redirect (Method 1)
- Valid JSON with matching metadata (Method 2)

### Step 3: Source Verification

If no DOI or DOI verification failed:

```bash
# Semantic Scholar
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=[TITLE]&fields=title,authors,year,venue,externalIds"

# DBLP (for CS)
curl "https://dblp.org/search/publ/api?q=[TITLE]&format=json"

# OpenAlex
curl "https://api.openalex.org/works?search=[TITLE]"
```

### Step 4: Metadata Cross-Check

Compare metadata across sources:

| Field | Tolerance |
|-------|-----------|
| Title | Exact match after normalization |
| First Author | Exact match |
| Year | +/- 1 year acceptable (conference vs journal) |
| Venue | Should match or be related |

### Step 5: Assign Grade

Based on verification results, assign appropriate grade.

---

## Citation Metadata Requirements

### Required Fields

Every citation MUST include:

```markdown
- **Title**: Exact title from publication
- **Authors**: At least first author full name
- **Year**: Publication year
- **Venue**: Conference, journal, or repository name
```

### Recommended Fields

```markdown
- **DOI**: Digital Object Identifier
- **URL**: Direct link to paper
- **Pages**: Page range for journals/conferences
- **Volume/Number**: For journals
- **Publisher**: For books
```

### Quality Enhancement Fields

```markdown
- **Access Date**: When the citation was verified
- **Verification Status**: Grade (A-F)
- **Verification Source**: Where it was verified
- **Published Version**: If citing preprint, link to published version
```

---

## Special Cases

### arXiv Preprints

**Rule**: Always check for published version before citing preprint.

```bash
# Check arXiv metadata for DOI
curl "https://export.arxiv.org/api/query?id_list=[ARXIV_ID]"

# Search for published version
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=[TITLE]&fields=title,year,venue,externalIds"
```

**If published version exists:**
- Cite the published version
- Note the arXiv ID in your notes
- Do NOT include arXiv in final bibliography

**If no published version:**
- Grade C acceptable
- Note that it is a preprint
- Consider if preprint is appropriate for your survey

### Conference vs Journal Versions

Many CS papers appear first as conference papers, then as journal extensions.

**Rule**: Cite the most complete/authoritative version.

- For methodology: Cite the version with full details
- For results: Cite the version with the results you reference
- When in doubt: Cite both with clear distinction

### Seminal Papers

Older seminal papers may lack DOI or have incomplete metadata.

**Acceptable for Grade B:**
- Paper is widely recognized as seminal
- Found in DBLP or other trusted bibliography
- Metadata confirmed through multiple sources
- Clearly marked as "seminal work"

### Dataset/Software Citations

Datasets and software should be cited, but with different standards:

**For Datasets:**
- Cite the dataset paper if available
- Include DOI or repository URL
- Note the version used

**For Software:**
- Cite the software paper if available
- Include repository URL
- Note the version used

---

## Novelty Claim Verification

### Required Evidence

When claiming novelty, provide:

1. **Prior Art Search**
   - Documented search across multiple databases
   - Query terms used
   - Date range searched
   - Results found

2. **Differentiation Evidence**
   - Specific differences with closest prior work
   - Technical novelty (not just application novelty)
   - Theoretical novelty (if applicable)

3. **Coverage Analysis**
   - Survey papers in the area
   - Recent workshops/tutorials
   - Benchmark papers

### Novelty Statement Template

```markdown
Our approach differs from [Prior Work A] in that we [specific difference].
Unlike [Prior Work B], our method [specific difference].
While [Prior Work C] addresses [their focus], we focus on [our focus].

Evidence:
- Searched [databases] with queries [queries]
- Found [N] related papers, none addressing [specific aspect]
- Closest prior work: [citation] which [brief description]
```

---

## Red Flags and Resolution

### Red Flag: "To the best of our knowledge, no work has..."

**Required Evidence:**
- Documented search across multiple databases
- Query terms used
- Date range searched
- Why existing works don't address the claimed gap

### Red Flag: Citation from obscure source

**Required Action:**
1. Verify the source exists
2. Check if cited correctly
3. Consider if a more mainstream source exists
4. Document verification effort

### Red Flag: Many citations from same author/group

**Required Check:**
1. Expand search to other groups
2. Include competing approaches
3. Ensure balanced perspective

### Red Flag: All citations are preprints

**Required Action:**
1. Check if published versions exist
2. Update to formal publications where available
3. Acknowledge preprint status in survey

### Red Flag: Citation count seems unrealistic

**Required Check:**
1. Verify citation count via Semantic Scholar
2. Cross-check with Google Scholar
3. Note any discrepancies

---

## Verification Checklist

Before finalizing survey:

- [ ] All citations have at least Grade C verification
- [ ] At least 80% are Grade A or B
- [ ] All DOI citations resolve correctly
- [ ] All arXiv citations checked for published versions
- [ ] Novelty claims have documented prior art search
- [ ] No "to our knowledge" claims without search evidence
- [ ] All references include access dates
- [ ] Competing approaches are represented
- [ ] No Grade F citations included

---

## Citation Format Standards

### BibTeX Format

```bibtex
@article{author2024title,
  author = {Author, First and Author, Second},
  title = {Full Title of the Paper},
  journal = {Journal Name},
  year = {2024},
  volume = {1},
  number = {1},
  pages = {1--10},
  doi = {10.xxxx/xxxxx},
  url = {https://doi.org/10.xxxx/xxxxx}
}
```

### Markdown Format

```markdown
[Author et al., 2024] Author, F., Author, S. (2024). Full Title of the Paper. *Journal Name*, 1(1), 1-10. https://doi.org/10.xxxx/xxxxx
```

### Verification Fields in BibTeX

Add custom fields to track verification:

```bibtex
@article{author2024title,
  ...,
  x-verified = {true},
  x-verification-grade = {A},
  x-verification-source = {CrossRef, Semantic Scholar},
  x-verification-date = {2024-03-15}
}
```

---

## Integration with latex-citation-curator

For paper writing phase, use the `latex-citation-curator` skill for:

- Finding verified BibTeX entries
- Checking DOI authenticity
- Semantic Scholar integration
- Quality scoring

See: `skills/latex-citation-curator/SKILL.md`