import json
import time
from datetime import datetime


class Beyin:
    def __init__(self):
        self.kararlar = []
        self.moduller = {}

    def modul_ekle(self, isim, modul):
        self.moduller[isim] = modul
        print(f"🧠 {isim} modülü eklendi")

    def karar_ver(self, gorev):
        karar = {
            "zaman": datetime.now().isoformat(),
            "gorev": gorev,
            "oncelik": self.oncelik_belirle(gorev),
            "moduller": self.uygun_modulleri_bul(gorev),
        }
        self.kararlar.append(karar)
        return karar

    def oncelik_belirle(self, gorev):
        """Görevin aciliyetine göre öncelik belirler."""
        gorev = gorev.lower()
        if "acil" in gorev or "hemen" in gorev or "kritik" in gorev:
            return "Yüksek"
        elif "önemli" in gorev or "raporla" in gorev:
            return "Orta"
        else:
            return "Düşük"

    def uygun_modulleri_bul(self, gorev):
        """Görevin içeriğine göre en uygun modülleri seçer."""
        gorev = gorev.lower()
        secilen_moduller = []

        # Anahtar kelime bazlı modül seçimi
        if "kod yaz" in gorev or "geliştir" in gorev or "script" in gorev:
            secilen_moduller.append("kod_uretici")
        if "görsel" in gorev or "resim" in gorev or "tasarım" in gorev:
            secilen_moduller.append("gorsel_uretici")
        if "analiz et" in gorev or "raporla" in gorev or "araştır" in gorev:
            secilen_moduller.append("analiz")
        if "planla" in gorev or "organize et" in gorev:
            secilen_moduller.append("gorev_yonetici")
        if "dosya" in gorev or "kaydet" in gorev or "oku" in gorev:
            secilen_moduller.append("dosya_yonetici")

        # Eğer hiç modül bulunamazsa, genel bir modül ekle
        if not secilen_moduller:
            secilen_moduller.append("genel_islem")

        return secilen_moduller

    def calistir(self, karar):
        print(f"▶️ Çalıştırılıyor: {karar['gorev']}")
        for modul_adi in karar["moduller"]:
            if modul_adi in self.moduller:
                sonuc = self.moduller[modul_adi].calis(karar["gorev"])
                print(f"   ✅ {modul_adi}: {sonuc}")
        return "Görev tamamlandı!"
