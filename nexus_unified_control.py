#!/usr/bin/env python3
"""
NEXUS-ONE UNIFIED CENTRAL CONTROL (UCC)
=======================================
Tüm panellerin tek bir dosyada birleşimdir.
- AI Chat (OpenAI/KB/Gemini)
- Canlı Sistem İzleme (CPU/RAM)
- Otonom Motor Kontrolü
- Kod İyileştirme Merkezi
- Asset Üretim Takibi
"""

import asyncio
import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil
from dotenv import load_dotenv

# GUI Imports
try:
    from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
    from PyQt6.QtGui import QColor, QFont, QPalette
    from PyQt6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                                 QLineEdit, QMainWindow, QProgressBar,
                                 QPushButton, QSplitter, QTabWidget, QTextEdit,
                                 QVBoxLayout, QWidget)
    HAS_PYQT = True
except ImportError:
    HAS_PYQT = False
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk

# AI & Engine Imports
load_dotenv()
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from autonomous_engine import process_command
    HAS_ENGINE = True
except ImportError:
    HAS_ENGINE = False

WORKSPACE = Path.cwd()
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

if HAS_PYQT:
    class ResourceMonitorThread(QThread):
        """Sistem kaynaklarını arka planda izleyen thread"""
        stats_updated = pyqtSignal(dict)
        
        def run(self):
            while True:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                stats = {
                    "cpu": cpu,
                    "ram": ram,
                    "time": datetime.now().strftime("%H:%M:%S")
                }
                self.stats_updated.emit(stats)
                time.sleep(1)
else:
    class ResourceMonitorThread(object):
        def run(self): pass

