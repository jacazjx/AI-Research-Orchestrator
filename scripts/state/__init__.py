"""State management module for AI Research Orchestrator.

Provides:
- I/O: load_state, save_state, load_json, write_json
- Builder: build_state
- Validator: validate_state_schema, validate_deliverable_content,
  validate_structured_signals, validate_deliverable_location,
  parse_markdown_fields, normalize_signal_value, is_unmodified_template,
  ensure_complete_deliverables
"""

from state.builder import build_state  # noqa: F401
from state.io import load_json, load_state, save_state, write_json  # noqa: F401
from state.validator import (  # noqa: F401
    ensure_complete_deliverables,
    is_unmodified_template,
    normalize_signal_value,
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
    "build_state",
    "validate_state_schema",
    "validate_deliverable_content",
    "validate_structured_signals",
    "validate_deliverable_location",
    "parse_markdown_fields",
    "normalize_signal_value",
    "is_unmodified_template",
    "ensure_complete_deliverables",
]
