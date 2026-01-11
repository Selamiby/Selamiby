"""
NEXUS-ONE - Ana Sistem Orkestrasyonu
Tüm 3 Seviyeyi kontrol eden merkez sistem
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

# Advanced AI Integration
try:
    from core.advanced_ai_integration import AdvancedAIIntegration
    ADVANCED_AI_AVAILABLE = True
except ImportError:
    ADVANCED_AI_AVAILABLE = False


class AutomationLevel(Enum):
    """Otomasyon seviyesi"""
    BASIC = "level1"
    ADVANCED = "level2"
    INTELLIGENT = "level3"


class AetherOSCore:
    """NEXUS-ONE Ana Merkezi"""
    
    def __init__(self):
        self.system_status = "INITIALIZING"
        self.automation_level = None
        self.active_modules = {}
        self.system_log = []
        self.config_path = Path("config/aether_config.json")
        
        # Advanced AI Integration
        if ADVANCED_AI_AVAILABLE:
            self.advanced_ai = AdvancedAIIntegration()
        else:
            self.advanced_ai = None
        
        self.log(f"NEXUS-ONE initialized at {datetime.now().isoformat()}")
    
    def initialize_all_systems(self) -> Dict:
        """Tüm seviyeleri başlat"""
        
        initialization_result = {
            "timestamp": datetime.now().isoformat(),
            "levels": {}
        }
        
        # Seviye 1: Otonom Temel
        try:
            from modules.backup_manager import backup_manager
            from modules.file_organizer import file_organizer
            from modules.system_maintenance import system_maintenance
            
            self.active_modules["file_organizer"] = file_organizer
            self.active_modules["backup_manager"] = backup_manager
            self.active_modules["system_maintenance"] = system_maintenance
            
            initialization_result["levels"]["level1"] = {
                "status": "OPERATIONAL",
                "modules": ["file_organizer", "backup_manager", "system_maintenance"]
            }
            
            self.log("Level 1 (Basic Autonomy) initialized")
        except Exception as e:
            initialization_result["levels"]["level1"] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.log(f"Level 1 initialization failed: {e}")
        
        # Seviye 2: AI-Destekli
        try:
            from modules.context_aware_help import (error_prevention,
                                                    user_context)
            from modules.smart_content_analyzer import smart_analyzer
            
            self.active_modules["smart_analyzer"] = smart_analyzer
            self.active_modules["user_context"] = user_context
            self.active_modules["error_prevention"] = error_prevention
            
            initialization_result["levels"]["level2"] = {
                "status": "OPERATIONAL",
                "modules": ["smart_analyzer", "user_context", "error_prevention"]
            }
            
            self.log("Level 2 (AI-Powered Autonomy) initialized")
        except Exception as e:
            initialization_result["levels"]["level2"] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.log(f"Level 2 initialization failed: {e}")
        
        # Seviye 3: İleri Otonom
        try:
            from modules.model_manager import model_manager
            from modules.realtime_monitor import realtime_monitor
            from modules.self_healing_system import self_healing_system
            from modules.workflow_engine import workflow_engine
            
            self.active_modules["workflow_engine"] = workflow_engine
            self.active_modules["self_healing_system"] = self_healing_system
            self.active_modules["model_manager"] = model_manager
            self.active_modules["realtime_monitor"] = realtime_monitor
            
            initialization_result["levels"]["level3"] = {
                "status": "OPERATIONAL",
                "modules": ["workflow_engine", "self_healing_system", "model_manager", "realtime_monitor"]
            }
            
            self.log("Level 3 (Advanced Autonomous) initialized")
        except Exception as e:
            initialization_result["levels"]["level3"] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.log(f"Level 3 initialization failed: {e}")
        
        self.system_status = "OPERATIONAL"
        
        return initialization_result
    
    def perform_system_check(self) -> Dict:
        """Sistem kontrolü yap"""
        check_result = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Disk kontrolü
        if "system_maintenance" in self.active_modules:
            sm = self.active_modules["system_maintenance"]
            disk_analysis = sm.analyze_disk()
            check_result["checks"]["disk"] = {
                "status": "OK" if disk_analysis.get("status") == "GOOD" else "WARNING",
                "usage_percent": disk_analysis.get("usage_percent"),
                "status_detail": disk_analysis.get("status")
            }
        
        # Sistem sağlığı
        if "system_maintenance" in self.active_modules:
            sm = self.active_modules["system_maintenance"]
            health = sm.health_report()
            check_result["checks"]["system_health"] = {
                "status": health.get("overall_status"),
                "cpu": health.get("cpu_percent"),
                "memory": health.get("memory_percent")
            }
        
        # Çalışan modüller
        check_result["active_modules"] = len(self.active_modules)
        
        return check_result
    
    def get_all_modules(self) -> Dict:
        """Tüm aktif modülleri getir"""
        return self.active_modules
    
    def get_advanced_ai_status(self) -> Dict:
        """Advanced AI durumunu getir"""
        if not self.advanced_ai:
            return {"status": "unavailable", "reason": "Advanced AI module not loaded"}
        
        return {
            "status": "available",
            **self.advanced_ai.get_system_status()
        }
    
    def start_continuous_monitoring(self) -> Dict:
        """Sürekli izlemeyi başlat"""
        if "realtime_monitor" not in self.active_modules:
            return {"error": "Realtime monitor not available"}
        
        monitor = self.active_modules["realtime_monitor"]
        result = monitor.start_monitoring(interval=5)
        
        self.log("Continuous monitoring started")
        
        return result
    
    def get_system_status(self) -> Dict:
        """Sistem durumunu al"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": self.system_status,
            "active_modules": len(self.active_modules),
            "modules_list": list(self.active_modules.keys()),
            "system_checks": {}
        }
        
        # Realtime monitor durumu
        if "realtime_monitor" in self.active_modules:
            monitor = self.active_modules["realtime_monitor"]
            if monitor.history:
                status["system_checks"]["realtime"] = monitor.get_current_status()
        
        # Model yöneticisi istatistikleri
        if "model_manager" in self.active_modules:
            mm = self.active_modules["model_manager"]
            status["models"] = mm.get_model_stats()
        
        return status
    
    def log(self, message: str):
        """Sistem günlüğüne ekle"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        self.system_log.append(log_entry)
        
        # Son 1000 girişi tut
        if len(self.system_log) > 1000:
            self.system_log = self.system_log[-1000:]
    
    def save_config(self) -> Dict:
        """Yapılandırmayı kaydet"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config = {
            "system_status": self.system_status,
            "active_modules": list(self.active_modules.keys()),
            "saved_at": datetime.now().isoformat(),
            "recent_logs": self.system_log[-50:]
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        
        return {"success": True, "path": str(self.config_path)}
    
    def get_automation_capabilities(self) -> Dict:
        """Otomasyon yeteneklerini al"""
        return {
            "level1_capabilities": {
                "name": "Autonomy Basics",
                "features": [
                    "Automatic file organization",
                    "Duplicate file detection",
                    "Smart backup management",
                    "System health monitoring",
                    "Disk space analysis",
                    "Temporary file cleanup"
                ]
            },
            "level2_capabilities": {
                "name": "AI-Powered Autonomy",
                "features": [
                    "Content analysis and categorization",
                    "Language detection",
                    "Sentiment analysis",
                    "Pattern recognition in files",
                    "User behavior learning",
                    "Proactive suggestions",
                    "Error prevention and risk detection"
                ]
            },
            "level3_capabilities": {
                "name": "Advanced Autonomous Systems",
                "features": [
                    "Workflow automation with dependencies",
                    "Parallel task execution",
                    "Self-healing and auto-repair",
                    "Performance optimization",
                    "Multi-model AI management",
                    "Real-time monitoring and anomaly detection",
                    "Emergency protocols and alerts",
                    "Fine-tuning and model optimization"
                ]
            }
        }


# Global instance
aether_core = AetherOSCore()


def quick_start() -> Dict:
    """Hızlı başlat"""
    
    # Tüm seviyeleri başlat
    init_result = aether_core.initialize_all_systems()
    
    # Sistem kontrolü
    check_result = aether_core.perform_system_check()
    
    # Sürekli izlemeyi başlat
    monitor_result = aether_core.start_continuous_monitoring()
    
    # Yapılandırmayı kaydet
    aether_core.save_config()
    
    return {
        "initialization": init_result,
        "system_check": check_result,
        "monitoring": monitor_result
    }


if __name__ == "__main__":
    print("Starting NEXUS-ONE...")
    result = quick_start()
    print(json.dumps(result, indent=2, default=str))
