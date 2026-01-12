# modules/otomatik_yedek.py
import os
import shutil
from datetime import datetime


class OtomatikYedek:
    def __init__(self):
        print("💾 OTOMATİK YEDEK MODÜLÜ HAZIR")

    def yedek_al(self, aciklama=""):
        """Otomatik yedek al"""
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_klasor = f"backups/yedek_{tarih}"

        # Yedeklenecek klasörler
        kaynaklar = ["modules", "generated", "logs"]

        try:
            os.makedirs(yedek_klasor, exist_ok=True)

            for kaynak in kaynaklar:
                if os.path.exists(kaynak):
                    hedef = os.path.join(yedek_klasor, kaynak)
                    if os.path.isdir(kaynak):
                        shutil.copytree(kaynak, hedef)
                    else:
                        shutil.copy2(kaynak, hedef)

            # Yedek bilgisini kaydet
            bilgi = {
                "tarih": datetime.now().isoformat(),
                "aciklama": aciklama,
                "yedek_klasor": yedek_klasor,
                "boyut": self.klasor_boyutu(yedek_klasor),
            }

            with open(f"{yedek_klasor}/yedek_bilgi.json", "w", encoding="utf-8") as f:
                json.dump(bilgi, f, indent=2, ensure_ascii=False)

            return f"✅ Yedek alındı: {yedek_klasor}"

        except Exception as e:
            return f"❌ Yedek hatası: {e}"

    def klasor_boyutu(self, yol):
        """Klasör boyutunu hesapla"""
        toplam = 0
        for kok, klasorler, dosyalar in os.walk(yol):
            for dosya in dosyalar:
                dosya_yolu = os.path.join(kok, dosya)
                if os.path.exists(dosya_yolu):
                    toplam += os.path.getsize(dosya_yolu)
        return f"{toplam / 1024:.1f} KB"

    def calis(self, gorev=""):
        return self.yedek_al(gorev)
