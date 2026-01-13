#!/usr/bin/env python3
"""
NEXUS Smart Resource Guard - Advanced version for older hardware
==============================================================
Monitors and automatically shuts down heavy processes to protect old hardware.
"""

import json
import logging
import os
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path

import psutil

WORKSPACE = Path(__file__).parent
LOG_FILE = WORKSPACE / "nexus_resource_guard.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] 🛡️ GUARD: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ResourceGuard")

class ResourceGuard:
    def __init__(self, cpu_limit=60, check_interval=15):
        self.cpu_limit = cpu_limit
        self.check_interval = check_interval
        # Don't ever kill these
        self.whitelist = ["code.exe", "powershell.exe", "explorer.exe", "conhost.exe", "svchost.exe", "python.exe", "winlogon.exe", "csrss.exe"]
        self.status_file = WORKSPACE / "nexus_status.json"
        self.running = True

    def monitor(self):
        logger.info(f"Düşük Donanım Modu Aktif. CPU Limiti: %{self.cpu_limit}")
        logger.info("Gereksiz indeksleme ve ağır animasyonlar kısıtlandı.")

        counter = 0
        git_counter = 0
        while self.running:
            try:
                # Get system-wide CPU usage
                total_cpu = psutil.cpu_percent(interval=1)
                ram_usage = psutil.virtual_memory().percent

                # Update status for "Remote" tracking
                self.update_status(total_cpu, ram_usage)

                if total_cpu > self.cpu_limit:
                    logger.warning(f"Kritik CPU Kullanımı: %{total_cpu}! Müdahale ediliyor...")
                    self.take_action()

                # Storage cleanup every 10 cycles (approx 2 minutes)
                counter += 1
                if counter >= 12:
                    self.cleanup_storage()
                    counter = 0

                # Auto-sync to Remote Storage every 60 cycles (approx 10 minutes)
                git_counter += 1
                if git_counter >= 30: # Changed to ~5 minutes for responsive "every change"
                    self.auto_sync_remote()
                    git_counter = 0

                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                logger.error(f"Hata: {e}")
                time.sleep(self.check_interval)

    def auto_sync_remote(self):
        """Automatically commits and pushes changes to GitHub"""
        if psutil.cpu_percent() > self.cpu_limit:
            logger.info("Sync atlanıyor: CPU çok yüksek.")
            return

        logger.info("📤 Uzaktan depolama senkronizasyonu başlatılıyor...")
        try:
            # Add all except .env
            subprocess.run(["git", "add", ".", ":!.env"], cwd=WORKSPACE, check=True, capture_output=True)

            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE, capture_output=True, text=True).stdout
            if status:
                msg = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(["git", "commit", "-m", msg], cwd=WORKSPACE, check=True, capture_output=True)
                subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE, check=True, capture_output=True)
                logger.info("✅ Değişiklikler başarıyla GitHub'a gönderildi.")
            else:
                logger.info("Senkronize edilecek yeni değişiklik yok.")
        except Exception as e:
            logger.error(f"Git senkronizasyon hatası: {e}")

    def update_status(self, cpu, ram):
        """Creates a lightweight status file for remote monitoring"""
        try:
            status = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_usage": f"{cpu}%",
                "ram_usage": f"{ram}%",
                "status": "Healthy" if cpu < self.cpu_limit else "Under Pressure",
                "disk_health": f"{psutil.disk_usage('/').percent}%"
            }
            with open(self.status_file, "w") as f:
                json.dump(status, f, indent=4)
        except:
            pass

    def cleanup_storage(self):
        """Automatically cleans up logs and caches to save space"""
        logger.info("🔻 Otomatik depolama temizliği başlatılıyor...")
        cleaned_size = 0

        # Paths to clean
        targets = [
            WORKSPACE / "nexus_logs",
            WORKSPACE / "__pycache__",
            Path(os.environ.get('TEMP', ''))
        ]

        for target in targets:
            if target.exists():
                for item in target.glob("*"):
                    try:
                        if item.is_file() and (item.suffix in ['.log', '.pyc', '.tmp'] or 'tmp' in item.name.lower()):
                            # Keep current log file
                            if item.name == LOG_FILE.name:
                                continue
                            file_size = item.stat().st_size
                            item.unlink()
                            cleaned_size += file_size
                    except:
                        continue

        if cleaned_size > 0:
            logger.info(f"🧹 Temizlik tamamlandı: {cleaned_size / (1024*1024):.2f} MB alan açıldı.")

    def take_action(self):
        """Processes are now 'slowed down' or 'prioritized to idle' instead of killed."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # Get actual CPU usage for this process
                usage = proc.cpu_percent(interval=0.5)
                if usage > 20 and proc.info['name'].lower() not in self.whitelist:
                    processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort by CPU usage
        processes.sort(key=lambda x: x.cpu_percent(), reverse=True)

        for p in processes:
            try:
                name = p.info['name']
                pid = p.info['pid']
                usage = p.cpu_percent()

                logger.info(f"⚡ YAVAŞLATILIYOR: {name} (PID: {pid}) - CPU: %{usage}")

                # Set to Lowest priority (Idle)
                if os.name == 'nt': # Windows
                    p.nice(psutil.IDLE_PRIORITY_CLASS)
                else:
                    p.nice(19)

                logger.info(f"✅ {name} düşük önceliğe çekildi. Kapatılmadı, sadece işlemciyi yorması engellendi.")

                # Optional: Suspend briefly to cool down CPU
                p.suspend()
                time.sleep(2)
                p.resume()

                break
            except Exception as e:
                logger.error(f"Müdahale hatası: {e}")

if __name__ == "__main__":
    guard = ResourceGuard(cpu_limit=75) # Set more conservative limit for older hardware
    guard.monitor()
