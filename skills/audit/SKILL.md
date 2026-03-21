---
name: airesearchorchestrator:audit
agent: orchestrator
description: Generic audit and quality review skill for any research deliverable. Adapts evaluation focus to the specific phase, deliverable type, and quality dimensions relevant to the artifact being reviewed. Use when user says "audit", "review", "quality check", "审核", or any phase-specific audit is needed.
user-invocable: false
argument-hint: [deliverable-path] [--phase survey|pilot|experiments|paper|reflection]
allowed-tools: Bash(curl, python, sympy), Read, Write, Edit, Grep, Glob, WebFetch
---
# Audit

## Overview

A unified audit and quality review skill that systematically evaluates any research deliverable against quality criteria appropriate to its phase and type. This skill replaces phase-specific audit skills with a flexible, adaptive methodology.

## Purpose

Critically review research artifacts for quality, correctness, completeness, and scientific rigor. The agent adapts its evaluation focus based on the deliverable being reviewed, consulting `references/gate-rubrics.md` for detailed scoring rubrics and `references/reporting_standards.md` for applicable reporting standards.

## General Audit Methodology

Every audit follows a consistent high-level process, regardless of the specific deliverable:

### Step 1: Identify the Deliverable and Phase

Determine what is being audited and which phase it belongs to. This determines which quality dimensions to prioritize.

### Step 2: Apply the 7-Stage Review Framework

Work through each stage, adapting the specific checks to the deliverable type:

#### Stage 1: Initial Assessment
- Does the deliverable meet its structural requirements?
- Are all required sections/components present?
- Is the scope clearly defined?
- Are objectives and success criteria stated?

#### Stage 2: Detailed Content Review
- Is each section complete and coherent?
- Does the content address its stated objectives?
- Are claims properly supported?
- Is the logical flow sound?

#### Stage 3: Methodological Rigor
- Is the methodology appropriate for the task?
- Are assumptions stated and justified?
- Is the approach reproducible?
- Are controls, baselines, or comparisons adequate?

#### Stage 4: Reproducibility Check
- Are all artifacts (code, data, configs, seeds) documented?
- Can the work be reproduced from the documentation alone?
- Are environment specifications complete?
- Calculate a reproducibility score: (documented items / required items) * 10

#### Stage 5: Presentation Quality
- Are figures, tables, and visualizations clear and properly labeled?
- Do error bars, captions, and legends meet standards?
- Is data presented accurately and without distortion?

#### Stage 6: Ethics and Integrity
- Are data usage rights, privacy, and consent addressed?
- Are conflicts of interest disclosed?
- Are limitations honestly reported?
- Are potential harms considered?

#### Stage 7: Writing and Communication Quality
- Is the writing clear, concise, and well-organized?
- Is terminology consistent?
- Are all claims supported by evidence?
- Is there any placeholder text (TODO, FIXME)?

### Step 3: Apply Phase-Specific Quality Dimensions

Consult the relevant section below for additional quality dimensions specific to the deliverable's phase.

### Step 4: Evaluate Statistical Rigor (when applicable)

For any deliverable containing quantitative claims:

- **Sample Size Adequacy**: Power analysis documented? Minimum runs met (>= 3)?
- **Test Selection**: Are statistical tests appropriate for the data type and design?
- **Multiple Comparisons**: Are corrections applied (Bonferroni, FDR, Holm)?
- **Effect Size Reporting**: Are effect sizes reported with confidence intervals?
- **P-value Interpretation**: Are exact p-values given? Is practical significance distinguished from statistical significance?

### Step 5: Verify Citations (when applicable)

For any deliverable containing references:

- Verify each citation via academic APIs (Semantic Scholar, arXiv, CrossRef, DBLP)
- Check DOI validity and metadata accuracy
- Flag potential fabrications (papers not found in any database)
- Verify that claims accurately reflect cited content
- Check attribution to original sources

### Step 6: Produce Audit Report

Generate a structured report with verdict and actionable recommendations.

---

## Phase-Specific Quality Dimensions

Adapt your evaluation focus to the specific deliverable being reviewed. These are reference sections, not rigid checklists -- use professional judgment to determine which dimensions are relevant.

### Survey Phase

**Key deliverables**: Literature survey report, research readiness report, ideation reports, novelty assessments, idea definitions, theoretical derivations.

