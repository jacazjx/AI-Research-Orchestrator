# Skills Directory

This directory contains 60 specialized skills for the AI Research Orchestrator. Each skill is a self-contained capability that can be invoked via slash commands or by other skills.

## Quick Navigation

- [Main Workflow Skills](#main-workflow-skills) - End-to-end research pipelines
- [Survey Phase Skills](#survey-phase-skills) - Literature review and idea formulation
- [Pilot Phase Skills](#pilot-phase-skills) - Small-scale validation
- [Experiments Phase Skills](#experiments-phase-skills) - Full experiment execution
- [Paper Phase Skills](#paper-phase-skills) - Manuscript writing and compilation
- [Reflection Phase Skills](#reflection-phase-skills) - Lessons extraction and improvement
- [Audit Skills](#audit-skills) - Quality gate reviews
- [Agent Skills](#agent-skills) - Primary and reviewer agents for each phase
- [Tool Skills](#tool-skills) - Utility capabilities

---

## Main Workflow Skills

End-to-end pipelines that orchestrate multiple sub-skills into complete research workflows.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [orchestrator](./orchestrator/) | Main five-phase research project orchestrator (Survey → Pilot → Experiments → Paper → Reflection) | "start research project", "research workflow", "five-phase research" |
| [idea-discovery](./idea-discovery/) | Workflow 1: Full idea discovery pipeline (research-lit → idea-creator → novelty-check → research-review) | "find ideas", "idea discovery pipeline", "from zero to validated ideas" |
| [research-pipeline](./research-pipeline/) | Full research pipeline: idea discovery → implementation → auto review loop | "full pipeline", "end-to-end research", "from idea to submission" |
| [paper-pipeline](./paper-pipeline/) | Workflow 3: Paper writing pipeline (paper-plan → paper-figure → paper-write → paper-compile → auto-paper-improvement-loop) | "write paper pipeline", "from report to PDF", "paper generation workflow" |
| [auto-review-loop](./auto-review-loop/) | Autonomous multi-round research review loop with external LLM | "auto review loop", "review until it passes", "iterative improvement" |
| [auto-paper-improvement-loop](./auto-paper-improvement-loop/) | Paper improvement loop: review → fix → recompile (2 rounds) | "improve paper", "paper polishing loop", "iterative paper refinement" |

**Usage Recommendation:** Start with `/orchestrator` for full research projects. Use `/idea-discovery` when exploring research directions. Use `/paper-pipeline` when you have results ready for publication.

---

## Survey Phase Skills

Skills for literature review, idea formulation, and research planning.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [research-lit](./research-lit/) | Literature survey using academic APIs (arXiv, Semantic Scholar, DBLP, OpenAlex) | "literature survey", "find related work", "map research landscape" |
| [literature-survey](./literature-survey/) | Systematic 7-phase literature survey with citation verification and visualizations | "systematic review", "comprehensive literature survey", "PRISMA review" |
| [novelty-check](./novelty-check/) | Verify novelty of research ideas against existing literature | "check novelty", "is this novel", "verify originality" |
| [research-review](./research-review/) | External critical review via Codex MCP (GPT-5.4) acting as senior reviewer | "review this idea", "critical feedback", "brutal review" |
| [define-idea](./define-idea/) | Formulate research hypothesis with problem statement, approach, and contributions | "define idea", "formulate hypothesis", "structure research concept" |
| [idea-creator](./idea-creator/) | Brainstorm 8-12 research ideas via LLM, filter by feasibility, run pilot experiments | "generate ideas", "brainstorm research ideas", "find research directions" |
| [research-ideation](./research-ideation/) | Research ideation through 5-phase innovation flow (analogies, reversal, scale shifting) | "research brainstorming", "structured ideation", "creative research thinking" |
| [hypothesis-formulation](./hypothesis-formulation/) | Formulate testable hypotheses through 8-stage systematic process | "formulate hypothesis", "generate hypothesis", "develop testable hypotheses" |
| [theoretical-derivation](./theoretical-derivation/) | Conduct theoretical derivation with mathematical formulation, proofs, complexity analysis | "theoretical derivation", "formal analysis", "mathematical proof" |
| [research-intent-clarification](./research-intent-clarification/) | Clarify research intent through first-principles questioning before starting | "clarify intent", "understand research goal", "before starting research" |
| [research-plan](./research-plan/) | Create comprehensive research execution plan with methodology and timeline | "research plan", "create execution plan", "plan research timeline" |
| [critical-evaluation](./critical-evaluation/) | Apply systematic critical evaluation (methodology, bias, statistics, evidence, fallacies) | "critically evaluate", "systematic review", "quality assessment" |

**Usage Recommendation:** Start with `/research-intent-clarification` to clarify goals. Then use `/research-lit` for literature review, followed by `/define-idea` to formulate your hypothesis. Use `/novelty-check` to verify originality.

---

## Pilot Phase Skills

Skills for small-scale validation experiments before committing to full experiments.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [validate-problem](./validate-problem/) | Validate research problem existence and significance with evidence gathering | "validate problem", "problem validation", "is this problem worth solving" |
| [analyze-problem](./analyze-problem/) | Analyze research problem with decomposition, challenges, and solution approach | "analyze problem", "problem decomposition", "break down research challenge" |
| [design-pilot](./design-pilot/) | Design minimal pilot experiment to validate core hypothesis (< 24 hours) | "design pilot", "pilot experiment design", "small-scale validation design" |
| [run-pilot](./run-pilot/) | Execute pilot experiment and report results with Go/No-Go recommendation | "run pilot", "execute pilot", "pilot validation" |

**Usage Recommendation:** Run `/validate-problem` first to ensure the problem is real. Then `/analyze-problem` for decomposition, `/design-pilot` for experiment design, and `/run-pilot` for execution.

---

## Experiments Phase Skills

Skills for designing, running, and analyzing full-scale experiments.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [design-exp](./design-exp/) | Design full experiment matrix with hyperparameter ranges and statistical tests | "design experiments", "experiment matrix", "comprehensive experiment planning" |
| [run-experiment](./run-experiment/) | Deploy and run ML experiments on local or remote GPU servers | "run experiment", "deploy to server", "launch training jobs" |
| [monitor-experiment](./monitor-experiment/) | Monitor running experiments, check progress, collect results | "check results", "is it done", "monitor experiment status" |
| [analyze-results](./analyze-results/) | Analyze ML experiment results, compute statistics, generate comparison tables | "analyze results", "compare experiments", "interpret experimental data" |
| [statistical-reporting](./statistical-reporting/) | Statistical analysis guidance including test selection, power analysis, APA reporting | "statistical analysis", "power analysis", "effect size", "statistical test selection" |

**Usage Recommendation:** Use `/design-exp` to create the experiment matrix, `/run-experiment` to deploy, `/monitor-experiment` to check progress, and `/analyze-results` to interpret outcomes.

---

## Paper Phase Skills

Skills for manuscript writing, figure generation, and compilation.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [paper-plan](./paper-plan/) | Create paper outline and Claims-Evidence Matrix from research narrative | "paper outline", "paper structure", "plan manuscript" |
| [paper-figure](./paper-figure/) | Generate data-driven plots (matplotlib/seaborn) and LaTeX tables | "generate figures", "create plots", "paper visualizations" |
| [paper-write](./paper-write/) | Generate LaTeX sections following IMRAD structure with academic style | "write paper", "generate LaTeX", "draft manuscript" |
| [paper-compile](./paper-compile/) | Compile LaTeX paper to PDF with auto-fix for common errors | "compile paper", "build PDF", "LaTeX compilation" |
| [paper-writing-guide](./paper-writing-guide/) | Comprehensive manuscript writing guide (paragraphs, transitions, common mistakes) | "writing guide", "manuscript guidance", "academic writing tips" |
| [curate-citation](./curate-citation/) | Finalize all citations with verification status and authenticity checks | "curate citations", "verify references", "finalize bibliography" |

**Usage Recommendation:** Start with `/paper-plan` to structure the manuscript. Use `/paper-figure` for visualizations, `/paper-write` for content generation, and `/paper-compile` for PDF output.

---

## Reflection Phase Skills

Skills for extracting lessons learned and proposing improvements.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [extract-lessons](./extract-lessons/) | Extract lessons learned from project for future improvement | "extract lessons", "lessons learned", "project retrospective" |
| [propose-overlay](./propose-overlay/) | Propose system improvements through prompt modifications and workflow changes | "propose overlay", "system improvement", "suggest enhancements" |

**Usage Recommendation:** Run `/extract-lessons` after project completion. Use `/propose-overlay` to suggest orchestrator improvements based on lessons learned.

---

## Audit Skills

Quality gate skills that review and validate outputs from each phase. All audit skills use a 7-stage review process.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [audit-survey](./audit-survey/) | Audit literature survey for completeness, citation authenticity, and novelty claims | "audit survey", "review literature survey", "verify survey quality" |
| [audit-pilot](./audit-pilot/) | Audit pilot results for hypothesis validation and reproducibility | "audit pilot", "review pilot results", "verify pilot outcomes" |
| [audit-design](./audit-design/) | Audit pilot design for validity and resource efficiency | "audit design", "review pilot design", "verify experiment design" |
| [audit-plan](./audit-plan/) | Audit research execution plan for feasibility and risk coverage | "audit plan", "review research plan", "verify execution plan" |
| [audit-exp-design](./audit-exp-design/) | Audit experiment design for statistical validity and baseline completeness | "audit experiment design", "verify experiment matrix" |
| [audit-results](./audit-results/) | Audit experiment results for traceability and statistical validity | "audit results", "review experiment results", "verify result quality" |
| [audit-paper-plan](./audit-paper-plan/) | Audit paper outline for claim-evidence alignment and structure | "audit paper plan", "review paper outline" |
| [audit-paper](./audit-paper/) | Review paper draft for scientific rigor, writing quality, and citation authenticity | "audit paper", "review paper", "verify manuscript quality" |
| [audit-citation](./audit-citation/) | Audit citation authenticity with detailed verification of each reference | "audit citations", "verify citations", "check reference authenticity" |
| [audit-lessons](./audit-lessons/) | Audit lessons learned for transferability and actionability | "audit lessons", "review lessons learned" |
| [audit-overlay](./audit-overlay/) | Audit proposed system improvements for safety and rollback capability | "audit overlay", "review system improvements" |
| [audit-analysis](./audit-analysis/) | Audit problem analysis for completeness and solution feasibility | "audit analysis", "review problem analysis" |
| [audit-derivation](./audit-derivation/) | Audit theoretical derivation for mathematical rigor and proof correctness | "audit derivation", "review theoretical derivation" |
| [audit-validation](./audit-validation/) | Audit problem validation for evidence quality and verdict justification | "audit validation", "review problem validation" |

**Usage Recommendation:** Audit skills are automatically invoked by the orchestrator during gate checks. They can also be manually invoked to verify phase deliverables before proceeding.

---

## Agent Skills

Agent skills define the primary and reviewer agents for each phase. These are invoked via `Agent(subagent_type="airesearchorchestrator:<agent>", ...)`.

### Primary Agents

| Agent | Phase(s) | Description |
|-------|----------|-------------|
| [survey](./survey/) | Survey | Literature review, idea formulation, theoretical derivation |
| [coder](./coder/) | Pilot, Experiments | Experiment design, implementation, execution, analysis |
| [writer](./writer/) | Paper | Manuscript writing, figure generation, citation curation |
| [reflector](./reflector/) | Reflection | Lessons extraction, system improvement proposals |

### Reviewer Agents

| Agent | Phase(s) | Description |
|-------|----------|-------------|
| [critic](./critic/) | Survey | Audit novelty, feasibility, theory risk, citation authenticity |
| [adviser](./adviser/) | Pilot, Experiments | Review experimental design, validate results, judge evidence |
| [reviewer](./reviewer/) | Paper | Review manuscript per top-tier standards, audit citations |
| [curator](./curator/) | Reflection | Judge which improvements are reusable, safe, and actionable |

**Usage:** These agents are typically spawned by the orchestrator as part of Agent Teams. Do not invoke directly unless testing.

---

## Tool Skills

Utility skills that support the research workflow.

| Skill | Description | Trigger Scenarios |
|-------|-------------|-------------------|
| [feishu-notify](./feishu-notify/) | Send notifications to Feishu/Lark (push-only or interactive mode) | "send notification", "notify feishu", "push status update" |
| [gitmem](./gitmem/) | Lightweight version control for agent-generated document changes | "commit changes", "create checkpoint", "check edit loops" |
| [latex-citation-curator](./latex-citation-curator/) | Find, verify, rank, and generate DOI-verified BibTeX citations | "find citations", "curate references", "generate BibTeX" |

**Usage Recommendation:** These are internal utilities used by other skills. Use `/feishu-notify` for mobile notifications. Use `/gitmem` for document version tracking. Use `/latex-citation-curator` for citation management.

---

## Skill Architecture

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md          # Skill definition with metadata and workflow
├── references/       # Reference documents (optional)
└── assets/           # Templates and prompts (optional)
```

### SKILL.md Format

```yaml
---
name: airesearchorchestrator:skill-name
agent: role-type                    # orchestrator, survey, critic, code, writer, etc.
description: "Brief description"
argument-hint: [expected-arguments]
allowed-tools: [...]                # Tools this skill can use
---

# Skill Title

## Purpose
...

## Workflow
...

## Output
...

## Key Rules
...
```

---

## Agent Roles

Skills are executed by agents with specific roles:

| Agent Role | Purpose | Primary Skills |
|------------|---------|----------------|
| orchestrator | Overall coordination and phase transitions | orchestrator, idea-discovery, research-pipeline, paper-pipeline |
| survey | Literature review and idea formulation | research-lit, literature-survey, define-idea, research-ideation |
| critic | Critical review and quality assessment | novelty-check, research-review, audit-* skills |
| code | Implementation and execution | design-pilot, run-pilot, design-exp, run-experiment, analyze-results |
| writer | Paper writing and compilation | paper-plan, paper-write, paper-compile, paper-figure |
| reviewer | Paper quality review | audit-paper, audit-citation, audit-paper-plan |
| adviser | Pilot/experiment guidance | audit-pilot, audit-exp-design, audit-results, audit-design |
| reflector | Lessons extraction | extract-lessons |
| curator | System improvement review | audit-overlay, audit-lessons |

---

## Using Skills

### Via Slash Commands

Most skills have corresponding slash commands defined in `commands/`:

```bash
/run-survey "transformer attention mechanisms"
/run-pilot
/write-paper
```

### By Other Skills

Skills can invoke other skills using the Skill tool:

```markdown
Invoke `/novelty-check "$IDEA_DESCRIPTION"`
```

### Direct Invocation

Skills can be invoked directly by the orchestrator during phase execution.

---

## Contributing

When adding a new skill:

1. Create a directory in `skills/` with the skill name
2. Create `SKILL.md` with required metadata and workflow
3. Add reference documents in `references/` if needed
4. Update this README.md with the new skill entry
5. Add corresponding command in `commands/` if user-facing