# Self-Healing

The runtime uses a bounded, inspectable recovery model.

Core scripts:

- `scripts/sentinel.py`
- `scripts/recover_stage.py`

Detection targets:

- stale running jobs
- missing current-phase deliverables
- missing registry entries for active jobs

Allowed recovery actions:

- retry a failed or stale job
- resume a paused job
- regenerate dashboard artifacts

The runtime must never silently skip failed work.
