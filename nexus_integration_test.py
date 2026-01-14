import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
"""
NEXUS Integration Test Suite
End-to-end game backend playthrough (no CPU spike)
"""
import json
import logging
import random
import sys
import time
from pathlib import Path

import requests

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "integration_test.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("e2e")

BACKENDS = {
    "game": "http://127.0.0.1:7000",
    "crash": "http://127.0.0.1:7001",
    "profiler": "http://127.0.0.1:7002",
    "multiplayer": "http://127.0.0.1:7003",
    "analytics": "http://127.0.0.1:7004",
}

TEST_RESULTS = {"passed": 0, "failed": 0, "errors": []}


def test(name: str, fn):
    """Run single test."""
    try:
        fn()
        TEST_RESULTS["passed"] += 1
        logger.info(f"✓ {name}")
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        TEST_RESULTS["errors"].append(f"{name}: {e}")
        logger.error(f"✗ {name}: {e}")


def test_game_backend():
    """Test leaderboard/telemetry/feature flags."""
    r = requests.post(
        f"{BACKENDS['game']}/leaderboard/submit",
        json={"player_id": "test-player", "score": 1000},
        timeout=5,
    )
    assert r.status_code == 200, f"Status {r.status_code}"

    r = requests.get(f"{BACKENDS['game']}/leaderboard/top?limit=5", timeout=5)
    assert r.status_code == 200
    assert "top" in r.json()


def test_crash_storage():
    """Test crash reporting."""
    r = requests.post(
        f"{BACKENDS['crash']}/crash/submit",
        json={
            "crash_id": f"crash-{int(time.time())}",
            "player_id": "test-player",
            "stacktrace": "test",
        },
        timeout=5,
    )
    assert r.status_code == 200 or r.status_code == 201


def test_profiler():
    """Test performance metrics submission."""
    r = requests.post(
        f"{BACKENDS['profiler']}/profile/frame",
        json={
            "player_id": "test-player",
            "metrics": {"fps": 60, "draw_calls": 20, "gc_memory_mb": 256},
            "platform": "pc",
            "quality": "high",
        },
        timeout=5,
    )
    assert r.status_code == 200


def test_multiplayer():
    """Test player join/state update."""
    player_id = f"mp-player-{random.randint(1000, 9999)}"

    r = requests.post(
        f"{BACKENDS['multiplayer']}/mp/join", json={"player_id": player_id}, timeout=5
    )
    assert r.status_code == 200

    r = requests.post(
        f"{BACKENDS['multiplayer']}/mp/update",
        json={"player_id": player_id, "x": 10, "y": 5, "z": 0},
        timeout=5,
    )
    assert r.status_code == 200


def test_analytics():
    """Test analytics endpoint."""
    r = requests.get(f"{BACKENDS['analytics']}/api/analytics", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "top_players" in data


def run_all_tests():
    """Execute full suite."""
    logger.info("=" * 60)
    logger.info("🧪 NEXUS INTEGRATION TEST SUITE")
    logger.info("=" * 60)

    test("GameBackend.Leaderboard", test_game_backend)
    time.sleep(0.5)  # Light pause

    test("CrashStorage.Report", test_crash_storage)
    time.sleep(0.5)

    test("Profiler.FrameMetrics", test_profiler)
    time.sleep(0.5)

    test("Multiplayer.JoinUpdate", test_multiplayer)
    time.sleep(0.5)

    test("Analytics.Dashboard", test_analytics)

    logger.info("=" * 60)
    logger.info(
        f"Results: {TEST_RESULTS['passed']} passed, {TEST_RESULTS['failed']} failed"
    )

    if TEST_RESULTS["errors"]:
        logger.error("Errors:")
        for err in TEST_RESULTS["errors"]:
            logger.error(f"  - {err}")

    logger.info("=" * 60)

    return TEST_RESULTS["failed"] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
