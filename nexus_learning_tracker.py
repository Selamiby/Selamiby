#!/usr/bin/env python3
"""
NEXUS-ONE Learning Tracker
- Centralized logging of learning events (workspace, web, self-learning, multimodal)
- Writes aggregated stats to nexus_data/learning_stats.json
- Appends human-readable entries to nexus_logs/learning_report.log
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

WORKSPACE = Path.cwd()
DATA_DIR = WORKSPACE / "nexus_data"
LOG_DIR = WORKSPACE / "nexus_logs"
STATS_FILE = DATA_DIR / "learning_stats.json"
REPORT_LOG = LOG_DIR / "learning_report.log"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def _load_stats() -> Dict[str, Any]:
    try:
        if STATS_FILE.exists():
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {
        "sessions": 0,
        "files_learned": 0,
        "concepts_learned": 0,
        "commands_learned": 0,
        "patterns_learned": 0,
        "web_sessions": 0,
        "vision_events": 0,
        "audio_events": 0,
        "last_learn_time": None,
    }


def record_event(source: str, **metrics):
    """Update global learning stats and append a human-friendly log line."""
    stats = _load_stats()
    stats["sessions"] = int(stats.get("sessions", 0)) + 1
    stats["last_learn_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Increment known counters if provided
    for key in [
        "files_learned",
        "concepts_learned",
        "commands_learned",
        "patterns_learned",
        "web_sessions",
        "vision_events",
        "audio_events",
    ]:
        if key in metrics:
            stats[key] = int(stats.get(key, 0)) + int(metrics.get(key, 0))

    try:
        STATS_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    except Exception:
        pass

    # Write human-readable report
    try:
        line = f"[{stats['last_learn_time']}] source={source} " + ", ".join(
            [f"{k}={v}" for k, v in metrics.items() if v is not None]
        )
        with REPORT_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

    return stats


def snapshot_stats() -> Dict[str, Any]:
    """Return current stats without modifying."""
    return _load_stats()


if __name__ == "__main__":
    print(json.dumps(snapshot_stats(), indent=2, ensure_ascii=False))
