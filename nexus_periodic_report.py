import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:23
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 NEXUS PERIODIC REPORT GENERATOR
Saatlik/Günlük özet rapor oluştur
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_dir / "periodic_report.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class PeriodicReportGenerator:
    """Periyodik rapor üreteci"""

    def __init__(self):
        self.metrics_file = log_dir / "learner_metrics.json"
        self.reports_dir = log_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.last_hourly = None
        self.last_daily = None
        logger.info("📊 PERIODIC REPORT GENERATOR BAŞLATILDI")

    def get_current_metrics(self):
        """Mevcut metrikleri al"""
        try:
            if self.metrics_file.exists():
                return json.loads(self.metrics_file.read_text(encoding="utf-8"))
            return {}
        except:
            return {}

    def generate_hourly_report(self):
        """Saatlik rapor oluştur"""
        metrics = self.get_current_metrics()

        report = {
            "type": "HOURLY",
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "summary": {
                "cycles": metrics.get("learning_cycles", 0),
                "topics_learned": metrics.get("total_topics_learned", 0),
                "rate": metrics.get("learning_rate_per_hour", 0),
                "uptime_hours": metrics.get("uptime_hours", 0),
                "top_3_domains": metrics.get("top_domains", [])[:3],
            },
        }

        # Raporu kaydet
        filename = f"hourly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.reports_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(
                f"📊 Hourly Report: {report['summary']['cycles']} cycles, "
                + f"{report['summary']['topics_learned']} topics"
            )
            return report
        except Exception as e:
            logger.error(f"Hourly report hatası: {e}")
            return None

    def generate_daily_report(self):
        """Günlük rapor oluştur"""
        metrics = self.get_current_metrics()

        # Tüm hourly raporları oku ve özet yap
        hourly_reports = sorted(self.reports_dir.glob("hourly_*.json"))

        total_cycles = 0
        total_topics = 0
        max_rate = 0

        for report_file in hourly_reports[-24:]:  # Son 24 saat
            try:
                report = json.loads(report_file.read_text(encoding="utf-8"))
                total_cycles += report["summary"]["cycles"]
                total_topics += report["summary"]["topics_learned"]
                max_rate = max(max_rate, report["summary"]["rate"])
            except:
                pass

        report = {
            "type": "DAILY",
            "timestamp": datetime.now().isoformat(),
            "daily_summary": {
                "total_cycles": total_cycles,
                "total_topics_learned": total_topics,
                "max_learning_rate": max_rate,
                "avg_rate": total_topics / 24 if total_topics > 0 else 0,
                "top_domains": metrics.get("top_domains", [])[:5],
            },
            "metrics": metrics,
        }

        # Raporu kaydet
        filename = f"daily_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = self.reports_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(
                f"📊 Daily Report: {report['daily_summary']['total_cycles']} cycles, "
                + f"{report['daily_summary']['total_topics_learned']} topics/day"
            )
            return report
        except Exception as e:
            logger.error(f"Daily report hatası: {e}")
            return None

    def generate_text_summary(self, report_type="hourly"):
        """Metin özeti oluştur (display için)"""
        if report_type == "hourly":
            report = self.generate_hourly_report()
            if not report:
                return ""

            summary = report["summary"]
            text = f"""
╔════════════════════════════════════════════════════════════════╗
║            📊 HOURLY LEARNING REPORT                           ║
╚════════════════════════════════════════════════════════════════╝
⏰ Timestamp: {report['timestamp']}
🔄 Learning Cycles: {summary['cycles']}
📚 Topics Learned: {summary['topics_learned']}
⚡ Learning Rate: {summary['rate']:.1f} topics/hour
⏱️ Uptime: {summary['uptime_hours']:.2f} hours

🏆 Top 3 Domains:
"""
            for domain, count in summary["top_3_domains"]:
                text += f"   • {domain.replace('_', ' ').title()}: {count} topics\n"

            return text

        elif report_type == "daily":
            report = self.generate_daily_report()
            if not report:
                return ""

            summary = report["daily_summary"]
            text = f"""
╔════════════════════════════════════════════════════════════════╗
║            📊 DAILY LEARNING REPORT                            ║
╚════════════════════════════════════════════════════════════════╝
📅 Date: {report['timestamp'].split('T')[0]}
🔄 Total Cycles (24h): {summary['total_cycles']}
📚 Total Topics Learned: {summary['total_topics_learned']}
⚡ Max Rate: {summary['max_learning_rate']:.1f} topics/hour
📈 Avg Rate: {summary['avg_rate']:.1f} topics/hour

🏆 Top Domains:
"""
            for domain, count in summary["top_domains"]:
                text += f"   • {domain.replace('_', ' ').title()}: {count} topics\n"

            return text

        return ""

    def monitor_loop(self):
        """Periyodik rapor monitoring"""
        logger.info("⏱️ Periodic reporting başladı")

        while True:
            try:
                now = datetime.now()

                # Saatlik rapor (her saat başında)
                if (
                    self.last_hourly is None
                    or (now - self.last_hourly).total_seconds() >= 3600
                ):
                    report = self.generate_hourly_report()
                    if report:
                        print(self.generate_text_summary("hourly"))
                        self.last_hourly = now

                # Günlük rapor (her gün 00:00'de)
                if (
                    self.last_daily is None
                    or (now - self.last_daily).total_seconds() >= 86400
                ):
                    report = self.generate_daily_report()
                    if report:
                        print(self.generate_text_summary("daily"))
                        self.last_daily = now

                time.sleep(60)  # Her dakika kontrol et
            except Exception as e:
                logger.error(f"Monitor loop hatası: {e}")
                time.sleep(60)


def main():
    logger.info("=" * 80)
    logger.info("📊 NEXUS PERIODIC REPORT GENERATOR")
    logger.info("=" * 80)

    generator = PeriodicReportGenerator()
    generator.monitor_loop()


if __name__ == "__main__":
    main()
