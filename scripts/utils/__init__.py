"""Utilities module for AI Research Orchestrator.

This module provides utility functions organized by category:
- yaml_utils: YAML serialization and file operations
- path_utils: Path normalization and security validation
- text_utils: Text processing and slug generation
- template_utils: Template rendering and materialization
"""

from .logging_utils import setup_logging
from .path_utils import normalize_relative_path
from .template_utils import (
    build_template_variables,
    render_template_string,
    render_template_tree,
    write_text_if_needed,
)
from .text_utils import build_list_section, shell_join, slugify
from .yaml_utils import read_yaml, write_yaml, yaml_dump, yaml_load

__all__ = [
    # YAML utilities
    "yaml_dump",
    "yaml_load",
    "read_yaml",
    "write_yaml",
    # Path utilities
    "normalize_relative_path",
    # Text utilities
    "slugify",
    "build_list_section",
    "shell_join",
    # Logging utilities
    "setup_logging",
    # Template utilities
    "build_template_variables",
    "render_template_string",
    "render_template_tree",
    "write_text_if_needed",
]
