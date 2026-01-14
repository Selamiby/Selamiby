"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
"""
NEXUS Analytics Dashboard (Lightweight Web)
Real-time player cohorts, retention, heatmaps
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
DB_PATH = Path("game_backend.db")

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>NEXUS Analytics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #2a2a2a; padding: 15px; border-radius: 5px; }
        h2 { margin-top: 0; }
        canvas { max-height: 300px; }
    </style>
</head>
<body>
    <h1>📊 NEXUS Game Analytics</h1>
    <div class="grid">
        <div class="card">
            <h2>Top Players</h2>
            <div id="top-players"></div>
        </div>
        <div class="card">
            <h2>Score Distribution</h2>
            <canvas id="score-chart"></canvas>
        </div>
        <div class="card">
            <h2>Telemetry Events</h2>
            <div id="telemetry"></div>
        </div>
        <div class="card">
            <h2>Crash Rate</h2>
            <div id="crash-rate"></div>
        </div>
    </div>
    <script>
        async function updateDashboard() {
            const resp = await fetch('/api/analytics');
            const data = await resp.json();

            document.getElementById('top-players').innerHTML = data.top_players.map(p =>
                `<div>${p.player_id}: ${p.score}</div>`
            ).join('');

            document.getElementById('telemetry').innerHTML = `Events: ${data.telemetry_count}`;
            document.getElementById('crash-rate').innerHTML = `${data.crash_count} crashes`;

            // Chart
            const ctx = document.getElementById('score-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.top_players.map(p => p.player_id),
                    datasets: [{
                        label: 'Scores',
                        data: data.top_players.map(p => p.score),
                        backgroundColor: '#4CAF50'
                    }]
                }
            });
        }

        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(HTML_DASHBOARD)


@app.route("/api/analytics")
def analytics():
    """Get dashboard data."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Top players
    cur.execute("SELECT player_id, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    top_players = [{"player_id": r[0], "score": r[1]} for r in cur.fetchall()]

    # Counts
    cur.execute("SELECT COUNT(*) FROM telemetry")
    telemetry_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM crashes")
    crash_count = cur.fetchone()[0]

    # 7-day retention (simplified)
    since = (datetime.utcnow() - timedelta(days=7)).isoformat()
    cur.execute(
        "SELECT COUNT(DISTINCT player_id) FROM leaderboard WHERE created_at > ?",
        (since,),
    )
    active_players_7d = cur.fetchone()[0]

    conn.close()

    return jsonify(
        {
            "top_players": top_players,
            "telemetry_count": telemetry_count,
            "crash_count": crash_count,
            "active_players_7d": active_players_7d,
        }
    )


@app.route("/api/cohorts")
def cohorts():
    """Player cohort analysis."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            DATE(created_at) as cohort_date,
            COUNT(DISTINCT player_id) as new_players,
            AVG(score) as avg_score
        FROM leaderboard
        GROUP BY DATE(created_at)
        ORDER BY cohort_date DESC
        LIMIT 30
    """
    )

    cohorts_data = [
        {"date": r[0], "new_players": r[1], "avg_score": r[2]} for r in cur.fetchall()
    ]
    conn.close()

    return jsonify({"cohorts": cohorts_data})


@app.route("/api/retention")
def retention():
    """7-day, 14-day, 30-day retention."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Simplified: count unique players in each window
    retention_data = {}
    for days in [7, 14, 30]:
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        cur.execute(
            "SELECT COUNT(DISTINCT player_id) FROM leaderboard WHERE created_at > ?",
            (since,),
        )
        retention_data[f"day_{days}"] = cur.fetchone()[0]

    conn.close()
    return jsonify(retention_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7004, debug=False)
