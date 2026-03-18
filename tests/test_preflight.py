#!/usr/bin/env python3
"""Tests for preflight.py module."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from preflight import (
    check_gpu_available,
    check_latex_available,
    check_semantic_scholar_reachable,
    format_preflight_warnings,
    run_preflight_checks,
)


class TestCheckLatexAvailable:
    def test_latex_found(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "pdfTeX 3.14"
        with patch("subprocess.run", return_value=mock_result):
            result = check_latex_available()
        assert result["available"] is True
        assert result["version"] is not None

    def test_latex_not_found(self) -> None:
        with patch("subprocess.run", side_effect=FileNotFoundError("pdflatex not found")):
            result = check_latex_available()
        assert result["available"] is False
        assert "message" in result

    def test_latex_timeout(self) -> None:
        import subprocess

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pdflatex", 10)):
            result = check_latex_available()
        assert result["available"] is False


class TestCheckSemanticScholarReachable:
    def test_reachable(self) -> None:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock_response):
            result = check_semantic_scholar_reachable(timeout=5)
        assert result["reachable"] is True
        assert result["latency_ms"] >= 0

    def test_unreachable(self) -> None:
        import urllib.error

        with patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("Network unreachable")
        ):
            result = check_semantic_scholar_reachable(timeout=5)
        assert result["reachable"] is False
        assert "message" in result

    def test_timeout(self) -> None:
        import socket

        with patch("urllib.request.urlopen", side_effect=socket.timeout("timed out")):
            result = check_semantic_scholar_reachable(timeout=1)
        assert result["reachable"] is False


class TestCheckGpuAvailable:
    def test_gpu_found(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "NVIDIA GeForce RTX 4090\nNVIDIA RTX 3090"
        with patch("subprocess.run", return_value=mock_result):
            result = check_gpu_available()
        assert result["available"] is True
        assert result["gpu_count"] == 2
        assert len(result["gpu_names"]) == 2

    def test_gpu_not_found(self) -> None:
        with patch("subprocess.run", side_effect=FileNotFoundError("nvidia-smi not found")):
            result = check_gpu_available()
        assert result["available"] is False
        assert result["gpu_count"] == 0

    def test_gpu_command_fails(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 6  # nvidia-smi error code
        mock_result.stdout = ""
        with patch("subprocess.run", return_value=mock_result):
            result = check_gpu_available()
        assert result["available"] is False


class TestRunPreflightChecks:
    def test_all_pass(self) -> None:
        mock_latex = {"available": True, "version": "3.14", "message": ""}
        mock_ss = {"reachable": True, "latency_ms": 50, "message": ""}
        mock_gpu = {"available": True, "gpu_count": 1, "gpu_names": ["RTX 4090"], "message": ""}
        with (
            patch("preflight.check_latex_available", return_value=mock_latex),
            patch("preflight.check_semantic_scholar_reachable", return_value=mock_ss),
            patch("preflight.check_gpu_available", return_value=mock_gpu),
        ):
            result = run_preflight_checks()
        assert result["warnings"] == []

    def test_partial_miss_produces_warnings(self) -> None:
        mock_latex = {"available": False, "version": None, "message": "not found"}
        mock_ss = {"reachable": True, "latency_ms": 50, "message": ""}
        mock_gpu = {"available": False, "gpu_count": 0, "gpu_names": [], "message": ""}
        with (
            patch("preflight.check_latex_available", return_value=mock_latex),
            patch("preflight.check_semantic_scholar_reachable", return_value=mock_ss),
            patch("preflight.check_gpu_available", return_value=mock_gpu),
        ):
            result = run_preflight_checks()
        assert len(result["warnings"]) >= 1
        assert any("latex" in w.lower() or "pdflatex" in w.lower() for w in result["warnings"])


class TestFormatPreflightWarnings:
    def test_no_warnings(self) -> None:
        result = {"warnings": []}
        assert format_preflight_warnings(result) == ""

    def test_with_warnings(self) -> None:
        result = {"warnings": ["pdflatex not found", "GPU not available"]}
        text = format_preflight_warnings(result)
        assert "WARNING" in text or "warning" in text.lower()
        assert "pdflatex" in text


class TestVerifySystemIntegration:
    def test_run_all_checks_includes_preflight(self, tmp_path: Path) -> None:
        import init_research_project as INIT
        from verify_system import run_all_checks

        INIT.initialize_research_project(project_root=tmp_path, topic="Preflight test")
        report = run_all_checks(tmp_path)
        assert "preflight" in report
        assert "warnings" in report["preflight"]
