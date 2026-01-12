# nexus_start.py - FAST START
import os
import time
from datetime import datetime

print("🚀 NEXUS SİSTEM BAŞLATILIYOR...")
print(f"Tarih: {datetime.now()}")

# Klasörleri oluştur
for klasor in ["modules", "logs", "data", "generated", "backups"]:
    os.makedirs(klasor, exist_ok=True)
    print(f"✅ {klasor} klasörü hazır")

# Modülleri yükle
print("\n📦 MODÜLLER YÜKLENİYOR...")
try:
    from modules.beyin import Beyin
    beyin = Beyin()
    print("✅ Beyin modülü yüklendi")
except Exception as e:
    print(f"❌ Modül yükleme hatası: {e}")

# Test görevi
print("\n🧪 TEST GÖREVİ...")
karar = beyin.karar_ver("Sistem başlat")
print(f"Karar: {karar}")
sonuc = beyin.calistir(karar)
print(f"Sonuç: {sonuc}")

# Sürekli çalışma döngüsü
print("\n👁️  SİSTEM ÇALIŞIYOR... (Ctrl+C ile durdur)")
sayac = 0
try:
    while True:
        sayac += 1
        print(f"\n🔄 Tur {sayac} - {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(5)  # 5 saniye bekle
except KeyboardInterrupt:
    print("\n🛑 Sistem durduruluyor...")

print("\n✅ NEXUS kapatıldı")
