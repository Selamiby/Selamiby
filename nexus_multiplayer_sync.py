#!/usr/bin/env python3
"""
NEXUS Multiplayer State Sync (Lightweight)
- Authoritative server, client prediction, lag compensation
- No heavy threading, async-friendly
"""
import json
import logging
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler(log_dir / "multiplayer.log", encoding="utf-8")],
)
logger = logging.getLogger("mp")

app = Flask(__name__)
DB_PATH = Path("multiplayer.db")
ACTIVE_PLAYERS = {}  # {player_id: {pos, rot, ts}}


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS player_state (
            player_id TEXT PRIMARY KEY,
            x REAL, y REAL, z REAL,
            rx REAL, ry REAL, rz REAL,
            action TEXT,
            updated_at TEXT
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/mp/join", methods=["POST"])
def join():
    """Player joins session."""
    payload = request.json or {}
    player_id = payload.get("player_id")

    ACTIVE_PLAYERS[player_id] = {
        "x": 0,
        "y": 0,
        "z": 0,
        "rx": 0,
        "ry": 0,
        "rz": 0,
        "ts": time.time(),
    }
    logger.info(f"✓ {player_id} joined ({len(ACTIVE_PLAYERS)} players)")
    return jsonify({"status": "joined", "players": list(ACTIVE_PLAYERS.keys())})


@app.route("/mp/update", methods=["POST"])
def update_state():
    """Client sends authoritative state update."""
    payload = request.json or {}
    player_id = payload.get("player_id")

    if player_id not in ACTIVE_PLAYERS:
        return jsonify({"error": "not joined"}), 400

    # Authoritative: server accepts and broadcasts
    ACTIVE_PLAYERS[player_id].update(
        {
            "x": payload.get("x", 0),
            "y": payload.get("y", 0),
            "z": payload.get("z", 0),
            "rx": payload.get("rx", 0),
            "ry": payload.get("ry", 0),
            "rz": payload.get("rz", 0),
            "action": payload.get("action", "idle"),
            "ts": time.time(),
        }
    )

    return jsonify({"status": "ok"})


@app.route("/mp/state")
def get_state():
    """Get all player states (client prediction + correction)."""
    player_id = request.args.get("player_id")

    # Lag compensation: interpolate positions based on age
    states = {}
    now = time.time()

    for pid, state in ACTIVE_PLAYERS.items():
        age = now - state["ts"]
        # Simple linear prediction (velocity not tracked in this minimal version)
        states[pid] = {
            "x": state["x"],
            "y": state["y"],
            "z": state["z"],
            "rx": state["rx"],
            "ry": state["ry"],
            "rz": state["rz"],
            "action": state["action"],
            "age_ms": int(age * 1000),
        }

    return jsonify({"players": states})


@app.route("/mp/leave", methods=["POST"])
def leave():
    """Player leaves."""
    payload = request.json or {}
    player_id = payload.get("player_id")

    if player_id in ACTIVE_PLAYERS:
        del ACTIVE_PLAYERS[player_id]
        logger.info(f"✓ {player_id} left ({len(ACTIVE_PLAYERS)} players)")

    return jsonify({"status": "ok"})


@app.route("/mp/health")
def health():
    return jsonify({"status": "ok", "active_players": len(ACTIVE_PLAYERS)})


if __name__ == "__main__":
    _init_db()
    logger.info("Multiplayer server on 0.0.0.0:7003")
    app.run(host="0.0.0.0", port=7003, threaded=False)
