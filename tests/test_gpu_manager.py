"""
Tests for gpu_manager.py module.
"""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    """Dynamically load a script module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# Load user_config first since gpu_manager depends on it
USER_CONFIG = load_script_module("user_config")
GPU_MANAGER = load_script_module("gpu_manager")
EXCEPTIONS = load_script_module("exceptions")


class GPUDeviceTest(unittest.TestCase):
    """Test GPUDevice dataclass."""

    def test_gpu_device_creation(self) -> None:
        """Test creating a GPUDevice."""
        device = GPU_MANAGER.GPUDevice(
            id="local-0",
            name="NVIDIA RTX 4090",
            type="local",
            status="available",
            memory_gb=24.0,
        )

        self.assertEqual(device.id, "local-0")
        self.assertEqual(device.name, "NVIDIA RTX 4090")
        self.assertEqual(device.type, "local")
        self.assertEqual(device.status, "available")
        self.assertEqual(device.memory_gb, 24.0)

    def test_gpu_device_to_dict(self) -> None:
        """Test GPUDevice.to_dict()."""
        device = GPU_MANAGER.GPUDevice(
            id="local-0",
            name="NVIDIA RTX 4090",
            type="local",
            status="available",
            memory_gb=24.0,
            total_hours=10.5,
        )

        d = device.to_dict()

        self.assertEqual(d["id"], "local-0")
        self.assertEqual(d["name"], "NVIDIA RTX 4090")
        self.assertEqual(d["type"], "local")
        self.assertEqual(d["status"], "available")
        self.assertEqual(d["memory_gb"], 24.0)
        self.assertEqual(d["total_hours"], 10.5)

    def test_gpu_device_from_dict(self) -> None:
        """Test GPUDevice.from_dict()."""
        data = {
            "id": "remote-1",
            "name": "NVIDIA A100",
            "type": "ssh",
            "status": "available",
            "memory_gb": 80.0,
            "host": "192.168.1.100",
            "user": "researcher",
            "port": 22,
        }

        device = GPU_MANAGER.GPUDevice.from_dict(data)

        self.assertEqual(device.id, "remote-1")
        self.assertEqual(device.name, "NVIDIA A100")
        self.assertEqual(device.type, "ssh")
        self.assertEqual(device.host, "192.168.1.100")
        self.assertEqual(device.user, "researcher")
        self.assertEqual(device.port, 22)

    def test_gpu_device_is_available(self) -> None:
        """Test GPUDevice.is_available()."""
        available = GPU_MANAGER.GPUDevice(id="test", status="available")
        busy = GPU_MANAGER.GPUDevice(id="test", status="busy")
        allocated = GPU_MANAGER.GPUDevice(id="test", status="available", allocated_to="job-1")

        self.assertTrue(available.is_available())
        self.assertFalse(busy.is_available())
        self.assertFalse(allocated.is_available())

    def test_gpu_device_is_remote(self) -> None:
        """Test GPUDevice.is_remote()."""
        local = GPU_MANAGER.GPUDevice(id="test", type="local")
        remote = GPU_MANAGER.GPUDevice(id="test", type="ssh")

        self.assertFalse(local.is_remote())
        self.assertTrue(remote.is_remote())


class GPURegistryTest(unittest.TestCase):
    """Test GPURegistry dataclass."""

    def test_gpu_registry_creation(self) -> None:
        """Test creating a GPURegistry."""
        registry = GPU_MANAGER.GPURegistry(
            devices=[
                GPU_MANAGER.GPUDevice(id="local-0", name="RTX 4090"),
            ]
        )

        self.assertEqual(len(registry.devices), 1)
        self.assertEqual(registry.devices[0].id, "local-0")

    def test_gpu_registry_to_dict(self) -> None:
        """Test GPURegistry.to_dict()."""
        registry = GPU_MANAGER.GPURegistry(
            devices=[
                GPU_MANAGER.GPUDevice(id="local-0", name="RTX 4090"),
                GPU_MANAGER.GPUDevice(id="remote-0", name="A100", type="ssh"),
            ]
        )

        d = registry.to_dict()

        self.assertEqual(d["version"], GPU_MANAGER.REGISTRY_VERSION)
        self.assertEqual(len(d["devices"]), 2)

    def test_gpu_registry_from_dict(self) -> None:
        """Test GPURegistry.from_dict()."""
        data = {
            "version": "1.0.0",
            "devices": [
                {"id": "local-0", "name": "RTX 4090"},
            ],
        }

        registry = GPU_MANAGER.GPURegistry.from_dict(data)

        self.assertEqual(registry.version, "1.0.0")
        self.assertEqual(len(registry.devices), 1)


class GPURegistryPathTest(unittest.TestCase):
    """Test GPU registry path functions."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_get_gpu_registry_path(self) -> None:
        """Test GPU registry path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            registry_path = GPU_MANAGER.get_gpu_registry_path()

            self.assertEqual(registry_path.name, "gpu-registry.yaml")
            self.assertTrue(str(registry_path).endswith(".autoresearch/gpu-registry.yaml"))

    def test_get_default_gpu_registry(self) -> None:
        """Test default GPU registry structure."""
        defaults = GPU_MANAGER.get_default_gpu_registry()

        self.assertIn("version", defaults)
        self.assertIn("devices", defaults)
        self.assertEqual(defaults["devices"], [])


class LoadSaveGPURegistryTest(unittest.TestCase):
    """Test loading and saving GPU registry."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_load_gpu_registry_not_exists(self) -> None:
        """Test loading registry when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            registry = GPU_MANAGER.load_user_gpu_registry()

            # Should return defaults
            self.assertEqual(registry["version"], GPU_MANAGER.REGISTRY_VERSION)
            self.assertEqual(registry["devices"], [])

    def test_save_and_load_gpu_registry(self) -> None:
        """Test saving and loading GPU registry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Save registry
            registry = {
                "version": "1.0.0",
                "devices": [
                    {
                        "id": "local-0",
                        "name": "NVIDIA RTX 4090",
                        "type": "local",
                        "status": "available",
                        "memory_gb": 24.0,
                        "total_hours": 5.0,
                    },
                    {
                        "id": "remote-server-0",
                        "name": "NVIDIA A100",
                        "type": "ssh",
                        "status": "available",
                        "host": "192.168.1.100",
                        "user": "researcher",
                        "port": 22,
                        "memory_gb": 80.0,
                    },
                ],
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            # Load registry
            loaded = GPU_MANAGER.load_user_gpu_registry()

            self.assertEqual(len(loaded["devices"]), 2)
            self.assertEqual(loaded["devices"][0]["id"], "local-0")
            self.assertEqual(loaded["devices"][1]["type"], "ssh")

    def test_save_gpu_registry_creates_directory(self) -> None:
        """Test that save creates the registry directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = GPU_MANAGER.get_default_gpu_registry()
            GPU_MANAGER.save_user_gpu_registry(registry)

            registry_path = GPU_MANAGER.get_gpu_registry_path()
            self.assertTrue(registry_path.exists())
            self.assertTrue(registry_path.parent.exists())


class DiscoverLocalGPUsTest(unittest.TestCase):
    """Test local GPU discovery."""

    @patch("subprocess.run")
    def test_discover_local_gpus_success(self, mock_run: MagicMock) -> None:
        """Test successful GPU discovery."""
        # Mock nvidia-smi output
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="0, NVIDIA RTX 4090, 24576\n1, NVIDIA RTX 3090, 24576\n",
        )

        devices = GPU_MANAGER.discover_local_gpus()

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]["id"], "local-0")
        self.assertEqual(devices[0]["name"], "NVIDIA RTX 4090")
        self.assertEqual(devices[0]["memory_gb"], 24.0)
        self.assertEqual(devices[1]["id"], "local-1")

    @patch("subprocess.run")
    def test_discover_local_gpus_no_gpus(self, mock_run: MagicMock) -> None:
        """Test GPU discovery with no GPUs."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        devices = GPU_MANAGER.discover_local_gpus()

        self.assertEqual(len(devices), 0)

    @patch("subprocess.run")
    def test_discover_local_gpus_nvidia_smi_not_found(self, mock_run: MagicMock) -> None:
        """Test GPU discovery when nvidia-smi is not found."""
        mock_run.side_effect = FileNotFoundError()

        devices = GPU_MANAGER.discover_local_gpus()

        self.assertEqual(len(devices), 0)

    @patch("subprocess.run")
    def test_discover_local_gpus_timeout(self, mock_run: MagicMock) -> None:
        """Test GPU discovery timeout."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired("nvidia-smi", 30)

        devices = GPU_MANAGER.discover_local_gpus()

        self.assertEqual(len(devices), 0)

    @patch("subprocess.run")
    def test_discover_local_gpus_failure(self, mock_run: MagicMock) -> None:
        """Test GPU discovery when nvidia-smi fails."""
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")

        devices = GPU_MANAGER.discover_local_gpus()

        self.assertEqual(len(devices), 0)


class ProbeRemoteGPUTest(unittest.TestCase):
    """Test remote GPU probing."""

    @patch("subprocess.run")
    def test_probe_remote_gpu_success(self, mock_run: MagicMock) -> None:
        """Test successful remote GPU probe."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="0, NVIDIA A100, 81920\n",
        )

        result = GPU_MANAGER.probe_remote_gpu("192.168.1.100", "researcher", 22)

        self.assertIsNotNone(result)
        assert result is not None  # Type guard
        self.assertEqual(result["type"], "ssh")
        self.assertEqual(result["host"], "192.168.1.100")
        self.assertEqual(result["user"], "researcher")
        self.assertEqual(result["memory_gb"], 80.0)

    @patch("subprocess.run")
    def test_probe_remote_gpu_no_gpus(self, mock_run: MagicMock) -> None:
        """Test remote probe with no GPUs."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        result = GPU_MANAGER.probe_remote_gpu("192.168.1.100", "researcher")

        self.assertIsNone(result)

    @patch("subprocess.run")
    def test_probe_remote_gpu_ssh_failure(self, mock_run: MagicMock) -> None:
        """Test remote probe when SSH fails."""
        mock_run.return_value = MagicMock(returncode=255, stderr="Connection refused")

        result = GPU_MANAGER.probe_remote_gpu("192.168.1.100", "researcher")

        self.assertIsNone(result)

    @patch("subprocess.run")
    def test_probe_remote_gpu_timeout(self, mock_run: MagicMock) -> None:
        """Test remote probe timeout."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired("ssh", 30)

        result = GPU_MANAGER.probe_remote_gpu("192.168.1.100", "researcher")

        self.assertIsNone(result)

    @patch("subprocess.run")
    def test_probe_remote_gpu_ssh_not_found(self, mock_run: MagicMock) -> None:
        """Test remote probe when SSH is not found."""
        mock_run.side_effect = FileNotFoundError()

        result = GPU_MANAGER.probe_remote_gpu("192.168.1.100", "researcher")

        self.assertIsNone(result)


