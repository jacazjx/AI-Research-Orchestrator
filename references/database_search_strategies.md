# Database Search Strategies

This document provides detailed guidelines for using academic database APIs during literature surveys. **Always use these APIs instead of web search for literature discovery.**

## API Overview

| API | Best For | Rate Limit | Key Features |
|-----|----------|------------|--------------|
| **Semantic Scholar** | AI/ML, Computer Science | 100 requests/5min (public) | Citation graph, paper relationships |
| **arXiv** | Preprints (CS, Physics, Math) | 1 request/3 seconds | Latest research, version tracking |
| **DBLP** | Computer Science bibliography | No documented limit | Venue-verified publications |
| **OpenAlex** | Comprehensive multi-disciplinary | 100,000 requests/day | Open access, institutional data |
| **CrossRef** | DOI verification | 50 requests/second | DOI metadata, reference linking |
| **PubMed** | Biomedical, Life Sciences | 3 requests/second | MeSH terms, medical literature |

---

## Semantic Scholar API

**Endpoint:** `https://api.semanticscholar.org/graph/v1`

### Search Papers

```bash
# Basic search
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=attention+mechanism&limit=10"

# Search with filters
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer&limit=20&year=2022-2025&fields=title,authors,year,venue,citationCount,abstract"

# Search by author
curl "https://api.semanticscholar.org/graph/v1/author/search?query=Vaswani"

# Get paper details
curl "https://api.semanticscholar.org/graph/v1/paper/CORPUS_ID?fields=title,authors,year,venue,abstract,references,citations"

# Search with venue filter
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=vision+transformer&venue=NeurIPS,ICML,ICLR&year=2022-2025"
```

### Available Fields

```
title, authors, year, venue, citationCount, abstract,
references, citations, publicationDate, journal,
externalIds (DOI, arXiv, PubMed), publicationTypes
```

### Search Strategies

| Strategy | Query Pattern | Use Case |
|----------|---------------|----------|
| Keyword search | `query=keyword1+keyword2` | Broad exploration |
| Title search | `query.title=exact+title` | Finding specific papers |
| Author search | `author/search?query=name` | Finding papers by author |
| Venue filter | `venue=NeurIPS,ICML,ICLR` | Top-tier publications only |
| Year range | `year=2022-2025` | Recent work |

### Best Practices

1. **Start broad, then narrow**: Begin with keyword search, add filters based on results
2. **Use citation count**: Sort by `citationCount` to find seminal papers
3. **Check references**: Use `references` field to find related work
4. **Follow citations**: Use `citations` field to find newer papers building on the work

---

## arXiv API

**Endpoint:** `https://export.arxiv.org/api/query`

### Search Papers

```bash
# Basic search
curl "https://export.arxiv.org/api/query?search_query=all:transformer+attention&start=0&max_results=10"

# Search by title
curl "https://export.arxiv.org/api/query?search_query=ti:vision+transformer&start=0&max_results=10"

# Search by author
curl "https://export.arxiv.org/api/query?search_query=au:Vaswani&start=0&max_results=10"

# Search by category
curl "https://export.arxiv.org/api/query?search_query=cat:cs.LG&start=0&max_results=10"

# Get by arXiv ID
curl "https://export.arxiv.org/api/query?id_list=1706.03762,2301.07094"
```

### Category Codes

| Category | Description |
|----------|-------------|
| `cs.LG` | Machine Learning |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision and Pattern Recognition |
| `cs.AI` | Artificial Intelligence |
| `cs.NE` | Neural and Evolutionary Computing |
| `stat.ML` | Machine Learning (Statistics) |

### Query Prefixes

| Prefix | Field | Example |
|--------|-------|---------|
| `ti` | Title | `ti:transformer` |
| `au` | Author | `au:Bengio` |
| `abs` | Abstract | `abs:attention+mechanism` |
| `cat` | Category | `cat:cs.LG` |
| `all` | All fields | `all:transformer` |

### Best Practices

1. **Respect rate limits**: 1 request per 3 seconds
2. **Check for published version**: arXiv papers may have peer-reviewed versions
3. **Note submission date**: Important for establishing precedence
4. **Use categories**: Narrow search to relevant subfields

---

## DBLP API

**Endpoint:** `https://dblp.org/search`

### Search Publications

```bash
# Search publications
curl "https://dblp.org/search/publ/api?q=transformer&format=json&h=20"

# Search authors
curl "https://dblp.org/search/author/api?q=Vaswani&format=json"

# Search venues
curl "https://dblp.org/search/venue/api?q=NeurIPS&format=json"
```

### Publication Types

| Type | Description |
|------|-------------|
| `Conference and Workshop Papers` | Peer-reviewed conference publications |
| `Journal Articles` | Peer-reviewed journal publications |
| `Informal and Refereed Publications` | Workshops, technical reports |
| `Books and Theses` | Books, book chapters, theses |

### Best Practices

