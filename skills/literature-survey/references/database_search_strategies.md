# Database Search Strategies

This document provides detailed guidance for searching academic databases using their APIs.

## IMPORTANT: Use Academic Database APIs, NOT Web Search

**CRITICAL: Do NOT use web search for literature discovery.**

Always use official academic database APIs for:
- Reproducibility of search results
- Access to structured metadata
- Proper citation information
- Verification capabilities

---

## Database Selection Guide

### Quick Reference

| Database | Primary Domain | API Type | Rate Limit |
|----------|---------------|----------|------------|
| **Semantic Scholar** | AI/ML, CS | REST | 100 req/5min (free) |
| **arXiv** | Preprints (CS, Physics, Math) | REST/XML | 1 req/3sec |
| **DBLP** | Computer Science | REST | Polite usage |
| **OpenAlex** | Comprehensive | REST | 10 req/sec |
| **PubMed** | Biomedical, Life Sciences | REST | 3 req/sec |
| **CrossRef** | DOI, Cross-disciplinary | REST | Polite usage |

---

## Semantic Scholar

### Best For
- AI and Machine Learning papers
- Computer Science research
- Citation network analysis
- Finding related papers

### API Endpoint
```
https://api.semanticscholar.org/graph/v1/paper/search
```

### Authentication
- Free tier: 100 requests per 5 minutes
- With API key: Higher limits available
- Request key at: https://www.semanticscholar.org/product/api

### Search Examples

```bash
# Basic search
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer+attention&limit=10"

# With filters and fields
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=vision+transformer&year=2022-2026&venue=NeurIPS,ICML,ICLR&fields=title,authors,year,venue,citationCount,abstract&limit=20"

# Get paper by ID
curl "https://api.semanticscholar.org/graph/v1/paper/CORPUS_ID?fields=title,authors,year,venue,abstract,references,citations"

# Search by author
curl "https://api.semanticscholar.org/graph/v1/author/search?query=Vaswani"

# Get author's papers
curl "https://api.semanticscholar.org/graph/v1/author/AUTHOR_ID/papers?fields=title,year,venue"
```

### Available Fields
```
title, authors, year, venue, citationCount, abstract,
references, citations, externalIds, url, publicationDate,
publicationTypes, journal, tldr
```

### Response Parsing

```python
import requests
import json

response = requests.get(
    "https://api.semanticscholar.org/graph/v1/paper/search",
    params={
        "query": "vision transformer",
        "year": "2023-2026",
        "fields": "title,authors,year,venue,citationCount,abstract",
        "limit": 20
    }
)
data = response.json()

for paper in data.get("data", []):
    print(f"{paper['year']} - {paper['title']}")
    print(f"  Venue: {paper.get('venue', 'N/A')}")
    print(f"  Citations: {paper.get('citationCount', 0)}")
```

### Tips
- Use `year` parameter to filter by publication year (e.g., `2022-2026`)
- Use `venue` parameter to filter by specific venues
- Use `fields` to specify what data to return
- The `tldr` field provides AI-generated summaries

---

## arXiv

### Best For
- Recent preprints (not yet peer-reviewed)
- Computer Science, Physics, Mathematics, Statistics
- Finding cutting-edge research
- Papers that may later appear in conferences

### API Endpoint
```
https://export.arxiv.org/api/query
```

### Rate Limit
- 1 request per 3 seconds
- Be respectful; add delays between requests

### Search Examples

```bash
# Basic search
curl "https://export.arxiv.org/api/query?search_query=all:transformer&start=0&max_results=10"

# Search by title
curl "https://export.arxiv.org/api/query?search_query=ti:attention+mechanism&max_results=10"

# Search by author
curl "https://export.arxiv.org/api/query?search_query=au:Vaswani&max_results=10"

# Search in specific category
curl "https://export.arxiv.org/api/query?search_query=cat:cs.LG+AND+all:neural&max_results=10"

# Get by arXiv ID
curl "https://export.arxiv.org/api/query?id_list=1706.03762,2301.00001"
```

### Subject Categories

| Prefix | Domain |
|--------|--------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language (NLP) |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.RO | Robotics |
| stat.ML | Machine Learning (Statistics) |
| physics | Physics |
| math | Mathematics |

### Response Parsing

