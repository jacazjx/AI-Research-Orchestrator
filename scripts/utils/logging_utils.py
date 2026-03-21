"""Logging utility functions for AI Research Orchestrator."""

from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    """Configure logging for the orchestrator.

    Args:
        level: Logging level (default: INFO).
        log_file: Optional path to a log file. Parent directories are created
            if they do not exist.
    """
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )
