from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from constants.phases import (
    LEGACY_TO_SEMANTIC_PHASE,
    PHASE_SEQUENCE,
    get_phase_sequence_for_research_type,
)
from user_config import load_user_config

from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    DEFAULT_LANGUAGE_POLICY,
    PHASE_TO_GATE,
    build_client_instruction_text,
    build_state,
    build_template_variables,
    detect_client_init_artifacts,
    detect_client_profile,
    ensure_project_structure,
    gitmem_init,
    normalize_phase_name,
    normalize_relative_path,
    render_template_tree,
    slugify,
    warn_starting_phase_prerequisites,
    write_text_if_needed,
    write_yaml,
)

try:
    from preflight import format_preflight_warnings, run_preflight_checks

    PREFLIGHT_AVAILABLE = True
except ImportError:
    PREFLIGHT_AVAILABLE = False

# Combined valid phases for argument parsing (semantic + legacy)
ALL_VALID_PHASES = list(PHASE_SEQUENCE) + list(LEGACY_TO_SEMANTIC_PHASE.keys())

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_ROOT = SKILL_DIR / "assets" / "templates"


# Subdirectories for main work areas
MAIN_WORK_SUBDIRECTORIES = (
    "paper/sections",
    "paper/figures",
    "code/src",
    "code/experiments",
    "code/configs",
    "code/checkpoints",
    "docs/survey",
    "docs/pilot",
    "docs/experiments",
    "docs/paper",
    "docs/reflection",
)

# Agent workspace subdirectories (created under each agent directory)
AGENT_WORK_SUBDIRECTORIES = tuple(
    f"agents/{agent}/{subdir}"
    for agent in (
        "survey",
        "critic",
        "coder",
        "adviser",
        "writer",
        "reviewer",
        "reflector",
        "curator",
    )
    for subdir in ("workspace", "battle", "output")
)


