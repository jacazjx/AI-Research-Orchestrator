#!/usr/bin/env python3
"""Interactive initialization wizard for AI Research Orchestrator.

This module provides an interactive wizard that guides users through the
process of initializing a new research project. It collects research ideas,
configures resources, and integrates with existing modules.

Wizard Steps:
    1. Welcome - Display welcome message and overview
    2. Research Idea - Collect research idea/topic
    3. Research Type - Select type of research
    4. Existing Resources - Handle existing directory contents
    5. Compute Resources - Configure GPU/compute settings
    6. User Profile - Confirm or update user information
    7. Confirmation - Review and confirm all settings

Usage:
    from init_wizard import InitWizard

    wizard = InitWizard(project_root=Path("/path/to/project"))
    responses = wizard.run()
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules  # noqa: E402
import gpu_manager  # noqa: E402
import legacy_handler  # noqa: E402
import prompts  # noqa: E402
import user_config  # noqa: E402
from exceptions import ValidationError  # noqa: E402

# Configure module logger
logger = logging.getLogger(__name__)

# Research type definitions
RESEARCH_TYPES: dict[str, dict[str, Any]] = {
    "ml_experiment": {
        "label": "ML Experiment",
        "description": "Machine learning experiments with training and evaluation",
        "requires_gpu": True,
        "example": "Fine-tuning a language model for code generation",
    },
    "theory": {
        "label": "Theory Research",
        "description": "Theoretical analysis and mathematical proofs",
        "requires_gpu": False,
        "example": "Convergence analysis of optimization algorithms",
    },
    "survey": {
        "label": "Survey/Review",
        "description": "Literature review and survey papers",
        "requires_gpu": False,
        "example": "A comprehensive survey on transformer architectures",
    },
    "applied": {
        "label": "Applied Research",
        "description": "Applied research with real-world applications",
        "requires_gpu": True,
        "example": "Medical image classification for disease detection",
    },
}

# Example research ideas for new users
EXAMPLE_IDEAS = [
    "How does the number of attention heads affect model performance on long-context tasks?",
    "Can we improve transformer efficiency by replacing attention with a simpler mechanism?",
    "What are the trade-offs between model size and inference speed for code generation?",
    "How do different data augmentation strategies impact few-shot learning?",
]

# Total wizard steps for progress indicator
TOTAL_WIZARD_STEPS = 7

# Valid phases for starting point
VALID_STARTING_PHASES = ["survey", "pilot", "experiments", "paper", "reflection"]


def print_welcome_banner() -> None:
    """Print a visually appealing welcome banner."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║        🔬  AI Research Orchestrator  🔬                     ║")
    print("║                                                              ║")
    print("║     From idea to paper in 5 structured phases               ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def print_quick_help() -> None:
    """Print quick help for navigation."""
    print("  Navigation tips:")
    print("  • Press Enter to accept default values")
    print("  • Type '?' for help on any field")
    print("  • Type 'b' to go back to previous step")
    print()


@dataclass
class WizardResponses:
    """Container for all wizard responses.

    Attributes:
        research_idea: The research idea or problem statement.
        research_type: Type of research (ml_experiment, theory, survey, applied).
        project_id: Unique project identifier.
        starting_phase: Phase to start the project at.
        compute_config: GPU and compute configuration.
        user_profile: User profile information from user_config.
        existing_resources_mode: How to handle existing files (preserve, migrate, cancel).
        legacy_analysis: Analysis of existing directory contents.
        clarity_score: Intent clarity score (0.0-1.0).
        clarification_rounds: Number of clarification rounds performed.
        clarified_idea: Final clarified research idea.
    """

    research_idea: str = ""
    research_type: str = "ml_experiment"
    project_id: str | None = None
    starting_phase: str = "survey"
    compute_config: dict[str, Any] = field(default_factory=dict)
    user_profile: dict[str, str] = field(default_factory=dict)
    existing_resources_mode: str = "preserve"
    legacy_analysis: dict[str, Any] = field(default_factory=dict)
    clarity_score: float = 0.0
    clarification_rounds: int = 0
    clarified_idea: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "research_idea": self.research_idea,
            "research_type": self.research_type,
            "project_id": self.project_id,
            "starting_phase": self.starting_phase,
            "compute_config": self.compute_config,
            "user_profile": self.user_profile,
            "existing_resources_mode": self.existing_resources_mode,
            "legacy_analysis": self.legacy_analysis,
            "clarity_score": self.clarity_score,
            "clarification_rounds": self.clarification_rounds,
            "clarified_idea": self.clarified_idea,
        }


