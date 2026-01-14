import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import os
import subprocess
import time
from pathlib import Path

import requests


class NexusGuardian:
    """
    NEXUS OTOMATİK KORUYUCU v4.0
    Panelin düşmesini (boş sayfa) engeller ve çökme durumunda otomatik iyileştirir.
    """
    def __init__(self, target_url="http://127.0.0.1:8501"):
        self.target_url = target_url
        self.retry_count = 0

    def is_dashboard_alive(self):
        try:
            response = requests.get(self.target_url, timeout=5)
            # Streamlit başlangıçta bazen 200 döner ama içerik boştur
            if response.status_code == 200 and "Streamlit" in response.text:
                return True
            return False
        except:
            return False

    def restart_dashboard(self):
        print("🚨 PANEL ÇÖKTÜ VEYA ERİŞİLEMEZ! OTOMATİK KURTARMA BAŞLATILIYOR...")
        # Önce portu temizle
        os.system("taskkill /F /IM streamlit.exe /T")
        time.sleep(2)

        # Dashboard'u yeniden başlat
        subprocess.Popen(["streamlit", "run", "nexus_dashboard_v3.py", "--server.port", "8501", "--server.address", "127.0.0.1"])
        print("✅ PANEL YENİDEN BAŞLATILDI. STABİLİTE BEKLENİYOR.")

    def watch(self):
        print(f"🛡️ NEXUS KORUYUCU AKTİF: {self.target_url} izleniyor...")
        while True:
            if not self.is_dashboard_alive():
                self.retry_count += 1
                if self.retry_count > 2: # 2 kez üst üste başarısız olursa
                    self.restart_dashboard()
                    self.retry_count = 0
            else:
                self.retry_count = 0 # Her şey yolundaysa sıfırla

            time.sleep(10) # 10 saniyede bir kontrol et

if __name__ == "__main__":
    guardian = NexusGuardian()
    guardian.watch()
