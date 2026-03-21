# Project Takeover Protocol

This document defines the procedures for taking over existing research projects and integrating them into the AI research orchestrator workflow.

## Overview

Project takeover is the process of analyzing an existing research project and bringing it into the orchestrator workflow. This enables researchers to continue work on projects that weren't originally created with the orchestrator.

## Starting Phase Feature

When initializing or migrating a project, you can specify a starting phase to:
- Resume work from a specific phase
- Skip completed phases
- Start at a later phase for projects with existing work

### Available Phases

| Phase | Description | Gate |
|-------|-------------|------|
| `survey` (or `01-survey`) | Literature survey and research readiness | gate_1 |
| `pilot` (or `02-pilot-analysis`) | Pilot experiments and validation | gate_2 |
| `experiments` (or `03-full-experiments`) | Full experiment execution | gate_3 |
| `paper` (or `04-paper`) | Paper development and review | gate_4 |
| `reflection` (or `05-reflection-evolution`) | Lessons learned and improvements | gate_5 |

### Usage

```bash
# Initialize with starting phase (semantic names)
python3 scripts/init_research_project.py \
  --project-root /path/to/project \
  --topic "Your research topic" \
  --starting-phase experiments

# Migrate with starting phase (legacy names still supported)
python3 scripts/migrate_project.py \
  --project-root /path/to/existing-project \
  --topic "Your research topic" \
  --starting-phase pilot
```

## When to Use Project Takeover

Use project takeover when:

1. **Inheriting a project** from another researcher
2. **Resuming work** on a personal project that lacks structure
3. **Adopting a legacy project** for continuation
4. **Migrating projects** from other workflow systems

## Takeover Process

### Phase 1: Initial Assessment

#### Step 1: Run Analysis

The orchestrator agent can analyze an existing project by reading its directory structure and state files. It checks:
- Directory structure analysis
- File pattern detection
- Existing deliverable inventory
- Estimated project phase
- Research state check

#### Step 2: Review Analysis Report

Key questions:
- Is this an orchestrated project already?
- What phase is the project at?
- What artifacts exist?
- What's missing?

#### Step 3: Interview Researcher

Ask the researcher:

1. **Project Status**
   - What have you completed?
   - What's the current state?

2. **Goals**
   - What do you want to achieve?
   - Is there a target venue?

3. **Constraints**
   - Timeline constraints?
   - Resource limitations?

4. **Quality Status**
   - Are results verified?
   - Any known issues?

### Phase 2: Migration Decision

#### Decision Matrix

| Scenario | Action |
|----------|--------|
| Empty/minimal project | Full initialization |
| Some artifacts, no structure | Partial migration |
| Well-structured, no state | Add state, verify |
| Already orchestrated | Verify and continue |

#### Phase Estimation

| Evidence | Estimated Phase |
|----------|-----------------|
| Nothing | Initialize (.autoresearch/) |
| Literature only | survey |
| Pilot code/results | pilot |
| Experiment results | experiments |
| Paper draft | paper |
| Published paper | reflection |

### Phase 3: Execute Migration

#### Full Migration

For projects with no structure:

```bash
python3 scripts/migrate_project.py \
  --project-root /path/to/project \
  --topic "Your research topic"
```

This creates:
- All phase directories
- .autoresearch/state/research-state.yaml
- .autoresearch/reference-papers/idea-brief.md
- .autoresearch/config/orchestrator-config.yaml

#### Partial Migration

For projects with some artifacts:

1. **Analyze first**
   Have the orchestrator agent analyze the project by reading its directory structure and state files.

2. **Create missing directories**
   ```bash
   python3 scripts/migrate_project.py --project-root /path/to/project --topic "Topic"
   ```

3. **Review imported artifacts**

4. **Initialize state at appropriate phase**

#### Dry Run First

Always preview changes:

```bash
python3 scripts/migrate_project.py \
  --project-root /path/to/project \
  --topic "Topic" \
  --dry-run
```

### Phase 4: Verification

After migration, verify:

1. **State Consistency**
   System verification is handled by the orchestrator at session start.

