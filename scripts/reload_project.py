#!/usr/bin/env python3
"""Reload project state and configuration for AI Research Orchestrator.

This script reloads all project state, configuration, and user preferences
to restore context when a new session starts.

Usage:
    python3 scripts/reload_project.py --project-root /path/to/project
    python3 scripts/reload_project.py --project-root /path/to/project --verbose
    python3 scripts/reload_project.py --project-root /path/to/project --json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
from constants import (  # noqa: E402
    DEFAULT_DELIVERABLES,
    PHASE_COMPLETION,
    PHASE_SEQUENCE,
    PHASE_TO_GATE,
)
from state_migrator import CURRENT_STATE_VERSION, migrate_state, needs_migration  # noqa: E402

from orchestrator_common import (  # noqa: E402
    DEFAULT_LANGUAGE_POLICY,
    load_json,
    read_yaml,
)

# Configure module logger
logger = logging.getLogger(__name__)


def detect_project_root(start_path: Path) -> Path | None:
    """Detect project root by searching for .autoresearch/ directory.

    Searches upward from the given path until .autoresearch/ is found
    or the filesystem root is reached.

    Args:
        start_path: Path to start searching from.

    Returns:
        Project root path if found, None otherwise.
    """
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".autoresearch").exists():
            return current
        current = current.parent
    return None


def load_project_state(project_root: Path) -> dict[str, Any]:
    """Load project state from research-state.yaml.

    Automatically migrates state if needed.

    Args:
        project_root: Project root directory.

    Returns:
        Project state dictionary.
    """
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]

    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")

    state = read_yaml(state_path)

    if state is None:
        raise ValueError(f"Failed to parse state file: {state_path}")

    # Check and perform migration if needed
    if needs_migration(state):
        logger.info("State migration required from version %s", state.get("state_version", "1.0.0"))
        state, migration_log = migrate_state(state)
        logger.info("Migration complete: %s", migration_log)
        # Note: We don't save the migrated state here to avoid side effects
        # The caller can save it if desired

    return state


def load_project_config(project_root: Path) -> dict[str, Any]:
    """Load project configuration from orchestrator-config.yaml.

    Args:
        project_root: Project root directory.

    Returns:
        Project configuration dictionary, or empty dict if not found.
    """
    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]

    if not config_path.exists():
        logger.debug("Project config not found: %s", config_path)
        return {}

    config = read_yaml(config_path)
    return config if config else {}


def load_dashboard_status(project_root: Path) -> dict[str, Any]:
    """Load dashboard status from status.json.

    Args:
        project_root: Project root directory.

    Returns:
        Dashboard status dictionary, or empty dict if not found.
    """
    status_path = project_root / DEFAULT_DELIVERABLES["dashboard_status"]
    return load_json(status_path, {})


def load_user_config() -> dict[str, Any]:
    """Load user-level configuration from ~/.autoresearch/.

    Returns:
        User configuration dictionary, or empty dict if not found.
    """
    try:
        from user_config import load_user_config as _load

        return _load()
    except Exception:
        logger.debug("Could not load user config, returning empty dict")
        return {}


def load_gpu_registry() -> dict[str, Any]:
    """Load GPU registry from ~/.autoresearch/gpu-registry.yaml.

    Returns:
        GPU registry dictionary, or empty dict if not found.
    """
    gpu_registry_path = Path.home() / ".autoresearch" / "gpu-registry.yaml"

    if not gpu_registry_path.exists():
        logger.debug("GPU registry not found: %s", gpu_registry_path)
        return {}

    registry = read_yaml(gpu_registry_path)
    return registry if registry else {}


def get_phase_progress(state: dict[str, Any]) -> dict[str, Any]:
    """Calculate progress information for each phase.

    Args:
        state: Project state dictionary.

    Returns:
        Dictionary with progress information per phase.
    """
    progress = {}
    current_phase = state.get("current_phase", "survey")

    for phase in PHASE_SEQUENCE:
        gate = PHASE_TO_GATE.get(phase, "gate_1")
        gate_score = state.get("gate_scores", {}).get(gate, 0)
        approval = state.get("approval_status", {}).get(gate, "pending")

        # Determine phase status
        if phase == current_phase:
            status = "in_progress"
        elif PHASE_SEQUENCE.index(phase) < PHASE_SEQUENCE.index(current_phase):
            status = "completed" if approval == "approved" else "in_progress"
        else:
            status = "pending"

        progress[phase] = {
            "status": status,
            "gate": gate,
            "gate_score": gate_score,
            "approval_status": approval,
            "completion_percent": PHASE_COMPLETION.get(phase, 0),
        }

    return progress


def get_completed_work(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Get list of completed work items.

    Args:
        state: Project state dictionary.

    Returns:
        List of completed work items.
    """
    completed = []
    phase_reviews = state.get("phase_reviews", {})
    gate_scores = state.get("gate_scores", {})
    approval_status = state.get("approval_status", {})

    phase_labels = {
        "survey": "Survey",
        "pilot": "Pilot",
        "experiments": "Experiments",
        "paper": "Paper",
        "reflection": "Reflection",
    }

    for phase in PHASE_SEQUENCE:
        gate = PHASE_TO_GATE.get(phase, "gate_1")
        review_key = {
            "survey": "survey_critic",
            "pilot": "pilot_adviser",
            "experiments": "experiment_adviser",
            "paper": "paper_reviewer",
            "reflection": "reflection_curator",
        }.get(phase, "")

        gate_score = gate_scores.get(gate, 0)
        approval = approval_status.get(gate, "pending")
        review = phase_reviews.get(review_key, "pending")

        if approval == "approved" or gate_score > 0:
            completed.append(
                {
                    "phase": phase,
                    "label": phase_labels.get(phase, phase),
                    "score": gate_score,
                    "approval": approval,
                    "review": review,
                }
            )

    return completed


