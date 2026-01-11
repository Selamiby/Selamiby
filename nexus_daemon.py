# nexus_daemon.py
import json
import time
from datetime import datetime



class NexusDaemon:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Gece görevlerini yükle"""
        self.tasks = [
            {"time": "02:00", "action": "autogpt", "task": "Sistem optimizasyonu"},
            {"time": "03:00", "action": "gpt_engineer", "task": "Backup script'i yaz"},
            {"time": "04:00", "action": "crewai", "task": "Yeni özellikler araştır"},
            {"time": "05:00", "action": "stable_diffusion", "task": "Dashboard için görsel üret"},
        ]

    def run_scheduled_tasks(self):
        """Zamanlanmış görevleri çalıştır"""
        current_time = datetime.now().strftime("%H:%M")

        for task in self.tasks:
            if task["time"] == current_time:
                print(f"⏰ {task['time']} - {task['action']}: {task['task']}")
                # Burada gerçek çalıştırma kodları olacak
                self.execute_task(task)
                time.sleep(60)  # 1 dakika bekle

    def execute_task(self, task):
        """Görevi çalıştır"""
        # Bu kısım hyper_integration.py ile entegre olacak
        print(f"▶️  Çalıştırılıyor: {task}")

    def run_forever(self):
        """Sonsuza kadar çalış"""
        print("👁️  NEXUS DAEMON AKTİF - Siz uyurken ben çalışacağım!")

        while True:
            try:
                self.run_scheduled_tasks()
                time.sleep(30)  # 30 saniyede bir kontrol et
            except KeyboardInterrupt:
                # nexus_daemon.py
import time
import json
from datetime import datetime
import os

# hyper_integration.py dosyasından ana kontrol sınıfını içe aktar
from hyper_integration import NexusHyperCore


class NexusDaemon:
    def __init__(self):
        print("🧠 Nexus Çekirdeği ve modüller yükleniyor...")
        self.nexus_core = NexusHyperCore()
        self.tasks = []
        self.load_tasks()
        # Görevler için bir çalışma alanı oluşturalım
        if not os.path.exists('daemon_projects'):
            os.makedirs('daemon_projects')

    def load_tasks(self):
        """Gece görevlerini yükle"""
        self.tasks = [
            {"time": "02:00", "action": "autogpt", "task": "Günün teknoloji haberlerini özetle ve raporla"},
            {"time": "03:00", "action": "gpt_engineer", "task": "Sistemin genel durumunu kontrol eden bir Python scripti yaz"},
            {"time": "04:00", "action": "crewai", "task": "Yapay zeka alanındaki yeni trendleri araştır ve bir sunum hazırla"},
            {"time": "05:00", "action": "stable_diffusion", "task": "Geleceğin teknolojisi temalı bir konsept sanat oluştur"},
        ]

    def run_scheduled_tasks(self):
        """Zamanlanmış görevleri çalıştır"""
        current_time = datetime.now().strftime("%H:%M")

        for task in self.tasks:
            if task["time"] == current_time:
                print(f"⏰ Zamanı geldi! Görev başlatılıyor: {task['action']} - {task['task']}")
                self.execute_task(task)
                # Görevin tekrar çalışmasını önlemek için 60 saniye bekle
                time.sleep(61)

    def execute_task(self, task_info):
        """Görevi ilgili modülü kullanarak çalıştırır."""
        action = task_info["action"]
        task_payload = task_info["task"]

        print(f"▶️  {action} modülü çalıştırılıyor... Görev: {task_payload}")

        try:
            if action == 'autogpt' and 'autogpt' in self.nexus_core.modules:
                runner = self.nexus_core.modules['autogpt'].get('runner')
                if hasattr(runner, 'decide'):
                    result = runner.decide(task_payload)
                else:
                    result = runner(f"--ai-goal={task_payload}")
                print(f"✅ Sonuç: {result}")

            elif action == 'gpt_engineer' and 'gpt_engineer' in self.nexus_core.modules:
                project_path = f"daemon_projects/project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.makedirs(project_path, exist_ok=True)
                runner = self.nexus_core.modules['gpt_engineer'].get('runner')
                if hasattr(runner, 'generate'):
                     result = runner.generate(task_payload, project_path)
                else:
                    print("Gerçek GPT-Engineer entegrasyonu gerektirir.")
                    result = "Simülasyon tamamlandı."
                print(f"✅ Kod '{project_path}' içine üretildi. Sonuç: {result}")

            elif action == 'crewai' and 'crewai' in self.nexus_core.modules:
                runner = self.nexus_core.modules['crewai'].get('runner')
                if hasattr(runner, 'execute_project'):
                    result = runner.execute_project(task_payload)
                else:
                    result = runner(task_payload)
                print(f"✅ CrewAI görevi tamamladı. Sonuç: {result}")

            elif action == 'stable_diffusion' and 'stable_diffusion' in self.nexus_core.modules:
                runner = self.nexus_core.modules['stable_diffusion']
                if hasattr(runner, 'generate'):
                    filename = runner.generate(task_payload)
                else:
                    image = runner(prompt=task_payload).images[0]
                    filename = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    image.save(filename)
                print(f"✅ Görsel '{filename}' olarak kaydedildi.")

            else:
                print(f"⚠️  Modül '{action}' bulunamadı veya çalıştırılamadı.")

        except Exception as e:
            print(f"❌ HATA: {action} çalıştırılırken bir sorun oluştu: {e}")

    def run_forever(self):
        """Sonsuza kadar çalış"""
        print("👁️  NEXUS DAEMON AKTİF - Siz uyurken ben çalışacağım!")

        while True:
            try:
                self.run_scheduled_tasks()
                time.sleep(30)  # 30 saniyede bir kontrol et
            except KeyboardInterrupt:
                print("\n🛑 Daemon durduruluyor...")
                break
            except Exception as e:
                print(f"⚠️ DAEMON ANA DÖNGÜ HATASI: {e}")
                time.sleep(60)

if __name__ == "__main__":
    daemon = NexusDaemon()
    daemon.run_forever()
                break
            except Exception as e:
                print(f"⚠️  Hata: {e}")
                time.sleep(60)

if __name__ == "__main__":
    daemon = NexusDaemon()
    daemon.run_forever()
