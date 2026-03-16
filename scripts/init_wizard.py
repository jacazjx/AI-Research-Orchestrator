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

from exceptions import ValidationError

# Import local modules
import gpu_manager
import legacy_handler
import prompts
import user_config

# Configure module logger
logger = logging.getLogger(__name__)

# Research type definitions
RESEARCH_TYPES: dict[str, dict[str, Any]] = {
    "ml_experiment": {
        "label": "ML Experiment",
        "description": "Machine learning experiments with training and evaluation",
        "requires_gpu": True,
    },
    "theory": {
        "label": "Theory Research",
        "description": "Theoretical analysis and mathematical proofs",
        "requires_gpu": False,
    },
    "survey": {
        "label": "Survey/Review",
        "description": "Literature review and survey papers",
        "requires_gpu": False,
    },
    "applied": {
        "label": "Applied Research",
        "description": "Applied research with real-world applications",
        "requires_gpu": True,
    },
}

# Valid phases for starting point
VALID_STARTING_PHASES = ["survey", "pilot", "experiments", "paper", "reflection"]


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
    """

    research_idea: str = ""
    research_type: str = "ml_experiment"
    project_id: str | None = None
    starting_phase: str = "survey"
    compute_config: dict[str, Any] = field(default_factory=dict)
    user_profile: dict[str, str] = field(default_factory=dict)
    existing_resources_mode: str = "preserve"
    legacy_analysis: dict[str, Any] = field(default_factory=dict)

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

        prompts.print_header("AI Research Orchestrator - Initialization Wizard")

        print("Welcome! This wizard will help you set up a new research project.")
        print("\nThe setup process includes:")
        print("  1. Define your research idea")
        print("  2. Select research type")
        print("  3. Handle existing resources (if any)")
        print("  4. Configure compute resources")
        print("  5. Confirm user profile")
        print("  6. Review and finalize")

        print("\nYour settings will be saved to:")
        print(f"  Project Root: {self.project_root}")

        prompts.prompt_yes_no("\nReady to begin?", default=True)

    def step_research_idea(self) -> None:
        """Step 2: Collect research idea from user."""
        if not self.interactive:
            # Use prefill or default in non-interactive mode
            if not self.responses.research_idea:
                self.responses.research_idea = "Research project"
            return

        prompts.print_section("Step 1: Research Idea")

        print("Please describe your research idea or problem statement.")
        print("This will be used to initialize your project and generate templates.")

        idea = prompts.prompt_multiline(
            "\nEnter your research idea",
            required=True,
            default=self.responses.research_idea,
        )

        self.responses.research_idea = idea

        # Generate project ID if not already set
        if not self.responses.project_id:
            suggested_id = prompts.generate_project_id_from_idea(idea)
            print(f"\nSuggested project ID: {suggested_id}")

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
                    error_message="Invalid project ID. Use lowercase letters, numbers, and hyphens only. Must start with a letter.",
                )

    def step_research_type(self) -> None:
        """Step 3: Select research type."""
        if not self.interactive:
            return

        prompts.print_section("Step 2: Research Type")

        print("Select the type of research you'll be conducting:")

        # Build choices dict
        choices = {
            key: f"{info['label']} - {info['description']}"
            for key, info in RESEARCH_TYPES.items()
        }

        selected = prompts.prompt_choice(
            "\nSelect research type",
            choices=choices,
            default=self.responses.research_type,
        )

        self.responses.research_type = selected

        # Show additional info
        info = RESEARCH_TYPES[selected]
        print(f"\nSelected: {info['label']}")
        if info["requires_gpu"]:
            print("Note: This research type typically requires GPU resources.")

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
        """Step 4: Detect and handle existing resources."""
        prompts.print_section("Step 3: Existing Resources")

        # Analyze directory
        try:
            analysis = legacy_handler.analyze_directory_contents(self.project_root)
            self.responses.legacy_analysis = {
                "is_empty": analysis.is_empty,
                "total_files": analysis.total_files,
                "recognized_patterns": analysis.recognized_patterns,
                "orphan_files_count": len(analysis.orphan_files),
                "orphan_files": analysis.orphan_files[:10],  # First 10
            }
        except legacy_handler.LegacyHandlerError as e:
            logger.warning("Failed to analyze directory: %s", e)
            self.responses.legacy_analysis = {"error": str(e)}
            return

        if analysis.is_empty:
            print("The project directory is empty. Ready for initialization.")
            self.responses.existing_resources_mode = "preserve"
            return

        if not self.interactive:
            # Default to preserve in non-interactive mode
            self.responses.existing_resources_mode = "preserve"
            return

        # Show analysis
        print(legacy_handler.format_analysis_summary(analysis))

        if analysis.orphan_files:
            print("\nHow would you like to handle these files?")

            choices = {
                "preserve": "Preserve - Keep files in place (recommended)",
                "migrate": "Migrate - Move non-standard files to legacy backup",
                "cancel": "Cancel - Abort initialization",
            }

            selected = prompts.prompt_choice(
                "Select handling mode",
                choices=choices,
                default="preserve",
            )

            self.responses.existing_resources_mode = selected

            if selected == "migrate":
                print("\nNon-standard files will be moved to .autoresearch/legacy/")
                prompts.prompt_yes_no("Proceed with migration?", default=True)
        else:
            print("\nAll files match recognized patterns. No action needed.")
            self.responses.existing_resources_mode = "preserve"

    def step_compute_resources(self) -> None:
        """Step 5: Configure compute resources (GPU)."""
        prompts.print_section("Step 4: Compute Resources")

        # Check if GPU is needed
        research_info = RESEARCH_TYPES.get(self.responses.research_type, {})
        needs_gpu = research_info.get("requires_gpu", False)

        if not needs_gpu:
            print("This research type does not typically require GPU resources.")
            self.responses.compute_config = {
                "requires_gpu": False,
                "gpu_preference": "none",
                "selected_gpu": None,
            }
            return

        print("This research type typically benefits from GPU acceleration.")

        if not self.interactive:
            # Auto-configure in non-interactive mode
            self.responses.compute_config = {
                "requires_gpu": True,
                "gpu_preference": "auto",
                "selected_gpu": None,
            }
            return

        # Get user's GPU preference
        print("\nGPU Preference:")

        choices = {
            "auto": "Auto - Let the system select the best available GPU",
            "local": "Local - Use only local GPUs",
            "remote": "Remote - Use only remote/cloud GPUs",
            "none": "None - No GPU required for this project",
        }

        preference = prompts.prompt_choice(
            "Select GPU preference",
            choices=choices,
            default="auto",
        )

        self.responses.compute_config = {
            "requires_gpu": True,
            "gpu_preference": preference,
            "selected_gpu": None,
        }

        # Discover available GPUs
        if preference in ("auto", "local"):
            print("\nDiscovering local GPUs...")
            local_gpus = gpu_manager.discover_local_gpus()

            if local_gpus:
                print(f"Found {len(local_gpus)} local GPU(s):")
                for gpu in local_gpus:
                    print(f"  - {gpu['name']} ({gpu['memory_gb']:.1f} GB)")
            else:
                print("No local GPUs detected.")

        # Ask about registering remote GPU
        if preference in ("auto", "remote"):
            if prompts.prompt_yes_no(
                "\nWould you like to register a remote GPU?",
                default=False,
            ):
                self._prompt_remote_gpu_registration()

    def _prompt_remote_gpu_registration(self) -> None:
        """Prompt user to register a remote GPU."""
        print("\nRegister Remote GPU:")
        print("Enter SSH connection details for the remote server with GPU.")

        host = prompts.prompt_text("SSH Host", required=True)
        user = prompts.prompt_text("SSH User", required=True)
        port = int(prompts.prompt_text("SSH Port", default="22"))

        print(f"\nProbing GPU at {user}@{host}...")

        gpu_info = gpu_manager.probe_remote_gpu(host, user, port)

        if gpu_info:
            print(f"Found: {gpu_info['name']} ({gpu_info['memory_gb']:.1f} GB)")

            if prompts.prompt_yes_no("Register this GPU?", default=True):
                device = gpu_manager.GPUDevice(
                    id=gpu_info["id"],
                    name=gpu_info["name"],
                    type="ssh",
                    status="available",
                    memory_gb=gpu_info["memory_gb"],
                    host=host,
                    user=user,
                    port=port,
                )
                gpu_manager.register_gpu(device)
                print(f"Registered GPU: {device.id}")
        else:
            print("Could not detect GPU on remote server.")
            if prompts.prompt_yes_no("Register anyway?", default=False):
                safe_host = host.replace(".", "-").replace(":", "-")
                device = gpu_manager.GPUDevice(
                    id=f"remote-{safe_host}-0",
                    name="Unknown Remote GPU",
                    type="ssh",
                    status="available",
                    host=host,
                    user=user,
                    port=port,
                )
                gpu_manager.register_gpu(device)
                print(f"Registered GPU: {device.id}")

    def step_user_profile(self) -> None:
        """Step 6: Confirm or update user profile."""
        prompts.print_section("Step 5: User Profile")

        # Load existing user config
        config = user_config.load_user_config()
        author = config.get("author", {})

        self.responses.user_profile = {
            "name": author.get("name", ""),
            "email": author.get("email", ""),
            "institution": author.get("institution", ""),
            "orcid": author.get("orcid", ""),
        }

        if not self.interactive:
            return

        # Show current profile
        if any(author.values()):
            print("Current user profile:")
            prompts.print_summary(
                "Profile",
                {
                    "Name": author.get("name", ""),
                    "Email": author.get("email", ""),
                    "Institution": author.get("institution", ""),
                    "ORCID": author.get("orcid", ""),
                },
            )

            if prompts.prompt_yes_no("\nIs this information correct?", default=True):
                return
        else:
            print("No user profile found. Please provide your information.")

        # Collect/update profile
        print("\nEnter your information (press Enter to keep current value):")

        name = prompts.prompt_text(
            "Name",
            default=author.get("name", ""),
            required=True,
        )
        email = prompts.prompt_text(
            "Email",
            default=author.get("email", ""),
            required=True,
            validator=prompts.validate_email,
            error_message="Invalid email format. Please enter a valid email.",
        )
        institution = prompts.prompt_text(
            "Institution",
            default=author.get("institution", ""),
        )
        orcid = prompts.prompt_text(
            "ORCID (optional)",
            default=author.get("orcid", ""),
            validator=prompts.validate_orcid,
            error_message="Invalid ORCID format. Expected: 0000-0000-0000-000X",
        )

        # Update profile
        self.responses.user_profile = {
            "name": name,
            "email": email,
            "institution": institution,
            "orcid": orcid,
        }

        # Save to user config
        author_info = user_config.AuthorInfo(
            name=name,
            email=email,
            institution=institution,
            orcid=orcid,
        )
        user_config.set_author_info(author_info)
        print("\nProfile saved to user configuration.")

    def step_confirmation(self) -> None:
        """Step 7: Review and confirm all settings."""
        if not self.interactive:
            return

        prompts.print_section("Step 6: Confirmation")

        print("Please review your settings before proceeding:\n")

        # Display summary
        print("=" * 50)
        print("PROJECT SUMMARY")
        print("=" * 50)

        print(f"\nProject ID: {self.responses.project_id}")
        print(f"Project Root: {self.project_root}")
        print(f"Starting Phase: {self.responses.starting_phase}")

        print(f"\nResearch Type: {RESEARCH_TYPES[self.responses.research_type]['label']}")
        print(f"\nResearch Idea:\n  {self.responses.research_idea[:200]}...")
        if len(self.responses.research_idea) > 200:
            print("  [truncated]")

        print(f"\nExisting Resources: {self.responses.existing_resources_mode}")
        if self.responses.legacy_analysis.get("total_files"):
            print(f"  Files found: {self.responses.legacy_analysis['total_files']}")

        print(f"\nCompute Config:")
        print(f"  GPU Preference: {self.responses.compute_config.get('gpu_preference', 'auto')}")

        print(f"\nUser Profile:")
        print(f"  Name: {self.responses.user_profile.get('name', '(not set)')}")
        print(f"  Email: {self.responses.user_profile.get('email', '(not set)')}")
        print(f"  Institution: {self.responses.user_profile.get('institution', '(not set)')}")

        print("\n" + "=" * 50)

        if not prompts.prompt_yes_no("\nProceed with initialization?", default=True):
            raise ValidationError("Initialization cancelled by user")

        print("\nInitialization settings confirmed. Proceeding...")


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