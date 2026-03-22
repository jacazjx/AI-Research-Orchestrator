"""State management module for AI Research Orchestrator.

Provides:
- I/O: load_state, save_state, load_json, write_json
- Builder: build_state
- Validator: validate_state_schema, validate_deliverable_content,
  validate_structured_signals, validate_deliverable_location,
  parse_markdown_fields, is_unmodified_template,
  ensure_complete_deliverables
"""

from state.builder import build_state  # noqa: F401
from state.io import (  # noqa: F401
    append_state_log,
    load_json,
    load_state,
    resolve_deliverable_path,
    save_state,
    write_json,
)
from state.validator import (  # noqa: F401
    ensure_complete_deliverables,
    is_unmodified_template,
    parse_markdown_fields,
    validate_deliverable_content,
    validate_deliverable_location,
    validate_state_schema,
    validate_structured_signals,
)

__all__ = [
    "load_state",
    "save_state",
    "load_json",
    "write_json",
    "resolve_deliverable_path",
    "append_state_log",
    "build_state",
    "validate_state_schema",
    "validate_deliverable_content",
    "validate_structured_signals",
    "validate_deliverable_location",
    "parse_markdown_fields",
    "is_unmodified_template",
    "ensure_complete_deliverables",
]
