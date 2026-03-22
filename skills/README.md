# Skills Directory

This directory contains 25 specialized skills for the AI Research Orchestrator.

> **Note**: Agent role definitions (survey, critic, coder, adviser, writer, reviewer, reflector, curator) are in `agents/`, not here. Each agent discovers skills dynamically from this directory at runtime.

## Orchestration & System (6)

| Skill | Description |
|-------|-------------|
| [orchestrator](./orchestrator/) | Main five-phase research project orchestrator |
| [audit](./audit/) | Generic quality gate review -- adapts to any phase deliverable |
| [reload](./reload/) | Reload project state for session resumption |
| [status](./status/) | Show live project status |
| [configure](./configure/) | Configure project settings |
| [insight](./insight/) | Interactive intent clarification before initialization |

## Research Capabilities (4)

| Skill | Description |
|-------|-------------|
| [literature](./literature/) | Literature search -- from quick check to systematic review |
| [citation](./citation/) | Citation discovery, DOI verification, ranking, BibTeX generation |
| [ideation](./ideation/) | Research ideation: generate, filter, verify novelty |
| [external-review](./external-review/) | External review via Codex MCP -- single-shot or multi-round improvement loop |

## Experiment Execution (3)

| Skill | Description |
|-------|-------------|
| [experiment-design](./experiment-design/) | Design experiments at pilot or full scale with statistical rigor |
| [run-experiment](./run-experiment/) | Execute experiments (pilot or full) on local or remote GPU |
| [monitor-experiment](./monitor-experiment/) | Monitor running experiments, collect results |

## Analysis (1)

| Skill | Description |
|-------|-------------|
| [analyze-results](./analyze-results/) | Analyze results, compute statistics, generate comparisons |

## Paper Writing (3)

| Skill | Description |
|-------|-------------|
| [paper-write](./paper-write/) | Plan structure (Claims-Evidence Matrix) and generate LaTeX sections |
| [paper-figure](./paper-figure/) | Generate data-driven plots and tables |
| [paper-compile](./paper-compile/) | Compile LaTeX to PDF with auto-fix |

## Writing Quality (1)

| Skill | Description |
|-------|-------------|
| [writing-deai](./writing-deai/) | Detect and remove LLM writing patterns from paper drafts |

## Post-Submission (3)

| Skill | Description |
|-------|-------------|
| [self-review](./self-review/) | Pre-submission self-review checklist for paper quality assurance |
| [rebuttal](./rebuttal/) | Write structured rebuttals responding to peer review comments |
| [post-acceptance](./post-acceptance/) | Generate post-acceptance materials: slides outline, poster layout, social media text |

## System Evaluation (2)

| Skill | Description |
|-------|-------------|
| [system-evaluation](./system-evaluation/) | Evaluate orchestrator performance across 6 dimensions during Reflection |
| [audit-system-evaluation](./audit-system-evaluation/) | Audit system evaluation reports for objectivity and scoring accuracy |

## Utilities (2)

| Skill | Description |
|-------|-------------|
| [feishu-notify](./feishu-notify/) | Send notifications to Feishu/Lark |
| [gitmem](./gitmem/) | Lightweight version control for agent edits |
