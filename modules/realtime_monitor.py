"""
Seviye 3: İLERİ OTONOM SİSTEMLER
Gerçek Zamanlı İzleme - Sistem kaynakları, anomali tespiti, acil durum protokolleri
"""

import json
import threading
import time
from collections import deque
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import psutil


class AlertLevel(Enum):
    """Uyarı seviyesi"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class Alert:
    """Sistem uyarısı"""

    def __init__(
        self,
        alert_id: str,
        level: AlertLevel,
        component: str,
        message: str,
        threshold: Optional[float] = None,
        current_value: Optional[float] = None,
    ):
        self.id: str = alert_id
        self.level: AlertLevel = level
        self.component: str = component
        self.message: str = message
        self.threshold: Optional[float] = threshold
        self.current_value: Optional[float] = current_value
        self.created_at: datetime = datetime.now()
        self.acknowledged: bool = False
        self.acknowledged_at: Optional[datetime] = None
        self.action_taken: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "level": self.level.value,
            "component": self.component,
            "message": self.message,
            "threshold": self.threshold,
            "current_value": self.current_value,
            "created_at": self.created_at.isoformat(),
            "acknowledged": self.acknowledged,
            "action_taken": self.action_taken,
        }


class MetricSnapshot:
    """Metrik anlık görüntüsü"""

    def __init__(self):
        self.timestamp = datetime.now()
        self.cpu_percent = psutil.cpu_percent(interval=0.1)
        self.memory_percent = psutil.virtual_memory().percent
        self.disk_percent = psutil.disk_usage("/").percent
        self.network_io = psutil.net_io_counters()
        self.process_count = len(psutil.pids())
        self.disk_io = psutil.disk_io_counters() if psutil.disk_io_counters() else None

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "disk_percent": self.disk_percent,
            "process_count": self.process_count,
            "network_bytes_sent": self.network_io.bytes_sent,
            "network_bytes_recv": self.network_io.bytes_recv,
            "disk_read_bytes": self.disk_io.read_bytes if self.disk_io else 0,
            "disk_write_bytes": self.disk_io.write_bytes if self.disk_io else 0,
        }


class RealtimeMonitor:
    """Gerçek zamanlı izleme sistemi"""

    def __init__(
        self, history_size: int = 3600
    ):  # 1 saatlik geçmiş (60 dakika * 60 saniye)
        self.is_monitoring = False
        self.monitor_thread = None
        self.history = deque(maxlen=history_size)
        self.alerts: Dict[str, Alert] = {}
        self.anomalies: List[Dict] = []
        self.thresholds = {
            "cpu_warning": 75,
            "cpu_critical": 90,
            "memory_warning": 80,
            "memory_critical": 95,
            "disk_warning": 80,
            "disk_critical": 95,
            "process_warning": 500,
        }

        # Anomali tespiti bazları
        self.baselines = {"cpu_avg": 30, "memory_avg": 50, "disk_io_avg": 100}  # MB/s

        self.alert_log_path = Path("data/alerts.json")
        self.metrics_log_path = Path("data/metrics.json")

    def start_monitoring(self, interval: int = 1) -> Dict:
        """İzlemeyi başlat"""
        if self.is_monitoring:
            return {"error": "Monitoring already running"}

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,), daemon=True
        )
        self.monitor_thread.start()

        return {
            "success": True,
            "status": "monitoring_started",
            "interval_seconds": interval,
        }

    def stop_monitoring(self) -> Dict:
        """İzlemeyi durdur"""
        self.is_monitoring = False

        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

        return {
            "success": True,
            "status": "monitoring_stopped",
            "alerts_count": len(self.alerts),
            "anomalies_count": len(self.anomalies),
        }

    def _monitor_loop(self, interval: int):
        """İzleme döngüsü"""
        while self.is_monitoring:
            try:
                snapshot = MetricSnapshot()
                self.history.append(snapshot)

                # Eşik kontrolleri
                self._check_thresholds(snapshot)

                # Anomali tespiti
                self._detect_anomalies(snapshot)

                time.sleep(interval)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(interval)

    def _check_thresholds(self, snapshot: MetricSnapshot):
        """Eşikleri kontrol et"""

        # CPU kontrolü
        if snapshot.cpu_percent >= self.thresholds["cpu_critical"]:
            self._create_alert(
                "cpu_critical",
                AlertLevel.CRITICAL,
                "CPU",
                f"CPU usage critical: {snapshot.cpu_percent:.1f}%",
                self.thresholds["cpu_critical"],
                snapshot.cpu_percent,
            )
        elif snapshot.cpu_percent >= self.thresholds["cpu_warning"]:
            self._create_alert(
                "cpu_warning",
                AlertLevel.WARNING,
                "CPU",
                f"CPU usage high: {snapshot.cpu_percent:.1f}%",
                self.thresholds["cpu_warning"],
                snapshot.cpu_percent,
            )

        # Bellek kontrolü
        if snapshot.memory_percent >= self.thresholds["memory_critical"]:
            self._create_alert(
                "memory_critical",
                AlertLevel.CRITICAL,
                "Memory",
                f"Memory usage critical: {snapshot.memory_percent:.1f}%",
                self.thresholds["memory_critical"],
                snapshot.memory_percent,
            )
        elif snapshot.memory_percent >= self.thresholds["memory_warning"]:
            self._create_alert(
                "memory_warning",
                AlertLevel.WARNING,
                "Memory",
                f"Memory usage high: {snapshot.memory_percent:.1f}%",
                self.thresholds["memory_warning"],
                snapshot.memory_percent,
            )

        # Disk kontrolü
        if snapshot.disk_percent >= self.thresholds["disk_critical"]:
            self._create_alert(
                "disk_critical",
                AlertLevel.CRITICAL,
                "Disk",
                f"Disk usage critical: {snapshot.disk_percent:.1f}%",
                self.thresholds["disk_critical"],
                snapshot.disk_percent,
            )
        elif snapshot.disk_percent >= self.thresholds["disk_warning"]:
            self._create_alert(
                "disk_warning",
                AlertLevel.WARNING,
                "Disk",
                f"Disk usage high: {snapshot.disk_percent:.1f}%",
                self.thresholds["disk_warning"],
                snapshot.disk_percent,
            )

        # Process sayısı kontrolü
        if snapshot.process_count >= self.thresholds["process_warning"]:
            self._create_alert(
                "process_warning",
                AlertLevel.WARNING,
                "Processes",
                f"High process count: {snapshot.process_count}",
                self.thresholds["process_warning"],
                snapshot.process_count,
            )

    def _detect_anomalies(self, snapshot: MetricSnapshot):
        """Anomalileri tespit et"""
        if len(self.history) < 10:
            return

        recent_snapshots = list(self.history)[-10:]

        # CPU anomalisi
        cpu_values = [s.cpu_percent for s in recent_snapshots]
        cpu_avg = sum(cpu_values) / len(cpu_values)
        cpu_std = (sum((x - cpu_avg) ** 2 for x in cpu_values) / len(cpu_values)) ** 0.5

        if snapshot.cpu_percent > cpu_avg + (2 * cpu_std) and cpu_std > 5:
            self._create_anomaly(
                "cpu_spike",
                f"CPU spike detected: {snapshot.cpu_percent:.1f}% (avg: {cpu_avg:.1f}%)",
                {
                    "type": "cpu_spike",
                    "value": snapshot.cpu_percent,
                    "average": cpu_avg,
                },
            )

        # Bellek anomalisi
        memory_values = [s.memory_percent for s in recent_snapshots]
        memory_avg = sum(memory_values) / len(memory_values)
        memory_std = (
            sum((x - memory_avg) ** 2 for x in memory_values) / len(memory_values)
        ) ** 0.5

        if snapshot.memory_percent > memory_avg + (2 * memory_std) and memory_std > 5:
            self._create_anomaly(
                "memory_spike",
                f"Memory spike detected: {snapshot.memory_percent:.1f}% (avg: {memory_avg:.1f}%)",
                {
                    "type": "memory_spike",
                    "value": snapshot.memory_percent,
                    "average": memory_avg,
                },
            )

        # Disk I/O anomalisi
        disk_io_current = (
            (snapshot.disk_io.read_bytes + snapshot.disk_io.write_bytes)
            if snapshot.disk_io
            else 0
        )

        if len(recent_snapshots) > 1:
            disk_io_prev = (
                (
                    recent_snapshots[-2].disk_io.read_bytes
                    + recent_snapshots[-2].disk_io.write_bytes
                )
                if recent_snapshots[-2].disk_io
                else 0
            )
            disk_io_rate = (disk_io_current - disk_io_prev) / (1024 * 1024)  # MB

            if disk_io_rate > 1000:  # 1000 MB burst
                self._create_anomaly(
                    "disk_io_spike",
                    f"High disk I/O detected: {disk_io_rate:.1f} MB",
                    {"type": "disk_io_spike", "rate_mb": disk_io_rate},
                )

    def _create_alert(
        self,
        alert_id: str,
        level: AlertLevel,
        component: str,
        message: str,
        threshold: float,
        current_value: float,
    ):
        """Uyarı oluştur"""
        # Aynı uyarı 30 saniye içinde tekrar oluşturulmasın
        if alert_id in self.alerts:
            existing = self.alerts[alert_id]
            if (datetime.now() - existing.created_at).total_seconds() < 30:
                return

        alert = Alert(alert_id, level, component, message, threshold, current_value)
        self.alerts[alert_id] = alert

        # Acil durum durumunda protokol çalıştır
        if level == AlertLevel.EMERGENCY:
            self._execute_emergency_protocol(alert)

    def _create_anomaly(self, anomaly_type: str, description: str, details: Dict):
        """Anomali oluştur"""
        anomaly = {
            "type": anomaly_type,
            "description": description,
            "details": details,
            "detected_at": datetime.now().isoformat(),
            "severity": "medium",
        }

        self.anomalies.append(anomaly)

        # Son 100 anomaliyi tut
        if len(self.anomalies) > 100:
            self.anomalies = self.anomalies[-100:]

    def _execute_emergency_protocol(self, alert: Alert):
        """Acil durum protokolü çalıştır"""
        alert.action_taken = "emergency_protocol_initiated"

        # Burada uygulamanıza özel acil durum işlemleri yapılır
        # Örn: kritik işlemleri durdur, sistem kaynaklarını serbest bırak, vb.

    def acknowledge_alert(self, alert_id: str) -> Dict:
        """Uyarıyı onayla"""
        if alert_id not in self.alerts:
            return {"error": f"Alert {alert_id} not found"}

        alert = self.alerts[alert_id]
        alert.acknowledged = True
        alert.acknowledged_at = datetime.now()

        return {
            "success": True,
            "alert_id": alert_id,
            "acknowledged_at": alert.acknowledged_at.isoformat(),
        }

    def get_current_status(self) -> Dict:
        """Güncel durumu al"""
        if not self.history:
            return {"error": "No data collected yet"}

        latest = self.history[-1]

        # Son 10 verinin ortalaması
        recent = list(self.history)[-10:]
        avg_cpu = sum(s.cpu_percent for s in recent) / len(recent)
        avg_memory = sum(s.memory_percent for s in recent) / len(recent)

        # Uyarı özeti
        critical_alerts = [
            a for a in self.alerts.values() if a.level == AlertLevel.CRITICAL
        ]
        warning_alerts = [
            a for a in self.alerts.values() if a.level == AlertLevel.WARNING
        ]

        health_status = "HEALTHY"
        if critical_alerts:
            health_status = "CRITICAL"
        elif warning_alerts or self.anomalies[-5:]:  # Son 5 anomali
            health_status = "WARNING"

        return {
            "health_status": health_status,
            "timestamp": latest.timestamp.isoformat(),
            "cpu": {"current": latest.cpu_percent, "average_10s": round(avg_cpu, 1)},
            "memory": {
                "current": latest.memory_percent,
                "average_10s": round(avg_memory, 1),
            },
            "disk": latest.disk_percent,
            "processes": latest.process_count,
            "alerts": {
                "critical": len(critical_alerts),
                "warning": len(warning_alerts),
                "total": len(self.alerts),
            },
            "anomalies_detected": len(self.anomalies),
        }

    def get_alerts(
        self, level: Optional[AlertLevel] = None, unacknowledged_only: bool = True
    ) -> Dict:
        """Uyarıları al"""
        alerts = list(self.alerts.values())

        if level:
            alerts = [a for a in alerts if a.level == level]

        if unacknowledged_only:
            alerts = [a for a in alerts if not a.acknowledged]

        return {"total": len(alerts), "alerts": [a.to_dict() for a in alerts]}

    def get_anomalies(self, limit: int = 50) -> Dict:
        """Anomalileri al"""
        recent_anomalies = self.anomalies[-limit:] if self.anomalies else []

        return {"total": len(self.anomalies), "recent": recent_anomalies}

    def get_metrics_history(self, minutes: int = 10) -> Dict:
        """Metrik geçmişini al"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)

        filtered_history = [s for s in self.history if s.timestamp > cutoff_time]

        return {
            "time_range_minutes": minutes,
            "data_points": len(filtered_history),
            "metrics": [s.to_dict() for s in filtered_history],
        }

    def save_logs(self) -> Dict:
        """Günlükleri kaydet"""
        self.alert_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.metrics_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Uyarıları kaydet
        alerts_data = [a.to_dict() for a in self.alerts.values()]
        with open(self.alert_log_path, "w") as f:
            json.dump(alerts_data, f, indent=2, default=str)

        # Metrikleri kaydet
        metrics_data = [s.to_dict() for s in self.history]
        with open(self.metrics_log_path, "w") as f:
            json.dump(metrics_data, f, indent=2, default=str)

        return {
            "success": True,
            "alerts_saved": len(alerts_data),
            "metrics_saved": len(metrics_data),
        }


# Global instance
realtime_monitor = RealtimeMonitor()
