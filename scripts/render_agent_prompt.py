from __future__ import annotations

import argparse
import json
from pathlib import Path

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

DEFAULT_MUST_READ = {
    "orchestrator": [
        "00-admin/research-state.yaml",
        "00-admin/idea-brief.md",
        "00-admin/dashboard/progress.md",
    ],
    "survey": [
        "00-admin/idea-brief.md",
        "00-admin/reference-papers/README.md",
        "01-survey/survey-round-summary.md",
    ],
    "critic": [
        "01-survey/survey-round-summary.md",
        "01-survey/critic-round-review.md",
        "01-survey/research-readiness-report.md",
    ],
    "code": [
        "01-survey/research-readiness-report.md",
        "02-pilot-analysis/problem-analysis.md",
        "02-pilot-analysis/pilot-validation-report.md",
        "03-full-experiments/experiment-spec.md",
    ],
    "adviser": [
        "02-pilot-analysis/pilot-experiment-plan.md",
        "02-pilot-analysis/pilot-results.md",
        "03-full-experiments/experiment-spec.md",
        "03-full-experiments/results-summary.md",
        "03-full-experiments/evidence-package-index.md",
    ],
    "paper-writer": [
        "01-survey/research-readiness-report.md",
        "02-pilot-analysis/pilot-validation-report.md",
        "03-full-experiments/evidence-package-index.md",
        "04-paper/citation-audit-report.md",
        "04-paper/paper-draft.md",
    ],
    "reviewer-editor": [
        "03-full-experiments/evidence-package-index.md",
        "04-paper/paper-draft.md",
        "04-paper/citation-audit-report.md",
        "04-paper/reviewer-report.md",
        "04-paper/rebuttal-log.md",
    ],
    "reflector": [
        "00-admin/dashboard/progress.md",
        "03-full-experiments/evidence-package-index.md",
        "04-paper/final-acceptance-report.md",
        "05-reflection-evolution/lessons-learned.md",
    ],
    "curator": [
        "00-admin/research-state.yaml",
        "05-reflection-evolution/lessons-learned.md",
        "05-reflection-evolution/overlay-draft.md",
        "05-reflection-evolution/runtime-improvement-report.md",
    ],
    "system-auditor": [
        "references/gate-rubrics.md",
        "references/experiment-integrity.md",
        "references/paper-quality-assurance.md",
        "references/literature-verification.md",
    ],
    "project-takeover": [
        "00-admin/research-state.yaml",
        "00-admin/idea-brief.md",
        "00-admin/workspace-manifest.md",
    ],
}


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
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
