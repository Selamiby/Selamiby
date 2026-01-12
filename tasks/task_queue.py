#!/usr/bin/env python3
"""
NEXUS-ONE Task Queue Runner (CPU-light)
- Reads tasks from nexus_data/task_queue.json
- Supports scheduled and interval tasks
- BelowNormal priority recommended
"""
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    import psutil
except Exception:
    psutil = None

WORKSPACE = Path.cwd()
DATA_DIR = WORKSPACE / "nexus_data"
DATA_DIR.mkdir(exist_ok=True)
QUEUE_FILE = DATA_DIR / "task_queue.json"
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "task_queue.log"

CPU_HIGH = 65.0
SLEEP_SEC = 1.0


def log(event, data=None):
    payload = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "data": data or {},
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    print(f"[LOG] {event}: {data or ''}")


def cpu_ok():
    if not psutil:
        return True
    try:
        return psutil.cpu_percent(interval=0.2) < CPU_HIGH
    except Exception:
        return True


def default_queue():
    return {
        "tasks": [
            {"name": "human_agent_demo", "type": "once", "at": int(time.time()) + 120},
            {"name": "format_python", "type": "interval", "every_sec": 1800},
        ]
    }


def load_queue():
    if not QUEUE_FILE.exists():
        QUEUE_FILE.write_text(json.dumps(default_queue(), indent=2), encoding="utf-8")
    try:
        return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        log("queue_load_error", {"error": str(e)})
        return default_queue()


def run_human_agent_demo():
    log("run_human_agent_demo")
    py = (
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs"
        / "Python"
        / "Python311"
        / "python.exe"
    )
    py = str(py if py.exists() else sys.executable)
    script = str(WORKSPACE / "human_interface_agent.py")
    try:
        subprocess.Popen([py, script])
    except Exception as e:
        log("human_agent_demo_error", {"error": str(e)})


def run_format_python():
    log("run_format_python")
    py = (
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs"
        / "Python"
        / "Python311"
        / "python.exe"
    )
    py = str(py if py.exists() else sys.executable)
    try:
        subprocess.Popen([py, "-m", "black", str(WORKSPACE)])
    except Exception as e:
        log("format_python_error", {"error": str(e)})


TASK_HANDLERS = {
    "human_agent_demo": run_human_agent_demo,
    "format_python": run_format_python,
}


class Scheduler:
    def __init__(self):
        self.queue = load_queue()
        self.last_run = {}
        self.stop_flag = False

    def loop(self):
        log("scheduler_start")
        while not self.stop_flag:
            if not cpu_ok():
                time.sleep(SLEEP_SEC)
                continue
            now = int(time.time())
            for t in list(self.queue.get("tasks", [])):
                name = t.get("name")
                typ = t.get("type")
                if name not in TASK_HANDLERS:
                    continue
                if typ == "once" and now >= int(t.get("at", now + 999999)):
                    try:
                        TASK_HANDLERS[name]()
                        self.queue["tasks"].remove(t)
                        QUEUE_FILE.write_text(
                            json.dumps(self.queue, indent=2), encoding="utf-8"
                        )
                        log("task_once_run", {"name": name})
                    except Exception as e:
                        log("task_once_error", {"name": name, "error": str(e)})
                elif typ == "interval":
                    every = int(t.get("every_sec", 600))
                    last = int(self.last_run.get(name, 0))
                    if now - last >= every:
                        try:
                            TASK_HANDLERS[name]()
                            self.last_run[name] = now
                            log("task_interval_run", {"name": name, "every": every})
                        except Exception as e:
                            log("task_interval_error", {"name": name, "error": str(e)})
            time.sleep(0.5)
        log("scheduler_stop")


def main():
    sched = Scheduler()
    try:
        sched.loop()
    except KeyboardInterrupt:
        sched.stop_flag = True


if __name__ == "__main__":
    main()
