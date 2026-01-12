#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ NEXUS INSTANT WORKER - ANLIK HIZLI ÇALIŞMA (BEKLEMESIZ!)
============================================================
Döngü yok, bekleme yok - ANINDA çalış, HEMEN sonuç göster!
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List


def log(msg: str, color: str = "white"):
    """Renkli log"""
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{colors.get(color, '')}{timestamp} {msg}{colors['reset']}", flush=True)


class InstantWorker:
    """Anlık hızlı çalışma - beklemesiz!"""

    def __init__(self):
        self.workspace = Path(__file__).parent
        self.improvements = 0

        log("🔥 INSTANT WORKER BAŞLATILDI!", "green")
        log("⚡ BEKLEMESIZ ANLIK ÇALIŞMA MODU!", "yellow")

    def improve_file_instantly(self, filepath: Path) -> bool:
        """Dosyayı ANINDA iyileştir"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            changes = []

            # 1. Fazla boş satırları temizle
            while "\n\n\n\n" in content:
                content = content.replace("\n\n\n\n", "\n\n\n")
                changes.append("Fazla boş satır")

            # 2. Trailing whitespace
            lines = content.split("\n")
            cleaned = [line.rstrip() for line in lines]
            if cleaned != lines:
                content = "\n".join(cleaned)
                changes.append("Whitespace temizlendi")

            # 3. Tab to space
            if "\t" in content:
                content = content.replace("\t", "    ")
                changes.append("Tab→Space")

            # Kaydet
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                log(f"✅ {filepath.name}: {', '.join(changes)}", "green")
                self.improvements += 1
                return True

            return False

        except Exception as e:
            log(f"❌ {filepath.name}: {e}", "red")
            return False

    def run_instant_batch(self):
        """Toplu anlık çalışma - beklemesiz!"""
        log("\n" + "=" * 70, "cyan")
        log("🚀 INSTANT BATCH BAŞLIYOR - BEKLEMESIZ!", "yellow")
        log("=" * 70, "cyan")

        # Tüm Python dosyalarını bul
        py_files = [
            f
            for f in self.workspace.glob("*.py")
            if f.name not in ["nexus_instant_worker.py"]
        ]

        log(f"\n📊 {len(py_files)} dosya taranacak...", "cyan")

        # HER BİRİNİ HEMEN İYİLEŞTİR
        for i, py_file in enumerate(py_files[:20], 1):  # İlk 20 dosya
            log(f"\n[{i}/20] İşleniyor: {py_file.name}", "magenta")
            self.improve_file_instantly(py_file)
            sys.stdout.flush()  # HEMEN göster

        # SONUÇ
        log("\n" + "=" * 70, "cyan")
        log(f"✅ TAMAMLANDI! {self.improvements} dosya iyileştirildi!", "green")
        log("=" * 70, "cyan")


if __name__ == "__main__":
    worker = InstantWorker()
    worker.run_instant_batch()

    log("\n💡 İyileştirmeler HEMEN uygulandı, beklemede değil!", "yellow")
