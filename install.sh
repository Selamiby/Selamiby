#!/bin/bash
echo "NEXUS-ONE REAL Kurulumu"
echo "======================"

# Sanal ortam oluştur
python3 -m venv .venv
source .venv/bin/activate

# Paketleri kur
pip install --upgrade pip
pip install psutil requests dnspython python-whois python-dotenv GitPython

# Requirements dosyasını oluştur
pip freeze > requirements.txt

echo ""
echo "✅ Kurulum tamamlandı!"
echo "🚀 Başlatmak için: python nexus_one_real.py"