**Priority dimensions**:
- **Literature Coverage**: Minimum 10 papers, recency (last 2-3 years priority), seminal papers included, competing approaches covered, geographic/institutional diversity
- **Search Methodology**: Databases documented, search queries reproducible, inclusion/exclusion criteria explicit, PRISMA guidelines followed if systematic
- **Citation Authenticity**: Every citation verified via academic APIs, fabrication risk assessed, claims match cited content
- **Novelty Claims**: Supported by gap analysis, similar/concurrent works acknowledged, differentiation clear, contribution size appropriate
- **Problem Definition**: Hypothesis testable, success criteria clear, scope appropriate, assumptions explicit
- **Theoretical Rigor** (for derivations): Mathematical formalization correct, theorem statements precise (quantifiers, bound variables, conditions), proofs valid (no circular reasoning, all cases covered), assumptions justified and realistic, complexity analysis verified, conjectures plausible with evidence
- **Experiment Mapping** (for derivations): Predictions testable, critical experiments identified, boundary conditions covered

### Pilot Phase

**Key deliverables**: Problem validation report, problem analysis, pilot design, pilot results/validation report.

**Priority dimensions**:
- **Problem Validation**: Evidence from multiple sources (literature + practical/data), significance scores justified, gap clearly articulated, verdict follows from analysis
- **Problem Decomposition**: All sub-problems identified, dependencies mapped, assumptions reasonable, at least 3 technical challenges identified
- **Solution Approach**: Addresses all challenges, technically sound, implementation feasible, integration points clear
- **Pilot Scope**: Tests core hypothesis directly, minimal but sufficient, completable in < 24 hours, success/failure determinable
- **Success Criteria**: Measurable, Go/No-Go thresholds clear, no ambiguous conditions, early stopping defined
- **Resource Estimates**: Time estimates realistic, GPU requirements appropriate, debugging buffer included (minimum 20%)
- **Hypothesis Validation**: Results match success criteria, claims supported by data, negative results reported honestly
- **Decision Support**: Go/No-Go recommendation supported by data, lessons learned actionable, next steps appropriate

### Experiments Phase

**Key deliverables**: Experiment specification, results summary, evidence package.

**Priority dimensions**:
- **Experiment Matrix**: Main experiments test core claims, ablation studies cover key components, baselines include strong and weak, sensitivity analysis appropriate
- **Statistical Validity**: Sufficient seeds (minimum 3), appropriate statistical tests, significance thresholds defined, multiple comparison corrections applied
- **Hyperparameter Design**: Search spaces appropriate, sampling strategy sound, computational budget feasible
- **Traceability**: All results have run IDs, configs logged, checkpoints exist, logs accessible
- **Baseline Comparisons**: Properly implemented, fair comparison conditions, reported accurately, statistical tests applied
- **Negative Results**: All experiments reported, negative results not hidden, failure analysis included
- **Resource Adequacy**: GPU hours realistic, timeline includes buffer (minimum 20%), storage adequate

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

1. **Be systematic**: Follow the 7-stage review framework for every audit
2. **Be constructive**: Identify issues AND provide specific, actionable recommendations
3. **Be evidence-based**: Support all assessments with specific evidence from the material
4. **Be proportionate**: Focus depth on high-risk areas relevant to the phase
5. **Distinguish severity**: Clearly separate critical, major, and minor issues
6. **Consult references**: Use `references/gate-rubrics.md` for scoring, `references/reporting_standards.md` for applicable standards
7. **Adapt flexibly**: Use the phase-specific dimensions as guidance, not a rigid checklist -- focus on what matters for the specific deliverable
8. **Gate strictly**: Block advancement when critical issues exist
9. **Verify citations**: Use academic APIs (Semantic Scholar, arXiv, CrossRef, DBLP), NOT web search
10. **Reproducibility minimum**: Score must be >= 7/10 to pass
11. **Be fair**: Acknowledge strengths, not just problems
12. **Know limits**: If uncertain about a proof step or claim, flag for expert review

## Blocking Conditions

Automatically BLOCK when:
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
- `references/literature-verification.md` - Citation verification standards
- `references/citation-authenticity.md` - Paper phase citation rules
- `references/experiment-integrity.md` - Experiment logging standards
