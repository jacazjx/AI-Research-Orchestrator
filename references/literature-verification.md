# Literature Verification Protocol

This document defines the standards and procedures for verifying citation authenticity in the survey phase.

## IMPORTANT: Use Academic Database APIs, NOT Web Search

**CRITICAL: Do NOT use websearch for literature search.**

Use these academic database APIs instead:

### Semantic Scholar API (Preferred for AI/ML)

```bash
# Search for papers
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=attention+mechanism&limit=10&year=2022-2025&fields=title,authors,year,venue,citationCount"

# Get paper details
curl "https://api.semanticscholar.org/graph/v1/paper/CORPUS_ID?fields=title,authors,year,venue,abstract,references"

# Search by author
curl "https://api.semanticscholar.org/graph/v1/author/search?query=Vaswani"
```

### arXiv API

```bash
# Search for papers
curl "https://export.arxiv.org/api/query?search_query=all:transformer+attention&start=0&max_results=10"

# Get by ID
curl "https://export.arxiv.org/api/query?id_list=1706.03762"
```

### CrossRef API (DOI Verification)

```bash
# Verify DOI
curl "https://api.crossref.org/works/10.48550/arXiv.1706.03762"

# Search by title
curl "https://api.crossref.org/works?query.title=attention+is+all+you+need&rows=5"
```

### DBLP API (Computer Science)

```bash
# Search publications
curl "https://dblp.org/search/publ/api?q=transformer&format=json&h=20"

# Search authors
curl "https://dblp.org/search/author/api?q=Vaswani"
```

### OpenAlex API

```bash
# Search works
curl "https://api.openalex.org/works?search=vision+transformer&filter=publication_year:2022-2025&per_page=10"
```

## Verification Standards

### Citation Quality Grades

| Grade | Criteria | Verification Method |
|-------|----------|---------------------|
| A | DOI-verified, peer-reviewed publication | DOI resolution check |
| B | Trusted source (DBLP, Semantic Scholar, publisher) | Source lookup |
| C | arXiv or other preprint server | URL verification |
| D | Unverified source, needs manual check | Requires human review |
| F | Cannot locate or verify | Must be removed or flagged |

### Minimum Acceptable Standards

For Gate 1 approval, the citation portfolio must satisfy:

1. **At least 80% of citations are Grade A or B**
2. **No Grade F citations without explicit justification**
3. **All Grade D citations have manual verification plan**
4. **All novelty claims are supported by at least one Grade A or B citation**

## Verification Methods

### 1. DOI Verification

```
DOI Check Process:
1. Extract DOI from citation
2. Resolve via https://doi.org/[DOI]
3. Verify title, authors, year match
4. Record resolution status
```

**Tools:**
- `curl -I https://doi.org/[DOI]` (returns HTTP 302 if valid)
- CrossRef API: `https://api.crossref.org/works/[DOI]`

### 2. Trusted Source Verification

**DBLP:**
- URL: `https://dblp.org/search?q=[title]`
- Use for: Computer Science venues

**Semantic Scholar:**
- API: `https://api.semanticscholar.org/graph/v1/paper/search?query=[title]`
- Use for: AI/ML papers

**Google Scholar:**
- URL: `https://scholar.google.com/scholar?q=[title]`
- Use for: General academic search

**Publisher Databases:**
- ACM DL: `https://dl.acm.org/doSearch?query=[title]`
- IEEE Xplore: `https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=[title]`
- Springer: `https://link.springer.com/search?query=[title]`

### 3. arXiv Verification

```
arXiv Check Process:
1. Extract arXiv ID (format: YYMM.NNNNN or arch-ive/YYMMNNN)
2. Resolve via https://arxiv.org/abs/[ID]
3. Check if published version exists
4. Recommend formal publication if available
```

**Tools:**
- arXiv API: `https://export.arxiv.org/api/query?id_list=[ID]`
- Check for DOI in arXiv metadata

## Citation Metadata Requirements

Every citation must include:

### Required Fields
- **Title**: Exact title from publication
- **Authors**: At least first author full name
- **Year**: Publication year
- **Venue**: Conference, journal, or repository name

### Recommended Fields
- **DOI**: Digital Object Identifier
- **URL**: Direct link to paper
- **Pages**: Page range for journals/conferences
- **Volume/Number**: For journals
- **Publisher**: For books

### Quality Enhancement Fields
- **Access Date**: When the citation was verified
- **Verification Status**: Grade (A-F)
- **Verification Source**: Where it was verified
- **Published Version**: If citing preprint, link to published version

## Novelty Claim Verification

### Required Evidence for Novelty

When claiming novelty, provide:

1. **Direct Prior Art Search**
   - Search results for key terms
   - Papers with similar titles/abstracts
   - Related work sections in similar papers

2. **Differentiation Evidence**
   - Specific differences with closest prior work
   - Technical novelty (not just application novelty)
   - Theoretical novelty (if applicable)

3. **Coverage Analysis**
   - Survey papers in the area
   - Recent workshops/tutorials
   - Benchmark papers

### Novelty Statement Template

```
Our approach differs from [Prior Work A] in that we [specific difference].
Unlike [Prior Work B], our method [specific difference].
While [Prior Work C] addresses [their focus], we focus on [our focus].
```