1. **Venue verification**: DBLP confirms publication in legitimate venues
2. **Author disambiguation**: Use DBLP author IDs to distinguish researchers
3. **Bibliography links**: Follow "citations" links for related work
4. **Note publication type**: Conferences vs journals have different review standards

---

## OpenAlex API

**Endpoint:** `https://api.openalex.org`

### Search Works

```bash
# Basic search
curl "https://api.openalex.org/works?search=vision+transformer&per_page=20"

# Search with filters
curl "https://api.openalex.org/works?search=transformer&filter=publication_year:2022-2025,type:article&per_page=20"

# Filter by venue
curl "https://api.openalex.org/works?filter=primary_location.source.id:https://openalex.org/V13797631"

# Filter by author
curl "https://api.openalex.org/works?filter=author.id:https://openalex.org/A5023888391"

# Get work by DOI
curl "https://api.openalex.org/works/https://doi.org/10.48550/arXiv.1706.03762"
```

### Work Types

| Type | Description |
|------|-------------|
| `article` | Journal article |
| `preprint` | Preprint/eprint |
| `proceedings-article` | Conference paper |
| `book` | Book |
| `dissertation` | Thesis |

### Filter Examples

```bash
# Multiple filters combined
curl "https://api.openalex.org/works?filter=publication_year:2022-2025,type:article,is_oa:true"

# Cited by count threshold
curl "https://api.openalex.org/works?filter=cited_by_count:>100"

# Specific venue
curl "https://api.openalex.org/works?filter=primary_location.source.display_name:NeurIPS"
```

---

## CrossRef API

**Endpoint:** `https://api.crossref.org`

### DOI Verification

```bash
# Verify DOI
curl "https://api.crossref.org/works/10.48550/arXiv.1706.03762"

# Search by title
curl "https://api.crossref.org/works?query.title=attention+is+all+you+need&rows=5"

# Search by author
curl "https://api.crossref.org/works?query.author=Vaswani&rows=10"

# Get works from member (publisher)
curl "https://api.crossref.org/members/1965/works?rows=20"
```

### Use Cases

| Use Case | API Call |
|----------|----------|
| Verify DOI authenticity | `GET /works/{doi}` |
| Find paper by title | `GET /works?query.title={title}` |
| Get citation metadata | `GET /works/{doi}` |
| Check publisher | `GET /works/{doi}?select=member,publisher` |

---

## PubMed API (NCBI E-utilities)

**Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`

### Search and Fetch

```bash
# Search for IDs
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=machine+learning&retmax=20"

# Fetch details
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=12345678&rettype=abstract"

# Get summary
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=12345678"
```

### MeSH Terms

```bash
# Search with MeSH term
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Neural+Networks[MeSH]+AND+Deep+Learning[Title/Abstract]"
```

---

## Combined Search Workflow

For a comprehensive literature search, follow this workflow:

### Step 1: Identify Keywords

1. Extract key terms from research question
2. Identify synonyms and related terms
3. Note important authors and venues

### Step 2: Search Multiple Databases

```bash
# 1. Semantic Scholar (for AI/ML papers)
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=YOUR_QUERY&limit=50&fields=title,authors,year,venue,citationCount"

# 2. arXiv (for preprints)
curl "https://export.arxiv.org/api/query?search_query=all:YOUR_QUERY&max_results=50"

# 3. DBLP (for verified CS publications)
curl "https://dblp.org/search/publ/api?q=YOUR_QUERY&format=json&h=50"

# 4. OpenAlex (comprehensive)
curl "https://api.openalex.org/works?search=YOUR_QUERY&per_page=50"
```

### Step 3: Deduplicate Results

1. Match by DOI (most reliable)
2. Match by title similarity
3. Match by arXiv ID

### Step 4: Verify Citations

1. Check DOI via CrossRef
2. Verify metadata matches
3. Assign verification grade

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Rate limit exceeded | Wait and retry |
| 404 Not Found | Invalid ID or query | Check query syntax |
| 500 Server Error | API temporarily down | Retry with backoff |
| Timeout | Slow response | Reduce query complexity |

### Retry Strategy

```bash
# Exponential backoff
for i in 1 2 3 4 5; do
  response=$(curl -s -w "%{http_code}" "API_URL")
  if [[ $response -eq 200 ]]; then
    break
  fi
  sleep $((2 ** i))
done
```

---

## Search Log Format

Record all searches in `docs/survey/search-log.md`:

```markdown
# Search Log

## Session: 2024-01-15T10:00:00Z

### Semantic Scholar
- Query: `attention mechanism`
- Filters: `year=2022-2025, fields=title,authors,year,venue,citationCount`
- Results: 50
- Timestamp: 2024-01-15T10:01:23Z

### arXiv
- Query: `all:attention mechanism`
- Categories: `cs.LG, cs.CL`
- Results: 30
- Timestamp: 2024-01-15T10:02:45Z

## Deduplication
- Total papers found: 80
- Duplicates removed: 15
- Unique papers: 65
```