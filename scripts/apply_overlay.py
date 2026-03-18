from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import PhaseTransitionError
from generate_dashboard import generate_dashboard
from user_library import save_overlay_to_library

from orchestrator_common import append_state_log, load_state, normalize_relative_path, save_state


def activate_overlay(
    project_root: Path,
    overlay_path: str,
    note: str = "",
    require_gate: bool = True,
    scope_roles: list[str] | None = None,
    scope_phases: list[str] | None = None,
    save_to_library: bool = False,
    library_title: str = "",
    library_description: str = "",
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    relative_path = normalize_relative_path(project_root, overlay_path)
    candidate = project_root / relative_path
    if not candidate.exists():
        raise FileNotFoundError(relative_path)

    if require_gate:
        if (
            state["phase_reviews"]["reflection_curator"] != "approved"
            or state["approval_status"]["gate_5"] != "approved"
        ):
            raise PhaseTransitionError(
                "Gate 5 approval and curator approval are required before activating overlays",
                from_phase="05-reflection-evolution",
                to_phase="overlay-activation",
                reason="gate_5_not_approved",
            )

    scope_roles = scope_roles or []
    scope_phases = scope_phases or []
    entry = json.dumps(
        {
            "path": relative_path,
            "roles": scope_roles,
            "phases": scope_phases,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    overlays = list(state.get("overlay_stack", []))
    if entry not in overlays and relative_path not in overlays:
        overlays.append(entry)
    state["overlay_stack"] = overlays
    append_state_log(
        state,
        "human_decisions",
        {
            "type": "overlay_activation",
            "path": relative_path,
            "roles": scope_roles,
            "phases": scope_phases,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    state["progress"]["next_action"] = "overlay-active"
    save_state(project_root, state)
    generate_dashboard(project_root)

    # Save to user library if requested
    library_path = None
    if save_to_library:
        overlay_content = candidate.read_text(encoding="utf-8")
        library_path = save_overlay_to_library(
            overlay_content=overlay_content,
            target_roles=scope_roles,
            target_phases=scope_phases,
            source_project=project_root.name,
            title=library_title or f"Overlay: {relative_path}",
            description=library_description,
        )

    return {
        "project_root": str(project_root),
        "overlay_path": relative_path,
        "scope_roles": scope_roles,
        "scope_phases": scope_phases,
        "status": "active",
        "saved_to_library": save_to_library,
        "library_path": str(library_path) if library_path else None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Activate an approved overlay draft for future prompt rendering."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--overlay-path", required=True)
    parser.add_argument("--note", default="")
    parser.add_argument("--scope-role", action="append", dest="scope_roles")
    parser.add_argument("--scope-phase", action="append", dest="scope_phases")
    parser.add_argument("--skip-approval-check", action="store_true")
    parser.add_argument("--save-to-library", action="store_true",
                        help="Save the overlay to the user-level library for cross-project reuse.")
    parser.add_argument("--library-title", default="",
                        help="Title for the overlay in the library (used with --save-to-library).")
    parser.add_argument("--library-description", default="",
                        help="Description of the overlay (used with --save-to-library).")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = activate_overlay(
        Path(args.project_root),
        overlay_path=args.overlay_path,
        note=args.note,
        require_gate=not args.skip_approval_check,
        scope_roles=args.scope_roles,
        scope_phases=args.scope_phases,
        save_to_library=args.save_to_library,
        library_title=args.library_title,
        library_description=args.library_description,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
