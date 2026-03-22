# Venue Requirements Reference

Formatting, submission, and checklist requirements for major ML/AI publication venues.
Use this document to ensure manuscripts meet venue-specific standards before submission.

---

## NeurIPS (Conference on Neural Information Processing Systems)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 9 pages (main content), unlimited appendix |
| **Format** | NeurIPS LaTeX template (`neurips_2025.sty`) |
| **Blind review** | Double-blind |
| **Checklist** | Paper Checklist required (ethics, reproducibility, limitations) |
| **Key dates** | Usually May submission, December conference |
| **Supplementary** | Separate PDF; code submission encouraged |
| **Abstract limit** | ~250 words (no strict hard limit, but keep concise) |

### NeurIPS-Specific Notes

- The Paper Checklist is **mandatory** and reviewed by area chairs. It covers:
  - Claims and evidence alignment
  - Limitations discussion
  - Societal impact statement
  - Reproducibility (code, data, hyperparameters)
  - Computational budget disclosure
- Supplementary material must be a single ZIP containing a PDF and optional code.
- Do not include author names, affiliations, or acknowledgments in the submitted version.

### Common Rejection Reasons

- Insufficient or unconvincing experiments (weak baselines, missing error bars)
- Overclaiming: claims not supported by the evidence presented
- Poor writing quality or unclear exposition of the main contribution
- Missing or superficial limitations discussion
- Novelty concerns: too incremental over existing work

---

## ICML (International Conference on Machine Learning)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 8 pages (main content) + unlimited references and appendix |
| **Format** | ICML LaTeX template |
| **Blind review** | Double-blind |
| **Checklist** | Reproducibility checklist required |
| **Key dates** | Usually January/February submission, July conference |
| **Supplementary** | Appendix in same PDF; code optional but encouraged |
| **Abstract limit** | ~200 words |

### ICML-Specific Notes

- The appendix follows the references in the same PDF file.
- Reviewers are not obligated to read the appendix; the main paper must be self-contained.
- The reproducibility checklist must be completed and included at the end of the paper.
- Impact statement is required (after the conclusion, before references).

### Common Rejection Reasons

- Weak baselines: comparisons against outdated or easy-to-beat methods
- Missing ablation studies: not isolating the contribution of each component
- Unclear contribution: difficulty identifying what is new versus prior work
- Theoretical claims without sufficient proof or experimental validation
- Presentation issues: dense notation without intuition, overly long proofs in main text

---

## ICLR (International Conference on Learning Representations)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 9 pages (main content), unlimited appendix |
| **Format** | ICLR LaTeX template (OpenReview-based) |
| **Blind review** | Double-blind; open review process (reviews publicly visible) |
| **Checklist** | Reproducibility statement required |
| **Key dates** | Usually September/October submission, May conference |
| **Supplementary** | Appendix in main PDF |
| **Abstract limit** | ~250 words |

### ICLR-Specific Notes

- Reviews, author responses, and meta-reviews are publicly visible on OpenReview.
- The open review process means the community can also comment on submissions.
- A reproducibility statement is required and should appear after the conclusion.
- Ethics review may be triggered if the paper touches sensitive topics.
- Code submission via OpenReview is supported and encouraged.

### Common Rejection Reasons

- Incremental contribution: not enough novelty over existing methods
- Missing related work: failing to position the work within the current landscape
- Poor experimental design: inappropriate datasets, missing standard benchmarks
- Lack of analysis: results reported without insight into why the method works
- Reproducibility concerns: insufficient detail to replicate results

---

## ACL / EMNLP / NAACL (Association for Computational Linguistics venues)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 8 pages (long paper), 4 pages (short paper) + unlimited references |
| **Format** | ACL LaTeX template (`acl2024.sty` or current year equivalent) |
| **Blind review** | Double-blind; ACL Rolling Review (ARR) system |
| **Checklist** | Responsible NLP Research checklist |
| **Key dates** | Varies by venue; ARR has monthly submission deadlines |
| **Supplementary** | Separate appendix; code encouraged |
| **Abstract limit** | ~200 words |

### ACL-Specific Notes

- The ACL Rolling Review (ARR) system allows submissions any month, with reviews reusable across ACL, EMNLP, NAACL, and other *ACL venues.
- A **Limitations** section is **mandatory** and does not count toward the page limit.
- An **Ethics/Broader Impact** section is required for relevant work.
- The Responsible NLP Research checklist covers reproducibility, data documentation, and human evaluation protocols.
- Short papers (4 pages) are for focused contributions, negative results, or opinion pieces.
- Appendices are submitted as separate supplementary material, not in the main PDF.

### Common Rejection Reasons

- Missing or inadequate Limitations section
- Insufficient analysis of model behavior (error analysis, qualitative examples)
- Evaluation on English-only datasets without acknowledging multilingual limitations
- Comparisons missing recent strong baselines (field moves quickly)
- Human evaluation without proper inter-annotator agreement reporting

