---
name: autoresearch:gitmem
description: Lightweight version control for agent-generated document changes. Tracks iterative refinement without creating v1, v2, v3 copies. Use when committing agent edits, creating checkpoints, or checking for edit loops.
argument-hint: <command> [options]
allowed-tools: Bash(git), Read, Write
---

## Purpose

GitMem provides lightweight version control for agent-generated documents during the research workflow. It maintains a separate git repository in `.gitmem/` to track changes without polluting the main project history.

## Commands

### gitmem init --project-root <path>

Initialize a `.gitmem` directory with a separate git repository.

**Behavior:**
- Creates `.gitmem/` directory at project root
- Initializes a bare git repo inside `.gitmem/`
- Configures git user as "GitMem <gitmem@orchestrator>"
- Creates initial commit with empty tree
- Ignores `.gitmem/` in main project's `.gitignore`

**Example:**
```bash
python3 scripts/gitmem.py init --project-root /path/to/project
```

### gitmem commit --project-root <path> --file <file> --message <msg>

Commit a file change to GitMem history.

**Behavior:**
- Stages the specified file (relative to project root)
- Creates a commit with the given message
- Returns commit hash on success

**Tracked directories:**
- `docs/reports/` - Phase deliverables
- `paper/` - Paper drafts and figures
- `code/` - Experiment code
- `agents/` - Agent working notes

**Example:**
```bash
python3 scripts/gitmem.py commit --project-root /path/to/project \
    --file docs/reports/survey/research-readiness-report.md \
    --message "Survey agent: updated readiness report"
```

### gitmem checkpoint --project-root <path> --name <name>

Create a named checkpoint (annotated tag).

**Behavior:**
- Creates an annotated git tag with the given name
- Checkpoint names follow pattern: `<phase>-<substep>-approved`
- Useful for marking stable states before major changes

**Example:**
```bash
python3 scripts/gitmem.py checkpoint --project-root /path/to/project \
    --name "survey-1.1-approved"
```

### gitmem check-loop --project-root <path> --file <file>

Check if a file is in an edit loop (5+ consecutive changes without checkpoint).

**Behavior:**
- Counts commits for the file since last checkpoint
- Returns warning if count >= 5
- Returns JSON with `in_loop` boolean and `change_count` integer

**Example:**
```bash
python3 scripts/gitmem.py check-loop --project-root /path/to/project \
    --file docs/reports/survey/research-readiness-report.md
```

### gitmem history <file>

View version history for a file.

**Behavior:**
- Shows commit hash, date, and message for each version
- Limited to last 20 commits by default

**Example:**
```bash
python3 scripts/gitmem.py history --project-root /path/to/project \
    --file docs/reports/survey/research-readiness-report.md
```

### gitmem diff --project-root <path> --file <file> [--from <rev>] [--to <rev>]

Compare versions of a file.

**Behavior:**
- Shows diff between two revisions
- Defaults to comparing HEAD~1 to HEAD if no revisions specified

**Example:**
```bash
python3 scripts/gitmem.py diff --project-root /path/to/project \
    --file docs/reports/survey/research-readiness-report.md
```

### gitmem rollback --project-root <path> --file <file> [--to <rev>]

Rollback a file to a previous version.

**Behavior:**
- Restores file to specified revision
- Defaults to HEAD~1 if no revision specified
- Creates a new commit with rollback message

**Example:**
```bash
python3 scripts/gitmem.py rollback --project-root /path/to/project \
    --file docs/reports/survey/research-readiness-report.md \
    --to HEAD~3
```

## Integration Points

### Project Initialization

The `init_research_project.py` script calls `gitmem_init()` to set up version tracking when creating a new project.

### Checkpoint Creation

After each substep approval, the orchestrator calls `gitmem_checkpoint()` to mark stable states.

### Loop Guard Monitoring

The `run_stage_loop.py` script calls `gitmem_check_loop()` to detect potential infinite edit cycles and warn the user.

## Key Rules

- All changes are tracked in `.gitmem/` (separate from main project git)
- Checkpoints use annotated tags for easy reference
- Loop detection triggers warning at 5+ consecutive edits
- Rollback creates new commits (never rewrites history)