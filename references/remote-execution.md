# Remote Execution

The runtime supports a platform-neutral execution abstraction.

Supported backends in the current implementation:

- `local`
- `ssh`

Core scripts:

- `scripts/schedule_jobs.py`
- `scripts/run_remote_job.py`

Current behavior:

- jobs are registered in `.autoresearch/runtime/job-registry.yaml`
- backends are tracked in `.autoresearch/runtime/backend-registry.yaml`
- GPU assignments are tracked in `.autoresearch/runtime/gpu-registry.yaml`
- stdout and stderr logs are written under `.autoresearch/runtime/logs/`

Project configuration may also record remote defaults in `.autoresearch/config/orchestrator-config.yaml`:

- `remote_defaults.ssh.host`
- `remote_defaults.ssh.project_root`

These values are project-level defaults for the human-facing orchestrator and prompt generation layer. The current runtime still accepts the concrete `--remote-host` and `--cwd` values per scheduled job.

This layer is designed to stay portable across Codex, Claude Code, and other agent shells.