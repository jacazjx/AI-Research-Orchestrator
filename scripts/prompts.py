"""
Interactive prompt and validation utilities for AI Research Orchestrator.

This module provides reusable prompt functions and validation helpers
for the initialization wizard and other interactive components.

Features:
- Text input with optional validation
- Multiple-choice selection
- Yes/No confirmation
- Project ID validation
- Email validation
"""

from __future__ import annotations

import re
import sys
from typing import Any


def prompt_text(
    message: str,
    default: str = "",
    required: bool = False,
    validator: callable[[str], bool] | None = None,
    error_message: str = "Invalid input. Please try again.",
) -> str:
    """Prompt user for text input.

    Args:
        message: Prompt message to display.
        default: Default value if user presses Enter (empty string if not provided).
        required: If True, user must provide a non-empty value.
        validator: Optional function to validate input. Should return True for valid input.
        error_message: Message to display when validation fails.

    Returns:
        User input string, or default value if user pressed Enter.
    """
    while True:
        # Build prompt with default indicator
        if default:
            prompt_str = f"{message} [{default}]: "
        else:
            prompt_str = f"{message}: "

        try:
            user_input = input(prompt_str).strip()
        except EOFError:
            # Non-interactive mode, return default
            return default

        # Use default if empty
        if not user_input:
            if required and not default:
                print("This field is required. Please provide a value.")
                continue
            return default

        # Validate if validator provided
        if validator and not validator(user_input):
            print(error_message)
            continue

        return user_input


def prompt_choice(
    message: str,
    choices: list[str] | dict[str, str],
    default: str | None = None,
) -> str:
    """Prompt user to select from multiple choices.

    Args:
        message: Prompt message to display.
        choices: List of choices or dict mapping choice keys to display labels.
        default: Default choice key if user presses Enter.

    Returns:
        Selected choice key.

    Raises:
        ValueError: If choices is empty or default is invalid.
    """
    if not choices:
        raise ValueError("Choices cannot be empty")

    # Convert list to dict for uniform handling
    if isinstance(choices, list):
        choices_dict = {c: c for c in choices}
    else:
        choices_dict = choices

    choice_keys = list(choices_dict.keys())

    if default and default not in choice_keys:
        raise ValueError(f"Default '{default}' is not a valid choice")

    # Display choices
    print(f"\n{message}")
    for i, key in enumerate(choice_keys, 1):
        label = choices_dict[key]
        if key == default:
            print(f"  [{i}] {label} (default)")
        else:
            print(f"  [{i}] {label}")

    while True:
        prompt_str = "Select option"
        if default:
            prompt_str += f" [{default}]"
        prompt_str += ": "

        try:
            user_input = input(prompt_str).strip()
        except EOFError:
            # Non-interactive mode, return default or first choice
            return default if default else choice_keys[0]

        # Handle empty input
        if not user_input:
            if default:
                return default
            print("Please select an option.")
            continue

        # Handle numeric input
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(choice_keys):
                return choice_keys[idx]
            print(f"Invalid selection. Please enter 1-{len(choice_keys)}.")
            continue

        # Handle string input (choice key)
        if user_input in choice_keys:
            return user_input

        # Try case-insensitive match
        lower_input = user_input.lower()
        for key in choice_keys:
            if key.lower() == lower_input:
                return key

        print(f"Invalid choice. Please select from: {', '.join(choice_keys)}")


def prompt_yes_no(message: str, default: bool = True) -> bool:
    """Prompt user for yes/no confirmation.

    Args:
        message: Prompt message to display.
        default: Default value if user presses Enter.

    Returns:
        True for yes, False for no.
    """
    default_str = "Y/n" if default else "y/N"
    prompt_str = f"{message} [{default_str}]: "

    while True:
        try:
            user_input = input(prompt_str).strip().lower()
        except EOFError:
            # Non-interactive mode, return default
            return default

        if not user_input:
            return default

        if user_input in ("y", "yes", "true", "1"):
            return True
        if user_input in ("n", "no", "false", "0"):
            return False

        print("Please enter 'y' for yes or 'n' for no.")


