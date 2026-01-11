@echo off
chcp 65001 >nul
echo.
echo ========================================
echo     NEXUS-ONE - Basit Test Sürümü
echo ========================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo Lütfen Python 3.8+ yükleyin: https://python.org
    pause
    exit /b 1
)

echo ✅ Python bulundu
echo 🚀 NEXUS-ONE başlatılıyor...
echo.

REM Ana uygulamayı çalıştır
python main.py

echo.
echo ========================================
echo     NEXUS-ONE kapatıldı
echo ========================================
echo.
pause
