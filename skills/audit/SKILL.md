---
name: airesearchorchestrator:audit
agent: orchestrator
description: Generic audit and quality review skill for any research deliverable. Adapts evaluation focus to the specific phase, deliverable type, and quality dimensions relevant to the artifact being reviewed. Use when user says "audit", "review", "quality check", "审核", or any phase-specific audit is needed.
user-invocable: false
argument-hint: [deliverable-path] [--phase survey|pilot|experiments|paper|reflection]
allowed-tools: Bash(curl, python, sympy), Read, Write, Edit, Grep, Glob, WebFetch
---
# Audit

This framework is a reference guide, not a rigid checklist. The auditor adapts depth and focus to the specific deliverable, its phase, and what matters most for quality.

## Overview

A unified audit and quality review skill that evaluates any research deliverable against quality criteria appropriate to its phase and type.

## Purpose

Critically review research artifacts for quality, correctness, completeness, and scientific rigor. The agent adapts its evaluation focus based on the deliverable being reviewed, consulting `references/gate-rubrics.md` for detailed scoring rubrics and `references/reporting_standards.md` for applicable reporting standards.

## 7-Stage Review Framework

This is a thinking framework, not a mandatory sequential procedure. Use professional judgment to determine which stages warrant deep scrutiny for a given deliverable.

### Stage 1: Initial Assessment
- Does the deliverable meet its structural requirements?
- Are required sections/components present?
- Is the scope clearly defined?
- Are objectives and success criteria stated?

### Stage 2: Detailed Content Review
- Is each section complete and coherent?
- Does the content address its stated objectives?
- Are claims properly supported?
- Is the logical flow sound?

### Stage 3: Methodological Rigor
- Is the methodology appropriate for the task?
- Are assumptions stated and justified?
- Is the approach reproducible?
- Are controls, baselines, or comparisons adequate?

### Stage 4: Reproducibility Check
- Are all artifacts (code, data, configs, seeds) documented?
- Can the work be reproduced from the documentation alone?
- Are environment specifications complete?
- Calculate a reproducibility score: (documented items / required items) * 10

### Stage 5: Presentation Quality
- Are figures, tables, and visualizations clear and properly labeled?
- Do error bars, captions, and legends meet standards?
- Is data presented accurately and without distortion?

### Stage 6: Ethics and Integrity
- Are data usage rights, privacy, and consent addressed?
- Are conflicts of interest disclosed?
- Are limitations honestly reported?
- Are potential harms considered?

### Stage 7: Writing and Communication Quality
- Is the writing clear, concise, and well-organized?
- Is terminology consistent?
- Are all claims supported by evidence?
- Is there any placeholder text (TODO, FIXME)?

---

## Statistical Rigor (when applicable)

For any deliverable containing quantitative claims, consider evaluating:

- **Sample Size Adequacy**: Power analysis documented? Sufficient runs (typically 3+)?
- **Test Selection**: Are statistical tests appropriate for the data type and design?
- **Multiple Comparisons**: Are corrections applied (Bonferroni, FDR, Holm) where needed?
- **Effect Size Reporting**: Are effect sizes reported with confidence intervals?
- **P-value Interpretation**: Are exact p-values given? Is practical significance distinguished from statistical significance?

## Citation Verification (when applicable)

For verification sources, grades, and workflow, see `references/citation-standards.md` (Citation Verification Methodology section).

For any deliverable containing references:

- Verify citations via academic APIs (Semantic Scholar, arXiv, CrossRef, DBLP), not web search
- Check DOI validity and metadata accuracy
- Flag potential fabrications (papers not found in any database)
- Verify that claims accurately reflect cited content
- Check attribution to original sources

---

## Phase-Specific Quality Dimensions

Adapt evaluation focus to the deliverable being reviewed. These are reference sections -- use professional judgment to determine which dimensions are relevant.

### Survey Phase

**Key deliverables**: Literature survey report, research readiness report, ideation reports, novelty assessments, idea definitions, theoretical derivations.

