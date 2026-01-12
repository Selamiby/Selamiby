#!/usr/bin/env python3
"""
NEXUS MMO Sharding + Global State Manager
- 1000+ oyuncu için server sharding
- Global state sync (cross-shard messaging)
- Zone-based load balancing
"""
import json
import logging
import sqlite3
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler(log_dir / "mmo_sharding.log", encoding="utf-8")],
)
logger = logging.getLogger("mmo")

app = Flask(__name__)
DB_PATH = Path("mmo_global_state.db")

# Shard registry: {shard_id: {players: [], capacity: 200, load: 0.0}}
SHARDS = {}
PLAYER_TO_SHARD = {}  # {player_id: shard_id}
GLOBAL_STATE = {}  # Cross-shard shared state
LOCK = threading.Lock()

MAX_SHARD_CAPACITY = 200


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS shard_registry (
            shard_id TEXT PRIMARY KEY,
            region TEXT,
            capacity INTEGER,
            current_load INTEGER,
            created_at TEXT
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS player_shard_mapping (
            player_id TEXT PRIMARY KEY,
            shard_id TEXT,
            zone_id TEXT,
            last_update TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def _create_shard(region: str = "default") -> str:
    """Create new shard when capacity reached."""
    shard_id = f"shard-{len(SHARDS)+1}-{region}"
    SHARDS[shard_id] = {
        "players": [],
        "capacity": MAX_SHARD_CAPACITY,
        "load": 0.0,
        "region": region,
    }

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO shard_registry (shard_id, region, capacity, current_load, created_at) VALUES (?, ?, ?, ?, ?)",
        (shard_id, region, MAX_SHARD_CAPACITY, 0, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

    logger.info(f"✓ Created {shard_id}")
    return shard_id


def _assign_shard(player_id: str, region: str = "default") -> str:
    """Assign player to least loaded shard."""
    with LOCK:
        # Find least loaded shard in region
        available = [
            s
            for s, data in SHARDS.items()
            if data["region"] == region and len(data["players"]) < data["capacity"]
        ]

        if not available:
            shard_id = _create_shard(region)
        else:
            shard_id = min(available, key=lambda s: len(SHARDS[s]["players"]))

        SHARDS[shard_id]["players"].append(player_id)
        SHARDS[shard_id]["load"] = (
            len(SHARDS[shard_id]["players"]) / SHARDS[shard_id]["capacity"]
        )
        PLAYER_TO_SHARD[player_id] = shard_id

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO player_shard_mapping (player_id, shard_id, zone_id, last_update) VALUES (?, ?, ?, ?)",
            (player_id, shard_id, "zone-1", datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()

        return shard_id


@app.route("/mmo/join", methods=["POST"])
def join():
    """Player joins MMO."""
    payload = request.json or {}
    player_id = payload.get("player_id")
    region = payload.get("region", "default")

    shard_id = _assign_shard(player_id, region)
    logger.info(
        f"✓ {player_id} → {shard_id} ({len(SHARDS[shard_id]['players'])} players)"
    )

    return jsonify(
        {
            "shard_id": shard_id,
            "capacity": SHARDS[shard_id]["capacity"],
            "load": SHARDS[shard_id]["load"],
        }
    )


@app.route("/mmo/state", methods=["POST"])
def update_global_state():
    """Update cross-shard global state (e.g., world boss HP)."""
    payload = request.json or {}
    key = payload.get("key")
    value = payload.get("value")

    with LOCK:
        GLOBAL_STATE[key] = {"value": value, "ts": time.time()}

    return jsonify({"status": "ok"})


@app.route("/mmo/state/<key>")
def get_global_state(key: str):
    """Get global state."""
    return jsonify(GLOBAL_STATE.get(key, {}))


@app.route("/mmo/transfer", methods=["POST"])
def transfer_shard():
    """Transfer player to different shard (zone change)."""
    payload = request.json or {}
    player_id = payload.get("player_id")
    target_shard = payload.get("target_shard")

    with LOCK:
        if player_id in PLAYER_TO_SHARD:
            old_shard = PLAYER_TO_SHARD[player_id]
            SHARDS[old_shard]["players"].remove(player_id)
            SHARDS[target_shard]["players"].append(player_id)
            PLAYER_TO_SHARD[player_id] = target_shard
            return jsonify(
                {"status": "transferred", "from": old_shard, "to": target_shard}
            )

    return jsonify({"status": "error", "message": "Player not found"})


@app.route("/mmo/stats")
def stats():
    """Get MMO statistics."""
    return jsonify(
        {
            "total_shards": len(SHARDS),
            "total_players": sum(len(s["players"]) for s in SHARDS.values()),
            "shards": {
                sid: {"players": len(s["players"]), "load": s["load"]}
                for sid, s in SHARDS.items()
            },
        }
    )


if __name__ == "__main__":
    _init_db()

    # Create initial shard
    if not SHARDS:
        _create_shard("default")

    logger.info("🚀 MMO Sharding Server starting on port 7005")
    app.run(host="0.0.0.0", port=7005, threaded=False)


@app.route("/mmo/shards")
def list_shards():
    """List all shards."""
    return jsonify(
        {
            "shards": {
                k: {"players": len(v["players"]), "load": v["load"]}
                for k, v in SHARDS.items()
            }
        }
    )


if __name__ == "__main__":
    _init_db()
    _create_shard("default")  # Bootstrap shard
    logger.info("MMO Sharding Manager on 0.0.0.0:7005")
    app.run(host="0.0.0.0", port=7005, threaded=True)
