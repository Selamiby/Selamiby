import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

import json
import os
import socket
import subprocess
import time
from pathlib import Path


class NexusResilience:
    def __init__(self):
        self.workspace = Path(os.getcwd())
        self.report_path = self.workspace / "logs" / "resilience_report.json"
        self.report_path.parent.mkdir(exist_ok=True)

    def check_port(self, port=8501):
        """Portun meşgul olup olmadığını kontrol eder."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                print(f"⚠️ DİKKAT: {port} portu şu an başka bir süreç tarafından kullanılıyor!")
                return False
            return True

    def validate_critical_files(self):
        """Hayati dosyaların sağlamlığını kontrol eder."""
        critical_files = [
            "nexus_dashboard_v3.py",
            "nexus_brain.py",
            "nexus_sovereign_core.py",
            "nexus_one_config.json"
        ]
        results = {}
        for file in critical_files:
            path = self.workspace / file
            exists = path.exists()
            size = path.stat().st_size if exists else 0
            results[file] = {"exists": exists, "healthy": exists and size > 0}
            if not exists or size == 0:
                print(f"❌ KRİTİK HATA: {file} eksik veya bozuk!")
        return results

    def pre_flight_check(self):
        """Gelişim öncesi tam tarama."""
        print("🔍 NEXUS REZYLIANS TARAŞI BAŞLATILDI...")
        
        port_ok = self.check_port(8501)
        files = self.validate_critical_files()
        
        all_passed = port_ok and all(f["healthy"] for f in files.values())
        
        report = {
            "timestamp": time.ctime(),
            "port_8501_available": port_ok,
            "file_integrity": files,
            "status": "READY" if all_passed else "ERROR"
        }
        
        self.report_path.write_text(json.dumps(report, indent=4))
        
        if all_passed:
            print("✅ TEST BAŞARILI: Sistem stabil, kuantum gelişimine uygun.")
        else:
            print("🚨 TEST BAŞARISIZ: Lütfen yukarıdaki hataları giderin!")
        
        return all_passed

if __name__ == "__main__":
    tester = NexusResilience()
    tester.pre_flight_check()
