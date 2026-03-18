#!/usr/bin/env python3
"""Configure project and user settings for AI Research Orchestrator.

This script allows users to view and modify configuration settings
at both project and user levels.

Usage:
    # Show current configuration
    python3 scripts/configure_project.py --project-root /path/to/project

    # Interactive configuration
    python3 scripts/configure_project.py --project-root /path/to/project --action interactive

    # Set specific configuration
    python3 scripts/configure_project.py --project-root /path/to/project --action set --key max-loops --value 5
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
from constants import DEFAULT_DELIVERABLES, PHASE_SEQUENCE
from orchestrator_common import (
    DEFAULT_LANGUAGE_POLICY,
    DEFAULT_LOOP_LIMITS,
    read_yaml,
    write_yaml,
)

# Configure module logger
logger = logging.getLogger(__name__)

# Configuration schema
PROJECT_CONFIG_KEYS = {
    "idea": {
        "type": "string",
        "description": "研究Idea",
        "state_key": "topic",
    },
    "research-type": {
        "type": "enum",
        "values": ["ml_experiment", "theory", "survey", "applied"],
        "description": "研究类型",
        "state_key": "research_type",
    },
    "max-loops": {
        "type": "int",
        "min": 1,
        "max": 10,
        "description": "阶段最大循环次数",
        "config_key": "loop_limits",
    },
    "language": {
        "type": "string",
        "pattern": r"^[a-z]{2}-[A-Z]{2},[a-z]{2}-[A-Z]{2}$",
        "description": "语言设置 (格式: process_lang,paper_lang)",
        "state_key": "language_policy",
    },
    "starting-phase": {
        "type": "enum",
        "values": list(PHASE_SEQUENCE),
        "description": "起始阶段",
        "state_key": "starting_phase",
    },
    "gpu": {
        "type": "string",
        "description": "GPU ID",
        "state_key": "progress.active_gpu",
    },
}

USER_CONFIG_KEYS = {
    "author.name": {
        "type": "string",
        "description": "作者姓名",
        "config_key": "author.name",
    },
    "author.email": {
        "type": "string",
        "description": "作者邮箱",
        "config_key": "author.email",
    },
    "author.institution": {
        "type": "string",
        "description": "所属机构",
        "config_key": "author.institution",
    },
    "preferences.venue": {
        "type": "string",
        "description": "默认投稿期刊/会议",
        "config_key": "preferences.default_venue",
    },
}


def load_project_state(project_root: Path) -> dict[str, Any]:
    """Load project state from research-state.yaml.

    Args:
        project_root: Project root directory.

    Returns:
        Project state dictionary, or empty dict if not found.
    """
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        return {}
    state = read_yaml(state_path)
    return state if state else {}


def save_project_state(project_root: Path, state: dict[str, Any]) -> None:
    """Save project state to research-state.yaml.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
    """
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(state_path, state)


def load_project_config(project_root: Path) -> dict[str, Any]:
    """Load project configuration from orchestrator-config.yaml.

    Args:
        project_root: Project root directory.

    Returns:
        Project configuration dictionary, or empty dict if not found.
    """
    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]
    if not config_path.exists():
        return {}
    config = read_yaml(config_path)
    return config if config else {}


def save_project_config(project_root: Path, config: dict[str, Any]) -> None:
    """Save project configuration to orchestrator-config.yaml.

    Args:
        project_root: Project root directory.
        config: Project configuration dictionary.
    """
    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(config_path, config)


def get_user_config_path() -> Path:
    """Get user configuration file path.

    Returns:
        Path to user configuration file.
    """
    return Path.home() / ".autoresearch" / "user-config.yaml"


def load_user_config() -> dict[str, Any]:
    """Load user-level configuration from ~/.autoresearch/.

    Returns:
        User configuration dictionary, or empty dict if not found.
    """
    config_path = get_user_config_path()
    if not config_path.exists():
        return {}
    config = read_yaml(config_path)
    return config if config else {}


def save_user_config(config: dict[str, Any]) -> None:
    """Save user-level configuration to ~/.autoresearch/.

    Args:
        config: User configuration dictionary.
    """
    config_path = get_user_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(config_path, config)


def validate_config_value(key: str, value: str, schema: dict[str, Any]) -> tuple[bool, str, Any]:
    """Validate a configuration value against its schema.

    Args:
        key: Configuration key.
        value: Configuration value as string.
        schema: Configuration schema.

    Returns:
        Tuple of (is_valid, error_message, parsed_value).
    """
    value_type = schema.get("type", "string")

    try:
        if value_type == "int":
            min_val = schema.get("min")
            max_val = schema.get("max")
            parsed = int(value)
            if min_val is not None and parsed < min_val:
                return False, f"值必须 >= {min_val}", None
            if max_val is not None and parsed > max_val:
                return False, f"值必须 <= {max_val}", None
            return True, "", parsed

        elif value_type == "enum":
            values = schema.get("values", [])
            if value not in values:
                return False, f"有效值: {', '.join(values)}", None
            return True, "", value

        elif value_type == "string":
            # Handle special language format
            if key == "language":
                parts = value.split(",")
                if len(parts) != 2:
                    return False, "格式: process_lang,paper_lang (如 zh-CN,en-US)", None
            return True, "", value

        else:
            return True, "", value

    except ValueError as e:
        return False, f"类型错误: {e}", None


def get_nested_value(data: dict[str, Any], key: str) -> Any:
    """Get a nested value from a dictionary using dot notation.

    Args:
        data: Dictionary to search.
        key: Dot-separated key path.

    Returns:
        Value at the key path, or None if not found.
    """
    keys = key.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return None
    return current


def set_nested_value(data: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    """Set a nested value in a dictionary using dot notation.

    Args:
        data: Dictionary to modify.
        key: Dot-separated key path.
        value: Value to set.

    Returns:
        Modified dictionary (new object, original not mutated).
    """
    result = dict(data)  # Shallow copy
    keys = key.split(".")

    if len(keys) == 1:
        result[keys[0]] = value
    else:
        # Need to create nested structure
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    return result


def show_current_config(
    project_root: Path,
    state: dict[str, Any],
    project_config: dict[str, Any],
    user_config: dict[str, Any],
) -> str:
    """Generate formatted display of current configuration.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        project_config: Project configuration dictionary.
        user_config: User configuration dictionary.

    Returns:
        Formatted configuration display string.
    """
    lines = []
    lines.append("⚙️  配置管理")
    lines.append("━" * 50)
    lines.append("")

    # Project configuration
    lines.append("┌─ 项目配置 ─────────────────────────────────────┐")
    lines.append(f"│ Idea: {state.get('topic', 'N/A')[:40]}")
    lines.append(f"│ 类型: {state.get('research_type', 'ml_experiment')}")
    loop_limits = state.get("loop_limits", DEFAULT_LOOP_LIMITS)
    max_loop = max(loop_limits.values()) if loop_limits else 3
    lines.append(f"│ 最大循环: {max_loop}")
    active_gpu = state.get("progress", {}).get("active_gpu", "unassigned")
    lines.append(f"│ GPU: {active_gpu}")
    lang = state.get("language_policy", DEFAULT_LANGUAGE_POLICY)
    lines.append(
        f"│ 语言: 过程/{lang.get('process_docs', 'zh-CN')}, 论文/{lang.get('paper_docs', 'en-US')}"
    )
    lines.append("└───────────────────────────────────────────────┘")
    lines.append("")

    # User configuration
    author = user_config.get("author", {})
    if author:
        lines.append("┌─ 用户配置 ─────────────────────────────────────┐")
        lines.append(f"│ 作者: {author.get('name', 'N/A')}")
        lines.append(f"│ 邮箱: {author.get('email', 'N/A')}")
        lines.append(f"│ 机构: {author.get('institution', 'N/A')}")
        lines.append("└───────────────────────────────────────────────┘")
        lines.append("")

    # Available configuration keys
    lines.append("可配置项:")
    lines.append("  项目级: idea, research-type, max-loops, language, gpu")
    lines.append("  用户级: author.name, author.email, author.institution")
    lines.append("")
    lines.append(f"项目路径: {project_root}")

    return "\n".join(lines)


def update_config(
    key: str,
    value: str,
    scope: str,
    state: dict[str, Any],
    project_config: dict[str, Any],
    user_config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    """Update a configuration value.

    Args:
        key: Configuration key to update.
        value: New value as string.
        scope: Configuration scope (project or user).
        state: Current project state.
        project_config: Current project configuration.
        user_config: Current user configuration.

    Returns:
        Tuple of (updated_state, updated_project_config, updated_user_config, message).
    """
    # Determine which schema to use
    if scope == "user" or key.startswith("author.") or key.startswith("preferences."):
        schema = USER_CONFIG_KEYS.get(key, {})
        if not schema:
            return state, project_config, user_config, f"未知的用户配置键: {key}"

        # Validate
        is_valid, error, parsed_value = validate_config_value(key, value, schema)
        if not is_valid:
            return state, project_config, user_config, f"配置值无效: {error}"

        # Update user config
        config_key = schema.get("config_key", key)
        updated_user_config = set_nested_value(user_config, config_key, parsed_value)

        return state, project_config, updated_user_config, f"已更新 {key} = {parsed_value}"

    else:
        # Project-level configuration
        schema = PROJECT_CONFIG_KEYS.get(key, {})
        if not schema:
            return state, project_config, user_config, f"未知的项目配置键: {key}"

        # Validate
        is_valid, error, parsed_value = validate_config_value(key, value, schema)
        if not is_valid:
            return state, project_config, user_config, f"配置值无效: {error}"

        # Update state
        updated_state = dict(state)
        updated_project_config = dict(project_config)

        state_key = schema.get("state_key")
        config_key = schema.get("config_key")

        if state_key:
            if "." in state_key:
                updated_state = set_nested_value(updated_state, state_key, parsed_value)
            else:
                updated_state[state_key] = parsed_value

        if config_key:
            if config_key == "loop_limits":
                # Update all loop limits
                current_limits = updated_state.get("loop_limits", dict(DEFAULT_LOOP_LIMITS))
                updated_limits = {k: parsed_value for k in current_limits}
                updated_state["loop_limits"] = updated_limits
            else:
                updated_project_config[config_key] = parsed_value

        return updated_state, updated_project_config, user_config, f"已更新 {key} = {parsed_value}"


def run_interactive_config(
    project_root: Path,
    state: dict[str, Any],
    project_config: dict[str, Any],
    user_config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], bool]:
    """Run interactive configuration wizard.

    Args:
        project_root: Project root directory.
        state: Current project state.
        project_config: Current project configuration.
        user_config: Current user configuration.

    Returns:
        Tuple of (updated_state, updated_project_config, updated_user_config, was_modified).
    """
    updated_state = dict(state)
    updated_project_config = dict(project_config)
    updated_user_config = dict(user_config)
    modified = False

    while True:
        print(
            "\n"
            + show_current_config(
                project_root, updated_state, updated_project_config, updated_user_config
            )
        )
        print("\n请选择要修改的配置:")
        print("1. 修改研究Idea")
        print("2. 修改研究类型")
        print("3. 修改最大循环次数")
        print("4. 配置GPU资源")
        print("5. 修改语言设置")
        print("6. 修改作者信息")
        print("7. 保存并退出")
        print("8. 放弃修改")

        try:
            choice = input("\n选择 [1-8]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n操作已取消")
            return state, project_config, user_config, False

        if choice == "1":
            try:
                new_idea = input(f"输入新的研究Idea [{updated_state.get('topic', '')}]: ").strip()
                if new_idea:
                    updated_state["topic"] = new_idea
                    modified = True
                    print("✓ 已更新研究Idea")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "2":
            print("研究类型: ml_experiment, theory, survey, applied")
            try:
                new_type = input(
                    f"输入研究类型 [{updated_state.get('research_type', 'ml_experiment')}]: "
                ).strip()
                if new_type in ["ml_experiment", "theory", "survey", "applied"]:
                    updated_state["research_type"] = new_type
                    modified = True
                    print("✓ 已更新研究类型")
                elif new_type:
                    print("无效的研究类型")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "3":
            try:
                current_max = max(updated_state.get("loop_limits", DEFAULT_LOOP_LIMITS).values())
                new_loops = input(f"输入最大循环次数 (1-10) [{current_max}]: ").strip()
                if new_loops:
                    try:
                        loops_int = int(new_loops)
                        if 1 <= loops_int <= 10:
                            current_limits = updated_state.get(
                                "loop_limits", dict(DEFAULT_LOOP_LIMITS)
                            )
                            updated_state["loop_limits"] = {k: loops_int for k in current_limits}
                            modified = True
                            print(f"✓ 已更新最大循环次数为 {loops_int}")
                        else:
                            print("循环次数必须在 1-10 之间")
                    except ValueError:
                        print("请输入数字")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "4":
            try:
                current_gpu = updated_state.get("progress", {}).get("active_gpu", "unassigned")
                new_gpu = input(f"输入GPU ID [{current_gpu}]: ").strip()
                if new_gpu:
                    if "progress" not in updated_state:
                        updated_state["progress"] = {}
                    updated_state["progress"]["active_gpu"] = new_gpu
                    modified = True
                    print(f"✓ 已设置GPU为 {new_gpu}")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "5":
            try:
                current_lang = updated_state.get(
                    "language_policy", DEFAULT_LANGUAGE_POLICY
                )
                current_process = current_lang.get("process_docs", "zh-CN")
                current_paper = current_lang.get("paper_docs", "en-US")
                prompt = f"输入语言设置 (process,paper) [{current_process},{current_paper}]: "
                new_lang = input(prompt).strip()
                if new_lang:
                    parts = new_lang.split(",")
                    if len(parts) == 2:
                        updated_state["language_policy"] = {
                            "process_docs": parts[0].strip(),
                            "paper_docs": parts[1].strip(),
                        }
                        modified = True
                        print("✓ 已更新语言设置")
                    else:
                        print("格式错误，应为: process_lang,paper_lang")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "6":
            author = updated_user_config.get("author", {})
            try:
                new_name = input(f"作者姓名 [{author.get('name', '')}]: ").strip()
                if new_name:
                    if "author" not in updated_user_config:
                        updated_user_config["author"] = {}
                    updated_user_config["author"]["name"] = new_name
                    modified = True

                new_email = input(f"作者邮箱 [{author.get('email', '')}]: ").strip()
                if new_email:
                    if "author" not in updated_user_config:
                        updated_user_config["author"] = {}
                    updated_user_config["author"]["email"] = new_email
                    modified = True

                new_inst = input(f"所属机构 [{author.get('institution', '')}]: ").strip()
                if new_inst:
                    if "author" not in updated_user_config:
                        updated_user_config["author"] = {}
                    updated_user_config["author"]["institution"] = new_inst
                    modified = True

                if modified:
                    print("✓ 已更新作者信息")
            except (EOFError, KeyboardInterrupt):
                print("已取消")

        elif choice == "7":
            print("\n保存配置...")
            return updated_state, updated_project_config, updated_user_config, modified

        elif choice == "8":
            print("\n已放弃修改")
            return state, project_config, user_config, False

        else:
            print("无效选择，请输入 1-8")

    return state, project_config, user_config, False


def configure_project(
    project_root: Path,
    action: str = "show",
    key: str | None = None,
    value: str | None = None,
    scope: str = "project",
) -> dict[str, Any]:
    """Configure project settings.

    Args:
        project_root: Project root directory.
        action: Configuration action (show, set, interactive).
        key: Configuration key to set.
        value: Configuration value to set.
        scope: Configuration scope (project or user).

    Returns:
        Dictionary with configuration results.
    """
    # Load current configuration
    state = load_project_state(project_root)
    project_config = load_project_config(project_root)
    user_config = load_user_config()

    if action == "show":
        return {
            "action": "show",
            "message": show_current_config(project_root, state, project_config, user_config),
            "state": state,
            "project_config": project_config,
            "user_config": user_config,
        }

    elif action == "set":
        if not key or value is None:
            raise ValueError("set 操作需要 --key 和 --value 参数")

        updated_state, updated_project_config, updated_user_config, message = update_config(
            key, value, scope, state, project_config, user_config
        )

        # Save if there was a change
        if updated_state != state:
            save_project_state(project_root, updated_state)
        if updated_project_config != project_config:
            save_project_config(project_root, updated_project_config)
        if updated_user_config != user_config:
            save_user_config(updated_user_config)

        return {
            "action": "set",
            "key": key,
            "value": value,
            "message": message,
            "state": updated_state,
            "project_config": updated_project_config,
            "user_config": updated_user_config,
        }

    elif action == "interactive":
        updated_state, updated_project_config, updated_user_config, modified = (
            run_interactive_config(project_root, state, project_config, user_config)
        )

        if modified:
            save_project_state(project_root, updated_state)
            if updated_project_config != project_config:
                save_project_config(project_root, updated_project_config)
            if updated_user_config != user_config:
                save_user_config(updated_user_config)
            return {
                "action": "interactive",
                "message": "配置已保存",
                "modified": True,
                "state": updated_state,
            }
        else:
            return {
                "action": "interactive",
                "message": "未做任何修改",
                "modified": False,
                "state": state,
            }

    else:
        raise ValueError(f"未知的操作: {action}")


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Configure project and user settings for AI Research Orchestrator."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to the AI Research project root directory.",
    )
    parser.add_argument(
        "--action",
        choices=["show", "set", "interactive"],
        default="show",
        help="Configuration action to perform.",
    )
    parser.add_argument(
        "--key",
        help="Configuration key to set (for 'set' action).",
    )
    parser.add_argument(
        "--value",
        help="Configuration value to set (for 'set' action).",
    )
    parser.add_argument(
        "--scope",
        choices=["project", "user"],
        default="project",
        help="Configuration scope.",
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

    project_root = Path(args.project_root).resolve()

    # Verify project exists
    if not (project_root / ".autoresearch").exists():
        print(f"Error: No AI Research project found at {project_root}", file=sys.stderr)
        return 1

    try:
        result = configure_project(
            project_root=project_root,
            action=args.action,
            key=args.key,
            value=args.value,
            scope=args.scope,
        )

        if args.json:
            # Remove state from output for brevity
            output = {
                k: v
                for k, v in result.items()
                if k not in ["state", "project_config", "user_config"]
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(result["message"])

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception("Failed to configure project")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