**Priority dimensions**:
- **Literature Coverage**: Aim for sufficient coverage (typically 10+ papers), recency (last 2-3 years priority), seminal papers included, competing approaches covered, geographic/institutional diversity
- **Search Methodology**: Databases documented, search queries reproducible, inclusion/exclusion criteria explicit, PRISMA guidelines followed if systematic
- **Citation Authenticity**: Verify citations via academic APIs to the extent feasible, assess fabrication risk, check that claims match cited content
- **Novelty Claims**: Supported by gap analysis, similar/concurrent works acknowledged, differentiation clear, contribution size appropriate
- **Problem Definition**: Hypothesis testable, success criteria clear, scope appropriate, assumptions explicit
- **Theoretical Rigor** (for derivations): Mathematical formalization correct, theorem statements precise, proofs valid, assumptions justified and realistic, complexity analysis verified
- **Experiment Mapping** (for derivations): Predictions testable, critical experiments identified, boundary conditions covered

### Pilot Phase

**Key deliverables**: Problem validation report, problem analysis, pilot design, pilot results/validation report.

**Priority dimensions**:
- **Problem Validation**: Evidence from multiple sources (literature + practical/data), significance scores justified, gap clearly articulated
- **Problem Decomposition**: Sub-problems identified, dependencies mapped, assumptions reasonable, consider covering multiple technical challenges (typically 3+)
- **Solution Approach**: Addresses identified challenges, technically sound, implementation feasible, integration points clear
- **Pilot Scope**: Tests core hypothesis directly, minimal but sufficient, completable in reasonable time, success/failure determinable
- **Success Criteria**: Measurable, Go/No-Go thresholds clear, no ambiguous conditions, early stopping defined
- **Resource Estimates**: Time estimates realistic, GPU requirements appropriate, consider including debugging buffer (typically 20%+)
- **Hypothesis Validation**: Results match success criteria, claims supported by data, negative results reported honestly
- **Decision Support**: Go/No-Go recommendation supported by data, lessons learned actionable, next steps appropriate

### Experiments Phase

**Key deliverables**: Experiment specification, results summary, evidence package.

**Priority dimensions**:
- **Experiment Matrix**: Main experiments test core claims, ablation studies cover key components, baselines include strong and weak, sensitivity analysis appropriate
- **Statistical Validity**: Use multiple seeds (typically 3+), apply appropriate statistical tests, define significance thresholds, apply multiple comparison corrections where needed
- **Hyperparameter Design**: Search spaces appropriate, sampling strategy sound, computational budget feasible
- **Traceability**: Results have run IDs, configs logged, checkpoints exist, logs accessible
- **Baseline Comparisons**: Properly implemented, fair comparison conditions, reported accurately, statistical tests applied
- **Negative Results**: All experiments reported, negative results not hidden, failure analysis included
- **Resource Adequacy**: GPU hours realistic, timeline includes buffer (typically 20%+), storage adequate

### Paper Phase

**Key deliverables**: Paper plan/outline, manuscript draft, citation index, final paper.

**Priority dimensions**:
- **Claim-Evidence Matrix**: Every claim has supporting evidence, evidence mapped to experiments, gaps identified
- **Section Structure**: Logical flow, standard sections present (Abstract, Introduction, Methods, Results, Discussion, Conclusion), appropriate length distribution
- **Figure/Table Plan**: Key figures identified, tables for main results, supporting materials adequate, publication-quality resolution
- **Citation Scaffolding**: Key citations identified per category (foundation, related work, baselines), missing citations noted
- **Scientific Rigor**: Claims match experimental results, numbers verified, no unsupported claims
- **Writing Quality**: Clear language, no AI-typical phrases, appropriate hedging, consistent terminology, no placeholders
- **Reporting Standards Compliance**: CONSORT/PRISMA/STROBE/ARRIVE/CLAIM as applicable (see `references/reporting_standards.md`)
- **Code and Data Availability**: Availability statements present, repository URLs documented

### Reflection Phase

**Key deliverables**: Lessons learned, overlay draft (system improvements), runtime improvement report.

**Priority dimensions**:
- **Lessons Honesty**: Both successes and failures included, root causes identified (not just surface observations), issues not whitewashed
- **Transferability**: Each lesson classified as project-specific vs. general, conditions for applicability stated, transfer methods described
- **Actionability**: Recommendations are concrete (not vague), owners/roles identified, effort estimates provided
- **Overlay Safety** (for system improvements): No changes bypass human gates, no data loss risk, edge cases considered, backward compatibility maintained
- **Rollback Capability**: Rollback procedure documented, no irreversible changes without justification
- **Testing Plan**: Test coverage adequate, edge cases tested, monitoring defined
- **Metrics Completeness**: Duration, resources, experiments, gate passes all documented

---

