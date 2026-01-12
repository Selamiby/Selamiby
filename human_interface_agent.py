#!/usr/bin/env python3
"""
Human Interface Agent (Windows)
- CPU-aware throttling
- Safe GUI automation demo (Notepad typing)
- VS Code workspace opening if available
- Logs interactions to nexus_logs/human_agent.log
"""
import json
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext

try:
    from autonomous_engine import process_command
except ImportError:
    # Fallback if autonomous_engine.py is not found or has issues
    def process_command(command_text):
        print(
            f"FALLBACK: Received command '{command_text}', but autonomous_engine could not be loaded."
        )
        messagebox.showwarning(
            "Engine Not Found",
            "The autonomous_engine.py module could not be loaded.\n"
            "Please ensure it is in the same directory.\n"
            f"Command '{command_text}' was printed to the console instead.",
        )


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
        "data": data or {},
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
    code_exe = (
        Path(os.environ.get("LocalAppData", ""))
        / "Programs"
        / "Microsoft VS Code"
        / "Code.exe"
    )
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
        pyautogui.typewrite(
            "This text was typed programmatically (safe demo).\n", interval=0.02
        )
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


def create_command_window():
    """Creates and runs the Tkinter GUI for command input."""
    log("create_command_window")

    def execute_task():
        command_text = text_area.get("1.0", tk.END).strip()
        if not command_text:
            messagebox.showinfo("Empty Command", "Please enter a task description.")
            return

        log("execute_task_button_clicked", {"command": command_text})
        # Disable button to prevent multiple clicks
        start_button.config(state=tk.DISABLED, text="Processing...")

        # Run the command processing in a separate thread to keep the GUI responsive
        def task_thread():
            try:
                # Call the core processing function from the autonomous engine
                process_command(command_text)
                messagebox.showinfo(
                    "Task Complete",
                    f"Task '{command_text[:30]}...' has been processed.",
                )
            except Exception as e:
                log("task_execution_error", {"error": str(e)})
                messagebox.showerror(
                    "Error", f"An error occurred while processing the task:\n{e}"
                )
            finally:
                # Re-enable the button on the main thread
                window.after(
                    0, lambda: start_button.config(state=tk.NORMAL, text="Start Task")
                )

        threading.Thread(target=task_thread, daemon=True).start()

    window = tk.Tk()
    window.title("NEXUS-ONE Command Console")
    window.geometry("600x400")

    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(main_frame, text="Enter task for NEXUS-ONE:", font=("Arial", 12))
    label.pack(pady=(0, 5))

    text_area = scrolledtext.ScrolledText(
        main_frame, wrap=tk.WORD, height=15, font=("Arial", 10)
    )
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.focus()

    start_button = tk.Button(
        main_frame,
        text="Start Task",
        command=execute_task,
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
    )
    start_button.pack(pady=(10, 0), fill=tk.X)

    log("gui_initialized")
    window.mainloop()
    log("gui_closed")


def main():
    print("\n===========================")
    print("Human Interface Agent")
    print("===========================\n")
    log("agent_start", {"workspace": str(WORKSPACE)})

    # Launch the command window as the primary interface
    create_command_window()

    # Optional: Keep old demo functions for testing if needed, but they won't run by default.
    # ok = demo_notepad_typing()
    # log("notepad_demo_result", {"success": ok})
    # cpu_throttle()
    # opened = open_vscode_workspace()
    # log("vscode_open_result", {"success": opened})

    log("agent_end")


if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
    main()
