from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    append_state_log,
    ensure_project_structure,
    load_state,
    save_state,
)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CITATION_SCRIPTS_DIR = SCRIPT_DIR / "citation"


def _get_latex_citation_skill_path() -> Path | None:
    """Get the path to the latex-citation-curator skill.

    Priority:
    1. Internal citation scripts directory (scripts/citation/)
    2. LATEX_CITATION_SKILL environment variable
    3. Relative path from this skill (../latex-citation-curator)
    4. Common installation directories

    Returns:
        Path to the skill directory or None if not found.
    """
    # 1. Internal citation scripts (built-in)
    if (CITATION_SCRIPTS_DIR / "fetch_verified_bibtex.py").exists():
        return CITATION_SCRIPTS_DIR

    # 2. Environment variable
    env_path = os.environ.get("LATEX_CITATION_SKILL")
    if env_path:
        path = Path(env_path)
        if path.exists():
            return path

    # 3. Relative path (sibling skill)
    sibling_path = SKILL_DIR.parent / "latex-citation-curator"
    if sibling_path.exists():
        return sibling_path

    # 4. Common installation directories
    common_paths = [
        Path.home() / ".codex" / "skills" / "latex-citation-curator",
        Path.home() / ".claude" / "skills" / "latex-citation-curator",
        Path("/usr/local/share/skills/latex-citation-curator"),
    ]
    for common_path in common_paths:
        if common_path.exists():
            return common_path

    return None


TRUSTED_VERIFICATION_STATUSES = {"verified-doi", "trusted-bibtex-no-doi"}
TRUSTED_BIB_SOURCES = {"doi-content-negotiation", "dblp", "local-bib", "user-library"}


