# Citation Formats

## Overview

Different academic disciplines and venues use different citation formats. This guide covers the most common formats used in computer science, AI/ML research, and related fields.

## IEEE Style

### In-Text Citations

**Numbered in order of appearance:**
```
Deep learning has transformed NLP [1].
Several studies [2], [5], [7] have demonstrated...
As shown in [3, pp. 45-50], the method achieves...
```

**Multiple citations:**
```
Related work includes [1]-[5] or [1], [3], [5]-[7]
```

### Reference List

**Journal Article:**
```
[1] A. Smith and B. Jones, "Title of the article," Journal Name,
    vol. 10, no. 2, pp. 100-115, Jan. 2020.
```

**Conference Paper:**
```
[2] C. Lee, D. Wang, and E. Chen, "Paper title," in Proc. Int.
    Conf. Machine Learning, 2021, pp. 1234-1245.
```

**Book:**
```
[3] J. Smith, Book Title, 2nd ed. City: Publisher, 2019.
```

**Website:**
```
[4] TensorFlow, "TensorFlow documentation," 2023. [Online].
    Available: https://www.tensorflow.org/
```

**arXiv Preprint:**
```
[5] A. Vaswani et al., "Attention is all you need," arXiv:1706.03762,
    2017.
```

## ACM Style

### In-Text Citations

**Author-year format:**
```
Deep learning has transformed NLP [Smith and Jones 2020].
Smith and Jones [2020] demonstrated that...
Several studies [Lee et al. 2021; Wang 2022] have shown...
```

**Multiple authors:**
```
First citation: Smith, Jones, and Lee [2020]
Subsequent: Smith et al. [2020]
```

### Reference List

**Journal Article:**
```
Smith, A. and Jones, B. 2020. Title of the article. Journal Name
10, 2 (Jan. 2020), 100–115.
```

**Conference Paper:**
```
Lee, C., Wang, D., and Chen, E. 2021. Paper title. In Proceedings
of the International Conference on Machine Learning, 1234–1245.
```

**Book:**
```
Smith, J. 2019. Book Title (2nd ed.). Publisher, City.
```

**DOI Format:**
```
Smith, A. 2020. Article title. Journal Name. DOI:https://doi.org/10.1000/xyz123
```

## APA Style (7th Edition)

### In-Text Citations

**Parenthetical:**
```
Deep learning has transformed NLP (Smith & Jones, 2020).
Several studies (Lee et al., 2021; Wang, 2022) have shown...
```

**Narrative:**
```
Smith and Jones (2020) demonstrated that...
According to Lee et al. (2021), the approach achieves...
```

**Direct quotation:**
```
(Smith, 2020, p. 15)
```

### Reference List

**Journal Article:**
```
Smith, A., & Jones, B. (2020). Title of the article. Journal Name,
10(2), 100–115. https://doi.org/10.1000/xyz123
```

**Conference Paper:**
```
Lee, C., Wang, D., & Chen, E. (2021, July). Paper title. In
Proceedings of the International Conference on Machine Learning
(pp. 1234–1245).
```

**Book:**
```
Smith, J. (2019). Book title: Subtitle (2nd ed.). Publisher.
```

**Website:**
```
TensorFlow. (2023). TensorFlow documentation.
https://www.tensorflow.org/
```

**arXiv Preprint:**
```
Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is
all you need. arXiv. https://arxiv.org/abs/1706.03762
```

## MLA Style (9th Edition)

### In-Text Citations

**Author-page:**
```
Deep learning has transformed NLP (Smith and Jones 20).
Smith and Jones argue that the field has changed (20).
```

### Works Cited

**Journal Article:**
```
Smith, Adam, and Beth Jones. "Title of the Article." Journal Name,
vol. 10, no. 2, 2020, pp. 100-15.
```

**Conference Paper:**
```
Lee, Chris, et al. "Paper Title." Proceedings of the International
Conference on Machine Learning, 2021, pp. 1234-45.
```

**Book:**
```
Smith, John. Book Title. 2nd ed., Publisher, 2019.
```

## BibTeX Formats

### Common Entry Types

```bibtex
@article{smith2020,
  author    = {Smith, Adam and Jones, Beth},
  title     = {Title of the Article},
  journal   = {Journal Name},
  volume    = {10},
  number    = {2},
  pages     = {100--115},
  year      = {2020},
  doi       = {10.1000/xyz123}
}

@inproceedings{lee2021,
  author    = {Lee, Chris and Wang, David and Chen, Eric},
  title     = {Paper Title},
  booktitle = {Proceedings of the International Conference on Machine Learning},
  pages     = {1234--1245},
  year      = {2021}
}

@book{smith2019,
  author    = {Smith, John},
  title     = {Book Title},
  edition   = {2},
  publisher = {Publisher},
  address   = {City},
  year      = {2019}
}

@misc{vaswani2017,
  author    = {Vaswani, Ashish and others},
  title     = {Attention Is All You Need},
  year      = {2017},
  eprint    = {1706.03762},
  archivePrefix = {arXiv}
}

@online{tensorflow2023,
  author    = {{TensorFlow}},
  title     = {TensorFlow Documentation},
  year      = {2023},
  url       = {https://www.tensorflow.org/}
}
```

