from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from constants.phases import (
    DEFAULT_DELIVERABLES,
    NEXT_PHASE,
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
)
from orchestrator_common import (
    PHASE_TO_GATE,
    build_list_section,
    build_template_variables,
    ensure_project_structure,
    load_state,
    render_template_string,
)
from user_library import load_all_overlays

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROMPT_ROOT = SKILL_DIR / "assets" / "prompts"

ROLE_TEMPLATE_MAP = {
    "orchestrator": "orchestrator.md.tmpl",
    "survey": "survey.md.tmpl",
    "critic": "critic.md.tmpl",
    "code": "code.md.tmpl",
    "adviser": "adviser.md.tmpl",
    "paper-writer": "paper-writer.md.tmpl",
    "reviewer-editor": "reviewer-editor.md.tmpl",
    "reflector": "reflector.md.tmpl",
    "curator": "curator.md.tmpl",
    "system-auditor": "system-auditor.md.tmpl",
    "project-takeover": "project-takeover.md.tmpl",
}

# Maps role name to the phase it primarily operates in (semantic phase names).
# Roles that span two phases (code, adviser) are mapped to both pilot and experiments;
# for injection purposes we map them to "pilot" as the base phase since experiments
# is the logical continuation — callers can rely on phase_override to be more precise.
ROLE_TO_PHASE = {
    "orchestrator": None,
    "survey": "survey",
    "critic": "survey",
    "code": "pilot",
    "adviser": "pilot",
    "paper-writer": "paper",
    "reviewer-editor": "paper",
    "reflector": "reflection",
    "curator": "reflection",
    "system-auditor": None,
    "project-takeover": None,
}

# Previous phase for each semantic phase (used to locate handoff files).
# Derived from NEXT_PHASE inverse; defined here explicitly for clarity.
PREV_PHASE = {v: k for k, v in NEXT_PHASE.items() if k in NEXT_PHASE}

DEFAULT_MUST_READ = {
    "orchestrator": [
        ".autoresearch/state/research-state.yaml",
        ".autoresearch/idea-brief.md",
        ".autoresearch/dashboard/progress.md",
    ],
    "survey": [
        ".autoresearch/idea-brief.md",
        ".autoresearch/reference-papers/README.md",
        "docs/survey/survey-round-summary.md",
    ],
    "critic": [
        "docs/survey/survey-round-summary.md",
        "docs/survey/critic-round-review.md",
        "docs/survey/research-readiness-report.md",
    ],
    "code": [
        "docs/survey/research-readiness-report.md",
        "docs/pilot/problem-analysis.md",
        "docs/pilot/pilot-validation-report.md",
        "docs/experiments/experiment-spec.md",
    ],
    "adviser": [
        "docs/pilot/pilot-experiment-plan.md",
        "docs/pilot/pilot-results.md",
        "docs/experiments/experiment-spec.md",
        "docs/experiments/results-summary.md",
        "docs/experiments/evidence-package-index.md",
    ],
    "paper-writer": [
        "docs/survey/research-readiness-report.md",
        "docs/pilot/pilot-validation-report.md",
        "docs/experiments/evidence-package-index.md",
        "docs/paper/citation-audit-report.md",
        "paper/paper-draft.md",
    ],
    "reviewer-editor": [
        "docs/experiments/evidence-package-index.md",
        "paper/paper-draft.md",
        "docs/paper/citation-audit-report.md",
        "docs/paper/reviewer-report.md",
        "docs/paper/rebuttal-log.md",
    ],
    "reflector": [
        ".autoresearch/dashboard/progress.md",
        "docs/experiments/evidence-package-index.md",
        "paper/final-acceptance-report.md",
        "docs/reflection/lessons-learned.md",
    ],
    "curator": [
        ".autoresearch/state/research-state.yaml",
        "docs/reflection/lessons-learned.md",
        "docs/reflection/overlay-draft.md",
        "docs/reflection/runtime-improvement-report.md",
    ],
    "system-auditor": [
        "references/gate-rubrics.md",
        "references/experiment-integrity.md",
        "references/paper-quality-assurance.md",
        "references/literature-verification.md",
    ],
    "project-takeover": [
        ".autoresearch/state/research-state.yaml",
        ".autoresearch/idea-brief.md",
        ".autoresearch/workspace-manifest.md",
    ],
}


