"""
User-level configuration management for AI Research Orchestrator.

This module provides functions to manage user-specific configuration that
persists across all research projects. Configuration is stored in
~/.autoresearch/user-config.yaml.

The configuration includes:
- Author information (name, email, institution, ORCID)
- User preferences (default venue, language settings)
- Research defaults (research type, GPU preference)

Priority: Project config > User config > Defaults
"""

from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from exceptions import ConfigurationError

# Configure module logger
logger = logging.getLogger(__name__)

# User config directory name
USER_CONFIG_DIR_NAME = ".autoresearch"

# Config file names
USER_CONFIG_FILENAME = "user-config.yaml"
GPU_REGISTRY_FILENAME = "gpu-registry.yaml"

# Current config version
CONFIG_VERSION = "1.0.0"


class AuthorInfo:
    """Author information for research projects.

    Attributes:
        name: Full name of the researcher.
        email: Email address.
        institution: Affiliated institution.
        orcid: ORCID identifier (optional).
    """

    def __init__(
        self,
        name: str = "",
        email: str = "",
        institution: str = "",
        orcid: str = "",
    ) -> None:
        self.name = name
        self.email = email
        self.institution = institution
        self.orcid = orcid

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "email": self.email,
            "institution": self.institution,
            "orcid": self.orcid,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuthorInfo:
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            institution=data.get("institution", ""),
            orcid=data.get("orcid", ""),
        )


class LanguagePreferences:
    """Language preferences for document generation.

    Attributes:
        process_docs: Language for process documentation (e.g., "zh-CN").
        paper_docs: Language for paper documentation (e.g., "en-US").
    """

    def __init__(
        self,
        process_docs: str = "zh-CN",
        paper_docs: str = "en-US",
    ) -> None:
        self.process_docs = process_docs
        self.paper_docs = paper_docs

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "process_docs": self.process_docs,
            "paper_docs": self.paper_docs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LanguagePreferences:
        """Create from dictionary."""
        return cls(
            process_docs=data.get("process_docs", "zh-CN"),
            paper_docs=data.get("paper_docs", "en-US"),
        )


class UserPreferences:
    """User preferences for research projects.

    Attributes:
        default_venue: Default publication venue.
        default_language: Language preferences for documents.
    """

    def __init__(
        self,
        default_venue: str = "",
        default_language: LanguagePreferences | None = None,
    ) -> None:
        self.default_venue = default_venue
        self.default_language = default_language or LanguagePreferences()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "default_venue": self.default_venue,
            "default_language": self.default_language.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserPreferences:
        """Create from dictionary."""
        lang_data = data.get("default_language", {})
        return cls(
            default_venue=data.get("default_venue", ""),
            default_language=LanguagePreferences.from_dict(lang_data),
        )


class ResearchDefaults:
    """Default settings for research projects.

    Attributes:
        research_type: Default type of research (e.g., "ml_experiment").
        gpu_preference: GPU selection preference ("auto", "local", "remote").
    """

    def __init__(
        self,
        research_type: str = "ml_experiment",
        gpu_preference: str = "auto",
    ) -> None:
        self.research_type = research_type
        self.gpu_preference = gpu_preference

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "research_type": self.research_type,
            "gpu_preference": self.gpu_preference,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ResearchDefaults:
        """Create from dictionary."""
        return cls(
            research_type=data.get("research_type", "ml_experiment"),
            gpu_preference=data.get("gpu_preference", "auto"),
        )


class UserConfig:
    """Complete user configuration.

    Attributes:
        version: Configuration schema version.
        author: Author information.
        preferences: User preferences.
        research_defaults: Research default settings.
    """

    def __init__(
        self,
        version: str = CONFIG_VERSION,
        author: AuthorInfo | None = None,
        preferences: UserPreferences | None = None,
        research_defaults: ResearchDefaults | None = None,
    ) -> None:
        self.version = version
        self.author = author or AuthorInfo()
        self.preferences = preferences or UserPreferences()
        self.research_defaults = research_defaults or ResearchDefaults()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "version": self.version,
            "author": self.author.to_dict(),
            "preferences": self.preferences.to_dict(),
            "research_defaults": self.research_defaults.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserConfig:
        """Create from dictionary."""
        return cls(
            version=data.get("version", CONFIG_VERSION),
            author=AuthorInfo.from_dict(data.get("author", {})),
            preferences=UserPreferences.from_dict(data.get("preferences", {})),
            research_defaults=ResearchDefaults.from_dict(data.get("research_defaults", {})),
        )


def get_user_config_dir() -> Path:
    """Get the user configuration directory path.

    Returns the path to ~/.autoresearch/. Creates the directory if it
    does not exist.

    Returns:
        Path to the user configuration directory.
    """
    config_dir = Path.home() / USER_CONFIG_DIR_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_user_config_path() -> Path:
    """Get the user configuration file path.

    Returns:
        Path to the user configuration file (~/.autoresearch/user-config.yaml).
    """
    return get_user_config_dir() / USER_CONFIG_FILENAME


def get_default_user_config() -> dict[str, Any]:
    """Get the default user configuration template.

    Returns:
        Dictionary containing default configuration values.
    """
    return UserConfig().to_dict()


