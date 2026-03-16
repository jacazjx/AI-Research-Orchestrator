# AI Research Orchestrator Commands

This directory contains user-facing commands for the five-phase research workflow.

## Available Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `/autoresearch:init-research` | Setup | Initialize a new research project |
| `/autoresearch:run-survey` | Phase 1 | Literature survey and readiness assessment |
| `/autoresearch:run-pilot` | Phase 2 | Pilot validation and feasibility check |
| `/autoresearch:run-experiments` | Phase 3 | Full experiments and evidence collection |
| `/autoresearch:write-paper` | Phase 4 | Paper writing and submission preparation |
| `/autoresearch:reflect` | Phase 5 | Lessons learned and project evolution |

## Workflow Order

```
/autoresearch:init-research → /autoresearch:run-survey → /autoresearch:run-pilot → /autoresearch:run-experiments → /autoresearch:write-paper → /autoresearch:reflect
           Setup                    Phase 1                  Phase 2                     Phase 3                           Phase 4                    Phase 5
```

## Quick Start

### Start a New Project

```
/autoresearch:init-research "Your research topic or idea"
```

### Run Full Pipeline

```
/autoresearch:run-survey
/autoresearch:run-pilot
/autoresearch:run-experiments
/autoresearch:write-paper
/autoresearch:reflect
```

## Gate Requirements

Each phase transition requires:

1. **Gate 0 → 1**: Project initialization complete
2. **Gate 1 → 2**: `research-readiness-report.md` approved
3. **Gate 2 → 3**: `pilot-validation-report.md` approved
4. **Gate 3 → 4**: `evidence-package-index.md` approved
5. **Gate 4 → 5**: `final-acceptance-report.md` approved
6. **Gate 5**: Project completion decision

## Command Details

Each command follows the same structure:

```yaml
---
name: command-name
description: "Description with trigger phrases"
argument-hint: [expected-argument]
allowed-tools: List of allowed tools
---
```

## Related Skills

The commands delegate to these skills:

- `skills/idea-discovery/` - Idea discovery workflow
- `skills/research-lit/` - Literature search
- `skills/run-experiment/` - Experiment execution
- `skills/paper-pipeline/` - Paper writing workflow
- `skills/auto-review-loop/` - Autonomous review

## Configuration

Commands respect settings in `.autoresearch/config/orchestrator-config.yaml`:

```yaml
aris:
  auto_proceed: false  # Require manual gate approval
  reviewer:
    enabled: true
    model: gpt-5.4
```