## Output Format

Adapt the report structure to the deliverable, but always include these sections:

```markdown
# Audit Report: [Deliverable Name]

## Summary
- **Deliverable**: [What was audited]
- **Phase**: [survey/pilot/experiments/paper/reflection]
- **Overall Assessment**: PASS / PASS_WITH_FIXES / REVISE / MAJOR_REVISION / BLOCK
- **7-Stage Score**: X/7 stages passed
- **Reproducibility Score**: X/10 (if applicable)

## 7-Stage Review

| Stage | Passed | Issues |
|-------|--------|--------|
| Initial Assessment | Yes/No | [Issues] |
| Detailed Content Review | Yes/No | [Issues] |
| Methodological Rigor | Yes/No | [Issues] |
| Reproducibility Check | Yes/No | [Issues] |
| Presentation Quality | Yes/No | [Issues] |
| Ethics and Integrity | Yes/No | [Issues] |
| Writing and Communication | Yes/No | [Issues] |

## Phase-Specific Findings

[Detailed findings organized by the relevant quality dimensions for this phase]

## Statistical Evaluation (if applicable)

| Criterion | Met? | Notes |
|-----------|------|-------|
| Sample size adequacy | Yes/No/N/A | |
| Test selection appropriate | Yes/No/N/A | |
| Multiple comparison correction | Yes/No/N/A | |
| Effect sizes reported | Yes/No/N/A | |
| Confidence intervals | Yes/No/N/A | |

## Citation Verification (if applicable)

| Citation | Status | Source | Notes |
|----------|--------|--------|-------|
| [key] | VERIFIED/UNVERIFIED/FABRICATION_RISK | [API] | |

**Verification Rate**: X% (Y/Z citations)
**Fabrication Risk**: LOW / MEDIUM / HIGH

## Critical Issues (Must Fix)

1. **[Issue]**: [Location] -- [What's wrong] -- [Suggested fix]

## Major Issues (Should Fix)

1. **[Issue]**: [Location] -- [What's wrong] -- [Suggested fix]

## Minor Issues (Consider Fixing)

1. **[Issue]**: [Suggested fix]

## Strengths

- [Strength 1]
- [Strength 2]

## Recommendations

1. [Actionable recommendation]
2. [Actionable recommendation]

## Gate Decision

- [ ] PASS - Ready to proceed
- [ ] PASS_WITH_FIXES - Minor issues, fix and proceed
- [ ] REVISE - Significant issues requiring revision
- [ ] MAJOR_REVISION - Fundamental problems, major rework needed
- [ ] BLOCK - Critical issues, do not proceed

### Rationale
[Explanation of gate decision]

### Required Actions Before Proceeding
1. [Action item]
```

## Key Rules

1. **Be systematic**: Use the 7-stage review framework as a thinking guide for every audit
2. **Be constructive**: Identify issues AND provide specific, actionable recommendations
3. **Be evidence-based**: Support all assessments with specific evidence from the material
4. **Be proportionate**: Focus depth on high-risk areas relevant to the phase
5. **Distinguish severity**: Clearly separate critical, major, and minor issues
6. **Consult references**: Use `references/gate-rubrics.md` for scoring, `references/reporting_standards.md` for applicable standards
7. **Adapt flexibly**: Focus on what matters for the specific deliverable
8. **Gate strictly**: Block advancement when critical issues exist
9. **Verify citations**: Use academic APIs (Semantic Scholar, arXiv, CrossRef, DBLP), not web search
10. **Aim for reproducibility**: Target a score of >= 7/10
11. **Be fair**: Acknowledge strengths, not just problems
12. **Know limits**: If uncertain about a proof step or claim, flag for expert review

## Blocking Conditions

These are mandatory -- automatically BLOCK when:
- Citation fabrications detected
- Critical proof gaps undermine theoretical foundations
- Untraceable results with no run IDs or configs
- Negative results are hidden or unreported
- Human gates would be bypassed by proposed changes
- Assumptions are clearly unrealistic without justification
- Placeholders remain in paper manuscript
- Claims are unsupported by experimental evidence

## References

- `references/gate-rubrics.md` - Detailed scoring rubrics for each phase gate
- `references/reporting_standards.md` - CONSORT, PRISMA, STROBE, ARRIVE, CLAIM checklists
- `references/citation-standards.md` - Citation verification standards
- `references/evidence-standards.md` - Experiment logging standards
