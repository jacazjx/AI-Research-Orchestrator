"""GitMem module for lightweight version control of agent documents."""

from gitmem.tracker import (  # noqa: F401
    GITMEM_DIR,
    GITMEM_LOOP_THRESHOLD,
    GITMEM_TRACKED_DIRS,
    gitmem_check_loop,
    gitmem_checkpoint,
    gitmem_commit,
    gitmem_diff,
    gitmem_get_loop_info,
    gitmem_history,
    gitmem_init,
    gitmem_is_initialized,
    gitmem_list_tags,
    gitmem_rollback,
)

__all__ = [
    "GITMEM_DIR",
    "GITMEM_LOOP_THRESHOLD",
    "GITMEM_TRACKED_DIRS",
    "gitmem_init",
    "gitmem_is_initialized",
    "gitmem_commit",
    "gitmem_checkpoint",
    "gitmem_list_tags",
    "gitmem_check_loop",
    "gitmem_get_loop_info",
    "gitmem_history",
    "gitmem_diff",
    "gitmem_rollback",
]
