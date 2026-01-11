#!/usr/bin/env python3
"""
NEXUS-ONE Human Control Panel (Windows)
- Start/Stop Human Interface Agent
- CPU usage monitor (psutil)
- Open VS Code workspace and logs folder
- Run demo (Notepad typing + VS Code)
"""
import os
import subprocess
import webbrowser
import sys
import time
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except Exception as e:
    print("Tkinter not available:", e)
    sys.exit(1)

try:
    import psutil
except Exception:
    psutil = None

WORKSPACE = Path.cwd()
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

PYTHON = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python" / "Python311" / "python.exe"
PYTHON = str(PYTHON if PYTHON.exists() else sys.executable)

AGENT_SCRIPT = str(WORKSPACE / "human_interface_agent.py")
RUN_AGENT_PS1 = str(WORKSPACE / "scripts" / "run_control_panel.ps1")
RUNNER_PS1 = str(WORKSPACE / "run_human_agent.ps1")

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS-ONE Control Panel")
        self.geometry("520x360")
        if sys.platform == "win32":
            os.system("chcp 65001 > nul")
        self.create_widgets()
        self.after(1000, self.update_status)

    def create_widgets(self):
        header = ttk.Label(self, text="NEXUS-ONE Human Interface Control", font=("Segoe UI", 12, "bold"))
        header.pack(pady=10)

        # CPU and status frame
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=12, pady=6)

        self.cpu_var = tk.StringVar(value="CPU: -- %")
        self.cpu_label = ttk.Label(status_frame, textvariable=self.cpu_var)
        self.cpu_label.pack(side="left")

        self.agent_var = tk.StringVar(value="Agent: STOPPED")
        ttk.Label(status_frame, textvariable=self.agent_var).pack(side="right")

        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", padx=12, pady=6)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=12, pady=6)

        ttk.Button(btn_frame, text="Run Demo", command=self.run_demo).grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Start Agent", command=self.start_agent).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Stop Agent", command=self.stop_agent).grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        ttk.Button(btn_frame, text="Open VS Code", command=self.open_vscode).grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Open Logs", command=self.open_logs).grid(row=1, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Open Workspace", command=self.open_workspace).grid(row=1, column=2, padx=6, pady=6, sticky="ew")

        # Row 2: VS Code actions
        ttk.Button(btn_frame, text="Open Search UI", command=self.vscode_search_ui).grid(row=2, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Format Python (black)", command=self.format_python).grid(row=2, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Start Task Queue", command=self.start_task_queue).grid(row=2, column=2, padx=6, pady=6, sticky="ew")

        # Row 3: Safe browser automation
        browser_frame = ttk.Frame(self)
        browser_frame.pack(fill="x", padx=12, pady=6)
        ttk.Label(browser_frame, text="Safe Browser (Whitelist)").grid(row=0, column=0, sticky="w")
        self.domain_var = tk.StringVar(value="https://github.com/Selamiby/Selamiby")
        domain_box = ttk.Combobox(browser_frame, textvariable=self.domain_var, values=[
            "https://github.com/Selamiby/Selamiby",
            "https://docs.python.org/",
            "https://code.visualstudio.com/",
            "https://www.microsoft.com/"
        ], state="readonly")
        domain_box.grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(browser_frame, text="Open", command=self.open_whitelisted_domain).grid(row=0, column=2, padx=6)
        browser_frame.grid_columnconfigure(1, weight=1)

        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

        # Log viewer (tail)
        self.log_text = tk.Text(self, height=10, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=12, pady=6)
        self.refresh_logs()

    def update_status(self):
        # CPU
        if psutil:
            try:
                cpu = psutil.cpu_percent(interval=0.2)
                self.cpu_var.set(f"CPU: {cpu:.1f} %")
            except Exception:
                self.cpu_var.set("CPU: n/a")
        else:
            self.cpu_var.set("CPU: n/a")

        # Agent status
        running = self.find_agent_pids()
        self.agent_var.set("Agent: RUNNING" if running else "Agent: STOPPED")

        # Refresh logs periodically
        self.refresh_logs()

        self.after(1500, self.update_status)

    def find_agent_pids(self):
        pids = []
        if not psutil:
            return pids
        try:
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmd = " ".join(p.info.get('cmdline') or [])
                if 'human_interface_agent.py' in cmd:
                    pids.append(p.info['pid'])
        except Exception:
            pass
        return pids

    def run_demo(self):
        try:
            subprocess.Popen([PYTHON, AGENT_SCRIPT])
            messagebox.showinfo("Demo", "Demo başlatıldı (Notepad + VS Code)")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def start_agent(self):
        # Prefer PowerShell runner if exists
        if Path(RUNNER_PS1).exists():
            try:
                subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", RUNNER_PS1])
                messagebox.showinfo("Agent", "Agent başlatıldı (BelowNormal)")
                return
            except Exception:
                pass
        # Fallback direct start
        try:
            subprocess.Popen([PYTHON, AGENT_SCRIPT])
            messagebox.showinfo("Agent", "Agent doğrudan başlatıldı")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def stop_agent(self):
        if not psutil:
            messagebox.showwarning("Uyarı", "psutil yok, durdurma yapılamadı")
            return
        pids = self.find_agent_pids()
        count = 0
        for pid in pids:
            try:
                p = psutil.Process(pid)
                p.terminate()
                count += 1
            except Exception:
                pass
        messagebox.showinfo("Agent", f"Durdurulan süreçler: {count}")

    def open_vscode(self):
        code_exe = Path(os.environ.get("LocalAppData", "")) / "Programs" / "Microsoft VS Code" / "Code.exe"
        cmd = [str(code_exe), str(WORKSPACE)] if code_exe.exists() else ["code", str(WORKSPACE)]
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def vscode_search_ui(self):
        # Opens VS Code and shows Search UI (workbench.action.findInFiles)
        code_exe = Path(os.environ.get("LocalAppData", "")) / "Programs" / "Microsoft VS Code" / "Code.exe"
        cmd = [str(code_exe), str(WORKSPACE)] if code_exe.exists() else ["code", str(WORKSPACE)]
        try:
            subprocess.Popen(cmd)
            messagebox.showinfo("VS Code", "Search UI açmak için Ctrl+Shift+F kullanın")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def open_logs(self):
        try:
            subprocess.Popen(["explorer", str(LOG_DIR)])
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def open_workspace(self):
        try:
            subprocess.Popen(["explorer", str(WORKSPACE)])
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def open_whitelisted_domain(self):
        url = self.domain_var.get()
        whitelist = {
            "https://github.com/Selamiby/Selamiby",
            "https://docs.python.org/",
            "https://code.visualstudio.com/",
            "https://www.microsoft.com/"
        }
        if url not in whitelist:
            messagebox.showwarning("Uyarı", "Domain whitelist dışında")
            return
        try:
            webbrowser.open(url)
            messagebox.showinfo("Browser", f"Açıldı: {url}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def format_python(self):
        try:
            subprocess.Popen([sys.executable, "-m", "black", str(WORKSPACE)])
            messagebox.showinfo("Format", "Python dosyaları (black) formatlanıyor")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def start_task_queue(self):
        runner = Path(WORKSPACE / "scripts" / "run_task_queue.ps1")
        if not runner.exists():
            messagebox.showerror("Hata", "run_task_queue.ps1 bulunamadı")
            return
        try:
            subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(runner)])
            messagebox.showinfo("Task Queue", "Görev kuyruğu başlatıldı")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def refresh_logs(self):
        log_file = LOG_DIR / "human_agent.log"
        if not log_file.exists():
            return
        try:
            text = log_file.read_text(encoding="utf-8")
            # Show only last ~200 lines
            lines = text.splitlines()[-200:]
            content = "\n".join(lines)
            self.log_text.delete("1.0", tk.END)
            self.log_text.insert(tk.END, content)
        except Exception:
            pass


def main():
    app = ControlPanel()
    app.mainloop()

if __name__ == "__main__":
    main()
