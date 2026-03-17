"""
GPU registry management for AI Research Orchestrator.

This module provides functions to manage GPU devices across local and
remote systems. The registry is stored in ~/.autoresearch/gpu-registry.yaml.

Features:
- Discover local GPUs using nvidia-smi
- Probe remote GPUs via SSH
- Track GPU usage statistics
- Select best GPU based on requirements
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from exceptions import ConfigurationError

# Configure module logger
logger = logging.getLogger(__name__)

# GPU registry version
REGISTRY_VERSION = "1.0.0"

# Default SSH port
DEFAULT_SSH_PORT = 22

# Default SSH timeout in seconds
DEFAULT_SSH_TIMEOUT = 30


class GPUDevice:
    """Represents a GPU device in the registry.

    Attributes:
        id: Unique identifier for the GPU (e.g., "local-0", "remote-server-1").
        name: Human-readable name (e.g., "NVIDIA RTX 4090").
        type: Device type ("local" or "ssh").
        status: Current status ("available", "busy", "offline", "error").
        memory_gb: Total GPU memory in GB.
        last_used: ISO timestamp of last usage (nullable).
        total_hours: Total hours of usage.
        host: SSH host for remote GPUs (nullable).
        user: SSH user for remote GPUs (nullable).
        port: SSH port for remote GPUs (default 22).
        allocated_to: Job ID this GPU is allocated to (nullable).
    """

    def __init__(
        self,
        id: str,
        name: str = "Unknown GPU",
        type: str = "local",
        status: str = "available",
        memory_gb: float = 0.0,
        last_used: str | None = None,
        total_hours: float = 0.0,
        host: str | None = None,
        user: str | None = None,
        port: int = DEFAULT_SSH_PORT,
        allocated_to: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.status = status
        self.memory_gb = memory_gb
        self.last_used = last_used
        self.total_hours = total_hours
        self.host = host
        self.user = user
        self.port = port
        self.allocated_to = allocated_to

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
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
        """Create from dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown GPU"),
            type=data.get("type", "local"),
            status=data.get("status", "available"),
            memory_gb=float(data.get("memory_gb", 0)),
            last_used=data.get("last_used"),
            total_hours=float(data.get("total_hours", 0)),
            host=data.get("host"),
            user=data.get("user"),
            port=int(data.get("port", DEFAULT_SSH_PORT)),
            allocated_to=data.get("allocated_to"),
        )

    def is_available(self) -> bool:
        """Check if GPU is available for allocation."""
        return self.status == "available" and self.allocated_to is None

    def is_remote(self) -> bool:
        """Check if this is a remote GPU."""
        return self.type == "ssh"


class GPURegistry:
    """GPU device registry.

    Attributes:
        version: Registry schema version.
        devices: List of registered GPU devices.
    """

    def __init__(
        self,
        version: str = REGISTRY_VERSION,
        devices: list[GPUDevice] | None = None,
    ) -> None:
        self.version = version
        self.devices = devices or []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "version": self.version,
            "devices": [d.to_dict() for d in self.devices],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GPURegistry:
        """Create from dictionary."""
        devices_data = data.get("devices", [])
        devices = [
            GPUDevice.from_dict(d) if isinstance(d, dict) else GPUDevice(id=str(d))
            for d in devices_data
        ]
        return cls(
            version=data.get("version", REGISTRY_VERSION),
            devices=devices,
        )


def get_gpu_registry_path() -> Path:
    """Get the GPU registry file path.

    Returns:
        Path to the GPU registry file (~/.autoresearch/gpu-registry.yaml).
    """
    from user_config import get_user_config_dir

    return get_user_config_dir() / "gpu-registry.yaml"


def get_default_gpu_registry() -> dict[str, Any]:
    """Get the default GPU registry template.

    Returns:
        Dictionary containing default registry structure.
    """
    return GPURegistry().to_dict()


def load_user_gpu_registry() -> dict[str, Any]:
    """Load GPU registry from disk.

    If the registry file does not exist, returns an empty registry.

    Returns:
        Dictionary containing GPU registry data.

    Raises:
        ConfigurationError: If the registry file exists but cannot be parsed.
    """
    registry_path = get_gpu_registry_path()

    if not registry_path.exists():
        logger.debug("GPU registry not found at %s, returning empty registry", registry_path)
        return get_default_gpu_registry()

    try:
        with open(registry_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Failed to parse GPU registry: {exc}",
            config_file=str(registry_path),
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to read GPU registry: {exc}",
            config_file=str(registry_path),
        ) from exc

    # Ensure version is set
    if "version" not in data:
        data["version"] = REGISTRY_VERSION
    if "devices" not in data:
        data["devices"] = []

    logger.debug(
        "Loaded GPU registry from %s with %d devices", registry_path, len(data.get("devices", []))
    )
    return data


