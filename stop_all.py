import json
import os
import signal

import psutil

PID_FILE = ".nexus_pids.json"


def stop_all():
    """PID dosyasında kayıtlı tüm süreçleri durdurur."""
    print("🛑 Nexus süreçleri durduruluyor...")
    if not os.path.exists(PID_FILE):
        print("⚠️ PID dosyası bulunamadı. Çalışan süreç yok veya manuel durdurulmuş.")
        return

    with open(PID_FILE, "r") as f:
        try:
            pids = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ PID dosyası bozuk.")
            pids = {}

    for script, pid in pids.items():
        try:
            process = psutil.Process(pid)
            # Önce alt süreçleri durdur
            for child in process.children(recursive=True):
                print(f"   -> Alt süreç durduruluyor: {child.pid}")
                child.kill()
            # Ana süreci durdur
            print(f"   -> Ana süreç durduruluyor: {script} (PID: {pid})")
            process.kill()
        except psutil.NoSuchProcess:
            print(f"   -> Süreç zaten durmuş: {script} (PID: {pid})")
        except Exception as e:
            print(f"❌ Hata: {pid} PID'li süreç durdurulurken sorun oluştu: {e}")

    # PID dosyasını temizle
    os.remove(PID_FILE)
    print("✅ Tüm Nexus süreçleri durduruldu.")


if __name__ == "__main__":
    stop_all()