def _build_state_section(project_root: Path, role: str, phase_override: str | None) -> str:
    """Build a markdown section summarising the current project state.

    Reads .autoresearch/state/research-state.yaml directly (without schema
    validation) so the injection never aborts the render even if the state is
    partially migrated.  Returns an empty string if the file does not exist.
    """
    state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
    if not state_path.exists():
        return ""
    try:
        with state_path.open(encoding="utf-8") as fh:
            state: dict[str, Any] = yaml.safe_load(fh) or {}
    except Exception:
        return ""

    current_phase: str = phase_override or state.get("current_phase", "unknown")
    current_gate: str = state.get("current_gate", "unknown")

    # Gate / review approval for the active phase
    approval_status: dict[str, Any] = state.get("approval_status", {})
    phase_reviews: dict[str, Any] = state.get("phase_reviews", {})

    # Gate key for the current phase
    gate_key = PHASE_TO_GATE.get(current_phase, "")
    gate_status = approval_status.get(gate_key, "unknown") if gate_key else "unknown"

    # Loop iteration count for the current phase
    loop_counts: dict[str, Any] = state.get("loop_counts", {})
    loop_key = PHASE_LOOP_KEY.get(current_phase, "")
    loop_iteration = loop_counts.get(loop_key, 0) if loop_key else 0

    lines = [
        "## Current Project State",
        "",
        f"- **Current phase**: {current_phase}",
        f"- **Current gate**: {current_gate}",
        f"- **Gate status** ({gate_key or 'n/a'}): {gate_status}",
        f"- **Loop iteration** ({loop_key or 'n/a'}): {loop_iteration}",
    ]

    # Include all gate statuses for broader context
    if approval_status:
        lines.append("- **All gate statuses**:")
        for gate, status in approval_status.items():
            lines.append(f"  - {gate}: {status}")

    # Include all phase review statuses
    if phase_reviews:
        lines.append("- **Phase review statuses**:")
        for review, status in phase_reviews.items():
            lines.append(f"  - {review}: {status}")

    return "\n".join(lines)


def _build_handoff_section(project_root: Path, role: str, phase_override: str | None) -> str:
    """Build a markdown section containing the previous-phase handoff summary.

    Probes several candidate locations in priority order:
      1. 00-admin/runtime/handoff-summaries/<prev_phase>-<agent>-handoff.yaml
         (primary path written by phase_handoff.py; tries all agents for that phase)
      2. .autoresearch/state/handoff-<prev_phase>.yaml
      3. .autoresearch/state/handoff-<prev_phase>.md
      4. docs/<prev_phase>/handoff-summary.md

    Returns an empty string if nothing is found.
    """
    # Determine the current role's phase then derive the previous phase
    role_phase = ROLE_TO_PHASE.get(role)
    if role_phase is None and phase_override:
        role_phase = phase_override
    if role_phase is None:
        return ""

    active_phase = phase_override or role_phase
    prev_phase = PREV_PHASE.get(active_phase, "")
    if not prev_phase:
        return ""

    # 1. Check the canonical handoff-summaries directory for any agent of prev_phase
    handoff_dir = project_root / ".autoresearch" / "runtime" / "handoff-summaries"
    if handoff_dir.exists():
        # Collect all YAML files matching <prev_phase>-*-handoff.yaml
        candidates = sorted(handoff_dir.glob(f"{prev_phase}-*-handoff.yaml"))
        if candidates:
            # Use the most recently modified file
            candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            try:
                with candidates[0].open(encoding="utf-8") as fh:
                    data: dict[str, Any] = yaml.safe_load(fh) or {}
                return _format_yaml_handoff_as_section(data, candidates[0].name)
            except Exception:
                pass

    # 2. .autoresearch/state/handoff-<prev_phase>.yaml
    for ext in (".yaml", ".md"):
        candidate = project_root / ".autoresearch" / "state" / f"handoff-{prev_phase}{ext}"
        if candidate.exists():
            try:
                text = candidate.read_text(encoding="utf-8").strip()
                if text:
                    return f"## Previous Phase Handoff\n\n{text}"
            except Exception:
                pass

    # 3. docs/<prev_phase>/handoff-summary.md
    candidate = project_root / "docs" / prev_phase / "handoff-summary.md"
    if candidate.exists():
        try:
            text = candidate.read_text(encoding="utf-8").strip()
            if text:
                return f"## Previous Phase Handoff\n\n{text}"
        except Exception:
            pass

    return ""