def save_user_gpu_registry(registry: dict[str, Any]) -> None:
    """Save GPU registry to disk.

    Uses atomic write pattern to prevent corruption.

    Args:
        registry: Dictionary containing registry data to save.

    Raises:
        ConfigurationError: If the registry cannot be saved.
    """
    registry_path = get_gpu_registry_path()

    # Ensure version is set
    if "version" not in registry:
        registry["version"] = REGISTRY_VERSION

    # Ensure directory exists
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Atomic write: write to temp file, then replace
        fd, temp_path = tempfile.mkstemp(
            dir=registry_path.parent,
            prefix=registry_path.name + ".",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.dump(
                    registry, f, default_flow_style=False, allow_unicode=True, sort_keys=False
                )
            os.replace(temp_path, registry_path)
        except Exception:
            # Clean up temp file on error
            Path(temp_path).unlink(missing_ok=True)
            raise

        logger.info("Saved GPU registry to %s", registry_path)
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to save GPU registry: {exc}",
            config_file=str(registry_path),
        ) from exc


def discover_local_gpus() -> list[dict[str, Any]]:
    """Discover local GPUs using nvidia-smi.

    Runs nvidia-smi to detect available NVIDIA GPUs on the local system.
    Returns an empty list if nvidia-smi is not available or fails.

    Returns:
        List of dictionaries containing GPU information:
        - id: GPU identifier (e.g., "local-0")
        - name: GPU name (e.g., "NVIDIA RTX 4090")
        - type: Always "local"
        - status: "available" or "offline"
        - memory_gb: GPU memory in GB
    """
    devices: list[dict[str, Any]] = []

    try:
        # Query GPU index, name, and memory
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except FileNotFoundError:
        logger.debug("nvidia-smi not found, no local GPUs detected")
        return devices
    except subprocess.TimeoutExpired:
        logger.warning("nvidia-smi timed out")
        return devices

    if completed.returncode != 0:
        logger.debug("nvidia-smi returned non-zero exit code: %s", completed.returncode)
        return devices

    for line in completed.stdout.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue

        try:
            index = int(parts[0])
            name = parts[1] if len(parts) > 1 else f"GPU-{index}"

            # Parse memory (in MiB from nvidia-smi)
            memory_gb = 0.0
            if len(parts) > 2:
                try:
                    memory_mib = int(parts[2])
                    memory_gb = round(memory_mib / 1024, 1)
                except ValueError:
                    pass

            device = {
                "id": f"local-{index}",
                "name": name,
                "type": "local",
                "status": "available",
                "memory_gb": memory_gb,
            }
            devices.append(device)
            logger.debug("Discovered local GPU: %s (%s, %.1f GB)", device["id"], name, memory_gb)
        except (ValueError, IndexError) as e:
            logger.warning("Failed to parse nvidia-smi output line '%s': %s", line, e)
            continue

    return devices