## Red Flags and How to Address Them

### Red Flag: "To the best of our knowledge, no work has..."

**Required Evidence:**
- Documented search across multiple databases
- Query terms used
- Date range searched
- Why existing works don't address the claimed gap

### Red Flag: Citation from obscure source

**Required Action:**
- Verify the source exists
- Check if cited correctly
- Consider if a more mainstream source exists
- Document verification effort

### Red Flag: Many citations from same author/group

**Required Check:**
- Expand search to other groups
- Include competing approaches
- Ensure balanced perspective

### Red Flag: All citations are preprints

**Required Action:**
- Check if published versions exist
- Update to formal publications where available
- Acknowledge preprint status in survey

## Verification Checklist

Before submitting survey for Gate 1:

- [ ] All citations have at least Grade C verification
- [ ] At least 80% are Grade A or B
- [ ] All DOI citations resolve correctly
- [ ] All arXiv citations checked for published versions
- [ ] Novelty claims have documented prior art search
- [ ] No "to our knowledge" claims without search evidence
- [ ] All references include access dates
- [ ] Competing approaches are represented

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

For papers phase, use `latex-citation-curator` skill for:
- Finding verified BibTeX entries
- Checking DOI authenticity
- Semantic Scholar integration

## Manual Review Process

When automated verification fails:

1. **Document the citation exactly as found**
2. **Search manually in multiple databases**
3. **Record search terms and results**
4. **If found, update metadata**
5. **If not found, flag for researcher review**

## Exceptions

### Acceptable Exceptions to Grade Requirements

1. **Very recent work** (within last 3 months) - preprint acceptable
2. **Unpublished seminal work** - document why unpublished is appropriate
3. **Dataset/software citations** - cite repository, not paper
4. **Historical context** - older seminal work may lack DOI

## API Configuration

### Semantic Scholar

**Rate Limits:**
- 100 requests per 5 minutes (unauthenticated)
- 5000 requests per 5 minutes (with API key)

**Configuration:**

```bash
# Set environment variable (optional, increases rate limit)
export SEMANTIC_SCHOLAR_API_KEY="your-api-key"
```

**Error Handling:**

```python
import os
import requests

API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
headers = {"x-api-key": API_KEY} if API_KEY else {}

def search_papers(query: str, limit: int = 10) -> dict:
    """Search Semantic Scholar with rate limit handling."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": query, "limit": limit}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            import time
            time.sleep(60)
            return search_papers(query, limit)
        raise
    except requests.exceptions.Timeout:
        raise TimeoutError("Semantic Scholar API request timed out")
```

### arXiv

**Rate Limits:**
- 1 request per 3 seconds (polite usage)

**Error Handling:**

```python
import time
import requests

def search_arxiv(query: str, max_results: int = 10) -> str:
    """Search arXiv with rate limit handling."""
    url = "https://export.arxiv.org/api/query"
    params = {"search_query": f"all:{query}", "max_results": max_results}

    time.sleep(3)  # Rate limiting
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.text
```

### CrossRef

**Rate Limits:**
- No strict limit, but be polite (add User-Agent header)

**Configuration:**

```python
import requests

headers = {
    "User-Agent": "AI-Research-Orchestrator/1.0 (mailto:your-email@example.com)"
}

def verify_doi(doi: str) -> dict:
    """Verify a DOI via CrossRef."""
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
```

### OpenAlex

**Rate Limits:**
- 100,000 requests per day (free tier)

**Configuration:**

```bash
# Optional: set email for faster access
export OPENALEX_EMAIL="your-email@example.com"
```

```python
import os
import requests

def search_openalex(query: str, per_page: int = 10) -> dict:
    """Search OpenAlex works."""
    url = "https://api.openalex.org/works"
    params = {"search": query, "per_page": per_page}

    email = os.environ.get("OPENALEX_EMAIL")
    if email:
        params["mailto"] = email

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
```

## Common Error Patterns

### Rate Limiting

Most APIs return HTTP 429 when rate limited. Handle gracefully:

```python
def api_call_with_retry(func, max_retries=3, backoff=60):
    """Call API with exponential backoff on rate limit."""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < max_retries - 1:
                time.sleep(backoff * (attempt + 1))
            else:
                raise
```

### Timeout Handling

Always set timeouts for external API calls:

```python
# Good: explicit timeout
response = requests.get(url, timeout=30)

# Bad: no timeout (can hang indefinitely)
response = requests.get(url)
```

### Graceful Degradation

When APIs are unavailable, log and continue:

```python
import logging

logger = logging.getLogger(__name__)

def search_with_fallback(query: str) -> list:
    """Search with fallback to alternative APIs."""
    results = []

    try:
        results = search_semantic_scholar(query)
    except Exception as e:
        logger.warning(f"Semantic Scholar failed: {e}")

        try:
            results = search_arxiv(query)
        except Exception as e:
            logger.error(f"All APIs failed: {e}")

    return results
```

## Project Configuration

Store API keys in `.autoresearch/config/orchestrator-config.yaml`:

```yaml
api_keys:
  semantic_scholar: "${SEMANTIC_SCHOLAR_API_KEY}"
  openalex_email: "${OPENALEX_EMAIL}"

rate_limits:
  respect_limits: true
  retry_on_429: true
  max_retries: 3
```