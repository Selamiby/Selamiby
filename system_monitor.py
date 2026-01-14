import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

"""
system_monitor.py - GERÇEK SİSTEM İZLEME
"""

import json
import logging
import platform
import socket
import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import GPUtil
import psutil


@dataclass
class SystemMetrics:
    """Sistem metrikleri"""

    timestamp: str
    cpu_percent: float
    cpu_freq_current: float
    cpu_freq_max: float
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_total: int
    disk_used: int
    disk_percent: float
    network_sent: int
    network_recv: int
    processes: int
    boot_time: float
    uptime: float


class SystemMonitor:
    """Gerçek sistem izleyici"""

    def __init__(self, log_interval: int = 60):
        self.log_interval = log_interval
        self.metrics_history = []
        self.alerts = []
        self.is_monitoring = False
        self.monitor_thread = None

        # Logging
        self.logger = logging.getLogger("SystemMonitor")

        # Threshold'lar
        self.thresholds = {
            "cpu_warning": 80.0,
            "cpu_critical": 95.0,
            "memory_warning": 85.0,
            "memory_critical": 95.0,
            "disk_warning": 80.0,
            "disk_critical": 90.0,
            "temperature_warning": 80.0,
            "temperature_critical": 90.0,
        }

    def get_current_metrics(self) -> SystemMetrics:
        """Güncel sistem metriklerini al"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq()

            # Memory
            memory = psutil.virtual_memory()

            # Disk (ana partition)
            disk = psutil.disk_usage("/")

            # Network
            net_io = psutil.net_io_counters()

            # Other
            processes = len(psutil.pids())
            boot_time = psutil.boot_time()

            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                cpu_freq_current=cpu_freq.current if cpu_freq else 0,
                cpu_freq_max=cpu_freq.max if cpu_freq else 0,
                memory_total=memory.total,
                memory_available=memory.available,
                memory_percent=memory.percent,
                disk_total=disk.total,
                disk_used=disk.used,
                disk_percent=disk.percent,
                network_sent=net_io.bytes_sent,
                network_recv=net_io.bytes_recv,
                processes=processes,
                boot_time=boot_time,
                uptime=time.time() - boot_time,
            )

        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            # Hata durumunda default değerlerle SystemMetrics nesnesi döndür
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                cpu_freq_current=0.0,
                cpu_freq_max=0.0,
                memory_total=0,
                memory_available=0,
                memory_percent=0.0,
                disk_total=0,
                disk_used=0,
                disk_percent=0.0,
                network_sent=0,
                network_recv=0,
                processes=0,
                boot_time=0.0,
                uptime=0.0,
            )

    def check_alerts(self, metrics: SystemMetrics) -> List[Dict]:
        """Sistem alert'larını kontrol et"""
        alerts = []

        # CPU alert
        if metrics.cpu_percent > self.thresholds["cpu_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "CPU",
                    "value": metrics.cpu_percent,
                    "threshold": self.thresholds["cpu_critical"],
                    "message": f"CPU usage critical: {metrics.cpu_percent:.1f}%",
                }
            )
        elif metrics.cpu_percent > self.thresholds["cpu_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "CPU",
                    "value": metrics.cpu_percent,
                    "threshold": self.thresholds["cpu_warning"],
                    "message": f"CPU usage high: {metrics.cpu_percent:.1f}%",
                }
            )

        # Memory alert
        if metrics.memory_percent > self.thresholds["memory_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "Memory",
                    "value": metrics.memory_percent,
                    "threshold": self.thresholds["memory_critical"],
                    "message": f"Memory usage critical: {metrics.memory_percent:.1f}%",
                }
            )
        elif metrics.memory_percent > self.thresholds["memory_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "Memory",
                    "value": metrics.memory_percent,
                    "threshold": self.thresholds["memory_warning"],
                    "message": f"Memory usage high: {metrics.memory_percent:.1f}%",
                }
            )

        # Disk alert
        if metrics.disk_percent > self.thresholds["disk_critical"]:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "metric": "Disk",
                    "value": metrics.disk_percent,
                    "threshold": self.thresholds["disk_critical"],
                    "message": f"Disk usage critical: {metrics.disk_percent:.1f}%",
                }
            )
        elif metrics.disk_percent > self.thresholds["disk_warning"]:
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "Disk",
                    "value": metrics.disk_percent,
                    "threshold": self.thresholds["disk_warning"],
                    "message": f"Disk usage high: {metrics.disk_percent:.1f}%",
                }
            )

        # Process alert (çok fazla process)
        if metrics.processes > 500:  # Adjust based on system
            alerts.append(
                {
                    "level": "WARNING",
                    "metric": "Processes",
                    "value": metrics.processes,
                    "threshold": 500,
                    "message": f"High number of processes: {metrics.processes}",
                }
            )

        return alerts

    def get_gpu_info(self) -> Optional[Dict]:
        """GPU bilgilerini al (NVIDIA için)"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # İlk GPU
                return {
                    "name": gpu.name,
                    "load": gpu.load * 100,
                    "memory_total": gpu.memoryTotal,
                    "memory_used": gpu.memoryUsed,
                    "memory_free": gpu.memoryFree,
                    "temperature": gpu.temperature,
                }
        except:
            pass
        return None

    def get_network_info(self) -> Dict:
        """Network bilgilerini al"""
        try:
            # IP adresi
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            # Network interfaces
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interfaces[interface] = addr.address

            # Connections
            connections = len(psutil.net_connections())

            return {
                "hostname": hostname,
                "local_ip": local_ip,
                "interfaces": interfaces,
                "active_connections": connections,
            }
        except Exception as e:
            self.logger.error(f"Network info error: {e}")
            return {}

    def get_top_processes(self, count: int = 5) -> List[Dict]:
        """En çok kaynak tüketen process'leri getir"""
        processes = []
        try:
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    cpu = proc.info["cpu_percent"] or 0
                    memory = proc.info["memory_percent"] or 0

                    if cpu > 0 or memory > 0:
                        processes.append(
                            {
                                "pid": proc.info["pid"],
                                "name": proc.info["name"],
                                "cpu": cpu,
                                "memory": memory,
                            }
                        )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # CPU'ya göre sırala
            processes.sort(key=lambda x: x["cpu"], reverse=True)
            return processes[:count]

        except Exception as e:
            self.logger.error(f"Top processes error: {e}")
            return []

    def start_monitoring(self):
        """Monitoring başlat"""
        if self.is_monitoring:
            return

        self.is_monitoring = True

        def monitor_loop():
            self.logger.info("System monitoring started")

            while self.is_monitoring:
                try:
                    metrics = self.get_current_metrics()
                    if metrics:
                        # History'e ekle
                        self.metrics_history.append(asdict(metrics))

                        # 1000 kayıtla sınırla
                        if len(self.metrics_history) > 1000:
                            self.metrics_history = self.metrics_history[-1000:]

                        # Alert'ları kontrol et
                        alerts = self.check_alerts(metrics)
                        if alerts:
                            self.alerts.extend(alerts)
                            for alert in alerts:
                                self.logger.warning(f"ALERT: {alert['message']}")

                    # Belirtilen aralıkta bekle
                    time.sleep(self.log_interval)

                except Exception as e:
                    self.logger.error(f"Monitoring loop error: {e}")
                    time.sleep(5)

        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Monitoring durdur"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("System monitoring stopped")

    def get_summary(self) -> Dict:
        """Sistem özetini getir"""
        metrics = self.get_current_metrics()
        if not metrics:
            return {}

        return {
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
            },
            "metrics": asdict(metrics),
            "gpu": self.get_gpu_info(),
            "network": self.get_network_info(),
            "top_processes": self.get_top_processes(5),
            "active_alerts": [a for a in self.alerts[-10:]],  # Son 10 alert
            "history_size": len(self.metrics_history),
        }

    def save_report(self, filepath: str = "system_report.json"):
        """Raporu JSON olarak kaydet"""
        try:
            report = self.get_summary()
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Report saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Save report error: {e}")
            return False


# HIZLI TEST
if __name__ == "__main__":
    print("🧪 Testing System Monitor...")

    monitor = SystemMonitor(log_interval=2)
    monitor.start_monitoring()

    # 5 saniye bekle
    time.sleep(5)

    # Özeti al
    summary = monitor.get_summary()
    print(f"CPU Usage: {summary.get('metrics', {}).get('cpu_percent', 0):.1f}%")
    print(f"Memory Usage: {summary.get('metrics', {}).get('memory_percent', 0):.1f}%")
    print(f"Disk Usage: {summary.get('metrics', {}).get('disk_percent', 0):.1f}%")

    # Rapor kaydet
    monitor.save_report("test_system_report.json")

    monitor.stop_monitoring()
    print("✅ System Monitor test completed")
    monitor.stop_monitoring()
    print("✅ System Monitor test completed")
    monitor.stop_monitoring()
    print("✅ System Monitor test completed")
