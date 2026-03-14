# Citation Authenticity

Paper-phase citation handling follows these rules:

- `Paper Writer` should use the local `latex-citation-curator` tool whenever a claim needs external support.
- Verified formal publications should replace preprints whenever possible.
- `Reviewer & Editor` must audit citation realism, support quality, and whether the citation audit report matches the manuscript.
- Gate 4 should not pass when citation authenticity remains unresolved.

Operational entry point:

- `scripts/run_citation_audit.py`

Primary external support comes from the local skill:

- [$latex-citation-curator](/mnt/c/Users/10848/.codex/skills/latex-citation-curator/SKILL.md)
