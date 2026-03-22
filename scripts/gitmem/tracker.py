"""GitMem: Lightweight version control for agent-generated documents."""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# GitMem configuration
GITMEM_DIR = ".gitmem"
GITMEM_LOOP_THRESHOLD = 5  # Warn if file has 5+ changes without checkpoint
GITMEM_TRACKED_DIRS = ("docs/", "paper/", "code/", "agents/")


def _run_git_command(project_root: Path, args: list[str], check: bool = True) -> str:
    """Run a git command in the GitMem repository."""
    gitmem_path = project_root / GITMEM_DIR
    cmd = ["git", "-C", str(gitmem_path)] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            timeout=30,
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Git command timed out: {' '.join(args)}")
    except subprocess.CalledProcessError as e:
        if check:
            raise RuntimeError(f"Git command failed: {e.stderr}") from e
        return ""


def gitmem_is_initialized(project_root: Path) -> bool:
    """Check if GitMem is initialized for the project."""
    gitmem_path = project_root / GITMEM_DIR
    return (gitmem_path / ".git").exists()


def gitmem_init(project_root: Path) -> None:
    """Initialize GitMem for a project."""
    gitmem_path = project_root / GITMEM_DIR

    if gitmem_is_initialized(project_root):
        logger.info(f"GitMem already initialized at {gitmem_path}")
        return

    gitmem_path.mkdir(parents=True, exist_ok=True)
    _run_git_command(project_root, ["init"])
    _run_git_command(project_root, ["config", "user.name", "GitMem"])
    _run_git_command(project_root, ["config", "user.email", "gitmem@orchestrator"])

    gitignore_content = """# GitMem tracks these directories
!docs/
!paper/
!code/
!agents/
"""
    (gitmem_path / ".gitignore").write_text(gitignore_content.strip(), encoding="utf-8")

    readme_content = """# GitMem Version Tracking

This directory contains a git repository that tracks changes to files in:
- docs/
- paper/
- code/
- agents/

Files are mirrored here with the same directory structure for version tracking.
"""
    (gitmem_path / "README.md").write_text(readme_content, encoding="utf-8")

    _run_git_command(project_root, ["add", ".gitignore", "README.md"])
    _run_git_command(project_root, ["commit", "-m", "GitMem initialized"])

    main_gitignore = project_root / ".gitignore"
    if main_gitignore.exists():
        content = main_gitignore.read_text(encoding="utf-8")
        if GITMEM_DIR not in content:
            main_gitignore.write_text(
                content + f"\n# GitMem version tracking\n{GITMEM_DIR}/\n",
                encoding="utf-8",
            )
    else:
        main_gitignore.write_text(f"# GitMem version tracking\n{GITMEM_DIR}/\n", encoding="utf-8")

    logger.info(f"Initialized GitMem at {gitmem_path}")


def gitmem_commit(project_root: Path, file_path: str, message: str) -> str:
    """Commit a file change to GitMem history."""
    if not gitmem_is_initialized(project_root):
        raise ValueError("GitMem not initialized. Call gitmem_init() first.")

    file_path = Path(file_path).as_posix()
    is_tracked = any(file_path.startswith(tracked) for tracked in GITMEM_TRACKED_DIRS)
    if not is_tracked:
        logger.warning(f"File {file_path} is not in GitMem tracked directories")

    source_path = project_root / file_path
    gitmem_path = project_root / GITMEM_DIR

    if not source_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    gitmem_file_path = gitmem_path / file_path
    gitmem_file_path.parent.mkdir(parents=True, exist_ok=True)
    gitmem_file_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")

    _run_git_command(project_root, ["add", file_path])

    status = _run_git_command(project_root, ["status", "--porcelain"])
    if not status:
        logger.info(f"No changes to commit for {file_path}")
        return _run_git_command(project_root, ["rev-parse", "HEAD"])

    _run_git_command(project_root, ["commit", "-m", message])
    commit_hash = _run_git_command(project_root, ["rev-parse", "HEAD"])
    logger.info(f"GitMem commit: {commit_hash[:8]} - {message}")
    return commit_hash


