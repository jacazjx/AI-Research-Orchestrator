# Skills Directory

This directory contains 37 specialized skills for the AI Research Orchestrator.

## Orchestration & System (6)

| Skill | Description |
|-------|-------------|
| [orchestrator](./orchestrator/) | Main five-phase research project orchestrator |
| [audit](./audit/) | Generic quality gate review — adapts to any phase deliverable |
| [reload](./reload/) | Reload project state for session resumption |
| [status](./status/) | Show live project status |
| [configure](./configure/) | Configure project settings |
| [insight](./insight/) | Interactive intent clarification before initialization |

## Agent Roles (8)

| Agent | Phase(s) |
|-------|----------|
| [survey](./survey/) | Survey — literature review, idea formulation |
| [critic](./critic/) | Survey — audit novelty, feasibility, citations |
| [coder](./coder/) | Pilot & Experiments — design, implement, execute |
| [adviser](./adviser/) | Pilot & Experiments — review design, validate evidence |
| [writer](./writer/) | Paper — manuscript writing, citations |
| [reviewer](./reviewer/) | Paper — top-tier venue quality review |
| [reflector](./reflector/) | Reflection — lessons extraction |
| [curator](./curator/) | Reflection — safety review for improvements |

## Research Capabilities (10)

| Skill | Description |
|-------|-------------|
| [literature](./literature/) | Literature search — from quick check to systematic 7-phase review |
| [citation](./citation/) | Citation discovery, DOI verification, ranking, BibTeX generation |
| [ideation](./ideation/) | Research brainstorming, idea generation, novelty verification |
| [hypothesis-formulation](./hypothesis-formulation/) | Systematic 8-stage hypothesis development |
| [theoretical-derivation](./theoretical-derivation/) | Mathematical formalization, proofs, complexity analysis |
| [problem-analysis](./problem-analysis/) | Problem definition, decomposition, significance validation |
| [experiment-design](./experiment-design/) | Design experiments — pilot (< 24hr) or full matrix |
| [research-plan](./research-plan/) | Research execution plan with methodology and timeline |
| [research-review](./research-review/) | External critical review via Codex MCP |
| [extract-lessons](./extract-lessons/) | Extract transferable lessons from project |

## Experiment Execution (4)

| Skill | Description |
|-------|-------------|
| [run-pilot](./run-pilot/) | Execute pilot experiment with Go/No-Go recommendation |
| [run-experiment](./run-experiment/) | Deploy experiments on local or remote GPU |
| [monitor-experiment](./monitor-experiment/) | Monitor running experiments, collect results |
| [analyze-results](./analyze-results/) | Analyze results, compute statistics, generate comparisons |

## Paper Writing (4)

| Skill | Description |
|-------|-------------|
| [paper-plan](./paper-plan/) | Create paper outline and Claims-Evidence Matrix |
| [paper-write](./paper-write/) | Generate LaTeX sections (IMRAD structure) |
| [paper-figure](./paper-figure/) | Generate data-driven plots and tables |
| [paper-compile](./paper-compile/) | Compile LaTeX to PDF with auto-fix |

## Improvement Loops (2)

| Skill | Description |
|-------|-------------|
| [auto-review-loop](./auto-review-loop/) | Autonomous multi-round review via external LLM |
| [auto-paper-improvement-loop](./auto-paper-improvement-loop/) | Paper review → fix → recompile loop |

## Utilities (3)

| Skill | Description |
|-------|-------------|
| [feishu-notify](./feishu-notify/) | Send notifications to Feishu/Lark |
| [gitmem](./gitmem/) | Lightweight version control for agent edits |
| [propose-overlay](./propose-overlay/) | Propose system improvements with safety assessment |