def load_user_config() -> dict[str, Any]:
    """Load user configuration from disk.

    If the configuration file does not exist, returns the default
    configuration without creating a file.

    Returns:
        Dictionary containing user configuration values.

    Raises:
        ConfigurationError: If the configuration file exists but cannot
            be parsed.
    """
    config_path = get_user_config_path()

    if not config_path.exists():
        logger.debug("User config not found at %s, returning defaults", config_path)
        return get_default_user_config()

    try:
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Failed to parse user configuration: {exc}",
            config_file=str(config_path),
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to read user configuration: {exc}",
            config_file=str(config_path),
        ) from exc

    # Merge with defaults to ensure all fields exist
    defaults = get_default_user_config()
    merged = _deep_merge(defaults, data)

    logger.debug("Loaded user config from %s", config_path)
    return merged


def save_user_config(config: dict[str, Any]) -> None:
    """Save user configuration to disk.

    Uses atomic write pattern to prevent corruption if the process
    crashes mid-write.

    Args:
        config: Dictionary containing configuration to save.

    Raises:
        ConfigurationError: If the configuration cannot be saved.
    """
    config_path = get_user_config_path()

    # Ensure version is set
    if "version" not in config:
        config["version"] = CONFIG_VERSION

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Atomic write: write to temp file, then replace
        fd, temp_path = tempfile.mkstemp(
            dir=config_path.parent,
            prefix=config_path.name + ".",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            os.replace(temp_path, config_path)
        except Exception:
            # Clean up temp file on error
            Path(temp_path).unlink(missing_ok=True)
            raise

        logger.info("Saved user config to %s", config_path)
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to save user configuration: {exc}",
            config_file=str(config_path),
        ) from exc


def merge_configs(project_config: dict[str, Any], user_config: dict[str, Any]) -> dict[str, Any]:
    """Merge project and user configurations.

    Project configuration takes priority over user configuration.
    This allows project-specific settings to override user defaults.

    Args:
        project_config: Project-specific configuration (higher priority).
        user_config: User-level configuration (lower priority).

    Returns:
        Merged configuration dictionary with project values taking precedence.
    """
    # Start with user config as base
    result = _deep_merge(user_config, project_config)
    return result


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries.

    Values in override take precedence over values in base.
    Nested dictionaries are merged recursively.

    Args:
        base: Base dictionary (lower priority).
        override: Override dictionary (higher priority).

    Returns:
        New dictionary with merged values.
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def get_author_info() -> AuthorInfo:
    """Get author information from user configuration.

    Returns:
        AuthorInfo object with user's author information.
    """
    config = load_user_config()
    return AuthorInfo.from_dict(config.get("author", {}))


def set_author_info(author: AuthorInfo) -> None:
    """Update author information in user configuration.

    Args:
        author: AuthorInfo object with author details to save.
    """
    config = load_user_config()
    config["author"] = author.to_dict()
    save_user_config(config)


def get_research_defaults() -> ResearchDefaults:
    """Get research defaults from user configuration.

    Returns:
        ResearchDefaults object with user's default settings.
    """
    config = load_user_config()
    return ResearchDefaults.from_dict(config.get("research_defaults", {}))


def set_research_defaults(defaults: ResearchDefaults) -> None:
    """Update research defaults in user configuration.

    Args:
        defaults: ResearchDefaults object with settings to save.
    """
    config = load_user_config()
    config["research_defaults"] = defaults.to_dict()
    save_user_config(config)


def init_user_config(
    name: str = "",
    email: str = "",
    institution: str = "",
    orcid: str = "",
    default_venue: str = "",
    process_docs_lang: str = "zh-CN",
    paper_docs_lang: str = "en-US",
    research_type: str = "ml_experiment",
    gpu_preference: str = "auto",
) -> Path:
    """Initialize user configuration with provided values.

    Creates a new user configuration file if it doesn't exist,
    or updates existing configuration with provided values.

    Args:
        name: Author name.
        email: Author email.
        institution: Author institution.
        orcid: Author ORCID.
        default_venue: Default publication venue.
        process_docs_lang: Language for process docs.
        paper_docs_lang: Language for paper docs.
        research_type: Default research type.
        gpu_preference: GPU selection preference.

    Returns:
        Path to the configuration file.
    """
    config = load_user_config()

    # Update author info if provided
    if name or email or institution or orcid:
        author = AuthorInfo.from_dict(config.get("author", {}))
        if name:
            author.name = name
        if email:
            author.email = email
        if institution:
            author.institution = institution
        if orcid:
            author.orcid = orcid
        config["author"] = author.to_dict()

    # Update preferences if provided
    if default_venue or process_docs_lang or paper_docs_lang:
        prefs = UserPreferences.from_dict(config.get("preferences", {}))
        if default_venue:
            prefs.default_venue = default_venue
        if process_docs_lang:
            prefs.default_language.process_docs = process_docs_lang
        if paper_docs_lang:
            prefs.default_language.paper_docs = paper_docs_lang
        config["preferences"] = prefs.to_dict()

    # Update research defaults if provided
    if research_type or gpu_preference:
        defaults = ResearchDefaults.from_dict(config.get("research_defaults", {}))
        if research_type:
            defaults.research_type = research_type
        if gpu_preference:
            defaults.gpu_preference = gpu_preference
        config["research_defaults"] = defaults.to_dict()

    save_user_config(config)
    return get_user_config_path()
