"""
Custom exceptions for the AI Research Orchestrator.

This module defines a hierarchy of exceptions to provide clear error
classification and enable precise error handling throughout the codebase.
"""

from __future__ import annotations


class OrchestratorError(Exception):
    """Base exception for all orchestrator errors."""

    def __init__(self, message: str, *, context: dict[str, str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}


class StateError(OrchestratorError):
    """Raised when the research state is invalid or corrupted."""

    def __init__(
        self,
        message: str,
        *,
        state_file: str | None = None,
        field: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.state_file = state_file
        self.field = field


class PathSecurityError(OrchestratorError):
    """Raised when a path violates security constraints (traversal, absolute, etc.)."""

    def __init__(
        self,
        message: str,
        *,
        path: str | None = None,
        reason: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.path = path
        self.reason = reason


class ConfigurationError(OrchestratorError):
    """Raised when configuration is missing or invalid."""

    def __init__(
        self,
        message: str,
        *,
        config_file: str | None = None,
        key: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.config_file = config_file
        self.key = key


class PhaseTransitionError(OrchestratorError):
    """Raised when an invalid phase transition is attempted."""

    def __init__(
        self,
        message: str,
        *,
        from_phase: str | None = None,
        to_phase: str | None = None,
        reason: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.from_phase = from_phase
        self.to_phase = to_phase
        self.reason = reason


class StateSchemaError(ValueError):
    """Raised when research-state.yaml is missing required fields or has invalid values."""

    pass
