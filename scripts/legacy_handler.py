#!/usr/bin/env python3
"""Legacy file handling and migration for non-empty directories.

This module handles the detection and processing of files in non-empty
project directories during initialization. It provides functionality to:
- Analyze directory contents and recognize patterns
- Move non-conforming files to a legacy backup
- Extract useful information from legacy files
- Generate migration reports

Usage:
    python3 scripts/legacy_handler.py --project-root /path/to/project --mode migrate
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from exceptions import OrchestratorError, ValidationError

from orchestrator_common import REQUIRED_DIRECTORIES  # noqa: E402

# Recognized file patterns for research projects
RECOGNIZED_PATTERNS: dict[str, list[str]] = {
    "paper_draft": ["*.tex", "*.md", "*.docx", "paper/**", "draft/**", "manuscript/**"],
    "code": ["*.py", "*.ipynb", "src/**", "code/**"],
    "data": ["*.csv", "*.json", "*.pkl", "*.pt", "*.pth", "data/**"],
    "experiments": ["experiments/**", "results/**", "outputs/**", "runs/**"],
    "references": ["*.bib", "references/**", "bibliography/**", "papers/**"],
    "notes": ["notes/**", "README*", "NOTES*"],
    "config": ["*.yaml", "*.yml", "*.toml", "config/**", "configs/**"],
    "models": ["*.pt", "*.pth", "*.ckpt", "*.h5", "models/**", "checkpoints/**"],
}

# Directories that are part of the orchestrator structure
ORCHESTRATOR_DIRS = {
    "paper",
    "code",
    "docs",
    "agents",
    ".autoresearch",
    "data",
    "experiments",
    "references",
    "notes",
}


@dataclass
class DirectoryAnalysis:
    """Analysis results for a directory.

    Attributes:
        is_empty: Whether the directory is empty
        total_files: Total number of files in the directory
        recognized_patterns: Files grouped by recognized patterns
        orphan_files: Files that don't match any recognized pattern
        recommended_actions: List of recommended actions for handling files
    """

    is_empty: bool
    total_files: int
    recognized_patterns: dict[str, list[str]] = field(default_factory=dict)
    orphan_files: list[str] = field(default_factory=list)
    recommended_actions: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MigrationResult:
    """Results of a legacy file migration.

    Attributes:
        success: Whether the migration was successful
        legacy_path: Path to the legacy backup directory
        migrated_files: List of files that were migrated
        extracted_content: Useful content extracted from legacy files
        report: Human-readable migration report
    """

    success: bool
    legacy_path: str | None = None
    migrated_files: list[str] = field(default_factory=list)
    extracted_content: dict[str, Any] = field(default_factory=dict)
    report: str = ""


class LegacyHandlerError(OrchestratorError):
    """Raised when legacy file handling fails."""

    def __init__(
        self,
        message: str,
        *,
        path: str | None = None,
        operation: str | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message, context=context)
        self.path = path
        self.operation = operation


def _match_pattern(file_path: Path, pattern: str, base_path: Path) -> bool:
    """Check if a file matches a pattern.

    Args:
        file_path: Path to the file
        pattern: Pattern to match (glob-style)
        base_path: Base path for relative matching

    Returns:
        True if the file matches the pattern
    """
    relative_path = file_path.relative_to(base_path)
    relative_str = str(relative_path)

    # Handle directory patterns (e.g., "paper/**")
    if "/**" in pattern:
        dir_pattern = pattern.replace("/**", "")
        return relative_str.startswith(dir_pattern + "/") or relative_str == dir_pattern

    # Handle glob patterns
    if fnmatch.fnmatch(file_path.name, pattern):
        return True

    # Handle relative path patterns
    if fnmatch.fnmatch(relative_str, pattern):
        return True

    return False


def _get_file_category(file_path: Path, base_path: Path) -> str | None:
    """Determine the category of a file based on patterns.

    Args:
        file_path: Path to the file
        base_path: Base path for relative matching

    Returns:
        Category name or None if no match
    """
    for category, patterns in RECOGNIZED_PATTERNS.items():
        for pattern in patterns:
            if _match_pattern(file_path, pattern, base_path):
                return category
    return None


def _is_orchestrator_file(file_path: Path, project_root: Path) -> bool:
    """Check if a file is part of the orchestrator structure.

    Args:
        file_path: Path to the file
        project_root: Project root directory

    Returns:
        True if the file is part of orchestrator structure
    """
    relative_path = file_path.relative_to(project_root)
    parts = relative_path.parts

    if not parts:
        return False

    # Check if any parent directory is an orchestrator directory
    first_dir = parts[0]

    # Skip hidden directories (except .autoresearch)
    if first_dir.startswith(".") and first_dir != ".autoresearch":
        return True  # Skip these files entirely

    # Check if it's in an orchestrator directory
    if first_dir in ORCHESTRATOR_DIRS:
        return True

    return False


def analyze_directory_contents(project_root: Path) -> DirectoryAnalysis:
    """Analyze the contents of a project directory.

    Examines all files in the directory and categorizes them based on
    recognized patterns. Identifies files that don't fit the standard
    research project structure.

    Args:
        project_root: Path to the project root directory

    Returns:
        DirectoryAnalysis with categorization results

    Raises:
        LegacyHandlerError: If the directory cannot be analyzed
    """
    if not project_root.exists():
        raise LegacyHandlerError(
            f"Project root does not exist: {project_root}",
            path=str(project_root),
            operation="analyze",
        )

    if not project_root.is_dir():
        raise LegacyHandlerError(
            f"Project root is not a directory: {project_root}",
            path=str(project_root),
            operation="analyze",
        )

    recognized: dict[str, list[str]] = {cat: [] for cat in RECOGNIZED_PATTERNS}
    orphans: list[str] = []
    total_files = 0
    recommended: list[dict[str, Any]] = []

    # Iterate through all files
    for item in project_root.rglob("*"):
        if not item.is_file():
            continue

        # Skip hidden directories and common exclusions
        relative = item.relative_to(project_root)
        if any(part.startswith(".") and part != ".autoresearch" for part in relative.parts):
            continue
        if "node_modules" in relative.parts or "__pycache__" in relative.parts:
            continue

        total_files += 1

        # Skip orchestrator files
        if _is_orchestrator_file(item, project_root):
            continue

        # Categorize the file
        category = _get_file_category(item, project_root)

        relative_str = str(relative)
        if category:
            recognized[category].append(relative_str)
        else:
            orphans.append(relative_str)

    # Filter out empty categories
    recognized = {k: v for k, v in recognized.items() if v}

    # Generate recommendations
    if orphans:
        recommended.append(
            {
                "action": "migrate",
                "reason": f"Found {len(orphans)} files not matching standard patterns",
                "files": orphans[:10],  # Show first 10
                "total": len(orphans),
            }
        )

    # Check for potential conflicts
    for category, files in recognized.items():
        if len(files) > 10:
            recommended.append(
                {
                    "action": "review",
                    "reason": f"Large number of {category} files may need organization",
                    "count": len(files),
                    "category": category,
                }
            )

    return DirectoryAnalysis(
        is_empty=total_files == 0,
        total_files=total_files,
        recognized_patterns=recognized,
        orphan_files=orphans,
        recommended_actions=recommended,
    )


def create_legacy_backup(project_root: Path, files: list[str]) -> Path:
    """Create a legacy backup directory and move files there.

    Creates a timestamped directory under .autoresearch/legacy/ and
    moves the specified files there for safekeeping.

    Args:
        project_root: Path to the project root directory
        files: List of relative file paths to migrate

    Returns:
        Path to the created legacy backup directory

    Raises:
        LegacyHandlerError: If backup creation fails
    """
    if not files:
        raise LegacyHandlerError(
            "No files provided for backup",
            path=str(project_root),
            operation="backup",
        )

    # Create legacy directory structure
    legacy_base = project_root / ".autoresearch" / "legacy"
    legacy_base.mkdir(parents=True, exist_ok=True)

    # Create timestamped subdirectory
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    legacy_path = legacy_base / timestamp
    legacy_path.mkdir(parents=True, exist_ok=True)

    migrated_count = 0
    errors: list[tuple[str, str]] = []

    for relative_file in files:
        src_path = project_root / relative_file

        if not src_path.exists():
            errors.append((relative_file, "Source file not found"))
            continue

        dst_path = legacy_path / relative_file

        try:
            # Create parent directories
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(src_path), str(dst_path))
            migrated_count += 1

        except Exception as e:
            errors.append((relative_file, str(e)))

    # Create manifest file
    manifest = {
        "timestamp": timestamp,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "migrated_count": migrated_count,
        "errors": [{"file": f, "error": e} for f, e in errors],
    }

    manifest_path = legacy_path / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    if errors and migrated_count == 0:
        raise LegacyHandlerError(
            f"Failed to migrate any files. Errors: {errors}",
            path=str(legacy_path),
            operation="backup",
        )

    return legacy_path


def extract_valuable_content(legacy_path: Path) -> dict[str, Any]:
    """Extract useful information from legacy files.

    Analyzes files in the legacy backup to extract potentially useful
    information such as paper titles, references, key terms, etc.

    Args:
        legacy_path: Path to the legacy backup directory

    Returns:
        Dictionary containing extracted content:
        - paper_titles: List of detected paper titles
        - references: List of detected references/citations
        - key_terms: List of important terms found
        - code_modules: List of detected code modules
        - data_files: List of data files with descriptions

    Raises:
        LegacyHandlerError: If extraction fails
    """
    if not legacy_path.exists():
        raise LegacyHandlerError(
            f"Legacy path does not exist: {legacy_path}",
            path=str(legacy_path),
            operation="extract",
        )

    extracted: dict[str, Any] = {
        "paper_titles": [],
        "references": [],
        "key_terms": [],
        "code_modules": [],
        "data_files": [],
        "metadata": {
            "extraction_time": datetime.now(timezone.utc).isoformat(),
            "files_analyzed": 0,
        },
    }

    # Patterns for extraction
    title_patterns = [
        r"^#\s+(.+)$",  # Markdown H1
        r"\\title\{(.+?)\}",  # LaTeX title
        r"title\s*=\s*['\"](.+?)['\"]",  # YAML/frontmatter title
    ]

    reference_patterns = [
        r"@(\w+)\{",  # BibTeX citation key
        r"\\cite\{(.+?)\}",  # LaTeX citation
        r"\[(.+?)\]\(.+?\.pdf\)",  # Markdown link to PDF
    ]

    files_analyzed = 0

    for file_path in legacy_path.rglob("*"):
        if not file_path.is_file():
            continue

        # Skip manifest
        if file_path.name == "manifest.json":
            continue

        files_analyzed += 1
        suffix = file_path.suffix.lower()
        relative = file_path.relative_to(legacy_path)

        try:
            if suffix in {".md", ".txt", ".tex", ".bib"}:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                # Extract titles
                for pattern in title_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    extracted["paper_titles"].extend(matches[:3])

                # Extract references
                if suffix == ".bib":
                    bib_keys = re.findall(r"@(\w+)\{([^,]+)", content)
                    extracted["references"].extend([key for _, key in bib_keys])
                else:
                    for pattern in reference_patterns:
                        matches = re.findall(pattern, content)
                        extracted["references"].extend(matches)

                # Extract key terms (simplified)
                words = re.findall(r"\b[A-Z][a-z]{3,}\b", content)
                word_freq: dict[str, int] = {}
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
                top_terms = sorted(word_freq.items(), key=lambda x: -x[1])[:10]
                extracted["key_terms"].extend([term for term, _ in top_terms])

            elif suffix in {".py", ".ipynb"}:
                # Extract module/class names
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                classes = re.findall(r"class\s+(\w+)", content)
                functions = re.findall(r"def\s+(\w+)", content)
                extracted["code_modules"].append(
                    {
                        "file": str(relative),
                        "classes": classes[:5],
                        "functions": functions[:10],
                    }
                )

            elif suffix in {".csv", ".json", ".pkl", ".pt", ".pth"}:
                # Record data files
                extracted["data_files"].append(
                    {
                        "file": str(relative),
                        "type": suffix[1:],
                        "size": file_path.stat().st_size,
                    }
                )

        except Exception:
            # Skip files that can't be read
            continue

    # Deduplicate and limit results
    extracted["paper_titles"] = list(set(extracted["paper_titles"]))[:20]
    extracted["references"] = list(set(extracted["references"]))[:50]
    extracted["key_terms"] = list(set(extracted["key_terms"]))[:30]
    extracted["metadata"]["files_analyzed"] = files_analyzed

    return extracted


def generate_migration_report(
    analysis: DirectoryAnalysis,
    result: MigrationResult,
) -> str:
    """Generate a human-readable migration report.

    Creates a detailed report of the directory analysis and migration
    results, suitable for display to the user.

    Args:
        analysis: DirectoryAnalysis from analyze_directory_contents
        result: MigrationResult from handle_non_empty_directory

    Returns:
        Formatted report string
    """
    lines = [
        "# Directory Migration Report",
        "",
        f"**Generated**: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Files Analyzed**: {analysis.total_files}")
    lines.append(f"- **Orphan Files**: {len(analysis.orphan_files)}")
    lines.append(f"- **Migration Status**: {'Success' if result.success else 'Failed'}")
    lines.append("")

    # Recognized Patterns
    if analysis.recognized_patterns:
        lines.append("## Recognized File Patterns")
        lines.append("")
        for category, files in sorted(analysis.recognized_patterns.items()):
            lines.append(f"- **{category}**: {len(files)} files")
            for f in files[:3]:
                lines.append(f"  - `{f}`")
            if len(files) > 3:
                lines.append(f"  - ... and {len(files) - 3} more")
        lines.append("")

    # Orphan Files
    if analysis.orphan_files:
        lines.append("## Orphan Files (Migrated)")
        lines.append("")
        for f in analysis.orphan_files[:10]:
            lines.append(f"- `{f}`")
        if len(analysis.orphan_files) > 10:
            lines.append(f"- ... and {len(analysis.orphan_files) - 10} more")
        lines.append("")

    # Legacy Backup Location
    if result.legacy_path:
        lines.append("## Legacy Backup")
        lines.append("")
        lines.append(f"- **Location**: `{result.legacy_path}`")
        lines.append(f"- **Files Migrated**: {len(result.migrated_files)}")
        lines.append("")

    # Extracted Content
    if result.extracted_content:
        content = result.extracted_content
        lines.append("## Extracted Content")
        lines.append("")

        if content.get("paper_titles"):
            lines.append("**Potential Paper Titles**:")
            for title in content["paper_titles"][:5]:
                lines.append(f"- {title}")
            lines.append("")

        if content.get("references"):
            lines.append(f"**References Found**: {len(content['references'])} citations")
            lines.append("")

        if content.get("code_modules"):
            lines.append("**Code Modules**:")
            for module in content["code_modules"][:5]:
                lines.append(
                    f"- `{module['file']}`: {len(module['classes'])} classes, {len(module['functions'])} functions"
                )
            lines.append("")

        if content.get("data_files"):
            lines.append("**Data Files**:")
            for df in content["data_files"][:5]:
                size_kb = df["size"] / 1024
                lines.append(f"- `{df['file']}` ({df['type']}, {size_kb:.1f} KB)")
            lines.append("")

    # Recommendations
    if analysis.recommended_actions:
        lines.append("## Recommendations")
        lines.append("")
        for rec in analysis.recommended_actions:
            lines.append(f"- **{rec['action'].title()}**: {rec['reason']}")
        lines.append("")

    return "\n".join(lines)


def handle_non_empty_directory(
    project_root: Path,
    mode: str,
    files_to_migrate: list[str] | None = None,
) -> MigrationResult:
    """Handle a non-empty directory during project initialization.

    This is the main entry point for handling existing files in a
    project directory. It supports three modes:
    - "migrate": Move non-conforming files to legacy backup
    - "preserve": Keep files in place, just analyze
    - "cancel": Return empty result

    Args:
        project_root: Path to the project root directory
        mode: Handling mode ("migrate", "preserve", or "cancel")
        files_to_migrate: Optional list of specific files to migrate
                         (if None, uses orphan files from analysis)

    Returns:
        MigrationResult with operation outcome

    Raises:
        ValidationError: If an invalid mode is specified
        LegacyHandlerError: If migration fails
    """
    valid_modes = {"migrate", "preserve", "cancel"}
    if mode not in valid_modes:
        raise ValidationError(
            f"Invalid mode: {mode}. Must be one of: {valid_modes}",
            errors=[f"Invalid mode: {mode}"],
        )

    # Analyze the directory
    analysis = analyze_directory_contents(project_root)

    # Handle cancel mode
    if mode == "cancel":
        return MigrationResult(
            success=True,
            legacy_path=None,
            migrated_files=[],
            extracted_content={},
            report="Operation cancelled by user. No changes made.",
        )

    # Handle preserve mode
    if mode == "preserve":
        report = generate_migration_report(
            analysis,
            MigrationResult(success=True),
        )
        return MigrationResult(
            success=True,
            legacy_path=None,
            migrated_files=[],
            extracted_content={},
            report=f"Files preserved in place.\n\n{report}",
        )

    # Handle migrate mode
    files = files_to_migrate if files_to_migrate is not None else analysis.orphan_files

    if not files:
        report = generate_migration_report(
            analysis,
            MigrationResult(success=True),
        )
        return MigrationResult(
            success=True,
            legacy_path=None,
            migrated_files=[],
            extracted_content={},
            report="No files need migration.\n\n" + report,
        )

    try:
        # Create legacy backup
        legacy_path = create_legacy_backup(project_root, files)

        # Extract valuable content
        extracted = extract_valuable_content(legacy_path)

        # Generate report
        result = MigrationResult(
            success=True,
            legacy_path=str(legacy_path),
            migrated_files=files,
            extracted_content=extracted,
        )
        result.report = generate_migration_report(analysis, result)

        return result

    except Exception as e:
        return MigrationResult(
            success=False,
            legacy_path=None,
            migrated_files=[],
            extracted_content={},
            report=f"Migration failed: {e}",
        )


def format_analysis_summary(analysis: DirectoryAnalysis) -> str:
    """Format a brief analysis summary for user display.

    Args:
        analysis: DirectoryAnalysis from analyze_directory_contents

    Returns:
        Brief summary string suitable for interactive display
    """
    if analysis.is_empty:
        return "Directory is empty."

    lines = [
        f"Found {analysis.total_files} files in directory.",
        "",
    ]

    if analysis.recognized_patterns:
        lines.append("Recognized patterns:")
        for category, files in sorted(analysis.recognized_patterns.items()):
            lines.append(f"  - {category}: {len(files)} files")
        lines.append("")

    if analysis.orphan_files:
        lines.append(f"Orphan files (not matching standard patterns): {len(analysis.orphan_files)}")
        for f in analysis.orphan_files[:5]:
            lines.append(f"  - {f}")
        if len(analysis.orphan_files) > 5:
            lines.append(f"  - ... and {len(analysis.orphan_files) - 5} more")

    return "\n".join(lines)


def main() -> int:
    """Main entry point for the legacy handler script.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Handle legacy files in non-empty project directories."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to project root directory",
    )
    parser.add_argument(
        "--mode",
        choices=["migrate", "preserve", "cancel", "analyze"],
        default="analyze",
        help="Handling mode (default: analyze)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output essential information",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    try:
        if args.mode == "analyze":
            analysis = analyze_directory_contents(project_root)

            if args.json:
                result = {
                    "is_empty": analysis.is_empty,
                    "total_files": analysis.total_files,
                    "recognized_patterns": analysis.recognized_patterns,
                    "orphan_files": analysis.orphan_files,
                    "recommended_actions": analysis.recommended_actions,
                }
                print(json.dumps(result, indent=2))
            elif args.quiet:
                print(f"{analysis.total_files} files, {len(analysis.orphan_files)} orphans")
            else:
                print(format_analysis_summary(analysis))

        else:
            result = handle_non_empty_directory(project_root, args.mode)

            if args.json:
                print(
                    json.dumps(
                        {
                            "success": result.success,
                            "legacy_path": result.legacy_path,
                            "migrated_files": result.migrated_files,
                            "extracted_content": result.extracted_content,
                        },
                        indent=2,
                        default=str,
                    )
                )
            elif args.quiet:
                print("success" if result.success else "failed")
            else:
                print(result.report)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
