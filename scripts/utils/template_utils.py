"""Template utility functions for AI Research Orchestrator.

Provides template rendering and materialization utilities for project scaffolding.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

# noqa: I001,I004 -- Use simple imports (not scripts.*) for script compatibility
from constants import DEFAULT_DELIVERABLES  # type: ignore[import-untyped]

# Configure module logger
logger = logging.getLogger(__name__)


def build_template_variables(project_root: Path, state: dict[str, Any]) -> dict[str, str]:
    """Build template variables from project state.

    Constructs a dictionary of template variables suitable for rendering
    project templates with project-specific values.

    Args:
        project_root: The root directory of the project.
        state: The project state dictionary.

    Returns:
        A dictionary of template variable names to their string values.
    """
    init_paths = state["init_artifacts"]["detected_paths"]
    if init_paths:
        init_paths_section = "\n".join(f"- `{path}`" for path in init_paths)
    else:
        init_paths_section = (
            "- No client `/init` artifact was detected; "
            "the skill bootstrap owns the initial project files."
        )

    # Safely get deliverable path, fallback to DEFAULT_DELIVERABLES if missing
    def get_deliverable(key: str) -> str:
        deliverables = state.get("deliverables", {})
        return deliverables.get(key, DEFAULT_DELIVERABLES.get(key, f"MISSING_{key}"))

    # Get intent clarification info
    intent_clarification = state.get("intent_clarification", {})

    return {
        "PROJECT_ID": state["project_id"],
        "TOPIC": state["topic"],
        "PROJECT_ROOT": str(project_root),
        "CLIENT_PROFILE": state.get("client_profile", "codex"),
        "CLIENT_INSTRUCTION_FILE": state.get("client_instruction_file", "AGENTS.md"),
        "PROCESS_LANGUAGE": state.get("language_policy", {}).get("process_docs", "zh-CN"),
        "PAPER_LANGUAGE": state.get("language_policy", {}).get("paper_docs", "en-US"),
        "INIT_SOURCE": state["init_artifacts"]["source"],
        "INIT_PATHS_SECTION": init_paths_section,
        "CURRENT_PHASE": state.get("current_phase", "01-survey"),
        "CURRENT_GATE": state.get("current_gate", "gate_1"),
        "PROJECT_CONFIG_PATH": get_deliverable("project_config"),
        "IDEA_BRIEF_PATH": get_deliverable("idea_brief"),
        "REFERENCE_LIBRARY_INDEX_PATH": get_deliverable("reference_library_index"),
        "DASHBOARD_STATUS_PATH": get_deliverable("dashboard_status"),
        "DASHBOARD_PROGRESS_PATH": get_deliverable("dashboard_progress"),
        "JOB_REGISTRY_PATH": get_deliverable("job_registry"),
        "GPU_REGISTRY_PATH": get_deliverable("gpu_registry"),
        "BACKEND_REGISTRY_PATH": get_deliverable("backend_registry"),
        "GATE_1_REPORT_PATH": get_deliverable("readiness_report"),
        "GATE_2_REPORT_PATH": get_deliverable("pilot_validation_report"),
        "GATE_3_REPORT_PATH": get_deliverable("evidence_package_index"),
        "GATE_4_REPORT_PATH": get_deliverable("final_acceptance_report"),
        "GATE_5_REPORT_PATH": get_deliverable("runtime_improvement_report"),
        "CITATION_AUDIT_REPORT_PATH": get_deliverable("citation_audit_report"),
        # Intent clarification variables
        "CLARITY_SCORE": f"{intent_clarification.get('clarity_score', 0.0):.2f}",
        "CLARIFICATION_ROUNDS": str(intent_clarification.get("clarification_rounds", 0)),
        "CLARIFIED_IDEA": intent_clarification.get("clarified_idea", state["topic"]),
        "RESEARCH_TYPE": state.get("research_type", "ml_experiment"),
    }


def render_template_string(template_text: str, variables: dict[str, str]) -> str:
    """Render a template string by replacing {{VARIABLE}} placeholders.

    Args:
        template_text: The template string with {{VARIABLE}} placeholders.
        variables: Dictionary of variable names to their values.

    Returns:
        The rendered string with all placeholders replaced.
    """
    rendered = template_text
    for key, value in variables.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def write_text_if_needed(path: Path, text: str, overwrite: bool = False) -> bool:
    """Write text to a file if needed.

    Args:
        path: The target file path.
        text: The text content to write.
        overwrite: Whether to overwrite existing files.

    Returns:
        True if the file was written, False if it already existed
        and overwrite was False.
    """
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def render_template_tree(
    template_root: Path,
    project_root: Path,
    variables: dict[str, str],
    overwrite: bool = False,
) -> list[Path]:
    """Render all template files in a directory tree.

    Finds all .tmpl files in the template root, renders them with the
    provided variables, and writes them to the project root.

    Args:
        template_root: Root directory containing .tmpl template files.
        project_root: Target directory for rendered files.
        variables: Dictionary of template variable values.
        overwrite: Whether to overwrite existing files.

    Returns:
        List of paths to files that were created/modified.
    """
    created: list[Path] = []
    for template_path in sorted(template_root.rglob("*.tmpl")):
        relative_path = template_path.relative_to(template_root)
        destination = project_root / str(relative_path)[:-5]
        content = render_template_string(template_path.read_text(encoding="utf-8"), variables)
        if write_text_if_needed(destination, content, overwrite=overwrite):
            created.append(destination)
    return created