def _format_yaml_handoff_as_section(data: dict[str, Any], filename: str) -> str:
    """Render a YAML handoff dict as a readable markdown section."""
    lines = [
        "## Previous Phase Handoff",
        "",
        f"*Source: {filename}*",
        "",
    ]

    phase = data.get("phase", "")
    agent = data.get("agent_role", "")
    ts = data.get("metadata", {}).get("timestamp", "")
    if phase or agent:
        lines.append(f"**Phase**: {phase}  **Agent**: {agent}  **Saved**: {ts}")
        lines.append("")

    field_labels = [
        ("key_findings", "Key Findings"),
        ("decisions_made", "Decisions Made"),
        ("deliverables_status", "Deliverables Status"),
        ("open_issues", "Open Issues"),
        ("blockers", "Blockers"),
        ("recommendations_for_next_phase", "Recommendations for Next Phase"),
        ("context_for_resume", "Context for Resume"),
    ]
    for key, label in field_labels:
        value = data.get(key)
        if not value:
            continue
        lines.append(f"**{label}**:")
        if isinstance(value, list):
            for item in value:
                lines.append(f"- {item}")
        elif isinstance(value, dict):
            for k, v in value.items():
                lines.append(f"- {k}: {v}")
        else:
            lines.append(str(value))
        lines.append("")

    return "\n".join(lines)


def _build_deliverables_section(role: str, phase_override: str | None) -> str:
    """Build a markdown checklist of required deliverables for the role's phase.

    Uses PHASE_REQUIRED_DELIVERABLES to get deliverable keys for the phase and
    resolves their file paths via DEFAULT_DELIVERABLES.
    Returns an empty string if the role has no mapped phase.
    """
    role_phase = ROLE_TO_PHASE.get(role)
    if role_phase is None and phase_override:
        role_phase = phase_override
    if role_phase is None:
        return ""

    active_phase = phase_override or role_phase
    deliverable_keys = PHASE_REQUIRED_DELIVERABLES.get(active_phase)
    if not deliverable_keys:
        return ""

    lines = [
        "## Required Deliverables Checklist",
        "",
        f"Phase: **{active_phase}**",
        "",
    ]
    for key in deliverable_keys:
        path = DEFAULT_DELIVERABLES.get(key, "(path unknown)")
        lines.append(f"- [ ] `{key}`: `{path}`")

    return "\n".join(lines)


