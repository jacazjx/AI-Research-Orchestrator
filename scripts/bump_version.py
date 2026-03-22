#!/usr/bin/env python3
"""
Bump version across all version-related files.

This script ensures all four version files are updated together:
1. scripts/constants/version.py (SYSTEM_VERSION + VERSION_HISTORY)
2. pyproject.toml
3. .claude-plugin/plugin.json
4. .claude-plugin/marketplace.json

Usage:
    python scripts/bump_version.py --minor --message "Add new feature"
    python scripts/bump_version.py --patch --message "Fix bug"
    python scripts/bump_version.py --major --message "Breaking changes"
    python scripts/bump_version.py --set 2.0.0 --message "Major release"

By default, bumps PATCH version. Use --minor or --major for larger bumps.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

VERSION_PY = PROJECT_ROOT / "scripts" / "constants" / "version.py"
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"
PLUGIN_JSON = PROJECT_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = PROJECT_ROOT / ".claude-plugin" / "marketplace.json"

BumpType = Literal["major", "minor", "patch"]


def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse semver string into tuple."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple as string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, bump_type: BumpType) -> str:
    """Bump version according to type."""
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    else:  # patch
        return format_version(major, minor, patch + 1)


def get_current_version() -> str:
    """Read current version from version.py."""
    content = VERSION_PY.read_text(encoding="utf-8")
    match = re.search(r'SYSTEM_VERSION\s*=\s*"([^"]+)"', content)
    if not match:
        raise RuntimeError("Could not find SYSTEM_VERSION in version.py")
    return match.group(1)


def update_version_py(new_version: str, message: str) -> None:
    """Update version.py with new version and history entry."""
    content = VERSION_PY.read_text(encoding="utf-8")

    # Update SYSTEM_VERSION
    content = re.sub(
        r'SYSTEM_VERSION\s*=\s*"[^"]+"',
        f'SYSTEM_VERSION = "{new_version}"',
        content,
    )

    # Add new history entry
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = (
        f'    (\n        "{new_version}",\n        "{today}",\n        "{message}",\n    ),\n'
    )

    # Find the last entry in VERSION_HISTORY and add after it
    # Look for the closing bracket of VERSION_HISTORY
    history_pattern = r"(VERSION_HISTORY\s*=\s*\[.*?\n)(\])"
    match = re.search(history_pattern, content, re.DOTALL)
    if match:
        # Insert new entry before the closing bracket
        insert_pos = match.end() - 1  # Before the ]
        content = content[:insert_pos] + new_entry + content[insert_pos:]

    VERSION_PY.write_text(content, encoding="utf-8")
    print(f"Updated {VERSION_PY.relative_to(PROJECT_ROOT)}")


def update_pyproject_toml(new_version: str) -> None:
    """Update pyproject.toml with new version."""
    content = PYPROJECT_TOML.read_text(encoding="utf-8")

    # Update version in [project] section
    content = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content,
        flags=re.MULTILINE,
    )

    PYPROJECT_TOML.write_text(content, encoding="utf-8")
    print(f"Updated {PYPROJECT_TOML.relative_to(PROJECT_ROOT)}")


def update_plugin_json(new_version: str) -> None:
    """Update plugin.json with new version."""
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    data["version"] = new_version
    PLUGIN_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {PLUGIN_JSON.relative_to(PROJECT_ROOT)}")


def update_marketplace_json(new_version: str) -> None:
    """Update marketplace.json with new version."""
    data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    for plugin in data.get("plugins", []):
        plugin["version"] = new_version
    MARKETPLACE_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {MARKETPLACE_JSON.relative_to(PROJECT_ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump version across all version files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --patch --message "Fix bug in init wizard"
    %(prog)s --minor --message "Add new skill"
    %(prog)s --major --message "Breaking API changes"
    %(prog)s --set 2.0.0 --message "Major release"

Files updated:
    - scripts/constants/version.py (SYSTEM_VERSION + VERSION_HISTORY)
    - pyproject.toml (version field)
    - .claude-plugin/plugin.json (version field)
    - .claude-plugin/marketplace.json (version field)
        """,
    )

    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument(
        "--major",
        action="store_true",
        help="Bump major version (X.0.0)",
    )
    version_group.add_argument(
        "--minor",
        action="store_true",
        help="Bump minor version (x.Y.0)",
    )
    version_group.add_argument(
        "--patch",
        action="store_true",
        default=True,
        help="Bump patch version (x.y.Z) [default]",
    )
    version_group.add_argument(
        "--set",
        metavar="VERSION",
        help="Set specific version (e.g., 2.0.0)",
    )

    parser.add_argument(
        "--message",
        "-m",
        required=True,
        help="Changelog message for this version",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )

    args = parser.parse_args()

    # Determine bump type
    if args.set:
        new_version = args.set
        try:
            parse_version(new_version)
        except ValueError:
            print(f"Error: Invalid version format: {new_version}", file=sys.stderr)
            return 1
    else:
        if args.major:
            bump_type: BumpType = "major"
        elif args.minor:
            bump_type = "minor"
        else:
            bump_type = "patch"

        current = get_current_version()
        new_version = bump_version(current, bump_type)

    print(f"Current version: {get_current_version()}")
    print(f"New version: {new_version}")
    print(f"Message: {args.message}")
    print()

    if args.dry_run:
        print("DRY RUN - would update:")
        print(f"  - {VERSION_PY.relative_to(PROJECT_ROOT)}")
        print(f"  - {PYPROJECT_TOML.relative_to(PROJECT_ROOT)}")
        print(f"  - {PLUGIN_JSON.relative_to(PROJECT_ROOT)}")
        print(f"  - {MARKETPLACE_JSON.relative_to(PROJECT_ROOT)}")
        return 0

    try:
        update_version_py(new_version, args.message)
        update_pyproject_toml(new_version)
        update_plugin_json(new_version)
        update_marketplace_json(new_version)
        print()
        print(f"Version bumped to {new_version}")
        print("Remember to commit and push these changes.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