def initialize_research_project(
    project_root: Path,
    topic: str,
    project_id: str | None = None,
    client_type: str = "auto",
    process_language: str = DEFAULT_LANGUAGE_POLICY["process_docs"],
    paper_language: str = DEFAULT_LANGUAGE_POLICY["paper_docs"],
    overwrite_templates: bool = False,
    explicit_init_paths: list[str] | None = None,
    starting_phase: str = "survey",
    research_type: str = "ml_experiment",
    compute_config: dict[str, Any] | None = None,
    user_profile: dict[str, Any] | None = None,
    existing_resources_mode: str | None = None,
) -> dict[str, object]:
    """Initialize a research project.

    All parameters are accepted directly (no interactive collection).

    Args:
        project_root: Path to the project directory.
        topic: Research topic or idea.
        project_id: Optional project identifier.
        client_type: Client type (auto, claude, codex).
        process_language: Language for process documents.
        paper_language: Language for paper documents.
        overwrite_templates: Whether to overwrite existing templates.
        explicit_init_paths: Explicit initialization paths.
        starting_phase: Starting phase for the project.
        research_type: Type of research (ml_experiment, theory, survey, applied).
        compute_config: Compute configuration.
        user_profile: User profile.
        existing_resources_mode: How to handle existing files
            ("preserve", "migrate", or "cancel").

    Returns:
        Dictionary with initialization results.
    """
    # Normalize phase name (convert legacy to new format)
    normalized_phase = normalize_phase_name(starting_phase)

    # Handle non-empty directory (only if directory exists and is non-empty)
    if project_root.exists() and any(project_root.iterdir()):
        mode = existing_resources_mode or "preserve"
        if mode == "cancel":
            return {"status": "cancelled", "message": "Initialization cancelled by user"}
        logging.warning(
            "Directory '%s' is not empty. Existing files will be preserved.", project_root
        )

    # Ensure project structure using new directory layout
    ensure_project_structure(project_root, create_if_missing=True)

    # Advisory preflight checks -- never raises, never blocks
    # Skip during test runs to avoid live network calls causing test interference
    _in_test = "pytest" in sys.modules
    if PREFLIGHT_AVAILABLE and not _in_test:
        try:
            preflight_results = run_preflight_checks()
            warning_text = format_preflight_warnings(preflight_results)
            if warning_text:
                print(warning_text)
        except Exception:  # noqa: BLE001
            pass  # preflight must never break initialization

    # Create main work subdirectories
    for subdir in MAIN_WORK_SUBDIRECTORIES:
        (project_root / subdir).mkdir(parents=True, exist_ok=True)

    # Create agent workspace subdirectories
    for subdir in AGENT_WORK_SUBDIRECTORIES:
        (project_root / subdir).mkdir(parents=True, exist_ok=True)

    # Initialize GitMem for version tracking
    gitmem_init(project_root)

    if explicit_init_paths is None:
        init_paths = detect_client_init_artifacts(project_root)
    else:
        init_paths = [normalize_relative_path(project_root, path) for path in explicit_init_paths]

    init_source = "client-init" if init_paths else "skill-bootstrap"
    client_profile = detect_client_profile(project_root, init_paths, client_type)
    client_instruction_file = "CLAUDE.md" if client_profile == "claude" else "AGENTS.md"
    project_identifier = project_id or slugify(project_root.name)

    # Load and merge user config
    user_config_inherited: dict[str, Any] = {}
    try:
        user_cfg = load_user_config()
        if user_cfg:
            user_config_inherited = {
                "author": user_cfg.get("author", {}),
                "preferences": user_cfg.get("preferences", {}),
            }
    except Exception as e:
        logging.warning(f"Could not load user config: {e}")

    state = build_state(
        project_id=project_identifier,
        topic=topic,
        init_source=init_source,
        init_paths=init_paths,
        client_profile=client_profile,
        client_instruction_file=client_instruction_file,
        process_language=process_language,
        paper_language=paper_language,
        starting_phase=normalized_phase,
    )

    # Update state with additional fields
    state["research_type"] = research_type
    state["phase_sequence"] = list(get_phase_sequence_for_research_type(research_type))
    state["user_config_inherited"] = user_config_inherited
    if compute_config:
        state["compute_config"] = compute_config
    if user_profile:
        state["user_profile"] = user_profile

    prereq_warnings = warn_starting_phase_prerequisites(starting_phase)
    if prereq_warnings:
        for w in prereq_warnings:
            logging.warning(w)

    variables = build_template_variables(project_root, state)
    rendered_files = render_template_tree(
        TEMPLATE_ROOT, project_root, variables, overwrite=overwrite_templates
    )
    write_yaml(project_root / DEFAULT_DELIVERABLES["research_state"], state)
    instruction_path = project_root / client_instruction_file
    instruction_text = build_client_instruction_text(client_profile, state)
    instruction_created = write_text_if_needed(
        instruction_path, instruction_text, overwrite=overwrite_templates
    )

    return {
        "project_root": str(project_root),
        "project_id": project_identifier,
        "init_source": init_source,
        "client_profile": client_profile,
        "client_instruction_file": client_instruction_file,
        "init_paths": init_paths,
        "rendered_files": [path.relative_to(project_root).as_posix() for path in rendered_files],
        "state_path": DEFAULT_DELIVERABLES["research_state"],
        "instruction_written": instruction_created,
        "starting_phase": normalized_phase,
        "starting_gate": PHASE_TO_GATE.get(normalized_phase, "gate_1"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a gated AI research workspace.")
    parser.add_argument(
        "--project-root", required=True, help="Path to the target research project root."
    )
    parser.add_argument("--topic", required=True, help="Research idea or problem statement.")
    parser.add_argument(
        "--project-id", help="Optional stable project id. Defaults to the project directory slug."
    )
    parser.add_argument(
        "--client-type",
        default="auto",
        choices=("auto", "codex", "claude"),
        help="Generate the client instruction file for Codex (AGENTS.md) or Claude (CLAUDE.md).",
    )
    parser.add_argument(
        "--process-language",
        default=os.environ.get(
            "AUTORESEARCH_PROCESS_LANGUAGE", DEFAULT_LANGUAGE_POLICY["process_docs"]
        ),
    )
    parser.add_argument(
        "--paper-language",
        default=os.environ.get(
            "AUTORESEARCH_PAPER_LANGUAGE", DEFAULT_LANGUAGE_POLICY["paper_docs"]
        ),
    )
    parser.add_argument(
        "--overwrite-templates", action="store_true", help="Rewrite existing template files."
    )
    parser.add_argument(
        "--client-init-path",
        action="append",
        dest="client_init_paths",
        help="Explicit client /init artifact path relative to the project root. Repeat as needed.",
    )
    parser.add_argument(
        "--starting-phase",
        default="survey",
        choices=ALL_VALID_PHASES,
        help="Phase to start the project at. Use for resuming work or skipping completed phases.",
    )
    parser.add_argument(
        "--research-type",
        default=os.environ.get("AUTORESEARCH_DEFAULT_RESEARCH_TYPE", "ml_experiment"),
        choices=["ml_experiment", "theory", "survey", "applied"],
        help="Type of research project.",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root)

    # Normalize phase name before passing to initialize_research_project
    normalized_phase = normalize_phase_name(args.starting_phase)

    result = initialize_research_project(
        project_root=project_root,
        topic=args.topic,
        project_id=args.project_id,
        client_type=args.client_type,
        process_language=args.process_language,
        paper_language=args.paper_language,
        overwrite_templates=args.overwrite_templates,
        explicit_init_paths=args.client_init_paths,
        starting_phase=normalized_phase,
        research_type=args.research_type,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Project root: {result['project_root']}")
        print(f"Project id: {result['project_id']}")
        print(f"Initialization source: {result['init_source']}")
        print(f"Client profile: {result['client_profile']}")
        print(f"Client instruction file: {result['client_instruction_file']}")
        print(f"Starting phase: {result['starting_phase']}")
        print(f"Starting gate: {result['starting_gate']}")
        if result["init_paths"]:
            print("Recorded client init artifacts:")
            for path in result["init_paths"]:
                print(f"- {path}")
        else:
            print("Recorded client init artifacts: none")
        print(f"State file: {result['state_path']}")
        print(f"Instruction file written: {result['instruction_written']}")
        print("Rendered templates:")
        for path in result["rendered_files"]:
            print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
