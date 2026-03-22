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

### 3. Custom Research Types

The system supports 4 built-in research types with different phase sequences. You can add more.

**To add a custom research type:**

1. Edit `scripts/constants/phases.py`:
   - Add your type to `RESEARCH_TYPE_PHASE_SEQUENCE`:
     ```python
     "genomics": ("survey", "pilot", "experiments", "paper", "reflection"),
     ```
   - Add to `RESEARCH_TYPE_GPU_REQUIRED`:
     ```python
     "genomics": True,
     ```
2. Add the type to `settings.schema.json` enum list for `AUTORESEARCH_DEFAULT_RESEARCH_TYPE`
3. Add a test in `tests/test_phases_naming.py` covering the new type
4. Update README.md research types table

**Current research types:**

| Type | Phase Sequence | GPU Required |
|------|----------------|--------------|
| `ml_experiment` | survey → pilot → experiments → paper → reflection | Yes |
| `theory` | survey → pilot → paper → reflection | No |
| `survey` | survey → paper → reflection | No |
| `applied` | survey → pilot → experiments → paper → reflection | Yes |

### 4. Reference Documents

Reference documents in `references/` define standards and protocols. Improvements to rubrics, evidence standards, or writing guidelines are welcome.

### 5. Bug Fixes

Check [open issues](https://github.com/jacazjx/AI-Research-Orchestrator/issues) for bugs. Fix, add a test, and submit a PR.

### 6. Python Scripts

Scripts in `scripts/` handle state management, gate evaluation, and project structure. Changes here require tests and backward compatibility.

## Extensibility Notes

**What can be extended:**
- Skills (add `skills/<name>/SKILL.md`)
- Agents (add `agents/<role>/AGENT.md`)
- Commands (add `commands/<name>.md`)
- Research types (edit `scripts/constants/phases.py`)
- Reference standards (edit `references/*.md`)
- Hook scripts (edit `hooks/hooks.json` + add scripts)

**What requires forking:**
- Adding custom phases beyond the 5-phase workflow
- Changing the gate scoring system
- Modifying the dual-loop runtime architecture

**Design intent:** The 5-phase workflow and dual-agent-per-phase constraint are intentional architectural decisions that ensure quality. Skills and agents are the primary extension points.

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
