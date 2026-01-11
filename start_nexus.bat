@echo off
echo 🚀 NEXUS SISTEM BASLATILIYOR...
echo Tarih: %date% %time%
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadi!
    pause
    exit /b 1
)

REM Gerekli kütüphaneler
echo 📦 Kutuphaneler kontrol ediliyor...
pip install psutil --quiet

REM Ana programi calistir
echo ⚡ NEXUS calistiriliyor...
python nexus_start.py

echo.
echo 🛑 NEXUS durduruldu
pause
