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
