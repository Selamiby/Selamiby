import json
import os
import subprocess
import sys
import time

import psutil

SCRIPTS_TO_RUN = ['hyper_integration.py', 'nexus_daemon.py']
PID_FILE = '.nexus_pids.json'

def run_command(command, description):
    """Komutu çalıştırır ve hataları yönetir."""
    print(f"🔄 {description}...")
    try:
        # Hataları ve çıktıları gizle
        subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {description} tamamlandı.")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ HATA: {description} sırasında bir sorun oluştu.")
        return False
    except FileNotFoundError:
        print(f"❌ HATA: '{command[0]}' komutu bulunamadı.")
        return False

def start_all():
    """Tüm Nexus sistemini başlatır."""
    print("🚀 NEXUS HYPER-EVOLUTION v1.0 🚀")
    print("================================")

    # 1. Bağımlılıkları yükle
    if os.path.exists('requirements_hyper.txt'):
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements_hyper.txt"], "Bağımlılıklar yükleniyor")
    else:
        print("⚠️ requirements_hyper.txt bulunamadı, kurulum atlandı.")

    # Mevcut PID'leri temizle
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    processes = {}
    for script in SCRIPTS_TO_RUN:
        if not os.path.exists(script):
            print(f"❌ HATA: Başlatılacak betik bulunamadı: {script}")
            continue
        
        print(f"⚡ '{script}' arka planda başlatılıyor...")
        # Her betik için ayrı log dosyası oluştur
        log_file = open(f"{script.split('.')[0]}.log", "w")
        # Popen ile betikleri arka planda başlat
        process = subprocess.Popen([sys.executable, script], stdout=log_file, stderr=log_file)
        processes[script] = process.pid
        print(f"   PID: {process.pid} | Log: {script.split('.')[0]}.log")

    # PID'leri dosyaya kaydet
    with open(PID_FILE, 'w') as f:
        json.dump(processes, f)

    print("\n✅ SİSTEM HAZIR!")
    print("🌐 Dashboard: http://localhost:5000")
    print("👁️  Daemon arka planda çalışıyor.")
    print("💤 Artık uyuyabilirsiniz! Sistem otomatik çalışacak.")

    # Çalışan süreçleri göster
    time.sleep(3) # Betiklerin başlaması için kısa bir süre bekle
    print("\n--- Aktif Python Süreçleri ---")
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        if p.info['name'] == os.path.basename(sys.executable) and any('nexus' in ' '.join(p.info['cmdline']) or 'hyper' in ' '.join(p.info['cmdline'])):
             print(f"  PID: {p.info['pid']}, Komut: {' '.join(p.info['cmdline'])}")
    
    print("\n🛑 Durdurmak için 'stop.bat' (Windows) veya './stop.sh' (Linux/macOS) çalıştırın.")

if __name__ == "__main__":
    start_all()
