import os
import socket
import subprocess
import sys
import time

import webview


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_nexus_app():
    print("🚀 NEXUS-ONE Motoru kontrol ediliyor...")
    
    # Port 8501 dolu değilse başlat
    if not is_port_in_use(8501):
        print("⚡ Dashboard başlatılıyor...")
        subprocess.Popen(
            ["streamlit", "run", "nexus_dashboard_v2.py", "--server.port", "8501", "--server.headless", "true"],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        time.sleep(5)
    else:
        print("✅ Dashboard zaten çalışıyor (Port 8501).")

    print("🖥️  Masaüstü penceresi açılıyor...")
    
    try:
        window = webview.create_window(
            'NEXUS-ONE Advanced OS', 
            'http://localhost:8501',
            width=1280,
            height=800,
            resizable=True
        )
        # gui='edgechromium' zorlaması Windows için en iyi seçenektir
        webview.start(gui='edgechromium')
    except Exception as e:
        print(f"❌ Pencere hatası: {e}")
        webview.start()

if __name__ == '__main__':
    start_nexus_app()
