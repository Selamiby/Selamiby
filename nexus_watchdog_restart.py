#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 NEXUS-ONE WATCHDOG RESTART
Job durursa/hata verirse kendini yeniden başlat
"""

import json
import logging
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_dir / "watchdog.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class NexusWatchdog:
    """Job'ları monitör et ve yeniden başlat"""

    def __init__(self):
        self.jobs_config = {
            "InfiniteLearner": {
                "command": "python nexus_infinite_learner.py",
                "restart_count": 0,
                "last_restart": None,
                "max_restarts": 10,
            },
            "Worker": {
                "command": "python nexus_realtime_worker.py",
                "restart_count": 0,
                "last_restart": None,
                "max_restarts": 10,
            },
        }
        self.heartbeat_timeout = 180  # 3 dakika
        self.status_file = log_dir / "watchdog_status.json"
        logger.info("🔄 WATCHDOG BAŞLATILDI")

    def check_job_heartbeat(self, job_name: str) -> bool:
        """Job'un nabzını kontrol et"""
        heartbeat_file = log_dir / f"{job_name.lower()}_heartbeat.txt"

        if not heartbeat_file.exists():
            logger.warning(f"⚠️ {job_name}: Heartbeat dosyası bulunamadı")
            return False

        try:
            last_beat = heartbeat_file.read_text().strip()
            last_time = datetime.fromisoformat(last_beat)
            age = (datetime.now() - last_time).total_seconds()

            if age > self.heartbeat_timeout:
                logger.error(
                    f"❌ {job_name}: Nabız gecikmiş ({int(age)}s). Yeniden başlatılıyor..."
                )
                return False
            else:
                logger.debug(f"✅ {job_name}: Nabız sağlıklı ({int(age)}s)")
                return True
        except Exception as e:
            logger.error(f"❌ {job_name}: Heartbeat kontrol hatası: {e}")
            return False

    def restart_job(self, job_name: str) -> bool:
        """Job'u yeniden başlat"""
        config = self.jobs_config[job_name]

        if config["restart_count"] >= config["max_restarts"]:
            logger.error(
                f"🛑 {job_name}: Max restart sayısına ulaşıldı ({config['max_restarts']})"
            )
            return False

        try:
            # Job'u durdur
            subprocess.run(
                f'powershell -Command "Stop-Job -Name {job_name} -ErrorAction SilentlyContinue; Remove-Job -Name {job_name} -ErrorAction SilentlyContinue"',
                shell=True,
                capture_output=True,
            )

            time.sleep(2)

            # Yeniden başlat
            ps_cmd = f'powershell -Command "Start-Job -ScriptBlock {{ {config["command"]} }} -Name {job_name}"'
            result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)

            config["restart_count"] += 1
            config["last_restart"] = datetime.now().isoformat()

            logger.info(
                f"🔄 {job_name}: Başarıyla yeniden başlatıldı (Attempt #{config['restart_count']})"
            )
            self._save_status()
            return True
        except Exception as e:
            logger.error(f"❌ {job_name}: Yeniden başlatma hatası: {e}")
            return False

    def _save_status(self):
        """Status dosyasını kaydet"""
        try:
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(self.jobs_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Status kaydedilemedi: {e}")

    def monitor_loop(self):
        """Sürekli monitöring döngüsü"""
        logger.info("🚀 Watchdog monitoring başladı (60s aralıklar)")

        while True:
            try:
                for job_name in self.jobs_config.keys():
                    if not self.check_job_heartbeat(job_name):
                        logger.warning(
                            f"⚠️ {job_name}: Heartbeat başarısız, yeniden başlatılıyor..."
                        )
                        self.restart_job(job_name)

                # 60 saniye bekle
                time.sleep(60)
            except Exception as e:
                logger.error(f"Monitor loop hatası: {e}")
                time.sleep(60)
                continue


def main():
    logger.info("=" * 80)
    logger.info("🔄 NEXUS WATCHDOG RESTART ENGINE")
    logger.info("=" * 80)

    watchdog = NexusWatchdog()
    watchdog.monitor_loop()


if __name__ == "__main__":
    main()
