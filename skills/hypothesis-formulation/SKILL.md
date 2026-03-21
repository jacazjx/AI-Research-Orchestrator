---
name: airesearchorchestrator:hypothesis-formulation
description: Formulate research hypotheses through systematic 8-stage process including literature synthesis, competing hypothesis generation, and quality evaluation. Use when user says "formulate hypothesis", "generate hypothesis", "构建假设", or needs to develop testable research hypotheses.
user-invocable: false
argument-hint: [research-topic-or-phenomenon]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---
## Purpose

Transform research observations into well-formed, testable hypotheses through a systematic 8-stage process that ensures scientific rigor, falsifiability, and clear experimental predictions.

## Workflow

### Stage 1: Understand the Phenomenon

**Objective**: Clearly define the observation or problem that motivates the research.

**Actions**:
1. Document the phenomenon or observation
2. Identify the core question or puzzle
3. Specify the domain and scope
4. Note any anomalies or unexpected patterns

**Output**: A clear problem statement with:
- Phenomenon description
- Key variables identified
- Boundary conditions
- Initial questions

**Key Questions**:
- What exactly is being observed?
- Why is this interesting or important?
- What is the scope of the investigation?
- What are the boundary conditions?

### Stage 2: Conduct Literature Search

**Objective**: Map existing knowledge and identify gaps.

**Actions**:
1. Search academic databases (Semantic Scholar, arXiv, DBLP, OpenAlex)
2. Identify seminal papers and recent work
3. Note established theories and findings
4. Document contradictory or inconclusive results

**Output**: Literature synthesis including:
- Key theoretical frameworks
- Established findings
- Open questions and gaps
- Conflicting evidence

**Search Strategy**:
```
Primary queries:
- [phenomenon] + theory
- [phenomenon] + mechanism
- [phenomenon] + explanation

Secondary queries:
- [related concepts] + [phenomenon]
- [phenomenon] + limitations
- [phenomenon] + open problems
```

**Key Rules**:
- Use academic APIs, NOT web search
- Include papers from last 2-3 years
- Note seminal papers for theoretical foundations
- Document search queries and results

### Stage 3: Synthesize Existing Evidence

**Objective**: Integrate findings to identify patterns and gaps.

**Actions**:
1. Organize evidence by type (empirical, theoretical, computational)
2. Identify convergent findings
3. Note contradictions and their sources
4. Map the evidence landscape

**Output**: Evidence synthesis table:

| Evidence Type | Finding | Source | Strength | Relevance |
|---------------|---------|--------|----------|-----------|
| Empirical | [finding] | [citation] | Strong/Moderate/Weak | Direct/Indirect |
| Theoretical | [finding] | [citation] | Strong/Moderate/Weak | Direct/Indirect |
| Computational | [finding] | [citation] | Strong/Moderate/Weak | Direct/Indirect |

**Synthesis Questions**:
- What patterns emerge across studies?
- Where do findings converge or diverge?
- What methodological limitations exist?
- What gaps remain unaddressed?

### Stage 4: Generate Competing Hypotheses

**Objective**: Develop 3-5 distinct, competing hypotheses.

**Actions**:
1. Brainstorm multiple explanations
2. Ensure hypotheses are mutually exclusive where possible
3. Include null and alternative hypotheses
4. Consider edge cases and boundary conditions

**Output**: For each hypothesis, document:

```markdown
## Hypothesis H{n}: [Name]

**Statement**: [Clear, testable statement]

**Mechanism**: [Proposed causal mechanism]

**Predictions**: [What would be observed if true]

**Prior Support**: [Existing evidence that supports this]

**Challenges**: [Known issues or contradictions]
```

**Generation Strategies**:
- **Theory-driven**: Derive from established theories
- **Data-driven**: Induce from observed patterns
- **Analogy**: Adapt explanations from related domains
- **Contradiction**: Propose opposite of prevailing view
- **Synthesis**: Combine elements from multiple theories

**Key Rules**:
- Generate at least 3 hypotheses
- Ensure each is independently testable
- Avoid hypotheses that are trivially true
- Include at least one "surprising" hypothesis

### Stage 5: Evaluate Hypothesis Quality

**Objective**: Assess each hypothesis against quality criteria.

**Actions**:
1. Score each hypothesis on quality dimensions
2. Identify strengths and weaknesses
3. Rank hypotheses by overall quality
4. Note gaps in testability

**Output**: Quality assessment matrix:

| Criterion | H1 | H2 | H3 | H4 | H5 |
|-----------|----|----|----|----|----|
| Testability | /5 | /5 | /5 | /5 | /5 |
| Falsifiability | /5 | /5 | /5 | /5 | /5 |
| Parsimony | /5 | /5 | /5 | /5 | /5 |
| Explanatory Power | /5 | /5 | /5 | /5 | /5 |
| Scope | /5 | /5 | /5 | /5 | /5 |
| Consistency | /5 | /5 | /5 | /5 | /5 |
| Novelty | /5 | /5 | /5 | /5 | /5 |
| **Total** | /35 | /35 | /35 | /35 | /35 |

**Scoring Guide** (see `references/hypothesis_quality_criteria.md`):
- 5: Excellent - Fully satisfies criterion
- 4: Good - Mostly satisfies with minor gaps
- 3: Adequate - Satisfies with some limitations
- 2: Weak - Significant limitations
- 1: Poor - Major deficiencies

**Key Rules**:
- Be objective and consistent in scoring
- Document justification for each score
- Consider inter-rater reliability
- Flag hypotheses with critical weaknesses

### Stage 6: Design Experimental Tests

**Objective**: Develop experimental designs to test each hypothesis.

