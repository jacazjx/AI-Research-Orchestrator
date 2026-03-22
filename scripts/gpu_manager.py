"""
GPU registry management for AI Research Orchestrator.

This module provides functions to manage GPU devices across local and
remote systems. The registry is stored in ~/.autoresearch/gpu-registry.yaml.

Features:
- Discover local GPUs using nvidia-smi
- Probe remote GPUs via SSH
- Register/unregister GPUs
- Allocate/release GPUs
"""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from exceptions import ConfigurationError

logger = logging.getLogger(__name__)

REGISTRY_VERSION = "1.0.0"
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_TIMEOUT = 30


class GPUDevice:
    def __init__(
        self,
        id: str,
        name: str = "Unknown GPU",
        type: str = "local",
        status: str = "available",
        memory_gb: float = 0.0,
        host: str | None = None,
        user: str | None = None,
        port: int = DEFAULT_SSH_PORT,
        allocated_to: str | None = None,
        total_hours: float = 0.0,
        last_used: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.status = status
        self.memory_gb = memory_gb
        self.host = host
        self.user = user
        self.port = port
        self.allocated_to = allocated_to
        self.total_hours = total_hours
        self.last_used = last_used

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "memory_gb": self.memory_gb,
            "total_hours": self.total_hours,
        }
        if self.last_used is not None:
            result["last_used"] = self.last_used
        if self.type == "ssh":
            result["host"] = self.host
            result["user"] = self.user
            result["port"] = self.port
        if self.allocated_to is not None:
            result["allocated_to"] = self.allocated_to
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GPUDevice:
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown GPU"),
            type=data.get("type", "local"),
            status=data.get("status", "available"),
            memory_gb=float(data.get("memory_gb", 0)),
            host=data.get("host"),
            user=data.get("user"),
            port=int(data.get("port", DEFAULT_SSH_PORT)),
            allocated_to=data.get("allocated_to"),
            total_hours=float(data.get("total_hours", 0)),
            last_used=data.get("last_used"),
        )

    def is_available(self) -> bool:
        return self.status == "available" and self.allocated_to is None

    def is_remote(self) -> bool:
        return self.type == "ssh"


class GPURegistry:
    def __init__(
        self,
        devices: list[GPUDevice] | None = None,
        version: str = REGISTRY_VERSION,
    ) -> None:
        self.devices = devices or []
        self.version = version

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "devices": [d.to_dict() for d in self.devices],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GPURegistry:
        devices = [GPUDevice.from_dict(d) for d in data.get("devices", [])]
        return cls(devices=devices, version=data.get("version", REGISTRY_VERSION))


def get_gpu_registry_path() -> Path:
    from user_config import get_user_config_dir

    return get_user_config_dir() / "gpu-registry.yaml"


def get_default_gpu_registry() -> dict[str, Any]:
    return {"version": REGISTRY_VERSION, "devices": []}


def load_user_gpu_registry() -> dict[str, Any]:
    registry_path = get_gpu_registry_path()
    if not registry_path.exists():
        return {"version": REGISTRY_VERSION, "devices": []}
    try:
        with open(registry_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError) as exc:
        raise ConfigurationError(
            f"Failed to load GPU registry: {exc}", config_file=str(registry_path)
        ) from exc
    if "version" not in data:
        data["version"] = REGISTRY_VERSION
    if "devices" not in data:
        data["devices"] = []
    return data


def save_user_gpu_registry(registry: dict[str, Any]) -> None:
    registry_path = get_gpu_registry_path()
    if "version" not in registry:
        registry["version"] = REGISTRY_VERSION
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = registry_path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            yaml.dump(registry, f, default_flow_style=False, allow_unicode=True)
        tmp_path.replace(registry_path)
    except OSError as exc:
        if tmp_path.exists():
            tmp_path.unlink()
        raise ConfigurationError(
            f"Failed to save GPU registry: {exc}", config_file=str(registry_path)
        ) from exc


def discover_local_gpus() -> list[dict[str, Any]]:
    try:
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if completed.returncode != 0:
        return []
    gpus = []
    for line in completed.stdout.strip().splitlines():
        parts = line.split(", ")
        if len(parts) >= 3:
            try:
                gpus.append(
                    {
                        "id": f"local-{parts[0].strip()}",
                        "name": parts[1].strip(),
                        "memory_gb": float(parts[2].strip()) / 1024,
                        "type": "local",
                    }
                )
            except (ValueError, IndexError):
                continue
    return gpus


