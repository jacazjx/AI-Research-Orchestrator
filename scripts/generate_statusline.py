#!/usr/bin/env python3
"""Generate statusline showing current phase and agent status.

This script generates a statusline display showing:
- Current phase with progress bar
- Agent list for each phase
- Color-coded active agent indicator
- Current task summary
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import (  # noqa: E402
    PHASE_AGENT_PAIRS,
    PHASE_LOOP_KEY,
    PHASE_SEQUENCE,
    SYSTEM_VERSION,
    SYSTEM_VERSION_NAME,
    ensure_project_structure,
    get_phase_agents,
    load_state,
    normalize_phase_name,
)

# ANSI color codes
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
}

# Phase display names (support both new and legacy names)
PHASE_NAMES = {
    "survey": "Survey",
    "pilot": "Pilot",
    "experiments": "Experiments",
    "paper": "Paper",
    "reflection": "Reflection",
    # Legacy names for backward compatibility
    "01-survey": "Survey",
    "02-pilot-analysis": "Pilot",
    "03-full-experiments": "Experiments",
    "04-paper": "Paper",
    "05-reflection-evolution": "Reflection",
}


def _get_phase_loop_key(phase: str) -> str:
    """Get loop key for a phase, supporting both semantic and legacy names."""
    normalized = normalize_phase_name(phase)
    return PHASE_LOOP_KEY.get(normalized, "")


def _agent_display_name(agent_role: str) -> str:
    """Convert agent role to display name."""
    # Map internal agent names to display names
    name_map = {
        "survey": "Survey",
        "critic": "Critic",
        "code": "Code",
        "adviser": "Adviser",
        "paper-writer": "Writer",
        "reviewer-editor": "Reviewer",
        "reflector": "Reflector",
        "curator": "Curator",
    }
    return name_map.get(agent_role, agent_role.title())


# Phase descriptions for display
_PHASE_DESCRIPTIONS = {
    "survey": "Literature survey and research readiness",
    "pilot": "Pilot experiments and validation",
    "experiments": "Full experiment execution",
    "paper": "Paper development and review",
    "reflection": "Lessons learned and improvements",
}


def _build_phase_agents() -> dict[str, dict[str, str]]:
    """Build PHASE_AGENTS from centralized PHASE_AGENT_PAIRS."""
    result = {}
    for phase, (primary, secondary) in PHASE_AGENT_PAIRS.items():
        result[phase] = {
            "primary": _agent_display_name(primary),
            "secondary": _agent_display_name(secondary),
            "loop_key": PHASE_LOOP_KEY.get(phase, ""),
            "description": _PHASE_DESCRIPTIONS.get(phase, ""),
        }
    return result


# Agent definitions for each phase (built from centralized PHASE_AGENT_PAIRS)
PHASE_AGENTS = _build_phase_agents()

# Agent role descriptions
AGENT_DESCRIPTIONS = {
    "orchestrator": "Coordinating research workflow",
    "Survey": "Analyzing literature and building research foundation",
    "Critic": "Reviewing survey quality and identifying gaps",
    "Code": "Implementing experiments and analysis",
    "Adviser": "Providing technical guidance and review",
    "Writer": "Drafting paper manuscript",
    "Reviewer": "Reviewing paper quality and completeness",
    "Reflector": "Documenting lessons learned",
    "Curator": "Organizing and archiving project artifacts",
}


def colorize(text: str, color: str, use_color: bool = True) -> str:
    """Apply ANSI color to text."""
    if not use_color or color not in COLORS:
        return text
    return f"{COLORS[color]}{text}{COLORS['reset']}"


def get_agent_status(
    state: dict[str, Any],
    phase: str,
    agent_type: str,
) -> str:
    """Determine agent status: active, pending, completed."""
    current_phase = state.get("current_phase", "01-survey")
    current_agent = state.get("progress", {}).get("current_agent", "orchestrator")

    # Check if this phase is completed
    phase_index = PHASE_SEQUENCE.index(phase) if phase in PHASE_SEQUENCE else -1
    current_index = PHASE_SEQUENCE.index(current_phase) if current_phase in PHASE_SEQUENCE else 0

    if phase_index < current_index:
        return "completed"
    elif phase_index > current_index:
        return "pending"
    else:
        # Current phase - check if this specific agent is active
        agent_name = PHASE_AGENTS[phase][agent_type].lower()
        if current_agent == agent_name:
            return "active"
        # Check inner loop to see which agent is working
        loop_key = _get_phase_loop_key(phase)
        inner_loops = state.get("inner_loops", {})
        loop_count = inner_loops.get(loop_key, 0)

        # Odd loop count = primary agent, even = secondary agent
        if agent_type == "primary":
            return "active" if loop_count % 2 == 0 else "reviewing"
        else:
            return "active" if loop_count % 2 == 1 else "reviewing"


def get_status_icon(status: str, use_color: bool = True) -> str:
    """Get icon and color for agent status."""
    if status == "active":
        return colorize("●", "green", use_color)
    elif status == "reviewing":
        return colorize("●", "yellow", use_color)
    elif status == "completed":
        return colorize("✓", "cyan", use_color)
    else:
        return colorize("○", "dim", use_color)


def generate_progress_bar(
    current_phase: str,
    completion_percent: int,
    width: int = 20,
    use_color: bool = True,
) -> str:
    """Generate a progress bar."""
    filled = int(width * completion_percent / 100)
    empty = width - filled

    bar = "█" * filled + "░" * empty
    if use_color:
        if completion_percent < 25:
            bar = colorize(bar, "red", True)
        elif completion_percent < 50:
            bar = colorize(bar, "yellow", True)
        elif completion_percent < 75:
            bar = colorize(bar, "blue", True)
        else:
            bar = colorize(bar, "green", True)

    return bar


def generate_statusline(
    project_root: Path,
    use_color: bool = True,
    compact: bool = False,
) -> str:
    """Generate the statusline display."""
    state = load_state(project_root)

    current_phase = state.get("current_phase", "01-survey")
    current_gate = state.get("current_gate", "gate_1")
    current_agent = state.get("progress", {}).get("current_agent", "orchestrator")
    completion_percent = state.get("progress", {}).get("completion_percent", 0)
    next_action = state.get("progress", {}).get("next_action", "")
    active_blocker = state.get("progress", {}).get("active_blocker", "none")

    lines = []

    # Header with project info
    if compact:
        # Compact single-line format
        phase_name = PHASE_NAMES.get(current_phase, current_phase)
        progress_bar = generate_progress_bar(
            current_phase, completion_percent, width=10, use_color=use_color
        )
        agent_display = (
            colorize(current_agent.upper(), "cyan", use_color)
            if use_color
            else current_agent.upper()
        )

        lines.append(f"[{progress_bar}] {phase_name} | {current_gate} | {agent_display}")
    else:
        # Full format
        lines.append("")
        lines.append(colorize("═" * 60, "cyan", use_color))
        lines.append("")

        # Project header
        project_id = state.get("project_id", "unknown")
        topic = state.get("topic", "No topic")
        if len(topic) > 50:
            topic = topic[:47] + "..."

        lines.append(f"  Project: {colorize(project_id, 'bold', use_color)}")
        lines.append(f"  Topic:   {topic}")
        lines.append("")

        # Progress section
        progress_bar = generate_progress_bar(
            current_phase, completion_percent, width=20, use_color=use_color
        )
        phase_name = PHASE_NAMES.get(current_phase, current_phase)

        lines.append(f"  Progress: [{progress_bar}] {completion_percent}%")
        lines.append(f"  Phase:    {colorize(phase_name, 'bold', use_color)} ({current_phase})")
        lines.append(f"  Gate:     {colorize(current_gate, 'yellow', use_color)}")
        lines.append("")

        # Agent list section
        lines.append(colorize("  Agents:", "bold", use_color))
        lines.append("")

        for phase in PHASE_SEQUENCE:
            agents = PHASE_AGENTS[phase]
            primary_status = get_agent_status(state, phase, "primary")
            secondary_status = get_agent_status(state, phase, "secondary")

            primary_icon = get_status_icon(primary_status, use_color)
            secondary_icon = get_status_icon(secondary_status, use_color)

            phase_label = PHASE_NAMES.get(phase, phase)

            # Highlight current phase
            if phase == current_phase:
                phase_label = colorize(phase_label, "bold", use_color)

            # Build agent line
            agent_line = (
                f"    {primary_icon} {agents['primary']:10} ↔ "
                f"{agents['secondary']:10} {secondary_icon}  {phase_label}"
            )

            # Add active task description
            if phase == current_phase and primary_status == "active":
                task_desc = AGENT_DESCRIPTIONS.get(agents["primary"], "")
                agent_line += f"  {colorize(task_desc, 'dim', use_color)}"
            elif phase == current_phase and secondary_status == "active":
                task_desc = AGENT_DESCRIPTIONS.get(agents["secondary"], "")
                agent_line += f"  {colorize(task_desc, 'dim', use_color)}"

            lines.append(agent_line)

        lines.append("")

        # Current activity section
        lines.append(colorize("  Current Activity:", "bold", use_color))
        lines.append("")

        # Current agent with description
        agent_display = (
            colorize(current_agent.upper(), "green", use_color)
            if use_color
            else current_agent.upper()
        )
        agent_desc = AGENT_DESCRIPTIONS.get(current_agent, "Working")
        lines.append(f"    Active Agent: {agent_display}")
        lines.append(f"    Task: {agent_desc}")
        lines.append(f"    Next Action: {colorize(next_action, 'cyan', use_color)}")

        # Blocker warning if any
        if active_blocker and active_blocker != "none":
            lines.append(f"    Blocker: {colorize(active_blocker, 'red', use_color)}")

        lines.append("")
        lines.append(colorize("═" * 60, "cyan", use_color))
        lines.append("")

        # Version footer
        system_version = state.get("system_version", SYSTEM_VERSION)
        lines.append(f"  {colorize(SYSTEM_VERSION_NAME, 'dim', use_color)} v{system_version}")
        lines.append("")

    return "\n".join(lines)


def generate_json_status(project_root: Path) -> dict[str, Any]:
    """Generate JSON status for programmatic use."""
    state = load_state(project_root)

    current_phase = state.get("current_phase", "01-survey")
    current_agent = state.get("progress", {}).get("current_agent", "orchestrator")

    # Build agent status list
    agents_status = []
    for phase in PHASE_SEQUENCE:
        agents = PHASE_AGENTS[phase]
        primary_status = get_agent_status(state, phase, "primary")
        secondary_status = get_agent_status(state, phase, "secondary")

        agents_status.append(
            {
                "phase": phase,
                "phase_name": PHASE_NAMES.get(phase, phase),
                "primary_agent": agents["primary"],
                "primary_status": primary_status,
                "secondary_agent": agents["secondary"],
                "secondary_status": secondary_status,
                "description": agents["description"],
            }
        )

    return {
        "project_id": state.get("project_id", "unknown"),
        "topic": state.get("topic", ""),
        "current_phase": current_phase,
        "current_phase_name": PHASE_NAMES.get(current_phase, current_phase),
        "current_gate": state.get("current_gate", "gate_1"),
        "current_agent": current_agent,
        "completion_percent": state.get("progress", {}).get("completion_percent", 0),
        "next_action": state.get("progress", {}).get("next_action", ""),
        "active_blocker": state.get("progress", {}).get("active_blocker", "none"),
        "system_version": state.get("system_version", SYSTEM_VERSION),
        "created_at": state.get("created_at", ""),
        "last_modified": state.get("last_modified", ""),
        "agents": agents_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate statusline showing current phase and agent status"
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to the project root",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON for programmatic use",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output compact single-line statusline",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    use_color = not args.no_color and sys.stdout.isatty()

    if args.json:
        import json

        status = generate_json_status(project_root)
        print(json.dumps(status, indent=2, ensure_ascii=False))
    else:
        statusline = generate_statusline(project_root, use_color=use_color, compact=args.compact)
        print(statusline)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