class UpdateGPUUsageTest(unittest.TestCase):
    """Test GPU usage update."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_update_gpu_usage(self) -> None:
        """Test updating GPU usage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Create registry with a GPU
            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 4090", "total_hours": 5.0},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            # Update usage
            GPU_MANAGER.update_gpu_usage("local-0", 2.5)

            # Check result
            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(loaded["devices"][0]["total_hours"], 7.5)
            self.assertIsNotNone(loaded["devices"][0]["last_used"])

    def test_update_gpu_usage_not_found(self) -> None:
        """Test updating usage for non-existent GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            GPU_MANAGER.save_user_gpu_registry({"devices": []})

            with self.assertRaises(GPU_MANAGER.ConfigurationError):
                GPU_MANAGER.update_gpu_usage("nonexistent", 1.0)


class GPUAllocationTest(unittest.TestCase):
    """Test GPU allocation functions."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_allocate_gpu(self) -> None:
        """Test allocating a GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 4090", "status": "available"},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            result = GPU_MANAGER.allocate_gpu("local-0", "job-1")

            self.assertTrue(result)
            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(loaded["devices"][0]["status"], "busy")
            self.assertEqual(loaded["devices"][0]["allocated_to"], "job-1")

    def test_allocate_gpu_already_allocated(self) -> None:
        """Test allocating an already allocated GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "busy",
                        "allocated_to": "job-0",
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            result = GPU_MANAGER.allocate_gpu("local-0", "job-1")

            self.assertFalse(result)

    def test_release_gpu(self) -> None:
        """Test releasing a GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "busy",
                        "allocated_to": "job-1",
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            result = GPU_MANAGER.release_gpu("local-0")

            self.assertTrue(result)
            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(loaded["devices"][0]["status"], "available")
            self.assertIsNone(loaded["devices"][0]["allocated_to"])


class RegisterGPUTest(unittest.TestCase):
    """Test GPU registration."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_register_gpu(self) -> None:
        """Test registering a new GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            GPU_MANAGER.save_user_gpu_registry({"devices": []})

            device = GPU_MANAGER.GPUDevice(
                id="local-0",
                name="RTX 4090",
                type="local",
                memory_gb=24.0,
            )
            GPU_MANAGER.register_gpu(device)

            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(len(loaded["devices"]), 1)
            self.assertEqual(loaded["devices"][0]["id"], "local-0")

    def test_register_gpu_update_existing(self) -> None:
        """Test updating an existing GPU registration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "Old Name", "status": "available"},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            device = GPU_MANAGER.GPUDevice(
                id="local-0",
                name="New Name",
                status="busy",
            )
            GPU_MANAGER.register_gpu(device)

            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(len(loaded["devices"]), 1)
            self.assertEqual(loaded["devices"][0]["name"], "New Name")
            self.assertEqual(loaded["devices"][0]["status"], "busy")

    def test_unregister_gpu(self) -> None:
        """Test unregistering a GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 4090"},
                    {"id": "local-1", "name": "RTX 3090"},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            result = GPU_MANAGER.unregister_gpu("local-0")

            self.assertTrue(result)
            loaded = GPU_MANAGER.load_user_gpu_registry()
            self.assertEqual(len(loaded["devices"]), 1)
            self.assertEqual(loaded["devices"][0]["id"], "local-1")

    def test_unregister_gpu_not_found(self) -> None:
        """Test unregistering a non-existent GPU."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            GPU_MANAGER.save_user_gpu_registry({"devices": []})

            result = GPU_MANAGER.unregister_gpu("nonexistent")

            self.assertFalse(result)


