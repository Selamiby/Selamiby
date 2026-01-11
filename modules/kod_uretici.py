# modules/kod_uretici.py
import os
from datetime import datetime


class KodUretici:
    def __init__(self):
        print("💻 KOD ÜRETİCİ MODÜLÜ HAZIR")
    
    def python_kodu_uret(self, aciklama):
        """Python kodu üret"""
        sifir = """# Otomatik üretildi: {tarih}
print("Merhaba Dünya!")
print("Bu kod Nexus tarafından üretildi.")

# Kullanıcı girişi
isim = input("İsminiz: ")
print(f"Hoş geldin, {isim}!")
"""
        
        hesap = """# Hesap makinesi - {tarih}
def topla(a, b):
    return a + b

def cikar(a, b):
    return a - b

def carp(a, b):
    return a * b

def bol(a, b):
    return a / b if b != 0 else "Hata: Sıfıra bölünemez"

# Test
print("Toplam:", topla(10, 5))
print("Fark:", cikar(10, 5))
"""
        
        oyun = """# Basit oyun - {tarih}
import random

print("🎮 SAYI TAHMİN OYUNU")
print("1-100 arası bir sayı tuttum...")

tutulan = random.randint(1, 100)
tahmin_hakki = 7

for deneme in range(1, tahmin_hakki + 1):
    tahmin = int(input(f"{{deneme}}. tahminin: "))
    
    if tahmin < tutulan:
        print("📈 Daha büyük!")
    elif tahmin > tutulan:
        print("📉 Daha küçük!")
    else:
        print(f"🎉 Tebrikler! {deneme}. denemede bildin!")
        break
else:
    print(f"❌ Bilemedin! Sayı: {tutulan}")
"""
        
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        if "merhaba" in aciklama.lower() or "basit" in aciklama.lower():
            kod = sifir.format(tarih=tarih)
            dosya = "merhaba.py"
        elif "hesap" in aciklama.lower() or "hesapla" in aciklama.lower():
            kod = hesap.format(tarih=tarih)
            dosya = "hesap_makinesi.py"
        elif "oyun" in aciklama.lower():
            kod = oyun.format(tarih=tarih)
            dosya = "sayi_tahmin_oyunu.py"
        else:
            kod = sifir.format(tarih=tarih)
            dosya = "program.py"
        
        # generated klasörüne kaydet
        os.makedirs("generated", exist_ok=True)
        yol = f"generated/{dosya}"
        
        with open(yol, "w", encoding="utf-8") as f:
            f.write(kod)
        
        return f"✅ Kod üretildi: {dosya} ({len(kod)} karakter)"
    
    def calis(self, gorev=""):
        return self.python_kodu_uret(gorev)