def get_next_actions(state: dict[str, Any]) -> list[str]:
    """Get list of suggested next actions.

    Args:
        state: Project state dictionary.

    Returns:
        List of next action suggestions.
    """
    actions = []
    current_phase = state.get("current_phase", "survey")
    current_substep = state.get("current_substep")
    approval_status = state.get("approval_status", {})

    # Check if waiting for gate approval
    gate = PHASE_TO_GATE.get(current_phase, "gate_1")
    if approval_status.get(gate) == "pending" and state.get("gate_scores", {}).get(gate, 0) > 0:
        actions.append(f"等待 {gate} 评审结果")
        return actions

    # Phase-specific suggestions
    if current_phase == "survey":
        if current_substep:
            actions.extend(
                [
                    "完成文献调研报告",
                    "生成研究准备报告",
                    "运行 Gate 1 质量检查",
                ]
            )
        else:
            actions.append("开始 Survey 阶段")

    elif current_phase == "pilot":
        actions.extend(
            [
                "完成 Pilot 实验设计",
                "运行 Pilot 验证",
                "等待 Gate 2 评审",
            ]
        )

    elif current_phase == "experiments":
        actions.extend(
            [
                "设计完整实验",
                "执行实验并记录结果",
                "等待 Gate 3 评审",
            ]
        )

    elif current_phase == "paper":
        actions.extend(
            [
                "撰写论文初稿",
                "整理引用文献",
                "等待 Gate 4 评审",
            ]
        )

    elif current_phase == "reflection":
        actions.extend(
            [
                "总结经验教训",
                "提出系统改进建议",
                "完成项目归档",
            ]
        )

    return actions