```python
import xml.etree.ElementTree as ET
import requests

response = requests.get(
    "https://export.arxiv.org/api/query",
    params={
        "search_query": "all:transformer",
        "start": 0,
        "max_results": 10
    }
)

root = ET.fromstring(response.content)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

for entry in root.findall('atom:entry', ns):
    title = entry.find('atom:title', ns).text
    summary = entry.find('atom:summary', ns).text
    published = entry.find('atom:published', ns).text

    arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]

    print(f"arXiv:{arxiv_id} - {title.strip()}")
```

### Tips
- Always check if arXiv preprints have been published in peer-reviewed venues
- Use `ti:` prefix to search only titles
- Use `au:` prefix to search by author
- Combine conditions with `AND`, `OR`, `ANDNOT`

---

## DBLP

### Best For
- Computer Science bibliography
- Finding peer-reviewed publications
- Author publication records
- Venue-specific searches

### API Endpoint
```
https://dblp.org/search/publ/api
```

### Search Examples

```bash
# Basic search
curl "https://dblp.org/search/publ/api?q=transformer+attention&format=json&h=20"

# Search by author
curl "https://dblp.org/search/author/api?q=Vaswani&format=json"

# Get author's publications
curl "https://dblp.org/pid/AUTHOR_PID.json"

# Search by venue
curl "https://dblp.org/search/venue/api?q=NeurIPS&format=json"
```

### Response Parsing

```python
import requests

response = requests.get(
    "https://dblp.org/search/publ/api",
    params={
        "q": "vision transformer",
        "format": "json",
        "h": 20
    }
)
data = response.json()

hits = data.get('result', {}).get('hits', {}).get('hit', [])
for hit in hits:
    info = hit.get('info', {})
    print(f"{info.get('year', 'N/A')} - {info.get('title', 'N/A')}")
    print(f"  Venue: {info.get('venue', 'N/A')}")
    print(f"  URL: {info.get('url', 'N/A')}")
```

### Tips
- Use DBLP to verify publication authenticity
- DBLP provides reliable BibTeX entries
- Check `type` field for publication type (Conference, Journal, etc.)

---

## OpenAlex

### Best For
- Comprehensive multi-disciplinary search
- Works across all academic domains
- Open access focus
- Institutional affiliation searches

### API Endpoint
```
https://api.openalex.org/works
```

### Rate Limit
- 10 requests per second (polite pool)
- With email: faster response times

### Search Examples

```bash
# Basic search
curl "https://api.openalex.org/works?search=machine+learning&per_page=20"

# With filters
curl "https://api.openalex.org/works?search=transformer&filter=publication_year:2023-2026,type:article&per_page=20"

# Filter by venue
curl "https://api.openalex.org/works?filter=primary_location.source.display_name:NeurIPS"

# Get by DOI
curl "https://api.openalex.org/works/https://doi.org/10.1234/example"

# Get author works
curl "https://api.openalex.org/works?filter=author.id:AUTOR_ID"
```

### Filter Options

| Filter | Example |
|--------|---------|
| `publication_year` | `2023-2026` or `2024` |
| `type` | `article`, `conference-paper`, `preprint` |
| `is_oa` | `true` (open access only) |
| `cited_by_count` | `>100` |
| `primary_location.source.id` | Specific venue ID |

### Response Parsing

```python
import requests

response = requests.get(
    "https://api.openalex.org/works",
    params={
        "search": "vision transformer",
        "filter": "publication_year:2023-2026",
        "per_page": 20
    }
)
data = response.json()

for work in data.get('results', []):
    print(f"{work.get('publication_year')} - {work.get('title')}")
    print(f"  DOI: {work.get('doi', 'N/A')}")
    print(f"  Citations: {work.get('cited_by_count', 0)}")

    # Venue info
    location = work.get('primary_location', {}) or {}
    source = location.get('source', {}) or {}
    print(f"  Venue: {source.get('display_name', 'N/A')}")
```

### Tips
- OpenAlex unifies multiple data sources
- Good for finding open access versions
- Use `mailto` parameter for faster responses

---

## PubMed

### Best For
- Biomedical and life sciences
- Medical research
- Biology and bioinformatics
- Health sciences

### API Endpoint (Entrez)
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

### Rate Limit
- 3 requests per second
- Use API key for higher limits

### Search Examples

