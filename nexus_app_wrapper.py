import os
import subprocess
import sys
import time

import webview


def start_nexus_app():
    # 1. Dashboard'un arka planda çalıştığından emin ol
    print("🚀 NEXUS-ONE Motoru çalıştırılıyor...")
    # Streamlit'i arka planda başlat
    subprocess.Popen(
        ["streamlit", "run", "nexus_dashboard_v2.py", "--server.port", "8501", "--server.headless", "true"],
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    )
    
    # Dashboard'un ayağa kalkması için kısa bir süre bekle
    time.sleep(5)
    
    # 2. Gerçek bir Windows Penceresi oluştur
    print("🖥️  Arayüz yükleniyor...")
    window = webview.create_window(
        'NEXUS-ONE Advanced OS', 
        'http://localhost:8501',
        width=1280,
        height=800,
        resizable=True,
        confirm_close=True
    )
    
    webview.start()

if __name__ == '__main__':
    start_nexus_app()
