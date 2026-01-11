@echo off
echo NEXUS-ONE REAL Kurulumu
echo ======================

REM Sanal ortam oluştur
python -m venv .venv
call .venv\Scripts\activate

REM Paketleri kur
pip install --upgrade pip
pip install psutil requests dnspython python-whois python-dotenv GitPython

REM Requirements dosyasını oluştur
pip freeze > requirements.txt

echo.
echo ✅ Kurulum tamamlandı!
echo 🚀 Başlatmak için: python nexus_one_real.py
pause
