#!/usr/bin/env python3
"""PreToolUse Hook: Security guard for dangerous operations.

Behavior:
- Blocks catastrophic system operations (exit code 2)
- Warns on dangerous-but-legitimate operations (exit 0 with JSON warning)
- Protects system directories from Write/Edit
- Detects path traversal in file operations
- Requires confirmation for sensitive files

This hook runs before Bash, Write, and Edit tool calls to prevent
accidental damage to the system or sensitive files.

Usage (automatic via hooks.json):
    Triggered by PreToolUse event with matcher "Bash|Write|Edit"

Manual test:
    echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' \
    | python3 scripts/hooks/security_guard.py

Input (from Claude Code via stdin):
    JSON with tool_name, tool_input

Output:
    Exit 0 with no output for safe operations
    Exit 0 with JSON warning for flagged operations
    Exit 2 with error message on stderr for blocked operations
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Setup path for imports - scripts directory is parent of hooks
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from hooks import read_hook_input  # noqa: E402

# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

# Catastrophic commands that must always be blocked
CATASTROPHIC_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|(-[a-zA-Z]*f[a-zA-Z]*r))\s+/\s*$"),
        "Blocked: 'rm -rf /' would destroy the entire filesystem",
    ),
    (
        re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|(-[a-zA-Z]*f[a-zA-Z]*r))\s+/\*"),
        "Blocked: 'rm -rf /*' would destroy the entire filesystem",
    ),
    (
        re.compile(r"\bmkfs\b"),
        "Blocked: 'mkfs' would format a filesystem",
    ),
    (
        re.compile(r"\bdd\s+.*\bif=.*\b(of=/dev/[a-z]|of=\s*/dev/[a-z])"),
        "Blocked: 'dd' targeting a device could destroy data",
    ),
    (
        re.compile(r"\bdd\s+.*\bof=/dev/[a-z]"),
        "Blocked: 'dd' writing to a device could destroy data",
    ),
    (
        re.compile(r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*\s+)?777\s+/\s*$"),
        "Blocked: 'chmod -R 777 /' would make the entire filesystem world-writable",
    ),
    (
        re.compile(r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*\s+)?777\s+/(etc|usr|bin|sbin|boot)\b"),
        "Blocked: 'chmod 777' on system directory is catastrophic",
    ),
    (
        re.compile(
            r"\bchown\s+(-[a-zA-Z]*R[a-zA-Z]*\s+)\S+\s+/(etc|usr|bin|sbin|boot|sys|proc)\b"
        ),
        "Blocked: recursive chown on system directory is catastrophic",
    ),
    (
        re.compile(r">\s*/dev/sd[a-z]"),
        "Blocked: writing to raw block device would destroy data",
    ),
    (
        re.compile(r"\bshutdown\b"),
        "Blocked: 'shutdown' would halt the system",
    ),
    (
        re.compile(r"\breboot\b"),
        "Blocked: 'reboot' would restart the system",
    ),
    (
        re.compile(r"\binit\s+0\b"),
        "Blocked: 'init 0' would halt the system",
    ),
]

# Dangerous-but-legitimate commands that deserve a warning
WARNING_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bgit\s+push\s+.*--force\b.*\b(main|master)\b"),
        "Force-pushing to main/master can destroy shared history",
    ),
    (
        re.compile(r"\bgit\s+push\s+.*\b(main|master)\b.*--force\b"),
        "Force-pushing to main/master can destroy shared history",
    ),
    (
        re.compile(r"\bgit\s+reset\s+--hard\b"),
        "git reset --hard discards all uncommitted changes",
    ),
    (
        re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|(-[a-zA-Z]*f[a-zA-Z]*r))\s+\S"),
        "Recursive deletion - verify the target path is correct",
    ),
    (
        re.compile(r"\bpip\s+install\b"),
        "pip install outside a virtualenv modifies the system Python environment",
    ),
]

# System directories that should not be written to
PROTECTED_SYSTEM_DIRS: list[str] = [
    "/etc/",
    "/usr/",
    "/bin/",
    "/sbin/",
    "/boot/",
    "/sys/",
    "/proc/",
]

# Home directory sensitive locations
HOME_SENSITIVE_DIRS: list[str] = [
    ".ssh/",
    ".gnupg/",
    ".aws/",
]

# Sensitive file patterns that require confirmation
SENSITIVE_FILE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(^|/)\.env$"), "Environment file may contain secrets"),
    (re.compile(r"(^|/)\.env\."), "Environment file may contain secrets"),
    (re.compile(r"(^|/)credentials\.json$"), "Credentials file contains secrets"),
    (re.compile(r"\.pem$"), "PEM file may contain private keys"),
    (re.compile(r"\.key$"), "Key file may contain private keys"),
    (re.compile(r"(^|/)id_rsa"), "SSH private key file"),
]


def _is_inside_venv(command: str) -> bool:
    """Check if pip install is likely running inside a virtualenv.

    Heuristics:
    - VIRTUAL_ENV environment variable is set
    - Command explicitly uses a venv python/pip path
    - Command activates a venv before pip install
    """
    if os.environ.get("VIRTUAL_ENV"):
        return True
    # Check if command activates a venv or uses a venv-relative pip
    venv_indicators = [
        r"source\s+\S*\.venv\S*/bin/activate",
        r"source\s+\S*venv\S*/bin/activate",
        r"\.\s+\S*\.venv\S*/bin/activate",
        r"\.\s+\S*venv\S*/bin/activate",
        r"\.venv/bin/pip",
        r"venv/bin/pip",
    ]
    for pattern in venv_indicators:
        if re.search(pattern, command):
            return True
    return False


def check_bash_command(command: str) -> tuple[str, str]:
    """Check a bash command for dangerous patterns.

    Args:
        command: The bash command string to check.

    Returns:
        Tuple of (level, message) where level is 'block', 'warn', or 'safe'.
    """
    # Strip leading/trailing whitespace for cleaner matching
    cmd = command.strip()

    if not cmd:
        return ("safe", "")

    # Check catastrophic patterns first
    for pattern, message in CATASTROPHIC_PATTERNS:
        if pattern.search(cmd):
            return ("block", message)

    # Check warning patterns
    for pattern, message in WARNING_PATTERNS:
        if pattern.search(cmd):
            # Special case: pip install inside a venv is fine
            if "pip install" in cmd and _is_inside_venv(cmd):
                continue
            return ("warn", message)

    return ("safe", "")


def check_file_path(file_path: str, tool_name: str) -> tuple[str, str]:
    """Check a file path for dangerous locations.

    Args:
        file_path: The file path to check.
        tool_name: The tool being used (Write or Edit).

    Returns:
        Tuple of (level, message) where level is 'block', 'warn', or 'safe'.
    """
    if not file_path:
        return ("safe", "")

    # Resolve the path to handle relative references.
    # Use both filesystem-aware resolve() and pure lexical normpath() so that
    # traversal attacks are caught even when intermediate directories don't exist.
    try:
        resolved = str(Path(file_path).resolve())
    except (OSError, ValueError):
        resolved = file_path
    normalized = os.path.normpath(file_path)

    # Check system directories first (block) - checks both resolved and
    # normalized paths so traversal attempts are caught regardless of
    # whether the intermediate directories exist on disk.
    for sys_dir in PROTECTED_SYSTEM_DIRS:
        for candidate in (resolved, normalized):
            if candidate.startswith(sys_dir) or candidate == sys_dir.rstrip("/"):
                return (
                    "block",
                    f"Blocked: {tool_name} to system directory '{sys_dir}' is not allowed",
                )

    # Check home directory sensitive locations (block)
    home_dir = os.path.expanduser("~")
    for sensitive_dir in HOME_SENSITIVE_DIRS:
        full_sensitive = os.path.join(home_dir, sensitive_dir)
        for candidate in (resolved, normalized):
            if candidate.startswith(full_sensitive):
                return (
                    "block",
                    f"Blocked: {tool_name} to sensitive directory '~/{sensitive_dir}' is not allowed",
                )

    # Check path traversal: raw path contains /../ segments
    # Runs after block checks so that traversal into protected dirs is blocked,
    # not merely warned about.
    if "/../" in file_path or file_path.endswith("/.."):
        return (
            "warn",
            f"Path traversal detected in '{file_path}' - verify this resolves safely",
        )

    # Check sensitive file patterns (warn)
    for pattern, message in SENSITIVE_FILE_PATTERNS:
        if pattern.search(resolved):
            return ("warn", f"{message}: '{file_path}'")

    return ("safe", "")


def main() -> int:
    """Main entry point for PreToolUse security guard hook.

    Returns:
        0 for safe or warned operations, 2 for blocked operations.
    """
    try:
        hook_input = read_hook_input()

        tool_name = hook_input.get("tool_name", "")
        tool_input = hook_input.get("tool_input", {})

        if not tool_name:
            return 0

        level = "safe"
        message = ""

        if tool_name == "Bash":
            command = tool_input.get("command", "")
            level, message = check_bash_command(command)

        elif tool_name in ("Write", "Edit"):
            file_path = tool_input.get("file_path", "")
            level, message = check_file_path(file_path, tool_name)

        # Handle results
        if level == "block":
            # Exit code 2: blocking error, stderr fed back as error
            print(message, file=sys.stderr)
            return 2

        if level == "warn":
            # Exit code 0 with JSON warning on stdout
            warning = {
                "hook": "security-guard",
                "level": "warn",
                "tool": tool_name,
                "message": message,
            }
            print(json.dumps(warning, ensure_ascii=False))
            return 0

        # Safe - no output needed
        return 0

    except Exception:
        # Security hook should never block on its own errors.
        # A failing guard is worse than no guard, but crashing the entire
        # tool pipeline is even worse - log nothing and let the tool proceed.
        return 0


if __name__ == "__main__":
    sys.exit(main())