def generate_status_report(
    project_root: Path,
    state: dict[str, Any],
    project_config: dict[str, Any],
    dashboard_status: dict[str, Any],
    user_config: dict[str, Any],
    gpu_registry: dict[str, Any],
    verbose: bool = False,
) -> str:
    """Generate a formatted status report.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        project_config: Project configuration dictionary.
        dashboard_status: Dashboard status dictionary.
        user_config: User configuration dictionary.
        gpu_registry: GPU registry dictionary.
        verbose: Whether to include detailed information.

    Returns:
        Formatted status report string.
    """
    lines = []

    # Header
    lines.append("## 项目状态重新加载")
    lines.append("")

    # Basic info
    lines.append("### 基本信息")
    lines.append(f"- **项目ID**: {state.get('project_id', 'unknown')}")
    lines.append(f"- **主题**: {state.get('topic', 'N/A')}")
    lines.append(f"- **研究类型**: {state.get('research_type', 'ml_experiment')}")
    lines.append(f"- **创建时间**: {state.get('created_at', 'N/A')}")
    lines.append(f"- **状态版本**: {state.get('state_version', CURRENT_STATE_VERSION)}")
    lines.append("")

    # Current progress
    current_phase = state.get("current_phase", "survey")
    current_gate = state.get("current_gate", "gate_1")
    phase_index = PHASE_SEQUENCE.index(current_phase) if current_phase in PHASE_SEQUENCE else 0
    completion_percent = PHASE_COMPLETION.get(current_phase, 0)

    lines.append("### 当前进度")
    lines.append(f"- **当前阶段**: {current_phase} (阶段{phase_index + 1}/{len(PHASE_SEQUENCE)})")
    lines.append(f"- **当前Gate**: {current_gate}")
    lines.append(f"- **完成度**: {completion_percent}%")
    lines.append("")

    # Completed work
    completed_work = get_completed_work(state)
    if completed_work:
        lines.append("### 已完成工作")
        for work in completed_work:
            status_icon = "✅" if work["approval"] == "approved" else "🔄"
            lines.append(f"- {status_icon} {work['label']}阶段 (得分: {work['score']})")
        lines.append("")

    # Configuration
    lines.append("### 配置信息")
    language_policy = state.get("language_policy", DEFAULT_LANGUAGE_POLICY)
    process_lang = language_policy.get("process_docs", "zh-CN")
    paper_lang = language_policy.get("paper_docs", "en-US")
    lines.append(f"- **语言**: 过程文档({process_lang}) / 论文({paper_lang})")

    # GPU info
    active_gpu = state.get("progress", {}).get("active_gpu", "unassigned")
    if active_gpu != "unassigned" and gpu_registry:
        gpu_info = gpu_registry.get("gpus", {}).get(active_gpu, {})
        gpu_name = gpu_info.get("name", active_gpu)
        lines.append(f"- **GPU**: {gpu_name} (ID: {active_gpu})")
    else:
        lines.append(f"- **GPU**: {active_gpu}")

    # Loop limits
    loop_limits = state.get("loop_limits", {})
    if loop_limits:
        max_loop = max(loop_limits.values()) if loop_limits else 3
        lines.append(f"- **最大循环次数**: {max_loop}")

    lines.append("")

    # Next actions
    next_actions = get_next_actions(state)
    if next_actions:
        lines.append("### 下一步行动")
        for i, action in enumerate(next_actions, 1):
            lines.append(f"{i}. {action}")
        lines.append("")

    # Verbose info
    if verbose:
        lines.append("### 详细信息")
        lines.append(f"- **项目路径**: {project_root}")
        lines.append(f"- **平台**: {state.get('platform', 'unknown')}")
        lines.append(f"- **子阶段**: {state.get('subphase', 'entry')}")

        if project_config:
            lines.append("- **项目配置**:")
            for key, value in project_config.items():
                lines.append(f"  - {key}: {value}")

        if user_config:
            author = user_config.get("author", {})
            if author:
                lines.append(
                    f"- **作者**: {author.get('name', 'N/A')} ({author.get('email', 'N/A')})"
                )

        lines.append("")

    return "\n".join(lines)


