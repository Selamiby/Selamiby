import time
from typing import Dict, Optional

import psutil

from modules.webhook_manager import WebhookManager
from modules.websocket_manager import WebSocketManager


class SystemMonitorPipeline:
    def __init__(self, ws_manager: Optional[WebSocketManager] = None, webhook_manager: Optional[WebhookManager] = None):
        self.ws_manager = ws_manager
        self.webhook_manager = webhook_manager
        self.thresholds = {"cpu": 90, "memory": 90, "disk": 90}  # Varsayılan eşikler

    def notify(self, event: str, data: Dict):
        if self.ws_manager:
            import asyncio
            asyncio.create_task(self.ws_manager.broadcast(f"{event}: {data}"))
        if self.webhook_manager:
            self.webhook_manager.notify(event, data)

    def collect_metrics(self) -> Dict:
        metrics = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
        self.notify("metrics_collected", metrics)
        return metrics

    def analyze(self, metrics: Dict) -> Dict:
        alerts = {}
        for key in ["cpu", "memory", "disk"]:
            if metrics[key] > self.thresholds[key]:
                alerts[key] = metrics[key]
        if alerts:
            self.notify("alert_generated", alerts)
        return alerts

    def log(self, message: str):
        print(f"[SystemMonitorPipeline] {message}")
        self.notify("log", {"message": message})

    def update_dashboard(self, metrics: Dict, alerts: Dict):
        dashboard_data = {"metrics": metrics, "alerts": alerts}
        self.notify("dashboard_update", dashboard_data)

    def run_once(self):
        metrics = self.collect_metrics()
        alerts = self.analyze(metrics)
        self.log(f"Metrics: {metrics}, Alerts: {alerts}")
        self.update_dashboard(metrics, alerts)
        alerts = self.analyze(metrics)
        self.log(f"Metrics: {metrics}, Alerts: {alerts}")
        self.update_dashboard(metrics, alerts)
        alerts = self.analyze(metrics)
        self.log(f"Metrics: {metrics}, Alerts: {alerts}")
        self.update_dashboard(metrics, alerts)
