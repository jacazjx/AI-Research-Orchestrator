#!/usr/bin/env python3
"""Display system version information.

This script shows:
- Current system version
- Version name
- Version history with release dates and descriptions
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import SYSTEM_VERSION, SYSTEM_VERSION_NAME, VERSION_HISTORY


def get_version_info() -> dict:
    """Get version information as a dictionary."""
    return {
        "version": SYSTEM_VERSION,
        "name": SYSTEM_VERSION_NAME,
        "history": [
            {
                "version": v,
                "date": d,
                "description": desc,
            }
            for v, d, desc in VERSION_HISTORY
        ],
    }


def format_version_report(use_color: bool = True) -> str:
    """Format version information as human-readable text."""
    # ANSI color codes
    if use_color:
        cyan = "\033[36m"
        green = "\033[32m"
        yellow = "\033[33m"
        bold = "\033[1m"
        reset = "\033[0m"
        dim = "\033[2m"
    else:
        cyan = green = yellow = bold = reset = dim = ""

    lines = [
        "",
        f"{cyan}{'═' * 60}{reset}",
        "",
        f"  {bold}{SYSTEM_VERSION_NAME}{reset}",
        f"  Version {green}{SYSTEM_VERSION}{reset}",
        "",
        f"{cyan}{'═' * 60}{reset}",
        "",
        f"  {bold}Version History:{reset}",
        "",
    ]

    for version, date, description in VERSION_HISTORY:
        # Highlight current version
        if version == SYSTEM_VERSION:
            lines.append(f"    {green}●{reset} {bold}{version}{reset} ({date}) - {description}")
        else:
            lines.append(f"    {dim}○{reset} {version} ({date}) - {description}")

    lines.extend([
        "",
        f"{cyan}{'═' * 60}{reset}",
        "",
    ])

    return "\n".join(lines)


def check_for_updates() -> dict:
    """Check if there are newer versions available (placeholder for future)."""
    # This is a placeholder for future update checking functionality
    return {
        "current_version": SYSTEM_VERSION,
        "latest_version": SYSTEM_VERSION,
        "update_available": False,
        "message": "You are running the latest version.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Display AI Research Orchestrator version information"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output version information as JSON",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--check-updates",
        action="store_true",
        help="Check for available updates (placeholder)",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help="Output only the version number",
    )
    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    if args.short:
        print(SYSTEM_VERSION)
    elif args.json:
        info = get_version_info()
        if args.check_updates:
            info["update_check"] = check_for_updates()
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print(format_version_report(use_color=use_color))
        if args.check_updates:
            update_info = check_for_updates()
            if update_info["update_available"]:
                print(f"\n  ⚠️  Update available: {update_info['latest_version']}")
            else:
                print(f"\n  ✓ {update_info['message']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())