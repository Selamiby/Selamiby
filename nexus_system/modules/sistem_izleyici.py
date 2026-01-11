# modules/sistem_izleyici.py
import time

import psutil


class SistemIzleyici:
    def __init__(self):
        self.log = []
    
    def calis(self, komut=""):
        durum = {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "islemler": len(psutil.pids()),
            "zaman": time.time()
        }
        
        self.log.append(durum)
        
        # Kaynak sınırlarını kontrol et
        if durum["cpu"] > 80:
            return "⚠️ CPU yüksek! Yavaşlatılıyor..."
        elif durum["ram"] > 85:
            return "⚠️ RAM dolu! Temizlik yapılıyor..."
        else:
            return f"✅ Sistem sağlıklı (CPU: %{durum['cpu']}, RAM: %{durum['ram']})"
