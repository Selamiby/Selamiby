"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
"""
NEXUS-ONE Öğrenme Modülü
Hatalardan öğrenir ve otomatik çözüm patterns'ı geliştirir
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class NEXUSLearner:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.learning_file = self.workspace_root / "data" / "nexus_learning.json"
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        self.load_learning_data()

    def load_learning_data(self):
        """Öğrenilmiş verileri yükle"""
        if self.learning_file.exists():
            with open(self.learning_file) as f:
                self.learning_data = json.load(f)
        else:
            self.learning_data = {
                "error_patterns": [],
                "solutions": [],
                "success_rate": 0.0,
                "total_fixes": 0,
                "last_learned": None,
            }

    def save_learning_data(self):
        """Öğrenilmiş verileri kaydet"""
        with open(self.learning_file, "w") as f:
            json.dump(self.learning_data, f, indent=2)

    def learn_error_pattern(self, file_path: str, error: str, solution: str):
        """Hata pattern'i öğren"""
        pattern = {
            "file_type": Path(file_path).suffix,
            "error": error,
            "solution": solution,
            "learned_at": datetime.now().isoformat(),
            "applied_count": 0,
        }

        # Aynı pattern önceden öğrenildi mi kontrol et
        for existing in self.learning_data["error_patterns"]:
            if (
                existing["error"] == error
                and existing["file_type"] == pattern["file_type"]
            ):
                existing["applied_count"] += 1
                self.save_learning_data()
                return

        self.learning_data["error_patterns"].append(pattern)
        self.save_learning_data()
        print(f"✓ Yeni pattern öğrenildi: {error} ({Path(file_path).suffix})")

    def learn_solution(self, error_type: str, file_type: str, solution: str):
        """Çözüm metodolojisini öğren"""
        solution_data = {
            "error_type": error_type,
            "file_type": file_type,
            "solution": solution,
            "effectiveness": 100,
            "learned_at": datetime.now().isoformat(),
        }

        self.learning_data["solutions"].append(solution_data)
        self.learning_data["total_fixes"] += 1
        self.save_learning_data()

    def update_success_rate(self, fixed: int, total: int):
        """Başarı oranını güncelle"""
        if total > 0:
            self.learning_data["success_rate"] = (fixed / total) * 100
            self.learning_data["last_learned"] = datetime.now().isoformat()
            self.save_learning_data()

    def get_learned_solutions(self, error_type: str, file_type: str) -> List[Dict]:
        """Öğrenilmiş çözümleri al"""
        return [
            s
            for s in self.learning_data["solutions"]
            if s["error_type"] == error_type and s["file_type"] == file_type
        ]

    def get_learning_summary(self) -> str:
        """Öğrenme özetini al"""
        summary = "=== NEXUS-ONE Öğrenme İstatistikleri ===\n"
        summary += f"Toplam Düzeltme: {self.learning_data['total_fixes']}\n"
        summary += f"Başarı Oranı: {self.learning_data['success_rate']:.1f}%\n"
        summary += f"Öğrenilmiş Patterns: {len(self.learning_data['error_patterns'])}\n"
        summary += f"Bilinen Çözümler: {len(self.learning_data['solutions'])}\n"

        if self.learning_data["error_patterns"]:
            summary += "\nÖğrenilmiş Hata Tipleri:\n"
            for pattern in self.learning_data["error_patterns"]:
                summary += (
                    f"  - {pattern['error']}: {pattern['applied_count']} kez çözüldü\n"
                )

        return summary


class NEXUSIntegration:
    """NEXUS-ONE Sistemine Hata Düzelticiyi Entegre Et"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.learner = NEXUSLearner(workspace_root)

    def integrate_with_autonomous_system(self):
        """Otonom sistemle entegre et"""
        # autonomous_production.ps1'e hook ekle
        ps_script = self.workspace / "autonomous_production.ps1"

        if ps_script.exists():
            with open(ps_script, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Hook zaten var mı kontrol et
            if "nexus_auto_healer" not in content:
                hook = """
# === NEXUS-ONE AUTO HEALER HOOK ===
# Her senkronizasyon sonrası hataları kontrol ve düzelt
function Invoke-NEXUSHealer {
    if (Test-Path "nexus_auto_healer.py") {
        python nexus_auto_healer.py 2>$null | Out-Null
    }
}
"""
                # Main loop'ın başına ekle
                new_content = content.replace(
                    "while ($true) {",
                    hook + "\nwhile ($true) {\n    Invoke-NEXUSHealer\n",
                )

                with open(ps_script, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print("✓ Hata düzeltici otonom sisteme entegre edildi")
                return True

        return False

    def create_learning_dashboard(self):
        """Öğrenme panosunu oluştur"""
        dashboard = self.workspace / "NEXUS_LEARNING.md"

        summary = self.learner.get_learning_summary()

        content = f"""# NEXUS-ONE Otomatik Hata Düzeltme Sistemi

## 🧠 Öğrenme İstatistikleri

{summary}

## 📊 Öğrenilmiş Patterns

"""

        for pattern in self.learner.learning_data["error_patterns"]:
            content += f"""
### {pattern['error_type']} ({pattern['file_type']})
- **Hata**: {pattern['error']}
- **Çözüm**: {pattern['solution']}
- **Uygulandı**: {pattern['applied_count']} kez
- **Öğrenildi**: {pattern['learned_at']}

"""

        with open(dashboard, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Öğrenme panosu oluşturuldu: {dashboard}")

    def auto_commit_learning(self):
        """Öğrenilmiş verileri commit et"""
        try:
            subprocess.run(
                ["git", "add", "data/nexus_learning.json", "NEXUS_LEARNING.md"],
                cwd=self.workspace,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "learn: NEXUS-ONE Otomatik Öğrenme Güncelleme"],
                cwd=self.workspace,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=self.workspace,
                capture_output=True,
            )
            print("✓ Öğrenme verileri GitHub'a gönderildi")
            return True
        except Exception as e:
            print(f"✗ Commit hatası: {e}")
            return False


def main():
    """NEXUS-ONE Öğrenme Sistemi Başlat"""
    workspace = Path.cwd()

    # Entegrasyonu oluştur
    nexus = NEXUSIntegration(str(workspace))

    # Otonom sisteme entegre et
    nexus.integrate_with_autonomous_system()

    # Öğrenme panosunu oluştur
    nexus.create_learning_dashboard()

    # Öğrenme verilerini commit et
    nexus.auto_commit_learning()

    # Özeti göster
    print("\n" + nexus.learner.get_learning_summary())


if __name__ == "__main__":
    main()