---

## AAAI (Association for the Advancement of Artificial Intelligence)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 7 pages (main content) + 1 page references + 1 page ethics statement |
| **Format** | AAAI LaTeX template (`aaai25.sty` or current year equivalent) |
| **Blind review** | Double-blind |
| **Checklist** | Ethics statement required |
| **Key dates** | Usually August submission, February conference |
| **Supplementary** | Up to 5-page supplementary PDF allowed |
| **Abstract limit** | ~150 words |

### AAAI-Specific Notes

- The 7+1+1 page structure is strict: 7 pages of content, 1 page for references only, 1 page for the required ethics statement.
- The ethics statement is mandatory even if no ethical concerns arise (state that explicitly).
- Supplementary material is limited to 5 pages and must be a single PDF.
- AAAI covers a broader range of AI topics than ML-focused venues; position the contribution accordingly.
- Two-column format is used (unlike NeurIPS/ICML/ICLR single-column).

### Common Rejection Reasons

- Page limit violations (strict enforcement)
- Mismatch between the paper's focus and AAAI's broader AI scope
- Ethics statement missing or insufficiently detailed
- Experimental evaluation too narrow (single dataset, single metric)
- Writing quality: grammar, clarity, and organization issues

---

## CVPR / ICCV / ECCV (Computer Vision venues)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 8 pages (main content) + unlimited references |
| **Format** | CVPR/ICCV/ECCV LaTeX template (venue-specific) |
| **Blind review** | Double-blind |
| **Checklist** | Reproducibility checklist |
| **Key dates** | CVPR: ~November submission, June conference; ICCV/ECCV alternate years |
| **Supplementary** | Separate PDF + video allowed |
| **Abstract limit** | ~200 words |

### CV Venue-Specific Notes

- Supplementary material can include both a PDF and a video demonstration.
- Video supplements are common and valued for visual results (demos, qualitative comparisons).
- Two-column format is standard across all three venues.
- References do not count toward the page limit.
- ECCV uses a slightly different template than CVPR/ICCV; verify the correct one.
- Qualitative results (visual comparisons) are expected alongside quantitative metrics.

### Common Rejection Reasons

- Missing visual comparisons: tables alone are insufficient for vision papers
- Evaluation on outdated benchmarks without current state-of-the-art comparisons
- Insufficient ablation of architectural choices
- Poor figure quality (low resolution, hard to read at print size)
- Reproducibility: missing implementation details (learning rate, augmentation, etc.)

---

## COLM (Conference on Language Modeling)

| Attribute | Requirement |
|-----------|-------------|
| **Page limit** | 9 pages (main content) + unlimited appendix |
| **Format** | Based on NeurIPS template |
| **Blind review** | Double-blind |
| **Key dates** | New venue; check the official website for current deadlines |
| **Focus** | Language modeling specifically |
| **Abstract limit** | ~250 words |

### COLM-Specific Notes

- COLM is a newer venue specifically focused on language modeling research.
- The template is based on the NeurIPS format; verify any COLM-specific modifications.
- Given the venue's focus, papers should clearly connect their contribution to language modeling even if the technique is general.
- Check the official COLM website for the most current requirements, as standards may evolve.

---

## General Pre-Submission Checklist

This checklist applies to all venues. Complete every item before submitting.

### Compilation and Formatting

1. Paper compiles without errors using the venue's expected toolchain (pdflatex/xelatex/lualatex)
2. Page count is within the venue's limit, including all figures and tables in the main text
3. All figures are readable at print resolution (300 DPI minimum for raster images; prefer vector PDF)
4. All tables fit within column and page margins with no overflow
5. References are complete (no "?" marks) and formatted consistently per venue style

### Anonymization (Double-Blind Compliance)

6. Author names and affiliations removed from the manuscript
7. No identifying information in PDF metadata (check with `pdfinfo` or `exiftool`)
8. Acknowledgments section removed or replaced with "Removed for review"
9. Self-citations written in third person ("Smith et al. [42] showed..." not "We previously showed [42]...")
10. Code and data links anonymized (use anonymous GitHub repos, Anonymous FTP, or anonymous file sharing)

### Content Completeness

11. Venue-specific checklist filled out completely and included in the submission
12. All TODO, FIXME, and placeholder markers removed from the text
13. Abstract is within the venue's word limit (typically 150-250 words)
14. Keywords and subject areas selected (if required by the submission system)
15. Supplementary material is properly referenced from the main text where relevant

### Final Verification

16. Submission file is in the correct format (PDF) and within the venue's file size limit
17. All co-authors have reviewed and approved the manuscript
18. The contribution statement is clear: reader can identify what is new in 30 seconds
19. Limitations are discussed honestly (required by most venues, valued by all)
20. Reproducibility information is sufficient: hyperparameters, compute budget, random seeds
