# distributed_processing.py
import math
import multiprocessing as mp
import time
from datetime import datetime
from multiprocessing import Pool, cpu_count


class DistributedProcessor:
    def __init__(self):
        self.cpu_count = cpu_count()
        print(f"💻 {self.cpu_count} CPU Çekirdeği Aktif")
        self.worker_count = self.cpu_count * 4  # Her çekirdek için 4 worker
        
    def isci(self, islem_id):
        """Her worker için işlem"""
        baslangic = time.time()
        
        # Yoğun matematik işlemleri
        sonuclar = []
        for i in range(10000):
            # 1. Karmaşık matematik
            x = math.sin(i) * math.cos(i) * math.tan(i)
            
            # 2. Fibonacci benzeri
            a, b = 0, 1
            for _ in range(100):
                a, b = b, a + b
            
            # 3. String işlemleri
            s = "".join([chr(65 + (i + j) % 26) for j in range(100)])
            
            # 4. Hash hesaplama
            import hashlib
            h = hashlib.sha256(s.encode()).hexdigest()
            
            sonuclar.append((x, a, h))
        
        sure = time.time() - baslangic
        return {
            "id": islem_id,
            "islemler": 10000,
            "sure": sure,
            "hiz": 10000/sure if sure > 0 else 0
        }
    
    def milyonluk_islem(self, hedef=1000000):
        """1M+ işlem paralel"""
        print(f"🚀 {hedef:,} İŞLEM BAŞLATILIYOR...")
        print(f"👷 {self.worker_count} worker hazır")
        
        # İşlem ID'leri oluştur
        islemler = list(range(hedef // 10000))
        
        baslangic = time.time()
        
        # Paralel işleme
        with Pool(processes=self.worker_count) as pool:
            sonuclar = pool.map(self.isci, islemler)
        
        bitis = time.time()
        
        # İstatistikler
        toplam_islem = sum(r["islemler"] for r in sonuclar)
        toplam_sure = bitis - baslangic
        ortalama_hiz = toplam_islem / toplam_sure
        
        print(f"\n✅ {toplam_islem:,} işlem {toplam_sure:.2f} saniyede tamamlandı!")
        print(f"⚡ Ortalama hız: {ortalama_hiz:,.0f} işlem/saniye")
        print(f"🔥 Saniyede: {ortalama_hiz/1000000:.2f}M işlem")
        
        return {
            "toplam_islem": toplam_islem,
            "toplam_sure": toplam_sure,
            "ortalama_hiz": ortalama_hiz,
            "worker_sayisi": self.worker_count
        }

# Test
if __name__ == "__main__":
    processor = DistributedProcessor()
    
    # 1M işlem testi
    processor.milyonluk_islem(1000000)
    
    # 10M işlem testi (daha uzun sürer)
    # processor.milyonluk_islem(10000000)