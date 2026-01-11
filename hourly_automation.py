# hourly_automation.py
import os
import subprocess
import sys
import threading
import time
from datetime import datetime

import schedule


class HourlyAutomation:
    def __init__(self):
        self.tasks_completed = 0
        print(f"⏰ SAATLİK OTOMASYON SİSTEMİ - {datetime.now()}")
    
    def task_github_learn(self):
        """GitHub'dan öğren"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📚 GitHub öğrenme başlıyor...")
        try:
            subprocess.run([sys.executable, "social_learner.py"], timeout=300)
            print("✅ GitHub öğrenme tamamlandı")
            return True
        except Exception as e:
            print(f"❌ GitHub hatası: {e}")
            return False
    
    def task_process_million(self):
        """1M işlem çalıştır"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 💥 1M işlem başlıyor...")
        try:
            subprocess.run([sys.executable, "distributed_processing.py"], timeout=600)
            print("✅ 1M işlem tamamlandı")
            return True
        except Exception as e:
            print(f"❌ İşlem hatası: {e}")
            return False
    
    def task_self_update(self):
        """Kendini güncelle"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Otomatik güncelleme...")
        try:
            # GitHub'dan güncelle
            import requests
            response = requests.get("https://api.github.com/repos/nexus-one/core/commits")
            if response.status_code == 200:
                print(f"📅 Son commit: {response.json()[0]['commit']['message'][:50]}...")
            
            # Gerekli kütüphaneleri güncelle
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "requests", "gitpython"])
            print("✅ Güncelleme tamamlandı")
            return True
        except Exception as e:
            print(f"❌ Güncelleme hatası: {e}")
            return False
    
    def task_data_processing(self):
        """Veri işleme"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌀 Veri işleme başlıyor...")
        try:
            # Büyük veri işleme simülasyonu
            import numpy as np
            data = np.random.rand(1000000)  # 1M rastgele sayı
            processed = np.mean(data), np.std(data), np.max(data)
            print(f"📊 Veri işleme: Ortalama={processed[0]:.4f}, STD={processed[1]:.4f}")
            return True
        except Exception as e:
            print(f"❌ Veri işleme hatası: {e}")
            return False
    
    def run_all_tasks(self):
        """Tüm görevleri çalıştır"""
        print(f"\n{'='*60}")
        print(f"🚀 SAATLİK GÖREVLER BAŞLIYOR - {datetime.now().strftime('%H:%M')}")
        print(f"{'='*60}")
        
        tasks = [
            ("GitHub Öğrenme", self.task_github_learn),
            ("1M İşlem", self.task_process_million),
            ("Otomatik Güncelleme", self.task_self_update),
            ("Veri İşleme", self.task_data_processing)
        ]
        
        completed = 0
        for task_name, task_func in tasks:
            try:
                if task_func():
                    completed += 1
                    print(f"   ✅ {task_name} tamamlandı")
                else:
                    print(f"   ⚠️ {task_name} atlandı")
            except Exception as e:
                print(f"   ❌ {task_name} hatası: {e}")
        
        self.tasks_completed += completed
        
        print(f"\n📈 SAATLİK ÖZET:")
        print(f"   • Tamamlanan görev: {completed}/{len(tasks)}")
        print(f"   • Toplam görev: {self.tasks_completed}")
        print(f"   • Sonraki saat: {datetime.now().hour + 1}:00")
        print(f"{'='*60}")
    
    def schedule_hourly(self):
        """Saatlik görevleri planla"""
        # Her saat başı
        schedule.every().hour.at(":00").do(self.run_all_tasks)
        
        # Ek görevler
        schedule.every(30).minutes.do(self.task_data_processing)
        schedule.every().day.at("02:00").do(self.task_self_update)
        
        print(f"⏰ Görevler planlandı:")
        print(f"   • Her saat: Tüm görevler")
        print(f"   • 30 dakikada bir: Veri işleme")
        print(f"   • Günlük 02:00: Otomatik güncelleme")
        
        # İlk görevi hemen çalıştır
        self.run_all_tasks()
        
        # Zamanlayıcıyı başlat
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """Sistemi başlat"""
        print("""
╔══════════════════════════════════════════╗
║     ⏰ SAATLİK OTOMASYON SİSTEMİ         ║
║     🚀 Her saat 1M+ işlem               ║
║     📚 Sürekli öğrenme                  ║
║     🔄 Otomatik güncelleme              ║
╚══════════════════════════════════════════╝
        """)
        
        # Thread'de başlat
        thread = threading.Thread(target=self.schedule_hourly, daemon=True)
        thread.start()
        
        # Ana thread'de bekle
        try:
            while True:
                time.sleep(60)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ Sistem aktif...")
        except KeyboardInterrupt:
            print(f"\n🛑 Sistem durduruluyor...")
            print(f"🎯 Toplam tamamlanan saat: {self.tasks_completed // 4}")
            print(f"✅ Otomasyon sistem kapatıldı")

# Çalıştır
if __name__ == "__main__":
    automation = HourlyAutomation()
    automation.start()
