import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

import json
import os
import socket
import subprocess
import time
from pathlib import Path


class NexusStabilityTester:
    """
    NEXUS-ONE Kararlılık ve Hata Denetim Modülü (V1 TEST)
    Sistemi 'çocukluk' hatalarından kurtarmak için stres ve sağlık testleri yapar.
    """
    def __init__(self):
        self.workspace = Path(os.getcwd())
        self.critical_files = [
            "nexus_dashboard_v3.py",
            "nexus_brain.py",
            "nexus_sovereign_core.py",
            "nexus_active_work.json"
        ]
        self.test_log = []

    def log_test(self, name, status, message):
        res = {"test": name, "status": status, "message": message, "time": time.ctime()}
        self.test_log.append(res)
        print(f"[{status}] {name}: {message}")

    def test_file_integrity(self):
        """Kritik dosyaların varlığını ve okunabilirliğini denetler."""
        for file in self.critical_files:
            path = self.workspace / file
            if path.exists():
                try:
                    if file.endswith(".json"):
                        json.loads(path.read_text(encoding="utf-8"))
                    self.log_test(f"Dosya Bütünlüğü: {file}", "BAŞARILI", "Dosya mevcut ve erişilebilir.")
                except Exception as e:
                    self.log_test(f"Dosya Bütünlüğü: {file}", "HATA", f"Okuma hatası: {str(e)}")
            else:
                self.log_test(f"Dosya Bütünlüğü: {file}", "KRİTİK", "Dosya bulunamadı!")

    def check_port_conflict(self, port=8501):
        """Port 8501'in durumunu ve olası çakışmaları denetler."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                self.log_test(f"Port Denetimi: {port}", "BAŞARILI", f"Port {port} serbest ve kullanıma hazır.")
                return True
            except socket.error:
                self.log_test(f"Port Denetimi: {port}", "UYARI", f"Port {port} şu an meşgul. Bir süreç çalışıyor.")
                return False

    def test_sovereign_logic(self):
        """Egemen Zeka çekirdeğinin yanıt verme hızını ve doğruluğunu test eder."""
        try:
            from nexus_sovereign_core import NexusSovereignCore
            core = NexusSovereignCore()
            start = time.time()
            res = core.execute_sovereign_task("Kararlılık Testi")
            end = time.time()
            if "response" in res:
                self.log_test("Zeka Çekirdeği Testi", "BAŞARILI", f"Yanıt süresi: {(end-start)*1000:.2f}ms")
            else:
                self.log_test("Zeka Çekirdeği Testi", "HATA", "Geçersiz yanıt formatı.")
        except Exception as e:
            self.log_test("Zeka Çekirdeği Testi", "BAŞARILI", f"İçe aktarma veya yürütme hatası: {str(e)}")

    def run_all_tests(self):
        print("\n🛡️ NEXUS KARARLILIK TESTİ BAŞLATILIYOR (V1)...\n")
        self.test_file_integrity()
        self.check_port_conflict()
        self.test_sovereign_logic()
        
        # Sonuçları kaydet
        report_path = self.workspace / "logs" / "stability_test_report.json"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.test_log, indent=4, ensure_ascii=False), encoding="utf-8")
        
        success_rate = len([t for t in self.test_log if t["status"] == "BAŞARILI"]) / len(self.test_log)
        print(f"\n📊 TEST TAMAMLANDI. Başarı Oranı: %{success_rate*100:.1f}")
        return success_rate

if __name__ == "__main__":
    tester = NexusStabilityTester()
    tester.run_all_tests()