```bash
# Search for PMIDs
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=machine+learning+diagnosis&retmax=20&retmode=json"

# Fetch paper details
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=12345678&retmode=xml"

# With date filter
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=deep+learning&datetype=pdat&mindate=2023&maxdate=2026"
```

### Response Parsing

```python
import requests

# Search
search_response = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={
        "db": "pubmed",
        "term": "machine learning diagnosis",
        "retmax": 20,
        "retmode": "json"
    }
)
pmids = search_response.json()['esearchresult']['idlist']

# Fetch details
fetch_response = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
    params={
        "db": "pubmed",
        "id": ",".join(pmids[:5]),
        "retmode": "xml"
    }
)
```

### Tips
- Use MeSH terms for more precise searches
- Combine with Boolean operators (AND, OR, NOT)
- Use `[ti]` for title, `[au]` for author

---

## CrossRef

### Best For
- DOI verification
- Metadata retrieval
- Cross-disciplinary search
- Publisher information

### API Endpoint
```
https://api.crossref.org/works
```

### Search Examples

```bash
# Verify DOI
curl "https://api.crossref.org/works/10.48550/arXiv.1706.03762"

# Search by title
curl "https://api.crossref.org/works?query.title=attention+is+all+you+need&rows=5"

# Search with filters
curl "https://api.crossref.org/works?query=transformer&filter=from-pub-date:2023,until-pub-date:2026&rows=20"
```

### DOI Verification

```bash
# Check if DOI exists and resolves
curl -I "https://doi.org/10.1234/example"

# Returns HTTP 302 if valid
# Returns HTTP 404 if not found
```

### Tips
- Always verify DOIs using CrossRef before citing
- Use `query.title` for title-specific searches
- Check `is-referenced-by-count` for citation count

---

## Multi-Database Search Strategy

### Recommended Order

1. **Start with Semantic Scholar** - Best for AI/ML topics, good metadata
2. **Add arXiv** - For recent preprints and CS topics
3. **Use DBLP** - For CS bibliography verification
4. **Include OpenAlex** - For comprehensive coverage
5. **Use PubMed** - For biomedical topics
6. **Verify with CrossRef** - For DOI confirmation

### Deduplication Strategy

After collecting results from multiple databases:

1. **Primary key**: DOI (if available)
2. **Secondary key**: Normalized title
3. **Tertiary key**: Author + Year + Venue

```python
def normalize_title(title):
    """Normalize title for deduplication."""
    import re
    return re.sub(r'[^\w\s]', '', title.lower()).strip()

def deduplicate_papers(papers):
    """Remove duplicate papers from multi-source results."""
    seen = set()
    unique = []

    for paper in papers:
        # Try DOI first
        if paper.get('doi'):
            key = f"doi:{paper['doi'].lower()}"
        # Fall back to title
        else:
            key = f"title:{normalize_title(paper.get('title', ''))}"

        if key not in seen:
            seen.add(key)
            unique.append(paper)

    return unique
```

### Query Translation

Adapt queries for each database's syntax:

| Concept | Semantic Scholar | arXiv | OpenAlex |
|---------|------------------|-------|----------|
| AND | space | AND | space |
| OR | OR | OR | OR |
| NOT | NOT | ANDNOT | NOT |
| Title | N/A | ti: | N/A |
| Author | N/A | au: | N/A |

---

## Rate Limiting Best Practices

1. **Add delays between requests**
   ```python
   import time
   time.sleep(1)  # 1 second between requests
   ```

2. **Use exponential backoff for errors**
   ```python
   import time

   def fetch_with_retry(url, max_retries=3):
       for attempt in range(max_retries):
           try:
               response = requests.get(url)
               if response.status_code == 200:
                   return response
               elif response.status_code == 429:
                   wait = 2 ** attempt
                   time.sleep(wait)
               else:
                   return None
           except Exception as e:
               time.sleep(2 ** attempt)
       return None
   ```

3. **Cache results locally**
   ```python
   import json
   import hashlib

   def cached_search(query, cache_dir=".cache"):
       cache_key = hashlib.md5(query.encode()).hexdigest()
       cache_file = f"{cache_dir}/{cache_key}.json"

       try:
           with open(cache_file) as f:
               return json.load(f)
       except FileNotFoundError:
           result = actual_search(query)
           with open(cache_file, 'w') as f:
               json.dump(result, f)
           return result
   ```