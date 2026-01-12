#!/usr/bin/env python3
"""
Human Interface Agent (Windows)
- CPU-aware throttling
- Safe GUI automation demo (Notepad typing)
- VS Code workspace opening if available
- Logs interactions to nexus_logs/human_agent.log
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path

try:
    import pyautogui
except Exception as e:
    pyautogui = None

try:
    import psutil
except Exception as e:
    psutil = None

LOG_DIR = Path("nexus_logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "human_agent.log"

WORKSPACE = Path.cwd()

CPU_HIGH_THRESHOLD = 60.0  # percent
CPU_SLEEP_SEC = 1.5

















def log(event, data=None):
    payload = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "data": data or {}
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    print(f"[LOG] {event}: {data or ''}")

















def cpu_throttle():
    if psutil is None:
        return
    try:
        usage = psutil.cpu_percent(interval=0.3)
        if usage >= CPU_HIGH_THRESHOLD:
            log("cpu_throttle", {"usage": usage})
            time.sleep(CPU_SLEEP_SEC)
    except Exception:
        pass

















def find_app_paths():
    paths = {}
    # VS Code
    code_exe = Path(os.environ.get("LocalAppData", "")) / "Programs" / "Microsoft VS Code" / "Code.exe"
    if code_exe.exists():
        paths["vscode"] = str(code_exe)
    # Notepad (system default)
    paths["notepad"] = "notepad.exe"
    return paths

















def launch_app(path, args=None):
    cpu_throttle()
    cmd = [path] + (args or [])
    log("launch_app", {"cmd": cmd})
    try:
        return subprocess.Popen(cmd)
    except Exception as e:
        log("launch_failed", {"error": str(e), "cmd": cmd})
        return None

















def demo_notepad_typing():
    log("demo_notepad_start")
    paths = find_app_paths()
    if "notepad" not in paths:
        log("notepad_missing")
        return False
    proc = launch_app(paths["notepad"], [])
    if proc is None:
        return False
    time.sleep(1.2)
    cpu_throttle()
    if pyautogui is None:
        log("pyautogui_missing", {"tip": "pip install pyautogui pillow"})
        return False
    try:
        pyautogui.typewrite("NEXUS-ONE Human Interface Agent demo\n", interval=0.02)
        pyautogui.typewrite(f"Workspace: {WORKSPACE}\n", interval=0.02)
        pyautogui.typewrite("This text was typed programmatically (safe demo).\n", interval=0.02)
        time.sleep(0.3)
        # Save file via Ctrl+S
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.5)
        save_path = str(WORKSPACE / "nexus_logs" / "human_agent_demo.txt")
        pyautogui.typewrite(save_path, interval=0.01)
        time.sleep(0.3)
        pyautogui.press("enter")
        log("demo_notepad_saved", {"path": save_path})
        time.sleep(0.5)
        # Close Notepad via Alt+F4
        pyautogui.hotkey("alt", "f4")
        log("demo_notepad_done")
        return True
    except Exception as e:
        log("demo_notepad_error", {"error": str(e)})
        return False

















def open_vscode_workspace():
    log("open_vscode_workspace")
    paths = find_app_paths()
    if "vscode" in paths:
        return launch_app(paths["vscode"], [str(WORKSPACE)]) is not None
    # Fallback to code CLI if on PATH
    try:
        return launch_app("code", [str(WORKSPACE)]) is not None
    except Exception:
        log("vscode_not_found")
        return False

















def main():
    print("\n===========================")
    print("Human Interface Agent Demo")
    print("===========================\n")
    log("agent_start", {"workspace": str(WORKSPACE)})
    ok = demo_notepad_typing()
    log("notepad_demo_result", {"success": ok})
    cpu_throttle()
    opened = open_vscode_workspace()
    log("vscode_open_result", {"success": opened})
    log("agent_end")


if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
    main()
