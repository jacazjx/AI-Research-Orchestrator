# Paper Quality Assurance Protocol

This document defines the standards and procedures for ensuring paper quality, content authenticity, and venue-readiness.

## Venue Standards

### Top-Tier Conference Criteria

| Venue | Acceptance Criteria | Typical Bar |
|-------|---------------------|-------------|
| CVPR | Novelty + Visual Evidence | Top 25% |
| NeurIPS | Novelty + Theory/Empirical | Top 20% |
| ICLR | Novelty + Reproducibility | Top 30% |
| ACL | Novelty + Linguistic Insight | Top 25% |
| SIGIR | Novelty + IR Relevance | Top 20% |

### Top-Tier Journal Criteria

| Venue | Acceptance Criteria | Typical Bar |
|-------|---------------------|-------------|
| TPAMI | Depth + Impact | ~15% |
| JMLR | Theory + Rigor | ~20% |
| TACL | NLP Depth + Clarity | ~20% |
| Nature/Science | Impact + Broad Interest | <10% |

## Quality Dimensions

### 1. Novelty Assessment

#### Types of Novelty

| Type | Description | Evidence Required |
|------|-------------|-------------------|
| Problem Novelty | New problem formulation | Problem not addressed before |
| Method Novelty | New algorithm/architecture | Technical innovation |
| Theoretical Novelty | New insight/proposition | Mathematical contribution |
| Empirical Novelty | New experimental findings | Novel results |

#### Novelty Verification

1. **Prior Art Search**
   - Query multiple databases
   - Search related work sections of similar papers
   - Check recent conference proceedings

2. **Differentiation Documentation**
   - List 3-5 most similar works
   - Identify specific technical differences
   - Quantify improvement where possible

3. **Novelty Statement Template**
   ```
   Our approach differs from [Prior Work] in the following ways:
   1. [Specific difference 1]
   2. [Specific difference 2]
   3. [Specific difference 3]

   This enables [new capability] that prior work could not achieve.
   ```

### 2. Evidence Strength

#### Experimental Rigor Checklist

- [ ] Clear hypothesis stated
- [ ] Appropriate evaluation metrics
- [ ] Statistical significance reported
- [ ] Multiple runs for variance
- [ ] Ablation studies included
- [ ] Baselines properly implemented

#### Statistical Reporting Requirements

| Metric | Required |
|--------|----------|
| Mean | Yes |
| Standard deviation | Yes |
| Confidence interval | Recommended |
| p-value | For comparisons |
| Effect size | Recommended |

#### Baseline Fairness Guidelines

1. **Implementation**
   - Use official code when available
   - Use recommended hyperparameters
   - Apply same preprocessing

2. **Comparison**
   - Same train/val/test splits
   - Same evaluation protocol
   - Same compute constraints

3. **Reporting**
   - Report best baseline results
   - Document tuning effort
   - Acknowledge baseline advantages

### 3. Theoretical Foundation

#### Correctness Checks

1. **Equations**
   - All variables defined
   - Notation consistent
   - Derivations correct

2. **Assumptions**
   - Clearly stated
   - Justified where possible
   - Limitations acknowledged

3. **Claims**
   - Precise wording
   - Scope limited to evidence
   - No over-claiming

#### Limitations Section

A good limitations section:

```markdown
## Limitations

1. **[Limitation 1]**: [Description]
   - Impact: [How this affects applicability]
   - Mitigation: [Possible future solutions]

2. **[Limitation 2]**: [Description]
   - Impact: [How this affects applicability]
   - Mitigation: [Possible future solutions]
```

### 4. Writing Quality

#### Section Quality Standards

| Section | Key Requirements |
|---------|-----------------|
| Abstract | 150-250 words, covers problem, approach, results, impact |
| Introduction | Clear motivation, contributions listed |
| Related Work | Comprehensive, fair, differentiated |
| Method | Complete, reproducible, well-illustrated |
| Experiments | Complete setup, all details |
| Conclusion | Summary + limitations + future work |

#### Figure and Table Standards

