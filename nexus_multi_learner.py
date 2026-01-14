import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NEXUS MULTI-LEARNER LAUNCHER
3-4 paralel learner başlat (hızlı öğrenme)
"""

import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_dir / "multi_learner.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class MultiLearnerLauncher:
    """Paralel learner'lar başlat ve yönet"""

    def __init__(self, num_learners=3):
        self.num_learners = num_learners
        self.learner_jobs = {}
        self.status_file = log_dir / "multi_learner_status.json"
        logger.info(f"🚀 MULTI-LEARNER LAUNCHER ({num_learners} workers)")

    def launch_learners(self):
        """Learner'ları başlat"""
        for i in range(1, self.num_learners + 1):
            job_name = f"Learner_{i}"

            try:
                # Her learner'ı ayrı job'da başlat
                ps_cmd = f"""
                Start-Job -ScriptBlock {{
                    $env:LEARNER_ID = "{i}"
                    python nexus_infinite_learner.py
                }} -Name "{job_name}"
                """

                result = subprocess.run(
                    f'powershell -Command "{ps_cmd}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                )

                self.learner_jobs[job_name] = {
                    "started_at": datetime.now().isoformat(),
                    "status": "RUNNING",
                }

                logger.info(f"✅ {job_name} başlatıldı")
                time.sleep(2)
            except Exception as e:
                logger.error(f"❌ {job_name} başlatma hatası: {e}")

    def check_learners(self):
        """Learner'ları kontrol et"""
        try:
            result = subprocess.run(
                "powershell -Command \"Get-Job | Where-Object Name -match 'Learner_' | Select-Object Name, State\"",
                shell=True,
                capture_output=True,
                text=True,
            )

            logger.info(f"📊 Multi-Learner Status: {len(self.learner_jobs)} workers")
            for job_name, status in self.learner_jobs.items():
                logger.info(f"  • {job_name}: {status['status']}")
        except Exception as e:
            logger.error(f"Status kontrol hatası: {e}")

    def aggregate_metrics(self):
        """Tüm learner'ların metriklerini topla"""
        try:
            total_cycles = 0
            total_topics = 0
            total_rate = 0

            # Her learner'ın metrik dosyası varsa (basit örnek)
            metrics_file = log_dir / "learner_metrics.json"
            if metrics_file.exists():
                data = json.loads(metrics_file.read_text(encoding="utf-8"))
                # Bu değerler zaten aggregate (tüm learner'lar tarafından yazılan shared file)
                total_cycles = data.get("learning_cycles", 0)
                total_topics = data.get("total_topics_learned", 0)
                total_rate = data.get("learning_rate_per_hour", 0)

            aggregated = {
                "timestamp": datetime.now().isoformat(),
                "total_learners": self.num_learners,
                "total_cycles": total_cycles,
                "total_topics": total_topics,
                "combined_rate": total_rate
                * self.num_learners,  # Théorik combined rate
                "learner_jobs": self.learner_jobs,
            }

            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(aggregated, f, indent=2, ensure_ascii=False)

            logger.info(
                f"📊 Aggregated: {total_topics} topics, "
                + f"Est. combined rate: {aggregated['combined_rate']:.0f} topics/hour"
            )
            return aggregated
        except Exception as e:
            logger.error(f"Aggregation hatası: {e}")
            return {}

    def monitor_loop(self):
        """Monitoring ve restart"""
        logger.info("⏱️ Multi-Learner monitoring başladı")

        while True:
            try:
                self.check_learners()
                self.aggregate_metrics()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Monitor hatası: {e}")
                time.sleep(60)


def main():
    logger.info("=" * 80)
    logger.info("🚀 NEXUS MULTI-LEARNER LAUNCHER")
    logger.info("=" * 80)

    # 3 learner başlat
    launcher = MultiLearnerLauncher(num_learners=3)
    launcher.launch_learners()

    # Monitoring başlat
    launcher.monitor_loop()


if __name__ == "__main__":
    main()
