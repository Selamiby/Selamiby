import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:21
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
# """
# NEXUS Advanced Performance Profiler
# - Real-time FPS, draw calls, GC, memory tracking
# - Per-frame metrics + aggregate analytics
# - Threshold alerts + frame budget analysis
# - Web dashboard integration
# """
import json
import logging
import sqlite3
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from flask import Flask, jsonify, request

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "performance_profiler.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("profiler")

app = Flask(__name__)
DB_PATH = Path("perf_metrics.db")
METRICS_BUFFER = deque(maxlen=10000)  # Last 10k frames


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS frame_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            player_id TEXT,
            frame_number INTEGER,
            fps REAL,
            draw_calls INTEGER,
            triangles INTEGER,
            gc_memory_mb INTEGER,
            heap_mb INTEGER,
            cpu_ms REAL,
            gpu_ms REAL,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS performance_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            player_id TEXT,
            alert_type TEXT,
            description TEXT,
            frame_number INTEGER,
            value REAL,
            threshold REAL,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS performance_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            quality TEXT,
            target_fps INTEGER,
            max_draw_calls INTEGER,
            max_triangles INTEGER,
            max_gc_memory_mb INTEGER,
            created_at TEXT NOT NULL
        )
        """
    )

    # Insert default profiles
    cur.execute(
        """
        INSERT OR IGNORE INTO performance_profiles
        (platform, quality, target_fps, max_draw_calls, max_triangles, max_gc_memory_mb, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ("android", "low", 30, 50, 50000, 256, datetime.utcnow().isoformat())
    )
    cur.execute(
        """
        INSERT OR IGNORE INTO performance_profiles
        (platform, quality, target_fps, max_draw_calls, max_triangles, max_gc_memory_mb, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ("ios", "medium", 60, 100, 150000, 512, datetime.utcnow().isoformat())
    )
    cur.execute(
        """
        INSERT OR IGNORE INTO performance_profiles
        (platform, quality, target_fps, max_draw_calls, max_triangles, max_gc_memory_mb, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ("pc", "high", 120, 500, 1000000, 2048, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


class PerformanceMonitor:
    def __init__(self):
        self.session_id = f"session-{int(time.time())}"
        self.frame_number = 0
        self.lock = threading.Lock()

    def record_frame(self, player_id: str, metrics: Dict) -> None:
        """Record per-frame metrics."""
        with self.lock:
            self.frame_number += 1

            frame_data = {
                "session_id": self.session_id,
                "player_id": player_id,
                "frame_number": self.frame_number,
                "fps": metrics.get("fps", 0),
                "draw_calls": metrics.get("draw_calls", 0),
                "triangles": metrics.get("triangles", 0),
                "gc_memory_mb": metrics.get("gc_memory_mb", 0),
                "heap_mb": metrics.get("heap_mb", 0),
                "cpu_ms": metrics.get("cpu_ms", 0.0),
                "gpu_ms": metrics.get("gpu_ms", 0.0),
                "timestamp": datetime.utcnow().isoformat()
            }

            METRICS_BUFFER.append(frame_data)

            # Persist to DB
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO frame_metrics
                (session_id, player_id, frame_number, fps, draw_calls, triangles, gc_memory_mb, heap_mb, cpu_ms, gpu_ms, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.session_id, player_id, self.frame_number,
                    metrics.get("fps"), metrics.get("draw_calls"), metrics.get("triangles"),
                    metrics.get("gc_memory_mb"), metrics.get("heap_mb"),
                    metrics.get("cpu_ms"), metrics.get("gpu_ms"),
                    frame_data["timestamp"]
                )
            )
            conn.commit()
            conn.close()

    def check_thresholds(self, player_id: str, metrics: Dict, platform: str, quality: str) -> List[Dict]:
        """Check if metrics exceed thresholds."""
        alerts = []

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT max_draw_calls, max_triangles, max_gc_memory_mb 
            FROM performance_profiles 
            WHERE platform = ? AND quality = ?
            """,
            (platform, quality)
        )
        profile = cur.fetchone()
        conn.close()

        if not profile:
            return alerts

        max_draw_calls, max_triangles, max_gc = profile

        if metrics.get("draw_calls", 0) > max_draw_calls:
            alerts.append({
                "type": "HIGH_DRAW_CALLS",
                "value": metrics["draw_calls"],
                "threshold": max_draw_calls
            })

        if metrics.get("triangles", 0) > max_triangles:
            alerts.append({
                "type": "HIGH_TRIANGLES",
                "value": metrics["triangles"],
                "threshold": max_triangles
            })

        if metrics.get("gc_memory_mb", 0) > max_gc:
            alerts.append({
                "type": "HIGH_GC_MEMORY",
                "value": metrics["gc_memory_mb"],
                "threshold": max_gc
            })

        # Persist alerts
        if alerts:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            for alert in alerts:
                cur.execute(
                    """
                    INSERT INTO performance_alerts
                    (session_id, player_id, alert_type, description, frame_number, value, threshold, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.session_id, player_id, alert["type"],
                        f"Value {alert['value']} exceeds threshold {alert['threshold']}",
                        self.frame_number, alert["value"], alert["threshold"],
                        datetime.utcnow().isoformat()
                    )
                )
            conn.commit()
            conn.close()

        return alerts


monitor = PerformanceMonitor()


@app.route("/profile/frame", methods=["POST"])
def profile_frame():
    """Ingest frame metrics from game client."""
    payload = request.json or {}
    player_id = payload.get("player_id")
    metrics = payload.get("metrics", {})
    platform = payload.get("platform", "pc")
    quality = payload.get("quality", "high")

    monitor.record_frame(player_id, metrics)
    alerts = monitor.check_thresholds(player_id, metrics, platform, quality)

    if alerts:
        logger.warning(f"⚠️  Performance alerts for {player_id}: {alerts}")

    return jsonify({"status": "ok", "alerts": alerts})


@app.route("/profile/stats")
def profile_stats():
    """Get session performance statistics."""
    if not METRICS_BUFFER:
        return jsonify({"error": "no metrics"}), 400

    metrics_list = list(METRICS_BUFFER)
    fps_values = [m["fps"] for m in metrics_list]
    draw_calls = [m["draw_calls"] for m in metrics_list]
    gc_memory = [m["gc_memory_mb"] for m in metrics_list]

    stats = {
        "session_id": monitor.session_id,
        "total_frames": len(metrics_list),
        "fps": {
            "avg": sum(fps_values) / len(fps_values) if fps_values else 0,
            "min": min(fps_values) if fps_values else 0,
            "max": max(fps_values) if fps_values else 0
        },
        "draw_calls": {
            "avg": sum(draw_calls) / len(draw_calls) if draw_calls else 0,
            "max": max(draw_calls) if draw_calls else 0
        },
        "gc_memory_mb": {
            "avg": sum(gc_memory) / len(gc_memory) if gc_memory else 0,
            "peak": max(gc_memory) if gc_memory else 0
        }
    }

    return jsonify(stats)


@app.route("/profile/health")
def health():
    return jsonify({"status": "ok", "session_id": monitor.session_id, "frames_buffered": len(METRICS_BUFFER)})


if __name__ == "__main__":
    _init_db()
    logger.info("Starting Performance Profiler on 0.0.0.0:7002")
    app.run(host="0.0.0.0", port=7002)
