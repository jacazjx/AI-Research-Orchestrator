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


class ValidationError(OrchestratorError):
    """Raised when validation of deliverables, signals, or state fails."""

    def __init__(
        self,
        message: str,
        *,
        errors: list[str] | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.errors = errors or []


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


class CommandExecutionError(OrchestratorError):
    """Raised when a subprocess command fails."""

    def __init__(
        self,
        message: str,
        *,
        command: list[str] | None = None,
        exit_code: int | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


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


class TemplateError(OrchestratorError):
    """Raised when template rendering fails."""

    def __init__(
        self,
        message: str,
        *,
        template_path: str | None = None,
        variable: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.template_path = template_path
        self.variable = variable


class DependencyError(OrchestratorError):
    """Raised when a required external dependency or skill is missing."""

    def __init__(
        self,
        message: str,
        *,
        dependency: str | None = None,
        path: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.dependency = dependency
        self.path = path