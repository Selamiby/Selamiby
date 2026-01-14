import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import os
import socket
import subprocess
import sys
import time


def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

print("🔍 NEXUS-ONE Diagnostik Başlatılıyor...")
print(f"Python: {sys.version}")
print(f"PATH: {os.environ.get('PATH')[:100]}...")

try:
    import webview
    print("✅ pywebview yüklü.")
except ImportError:
    print("❌ pywebview YÜKLÜ DEĞİL!")

# Check streamlit
try:
    import streamlit
    print("✅ streamlit yüklü.")
except ImportError:
    print("❌ streamlit YÜKLÜ DEĞİL!")

# Check if streamlit is already running
if check_port(8501):
    print("⚠️  8501 portu zaten kullanımda. Streamlit zaten çalışıyor olabilir.")
else:
    print("ℹ️  8501 portu boş.")

# Try to start streamlit and see if it fails
print("🔄 Streamlit başlatma testi yapılıyor...")
try:
    proc = subprocess.Popen(
        ["streamlit", "run", "nexus_dashboard_v2.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(3)
    if proc.poll() is not None:
        out, err = proc.communicate()
        print(f"❌ Streamlit hemen kapandı: {err}")
    else:
        print("✅ Streamlit arka planda çalışıyor.")
        proc.terminate()
except Exception as e:
    print(f"❌ Streamlit başlatılamadı: {e}")

print("🏁 Diagnostik tamamlandı.")
