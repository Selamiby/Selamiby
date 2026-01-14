import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

"""
AetherOS System Monitor - Gerçek Zamanlı Sistem İzleme
"""

import psutil
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
import threading
import time
from collections import deque
import warnings


@dataclass
class SystemMetrics:
    """Sistem metrikleri"""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_sent_mb: float
    network_recv_mb: float
    processes_count: int
    boot_time: datetime
    uptime_seconds: float


@dataclass
class ProcessInfo:
    """Process bilgileri"""

    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str
    create_time: datetime
    cmdline: List[str]


class SystemMonitor:
    """Gerçek zamanlı sistem izleyici"""

    def __init__(self, update_interval: int = 5):
        self.update_interval = update_interval
        self.metrics_history = deque(maxlen=1000)  # Son 1000 ölçüm
        self.alerts = []
        self.is_monitoring = False
        self.monitor_thread = None

        # Threshold'lar
        self.thresholds = {
            "cpu_warning": 80.0,
            "cpu_critical": 95.0,
            "memory_warning": 85.0,
            "memory_critical": 95.0,
            "disk_warning": 90.0,
            "disk_critical": 98.0,
        }

        # Sistem bilgileri
        self.system_info = self._get_system_info()

    def _get_system_info(self) -> Dict[str, Any]:
        """Sistem bilgilerini al"""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "total_memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()),
            "timestamp": datetime.now(),
        }

    def collect_metrics(self) -> SystemMetrics:
        """Anlık sistem metriklerini topla"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)

        # Memory
        memory = psutil.virtual_memory()

        # Disk (ana dizin)
        disk = (
            psutil.disk_usage("/")
            if platform.system() != "Windows"
            else psutil.disk_usage("C:\\")
        )

        # Network
        net_io = psutil.net_io_counters()

        # Processes
        processes = list(psutil.process_iter(["pid", "name"]))

        metrics = SystemMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            disk_usage_percent=disk.percent,
            network_sent_mb=net_io.bytes_sent / (1024**2),
            network_recv_mb=net_io.bytes_recv / (1024**2),
            processes_count=len(processes),
            boot_time=datetime.fromtimestamp(psutil.boot_time()),
            uptime_seconds=(
                datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            ).total_seconds(),
        )

        return metrics

    def check_thresholds(self, metrics: SystemMetrics) -> List[Dict]:
        """Threshold kontrolü yap ve alert üret"""
        alerts = []

        # CPU kontrolü
        if metrics.cpu_percent >= self.thresholds["cpu_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "CPU",
                    "value": metrics.cpu_percent,
                    "threshold": self.thresholds["cpu_critical"],
                    "message": f"CPU usage critically high: {metrics.cpu_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )
        elif metrics.cpu_percent >= self.thresholds["cpu_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "CPU",
                    "value": metrics.cpu_percent,
                    "threshold": self.thresholds["cpu_warning"],
                    "message": f"CPU usage high: {metrics.cpu_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )

        # Memory kontrolü
        if metrics.memory_percent >= self.thresholds["memory_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "Memory",
                    "value": metrics.memory_percent,
                    "threshold": self.thresholds["memory_critical"],
                    "message": f"Memory usage critically high: {metrics.memory_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )
        elif metrics.memory_percent >= self.thresholds["memory_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "Memory",
                    "value": metrics.memory_percent,
                    "threshold": self.thresholds["memory_warning"],
                    "message": f"Memory usage high: {metrics.memory_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )

        # Disk kontrolü
        if metrics.disk_usage_percent >= self.thresholds["disk_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "Disk",
                    "value": metrics.disk_usage_percent,
                    "threshold": self.thresholds["disk_critical"],
                    "message": f"Disk usage critically high: {metrics.disk_usage_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )
        elif metrics.disk_usage_percent >= self.thresholds["disk_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "Disk",
                    "value": metrics.disk_usage_percent,
                    "threshold": self.thresholds["disk_warning"],
                    "message": f"Disk usage high: {metrics.disk_usage_percent:.1f}%",
                    "timestamp": metrics.timestamp.isoformat(),
                }
            )

        return alerts

    def get_top_processes(self, n: int = 10, sort_by: str = "cpu") -> List[ProcessInfo]:
        """En çok kaynak kullanan process'leri getir"""
        processes = []

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "cpu_percent",
                "memory_percent",
                "status",
                "create_time",
                "cmdline",
            ]
        ):
            try:
                # CPU yüzdesini güncelle
                proc.cpu_percent()
            except:
                continue

        # 0.1 saniye bekle
        time.sleep(0.1)

        # Process'leri topla
        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "cpu_percent",
                "memory_percent",
                "status",
                "create_time",
                "cmdline",
            ]
        ):
            try:
                pinfo = proc.info
                processes.append(
                    ProcessInfo(
                        pid=pinfo["pid"],
                        name=pinfo["name"] or "Unknown",
                        cpu_percent=pinfo["cpu_percent"] or 0.0,
                        memory_percent=pinfo["memory_percent"] or 0.0,
                        status=pinfo["status"],
                        create_time=(
                            datetime.fromtimestamp(pinfo["create_time"])
                            if pinfo["create_time"]
                            else datetime.now()
                        ),
                        cmdline=pinfo["cmdline"] or [],
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sırala
        if sort_by == "cpu":
            processes.sort(key=lambda x: x.cpu_percent, reverse=True)
        elif sort_by == "memory":
            processes.sort(key=lambda x: x.memory_percent, reverse=True)

        return processes[:n]

    def get_disk_info(self) -> List[Dict]:
        """Tüm disk bölümlerinin bilgilerini getir"""
        disk_info = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append(
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent": usage.percent,
                    }
                )
            except:
                continue

        return disk_info

    def monitor_loop(self):
        """Monitoring döngüsü"""
        while self.is_monitoring:
            try:
                # Metrikleri topla
                metrics = self.collect_metrics()
                self.metrics_history.append(metrics)

                # Alert kontrolü
                alerts = self.check_thresholds(metrics)
                if alerts:
                    self.alerts.extend(alerts)
                    # Alert'leri logla (ileride dosyaya da yazabiliriz)
                    for alert in alerts:
                        print(f"[{alert['level']}] {alert['message']}")

                # Bekle
                time.sleep(self.update_interval)

            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(self.update_interval)

    def start_monitoring(self):
        """Monitoring'i başlat"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(
                target=self.monitor_loop, daemon=True
            )
            self.monitor_thread.start()
            print(f"✅ System monitoring started (interval: {self.update_interval}s)")

    def stop_monitoring(self):
        """Monitoring'i durdur"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("✅ System monitoring stopped")

    def get_metrics_summary(self, hours: int = 1) -> Dict:
        """Belirli saat aralığındaki metrik özetini getir"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]

        if not recent_metrics:
            return {"error": "No recent metrics available"}

        return {
            "time_range": {
                "from": recent_metrics[0].timestamp.isoformat(),
                "to": recent_metrics[-1].timestamp.isoformat(),
                "duration_hours": hours,
            },
            "averages": {
                "cpu_percent": round(
                    sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics), 2
                ),
                "memory_percent": round(
                    sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
                    2,
                ),
                "disk_usage_percent": round(
                    sum(m.disk_usage_percent for m in recent_metrics)
                    / len(recent_metrics),
                    2,
                ),
            },
            "maximums": {
                "cpu_percent": round(max(m.cpu_percent for m in recent_metrics), 2),
                "memory_percent": round(
                    max(m.memory_percent for m in recent_metrics), 2
                ),
                "disk_usage_percent": round(
                    max(m.disk_usage_percent for m in recent_metrics), 2
                ),
            },
            "alerts_count": len(
                [
                    a
                    for a in self.alerts
                    if datetime.fromisoformat(a["timestamp"]) > cutoff_time
                ]
            ),
            "metrics_count": len(recent_metrics),
        }

    def cleanup_old_data(self, days_to_keep: int = 7):
        """Eski verileri temizle"""
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)

        # Eski metrikleri temizle
        initial_count = len(self.metrics_history)
        self.metrics_history = deque(
            [m for m in self.metrics_history if m.timestamp > cutoff_time], maxlen=1000
        )

        # Eski alert'leri temizle
        initial_alerts = len(self.alerts)
        self.alerts = [
            a
            for a in self.alerts
            if datetime.fromisoformat(a["timestamp"]) > cutoff_time
        ]

        return {
            "metrics_removed": initial_count - len(self.metrics_history),
            "alerts_removed": initial_alerts - len(self.alerts),
            "cutoff_time": cutoff_time.isoformat(),
        }

    def to_dict(self) -> Dict:
        """Nesneyi dictionary'e çevir"""
        return {
            "system_info": self.system_info,
            "current_metrics": (
                asdict(self.collect_metrics()) if self.metrics_history else {}
            ),
            "thresholds": self.thresholds,
            "alerts_count": len(self.alerts),
            "metrics_history_count": len(self.metrics_history),
            "is_monitoring": self.is_monitoring,
            "update_interval": self.update_interval,
        }


# Kullanım örneği
if __name__ == "__main__":
    monitor = SystemMonitor(update_interval=2)

    print("=== SYSTEM MONITOR TEST ===")
    print(
        f"System: {monitor.system_info['platform']} {monitor.system_info['platform_release']}"
    )
    print(f"CPU: {monitor.system_info['cpu_count_logical']} logical cores")
    print(f"Memory: {monitor.system_info['total_memory_gb']} GB")

    # Test ölçümü
    metrics = monitor.collect_metrics()
    print(f"\nCurrent Metrics:")
    print(f"  CPU: {metrics.cpu_percent:.1f}%")
    print(f"  Memory: {metrics.memory_percent:.1f}%")
    print(f"  Disk: {metrics.disk_usage_percent:.1f}%")
    print(f"  Processes: {metrics.processes_count}")

    # Top processes
    print(f"\nTop 5 Processes by CPU:")
    for i, proc in enumerate(monitor.get_top_processes(5, "cpu"), 1):
        print(f"  {i}. {proc.name} (PID: {proc.pid}): {proc.cpu_percent:.1f}% CPU")

    # Disk info
    print(f"\nDisk Information:")
    for disk in monitor.get_disk_info():
        print(
            f"  {disk['mountpoint']}: {disk['used_gb']:.1f}/{disk['total_gb']:.1f} GB ({disk['percent']:.1f}%)"
        )
