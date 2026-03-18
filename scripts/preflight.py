#!/usr/bin/env python3
"""Environment preflight checks for AI Research Orchestrator.

Checks for LaTeX, Semantic Scholar API reachability, and GPU availability.
All checks are advisory — they never raise or block initialization.
"""
from __future__ import annotations

import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

_SS_PROBE_URL = (
    "https://api.semanticscholar.org/graph/v1/paper/search"
    "?query=transformer&limit=1&fields=paperId"
)


def check_latex_available() -> dict[str, Any]:
    """Check if pdflatex is on PATH."""
    try:
        result = subprocess.run(
            ["pdflatex", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.splitlines()[0] if result.stdout else "unknown"
            return {"available": True, "version": version, "message": ""}
        return {"available": False, "version": None,
                "message": f"pdflatex exited with code {result.returncode}"}
    except FileNotFoundError:
        return {"available": False, "version": None,
                "message": "pdflatex not found on PATH"}
    except subprocess.TimeoutExpired:
        return {"available": False, "version": None,
                "message": "pdflatex check timed out"}
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "version": None, "message": str(exc)}


def check_semantic_scholar_reachable(timeout: int = 5) -> dict[str, Any]:
    """Check if Semantic Scholar API is reachable."""
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(_SS_PROBE_URL, timeout=timeout) as resp:
            latency_ms = int((time.monotonic() - t0) * 1000)
            if resp.status == 200:
                return {"reachable": True, "latency_ms": latency_ms, "message": ""}
            return {"reachable": False, "latency_ms": latency_ms,
                    "message": f"HTTP {resp.status}"}
    except urllib.error.URLError as exc:
        return {"reachable": False, "latency_ms": None, "message": str(exc.reason)}
    except socket.timeout:
        return {"reachable": False, "latency_ms": None,
                "message": f"timed out after {timeout}s"}
    except Exception as exc:  # noqa: BLE001
        return {"reachable": False, "latency_ms": None, "message": str(exc)}


def check_gpu_available() -> dict[str, Any]:
    """Check if at least one NVIDIA GPU is accessible via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            names = [n.strip() for n in result.stdout.strip().splitlines() if n.strip()]
            return {"available": True, "gpu_count": len(names),
                    "gpu_names": names, "message": ""}
        return {"available": False, "gpu_count": 0, "gpu_names": [],
                "message": f"nvidia-smi exited with code {result.returncode}"}
    except FileNotFoundError:
        return {"available": False, "gpu_count": 0, "gpu_names": [],
                "message": "nvidia-smi not found on PATH"}
    except subprocess.TimeoutExpired:
        return {"available": False, "gpu_count": 0, "gpu_names": [],
                "message": "nvidia-smi check timed out"}
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "gpu_count": 0, "gpu_names": [], "message": str(exc)}


def run_preflight_checks(timeout: int = 5) -> dict[str, Any]:
    """Run all three preflight checks and return aggregated results."""
    latex = check_latex_available()
    ss = check_semantic_scholar_reachable(timeout=timeout)
    gpu = check_gpu_available()

    warnings: list[str] = []
    if not latex["available"]:
        warnings.append(
            f"pdflatex not found ({latex['message']}). "
            "Paper phase will fail without LaTeX. Install: apt install texlive-full"
        )
    if not ss["reachable"]:
        warnings.append(
            f"Semantic Scholar API unreachable ({ss['message']}). "
            "Survey phase literature search may fail."
        )
    if not gpu["available"]:
        warnings.append(
            f"No NVIDIA GPU detected ({gpu['message']}). "
            "Skip this warning if your research type is 'theory' or 'survey'."
        )

    return {
        "latex": latex,
        "semantic_scholar": ss,
        "gpu": gpu,
        "warnings": warnings,
    }


def format_preflight_warnings(results: dict[str, Any]) -> str:
    """Format warnings as a printable advisory block."""
    warnings = results.get("warnings", [])
    if not warnings:
        return ""
    lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║  ENVIRONMENT WARNINGS (advisory — initialization continues) ║",
        "╚══════════════════════════════════════════════════════════╝",
    ]
    for i, w in enumerate(warnings, 1):
        lines.append(f"  {i}. {w}")
    lines.append("")
    return "\n".join(lines)