def generate_json_output(
    state: dict[str, Any],
    project_config: dict[str, Any],
    dashboard_status: dict[str, Any],
    user_config: dict[str, Any],
    gpu_registry: dict[str, Any],
) -> dict[str, Any]:
    """Generate JSON output for programmatic use.

    Args:
        state: Project state dictionary.
        project_config: Project configuration dictionary.
        dashboard_status: Dashboard status dictionary.
        user_config: User configuration dictionary.
        gpu_registry: GPU registry dictionary.

    Returns:
        Dictionary with structured output.
    """
    return {
        "project_id": state.get("project_id", "unknown"),
        "topic": state.get("topic", ""),
        "research_type": state.get("research_type", "ml_experiment"),
        "current_phase": state.get("current_phase", "survey"),
        "current_gate": state.get("current_gate", "gate_1"),
        "state_version": state.get("state_version", CURRENT_STATE_VERSION),
        "created_at": state.get("created_at", ""),
        "last_modified": state.get("last_modified", ""),
        "progress": {
            "completion_percent": PHASE_COMPLETION.get(state.get("current_phase", "survey"), 0),
            "phase_progress": get_phase_progress(state),
            "completed_work": get_completed_work(state),
            "next_actions": get_next_actions(state),
        },
        "config": {
            "language_policy": state.get("language_policy", DEFAULT_LANGUAGE_POLICY),
            "loop_limits": state.get("loop_limits", {}),
            "project_config": project_config,
        },
        "user": {
            "author": user_config.get("author", {}),
            "preferences": user_config.get("preferences", {}),
        },
        "resources": {
            "active_gpu": state.get("progress", {}).get("active_gpu", "unassigned"),
            "gpu_registry": gpu_registry.get("gpus", {}),
        },
        "dashboard": dashboard_status,
    }


def reload_project(
    project_root: Path,
    verbose: bool = False,
    json_output: bool = False,
) -> dict[str, Any]:
    """Reload project state and generate report.

    Args:
        project_root: Project root directory.
        verbose: Whether to include detailed information.
        json_output: Whether to output as JSON.

    Returns:
        Dictionary with reload results.
    """
    # Verify project exists
    autoresearch_dir = project_root / ".autoresearch"
    if not autoresearch_dir.exists():
        raise FileNotFoundError(
            f"Not a valid AI Research project: {project_root}\n"
            f"Missing .autoresearch/ directory. "
            f"Run /init-research to create a new project."
        )

    # Load all state and configuration
    state = load_project_state(project_root)
    project_config = load_project_config(project_root)
    dashboard_status = load_dashboard_status(project_root)
    user_config = load_user_config()
    gpu_registry = load_gpu_registry()

    # Generate output
    if json_output:
        output = generate_json_output(
            state, project_config, dashboard_status, user_config, gpu_registry
        )
        output["project_root"] = str(project_root)
        return output
    else:
        report = generate_status_report(
            project_root,
            state,
            project_config,
            dashboard_status,
            user_config,
            gpu_registry,
            verbose,
        )
        return {
            "project_root": str(project_root),
            "report": report,
            "state": state,
        }


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Reload project state and configuration for AI Research Orchestrator."
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Path to the project root. Defaults to the nearest parent containing .autoresearch/.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format.",
    )
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.project_root is not None:
        project_root = Path(args.project_root).resolve()
    else:
        project_root = Path.cwd()

    # Try to auto-detect project root if not found
    if not (project_root / ".autoresearch").exists():
        detected = detect_project_root(project_root)
        if detected:
            logger.info("Auto-detected project root: %s", detected)
            project_root = detected
        else:
            print(
                f"Error: No AI Research project found at or above {project_root}", file=sys.stderr
            )
            print("Run /init-research to create a new project.", file=sys.stderr)
            return 1

    try:
        result = reload_project(
            project_root=project_root,
            verbose=args.verbose,
            json_output=args.json,
        )

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            print(result["report"])

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception("Failed to reload project")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