def run_citation_audit(
    project_root: Path,
    draft_path: str | None = None,
    claims: list[str] | None = None,
    existing_bib: str | None = None,
    append_bib: str | None = None,
    verify: bool = False,
    semantic_scholar_api_key: str = "",
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    draft_relative = draft_path or DEFAULT_DELIVERABLES["paper_draft"]
    draft_file = project_root / draft_relative
    report_path = project_root / DEFAULT_DELIVERABLES["citation_audit_report"]

    detected_claims = _extract_claims(draft_file)
    requested_claims = claims or []
    all_claims = _dedupe_preserve_order(
        requested_claims
        + [item["clean_claim"] for item in detected_claims if item.get("clean_claim")]
    )

    verification_results: list[dict[str, object]] = []
    if verify and all_claims:
        for claim in all_claims:
            verification_results.append(
                _verify_claim(
                    claim,
                    project_root=project_root,
                    existing_bib=existing_bib,
                    append_bib=append_bib,
                    semantic_scholar_api_key=semantic_scholar_api_key,
                )
            )

    bib_paths = _resolve_bib_files(project_root, existing_bib=existing_bib, append_bib=append_bib)
    citation_audit = _audit_existing_citations(draft_file, bib_paths)
    authenticity_status, blocking_issues = _determine_authenticity_status(
        detected_claims=detected_claims,
        all_claims=all_claims,
        verification_results=verification_results,
        citation_audit=citation_audit,
        verify=verify,
    )

    report_lines = [
        "# Citation Audit Report",
        "",
        f"- Project ID: `{state['project_id']}`",
        f"- Topic: {state['topic']}",
        f"- Language: `{state['language_policy']['process_docs']}`",
        f"- Status: `{authenticity_status}`",
        "",
        "## Scope",
        "",
        f"- Draft under audit: `{draft_relative}`",
        "- Citation curator integration: `latex-citation-curator`",
        f"- Audited BibTeX files: {_render_bib_scope(project_root, bib_paths)}",
        "",
        "## Gap scan",
        "",
        f"- Detected citation gaps: "
        f"{_render_counted_items(_render_detected_claims(detected_claims))}",
        f"- Claims queued for verification: " f"{_render_counted_items(all_claims)}",
        "",
        "## Authenticity checks",
        "",
        f"- DOI-verified citations: " f"{_render_counted_items(citation_audit['verified_keys'])}",
        f"- Trusted-source citations without DOI: "
        f"{_render_counted_items(citation_audit['trusted_no_doi_keys'])}",
        f"- Preprints that should be replaced by formal publications: "
        f"{_render_counted_items(citation_audit['preprint_keys'])}",
        f"- Citations that require manual second checking: "
        f"{_render_counted_items(citation_audit['manual_check_keys'])}",
        f"- Missing cited keys in available BibTeX: "
        f"{_render_counted_items(citation_audit['missing_keys'])}",
        "",
        "## Verification results",
        "",
    ]
    if verification_results:
        for item in verification_results:
            report_lines.append(f"### Claim: {item['claim']}")
            report_lines.append("")
            report_lines.append(f"- Status: `{item['status']}`")
            report_lines.append(f"- Output file: `{item['output_file']}`")
            if item["status"] != "verified":
                report_lines.append(f"- Error: {item['error']}")
            report_lines.append("")
    else:
        report_lines.append("- No online claim verification was run.")
        if all_claims:
            report_lines.append(
                "- Existing claims remain blocked until verification is run or manually resolved."
            )
        else:
            report_lines.append("- No citation-gap claims were queued for online verification.")
    report_lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- Citation authenticity status: `{authenticity_status}`",
            f"- Blocking issues: {_render_counted_items(blocking_issues)}",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    append_state_log(
        state,
        "human_decisions",
        {
            "type": "citation_audit",
            "draft": draft_relative,
            "verify": verify,
            "claims": len(all_claims),
            "audited_bib_files": len(bib_paths),
            "status": authenticity_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    state["progress"]["next_action"] = "review-citation-audit"
    save_state(project_root, state)
    return {
        "project_root": str(project_root),
        "report_path": DEFAULT_DELIVERABLES["citation_audit_report"],
        "detected_claims": len(detected_claims),
        "verified_claims": len(verification_results),
        "audited_citation_keys": len(citation_audit["audited_keys"]),
        "authenticity_status": authenticity_status,
        "blocking_issues": blocking_issues,
    }


def _extract_claims(draft_file: Path) -> list[dict[str, object]]:
    skill_path = _get_latex_citation_skill_path()
    if skill_path is None:
        return []
    # Check if scripts are directly in skill_path (internal) or in scripts/ subdirectory
    if (skill_path / "extract_citation_needs.py").exists():
        script = skill_path / "extract_citation_needs.py"
    else:
        script = skill_path / "scripts" / "extract_citation_needs.py"
    if not draft_file.exists() or not script.exists():
        return []
    try:
        completed = subprocess.run(
            ["python3", str(script), str(draft_file), "--json"],
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if completed.returncode != 0 or not completed.stdout.strip():
            return []
        return json.loads(completed.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return []


def _verify_claim(
    claim: str,
    *,
    project_root: Path,
    existing_bib: str | None,
    append_bib: str | None,
    semantic_scholar_api_key: str,
) -> dict[str, object]:
    skill_path = _get_latex_citation_skill_path()
    if skill_path is None:
        return {
            "claim": claim,
            "status": "failed",
            "output_file": "",
            "error": (
                "latex-citation-curator skill not found. "
                "Set LATEX_CITATION_SKILL environment variable."
            ),
        }

    # Check if scripts are directly in skill_path (internal) or in scripts/ subdirectory
    if (skill_path / "fetch_verified_bibtex.py").exists():
        script = skill_path / "fetch_verified_bibtex.py"
    else:
        script = skill_path / "scripts" / "fetch_verified_bibtex.py"
    if not script.exists():
        return {
            "claim": claim,
            "status": "failed",
            "output_file": "",
            "error": f"Script not found: {script}",
        }

    output_dir = project_root / "04-paper" / "citation-audit"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(claim)[:48]
    output_path = output_dir / f"{slug}.bib"
    command = ["python3", str(script), "--query", claim, "--write-bib", str(output_path)]
    if existing_bib:
        command.extend(["--existing-bib", existing_bib])
    if append_bib:
        command.extend(["--append-bib", append_bib])
    if semantic_scholar_api_key:
        command.extend(["--semantic-scholar-api-key", semantic_scholar_api_key])

    try:
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            cwd=project_root,
            timeout=120,
        )
        return {
            "claim": claim,
            "status": "verified" if completed.returncode == 0 else "failed",
            "output_file": output_path.relative_to(project_root).as_posix(),
            "error": completed.stderr.strip() if completed.returncode != 0 else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "claim": claim,
            "status": "failed",
            "output_file": (
                output_path.relative_to(project_root).as_posix() if output_path.exists() else ""
            ),
            "error": "Claim verification timed out after 120 seconds",
        }
    except OSError as exc:
        return {
            "claim": claim,
            "status": "failed",
            "output_file": "",
            "error": f"Execution error: {exc}",
        }


def _resolve_bib_files(
    project_root: Path, *, existing_bib: str | None, append_bib: str | None
) -> list[Path]:
    candidates: list[Path] = []
    for raw_path in (existing_bib, append_bib):
        if not raw_path:
            continue
        path = Path(raw_path)
        resolved = path if path.is_absolute() else (project_root / path)
        if resolved.exists() and resolved.suffix.lower() == ".bib":
            candidates.append(resolved.resolve())
    if candidates:
        return _dedupe_paths(candidates)

    paper_dir = project_root / "04-paper"
    discovered = sorted(paper_dir.rglob("*.bib")) if paper_dir.exists() else []
    return _dedupe_paths(path.resolve() for path in discovered)


def _audit_existing_citations(draft_file: Path, bib_paths: list[Path]) -> dict[str, list[str]]:
    citation_keys = (
        _extract_citation_keys(draft_file.read_text(encoding="utf-8"))
        if draft_file.exists()
        else []
    )
    entries = _load_bib_entries(bib_paths)
    keys_to_audit = citation_keys or list(entries.keys())

    verified_keys: list[str] = []
    trusted_no_doi_keys: list[str] = []
    preprint_keys: list[str] = []
    manual_check_keys: list[str] = []
    missing_keys: list[str] = []

    for key in keys_to_audit:
        entry = entries.get(key)
        if entry is None:
            missing_keys.append(key)
            continue

        verification_status = entry.get("verification_status", "")
        has_doi = bool(entry.get("doi"))
        trusted_source = entry.get("bib_source", "") in TRUSTED_BIB_SOURCES
        manual_check_required = entry.get("manual_check_required", False)
        preprint = entry.get("is_preprint", False)

        if preprint:
            preprint_keys.append(key)
        if manual_check_required:
            manual_check_keys.append(key)
            continue
        if has_doi or verification_status == "verified-doi":
            verified_keys.append(key)
            continue
        if verification_status == "trusted-bibtex-no-doi" or trusted_source:
            trusted_no_doi_keys.append(key)
            continue
        manual_check_keys.append(key)

    return {
        "audited_keys": keys_to_audit,
        "verified_keys": verified_keys,
        "trusted_no_doi_keys": trusted_no_doi_keys,
        "preprint_keys": preprint_keys,
        "manual_check_keys": manual_check_keys,
        "missing_keys": missing_keys,
    }


def _extract_citation_keys(text: str) -> list[str]:
    keys: list[str] = []
    for raw_group in re.findall(r"\\cite[a-zA-Z*]*\{([^}]+)\}", text):
        for item in raw_group.split(","):
            candidate = item.strip()
            if candidate:
                keys.append(candidate)
    for key in re.findall(r"@([A-Za-z0-9:._/-]+)", text):
        keys.append(key.strip())
    return _dedupe_preserve_order(keys)


def _load_bib_entries(paths: list[Path]) -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for entry in _split_bibtex_entries(text):
            key = _bibtex_entry_key(entry)
            if not key:
                continue
            doi = _bibtex_field_value(entry, "doi")
            verification_status = _bibtex_field_value(entry, "x-verification-status").lower()
            bib_source = _bibtex_field_value(entry, "x-bib-source").lower()
            journal = _bibtex_field_value(entry, "journal")
            booktitle = _bibtex_field_value(entry, "booktitle")
            archive_prefix = _bibtex_field_value(entry, "archiveprefix").lower()
            eprint = _bibtex_field_value(entry, "eprint")
            url = _bibtex_field_value(entry, "url").lower()
            ee = _bibtex_field_value(entry, "ee").lower()
            manual_check = _bibtex_field_value(entry, "x-secondary-check-required").lower() in {
                "1",
                "true",
                "yes",
            }
            is_preprint = bool(
                archive_prefix == "arxiv" or eprint or "arxiv.org" in url or "arxiv.org" in ee
            ) and not (journal or booktitle)
            entries[key] = {
                "doi": doi,
                "verification_status": verification_status,
                "bib_source": bib_source,
                "manual_check_required": manual_check,
                "is_preprint": is_preprint,
            }
    return entries


def _split_bibtex_entries(text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?m)^@\w+\s*\{", text)]
    if not starts:
        return []
    starts.append(len(text))
    entries: list[str] = []
    for index in range(len(starts) - 1):
        candidate = text[starts[index] : starts[index + 1]].strip()
        if candidate:
            entries.append(candidate)
    return entries


def _bibtex_entry_key(entry: str) -> str:
    match = re.search(r"@\w+\s*\{\s*([^,\s]+)", entry)
    return match.group(1).strip() if match else ""


def _bibtex_field_value(entry: str, field: str) -> str:
    for pattern in (
        rf"(?im)^\s*{re.escape(field)}\s*=\s*\{{([^}}]+)\}}\s*,?",
        rf'(?im)^\s*{re.escape(field)}\s*=\s*"([^"]+)"\s*,?',
        rf"(?im)^\s*{re.escape(field)}\s*=\s*([^,\n]+)\s*,?",
    ):
        match = re.search(pattern, entry)
        if match:
            return match.group(1).strip()
    return ""


def _determine_authenticity_status(
    *,
    detected_claims: list[dict[str, object]],
    all_claims: list[str],
    verification_results: list[dict[str, object]],
    citation_audit: dict[str, list[str]],
    verify: bool,
) -> tuple[str, list[str]]:
    blocking_issues: list[str] = []

    if all_claims and not verify:
        blocking_issues.append("citation-gaps-detected-but-not-verified")
    if any(item["status"] != "verified" for item in verification_results):
        blocking_issues.append("claim-verification-failed")
    if citation_audit["missing_keys"]:
        blocking_issues.append("missing-bibtex-entries-for-cited-keys")
    if citation_audit["preprint_keys"]:
        blocking_issues.append("preprints-need-formal-publication-replacement")
    if citation_audit["manual_check_keys"]:
        blocking_issues.append("citations-require-manual-second-check")
    if not all_claims and not citation_audit["audited_keys"]:
        blocking_issues.append("no-citations-audited")

    if blocking_issues:
        return "revise", blocking_issues
    if verify and (all_claims or citation_audit["audited_keys"]):
        return "verified", []
    return "approved", []


def _render_detected_claims(items: list[dict[str, object]]) -> list[str]:
    rendered: list[str] = []
    for item in items:
        clean_claim = str(item.get("clean_claim", "") or "").strip()
        rendered.append(clean_claim or str(item.get("text", "") or "").strip())
    return [item for item in rendered if item]


def _render_bib_scope(project_root: Path, bib_paths: list[Path]) -> str:
    if not bib_paths:
        return "`none`"
    rendered = []
    for path in bib_paths:
        try:
            rendered.append(f"`{path.relative_to(project_root).as_posix()}`")
        except ValueError:
            rendered.append(f"`{path}`")
    return ", ".join(rendered)


def _render_counted_items(items: list[str]) -> str:
    if not items:
        return "`none`"
    return ", ".join(f"`{item}`" for item in items)


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _dedupe_paths(paths) -> list[Path]:
    seen: set[str] = set()
    deduped: list[Path] = []
    for path in paths:
        normalized = str(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(Path(normalized))
    return deduped


def _slugify(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-") or "citation"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a paper-phase citation authenticity audit.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--draft-path")
    parser.add_argument("--claim", action="append", dest="claims")
    parser.add_argument("--existing-bib")
    parser.add_argument("--append-bib")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--semantic-scholar-api-key", default="")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = run_citation_audit(
        project_root,
        draft_path=args.draft_path,
        claims=args.claims,
        existing_bib=args.existing_bib,
        append_bib=args.append_bib,
        verify=args.verify,
        semantic_scholar_api_key=args.semantic_scholar_api_key,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