def gitmem_checkpoint(project_root: Path, name: str) -> None:
    """Create a named checkpoint (annotated tag)."""
    if not gitmem_is_initialized(project_root):
        raise ValueError("GitMem not initialized. Call gitmem_init() first.")

    timestamp = datetime.now(timezone.utc).isoformat()
    _run_git_command(
        project_root,
        ["tag", "-a", name, "-m", f"Checkpoint: {name} at {timestamp}"],
    )
    logger.info(f"GitMem checkpoint created: {name}")


def gitmem_list_tags(project_root: Path) -> list[str]:
    """List all tags (checkpoints) in the GitMem repository."""
    if not gitmem_is_initialized(project_root):
        return []

    tags_output = _run_git_command(project_root, ["tag", "-l"], check=False)
    if not tags_output:
        return []
    return [tag.strip() for tag in tags_output.split("\n") if tag.strip()]


def gitmem_check_loop(project_root: Path, file_path: str) -> bool:
    """Check if a file is in an edit loop."""
    loop_info = gitmem_get_loop_info(project_root, file_path)
    if loop_info["in_loop"]:
        logger.warning(
            f"Loop detected: {file_path} has {loop_info['change_count']} "
            f"changes without checkpoint"
        )
    return loop_info["in_loop"]


def gitmem_get_loop_info(project_root: Path, file_path: str) -> dict[str, Any]:
    """Get detailed loop information for a file."""
    result: dict[str, Any] = {
        "in_loop": False,
        "change_count": 0,
        "last_checkpoint": None,
    }

    if not gitmem_is_initialized(project_root):
        return result

    log_output = _run_git_command(
        project_root,
        ["log", "--oneline", "--follow", "--", file_path],
        check=False,
    )

    if not log_output:
        return result

    commits = log_output.split("\n")
    result["change_count"] = len(commits)

    for commit_line in commits[:10]:
        commit_hash = commit_line.split()[0] if commit_line else ""
        if commit_hash:
            tags_output = _run_git_command(
                project_root,
                ["tag", "--points-at", commit_hash],
                check=False,
            )
            if tags_output:
                result["last_checkpoint"] = tags_output.split("\n")[0]
                break

    result["in_loop"] = (
        result["change_count"] >= GITMEM_LOOP_THRESHOLD and result["last_checkpoint"] is None
    )
    return result


def gitmem_history(project_root: Path, file_path: str, limit: int = 20) -> list[dict[str, str]]:
    """Get commit history for a file."""
    if not gitmem_is_initialized(project_root):
        return []

    log_format = "--format=%H|%s|%ci"
    log_output = _run_git_command(
        project_root,
        ["log", log_format, f"-{limit}", "--follow", "--", file_path],
        check=False,
    )

    if not log_output:
        return []

    history: list[dict[str, str]] = []
    for line in log_output.split("\n"):
        if "|" in line:
            parts = line.split("|", 2)
            if len(parts) >= 3:
                history.append({"hash": parts[0], "message": parts[1], "date": parts[2]})
    return history


def gitmem_diff(
    project_root: Path,
    file_path: str,
    from_rev: str = "HEAD~1",
    to_rev: str = "HEAD",
) -> str:
    """Compare versions of a file."""
    if not gitmem_is_initialized(project_root):
        return "GitMem not initialized"

    file_path = Path(file_path).as_posix()
    return _run_git_command(
        project_root,
        ["diff", from_rev, to_rev, "--", file_path],
        check=False,
    )


def gitmem_rollback(
    project_root: Path,
    file_path: str,
    to_rev: str = "HEAD~1",
) -> bool:
    """Rollback a file to a previous version."""
    if not gitmem_is_initialized(project_root):
        logger.warning("GitMem not initialized, cannot rollback")
        return False

    file_path = Path(file_path).as_posix()

    try:
        content = _run_git_command(
            project_root,
            ["show", f"{to_rev}:{file_path}"],
            check=True,
        )
    except RuntimeError as e:
        logger.error(f"Cannot find revision {to_rev}: {e}")
        return False

    source_path = project_root / file_path
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(content, encoding="utf-8")

    gitmem_commit(project_root, file_path, f"Rollback {file_path} to {to_rev}")
    logger.info(f"Rolled back {file_path} to {to_rev}")
    return True
