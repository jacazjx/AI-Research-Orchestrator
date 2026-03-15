<p align="center">
  <img src="assets/images/logo.svg" alt="AI Research Orchestrator" width="200">
</p>

<h1 align="center">AI Research Orchestrator</h1>

<p align="center">
  <strong>Turn a research IDEA into a controlled five-phase project with explicit human gates</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> | English
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blue?logo=anthropic" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Version-1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Python-3.9+-blue" alt="Python">
  <img src="https://img.shields.io/badge/Phase-5-orange" alt="5 Phases">
</p>

---

`ai-research-orchestrator` is a research workflow skill for Claude Code, Codex, and Openclaw environments. It transforms a research IDEA into a project with state machines, deliverables, visual progress tracking, and explicit human gates.

## Key Features

- **Five-Phase Workflow**: `Survey/Critic → Pilot Code/Adviser → Experiment Code/Adviser → Paper Writer/Reviewer → Reflector/Curator`
- **Dual-Loop Architecture**: Inner loop with dual-agent iteration per phase, outer loop for phase transitions
- **Five Human Gates**: Survey, Pilot, Full Experiments, Paper, Reflection/Evolution
- **Visual Progress**: `.autoresearch/dashboard/` for runtime visualization
- **Quality Gates**: `scripts/quality_gate.py` with score thresholds
- **Standardized Workspace**: Templates, state files, and handoff validation

## Installation

### Option 1: Install from GitHub Marketplace (Recommended)

```bash
# 1. Add the marketplace
/plugin marketplace add jacazjx/AI-Research-Orchestrator

# 2. Install the plugin
/plugin install autoresearch@autoresearch
```

Restart Claude Code after installation.

### Option 2: Configure settings.json

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "autoresearch": {
      "source": {
        "source": "github",
        "repo": "jacazjx/AI-Research-Orchestrator"
      }
    }
  },
  "enabledPlugins": {
    "autoresearch@autoresearch": true
  }
}
```

### Option 3: Local Development

```bash
cc --plugin-dir /path/to/AI-Research-Orchestrator
```

## Quick Start

```bash
# Initialize a new research project
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea" \
  --client-type auto
```

## Workflow Phases

| Phase | Agents | Key Deliverable |
|-------|--------|-----------------|
| Survey | Survey ↔ Critic | `docs/reports/survey/research-readiness-report.md` |
| Pilot | Code ↔ Adviser | `docs/reports/pilot/pilot-validation-report.md` |
| Experiments | Code ↔ Adviser | `docs/reports/experiments/evidence-package-index.md` |
| Paper | Writer ↔ Reviewer | `paper/final-acceptance-report.md` |
| Reflection | Reflector ↔ Curator | `docs/reports/reflection/runtime-improvement-report.md` |

## Commands

| Command | Description |
|---------|-------------|
| `/init-research` | Initialize a new research project |
| `/run-survey` | Run the Survey phase |
| `/run-pilot` | Run the Pilot phase |
| `/run-experiments` | Run the full Experiments phase |
| `/write-paper` | Run the Paper Writing phase |
| `/reflect` | Run the Reflection phase |

## Directory Structure

```
my-project/
├── .autoresearch/           # System directory
│   ├── state/               # State files
│   ├── config/              # Configuration
│   ├── dashboard/           # Runtime dashboard
│   └── runtime/             # Job/GPU/Backend registries
├── agents/                  # Agent work directories
├── paper/                   # Paper-related files
├── code/                    # Code-related files
└── docs/reports/            # Phase deliverables
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `scripts/init_research_project.py` | Initialize five-phase workspace |
| `scripts/quality_gate.py` | Gate evaluation with scoring |
| `scripts/generate_dashboard.py` | Generate progress dashboard |
| `scripts/validate_handoff.py` | Validate phase transitions |
| `scripts/run_stage_loop.py` | Execute phase iteration loops |

## Documentation

- [Workflow Protocol](references/workflow-protocol.md)
- [Gate Rubrics](references/gate-rubrics.md)
- [System Architecture](references/system-architecture.md)
- [Phase Execution Details](references/phase-execution-details.md)

## Testing

```bash
python3 -m pytest tests/ -v
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for AI Researchers
</p>