def probe_remote_gpu(host: str, user: str, port: int = DEFAULT_SSH_PORT) -> dict[str, Any] | None:
    """Probe a remote GPU via SSH.

    Attempts to connect to a remote server and run nvidia-smi to
    discover available GPUs. Returns None if the connection fails
    or no GPUs are found.

    Args:
        host: SSH hostname or IP address.
        user: SSH username.
        port: SSH port number (default 22).

    Returns:
        Dictionary containing GPU information if successful, None otherwise.
        The dictionary includes:
        - id: GPU identifier (e.g., "remote-host-0")
        - name: GPU name
        - type: Always "ssh"
        - status: "available" or "offline"
        - host: SSH host
        - user: SSH user
        - port: SSH port
        - memory_gb: GPU memory in GB
    """
    # Build SSH command
    ssh_target = f"{user}@{host}" if user else host

    try:
        # Run nvidia-smi on remote host
        completed = subprocess.run(
            [
                "ssh",
                "-p",
                str(port),
                "-o",
                "ConnectTimeout=10",
                "-o",
                "BatchMode=yes",
                "-o",
                "StrictHostKeyChecking=accept-new",
                ssh_target,
                "nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader,nounits",
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=DEFAULT_SSH_TIMEOUT,
        )
    except FileNotFoundError:
        logger.debug("ssh command not found, cannot probe remote GPU")
        return None
    except subprocess.TimeoutExpired:
        logger.warning("SSH connection to %s timed out", host)
        return None

    if completed.returncode != 0:
        logger.debug(
            "SSH command to %s failed with exit code %d: %s",
            host,
            completed.returncode,
            completed.stderr.strip(),
        )
        return None

    # Parse output - take first GPU found
    lines = completed.stdout.strip().splitlines()
    if not lines:
        logger.debug("No GPUs found on remote host %s", host)
        return None

    # Parse first GPU
    line = lines[0].strip()
    parts = [p.strip() for p in line.split(",")]

    if len(parts) < 2:
        logger.warning("Unexpected nvidia-smi output format from %s: %s", host, line)
        return None

    try:
        index = int(parts[0])
        name = parts[1] if len(parts) > 1 else f"Remote GPU {index}"

        # Parse memory
        memory_gb = 0.0
        if len(parts) > 2:
            try:
                memory_mib = int(parts[2])
                memory_gb = round(memory_mib / 1024, 1)
            except ValueError:
                pass

        # Generate a stable ID from host
        safe_host = re.sub(r"[^a-zA-Z0-9]", "-", host)
        gpu_id = f"remote-{safe_host}-{index}"

        device = {
            "id": gpu_id,
            "name": name,
            "type": "ssh",
            "status": "available",
            "host": host,
            "user": user,
            "port": port,
            "memory_gb": memory_gb,
        }

        logger.info("Probed remote GPU: %s at %s (%s, %.1f GB)", gpu_id, host, name, memory_gb)
        return device

    except (ValueError, IndexError) as e:
        logger.warning("Failed to parse remote GPU info from %s: %s", host, e)
        return None


def update_gpu_usage(gpu_id: str, hours: float) -> None:
    """Update GPU usage statistics.

    Adds the specified hours to the total usage and updates the
    last_used timestamp.

    Args:
        gpu_id: ID of the GPU to update.
        hours: Hours to add to total usage.

    Raises:
        ConfigurationError: If GPU is not found in registry.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    for i, device in enumerate(devices):
        if device.get("id") == gpu_id:
            current_hours = float(device.get("total_hours", 0))
            devices[i]["total_hours"] = current_hours + hours
            devices[i]["last_used"] = datetime.now(timezone.utc).isoformat()
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            logger.info(
                "Updated GPU %s usage: +%.2f hours (total: %.2f)",
                gpu_id,
                hours,
                devices[i]["total_hours"],
            )
            return

    raise ConfigurationError(
        f"GPU not found in registry: {gpu_id}",
        config_file=str(get_gpu_registry_path()),
        key="devices",
    )


def register_gpu(device: GPUDevice) -> None:
    """Register a new GPU device.

    Adds the GPU to the registry if it doesn't already exist.

    Args:
        device: GPUDevice to register.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    # Check if GPU already exists
    for existing in devices:
        if existing.get("id") == device.id:
            logger.debug("GPU %s already registered, updating", device.id)
            existing.update(device.to_dict())
            save_user_gpu_registry(registry)
            return

    # Add new device
    devices.append(device.to_dict())
    registry["devices"] = devices
    save_user_gpu_registry(registry)
    logger.info("Registered GPU: %s (%s)", device.id, device.name)


def unregister_gpu(gpu_id: str) -> bool:
    """Unregister a GPU device.

    Removes the GPU from the registry.

    Args:
        gpu_id: ID of the GPU to unregister.

    Returns:
        True if GPU was removed, False if not found.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    original_count = len(devices)
    devices = [d for d in devices if d.get("id") != gpu_id]

    if len(devices) < original_count:
        registry["devices"] = devices
        save_user_gpu_registry(registry)
        logger.info("Unregistered GPU: %s", gpu_id)
        return True

    return False


def allocate_gpu(gpu_id: str, job_id: str) -> bool:
    """Allocate a GPU to a job.

    Marks the GPU as allocated to the specified job.

    Args:
        gpu_id: ID of the GPU to allocate.
        job_id: ID of the job to allocate to.

    Returns:
        True if allocation succeeded, False if GPU not available.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    for i, device in enumerate(devices):
        if device.get("id") == gpu_id:
            if device.get("status") != "available" or device.get("allocated_to"):
                logger.warning("GPU %s is not available for allocation", gpu_id)
                return False

            devices[i]["status"] = "busy"
            devices[i]["allocated_to"] = job_id
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            logger.info("Allocated GPU %s to job %s", gpu_id, job_id)
            return True

    logger.warning("GPU %s not found for allocation", gpu_id)
    return False


def release_gpu(gpu_id: str) -> bool:
    """Release a GPU from its current allocation.

    Marks the GPU as available again.

    Args:
        gpu_id: ID of the GPU to release.

    Returns:
        True if release succeeded, False if GPU not found.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    for i, device in enumerate(devices):
        if device.get("id") == gpu_id:
            devices[i]["status"] = "available"
            devices[i]["allocated_to"] = None
            registry["devices"] = devices
            save_user_gpu_registry(registry)
            logger.info("Released GPU %s", gpu_id)
            return True

    return False


def select_best_gpu(requirements: dict[str, Any]) -> str | None:
    """Select the best GPU based on requirements.

    Selects an available GPU that meets the specified requirements.
    Prioritizes:
    1. GPUs with required minimum memory
    2. GPUs with type matching preference (local/remote)
    3. GPUs with lowest total usage (load balancing)

    Args:
        requirements: Dictionary with optional keys:
            - min_memory_gb: Minimum GPU memory in GB
            - preference: "local", "remote", or "auto" (default)
            - exclude: List of GPU IDs to exclude

    Returns:
        ID of the best available GPU, or None if none available.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    min_memory = float(requirements.get("min_memory_gb", 0))
    preference = requirements.get("preference", "auto")
    exclude = set(requirements.get("exclude", []))

    # Filter available GPUs
    candidates = []
    for device_data in devices:
        device = GPUDevice.from_dict(device_data)

        # Skip excluded GPUs
        if device.id in exclude:
            continue

        # Skip unavailable GPUs
        if not device.is_available():
            continue

        # Check memory requirement
        if device.memory_gb < min_memory:
            continue

        candidates.append(device)

    if not candidates:
        logger.debug("No available GPUs meeting requirements: %s", requirements)
        return None

    # Sort by preference and usage
    def sort_key(gpu: GPUDevice) -> tuple[int, float]:
        # Priority: matching preference (0), wrong preference (1)
        if preference == "local":
            pref_match = 0 if gpu.type == "local" else 1
        elif preference == "remote":
            pref_match = 0 if gpu.type == "ssh" else 1
        else:
            pref_match = 0  # Auto: no preference

        # Secondary: lowest usage for load balancing
        return (pref_match, gpu.total_hours)

    candidates.sort(key=sort_key)

    selected = candidates[0]
    logger.info(
        "Selected GPU %s for requirements: memory=%.1f GB, preference=%s",
        selected.id,
        min_memory,
        preference,
    )
    return selected.id


def get_gpu_by_id(gpu_id: str) -> GPUDevice | None:
    """Get a GPU device by its ID.

    Args:
        gpu_id: ID of the GPU to retrieve.

    Returns:
        GPUDevice if found, None otherwise.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    for device_data in devices:
        if device_data.get("id") == gpu_id:
            return GPUDevice.from_dict(device_data)

    return None


def list_available_gpus() -> list[GPUDevice]:
    """List all available GPUs.

    Returns:
        List of GPUDevice objects that are currently available.
    """
    registry = load_user_gpu_registry()
    devices = registry.get("devices", [])

    available = []
    for device_data in devices:
        device = GPUDevice.from_dict(device_data)
        if device.is_available():
            available.append(device)

    return available


def refresh_gpu_registry(auto_discover: bool = True) -> dict[str, Any]:
    """Refresh the GPU registry by re-discovering local GPUs.

    Updates status of existing GPUs and adds newly discovered local GPUs.
    Does not remove manually registered remote GPUs.

    Args:
        auto_discover: If True, discover local GPUs automatically.

    Returns:
        Updated registry dictionary.
    """
    registry = load_user_gpu_registry()
    existing_devices = {d.get("id"): d for d in registry.get("devices", [])}

    if auto_discover:
        # Discover local GPUs
        local_gpus = discover_local_gpus()

        for gpu in local_gpus:
            gpu_id = gpu["id"]
            if gpu_id in existing_devices:
                # Update existing device
                existing_devices[gpu_id].update(gpu)
                # Reset status if it was offline
                if existing_devices[gpu_id].get("status") == "offline":
                    existing_devices[gpu_id]["status"] = "available"
            else:
                # Add new device
                existing_devices[gpu_id] = gpu

        # Mark local GPUs that weren't discovered as offline
        discovered_ids = {g["id"] for g in local_gpus}
        for device_id, device in existing_devices.items():
            if device.get("type") == "local" and device_id not in discovered_ids:
                device["status"] = "offline"

    registry["devices"] = list(existing_devices.values())
    save_user_gpu_registry(registry)

    logger.info("Refreshed GPU registry: %d devices", len(registry["devices"]))
    return registry
