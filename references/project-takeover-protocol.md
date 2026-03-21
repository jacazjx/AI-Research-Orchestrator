# Project Takeover Protocol

Edge-case guidance for adopting existing projects into the orchestrator. Standard project initialization and state reload are handled by `init_research_project.py` and the `reload` skill. This document covers scenarios those tools do not fully automate.

---

## When to Use This Protocol

- Inheriting a project from another researcher with scattered artifacts
- Adopting a legacy project with no documentation structure
- Resuming a project where experiment records are incomplete or ambiguous
- Resolving state-file conflicts after partial migration

## Phase Estimation

| Evidence Found | Estimated Starting Phase |
|----------------|--------------------------|
| Nothing | Initialize from scratch |
| Literature notes only | `survey` |
| Pilot code or results | `pilot` |
| Full experiment results | `experiments` |
| Paper draft | `paper` |
| Published paper | `reflection` |

## Starting Phase

When taking over a project, specify the starting phase to skip completed work:

```bash
python3 scripts/init_research_project.py \
  --project-root /path/to/project \
  --topic "Topic" \
  --starting-phase experiments
```

## Edge Cases

### Scattered Artifacts, No Clear Structure

1. Have the orchestrator analyze the directory structure
2. Run `init_research_project.py` to create the standard structure
3. Manually map existing files to target locations:

| Source Pattern | Target Location |
|----------------|-----------------|
| *.bib, papers/*.pdf | .autoresearch/reference-papers/ |
| survey*.md, literature*.md | docs/survey/ |
| pilot*.py, pilot*.md | code/pilot/ |
| experiment*.py, results*.md | code/experiments/ |
| paper*.tex, draft*.md | paper/ |

4. Set state phase to match the most advanced completed work

### Paper Draft Exists, No Experiment Documentation

1. Import paper to `paper/`
2. Reconstruct experiment documentation from code and logs
3. Set phase based on paper completeness (usually `paper`)
4. Run quality gate to identify gaps before continuing

### State File Conflicts

Use `--dry-run` first. If conflicts exist between existing state and reality:
- Back up the existing state file
- Re-run migration with the correct `--starting-phase`
- Verify state alignment with `quality_gate.py`

### Multiple Paper Drafts

Identify the most recent/complete version. Archive others to `.autoresearch/archive/`.

## Post-Takeover Verification

1. Run the orchestrator's session-start hook (automatic on next session)
2. Run `quality_gate.py --phase <current_phase>` to check deliverable completeness
3. Review with the researcher: confirm phase, identify gaps, agree on next steps