**Figures:**
- Resolution: 300 DPI minimum
- Format: Vector (PDF/EPS) preferred
- Labels: Readable at printed size
- Captions: Self-contained explanation

**Tables:**
- Format: Consistent across paper
- Units: Specified for all numbers
- Significant figures: Appropriate (2-3)
- Captions: Self-contained explanation

#### Citation Standards

| Citation Type | Quality Bar |
|--------------|-------------|
| Method claim | Peer-reviewed source |
| SOTA claim | Recent top-venue paper |
| Dataset | Original source |
| Baseline | Original paper |

## Content Authenticity

### Evidence-to-Claim Mapping

For each claim in the manuscript:

```markdown
### Claim: "[exact quote from paper]"

**Evidence Source:**
- Document: [filename]
- Section: [section]
- Data: [specific numbers]

**Verification Status:** [Verified/Partial/Unsupported]

**Notes:** [any discrepancies]
```

### Authenticity Audit Process

1. **Extract Claims**
   - Identify all claims in manuscript
   - Note location (section, page, line)

2. **Map to Evidence**
   - Find supporting evidence
   - Check consistency
   - Note gaps

3. **Report Issues**
   - Unsupported claims
   - Exaggerated claims
   - Missing evidence

### Fabrication Prevention

| Red Flag | Detection Method |
|----------|-----------------|
| Numbers not in logs | Cross-check with evidence package |
| Citations to non-existent papers | DOI/Scholar verification |
| Perfect results | Statistical plausibility check |
| Missing experiments | Compare to experiment plan |

## Citation Audit

### Verification Process

1. **DOI Check**
   ```
   https://doi.org/[DOI]
   → Should redirect to publisher page
   ```

2. **Source Check**
   - DBLP for CS papers
   - Semantic Scholar for AI/ML
   - Google Scholar for general

3. **Content Check**
   - Does cited paper make the claimed claim?
   - Is citation context accurate?
   - Is there a better citation?

### Citation Quality Scoring

| Grade | Criteria | Action |
|-------|----------|--------|
| A | DOI-verified, peer-reviewed | Accept |
| B | Trusted source, no DOI | Accept |
| C | arXiv preprint | Flag for update |
| D | Unverified source | Require manual check |
| F | Cannot verify | Remove or flag |

## Review Protocol

### Review Dimensions

| Dimension | Weight | Focus Areas |
|-----------|--------|-------------|
| Novelty | 25% | Problem, method, theory, empirical |
| Evidence | 30% | Rigor, statistics, baselines, reproducibility |
| Theory | 15% | Grounding, correctness, limitations |
| Analysis | 15% | Depth, discussion, future work |
| Writing | 15% | Clarity, structure, presentation |

### Review Template

```markdown
# Manuscript Review

## Decision: [Accept / Minor Revision / Major Revision / Reject]

## Summary
[Brief overall assessment]

## Strengths
1. [Specific strength]
2. [Specific strength]

## Weaknesses
1. [Specific weakness with location]

## Detailed Scores

| Dimension | Score | Comments |
|-----------|-------|----------|
| Novelty | [1-5] | [comments] |
| Evidence | [1-5] | [comments] |
| Theory | [1-5] | [comments] |
| Analysis | [1-5] | [comments] |
| Writing | [1-5] | [comments] |

## Blocking Issues
[List issues that prevent acceptance]

## Recommendations
[List specific, actionable recommendations]
```

## Gate Criteria

### Gate 4 Requirements

| Requirement | Status |
|-------------|--------|
| Manuscript complete | [ ] |
| Citation audit passed | [ ] |
| Content authenticity verified | [ ] |
| Venue formatting compliant | [ ] |
| Score ≥ 4.0 average | [ ] |
| No blocking issues | [ ] |

### Final Acceptance

Before Gate 4 approval:

1. Run citation audit: `python3 scripts/run_citation_audit.py --verify`
2. Verify content authenticity: Check all claims mapped to evidence
3. Check venue compliance: Format, length, required sections
4. Final review: No blocking issues, score ≥ 4.0