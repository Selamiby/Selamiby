# nexus_core.py
import logging
import os
import threading
import time
import traceback  # Hata ayıklama için eklendi

from backend.self_healing import SelfHealingSystem


class NexusCore:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(self.project_root, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, 'nexus_core.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [NEXUS_CORE] - %(message)s',
            handlers=[logging.FileHandler(log_file_path, encoding='utf-8')]
        )
        self.healer = SelfHealingSystem(self.project_root)
        self.monitor_thread = threading.Thread(target=self.healer.start_monitoring, kwargs={"interval": 300}, daemon=True)
        self.monitor_thread.start()
        logging.info("NexusCore initialized and self-healing monitoring started.")

    def run(self):
        try:
            logging.info("NEXUS ÇEKİRDEK SERVİSİ BAŞLATILDI!")
            sayac = 0
            while True:
                sayac += 1
                logging.info(f"Servis döngüsü: {sayac}. Sistem aktif.")
                if sayac % 10 == 0:
                    logging.info("Periyodik yedekleme simülasyonu çalıştırılıyor...")
                time.sleep(3)
        except Exception as e:
            logging.error("KRİTİK HATA OLUŞTU!")
            logging.error(traceback.format_exc())

    def shutdown(self):
        self.healer.stop_monitoring()
        logging.info("NexusCore shutdown: self-healing monitoring stopped.")

if __name__ == "__main__":
    core = NexusCore()
    try:
        core.run()
    except KeyboardInterrupt:
        core.shutdown()
        print("NexusCore stopped.")


# Proje ana dizinini al
project_root = os.path.dirname(os.path.abspath(__file__))

# Log dizinini ve dosyasını oluştur
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'nexus_core.log')

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [NEXUS_CORE] - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8')
    ]
)

try:
    logging.info("NEXUS ÇEKİRDEK SERVİSİ BAŞLATILDI!")
    sayac = 0
    while True: 
        sayac += 1
        logging.info(f"Servis döngüsü: {sayac}. Sistem aktif.")
        if sayac % 10 == 0: # Her 10 döngüde bir (30 saniyede bir)
            logging.info("Periyodik yedekleme simülasyonu çalıştırılıyor...")
        time.sleep(3)
except Exception as e:
    # Herhangi bir hata olursa, hatayı log dosyasına yaz
    logging.error("KRİTİK HATA OLUŞTU!")
    logging.error(traceback.format_exc())