class SelectBestGPUTest(unittest.TestCase):
    """Test GPU selection."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_select_best_gpu_basic(self) -> None:
        """Test basic GPU selection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "available",
                        "memory_gb": 24.0,
                        "total_hours": 10.0,
                    },
                    {
                        "id": "local-1",
                        "name": "RTX 3090",
                        "status": "available",
                        "memory_gb": 24.0,
                        "total_hours": 5.0,
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            selected = GPU_MANAGER.select_best_gpu({})

            # Should select GPU with lowest usage
            self.assertEqual(selected, "local-1")

    def test_select_best_gpu_with_memory_requirement(self) -> None:
        """Test GPU selection with memory requirement."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 3090", "status": "available", "memory_gb": 24.0},
                    {
                        "id": "remote-0",
                        "name": "A100",
                        "status": "available",
                        "memory_gb": 80.0,
                        "type": "ssh",
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            selected = GPU_MANAGER.select_best_gpu({"min_memory_gb": 40})

            self.assertEqual(selected, "remote-0")

    def test_select_best_gpu_with_preference(self) -> None:
        """Test GPU selection with type preference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "available",
                        "memory_gb": 24.0,
                        "type": "local",
                        "total_hours": 0,
                    },
                    {
                        "id": "remote-0",
                        "name": "A100",
                        "status": "available",
                        "memory_gb": 80.0,
                        "type": "ssh",
                        "total_hours": 0,
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            selected = GPU_MANAGER.select_best_gpu({"preference": "local"})

            self.assertEqual(selected, "local-0")

    def test_select_best_gpu_exclude(self) -> None:
        """Test GPU selection with exclusion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "available",
                        "memory_gb": 24.0,
                        "total_hours": 0,
                    },
                    {
                        "id": "local-1",
                        "name": "RTX 3090",
                        "status": "available",
                        "memory_gb": 24.0,
                        "total_hours": 0,
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            selected = GPU_MANAGER.select_best_gpu({"exclude": ["local-0"]})

            self.assertEqual(selected, "local-1")

    def test_select_best_gpu_none_available(self) -> None:
        """Test GPU selection when none available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {
                        "id": "local-0",
                        "name": "RTX 4090",
                        "status": "busy",
                        "allocated_to": "job-1",
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            selected = GPU_MANAGER.select_best_gpu({})

            self.assertIsNone(selected)


class ListAvailableGPUsTest(unittest.TestCase):
    """Test listing available GPUs."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_list_available_gpus(self) -> None:
        """Test listing available GPUs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 4090", "status": "available"},
                    {
                        "id": "local-1",
                        "name": "RTX 3090",
                        "status": "busy",
                        "allocated_to": "job-1",
                    },
                    {"id": "local-2", "name": "RTX 3080", "status": "available"},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            available = GPU_MANAGER.list_available_gpus()

            self.assertEqual(len(available), 2)
            ids = [g.id for g in available]
            self.assertIn("local-0", ids)
            self.assertIn("local-2", ids)
            self.assertNotIn("local-1", ids)


class RefreshGPURegistryTest(unittest.TestCase):
    """Test GPU registry refresh."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    @patch("subprocess.run")
    def test_refresh_gpu_registry(self, mock_run: MagicMock) -> None:
        """Test refreshing GPU registry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Existing registry with a remote GPU
            registry = {
                "devices": [
                    {
                        "id": "remote-0",
                        "name": "A100",
                        "type": "ssh",
                        "host": "server1",
                        "status": "available",
                    },
                    {
                        "id": "local-0",
                        "name": "Old GPU",
                        "type": "local",
                        "status": "available",
                    },
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            # Mock discovering new local GPU
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="0, NVIDIA RTX 4090, 24576\n",
            )

            refreshed = GPU_MANAGER.refresh_gpu_registry(auto_discover=True)

            # Should have remote GPU and updated local GPU
            ids = [d["id"] for d in refreshed["devices"]]
            self.assertIn("remote-0", ids)
            self.assertIn("local-0", ids)

    def test_refresh_gpu_registry_skip_discovery(self) -> None:
        """Test refreshing GPU registry without discovery."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            registry = {
                "devices": [
                    {"id": "local-0", "name": "RTX 4090", "status": "available"},
                ]
            }
            GPU_MANAGER.save_user_gpu_registry(registry)

            refreshed = GPU_MANAGER.refresh_gpu_registry(auto_discover=False)

            self.assertEqual(len(refreshed["devices"]), 1)


if __name__ == "__main__":
    unittest.main()
