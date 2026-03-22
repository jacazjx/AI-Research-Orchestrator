"""Global system evaluation registry for cross-project trend tracking."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from orchestrator_common import load_state

DEFAULT_REGISTRY_PATH = Path.home() / ".autoresearch" / "system-eval-history.yaml"

REQUIRED_DIMENSIONS = (
    "workflow_effectiveness",
    "agent_collaboration",
    "gate_accuracy",
    "template_effectiveness",
    "resource_efficiency",
    "user_experience",
)


def validate_scores(scores: dict[str, float]) -> None:
    """Validate scores contain all required dimensions with values 0-5.
    Raises ValueError if invalid."""
    for dim in REQUIRED_DIMENSIONS:
        if dim not in scores:
            raise ValueError(f"Missing required dimension: {dim}")
    for dim, val in scores.items():
        if not (0.0 <= val <= 5.0):
            raise ValueError(f"Score for {dim} must be 0-5, got {val}")


def _load_registry(registry_path: Path) -> list[dict[str, Any]]:
    """Load evaluations from registry file. Returns [] if not found or corrupt.
    If YAML is corrupt, backup to .yaml.bak before returning []."""
    if not registry_path.exists():
        return []
    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        backup = registry_path.with_suffix(".yaml.bak")
        shutil.copy2(registry_path, backup)
        return []
    if not isinstance(data, dict) or "evaluations" not in data:
        return []
    return data["evaluations"] or []


def _save_registry(registry_path: Path, evaluations: list[dict[str, Any]]) -> None:
    """Save evaluations to registry file. Creates parent dirs if needed."""
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    data = {"evaluations": evaluations}
    registry_path.write_text(
        yaml.dump(data, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )


def record_evaluation(
    project_root: Path,
    scores: dict[str, float],
    weighted_total: float,
    recommendation: str,
    top_issues: list[str],
    registry_path: Path | None = None,
) -> dict[str, Any]:
    """Record evaluation to global registry. Reads project_id and topic from state."""
    validate_scores(scores)
    registry_path = registry_path or DEFAULT_REGISTRY_PATH
    state = load_state(project_root)
    report_path = str(
        project_root / state["deliverables"].get(
            "system_evaluation_report",
            "docs/reflection/system-evaluation-report.md",
        )
    )
    entry = {
        "project_id": state.get("project_id", "unknown"),
        "topic": state.get("topic", "unknown"),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "scores": dict(scores),
        "weighted_total": weighted_total,
        "recommendation": recommendation,
        "top_issues": list(top_issues),
        "report_path": report_path,
    }
    evaluations = _load_registry(registry_path)
    evaluations.append(entry)
    _save_registry(registry_path, evaluations)
    return entry


def query_history(
    registry_path: Path | None = None,
    last: int | None = None,
    project_id: str | None = None,
) -> list[dict[str, Any]]:
    """Query evaluation history. Returns most-recent-first. Filters by last N and/or project_id."""
    registry_path = registry_path or DEFAULT_REGISTRY_PATH
    evaluations = _load_registry(registry_path)
    if project_id:
        evaluations = [e for e in evaluations if e.get("project_id") == project_id]
    evaluations.reverse()
    if last is not None:
        evaluations = evaluations[:last]
    return evaluations


def compute_trend(
    registry_path: Path | None = None,
    dimension: str | None = None,
    last: int | None = None,
) -> list[dict[str, Any]]:
    """Compute trend data. If dimension specified, returns {project_id, evaluated_at, value}.
    If dimension is None, returns {project_id, evaluated_at, scores, weighted_total}.
    Chronological order."""
    registry_path = registry_path or DEFAULT_REGISTRY_PATH
    evaluations = _load_registry(registry_path)
    if last is not None:
        evaluations = evaluations[-last:]
    trend = []
    for entry in evaluations:
        if dimension:
            trend.append({
                "project_id": entry.get("project_id"),
                "evaluated_at": entry.get("evaluated_at"),
                "value": entry["scores"].get(dimension, 0.0),
            })
        else:
            trend.append({
                "project_id": entry.get("project_id"),
                "evaluated_at": entry.get("evaluated_at"),
                "scores": entry["scores"],
                "weighted_total": entry.get("weighted_total", 0.0),
            })
    return trend


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the global system evaluation registry.")
    parser.add_argument("--action", required=True, choices=["record", "history", "trend"])
    parser.add_argument("--project-root", type=str)
    parser.add_argument("--scores", type=str, help="JSON string of dimension scores")
    parser.add_argument("--weighted-total", type=float)
    parser.add_argument("--recommendation", type=str)
    parser.add_argument("--top-issues", type=str, help="JSON array of issue strings")
    parser.add_argument("--last", type=int)
    parser.add_argument("--project-id", type=str)
    parser.add_argument("--dimension", type=str)
    parser.add_argument("--registry-path", type=str)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    registry_path = Path(args.registry_path) if args.registry_path else None
    if args.action == "record":
        if not args.project_root or not args.scores:
            parser.error("--project-root and --scores required for record action")
            return 2
        scores = json.loads(args.scores)
        top_issues = json.loads(args.top_issues) if args.top_issues else []
        record_evaluation(
            project_root=Path(args.project_root),
            scores=scores,
            weighted_total=args.weighted_total or 0.0,
            recommendation=args.recommendation or "",
            top_issues=top_issues,
            registry_path=registry_path,
        )
        return 0
    elif args.action == "history":
        history = query_history(
            registry_path=registry_path,
            last=args.last,
            project_id=args.project_id,
        )
        print(json.dumps(history, ensure_ascii=False, indent=2))
        return 0
    elif args.action == "trend":
        trend = compute_trend(
            registry_path=registry_path,
            dimension=args.dimension,
            last=args.last,
        )
        print(json.dumps(trend, ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
