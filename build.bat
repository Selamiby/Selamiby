# Sadece bu komutu yaz:
cd C:\
python nexus_simple.py # 1. PyInstaller yükle (sadece 1 kez)
pip install pyinstaller

# 2. EXE yap
pyinstaller --onefile --name NexusOne nexus_simple.py

# 3. EXE'yi bul
# dist klasöründe NexusOne.exe olacak # Tüm projeyi sıkıştır
Compress-Archive -Path "C:\Nexus-One\*" -DestinationPath "NexusOne_Portable.zip"