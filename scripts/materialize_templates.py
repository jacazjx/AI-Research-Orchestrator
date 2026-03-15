from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    build_template_variables,
    ensure_project_structure,
    load_state,
    render_template_tree,
)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_ROOT = SKILL_DIR / "assets" / "templates"


def materialize_project_templates(project_root: Path, overwrite: bool = False) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    variables = build_template_variables(project_root, state)
    rendered_files = render_template_tree(
        TEMPLATE_ROOT, project_root, variables, overwrite=overwrite
    )
    return {
        "project_root": str(project_root),
        "state_path": DEFAULT_DELIVERABLES["research_state"],
        "overwrite": overwrite,
        "rendered_files": [path.relative_to(project_root).as_posix() for path in rendered_files],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Materialize the standard workspace templates into a project."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--overwrite", action="store_true", help="Rewrite existing template files.")
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = materialize_project_templates(project_root, overwrite=args.overwrite)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Project root: {result['project_root']}")
        print(f"State file: {result['state_path']}")
        print(f"Overwrite existing files: {result['overwrite']}")
        if result["rendered_files"]:
            print("Rendered templates:")
            for path in result["rendered_files"]:
                print(f"- {path}")
        else:
            print("Rendered templates: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