2. **Phase Artifacts**
   - Check each phase directory
   - Verify imported files
   - Confirm nothing was lost

3. **State Alignment**
   - Confirm current_phase matches reality
   - Check gate status is appropriate

### Phase 5: Continue Work

Once verified:

1. **Agent prompts** are defined in `agents/<role>/AGENT.md` files. The orchestrator renders appropriate prompts for each phase.

2. **Begin phase work**
   - Continue from current phase
   - Address identified gaps
   - Follow standard workflow

## Common Scenarios

### Scenario 1: Empty Project Directory

**Situation**: Researcher has a topic but no files.

**Action**: Initialize new project.

```bash
python3 scripts/init_research_project.py \
  --project-root /path/to/project \
  --topic "Research topic"
```

### Scenario 2: Code Only, No Documentation

**Situation**: Researcher has experiment code but no documentation.

**Action**: Partial migration.

1. Run analysis
2. Create structure
3. Import code to appropriate phase directory
4. Create documentation
5. Set phase to pilot or experiments

### Scenario 3: Paper Draft Exists, No Experiments Documented

**Situation**: Researcher has a paper draft but experiment records are scattered.

**Action**:
1. Import paper to paper/
2. Survey existing experiment code
3. Reconstruct experiment documentation
4. Set phase based on paper completeness

### Scenario 4: Previous Orchestrator Project

**Situation**: Project was previously created with orchestrator.

**Action**:
1. Verify state file
2. Check artifact consistency
3. Update if needed
4. Continue from recorded phase

## Artifact Mapping

| Source Pattern | Target Location |
|----------------|-----------------|
| *.bib, papers/*.pdf | .autoresearch/reference-papers/ |
| survey*.md, literature*.md | docs/survey/ |
| pilot*.py, pilot*.md | code/pilot/ |
| experiment*.py, results*.md | code/experiments/ |
| paper*.tex, draft*.md | paper/ |

## Quality Verification

### What to Verify

1. **Citation Authenticity** (if paper phase)
   - Check BibTeX files
   - Verify DOI references
   - Flag unverified citations

2. **Experimental Integrity** (if experiment phase)
   - Check for log files
   - Verify checkpoint existence
   - Trace result provenance

3. **Paper Quality** (if paper phase)
   - Check draft completeness
   - Verify figure/table presence
   - Assess writing quality

### Verification Commands

```bash
# System verification is handled by the orchestrator at session start

# Audit citations (paper phase)
python3 scripts/run_citation_audit.py --project-root /path/to/project

# Check gate readiness
python3 scripts/quality_gate.py --project-root /path/to/project --phase [phase]
```

## Researcher Communication

### Initial Questions

1. "Can you tell me about the current state of this project?"
2. "What have you completed so far?"
3. "What's your goal for this project?"
4. "Are there any urgent deadlines?"

### During Migration

1. "I found these files. Should they be included?"
2. "This appears to be at phase X. Is that correct?"
3. "I notice these gaps. Should we address them?"

### After Migration

1. "Here's the project structure. Does this look right?"
2. "I've set the phase to X. Should we start there?"
3. "These artifacts need attention before proceeding."

## Troubleshooting

### Common Issues

#### Issue: State file conflicts with existing files

**Solution**: Use --dry-run first, review conflicts, then decide whether to skip or overwrite.

#### Issue: Unclear project phase

**Solution**: Interview researcher about project status, then make informed decision.

#### Issue: Missing critical artifacts

**Solution**: Create placeholders, then address in phase work.

#### Issue: Multiple paper drafts

**Solution**: Identify the most recent/complete, archive others.

## Checklist

### Pre-Takeover
- [ ] Have the orchestrator analyze the project directory
- [ ] Review analysis report
- [ ] Interview researcher
- [ ] Decide migration approach

### During Takeover
- [ ] Run migrate_project.py (or init_research_project.py)
- [ ] Import existing artifacts
- [ ] Verify nothing lost
- [ ] Initialize state

### Post-Takeover
- [ ] Verify system integrity via orchestrator session start
- [ ] Review with researcher
- [ ] Begin phase work (agent prompts are in `agents/<role>/AGENT.md`)