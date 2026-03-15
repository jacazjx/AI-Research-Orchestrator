from __future__ import annotations

import argparse
import json
from pathlib import Path

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
    normalize_relative_path,
    render_template_tree,
    slugify,
    write_text_if_needed,
    write_yaml,
)

# New semantic phase names
VALID_PHASES = ["survey", "pilot", "experiments", "paper", "reflection"]

# Legacy phase names for backward compatibility
VALID_PHASES_LEGACY = [
    "01-survey",
    "02-pilot-analysis",
    "03-full-experiments",
    "04-paper",
    "05-reflection-evolution",
]

# Combined valid phases for argument parsing
ALL_VALID_PHASES = VALID_PHASES + VALID_PHASES_LEGACY

# Phase name normalization mapping (legacy -> new)
PHASE_NAME_MAP = {
    "01-survey": "survey",
    "02-pilot-analysis": "pilot",
    "03-full-experiments": "experiments",
    "04-paper": "paper",
    "05-reflection-evolution": "reflection",
}


def normalize_phase_name(phase: str) -> str:
    """Normalize phase name from legacy to new semantic format.

    Args:
        phase: Phase name (legacy or new format)

    Returns:
        Normalized phase name in new semantic format
    """
    return PHASE_NAME_MAP.get(phase, phase)


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
    "docs/reports/survey",
    "docs/reports/pilot",
    "docs/reports/experiments",
    "docs/reports/paper",
    "docs/reports/reflection",
)


def detect_codex_mcp() -> bool:
    """Check if Codex MCP is available.

    This performs a static config check. Actual tool availability
    is determined at runtime by the client, but this provides
    a reasonable heuristic for setup suggestions.

    Returns:
        True if Codex MCP appears to be configured.
    """
    # Check for Claude Code MCP config
    claude_config = Path.home() / ".claude" / "mcp.json"
    if claude_config.exists():
        try:
            config = json.loads(claude_config.read_text())
            mcp_servers = config.get("mcpServers", {})
            # Check for codex server in various possible names
            for name in ["codex", "openai", "openai-codex"]:
                if name in mcp_servers:
                    return True
        except Exception:
            pass

    return False


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
) -> dict[str, object]:
    # Normalize phase name (convert legacy to new format)
    normalized_phase = normalize_phase_name(starting_phase)

    # Ensure project structure using new directory layout
    ensure_project_structure(project_root, create_if_missing=True)

    # Create main work subdirectories
    for subdir in MAIN_WORK_SUBDIRECTORIES:
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
    parser.add_argument(
        "--topic", default="TODO: replace with the research idea or problem statement"
    )
    parser.add_argument(
        "--project-id", help="Optional stable project id. Defaults to the project directory slug."
    )
    parser.add_argument(
        "--client-type",
        default="auto",
        choices=("auto", "codex", "claude"),
        help="Generate the client instruction file for Codex (AGENTS.md) or Claude (CLAUDE.md).",
    )
    parser.add_argument("--process-language", default=DEFAULT_LANGUAGE_POLICY["process_docs"])
    parser.add_argument("--paper-language", default=DEFAULT_LANGUAGE_POLICY["paper_docs"])
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
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    # Normalize phase name before passing to initialize_research_project
    normalized_phase = normalize_phase_name(args.starting_phase)
    result = initialize_research_project(
        project_root=Path(args.project_root),
        topic=args.topic,
        project_id=args.project_id,
        client_type=args.client_type,
        process_language=args.process_language,
        paper_language=args.paper_language,
        overwrite_templates=args.overwrite_templates,
        explicit_init_paths=args.client_init_paths,
        starting_phase=normalized_phase,
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

        # Codex MCP detection and suggestion
        codex_available = detect_codex_mcp()
        if not codex_available:
            print("")
            print("ℹ️  Cross-model review (Codex MCP) not detected.")
            print("   To enable external LLM review, configure Codex MCP:")
            print("   See: https://github.com/openai/codex")
            print("   This allows higher quality feedback via cross-model review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
