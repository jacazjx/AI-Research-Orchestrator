"""Version and version history constants."""

# System version
SYSTEM_VERSION = "1.17.0"
SYSTEM_VERSION_NAME = "Research Orchestrator"

VERSION_HISTORY = [
    ("1.0.0", "2026-03-01", "Initial release with five-phase workflow"),
    ("1.1.0", "2026-03-05", "Added agent responsibilities and literature verification"),
    ("1.2.0", "2026-03-08", "Added system audit and quality enforcement"),
    ("1.3.0", "2026-03-10", "Added project takeover capability"),
    ("1.4.0", "2026-03-13", "Added starting phase selection"),
    ("1.5.0", "2026-03-13", "Added statusline display and version tracking"),
    (
        "1.6.0",
        "2026-03-13",
        "Switched to PyYAML for full YAML support (comments, complex structures)",
    ),
    (
        "1.7.0",
        "2026-03-13",
        "Fixed KeyError in deliverables, added sub-agent failure recovery protocol",
    ),
    (
        "1.8.0",
        "2026-03-13",
        "Auto-complete missing deliverables on state load for backward compatibility",
    ),
    (
        "1.9.0",
        "2026-03-14",
        "Integrated ralph-loop for phase iteration control with completion promises",
    ),
    (
        "1.10.0",
        "2026-03-14",
        "Added experiment execution best practices (unbuffered output, "
        "checkpoint, process management) and document sync rules",
    ),
    (
        "1.11.0",
        "2026-03-14",
        "ARIS integration: cross-model review via Codex MCP, "
        "REVIEW_STATE persistence for long-running loops",
    ),
    (
        "1.12.0",
        "2026-03-14",
        "Full ARIS integration: 17 skills, three workflows, "
        "IDEA_STATE persistence, GPU protection, AUTO_PROCEED switch",
    ),
    (
        "1.13.0",
        "2026-03-19",
        "Semantic directory layout (docs/reports/ flattened), agent workspace "
        "structure, battle_protocol state machine, render_agent_prompt auto-inject, "
        "Agent Teams communication protocol, config quality/gpu fields",
    ),
    (
        "1.14.0",
        "2026-03-19",
        "Removed /reload command (auto-reload via SessionStart hook), "
        "removed argument-hint from commands, added interactive command workflows "
        "with AskUserQuestion, updated CLAUDE.md with plugin development standards",
    ),
    (
        "1.15.0",
        "2026-03-19",
        "Added Agent Skills (survey, critic, coder, adviser, writer, reviewer, "
        "reflector, curator) to fix subagent_type naming, updated skills/README.md",
    ),
    (
        "1.16.0",
        "2026-03-22",
        "Added system evaluation grader to Reflection phase: 6-dimension scoring "
        "(workflow, collaboration, gate accuracy, templates, efficiency, UX), "
        "global registry for cross-project trend tracking, Curator audit workflow",
    ),
    (
        "1.17.0",
        "2026-03-22",
        "Fix system audit issues: state migration consistency, gate race condition, schema validation, pivot validation, GPU error handling, version sync, env var config support",
    ),
]
