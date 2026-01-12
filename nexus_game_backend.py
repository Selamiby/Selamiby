#!/usr/bin/env python3
"""
NEXUS Game Backend
- Leaderboard + telemetry + crash ingest
- Feature flags + A/B variant helper
- Lightweight lobby skeleton (multiplayer placeholder)
Runs on Flask at 0.0.0.0:7000
"""
import json
import logging
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "nexus_game_backend.db"
FLAGS_PATH = BASE_DIR / "game_feature_flags.json"

log_dir = BASE_DIR / "nexus_logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "game_backend.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("game_backend")

app = Flask(__name__)
lock = threading.Lock()


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            meta TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT,
            event TEXT,
            payload TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS crashes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT,
            stacktrace TEXT,
            device_info TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lobbies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id TEXT UNIQUE,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lobby_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id TEXT NOT NULL,
            player_id TEXT NOT NULL,
            joined_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _default_flags() -> Dict[str, Any]:
    return {
        "version": 1,
        "flags": {
            "new_ui": True,
            "reduced_fx": False,
            "double_rewards": False,
            "experimental_netcode": False,
        },
    }


def _load_flags() -> Dict[str, Any]:
    if not FLAGS_PATH.exists():
        FLAGS_PATH.write_text(json.dumps(_default_flags(), indent=2), encoding="utf-8")
    try:
        return json.loads(FLAGS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.error("feature flags JSON invalid; restoring defaults")
        FLAGS_PATH.write_text(json.dumps(_default_flags(), indent=2), encoding="utf-8")
        return _default_flags()


def _variant_for_player(player_id: str) -> str:
    return "A" if (hash(player_id) % 2 == 0) else "B"


@app.route("/health")
def health():
    return jsonify({"status": "ok", "ts": datetime.utcnow().isoformat()})


@app.route("/leaderboard/submit", methods=["POST"])
def submit_score():
    payload = request.json or {}
    player_id = payload.get("player_id")
    score = payload.get("score")
    meta = payload.get("meta", {})
    if not player_id or score is None:
        return jsonify({"error": "player_id and score required"}), 400
    with lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO leaderboard (player_id, score, meta, created_at) VALUES (?, ?, ?, ?)",
            (player_id, int(score), json.dumps(meta), datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    return jsonify({"status": "ok"})


@app.route("/leaderboard/top")
def top_scores():
    limit = int(request.args.get("limit", 50))
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT player_id, score, meta, created_at FROM leaderboard ORDER BY score DESC LIMIT ?",
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({"top": rows})


@app.route("/telemetry", methods=["POST"])
def telemetry():
    payload = request.json or {}
    player_id = payload.get("player_id")
    event = payload.get("event")
    data = payload.get("payload", {})
    if not event:
        return jsonify({"error": "event required"}), 400
    with lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO telemetry (player_id, event, payload, created_at) VALUES (?, ?, ?, ?)",
            (player_id, event, json.dumps(data), datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    return jsonify({"status": "ok"})


@app.route("/crash", methods=["POST"])
def crash():
    payload = request.json or {}
    player_id = payload.get("player_id")
    stacktrace = payload.get("stacktrace")
    device_info = payload.get("device_info", {})
    if not stacktrace:
        return jsonify({"error": "stacktrace required"}), 400
    with lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO crashes (player_id, stacktrace, device_info, created_at) VALUES (?, ?, ?, ?)",
            (
                player_id,
                stacktrace,
                json.dumps(device_info),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()
    return jsonify({"status": "ok"})


@app.route("/feature-flags")
def feature_flags():
    return jsonify(_load_flags())


@app.route("/ab-variant")
def ab_variant():
    player_id = request.args.get("player_id", "guest")
    variant = _variant_for_player(player_id)
    return jsonify({"variant": variant})


@app.route("/lobby/create", methods=["POST"])
def lobby_create():
    payload = request.json or {}
    lobby_id = payload.get("lobby_id") or f"lobby-{int(time.time()*1000)}"
    with lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO lobbies (lobby_id, created_at) VALUES (?, ?)",
            (lobby_id, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    return jsonify({"lobby_id": lobby_id})


@app.route("/lobby/join", methods=["POST"])
def lobby_join():
    payload = request.json or {}
    lobby_id = payload.get("lobby_id")
    player_id = payload.get("player_id")
    if not lobby_id or not player_id:
        return jsonify({"error": "lobby_id and player_id required"}), 400
    with lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lobby_members (lobby_id, player_id, joined_at) VALUES (?, ?, ?)",
            (lobby_id, player_id, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    return jsonify({"status": "ok"})


@app.route("/lobby/state")
def lobby_state():
    lobby_id = request.args.get("lobby_id")
    if not lobby_id:
        return jsonify({"error": "lobby_id required"}), 400
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT player_id, joined_at FROM lobby_members WHERE lobby_id = ? ORDER BY joined_at",
        (lobby_id,),
    )
    members = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({"lobby_id": lobby_id, "members": members})


@app.route("/stats")
def stats():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM leaderboard")
    scores = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM telemetry")
    telemetry_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM crashes")
    crash_count = cur.fetchone()[0]
    conn.close()
    return jsonify(
        {"scores": scores, "telemetry": telemetry_count, "crashes": crash_count}
    )


if __name__ == "__main__":
    _init_db()
    logger.info("Starting NEXUS Game Backend on 0.0.0.0:7000")
    app.run(host="0.0.0.0", port=7000)
