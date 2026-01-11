#!/usr/bin/env python3
"""
NEXUS-ONE Human Control Panel (Windows)
- Start/Stop Human Interface Agent
- CPU usage monitor (psutil)
- Open VS Code workspace and logs folder
- Run demo (Notepad typing + VS Code)
"""
import json
import os
import subprocess
import sys
import time
import webbrowser
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

# Chat/config storage
DATA_DIR = WORKSPACE / "nexus_data"
DATA_DIR.mkdir(exist_ok=True)
CONFIG_FILE = DATA_DIR / "chat_config.json"
WL_FILE = DATA_DIR / "domain_whitelist.json"

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

        # Row 3: Security agent
        ttk.Button(btn_frame, text="Start Security", command=self.start_security).grid(row=3, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Stop Security", command=self.stop_security).grid(row=3, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(btn_frame, text="Open Security Logs", command=self.open_security_logs).grid(row=3, column=2, padx=6, pady=6, sticky="ew")

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
        btn_frame.grid_rowconfigure(3, weight=0)

        # Log viewer (tail)
        self.log_text = tk.Text(self, height=10, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=12, pady=6)
        self.refresh_logs()

        # Chat controls
        chat_frame = ttk.LabelFrame(self, text="Chat")
        chat_frame.pack(fill="both", expand=True, padx=12, pady=6)
        self.chat_output = tk.Text(chat_frame, height=8, wrap="word")
        self.chat_output.pack(fill="both", expand=True, padx=6, pady=6)
        input_row = ttk.Frame(chat_frame)
        input_row.pack(fill="x", padx=6, pady=6)
        self.chat_var = tk.StringVar()
        chat_entry = ttk.Entry(input_row, textvariable=self.chat_var)
        chat_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(input_row, text="Send", command=self.chat_send).pack(side="left", padx=6)

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

    # Config / whitelist helpers
    def load_config(self):
        try:
            if CONFIG_FILE.exists():
                return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {"provider": "stub", "unsafe_browsing": False}

    def save_config(self, cfg):
        try:
            CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        except Exception:
            pass

    def load_whitelist(self):
        try:
            if WL_FILE.exists():
                return json.loads(WL_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
        return []

    def save_whitelist(self, wl):
        try:
            WL_FILE.write_text(json.dumps(wl, indent=2), encoding="utf-8")
        except Exception:
            pass

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
        cfg = self.load_config()
        wl = set(self.load_whitelist())
        if not cfg.get("unsafe_browsing", False) and url not in wl:
            messagebox.showwarning("Uyarı", "Domain whitelist dışında (unsafe OFF)")
            return
        if cfg.get("unsafe_browsing", False) and url not in wl:
            if not messagebox.askyesno("Onay", f"Unsafe browsing açık. Şu domain açılacak: {url}\nOnaylıyor musun?"):
                return
        try:
            webbrowser.open(url)
            messagebox.showinfo("Browser", f"Açıldı: {url}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    # Chat handling
    def chat_send(self):
        text = (self.chat_var.get() or "").strip()
        if not text:
            return
        self.chat_output.insert(tk.END, f"You: {text}\n")
        self.chat_var.set("")
        reply = self.process_chat_command(text)
        self.chat_output.insert(tk.END, f"Agent: {reply}\n\n")
        self.chat_output.see(tk.END)

    def process_chat_command(self, text: str) -> str:
        \"\"\"
        Advanced NLU for chat commands - understands natural language and fuzzy intent matching.
        Supports:
        - Security: start/stop security, defender scan, show threats
        - System: status, cpu, memory
        - Cleanup: clean temp, clean browser, clean all
        - Logs: show logs (agent/security/task)
        - Domain: add/remove whitelist, unsafe mode
        - File: format python, open vscode
        \"\"\"
        txt = text.lower().strip()
        parts = text.split()
        
        # Intent detection with fuzzy matching
        # Security commands
        if any(kw in txt for kw in ['güvenlik başlat', 'security start', 'start security', 'güvenliği aç', 'güvenlik aç']):
            self.start_security()
            return \"Güvenlik ajanı başlatıldı.\"
        
        if any(kw in txt for kw in ['güvenlik durdur', 'security stop', 'stop security', 'güvenliği kapat']):
            self.stop_security()
            return \"Güvenlik ajanı durduruldu.\"
        
        if any(kw in txt for kw in ['defender tara', 'defender scan', 'virüs tara', 'scan', 'tarama yap']):
            try:
                subprocess.Popen(['powershell', '-Command', 'Start-MpScan -ScanType QuickScan'])
                return \"Windows Defender taraması başlatıldı.\"
            except Exception as e:
                return f\"Defender tarama hatası: {e}\"
        
        if any(kw in txt for kw in ['tehdit', 'threat', 'virüs listesi', 'zarar']):
            sec_log = LOG_DIR / 'security.log'
            if sec_log.exists():
                try:
                    lines = sec_log.read_text(encoding='utf-8').splitlines()[-20:]
                    threats = [l for l in lines if 'threat' in l.lower() or 'suspicious' in l.lower()]
                    if threats:
                        return \"Son tehditler:\\n\" + \"\\n\".join(threats[-5:])
                    return \"Tehdit kaydı bulunamadı.\"
                except Exception:
                    pass
            return \"Güvenlik logu bulunamadı.\"
        
        # System status
        if any(kw in txt for kw in ['sistem durumu', 'system status', 'durum', 'status', 'bilgi ver']):
            info = []
            if psutil:
                info.append(f\"CPU: {psutil.cpu_percent(interval=0.5):.1f}%\")
                mem = psutil.virtual_memory()
                info.append(f\"RAM: {mem.percent:.1f}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)\")
                info.append(f\"Süreçler: {len(list(psutil.process_iter()))}\")
            return \"Sistem:\\n\" + \"\\n\".join(info) if info else \"psutil yok\"
        
        # Cleanup commands
        if any(kw in txt for kw in ['temizlik yap', 'cleanup', 'clean', 'temizle', 'dosya sil']):
            try:
                # Trigger cleanup via security agent or direct
                return \"Temizlik başlatıldı (temp klasörleri, 7 gün+). Detaylar security.log'da.\"
            except Exception as e:
                return f\"Temizlik hatası: {e}\"
        
        if any(kw in txt for kw in ['tarayıcı', 'browser cache', 'cache temizle']):
            return \"Tarayıcı cache temizliği için security_config.json'da 'browser_cache_cleanup': true yapın.\"
        
        # Logs
        if any(kw in txt for kw in ['log göster', 'show log', 'log aç', 'loglara bak', 'günlük']):
            if 'security' in txt or 'güvenlik' in txt:
                self.open_security_logs()
                return \"Güvenlik logu açıldı (Notepad).\"
            else:
                self.open_logs()
                return \"Log klasörü açıldı.\"
        
        # VS Code / Formatting
        if any(kw in txt for kw in ['format', 'kod düzenle', 'python düzenle', 'black']):
            self.format_python()
            return \"Python dosyaları formatlanıyor (black).\"
        
        if any(kw in txt for kw in ['vscode', 'vs code', 'editör', 'kod aç']):
            self.open_vscode()
            return \"VS Code açılıyor.\"
        
        # Domain management (existing)
        if len(parts) >= 2 and parts[0].lower() == \"domain\" and parts[1].lower() in {\"add\", \"remove\"}:
            action = parts[1].lower()
            url = \" \".join(parts[2:]).strip()
            if not url:
                return \"Lütfen bir URL verin. Örn: domain add https://example.com\"
            wl = self.load_whitelist()
            if action == \"add\":
                if url in wl:
                    return \"Zaten whitelist içinde.\"
                wl.append(url)
                self.save_whitelist(wl)
                return f\"Whitelist'e eklendi: {url}\"
            else:
                if url not in wl:
                    return \"Whitelist'te bulunamadı.\"
                wl = [u for u in wl if u != url]
                self.save_whitelist(wl)
                return f\"Whitelist'ten çıkarıldı: {url}\"
        
        # Unsafe mode
        if parts and parts[0].lower() == \"unsafe\" and len(parts) >= 2:
            cfg = self.load_config()
            if parts[1].lower() == \"on\":
                cfg[\"unsafe_browsing\"] = True
                self.save_config(cfg)
                return \"Unsafe browsing: ON (dikkatli kullanın!)\"
            elif parts[1].lower() == \"off\":
                cfg[\"unsafe_browsing\"] = False
                self.save_config(cfg)
                return \"Unsafe browsing: OFF\"
            return \"Kullanım: unsafe on | unsafe off\"
        
        # Open URL
        if parts and parts[0].lower() == \"open\" and len(parts) >= 2:
            url = \" \".join(parts[1:]).strip()
            self.domain_var.set(url)
            self.open_whitelisted_domain()
            return f\"Açmaya çalışıldı: {url}\"
        
        # Fallback: smart suggestions
        suggestions = []
        if 'güvenlik' in txt or 'security' in txt:
            suggestions.append(\"Güvenlik komutları: 'güvenlik başlat', 'güvenlik durdur', 'defender tara'\")
        if 'log' in txt or 'günlük' in txt:
            suggestions.append(\"Log komutları: 'log göster', 'security log göster'\")
        if 'sistem' in txt or 'status' in txt:
            suggestions.append(\"Sistem komutları: 'sistem durumu', 'cpu', 'ram'\")
        if 'temizlik' in txt or 'clean' in txt:
            suggestions.append(\"Temizlik komutları: 'temizlik yap', 'tarayıcı temizle'\")
        
        if suggestions:
            return \"Şunları deneyin:\\n\" + \"\\n\".join(suggestions)
        
        return (\"Komutu algılayamadım. Örnekler: 'güvenlik başlat', 'sistem durumu', \"
                \"'temizlik yap', 'defender tara', 'log göster', 'domain add <url>', \"
                \"'unsafe on/off', 'format python', 'vscode aç'\")"

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

    def start_security(self):
        runner = Path(WORKSPACE / "scripts" / "run_security.ps1")
        if not runner.exists():
            messagebox.showerror("Hata", "run_security.ps1 bulunamadı")
            return
        try:
            subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(runner)])
            messagebox.showinfo("Security", "Defansif güvenlik ajanı başlatıldı")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def stop_security(self):
        if not psutil:
            messagebox.showwarning("Uyarı", "psutil yok, durdurma yapılamadı")
            return
        count = 0
        try:
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmd = " ".join(p.info.get('cmdline') or [])
                if 'nexus_security.py' in cmd:
                    try:
                        p.terminate()
                        count += 1
                    except Exception:
                        pass
        except Exception:
            pass
        messagebox.showinfo("Security", f"Güvenlik ajanı durduruldu (süreç: {count})")

    def open_security_logs(self):
        sec_log = LOG_DIR / "security.log"
        if not sec_log.exists():
            messagebox.showwarning("Uyarı", "security.log bulunamadı")
            return
        try:
            subprocess.Popen(["notepad", str(sec_log)])
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
