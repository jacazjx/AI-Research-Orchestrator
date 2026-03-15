#!/usr/bin/env python3
"""System audit script.

This script performs a comprehensive audit of the AI research orchestrator system
to determine if it is ready for delivery to research institutions.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))


def check_scripts_exist() -> dict[str, Any]:
    """Check that all required scripts exist."""
    required_scripts = [
        "orchestrator_common.py",
        "init_research_project.py",
        "render_agent_prompt.py",
        "quality_gate.py",
        "validate_handoff.py",
        "generate_dashboard.py",
        "generate_statusline.py",
        "run_citation_audit.py",
        "pivot_manager.py",
        "sentinel.py",
        "recover_stage.py",
        "apply_overlay.py",
        "materialize_templates.py",
        "verify_system.py",
        "analyze_project.py",
        "migrate_project.py",
        "show_version.py",
        "phase_handoff.py",
    ]

    results = {
        "category": "scripts",
        "passed": True,
        "checks": [],
    }

    for script in required_scripts:
        script_path = SCRIPT_DIR / script
        exists = script_path.exists()
        results["checks"].append(
            {
                "name": script,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False

    return results


def check_templates_exist() -> dict[str, Any]:
    """Check that all required templates exist."""
    template_root = SKILL_DIR / "assets" / "templates"

    required_templates = [
        "00-admin/idea-brief.md.tmpl",
        "00-admin/workspace-manifest.md.tmpl",
        "00-admin/orchestrator-config.yaml.tmpl",
        "00-admin/dashboard/progress.md.tmpl",
        "01-survey/research-readiness-report.md.tmpl",
        "01-survey/phase-scorecard.md.tmpl",
        "02-pilot-analysis/pilot-validation-report.md.tmpl",
        "02-pilot-analysis/phase-scorecard.md.tmpl",
        "03-full-experiments/evidence-package-index.md.tmpl",
        "03-full-experiments/phase-scorecard.md.tmpl",
        "04-paper/paper-draft.md.tmpl",
        "04-paper/citation-audit-report.md.tmpl",
        "04-paper/phase-scorecard.md.tmpl",
        "05-reflection-evolution/lessons-learned.md.tmpl",
        "05-reflection-evolution/phase-scorecard.md.tmpl",
    ]

    results = {
        "category": "templates",
        "passed": True,
        "checks": [],
    }

    for template in required_templates:
        template_path = template_root / template
        exists = template_path.exists()
        results["checks"].append(
            {
                "name": template,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False

    return results


def check_prompts_exist() -> dict[str, Any]:
    """Check that all required prompts exist."""
    prompt_root = SKILL_DIR / "assets" / "prompts"

    required_prompts = [
        "orchestrator.md.tmpl",
        "survey.md.tmpl",
        "critic.md.tmpl",
        "code.md.tmpl",
        "adviser.md.tmpl",
        "paper-writer.md.tmpl",
        "reviewer-editor.md.tmpl",
        "reflector.md.tmpl",
        "curator.md.tmpl",
        "system-auditor.md.tmpl",
        "project-takeover.md.tmpl",
    ]

    results = {
        "category": "prompts",
        "passed": True,
        "checks": [],
    }

    for prompt in required_prompts:
        prompt_path = prompt_root / prompt
        exists = prompt_path.exists()
        results["checks"].append(
            {
                "name": prompt,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False

    return results


def check_references_exist() -> dict[str, Any]:
    """Check that all required reference documents exist."""
    ref_root = SKILL_DIR / "references"

    required_refs = [
        "workflow-protocol.md",
        "system-architecture.md",
        "orchestrator-protocol.md",
        "role-protocols.md",
        "gate-rubrics.md",
        "deliverable-contracts.md",
        "evidence-rules.md",
        "citation-authenticity.md",
        "literature-verification.md",
        "experiment-integrity.md",
        "paper-quality-assurance.md",
        "phase-execution-details.md",
        "project-takeover-protocol.md",
    ]

    results = {
        "category": "references",
        "passed": True,
        "checks": [],
    }

    for ref in required_refs:
        ref_path = ref_root / ref
        exists = ref_path.exists()
        results["checks"].append(
            {
                "name": ref,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False

    return results


def check_quality_enforcement() -> dict[str, Any]:
    """Check that quality enforcement mechanisms are present."""
    results = {
        "category": "quality_enforcement",
        "passed": True,
        "checks": [],
    }

    # Check citation audit script
    citation_audit = SCRIPT_DIR / "run_citation_audit.py"
    results["checks"].append(
        {
            "name": "citation_audit_script",
            "exists": citation_audit.exists(),
            "status": "pass" if citation_audit.exists() else "fail",
        }
    )

    # Check quality gate script
    quality_gate = SCRIPT_DIR / "quality_gate.py"
    results["checks"].append(
        {
            "name": "quality_gate_script",
            "exists": quality_gate.exists(),
            "status": "pass" if quality_gate.exists() else "fail",
        }
    )

    # Check validate handoff script
    validate_handoff = SCRIPT_DIR / "validate_handoff.py"
    results["checks"].append(
        {
            "name": "validate_handoff_script",
            "exists": validate_handoff.exists(),
            "status": "pass" if validate_handoff.exists() else "fail",
        }
    )

    # Check for gate rubrics
    gate_rubrics = SKILL_DIR / "references" / "gate-rubrics.md"
    results["checks"].append(
        {
            "name": "gate_rubrics_doc",
            "exists": gate_rubrics.exists(),
            "status": "pass" if gate_rubrics.exists() else "fail",
        }
    )

    # Check for integrity protocols
    integrity_doc = SKILL_DIR / "references" / "experiment-integrity.md"
    results["checks"].append(
        {
            "name": "experiment_integrity_doc",
            "exists": integrity_doc.exists(),
            "status": "pass" if integrity_doc.exists() else "fail",
        }
    )

    for check in results["checks"]:
        if check["status"] == "fail":
            results["passed"] = False
            break

    return results


def check_human_gate_enforcement() -> dict[str, Any]:
    """Check that human gate enforcement is present."""
    results = {
        "category": "human_gates",
        "passed": True,
        "checks": [],
    }

    # Check for gate requirements in HANDOFF_REQUIREMENTS
    try:
        from orchestrator_common import HANDOFF_REQUIREMENTS

        gates_defined = len(HANDOFF_REQUIREMENTS) >= 5  # 5 gates minimum
        results["checks"].append(
            {
                "name": "gate_requirements_defined",
                "status": "pass" if gates_defined else "fail",
                "count": len(HANDOFF_REQUIREMENTS),
            }
        )

        # Check that each gate requires approval
        for gate_name, requirements in HANDOFF_REQUIREMENTS.items():
            approval_required = "approval_status" in str(requirements.get("statuses", []))
            results["checks"].append(
                {
                    "name": f"{gate_name}_approval_required",
                    "status": "pass" if approval_required else "warn",
                }
            )

    except Exception as e:
        results["checks"].append(
            {
                "name": "gate_requirements_check",
                "status": "fail",
                "error": str(e),
            }
        )
        results["passed"] = False

    for check in results["checks"]:
        if check["status"] == "fail":
            results["passed"] = False
            break

    return results


def check_test_coverage() -> dict[str, Any]:
    """Check test coverage by running tests."""
    import subprocess

    results = {
        "category": "tests",
        "passed": True,
        "checks": [],
    }

    # Run tests
    try:
        result = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "tests"],
            cwd=SKILL_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout + result.stderr

        # Parse test results
        if "OK" in output:
            results["checks"].append(
                {
                    "name": "all_tests_pass",
                    "status": "pass",
                    "output": "All tests passed",
                }
            )
        else:
            results["checks"].append(
                {
                    "name": "all_tests_pass",
                    "status": "fail",
                    "output": output[-500:] if len(output) > 500 else output,
                }
            )
            results["passed"] = False

        # Count tests
        import re

        match = re.search(r"Ran (\d+) tests", output)
        if match:
            test_count = int(match.group(1))
            results["checks"].append(
                {
                    "name": "test_count",
                    "status": "pass" if test_count >= 30 else "warn",
                    "count": test_count,
                }
            )

    except subprocess.TimeoutExpired:
        results["checks"].append(
            {
                "name": "all_tests_pass",
                "status": "fail",
                "error": "Tests timed out",
            }
        )
        results["passed"] = False
    except Exception as e:
        results["checks"].append(
            {
                "name": "all_tests_pass",
                "status": "fail",
                "error": str(e),
            }
        )
        results["passed"] = False

    return results


def run_audit() -> dict[str, Any]:
    """Run comprehensive system audit."""
    audit_time = datetime.now(timezone.utc).isoformat()

    results = {
        "audit_time": audit_time,
        "skill_dir": str(SKILL_DIR),
        "categories": [
            check_scripts_exist(),
            check_templates_exist(),
            check_prompts_exist(),
            check_references_exist(),
            check_quality_enforcement(),
            check_human_gate_enforcement(),
            check_test_coverage(),
        ],
    }

    # Calculate overall status
    all_passed = all(cat["passed"] for cat in results["categories"])
    results["overall_passed"] = all_passed

    # Determine delivery readiness
    critical_categories = ["scripts", "quality_enforcement", "human_gates", "tests"]
    critical_passed = all(
        cat["passed"] for cat in results["categories"] if cat["category"] in critical_categories
    )

    if all_passed:
        results["delivery_readiness"] = "READY"
    elif critical_passed:
        results["delivery_readiness"] = "CONDITIONALLY_READY"
    else:
        results["delivery_readiness"] = "NOT_READY"

    return results


def format_report(report: dict[str, Any]) -> str:
    """Format the audit report as human-readable text."""
    lines = [
        "# System Audit Report",
        "",
        f"**Audit Time**: {report['audit_time']}",
        f"**Skill Directory**: `{report['skill_dir']}`",
        f"**Delivery Readiness**: {report['delivery_readiness']}",
        "",
    ]

    # Overall status
    icon = "✅" if report["overall_passed"] else "❌"
    lines.append(f"**Overall Status**: {icon} {'PASS' if report['overall_passed'] else 'FAIL'}")
    lines.append("")

    # Category results
    for category in report["categories"]:
        icon = "✅" if category["passed"] else "❌"
        lines.append(f"## {icon} {category['category'].replace('_', ' ').title()}")
        lines.append("")

        for check in category["checks"]:
            status_icon = (
                "✅" if check["status"] == "pass" else "⚠️" if check["status"] == "warn" else "❌"
            )
            name = check["name"]
            lines.append(f"- {status_icon} {name}")
            if "error" in check:
                lines.append(f"  - Error: {check['error']}")
            if "count" in check:
                lines.append(f"  - Count: {check['count']}")

        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Delivery Readiness**: {report['delivery_readiness']}")
    lines.append("")

    if report["delivery_readiness"] == "READY":
        lines.append("The system meets all requirements for delivery to research institutions.")
    elif report["delivery_readiness"] == "CONDITIONALLY_READY":
        lines.append("The system meets critical requirements but has some non-critical issues.")
    else:
        lines.append("The system does not meet critical requirements for delivery.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the AI research orchestrator system")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output readiness status")
    args = parser.parse_args()

    report = run_audit()

    if args.json:
        print(json.dumps(report, indent=2, default=str))
    elif args.quiet:
        print(report["delivery_readiness"])
    else:
        print(format_report(report))

    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