def validate_project_id(project_id: str) -> bool:
    """Validate project ID format.

    A valid project ID:
    - Contains only lowercase letters, numbers, and hyphens
    - Starts with a letter
    - Is between 2 and 64 characters
    - Does not end with a hyphen
    - Does not contain consecutive hyphens

    Args:
        project_id: Project ID to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not project_id:
        return False

    if len(project_id) < 2 or len(project_id) > 64:
        return False

    if not project_id[0].isalpha():
        return False

    if project_id[-1] == "-":
        return False

    if "--" in project_id:
        return False

    # Check for valid characters
    pattern = r"^[a-z][a-z0-9-]*$"
    return bool(re.match(pattern, project_id))


def validate_email(email: str) -> bool:
    """Validate email format.

    Uses a simple but practical email validation pattern.

    Args:
        email: Email address to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not email:
        return False

    # Simple but practical email pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_orcid(orcid: str) -> bool:
    """Validate ORCID format.

    ORCID format: 0000-0000-0000-000X (where X is a digit or X)

    Args:
        orcid: ORCID identifier to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not orcid:
        return True  # ORCID is optional

    pattern = r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$"
    return bool(re.match(pattern, orcid.upper()))


def format_choices(choices: list[str] | dict[str, str], default: str | None = None) -> str:
    """Format a list of choices for display.

    Args:
        choices: List of choices or dict mapping keys to labels.
        default: Default choice key to highlight.

    Returns:
        Formatted string of choices.
    """
    if isinstance(choices, list):
        choices_dict = {c: c for c in choices}
    else:
        choices_dict = choices

    parts = []
    for key, label in choices_dict.items():
        if key == default:
            parts.append(f"[{label}]")
        else:
            parts.append(label)

    return " | ".join(parts)


def generate_project_id_from_idea(idea: str) -> str:
    """Generate a project ID from a research idea.

    Creates a slug from the first few words of the idea.

    Args:
        idea: Research idea string.

    Returns:
        Generated project ID.
    """
    if not idea:
        return "research-project"

    # Extract first significant words
    words = re.findall(r"\b[a-zA-Z]+\b", idea.lower())

    if not words:
        return "research-project"

    # Take first 3-4 meaningful words
    significant_words = []
    skip_words = {"a", "an", "the", "of", "for", "in", "on", "to", "and", "or", "with"}

    for word in words[:10]:  # Look at first 10 words
        if word not in skip_words and len(word) > 1:
            significant_words.append(word)
            if len(significant_words) >= 4:
                break

    if not significant_words:
        return "research-project"

    # Create slug
    slug = "-".join(significant_words[:4])

    # Ensure it starts with a letter
    if not slug[0].isalpha():
        slug = "research-" + slug

    # Truncate if too long
    if len(slug) > 50:
        slug = slug[:50].rsplit("-", 1)[0]

    return slug


def print_header(title: str, width: int = 60) -> None:
    """Print a formatted header.

    Args:
        title: Header title.
        width: Total width of the header.
    """
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)
    print()


def print_section(title: str, width: int = 60) -> None:
    """Print a formatted section header.

    Args:
        title: Section title.
        width: Total width of the section line.
    """
    print()
    print(f"\n--- {title} ---")
    print()


def print_summary(title: str, items: dict[str, Any], indent: int = 2) -> None:
    """Print a formatted summary of key-value items.

    Args:
        title: Summary title.
        items: Dictionary of items to display.
        indent: Indentation level.
    """
    print(f"\n{title}:")
    indent_str = " " * indent

    for key, value in items.items():
        if value is None or value == "":
            display_value = "(not set)"
        elif isinstance(value, dict):
            display_value = "..."
        elif isinstance(value, list):
            display_value = f"[{len(value)} items]"
        else:
            display_value = str(value)

        print(f"{indent_str}{key}: {display_value}")


def prompt_multiline(
    message: str,
    end_marker: str = "END",
    default: str = "",
    required: bool = False,
) -> str:
    """Prompt for multi-line input.

    Args:
        message: Prompt message to display.
        end_marker: String to enter on a new line to finish input.
        default: Default value if user presses Enter immediately.
        required: If True, user must provide non-empty input.

    Returns:
        Multi-line input string.
    """
    print(f"\n{message}")
    print(f"(Enter '{end_marker}' on a new line to finish)")

    lines = []
    try:
        while True:
            line = input()
            if line.strip() == end_marker:
                break
            lines.append(line)
    except EOFError:
        pass

    result = "\n".join(lines).strip()

    if not result:
        if required and not default:
            print("This field is required. Please provide a value.")
            return prompt_multiline(message, end_marker, default, required)
        return default

    return result
