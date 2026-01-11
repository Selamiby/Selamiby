# nexus_quick_setup.ps1
Write-Host "🚀 NEXUS HIZLI KURULUM" -ForegroundColor Green

# Klasörleri oluştur
$folders = @("modules", "logs", "data", "generated", "backups", "templates")
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder
    Write-Host "✅ $folder klasörü oluşturuldu" -ForegroundColor Cyan
}

# Temel modülleri oluştur
# 1. Beyin modülü
$beyinCode = @'
# modules/beyin.py
class Beyin:
    def __init__(self):
        print("🧠 Beyin modülü hazır")
    
    def calis(self, gorev):
        return f"Beyin çalışıyor: {gorev}"
'@
$beyinCode | Out-File -FilePath "modules\beyin.py" -Encoding UTF8

# 2. Sistem izleyici
$sistemCode = @'
# modules/sistem_izleyici.py
import psutil

class SistemIzleyici:
    def calis(self, gorev=""):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"CPU: %{cpu}, RAM: %{ram}"
'@
$sistemCode | Out-File -FilePath "modules\sistem_izleyici.py" -Encoding UTF8

# Ana program
$mainCode = @'
# nexus_core.py
import time
from datetime import datetime
from modules.beyin import Beyin
from modules.sistem_izleyici import SistemIzleyici

print("🚀 NEXUS CORE BAŞLATILDI")

# Modülleri yükle
beyin = Beyin()
sistem = SistemIzleyici()

# Sonsuz döngü
sayac = 0
try:
    while True:
        sayac += 1
        print(f"\n📊 Tur {sayac} - {datetime.now().strftime('%H:%M:%S')}")
        
        # Sistem durumu
        durum = sistem.calis()
        print(f"📈 {durum}")
        
        # Beyin çalıştır
        sonuc = beyin.calis(f"Tur {sayac}")
        print(f"🤖 {sonuc}")
        
        time.sleep(10)  # 10 saniye bekle
        
except KeyboardInterrupt:
    print("\n🛑 Sistem durduruldu")
'@
$mainCode | Out-File -FilePath "nexus_core.py" -Encoding UTF8

Write-Host "✅ Kurulum tamamlandı!" -ForegroundColor Green
Write-Host "Çalıştırmak için: python nexus_core.py" -ForegroundColor Yellow