def render_agent_prompt(
    project_root: Path,
    role: str,
    task_summary: str,
    current_objective: str = "",
    phase_override: str | None = None,
    loop_label: str = "",
    required_inputs: list[str] | None = None,
    must_read: list[str] | None = None,
    extra_instructions: list[str] | None = None,
    inject_state: bool = True,
    inject_handoff: bool = True,
    inject_deliverables: bool = True,
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    effective_phase = phase_override or state["current_phase"]
    effective_gate = PHASE_TO_GATE.get(
        effective_phase, "complete" if effective_phase == "06-archive" else state["current_gate"]
    )
    template_name = ROLE_TEMPLATE_MAP[role]
    template_path = PROMPT_ROOT / template_name
    template_text = template_path.read_text(encoding="utf-8")

    required_inputs = required_inputs or []
    must_read = must_read or list(DEFAULT_MUST_READ[role])
    extra_instructions = extra_instructions or []

    variables = build_template_variables(project_root, state)
    variables.update(
        {
            "ROLE_NAME": role,
            "CURRENT_PHASE": effective_phase,
            "CURRENT_GATE": effective_gate,
            "TASK_SUMMARY": task_summary,
            "CURRENT_OBJECTIVE": current_objective
            or "Follow the current phase objective without inventing scope.",
            "LOOP_LABEL": loop_label or "default",
            "REQUIRED_INPUTS_SECTION": build_list_section(
                required_inputs,
                "No extra required inputs were supplied by the orchestrator.",
            ),
            "MUST_READ_SECTION": build_list_section(must_read, "No mandatory files were supplied."),
            "EXTRA_INSTRUCTIONS_SECTION": build_list_section(
                extra_instructions,
                "No extra orchestration instructions were supplied.",
            ),
        }
    )
    prompt = render_template_string(template_text, variables)
    prompt_phase = phase_override or state["current_phase"]
    overlay_text = _build_overlay_section(project_root, state, role, prompt_phase)
    if overlay_text:
        prompt = prompt + "\n\n## Approved Overlays\n\n" + overlay_text

    # --- Auto-injection of state, handoff, and deliverables (additive) ---
    if inject_state:
        state_section = _build_state_section(project_root, role, phase_override)
        if state_section:
            prompt = prompt + "\n\n" + state_section

    if inject_handoff:
        handoff_section = _build_handoff_section(project_root, role, phase_override)
        if handoff_section:
            prompt = prompt + "\n\n" + handoff_section

    if inject_deliverables:
        deliverables_section = _build_deliverables_section(role, phase_override)
        if deliverables_section:
            prompt = prompt + "\n\n" + deliverables_section

    return {
        "role": role,
        "project_root": str(project_root),
        "template": template_name,
        "prompt": prompt,
        "must_read": must_read,
        "required_inputs": required_inputs,
        "extra_instructions": extra_instructions,
        "overlay_count": len(state.get("overlay_stack", [])),
    }


def _build_overlay_section(
    project_root: Path, state: dict[str, object], role: str, phase_name: str
) -> str:
    overlay_paths = state.get("overlay_stack", [])
    sections: list[str] = []

    # 1. Project-level overlays
    for raw_entry in overlay_paths:
        entry = _parse_overlay_entry(raw_entry)
        if entry["roles"] and role not in entry["roles"]:
            continue
        if entry["phases"] and phase_name not in entry["phases"]:
            continue
        candidate = project_root / entry["path"]
        if not candidate.exists():
            continue
        text = candidate.read_text(encoding="utf-8").strip()
        if not text:
            continue
        sections.append(f"### `{entry['path']}`\n\n{text}")

    # 2. User library overlays (cross-project reusable overlays)
    try:
        for overlay in load_all_overlays():
            if overlay["roles"] and role not in overlay["roles"]:
                continue
            if overlay["phases"] and phase_name not in overlay["phases"]:
                continue
            content = overlay.get("content", "")
            if not content:
                continue
            overlay_id = overlay.get("id", "unknown")
            overlay_title = overlay.get("title", "User Library Overlay")
            sections.append(f"### User Library: `{overlay_id}` - {overlay_title}\n\n{content}")
    except Exception:
        # If user library is not available, continue without it
        pass

    return "\n\n".join(sections)


def _parse_overlay_entry(raw_entry: object) -> dict[str, object]:
    if isinstance(raw_entry, str) and raw_entry.startswith("{"):
        payload = json.loads(raw_entry)
        return {
            "path": str(payload["path"]),
            "roles": list(payload.get("roles", [])),
            "phases": list(payload.get("phases", [])),
        }
    return {"path": str(raw_entry), "roles": [], "phases": []}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a role prompt from the fixed template plus orchestrator context."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--role", required=True, choices=sorted(ROLE_TEMPLATE_MAP))
    parser.add_argument("--task-summary", required=True)
    parser.add_argument("--current-objective", default="")
    parser.add_argument("--phase-override")
    parser.add_argument("--loop-label", default="")
    parser.add_argument("--required-input", action="append", dest="required_inputs")
    parser.add_argument("--must-read", action="append", dest="must_read")
    parser.add_argument("--extra-instruction", action="append", dest="extra_instructions")
    parser.add_argument("--json", action="store_true")
    # Auto-injection flags (all default to True; pass --no-inject-* to disable)
    parser.add_argument(
        "--inject-state",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Auto-inject current project state from research-state.yaml (default: True)",
    )
    parser.add_argument(
        "--inject-handoff",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Auto-inject previous phase handoff summary (default: True)",
    )
    parser.add_argument(
        "--inject-deliverables",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Auto-inject required deliverables checklist for the role (default: True)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = render_agent_prompt(
        project_root=project_root,
        role=args.role,
        task_summary=args.task_summary,
        current_objective=args.current_objective,
        phase_override=args.phase_override,
        loop_label=args.loop_label,
        required_inputs=args.required_inputs,
        must_read=args.must_read,
        extra_instructions=args.extra_instructions,
        inject_state=args.inject_state,
        inject_handoff=args.inject_handoff,
        inject_deliverables=args.inject_deliverables,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
