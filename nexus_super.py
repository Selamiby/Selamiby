# nexus_super.py
import os
import sys
import time
from datetime import datetime

print(
    """
╔══════════════════════════════════════════╗
║     🚀 NEXUS SUPER SYSTEM v3.0           ║
║     ⚡ Gerçek Modüller Aktif             ║
╚══════════════════════════════════════════╝
"""
)

# Klasörleri oluştur
for klasor in ["modules", "logs", "data", "generated", "backups"]:
    os.makedirs(klasor, exist_ok=True)

# Modülleri yükle
print("\n📦 MODÜLLER YÜKLENİYOR...")
try:
    from modules.beyin_gelismis import BeyinGelismis
    from modules.kod_uretici import KodUretici
    from modules.otomatik_yedek import OtomatikYedek
    from modules.sistem_monitor import SistemMonitor

    beyin = BeyinGelismis()
    kodcu = KodUretici()
    monitor = SistemMonitor()
    yedekci = OtomatikYedek()

    print("✅ Tüm modüller yüklendi!")

except Exception as e:
    print(f"❌ Modül yükleme hatası: {e}")
    print("⚠️  Basit modda devam ediliyor...")

    class BasitModul:
        def __init__(self, isim):
            self.isim = isim

        def calis(self, gorev=""):
            return f"{self.isim}: Basit mod"

        def kontrol_et(self):
            return {"cpu": 0, "ram": 0}

        def karar_ver(self, durum):
            return {"karar": "Basit modda devam et"}

        def calistir(self, karar):
            return "Basit modda karar uygulandı."

    beyin = BasitModul("🧠 Beyin")
    kodcu = BasitModul("💻 Kodcu")
    monitor = BasitModul("📊 Monitor")
    yedekci = BasitModul("💾 Yedek")

print("\n" + "=" * 50)
print("👁️  SÜPER SİSTEM AKTİF")
print("=" * 50)

# Ana çalışma döngüsü
tur = 0
try:
    while True:
        tur += 1

        print(f"\n{'='*60}")
        print(f"🌀 TUR {tur} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")

        # 1. Sistem durumunu kontrol et
        print("\n📊 SİSTEM DURUMU:")
        sistem_verisi = (
            monitor.kontrol_et()
            if hasattr(monitor, "kontrol_et")
            else {"cpu": 50, "ram": 50}
        )
        rapor = monitor.calis() if hasattr(monitor, "calis") else "Monitor aktif"
        print(rapor)

        # 2. Beyin karar versin
        print("\n🤖 BEYİN KARARI:")
        karar = (
            beyin.karar_ver(sistem_verisi)
            if hasattr(beyin, "karar_ver")
            else {"karar": "Devam et"}
        )
        karar_sonucu = (
            beyin.calistir(karar) if hasattr(beyin, "calistir") else "Karar uygulandı"
        )
        print(f"Karar: {karar.get('karar', 'Bilinmiyor')}")
        print(f"Sonuç: {karar_sonucu}")

        # 3. Her 5 turda bir kod üret
        if tur % 5 == 0:
            print("\n💻 KOD ÜRETİMİ:")
            kod_gorevi = ["basit program", "hesap makinesi", "oyun"][tur % 3]
            kod_sonuc = kodcu.calis(f"{kod_gorevi} yap")
            print(f"Görev: {kod_gorevi}")
            print(f"Sonuç: {kod_sonuc}")

        # 4. Her 10 turda bir yedek al
        if tur % 10 == 0:
            print("\n💾 YEDEKLEME:")
            yedek_sonuc = yedekci.calis(f"Tur {tur} yedeği")
            print(yedek_sonuc)

        # 5. Her 15 turda bir özet
        if tur % 15 == 0:
            print(f"\n📈 TUR {tur} ÖZETİ:")
            print(f"• Toplam tur: {tur}")
            print(f"• Sistem saati: {datetime.now().strftime('%H:%M:%S')}")
            print(f"• Modüller: Aktif")
            print(f"• Durum: Süper!")

        # 10 saniye bekle
        print(f"\n⏳ Sonraki tur için bekleniyor... (10 saniye)")
        time.sleep(10)

except KeyboardInterrupt:
    print(f"\n\n{'='*60}")
    print("🛑 SİSTEM DURDURULUYOR...")
    print(f"Toplam tur sayısı: {tur}")
    print(f"Bitiş saati: {datetime.now().strftime('%H:%M:%S')}")
    print("✅ Nexus Super System kapatıldı")
    print(f"{'='*60}")