class InitWizard:
    """Interactive initialization wizard for research projects.

    This wizard guides users through the initialization process, collecting
    necessary information and integrating with user_config, gpu_manager,
    and legacy_handler modules.

    Attributes:
        project_root: Path to the project root directory.
        interactive: Whether to run in interactive mode.
        responses: Collected wizard responses.
    """

    def __init__(
        self,
        project_root: Path,
        interactive: bool = True,
        prefill: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the wizard.

        Args:
            project_root: Path to the project root directory.
            interactive: If False, use defaults without prompting.
            prefill: Optional dictionary to prefill responses.
        """
        self.project_root = project_root.resolve()
        self.interactive = interactive
        self.responses = WizardResponses()

        # Apply prefilled values
        if prefill:
            for key, value in prefill.items():
                if hasattr(self.responses, key):
                    setattr(self.responses, key, value)

    def run(self) -> dict[str, Any]:
        """Run the complete wizard flow.

        Executes all wizard steps in sequence and returns the collected
        responses.

        Returns:
            Dictionary containing all wizard responses.
        """
        logger.info("Starting initialization wizard for %s", self.project_root)

        self.step_welcome()
        self.step_research_idea()
        self.step_intent_clarity_assessment()
        self.step_intent_clarification_loop()
        self.step_research_type()
        self.step_existing_resources()
        self.step_compute_resources()
        self.step_user_profile()
        self.step_confirmation()

        logger.info("Wizard completed successfully")
        return self.responses.to_dict()

    def step_welcome(self) -> None:
        """Step 1: Display welcome message and overview."""
        if not self.interactive:
            return

        print_welcome_banner()

        print("Welcome! This wizard will help you set up a new research project.")
        print()

        print_quick_help()

        print("The setup process includes:")
        print("  1. Define your research idea")
        print("  2. Assess and clarify your intent")
        print("  3. Select research type")
        print("  4. Handle existing resources (if any)")
        print("  5. Configure compute resources")
        print("  6. Confirm user profile")
        print("  7. Review and finalize")

        print(f"\n📁 Project location: {self.project_root}")

        prompts.prompt_yes_no("\nReady to begin?", default=True)

    def step_research_idea(self) -> None:
        """Step 2: Collect research idea from user."""
        if not self.interactive:
            # Use prefill or default in non-interactive mode
            if not self.responses.research_idea:
                self.responses.research_idea = "Research project"
            return

        prompts.set_step_context(1, TOTAL_WIZARD_STEPS)
        prompts.print_section("Research Idea")

        print("Describe your research idea or problem statement.")
        print("This will be used to initialize your project and generate templates.")
        print()

        # Show example ideas
        print("💡 Example ideas:")
        for i, ex in enumerate(EXAMPLE_IDEAS[:2], 1):
            print(f"   {i}. {ex[:60]}...")
        print()

        # Simplified input - single line first
        print(
            "Enter your research idea (one line is fine, or type 'more' for detailed input):"
        )

        idea = prompts.prompt_text(
            "",
            required=True,
            default=self.responses.research_idea,
            help_text=(
                "A clear description of what you want to research. "
                "Include the problem, approach, and expected outcome."
            ),
        )

        # Check if user wants more detailed input
        if idea.lower() == "more":
            print("\nEnter your detailed research idea (press Enter twice to finish):")
            idea = prompts.prompt_multiline(
                "",
                end_marker="",
                required=True,
                default=self.responses.research_idea,
            )

        self.responses.research_idea = idea

        # Generate project ID if not already set
        if not self.responses.project_id:
            suggested_id = prompts.generate_project_id_from_idea(idea)
            print(f"\n📋 Suggested project ID: {suggested_id}")

            use_suggested = prompts.prompt_yes_no(
                "Use this project ID?",
                default=True,
            )

            if use_suggested:
                self.responses.project_id = suggested_id
            else:
                self.responses.project_id = prompts.prompt_text(
                    "Enter project ID",
                    default=suggested_id,
                    required=True,
                    validator=prompts.validate_project_id,
                    error_message=(
                        "Invalid project ID. Use lowercase letters, numbers, and hyphens only. "
                        "Must start with a letter."
                    ),
                )

    def step_intent_clarity_assessment(self) -> None:
        prompts.set_step_context(2, TOTAL_WIZARD_STEPS)
        prompts.print_section("Intent Clarity")

        print("🔍 Analyzing your research idea...")
        idea_length = len(self.responses.research_idea.split())
        self.responses.clarity_score = min(1.0, idea_length / 20.0)

        if idea_length < 10:
            print("\n📊 Your research idea is brief.")
            print("   Consider using /insight command to develop it further.")
            if self.interactive:
                if prompts.prompt_yes_no(
                    "\nWould you like to continue with this idea?",
                    default=True,
                ):
                    self._trigger_brainstorming()
                else:
                    print("\nTip: Use /insight before initializing your project.")
        elif idea_length < 20:
            print(f"\n📈 Your idea has some detail ({idea_length} words).")
            print("   You can clarify more during the research process.")
        else:
            print(f"\n✅ Your research idea has good detail ({idea_length} words).")
            self.responses.clarified_idea = self.responses.research_idea

    def _trigger_brainstorming(self) -> None:
        print("\n💡 Your research idea needs more development.")
        print("   Tip: Use /insight command before initializing your project.")
        print("   This will help you clarify and refine your research idea.")

    def step_intent_clarification_loop(self) -> None:
        if not self.interactive:
            self.responses.clarified_idea = self.responses.research_idea
            return

        idea_length = len(self.responses.research_idea.split())
        if idea_length >= 20:
            self.responses.clarified_idea = self.responses.research_idea
            return

        prompts.print_section("Quick Clarification")

        questions = [
            "What specific problem are you trying to solve?",
            "What's your intuition about what might work?",
        ]

        for i, question in enumerate(questions, 1):
            print(f"\nQ{i}: {question}")
            response = prompts.prompt_text("Your answer", required=False, default="")
            if response.strip():
                self.responses.research_idea += (
                    f"\n\n[Clarification] {question}\n{response}"
                )

        self.responses.clarified_idea = self.responses.research_idea

    def step_research_type(self) -> None:
        """Step: Select research type."""
        if not self.interactive:
            return

        prompts.set_step_context(3, TOTAL_WIZARD_STEPS)
        prompts.print_section("Research Type")

        print("Select the type of research you'll be conducting:")
        print()

        # Build choices dict with examples
        for key, info in RESEARCH_TYPES.items():
            gpu_mark = "🎮" if info["requires_gpu"] else "📝"
            default_mark = " (default)" if key == self.responses.research_type else ""
            print(f"  [{key[0].upper()}] {gpu_mark} {info['label']}{default_mark}")
            print(f"      {info['description']}")
            print(f"      Example: {info['example']}")
            print()

        # Build choices dict
        choices = {
            key: f"{info['label']} - {info['description']}"
            for key, info in RESEARCH_TYPES.items()
        }

        selected = prompts.prompt_choice(
            "Select research type",
            choices=choices,
            default=self.responses.research_type,
        )

        self.responses.research_type = selected

        # Show additional info
        info = RESEARCH_TYPES[selected]
        print(f"\n✅ Selected: {info['label']}")
        if info["requires_gpu"]:
            print("📌 Note: This research type typically requires GPU resources.")

        # Ask about starting phase
        if prompts.prompt_yes_no(
            "\nStart from the beginning (survey phase)?",
            default=True,
        ):
            self.responses.starting_phase = "survey"
        else:
            phase_choices = {
                phase: phase.replace("_", " ").title()
                for phase in VALID_STARTING_PHASES
            }
            self.responses.starting_phase = prompts.prompt_choice(
                "Select starting phase",
                choices=phase_choices,
                default="survey",
            )

    def step_existing_resources(self) -> None:
        prompts.set_step_context(4, TOTAL_WIZARD_STEPS)
        prompts.print_section("Existing Resources")

        if not self.project_root.exists():
            self.responses.existing_resources_mode = "preserve"
            return

        existing_files = list(self.project_root.glob("*"))
        if not existing_files:
            self.responses.existing_resources_mode = "preserve"
            return

        if self.interactive:
            print(f"Found {len(existing_files)} items in project directory.")
            if prompts.prompt_yes_no("Preserve existing files?", default=True):
                self.responses.existing_resources_mode = "preserve"
            else:
                self.responses.existing_resources_mode = "migrate"
        else:
            self.responses.existing_resources_mode = "preserve"

    def step_compute_resources(self) -> None:
        prompts.set_step_context(5, TOTAL_WIZARD_STEPS)
        prompts.print_section("Compute Resources")

        research_info = RESEARCH_TYPES.get(self.responses.research_type, {})
        needs_gpu = research_info.get("requires_gpu", False)

        if not needs_gpu:
            self.responses.compute_config = {
                "requires_gpu": False,
                "gpu_preference": "none",
            }
            return

        if self.interactive:
            preference = prompts.prompt_choice(
                "GPU preference",
                choices={
                    "auto": "Auto",
                    "local": "Local only",
                    "remote": "Remote only",
                    "none": "None",
                },
                default="auto",
            )
        else:
            preference = "auto"

        self.responses.compute_config = {
            "requires_gpu": True,
            "gpu_preference": preference,
        }

    def step_user_profile(self) -> None:
        prompts.set_step_context(6, TOTAL_WIZARD_STEPS)
        prompts.print_section("User Profile")

        config = user_config.load_user_config()
        author = config.get("author", {})

        self.responses.user_profile = {
            "name": author.get("name", ""),
            "email": author.get("email", ""),
        }

        if not self.interactive:
            return

        if prompts.prompt_yes_no("Update user profile?", default=False):
            name = prompts.prompt_text(
                "Name", default=author.get("name", ""), required=False
            )
            email = prompts.prompt_text(
                "Email", default=author.get("email", ""), required=False
            )
            if name or email:
                self.responses.user_profile = {"name": name, "email": email}

    def step_confirmation(self) -> None:
        """Step 8: Review and confirm all settings."""
        if not self.interactive:
            return

        prompts.set_step_context(7, TOTAL_WIZARD_STEPS)
        prompts.print_section("Review & Confirm")

        print("Please review your settings before proceeding:\n")

        # Display summary in a nice format
        print("┌" + "─" * 56 + "┐")
        print("│                    PROJECT SUMMARY                      │")
        print("├" + "─" * 56 + "┤")

        project_id_display = self.responses.project_id or "(not set)"
        print(f"│  📋 Project ID:     {project_id_display:<37}│")
        print(f"│  📁 Location:       {str(self.project_root)[-37:]:<37}│")
        print(f"│  🎯 Starting Phase: {self.responses.starting_phase:<37}│")

        print("├" + "─" * 56 + "┤")

        research_type_label = RESEARCH_TYPES[self.responses.research_type]["label"]
        print(f"│  📚 Research Type:  {research_type_label:<37}│")

        # Display clarity score if available
        if self.responses.clarity_score > 0:
            clarity_status = (
                "✅ Clear" if self.responses.clarity_score >= 0.7 else "⚠️ Needs work"
            )
            clarity_line = (
                f"│  🎯 Intent Clarity: {self.responses.clarity_score:.2f} "
                f"({clarity_status}){' ' * 20}│"
            )
            print(clarity_line)

        print("├" + "─" * 56 + "┤")

        # Display research idea (truncated)
        display_idea = self.responses.clarified_idea or self.responses.research_idea
        idea_display = display_idea[:50].replace("\n", " ")
        if len(display_idea) > 50:
            idea_display += "..."
        print(f"│  💡 Research Idea:  {idea_display:<37}│")

        print("├" + "─" * 56 + "┤")

        gpu_pref = self.responses.compute_config.get("gpu_preference", "auto")
        print(f"│  🎮 GPU:            {gpu_pref:<37}│")

        user_name = self.responses.user_profile.get("name", "(not set)")
        print(f"│  👤 Author:         {user_name[:37]:<37}│")

        print("└" + "─" * 56 + "┘")

        print("\n📌 What will be created:")
        print("   • .autoresearch/  - System configuration and state")
        print("   • agents/         - Agent work directories")
        print("   • code/           - Code and experiments")
        print("   • docs/           - Research deliverables")
        print("   • paper/          - Manuscript files")

        if not prompts.prompt_yes_no("\n✅ Proceed with initialization?", default=True):
            raise ValidationError("Initialization cancelled by user")

        print("\n🚀 Creating project structure...")


def run_wizard(
    project_root: Path,
    interactive: bool = True,
    prefill: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Convenience function to run the initialization wizard.

    Args:
        project_root: Path to the project root directory.
        interactive: If False, use defaults without prompting.
        prefill: Optional dictionary to prefill responses.

    Returns:
        Dictionary containing all wizard responses.
    """
    wizard = InitWizard(
        project_root=project_root,
        interactive=interactive,
        prefill=prefill,
    )
    return wizard.run()


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Interactive initialization wizard for AI Research Orchestrator"
    )

    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to the project root directory",
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without interactive prompts (use defaults)",
    )

    parser.add_argument(
        "--idea",
        help="Research idea (skip prompt if provided)",
    )

    parser.add_argument(
        "--research-type",
        choices=list(RESEARCH_TYPES.keys()),
        default="ml_experiment",
        help="Type of research",
    )

    parser.add_argument(
        "--project-id",
        help="Project identifier",
    )

    parser.add_argument(
        "--starting-phase",
        choices=VALID_STARTING_PHASES,
        default="survey",
        help="Phase to start at",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output responses as JSON",
    )

    return parser


def main() -> int:
    """Main entry point for the wizard script."""
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(args.project_root)

    # Build prefill from arguments
    prefill = {}
    if args.idea:
        prefill["research_idea"] = args.idea
    if args.research_type:
        prefill["research_type"] = args.research_type
    if args.project_id:
        prefill["project_id"] = args.project_id
    if args.starting_phase:
        prefill["starting_phase"] = args.starting_phase

    try:
        responses = run_wizard(
            project_root=project_root,
            interactive=not args.non_interactive,
            prefill=prefill if prefill else None,
        )

        if args.json:
            print(json.dumps(responses, indent=2, default=str))
        else:
            print("\n" + "=" * 50)
            print("WIZARD COMPLETE")
            print("=" * 50)
            print(f"\nProject ID: {responses['project_id']}")
            print(f"Research Type: {responses['research_type']}")
            print(f"Starting Phase: {responses['starting_phase']}")

        return 0

    except ValidationError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\nWizard cancelled by user.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
