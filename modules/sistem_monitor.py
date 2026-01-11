# modules/sistem_monitor.py
import time

import psutil


class SistemMonitor:
    def __init__(self):
        self.log = []
        print("📊 SİSTEM MONİTÖR AKTİF")
    
    def kontrol_et(self):
        """Sistem durumunu kontrol et"""
        veri = {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("C:").percent,
            "ag_giden": psutil.net_io_counters().bytes_sent,
            "ag_gelen": psutil.net_io_counters().bytes_recv,
            "zaman": time.time(),
            "calisma_suresi": time.time() - psutil.boot_time()
        }
        
        self.log.append(veri)
        
        # Son 10 kaydı tut
        if len(self.log) > 10:
            self.log = self.log[-10:]
        
        return veri
    
    def rapor_olustur(self):
        """Sistem raporu oluştur"""
        if not self.log:
            return "Henüz veri yok"
        
        son = self.log[-1]
        
        rapor = f"""
📈 SİSTEM RAPORU
════════════════════
• CPU Kullanımı: %{son['cpu']:.1f}
• RAM Kullanımı: %{son['ram']:.1f}
• Disk Kullanımı: %{son['disk']:.1f}
• Çalışma Süresi: {son['calisma_suresi']/3600:.1f} saat
"""
        
        # Uyarılar
        if son['cpu'] > 80:
            rapor += "⚠️  CPU YÜKSEK!\n"
        if son['ram'] > 85:
            rapor += "⚠️  RAM DOLU!\n"
        if son['disk'] > 90:
            rapor += "⚠️  DISK DOLU!\n"
        
        return rapor
    
    def calis(self, gorev=""):
        return self.rapor_olustur()