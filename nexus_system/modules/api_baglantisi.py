# modules/api_baglantisi.py
import requests


class APIBaglantisi:
    def calis(self, talimat):
        if "hava" in talimat:
            return self.hava_durumu()
        elif "haber" in talimat:
            return self.haber_getir()
        else:
            return self.internet_kontrol()

    def hava_durumu(self, sehir="Istanbul"):
        try:
            # Örnek API (gerçek API key gerekli)
            # Ücretsiz bir API kullandım, bu yüzden anahtar gerekmiyor
            response = requests.get(f"https://goweather.herokuapp.com/weather/{sehir}")
            data = response.json()
            return f"{sehir} için hava durumu: {data['temperature']}, {data['description']}"
        except Exception as e:
            print(f"Hava durumu API hatası: {e}")
            return "⛅ Hava durumu bilgisi alınamadı, ancak gökyüzü açık görünüyor (simüle edildi)."

    def haber_getir(self):
        """Basit bir haber getirme simülasyonu."""
        # Gerçek bir haber API'si (NewsAPI, GNews vb.) entegre edilebilir.
        haberler = [
            "Yapay zeka teknolojisi hızla gelişmeye devam ediyor.",
            "Yeni nesil kuantum bilgisayarlar için önemli bir adım atıldı.",
            "Otonom araçlar şehir içi test sürüşlerine başladı.",
        ]
        import random

        return f"📰 Günün haberi: {random.choice(haberler)}"

    def internet_kontrol(self):
        try:
            requests.get("https://google.com", timeout=3)
            return "🌐 İnternet bağlantısı var"
        except requests.ConnectionError:
            return "❌ İnternet bağlantısı yok"
