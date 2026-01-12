#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NEXUS AGGRESSIVE IMPROVER - SÜPER HIZLI SÜREKLİ İYİLEŞTİRME
===============================================================
5 SANİYEDE BİR çalışır - çok hızlı, sürekli, beklemesiz!
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path


class AggressiveImprover:
    """Süper hızlı, agresif iyileştirici"""

    def __init__(self):
        self.workspace = Path(__file__).parent
        self.cycle = 0
        self.total_improved = 0

        print("\n" + "=" * 70)
        print("AGGRESSIVE IMPROVER - SUPER HIZLI MOD")
        print("=" * 70 + "\n")

    def quick_improve(self):
        """Hızlı iyileştirme"""
        self.cycle += 1

        print(f"\n{'='*60}")
        print(f"🔥 CYCLE #{self.cycle} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")

        # Python dosyalarını bul
        py_files = [
            f
            for f in self.workspace.glob("*.py")
            if f.name not in ["nexus_aggressive_improver.py", "nexus_instant_worker.py"]
        ]

        # Rastgele 3 dosya seç ve iyileştir
        import random

        targets = random.sample(py_files, min(3, len(py_files)))

        for target in targets:
            try:
                with open(target, "r", encoding="utf-8") as f:
                    content = f.read()

                original = content

                # Hızlı temizlik
                if "\n\n\n\n" in content:
                    content = content.replace("\n\n\n\n", "\n\n\n")

                lines = [line.rstrip() for line in content.split("\n")]
                content = "\n".join(lines)

                if content != original:
                    with open(target, "w", encoding="utf-8") as f:
                        f.write(content)

                    print(f"[OK] {target.name} - IYILESTIRILDI!", flush=True)
                    self.total_improved += 1
            except:
                pass

        print(f"\n[STATS] TOPLAM IYILESTIRME: {self.total_improved}")
        print(f"⏱️  5 saniye sonra devam...\n")
        sys.stdout.flush()

    def run(self):
        """Sürekli çalış"""
        print("[START] BASLIYOR - Her 5 saniyede calisacak!\n")

        while True:
            try:
                self.quick_improve()
                time.sleep(5)  # 5 saniye - çok hızlı!
            except KeyboardInterrupt:
                print("\n\n[STOP] DURDURULDU")
                print(
                    f"[STATS] TOPLAM {self.cycle} dongu, {self.total_improved} iyilestirme"
                )
                break
            except Exception as e:
                print(f"[ERROR] Hata: {e}")
                time.sleep(5)


if __name__ == "__main__":
    improver = AggressiveImprover()
    improver.run()