**Actions**:
1. Identify key variables (independent, dependent, control)
2. Design experiments that can falsify each hypothesis
3. Consider practical constraints
4. Plan for confound mitigation

**Output**: For each hypothesis, specify:

```markdown
## Experimental Design for H{n}

**Objective**: [What the experiment tests]

**Independent Variables**:
- IV1: [variable] (levels: [...])
- IV2: [variable] (levels: [...])

**Dependent Variables**:
- DV1: [variable] (measurement: [...])
- DV2: [variable] (measurement: [...])

**Control Variables**:
- [variable]: [how controlled]

**Procedure**:
1. [Step 1]
2. [Step 2]
...

**Sample Size**: [N] (power analysis: [...])

**Expected Outcomes**:
- If H{n} is true: [expected pattern]
- If H{n} is false: [expected pattern]

**Potential Confounds**: [and mitigation strategies]
```

**Design Patterns** (see `references/experimental_design_patterns.md`):
- A/B testing
- Controlled experiments
- Observational studies
- Simulation experiments
- Ablation studies

**Key Rules**:
- Each experiment must be capable of falsifying the hypothesis
- Include appropriate controls
- Consider statistical power
- Address potential confounds

### Stage 7: Formulate Testable Predictions

**Objective**: Derive specific, measurable predictions from each hypothesis.

**Actions**:
1. Extract concrete predictions from each hypothesis
2. Specify measurement methods
3. Define success/failure criteria
4. Identify critical tests that distinguish hypotheses

**Output**: Prediction table:

| Hypothesis | Prediction | Measurement | Success Criterion | Distinguishing? |
|------------|------------|-------------|-------------------|-----------------|
| H1 | [prediction] | [method] | [criterion] | Yes/No |
| H2 | [prediction] | [method] | [criterion] | Yes/No |
| ... | ... | ... | ... | ... |

**Prediction Format**:
```
If [hypothesis] is true, then [specific condition] should lead to
[measurable outcome], measured by [method], with effect size of at
least [threshold].
```

**Critical Tests**:
- Identify predictions that differentiate hypotheses
- Design experiments where hypotheses make opposite predictions
- Prioritize tests with highest information gain

**Key Rules**:
- Predictions must be falsifiable
- Include quantitative predictions where possible
- Specify effect sizes and confidence intervals
- Define clear decision criteria

### Stage 8: Present Structured Output

**Objective**: Compile findings into a comprehensive hypothesis report.

**Actions**:
1. Synthesize all stages into coherent report
2. Generate LaTeX report using template
3. Include all supporting evidence
4. Provide clear recommendations

**Output**: Save to `docs/survey/hypothesis-report.md` and optionally compile LaTeX:

```markdown
# Hypothesis Formulation Report

## Executive Summary
- Research question
- Top-ranked hypothesis
- Key predictions
- Recommended next steps

## 1. Phenomenon Description
[From Stage 1]

## 2. Literature Synthesis
[From Stage 2-3]

## 3. Competing Hypotheses
[From Stage 4]

## 4. Quality Assessment
[From Stage 5]

## 5. Experimental Designs
[From Stage 6]

## 6. Testable Predictions
[From Stage 7]

## 7. Recommendations
- Primary hypothesis to test
- Priority experiments
- Resource requirements
- Timeline estimates

## Appendix A: Detailed Evidence Tables
## Appendix B: Full Experimental Protocols
## Appendix C: Statistical Power Analysis
```

**LaTeX Report** (optional):
Use `assets/hypothesis_report_template.tex` to generate a formatted PDF with:
- Color-coded hypothesis boxes (tcolorbox)
- Quality assessment tables
- Experimental design diagrams
- Prediction matrices

## Key Rules

1. **Academic API Priority**: Use Semantic Scholar, arXiv, DBLP, OpenAlex for literature search - NOT web search
2. **Minimum Hypotheses**: Generate at least 3 competing hypotheses
3. **Falsifiability Requirement**: Every hypothesis must be falsifiable
4. **Evidence-Based**: All claims must be supported by cited evidence
5. **Distinguishing Tests**: Include predictions that differentiate hypotheses
6. **Quality Scoring**: Apply all 7 quality criteria consistently
7. **Structured Output**: Follow the report template format

## Quality Criteria Reference

See `references/hypothesis_quality_criteria.md` for detailed scoring rubrics:

| Criterion | Definition | Key Question |
|-----------|------------|--------------|
| Testability | Can be empirically tested | Is there a feasible experiment? |
| Falsifiability | Can be proven false | What evidence would disprove it? |
| Parsimony | Simplest explanation | Does it avoid unnecessary complexity? |
| Explanatory Power | Explains observations | How much does it explain? |
| Scope | Generalizability | How widely does it apply? |
| Consistency | Aligns with known facts | Does it contradict established findings? |
| Novelty | New insight | Does it advance understanding? |

## Experimental Design Reference

See `references/experimental_design_patterns.md` for design patterns:

- **Controlled Experiments**: Randomized, with control group
- **A/B Testing**: Compare two conditions
- **Observational Studies**: Natural variation analysis
- **Simulation Experiments**: Computational validation
- **Ablation Studies**: Component isolation

## Integration with Research Pipeline

This skill integrates with:
- **literature**: Uses literature search results
- **problem-analysis**: Provides hypothesis for problem analysis
- **audit**: Quality gate for hypothesis quality
- **experiment-design**: Receives hypotheses for experiment design

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Hypothesis Report | `docs/survey/hypothesis-report.md` | Main output |
| LaTeX Report | `docs/survey/hypothesis-report.tex` | Formatted PDF |
| Evidence Tables | `docs/survey/evidence-synthesis.md` | Supporting data |
| Prediction Matrix | `docs/survey/prediction-matrix.md` | Testable predictions |