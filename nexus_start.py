# nexus_start.py - FAST START
import os
import time
from datetime import datetime

print("?? NEXUS SÝSTEM BAÞLATILIYOR...")
print(f"Tarih: {datetime.now()}")

# Klasörleri oluþtur
for klasor in ["modules", "logs", "data", "generated", "backups"]:
    os.makedirs(klasor, exist_ok=True)
    print(f"? {klasor} klasörü hazýr")

# Modülleri yükle
print("\n?? MODÜLLER YÜKLENÝYOR...")
beyin = None
try:
    if os.path.exists("modules"):
        from modules.beyin import Beyin

        beyin = Beyin()
        print("? Beyin modülü yüklendi")
    else:
        print("??  Beyin modülü bulunamadý - devam ediliyor")
except Exception as e:
    print(f"??  Modül yükleme hatasý: {e} - devam ediliyor")

# Test görevi
print("\n?? TEST GÖREVÝ...")
if beyin:
    karar = beyin.karar_ver("Sistem baþlat")
    print(f"Karar: {karar}")
    sonuc = beyin.calistir(karar)
    print(f"Sonuç: {sonuc}")
else:
    print("??  Beyin modülü yok - test atlanýyor")

# Sürekli çalýþma döngüsü
print("\n???  SÝSTEM ÇALIÞIYOR... (Ctrl+C ile durdur)")
sayac = 0
try:
    while True:
        sayac += 1
        print(f"\n?? Tur {sayac} - {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(5)  # 5 saniye bekle
except KeyboardInterrupt:
    print("\n?? Sistem durduruluyor...")

print("\n? NEXUS kapatýldý")
