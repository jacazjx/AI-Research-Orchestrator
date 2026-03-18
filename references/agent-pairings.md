# Agent Pairings

This document describes the agent pairing system used throughout the research pipeline.

## Overview

Each phase uses a dual-agent system with a Primary (Doer) agent and a Reviewer (Auditor) agent. This ensures quality through built-in review cycles.

## Phase-Agent Mapping

| Phase | Primary Agent | Reviewer Agent | Gate |
|-------|---------------|----------------|------|
| Survey | [Survey](../agents/survey/AGENT.md) | [Critic](../agents/critic/AGENT.md) | Gate 1 |
| Pilot | [Coder](../agents/coder/AGENT.md) | [Adviser](../agents/adviser/AGENT.md) | Gate 2 |
| Experiments | [Coder](../agents/coder/AGENT.md) | [Adviser](../agents/adviser/AGENT.md) | Gate 3 |
| Paper | [Writer](../agents/writer/AGENT.md) | [Reviewer](../agents/reviewer/AGENT.md) | Gate 4 |
| Reflection | [Reflector](../agents/reflector/AGENT.md) | [Curator](../agents/curator/AGENT.md) | Gate 5 |

## Agent Responsibilities

### Primary Agents (Doers)

| Agent | Phase | Key Responsibilities |
|-------|-------|---------------------|
| Survey | Phase 1 | Literature review, gap analysis, novelty argument |
| Coder | Phase 2-3 | Experiment design, implementation, execution |
| Writer | Phase 4 | Manuscript drafting, evidence integration |
| Reflector | Phase 5 | Lessons extraction, improvement proposals |

### Reviewer Agents (Auditors)

| Agent | Phase | Key Responsibilities |
|-------|-------|---------------------|
| Critic | Phase 1 | Novelty verification, citation authenticity audit |
| Adviser | Phase 2-3 | Design review, evidence validation |
| Reviewer | Phase 4 | Manuscript quality review, citation audit |
| Curator | Phase 5 | Improvement proposal validation |

## Communication Flow

```
[Orchestrator] ──dispatch──▶ [Primary Agent]
       ▲                          │
       │                          ▼
       │                    [Deliverable]
       │                          │
       │                          ▼
       └────report──────── [Reviewer Agent]
```

## Inner Loop Process

1. **Primary Agent** executes task, produces deliverable
2. **Reviewer Agent** reviews deliverable, provides score and feedback
3. If score < 3.5: Primary Agent revises, loop continues
4. If score >= 3.5: Proceed to Gate
5. **Gate** requires human approval before next phase

## Interaction Rules

1. **Orchestrator is the hub**: All agent communication flows through the Orchestrator
2. **No direct agent-to-agent communication**: Prevents context pollution
3. **Explicit handoffs**: Agents save summaries when dismissed
4. **Fresh context per agent**: Each agent starts with relevant context from state

## External Agents

| Agent | Purpose | Invocation |
|-------|---------|------------|
| codex-mcp | Cross-model review | Via MCP tool `mcp__codex__codex` |
| openai | Alternative interface | Configured in agent settings |

## See Also

- [System Architecture](system-architecture.md) - Overall runtime design
- [Orchestrator Protocol](orchestrator-protocol.md) - Communication standards
- [Gate Rubrics](gate-rubrics.md) - Scoring criteria for each phase
