"""ARIS (Autonomous Research Improvement System) integration constants."""

REVIEW_STATE_FILENAME = "REVIEW_STATE.json"
IDEA_STATE_FILENAME = "IDEA_STATE.json"
MAX_REVIEW_ROUNDS = 4
POSITIVE_SCORE_THRESHOLD = 6.0
POSITIVE_VERDICT_KEYWORDS = ("accept", "sufficient", "ready for submission", "almost")

DEFAULT_ARIS_CONFIG = {
    "auto_proceed": False,
    "pilot_max_hours": 2,
    "pilot_timeout_hours": 3,
    "max_pilot_ideas": 3,
    "max_total_gpu_hours": 8,
    "reviewer": {
        "enabled": False,
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
    },
    "max_review_rounds": 4,
    "positive_score_threshold": 6.0,
    "feishu": {
        "enabled": False,
        "mode": "off",
    },
}
