import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
"""
NEXUS Playtest Bot (advanced)
- Robust smoke & mini-load scenarios against game backend
- Retries, latency capture, basic assertions, JSON summary
"""
import json
import os
import random
import time
from typing import Any, Dict, List

import requests

BACKEND = os.getenv("NEXUS_GAME_BACKEND", "http://127.0.0.1:7000")
DEFAULT_TIMEOUT = 5
RETRIES = 3


def _post(
    session: requests.Session, path: str, payload: Dict[str, Any]
) -> requests.Response:
    url = f"{BACKEND}{path}"
    for attempt in range(RETRIES):
        try:
            resp = session.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
            if resp.ok:
                return resp
            time.sleep(0.5 * (attempt + 1))
        except requests.RequestException:
            if attempt == RETRIES - 1:
                raise
            time.sleep(0.5 * (attempt + 1))
    return resp  # type: ignore


def _get(session: requests.Session, path: str) -> requests.Response:
    url = f"{BACKEND}{path}"
    for attempt in range(RETRIES):
        try:
            resp = session.get(url, timeout=DEFAULT_TIMEOUT)
            if resp.ok:
                return resp
            time.sleep(0.5 * (attempt + 1))
        except requests.RequestException:
            if attempt == RETRIES - 1:
                raise
            time.sleep(0.5 * (attempt + 1))
    return resp  # type: ignore


def run_scenario(session: requests.Session) -> Dict[str, Any]:
    player = f"bot-{random.randint(1000, 9999)}"
    started = time.time()

    score = random.randint(500, 5000)
    meta = {"mode": "smoke", "device": "test"}
    r1 = _post(
        session,
        "/leaderboard/submit",
        {"player_id": player, "score": score, "meta": meta},
    )
    r1.raise_for_status()

    events = [
        ("level_start", {"level": 1}),
        ("level_complete", {"time": round(random.random() * 120, 2)}),
        ("loot_pickup", {"item": "coin", "amount": random.randint(1, 50)}),
    ]
    for ev, payload in events:
        r_ev = _post(
            session,
            "/telemetry",
            {"player_id": player, "event": ev, "payload": payload},
        )
        r_ev.raise_for_status()

    _post(
        session,
        "/crash",
        {
            "player_id": player,
            "stacktrace": "Traceback (most recent call last): simulated crash",
            "device_info": {"os": "test", "gpu": "test"},
        },
    ).raise_for_status()

    top = _get(session, "/leaderboard/top?limit=5").json()
    flags = _get(session, "/feature-flags").json()
    variant = _get(session, f"/ab-variant?player_id={player}").json()
    stats = _get(session, "/stats").json()

    elapsed = round(time.time() - started, 3)

    assert "top" in top, "leaderboard/top missing 'top' key"
    assert "flags" in flags, "feature-flags missing 'flags' key"
    assert "variant" in variant, "ab-variant missing 'variant' key"

    return {
        "player": player,
        "score": score,
        "variant": variant.get("variant"),
        "top_count": len(top.get("top", [])),
        "flags_version": flags.get("version"),
        "stats": stats,
        "elapsed_sec": elapsed,
    }


def run_batch(batch_size: int = 5) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    with requests.Session() as session:
        for _ in range(batch_size):
            out.append(run_scenario(session))
            time.sleep(0.2)
    return out


def main():
    batch_size = int(os.getenv("NEXUS_PLAYTEST_BATCH", "5"))
    results = run_batch(batch_size)
    print(
        json.dumps(
            {"backend": BACKEND, "batch_size": batch_size, "results": results}, indent=2
        )
    )


if __name__ == "__main__":
    main()
