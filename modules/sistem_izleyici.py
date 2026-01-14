"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

# modules/sistem_izleyici.py
import psutil


class SistemIzleyici:
    def calis(self, gorev=""):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"CPU: %{cpu}, RAM: %{ram}"