def probe_remote_gpu(host: str, user: str, port: int = DEFAULT_SSH_PORT) -> dict[str, Any] | None:
    cmd = [
        "ssh",
        "-o",
        f"ConnectTimeout={DEFAULT_SSH_TIMEOUT}",
        "-o",
        "StrictHostKeyChecking=no",
        "-p",
        str(port),
        f"{user}@{host}",
        "nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader,nounits 2>/dev/null | head -1",
    ]
    try:
        completed = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=False,
            timeout=DEFAULT_SSH_TIMEOUT + 10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0 or not completed.stdout.strip():
        return None
    parts = completed.stdout.strip().split(", ")
    if len(parts) >= 3:
        try:
            return {
                "id": f"remote-{host.replace('.', '-')}-{parts[0].strip()}",
                "name": parts[1].strip(),
                "memory_gb": float(parts[2].strip()) / 1024,
                "type": "ssh",
                "host": host,
                "user": user,
                "port": port,
            }
        except (ValueError, IndexError):
            return None
    return None


def register_gpu(device: GPUDevice) -> None:
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])
    for i, d in enumerate(devices):
        if isinstance(d, dict) and d.get("id") == device.id:
            devices[i] = device.to_dict()
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            return
    devices.append(device.to_dict())
    registry["devices"] = devices
    save_user_gpu_registry(registry)


def unregister_gpu(gpu_id: str) -> bool:
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])
    new_devices = [d for d in devices if not (isinstance(d, dict) and d.get("id") == gpu_id)]
    if len(new_devices) == len(devices):
        return False
    registry["devices"] = new_devices
    save_user_gpu_registry(registry)
    return True


def allocate_gpu(gpu_id: str, job_id: str) -> bool:
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])
    for d in devices:
        if isinstance(d, dict) and d.get("id") == gpu_id:
            if d.get("status") != "available" or d.get("allocated_to"):
                return False
            d["status"] = "busy"
            d["allocated_to"] = job_id
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            return True
    return False


def release_gpu(gpu_id: str) -> bool:
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])
    for d in devices:
        if isinstance(d, dict) and d.get("id") == gpu_id:
            d["status"] = "available"
            d["allocated_to"] = None
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            return True
    return False


def update_gpu_usage(gpu_id: str, hours: float) -> None:
    registry = load_user_gpu_registry()
    for d in registry.get("devices", []):
        if isinstance(d, dict) and d.get("id") == gpu_id:
            d["total_hours"] = d.get("total_hours", 0.0) + hours
            d["last_used"] = datetime.now(timezone.utc).isoformat()
            save_user_gpu_registry(registry)
            return
    raise ConfigurationError(
        f"GPU '{gpu_id}' not found in registry", config_file="gpu-registry.yaml"
    )


def select_best_gpu(criteria: dict[str, Any]) -> str | None:
    registry = load_user_gpu_registry()
    devices = [GPUDevice.from_dict(d) for d in registry.get("devices", [])]
    available = [d for d in devices if d.is_available()]

    exclude = criteria.get("exclude", [])
    available = [d for d in available if d.id not in exclude]

    min_memory = criteria.get("min_memory_gb")
    if min_memory is not None:
        available = [d for d in available if d.memory_gb >= min_memory]

    if not available:
        return None

    preference = criteria.get("preference")
    if preference:
        preferred = [d for d in available if d.type == preference]
        if preferred:
            available = preferred

    available.sort(key=lambda d: d.total_hours)
    return available[0].id


def list_available_gpus() -> list[GPUDevice]:
    registry = load_user_gpu_registry()
    devices = [GPUDevice.from_dict(d) for d in registry.get("devices", [])]
    return [d for d in devices if d.is_available()]


def refresh_gpu_registry(auto_discover: bool = True) -> dict[str, Any]:
    registry = load_user_gpu_registry()
    if auto_discover:
        local_gpus = discover_local_gpus()
        existing_local = {
            d["id"] for d in registry.get("devices", []) if d.get("type", "local") == "local"
        }
        for gpu in local_gpus:
            found = False
            for i, d in enumerate(registry.get("devices", [])):
                if d.get("id") == gpu["id"]:
                    d.update(gpu)
                    found = True
                    break
            if not found:
                registry.setdefault("devices", []).append(gpu)
    save_user_gpu_registry(registry)
    return registry