### Required Fields by Type

| Entry Type | Required Fields |
|------------|-----------------|
| @article | author, title, journal, year |
| @inproceedings | author, title, booktitle, year |
| @book | author, title, publisher, year |
| @misc | author, title, year |
| @phdthesis | author, title, school, year |

## ML/AI Conference Style Preferences

### Major Venues

| Venue | Style | Notes |
|-------|-------|-------|
| NeurIPS | BibTeX | LaTeX template provided |
| ICML | BibTeX | Author-year in-text |
| ICLR | BibTeX | Open review format |
| CVPR | IEEE-like | Numbered citations |
| ACL | ACL style | Custom BibTeX style |
| EMNLP | ACL style | Same as ACL |
| AAAI | AAAI style | Numbered citations |
| JMLR | MLA-like | Author-year |

### Conference-Specific Formatting

**NeurIPS:**
```latex
\usepackage{neurips_2023}

% Citation style
\cite{vaswani2017}  % produces [Vaswani et al., 2017]
```

**ICML:**
```latex
\usepackage{icml2024}

% Citation style
\cite{vaswani2017}  % produces (Vaswani et al., 2017)
```

## Citation Best Practices

### What to Cite

| Cite | Don't Cite |
|------|------------|
| Direct quotes | Common knowledge |
| Paraphrased ideas | Your own prior work (unless published) |
| Methods from others | Facts in public domain |
| Data sources | General concepts |
| Code/software | Your unpublished thoughts |

### Number of Sources

| Document Type | Typical Citations |
|---------------|-------------------|
| Conference paper | 20-40 |
| Journal article | 30-60 |
| Survey paper | 100+ |
| PhD thesis | 200+ |

### Citing Software and Data

**Software:**
```
We used PyTorch 2.0 [Paszke et al., 2019] for model implementation.
```

**Dataset:**
```
We evaluated on ImageNet [Deng et al., 2009], containing 1.2M images.
```

**Code repository:**
```
Our implementation is based on the Hugging Face Transformers library
[Wolf et al., 2020], available at https://github.com/huggingface/transformers.
```

## Common Errors

### IEEE

| Error | Correction |
|-------|------------|
| [Smith, 2020] | [1] (use numbers) |
| pp. in volume | vol. 10, no. 2, pp. 100-115 |
| Missing year | Always include year |

### ACM

| Error | Correction |
|-------|------------|
| [1] | [Smith 2020] (author-year) |
| pp. 100-115 | 100–115 (en-dash) |
| Vol. 10 | 10 (no "vol.") |

### APA

| Error | Correction |
|-------|------------|
| Smith, A., Jones, B. | Smith, A., & Jones, B. (ampersand in refs) |
| (Smith 2020) | (Smith, 2020) (comma before year) |
| pp. 100-115 | 100–115 (no "pp." in journals) |

## Citation Management Tools

| Tool | Best For | Format Support |
|------|----------|----------------|
| Zotero | Free, browser integration | All major styles |
| Mendeley | PDF management | All major styles |
| BibDesk (Mac) | BibTeX focus | BibTeX |
| JabRef | BibTeX focus | BibTeX |
| EndNote | Institution use | All major styles |

### BibTeX Management Workflow

```bash
# Organize by year
.bib
├── 2020.bib
├── 2021.bib
├── 2022.bib
└── 2023.bib

# Use citation keys consistently
authorYYYY_firstword  # smith2020_attention
```

## Quick Reference Card

| Element | IEEE | ACM | APA |
|---------|------|-----|-----|
| In-text | [1] | [Smith 2020] | (Smith, 2020) |
| Authors | A. Smith | Smith, A. | Smith, A. |
| Year | After title | After author | After author |
| Journal | Italic | Roman | Italic |
| Volume | Italic | Roman | Italic |
| Pages | 100-115 | 100–115 | 100–115 |
| DOI | Optional | DOI: | https://doi.org/ |

## References

- IEEE Citation Reference: ieeeauthorcenter.ieee.org
- ACM Style Guide: acm.org/publications/authors/reference-formatting
- APA Style: apastyle.apa.org
- MLA Handbook: mla.org