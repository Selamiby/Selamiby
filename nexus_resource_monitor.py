import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💻 NEXUS-ONE RESOURCE MONITOR
CPU/GPU kaynakları monitör et, yüksek ise learner'ı pause et
"""

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_dir / "resource_monitor.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ResourceMonitor:
    """System kaynakları monitör et ve yönet"""

    def __init__(self):
        self.cpu_threshold = 80  # % (User request: increased for speed)
        self.ram_threshold = 85  # %
        self.pause_signal_file = log_dir / "learner_pause_signal.txt"
        self.metrics_file = log_dir / "resource_metrics.json"
        self.is_paused = False
        logger.info("💻 RESOURCE MONITOR BAŞLATILDI")

    def get_system_stats(self) -> dict:
        """Sistem istatistiklerini al"""
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # GPU kontrolü (basit - nvidia varsa)
        gpu_usage = "N/A"
        try:
            import GPUtil

            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = f"{gpus[0].load*100:.1f}%"
        except:
            gpu_usage = "N/A"

        stats = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": cpu,
            "ram_percent": ram.percent,
            "ram_used_gb": round(ram.used / (1024**3), 2),
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "disk_percent": disk.percent,
            "gpu_usage": gpu_usage,
            "cpu_warning": cpu > self.cpu_threshold,
            "ram_warning": ram.percent > self.ram_threshold,
        }
        return stats

    def should_pause_learning(self, stats: dict) -> bool:
        """Öğrenmeyi pause etmeli miyiz?"""
        if stats["cpu_warning"] or stats["ram_warning"]:
            return True
        return False

    def manage_pause_signal(self, should_pause: bool):
        """Pause sinyali dosyasını yönet"""
        try:
            if should_pause and not self.is_paused:
                # Pause sinyali gönder
                with open(self.pause_signal_file, "w", encoding="utf-8") as f:
                    f.write("PAUSE")
                self.is_paused = True
                logger.warning(
                    "⏸️ Learner PAUSE sinyali gönderildi (yüksek kaynak kullanımı)"
                )

            elif not should_pause and self.is_paused:
                # Pause sinyalini kaldır
                if self.pause_signal_file.exists():
                    self.pause_signal_file.unlink()
                self.is_paused = False
                logger.info("▶️ Learner RESUME sinyali gönderildi (kaynaklar normal)")
        except Exception as e:
            logger.error(f"Pause sinyal hatası: {e}")

    def log_metrics(self, stats: dict):
        """Metrikleri dosyaya kaydet"""
        try:
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Metrik kaydedilemedi: {e}")

    def monitor_loop(self):
        """Sürekli monitöring"""
        logger.info("🚀 Resource monitoring başladı (5s aralıklar)")

        while True:
            try:
                stats = self.get_system_stats()
                should_pause = self.should_pause_learning(stats)
                self.manage_pause_signal(should_pause)
                self.log_metrics(stats)

                # Log
                status = "⚠️ HIGH" if should_pause else "✅ OK"
                logger.info(
                    f"{status} | CPU: {stats['cpu_percent']:.1f}% | "
                    f"RAM: {stats['ram_percent']:.1f}% ({stats['ram_used_gb']}GB) | "
                    f"Paused: {self.is_paused}"
                )

                time.sleep(5)
            except Exception as e:
                logger.error(f"Monitor hatası: {e}")
                time.sleep(5)


def main():
    logger.info("=" * 80)
    logger.info("💻 NEXUS RESOURCE MONITOR")
    logger.info("=" * 80)

    monitor = ResourceMonitor()
    monitor.monitor_loop()


if __name__ == "__main__":
    main()