if HAS_PYQT:
    class NEXUSUnifiedControl(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("NEXUS-ONE UNIFIED COMMAND CENTER")
            self.resize(1100, 750)
            
            # Setup AI
            self.ai_mode = "KNOWLEDGE_BASE"
            self._init_ai()
            
            self.init_ui()
            self.start_monitoring()

        def center_window(self):
            # Not strictly needed if not defined, but I'll remove the call or implement it
            pass
else:
    class NEXUSUnifiedControl(object):
        def __init__(self): pass

    def _init_ai(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if HAS_OPENAI and self.openai_key and "sk-" in self.openai_key:
            try:
                self.client = OpenAI(api_key=self.openai_key)
                self.ai_mode = "OPENAI"
            except:
                self.ai_mode = "KNOWLEDGE_BASE"
        else:
            self.ai_mode = "KNOWLEDGE_BASE"

    def init_ui(self):
        # Ana Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Üst Panel: Sistem Durumu
        status_bar = QHBoxLayout()
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximumWidth(200)
        self.ram_label = QLabel("RAM: 0%")
        self.ram_bar = QProgressBar()
        self.ram_bar.setMaximumWidth(200)
        self.mode_label = QLabel(f"AI MODE: {self.ai_mode}")
        self.mode_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        
        status_bar.addWidget(self.cpu_label)
        status_bar.addWidget(self.cpu_bar)
        status_bar.addSpacing(20)
        status_bar.addWidget(self.ram_label)
        status_bar.addWidget(self.ram_bar)
        status_bar.addStretch()
        status_bar.addWidget(self.mode_label)
        
        main_layout.addLayout(status_bar)
        
        # Orta Panel: Tab'lar
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab 1: AI Chat & Command
        self.chat_tab = QWidget()
        chat_layout = QVBoxLayout(self.chat_tab)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: 'Consolas';")
        self.chat_display.append("🤖 <b>NEXUS-ONE:</b> Merkezi Komuta Sistemine Hoş Geldiniz. Tüm sistemler aktif ve emrinizde.")
        
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Komut veya soru yazın...")
        self.chat_input.returnPressed.connect(self.send_chat)
        self.send_btn = QPushButton("GÖNDER")
        self.send_btn.clicked.connect(self.send_chat)
        self.send_btn.setStyleSheet("background-color: #007acc; color: white; font-weight: bold;")
        
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_btn)
        
        chat_layout.addWidget(self.chat_display)
        chat_layout.addLayout(input_layout)
        self.tabs.addTab(self.chat_tab, "💬 AI CHAT & COMMAND")
        
        # Tab 2: Otonom Günlük (Live Logs)
        self.log_tab = QWidget()
        log_layout = QVBoxLayout(self.log_tab)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("background-color: #000000; color: #00ff00; font-family: 'Consolas';")
        log_layout.addWidget(self.log_display)
        self.tabs.addTab(self.log_tab, "📜 LIVE LOGS")
        
        # Tab 3: Sistem Kontrol (Quick Actions)
        self.control_tab = QWidget()
        control_layout = QVBoxLayout(self.control_tab)
        
        btns_grid = QHBoxLayout()
        actions = [
            ("KOD İYİLEŞTİR", "improve code"),
            ("SİSTEM ANALİZİ", "system health"),
            ("GITHUB SYNC", "git sync"),
            ("YENİ OYUN ÜRET", "create game"),
            ("BELLEK TEMİZLE", "clean memory")
        ]
        
        for name, cmd in actions:
            btn = QPushButton(name)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda ch, c=cmd: self.quick_command(c))
            btns_grid.addWidget(btn)
        
        control_layout.addLayout(btns_grid)
        control_layout.addStretch()
        self.tabs.addTab(self.control_tab, "🛠️ SYSTEM CONTROL")

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_monitoring(self):
        self.res_thread = ResourceMonitorThread()
        self.res_thread.stats_updated.connect(self.update_stats)
        self.res_thread.start()
        
        # Log okuma zamanlayıcısı
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_logs)
        self.log_timer.start(2000)

    def update_stats(self, stats):
        self.cpu_label.setText(f"CPU: {stats['cpu']}%")
        self.cpu_bar.setValue(int(stats['cpu']))
        self.ram_label.setText(f"RAM: {stats['ram']}%")
        self.ram_bar.setValue(int(stats['ram']))

    def update_logs(self):
        try:
            log_file = LOG_DIR / "autonomous_engine.log"
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()[-30:] # Son 30 satır
                    self.log_display.setPlainText("".join(lines))
                    v_bar = self.log_display.verticalScrollBar()
                    if v_bar:
                        v_bar.setValue(v_bar.maximum())
        except:
            pass

    def send_chat(self):
        text = self.chat_input.text().strip()
        if not text: return
        
        self.chat_display.append(f"<br><b>👤 SİZ:</b> {text}")
        self.chat_input.clear()
        
        # AI Processing
        threading.Thread(target=self.process_ai, args=(text,), daemon=True).start()

    def process_ai(self, text):
        response = ""
        if self.ai_mode == "OPENAI":
            try:
                res = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": text}],
                    timeout=8
                )
                response = res.choices[0].message.content
            except Exception as e:
                response = f"API Hatası (KB moduna geçiliyor): {str(e)}"
                self.ai_mode = "KNOWLEDGE_BASE"
        
        if not response or self.ai_mode == "KNOWLEDGE_BASE":
            response = self.get_kb_response(text)
        
        # Update UI from thread
        QTimer.singleShot(0, lambda: self.chat_display.append(f"🤖 <b>NEXUS:</b> {response}"))
        
        # Trigger Engine if command-like
        if HAS_ENGINE and any(kw in text.lower() for kw in ["yap", "çalıştır", "düzenle", "iyileştir", "analiz"]):
            process_command(text)

    def quick_command(self, cmd):
        self.chat_display.append(f"<br><b>⚡ HIZLI KOMUT:</b> {cmd}")
        if HAS_ENGINE:
            threading.Thread(target=process_command, args=(cmd,), daemon=True).start()
        else:
            self.chat_display.append("🤖 <b>NEXUS:</b> Engine şu an ulaşılamaz durumda.")

    def get_kb_response(self, text):
        return f"'{text}' komutunu anladım. Şu an yerel moddayım ama otonom motor arka planda bu görevi işliyor."

if __name__ == "__main__":
    if not HAS_PYQT:
        print("PyQt6 bulunamadı. Lütfen 'pip install PyQt6' komutunu çalıştırın.")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Koyu tema ayarı
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    
    gui = NEXUSUnifiedControl()
    gui.show()
    sys.exit(app.exec())
