from typing import Dict


class BaseModule:
    """
    Tüm modüller için temel arayüz.
    Yaşam döngüsü: Initialization → Configuration → Dependency Resolution → Startup → Running State → Shutdown
    """
    def __init__(self):
        self.initialized = False
        self.configured = False
        self.dependencies_resolved = False
        self.running = False
        self.shutdown = False

    def initialize(self) -> bool:
        """Modülün temel başlatma işlemleri"""
        self.initialized = True
        return True

    def configure(self, config: Dict) -> bool:
        """Modül yapılandırmasını uygula"""
        self.configured = True
        return True

    def resolve_dependencies(self) -> bool:
        """Bağımlılıkları çöz"""
        self.dependencies_resolved = True
        return True

    def start(self) -> bool:
        """Modülü başlat"""
        if self.initialized and self.configured and self.dependencies_resolved:
            self.running = True
            return True
        return False

    def stop(self) -> bool:
        """Modülü durdur"""
        self.running = False
        self.shutdown = True
        return True

    def get_status(self) -> Dict:
        """Modülün mevcut durumunu döndür"""
        return {
            "initialized": self.initialized,
            "configured": self.configured,
            "dependencies_resolved": self.dependencies_resolved,
            "running": self.running,
            "shutdown": self.shutdown
        }

    def handle_command(self, command: str, params: Dict) -> Dict:
        """Modüle komut gönder"""
        return {"success": False, "message": f"Command '{command}' desteklenmiyor."}
        return {"success": False, "message": f"Command '{command}' desteklenmiyor."}
        return {"success": False, "message": f"Command '{command}' desteklenmiyor."}
