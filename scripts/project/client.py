"""Platform detection and client configuration."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from constants import DEFAULT_DELIVERABLES, DEFAULT_LOOP_LIMITS

from utils import read_yaml

logger = logging.getLogger(__name__)

# Language policy defaults
DEFAULT_LANGUAGE_POLICY = {
    "process_docs": "zh-CN",
    "paper_docs": "en-US",
}

# Default reviewer config
DEFAULT_REVIEWER_CONFIG = {
    "model": "gpt-5.4",
    "reasoning_effort": "xhigh",
    "enabled": False,
}

DEFAULT_RUNTIME_CONFIG = {
    "languages": dict(DEFAULT_LANGUAGE_POLICY),
    "loop_limits": dict(DEFAULT_LOOP_LIMITS),
    "runtime": {
        "stale_after_minutes": 30,
        "auto_discover_gpu": True,
    },
    "backends": {
        "local": "enabled",
        "ssh": "enabled",
    },
    "reviewer": dict(DEFAULT_REVIEWER_CONFIG),
}


def detect_platform() -> str:
    """Detect the current running platform.

    Returns:
        Platform name: "claude-code", "codex", or "unknown".
    """
    if os.environ.get("CLAUDE_CODE"):
        return "claude-code"
    if os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        return "codex"
    return "claude-code"


def select_client_template(platform: str, template_root: Path) -> Path | None:
    """Select the appropriate client instruction template.

    Args:
        platform: Platform name.
        template_root: Root directory for templates.

    Returns:
        Path to the appropriate template file, or None if not found.
    """
    template_name = (
        "CLAUDE.md.tmpl" if platform in ("claude-code", "claude") else "AGENTS.md.tmpl"
    )
    template_path = template_root / "project-root" / template_name

    if not template_path.exists():
        logger.warning(f"Template not found: {template_path}, using default")
        return None

    return template_path


def detect_client_profile(
    project_root: Path, init_paths: list[str], client_type: str
) -> str:
    """Detect the client profile based on existing files or explicit type.

    Args:
        project_root: Project root directory.
        init_paths: List of detected init artifact paths.
        client_type: Explicit client type ("codex", "claude", or "auto").

    Returns:
        Detected client profile name.
    """
    if client_type in {"codex", "claude"}:
        return client_type

    candidates = [Path(path).name for path in init_paths]
    if (project_root / "CLAUDE.md").exists() or "CLAUDE.md" in candidates:
        return "claude"
    if (project_root / "AGENTS.md").exists() or "AGENTS.md" in candidates:
        return "codex"
    return "codex"


def build_client_instruction_text(client_profile: str, state: dict[str, Any]) -> str:
    """Build the client instruction text for AGENTS.md or CLAUDE.md.

    Args:
        client_profile: Client profile name ("codex" or "claude").
        state: Project state dictionary.

    Returns:
        Client instruction text.
    """
    filename = "CLAUDE.md" if client_profile == "claude" else "AGENTS.md"
    return "\n".join(
        [
            f"# {filename}",
            "",
            "This workspace is initialized by the ai-research-orchestrator skill.",
            "",
            "## Core contracts",
            "",
            f"- Machine-readable state: `{DEFAULT_DELIVERABLES['research_state']}`",
            f"- Human-readable manifest: `{DEFAULT_DELIVERABLES['workspace_manifest']}`",
            f"- User IDEA template: `{DEFAULT_DELIVERABLES['idea_brief']}`",
            f"- User reference library: `{DEFAULT_DELIVERABLES['reference_library_index']}`",
            f"- Dashboard status: `{DEFAULT_DELIVERABLES['dashboard_progress']}`",
            "",
            "## Required phases",
            "",
            "- Phase 1: Survey <-> Critic",
            "- Phase 2: Pilot Code <-> Pilot Adviser",
            "- Phase 3: Experiment Code <-> Experiment Adviser",
            "- Phase 4: Paper Writer <-> Reviewer & Editor",
            "- Phase 5: Reflector <-> Curator",
            "",
            "## Required gates",
            "",
            "- Gate 1: research-readiness report approved by the user",
            "- Gate 2: pilot validation pack approved by the user",
            "- Gate 3: experiment evidence package approved by the user",
            "- Gate 4: paper package approved by the user",
            "- Gate 5: reflection/evolution package approved by the user "
            "before overlays or policy changes apply",
            "",
            "## Runtime rules",
            "",
            "- Keep every phase as a two-agent loop under the user-facing orchestrator.",
            "- Update dashboard and runtime registries as phase status changes.",
            "- Do not bypass `research-state.yaml`.",
            "- Do not pivot without explicit human approval.",
            "- Do not claim plagiarism clearance, AI-detection clearance, "
            "or formal proof verification in v1.",
            "",
            "## Language policy",
            "",
            f"- Process documents: `{state['language_policy']['process_docs']}`",
            f"- Paper-facing documents: `{state['language_policy']['paper_docs']}`",
            "",
        ]
    )


def load_project_config(project_root: Path) -> dict[str, Any]:
    """Load project configuration with defaults.

    Args:
        project_root: Project root directory.

    Returns:
        Merged configuration dictionary.
    """
    path = project_root / DEFAULT_DELIVERABLES["project_config"]
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    config = read_yaml(path)
    merged = json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    for key, value in config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged
