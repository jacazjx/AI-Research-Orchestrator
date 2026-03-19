# System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│                   (Outer Loop Control)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│   │ SURVEY   │───▶│  PILOT   │───▶│EXPERIMENTS│                │
│   │ Phase 1  │    │ Phase 2  │    │ Phase 3   │                │
│   └────┬─────┘    └────┬─────┘    └────┬──────┘                │
│        │               │               │                        │
│        │  ┌────────────┼───────────────┼────────────┐          │
│        │  │            │               │            │          │
│        ▼  ▼            ▼               ▼            ▼          │
│   ┌─────────────────────────────────────────────────┐          │
│   │              INNER LOOP (Per Phase)              │          │
│   │  ┌─────────────┐         ┌─────────────┐        │          │
│   │  │   PRIMARY   │ ◀─────▶ │   REVIEWER  │        │          │
│   │  │   (Doer)    │         │  (Auditor)  │        │          │
│   │  └─────────────┘         └─────────────┘        │          │
│   └─────────────────────────────────────────────────┘          │
│        │               │               │                        │
│        ▼               ▼               ▼                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│   │  PAPER   │───▶│REFLECTION│───▶│  CLOSED  │                 │
│   │ Phase 4  │    │ Phase 5  │    │          │                 │
│   └──────────┘    └──────────┘    └──────────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Key:
  ───▶ Phase flow (requires Gate approval)
  ◀───▶ Agent interaction (Inner Loop iteration)
```

The runtime uses two loops:

- `inner_loop`: phase-local iteration driven by direct `SendMessage` exchange between the Primary and Reviewer agents (not relayed through the Orchestrator)
- `outer_loop`: Orchestrator manages phase lifecycle via Team/Task tools (`TeamCreate`, `TeamDelete`, `TaskCreate`, `TaskUpdate`) and monitors agent progress via `TaskList`

Core files:

- `.autoresearch/state/research-state.yaml`: machine-readable source of truth
- `.autoresearch/config/orchestrator-config.yaml`: project-level runtime configuration
- `.autoresearch/dashboard/`: visible progress and event stream
- `.autoresearch/runtime/`: job, GPU, backend, and sentinel registries

The orchestrator is the only role that talks directly to the user. It acts as Team Lead (not a communication relay): it manages the team and task lifecycle, but agents communicate directly with each other via `SendMessage` during inner-loop iteration. All sub-agent prompts are rendered from fixed templates and then adjusted for the current task.

## Agent Teams Update (2026-03-19)

This system uses the Claude Code Agent Teams feature. Key architecture points:

- **Orchestrator is Team Lead, not relay.** The Orchestrator creates/deletes teams and tasks, spawns agents, and monitors progress — it does not forward or relay messages between agents.
- **Direct agent communication.** Primary and Reviewer agents communicate directly via `SendMessage` during inner-loop iteration without Orchestrator intermediation.
- **Task tools replace manual state tracking.** Per-task status, agent assignments, and inter-agent dependencies are managed by `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList`. The `research-state.yaml` file tracks phase-level status, gate approvals, loop counts, and substep persistence across context resets only — it is not used for per-task tracking.

## Directory Structure

```
my-project/
├── .autoresearch/           # System directory (hidden)
│   ├── state/               # State files
│   │   └── research-state.yaml
│   ├── config/              # Configuration
│   │   └── orchestrator-config.yaml
│   ├── dashboard/           # Runtime dashboard
│   ├── runtime/             # Runtime registries
│   ├── reference-papers/    # Reference papers
│   ├── templates/           # Template cache
│   └── archive/             # Archive
├── agents/                  # Agent work directories (by role)
│   ├── survey/
│   ├── critic/
│   ├── coder/
│   ├── adviser/
│   ├── writer/
│   ├── reviewer/
│   ├── reflector/
│   └── curator/
├── paper/                   # Paper-related files
├── code/                    # Code-related files
└── docs/                    # Documentation and reports
    └── reports/
        ├── survey/
        ├── pilot/
        ├── experiments/
        └── reflection/
```