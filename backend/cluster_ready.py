"""
ClusterManager: Self-healing, background, cluster-ready yönetim
"""
import json
import os
import socket
import threading
import time
from collections.abc import Awaitable
from datetime import datetime
from typing import Dict, List, Optional

import redis  # pip install redis


class ClusterManager:
    """Basit ama etkili, self-healing destekli cluster yönetimi"""
    def __init__(self, config_file: str = "config/cluster_config.json"):
        self.node_id = f"node_{socket.gethostname()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.config = self._load_config(config_file)
        self.lock = threading.Lock()
        self.nodes = {}
        self.redis_client = None
        # Redis kullan (local veya remote)
        try:
            self.redis_client = redis.Redis(
                host=self.config.get('redis_host', 'localhost'),
                port=self.config.get('redis_port', 6379),
                decode_responses=True
            )
            self.redis_client.ping()
            print(f"✅ Cluster node {self.node_id} connected to Redis")
        except Exception as e:
            print(f"⚠️ Redis not available, using in-memory cluster: {e}")
            self.redis_client = None
        # Heartbeat thread
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def _load_config(self, config_file: str) -> Dict:
        """Cluster config yükle, dosya yoksa default döndür"""
        default = {
            "cluster_enabled": True,
            "redis_host": "localhost",
            "redis_port": 6379,
            "heartbeat_interval": 5,
            "node_timeout": 15
        }
        if not os.path.exists(config_file):
            return default
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return {**default, **json.load(f)}
        except Exception as e:
            print(f"Config load error: {e}")
            return default

    def _heartbeat_loop(self):
        """Node heartbeat gönder, self-healing ile yeniden başlat"""
        while True:
            try:
                node_info = {
                    "node_id": self.node_id,
                    "hostname": socket.gethostname(),
                    "ip": self._get_ip(),
                    "timestamp": datetime.now().isoformat(),
                    "status": "active"
                }
                if self.redis_client:
                    self.redis_client.setex(
                        f"cluster:node:{self.node_id}",
                        self.config["node_timeout"],
                        json.dumps(node_info)
                    )
                    self.redis_client.sadd("cluster:nodes", self.node_id)
                else:
                    with self.lock:
                        self.nodes[self.node_id] = {
                            **node_info,
                            "expires": time.time() + self.config["node_timeout"]
                        }
                time.sleep(self.config["heartbeat_interval"])
            except Exception as e:
                print(f"Heartbeat error: {e}")
                time.sleep(5)

    def _get_ip(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

    def get_active_nodes(self) -> List[Dict]:
        """Aktif node'ları getir, self-healing ile"""
        import asyncio
        try:
            if self.redis_client:
                nodes = []
                node_ids_raw = self.redis_client.smembers("cluster:nodes")
                if hasattr(node_ids_raw, "__await__"):
                    node_ids = asyncio.run(node_ids_raw)  # type: ignore
                else:
                    node_ids = node_ids_raw
                if isinstance(node_ids, set):
                    node_ids = list(node_ids)
                elif hasattr(node_ids, "__iter__"):
                    node_ids = list(node_ids)  # type: ignore
                else:
                    node_ids = []  # type: ignore
                for node_id in node_ids:
                    if isinstance(node_id, bytes):
                        node_id = node_id.decode("utf-8")
                    node_data = self.redis_client.get(f"cluster:node:{node_id}")
                    if hasattr(node_data, "__await__"):
                        node_data = asyncio.run(node_data)  # type: ignore
                    if node_data:
                        try:
                            if isinstance(node_data, bytes):
                                node_data = node_data.decode("utf-8")
                            if isinstance(node_data, str):
                                nodes.append(json.loads(node_data))
                        except Exception:
                            continue
                return nodes
            else:
                current_time = time.time()
                with self.lock:
                    return [
                        {k: v for k, v in info.items() if k != "expires"}
                        for node_id, info in self.nodes.items()
                        if info.get("expires", 0) > current_time
                    ]
        except Exception as e:
            print(f"get_active_nodes error: {e}")
            return []

    def distribute_task(self, task_type: str, data: Dict) -> str:
        """Task'ı node'lara dağıt, self-healing ile"""
        nodes = self.get_active_nodes()
        if not nodes:
            return "local"  # Local'de çalıştır
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{abs(hash(str(data))) % 1000000}"
        if self.redis_client:
            queue_key = f"tasks:{task_type}"
            task_info = {
                "task_id": task_id,
                "type": task_type,
                "data": data,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            }
            try:
                self.redis_client.rpush(queue_key, json.dumps(task_info))
                self.redis_client.setex(f"task:{task_id}", 3600, json.dumps(task_info))
            except Exception as e:
                print(f"Task distribute error: {e}")
                return "local"
        return task_id

# Nexus Core'da örnek kullanım:
class NexusCore:
    def __init__(self):
        # ... diğer init ...
        self.cluster = ClusterManager()

    def handle_request(self, request):
        # Request'i cluster'a dağıt
        if self.cluster.config.get("cluster_enabled", True):
            task_id = self.cluster.distribute_task("api_request", request)
            return {"task_id": task_id, "distributed": True}
        else:
            return self._process_locally(request)

    def _process_locally(self, request):
        # Yerel işleme örneği
        return {"result": "processed locally", "request": request}
        # Yerel işleme örneği
        return {"result": "processed locally", "request": request}
        # Yerel işleme örneği
        return {"result": "processed locally", "request": request}

from typing import Dict, List, Optional


class SelfHealingPipeline:
    def __init__(self, ws_manager: Optional[object] = None, webhook_manager: Optional[object] = None):
        self.ws_manager = ws_manager
        self.webhook_manager = webhook_manager
        self.rules = [
            {"pattern": "disk_full", "action": self.cleanup_disk},
            {"pattern": "service_down", "action": self.restart_service}
        ]
        self.learning_log: List[Dict] = []

    def notify(self, event: str, data: Dict):
        if self.ws_manager and hasattr(self.ws_manager, "broadcast") and callable(getattr(self.ws_manager, "broadcast", None)):
            try:
                import asyncio
                asyncio.create_task(self.ws_manager.broadcast(f"{event}: {data}"))  # type: ignore
            except Exception:
                pass
        if self.webhook_manager and hasattr(self.webhook_manager, "notify") and callable(getattr(self.webhook_manager, "notify", None)):
            try:
                self.webhook_manager.notify(event, data)  # type: ignore
            except Exception:
                pass

    def diagnose(self, system_state: Dict) -> List[str]:
        issues = []
        if system_state.get("disk_usage", 0) > 95:
            issues.append("disk_full")
        if not system_state.get("service_running", True):
            issues.append("service_down")
        self.notify("diagnosis_complete", {"issues": issues})
        return issues

    def match_rules(self, issues: List[str]) -> List[Dict]:
        plans = []
        for issue in issues:
            for rule in self.rules:
                if rule["pattern"] == issue:
                    plans.append(rule)
        self.notify("repair_plan", {"plans": [p["pattern"] for p in plans]})
        return plans

    def execute_actions(self, plans: List[Dict]) -> List[Dict]:
        results = []
        for plan in plans:
            action = plan["action"]
            result = action()
            results.append({"pattern": plan["pattern"], "result": result})
        self.notify("actions_executed", {"results": results})
        return results

    def verify(self, system_state: Dict) -> bool:
        ok = system_state.get("disk_usage", 0) < 95 and system_state.get("service_running", True)
        self.notify("verification", {"ok": ok})
        return ok

    def repair(self) -> dict:
        print("Basic repair completed")
        return {"success": True}

    def create_self_repair_script(self) -> str:
        script = '''#!/usr/bin/env python3
import os
import sys
import shutil
import logging
import subprocess
from datetime import datetime

LOG_FILE = "self_repair.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def check_disk_space(threshold=90):
    try:
        import psutil
        usage = psutil.disk_usage('/')
        percent = usage.percent
        if percent > threshold:
            logging.warning(f"Disk doluluk oranı yüksek: %{percent}")
            return False
        return True
    except Exception as e:
        logging.error(f"Disk kontrol hatası: {e}")
        return True

def restart_service(service_name):
    try:
        if os.name == 'nt':
            subprocess.run(["sc", "stop", service_name], check=False)
            subprocess.run(["sc", "start", service_name], check=False)
        else:
            subprocess.run(["systemctl", "restart", service_name], check=False)
        logging.info(f"Service {service_name} restarted.")
    except Exception as e:
        logging.error(f"Service restart error: {e}")

def cleanup_temp():
    try:
        temp_dirs = ["/tmp", os.path.expanduser("~/.cache")]
        for d in temp_dirs:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)
        logging.info("Temp dosyalar temizlendi.")
    except Exception as e:
        logging.error(f"Temp temizleme hatası: {e}")

def main():
    logging.info("Self-repair script started.")
    if not check_disk_space():
        cleanup_temp()
    service_name = os.environ.get('REPAIR_SERVICE', 'nexus-core')
    restart_service(service_name)
    logging.info("Self-repair script finished.")

if __name__ == "__main__":
    main()
'''
        return script

    def save_self_repair_script(self, script: str) -> str:
        import os
        from pathlib import Path
        script_path = Path(getattr(self, 'project_root', Path.cwd())) / "self_repair.py"
        script_path.write_text(script, encoding='utf-8')
        try:
            script_path.chmod(0o755)
        except Exception:
            pass
        return str(script_path)

    def cleanup_disk(self):
        return "Disk cleanup executed"

    def restart_service(self):
        return "Service restart executed"

    def run_once(self, system_state: Dict):
        issues = self.diagnose(system_state)
        plans = self.match_rules(issues)
        actions = self.execute_actions(plans)
        verified = self.verify(system_state)
        self.learn(issues, actions, verified)

    def learn(self, issues: List[str], actions: List[Dict], verified: bool):
        self.learning_log.append({"issues": issues, "actions": actions, "verified": verified})
        self.notify("learning", {"log_size": len(self.learning_log)})
        self.notify("learning", {"log_size": len(self.learning_log)})
        self.notify("learning", {"log_size": len(self.learning_log)})
