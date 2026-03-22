# Contributing to AI Research Orchestrator

Thank you for your interest in improving the AI Research Orchestrator! This guide covers everything you need to get started.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/jacazjx/AI-Research-Orchestrator.git
cd AI-Research-Orchestrator
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v --tb=short

# Format and lint
black scripts/ tests/ && isort scripts/ tests/
flake8 scripts/ tests/ --max-line-length=100 --extend-ignore=E203,W503
```

## What Can You Contribute?

### 1. New Skills (Easiest)

Skills are the primary extension point. A skill is a markdown file that instructs Claude how to perform a specific research task.

**To add a new skill:**

1. Create `skills/<skill-name>/SKILL.md` using the template below
2. Add an entry to `skills/README.md`
3. If user-facing, add a command in `commands/<name>.md`
4. Add tests in `tests/test_<skill_name>.py`
5. Submit a PR

**Skill template** (`skills/<name>/SKILL.md`):

```yaml
---
name: airesearchorchestrator:<skill-name>
agent: <agent-role>
description: "<When to use this skill and what it does>"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Skill Title

## Purpose

What this skill does and when to use it.

## Workflow

Step-by-step instructions for the agent executing this skill.

## Output

What artifacts this skill produces.
```

**Agent roles:** `orchestrator`, `survey`, `critic`, `coder`, `adviser`, `writer`, `reviewer`, `reflector`, `curator`

### 2. Custom Agents (Advanced)

Agents are role definitions that give Claude a specific persona and expertise. Each phase uses exactly two agents (primary + reviewer).

**To add a new agent:**

1. Create `agents/<role-name>/AGENT.md` with the template below
2. To use the agent in a phase, update `PHASE_AGENT_PAIRS` in `scripts/constants/phases.py`
3. Create skills that reference the new agent via the `agent:` frontmatter field

**Agent template** (`agents/<role>/AGENT.md`):

```yaml
---
name: <role-name>
description: "When to invoke this agent"
---

# Identity & Expertise

You are the <Role Name> agent. Your expertise is in <domain>.

# Mission

<What this agent is responsible for achieving>

# Quality Standards

- <Standard 1>
- <Standard 2>

# Hard Constraints

- <Constraint 1>
- <Constraint 2>
```

**Current agent pairs per phase:**

| Phase | Primary | Reviewer |
|-------|---------|----------|
| survey | survey | critic |
| pilot | code | adviser |
| experiments | code | adviser |
| paper | writer | reviewer |
| reflection | reflector | curator |

### 3. Reference Documents

Reference documents in `references/` define standards and protocols. Improvements to rubrics, evidence standards, or writing guidelines are welcome.

### 4. Bug Fixes

Check [open issues](https://github.com/jacazjx/AI-Research-Orchestrator/issues) for bugs. Fix, add a test, and submit a PR.

### 5. Python Scripts

Scripts in `scripts/` handle state management, gate evaluation, and project structure. Changes here require tests and backward compatibility.

## Architecture Notes

- **Skills instruct agents** (declarative orchestration in SKILL.md)
- **Scripts handle logic** (testable Python in scripts/)
- **State is YAML** (`.autoresearch/state/research-state.yaml` is the single source of truth)
- **Exactly 2 agents per phase** (primary + reviewer)
- **Human gates are mandatory** (no automatic phase transitions)

## Code Standards

- Python >= 3.9
- Format with `black` and `isort`
- Lint with `flake8` (max line 100) and `mypy`
- All new code needs tests
- Run `python -m pytest tests/ -v` before submitting

## Pull Request Checklist

- [ ] Tests pass (`python -m pytest tests/ -v`)
- [ ] Code formatted (`black scripts/ tests/ && isort scripts/ tests/`)
- [ ] No lint errors (`flake8 scripts/ tests/`)
- [ ] New features have tests
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] skills/README.md updated (if adding a skill)

## Versioning

Version bumps are handled by maintainers using:

```bash
python3 scripts/bump_version.py --minor --message "Description"
```

Do not manually edit version numbers in your PR.

## Questions?

Open a [discussion](https://github.com/jacazjx/AI-Research-Orchestrator/discussions) or [issue](https://github.com/jacazjx/AI-Research-Orchestrator/issues).
