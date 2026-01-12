#!/usr/bin/env python3
"""
NEXUS CPU Guardian - System Resource Protection
=================================================
Monitors and limits CPU/RAM usage to prevent system freeze.
"""

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psutil

WORKSPACE = Path(__file__).parent
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] NEXUS-CPU - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "cpu_guardian.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CPUGuardian")

class CPUGuardian:
    """Protects system from CPU/RAM overload"""
    
    def __init__(self, cpu_threshold=70, ram_threshold=80):
        self.cpu_threshold = cpu_threshold
        self.ram_threshold = ram_threshold
        self.running = True
        self.active_processes = {}
        self.throttled = False
        
    def get_system_stats(self) -> Dict:
        """Get current CPU and RAM usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': cpu_percent,
            'ram_percent': ram.percent,
            'ram_available_mb': ram.available / (1024 * 1024),
            'processes_count': len(psutil.pids())
        }
    
    def should_throttle(self) -> bool:
        """Determine if system needs throttling"""
        stats = self.get_system_stats()
        
        if stats['cpu_percent'] > self.cpu_threshold:
            logger.warning(f"⚠️ CPU YÜKSEK: {stats['cpu_percent']:.1f}% - THROTTLING BAŞLATIYOR")
            return True
        
        if stats['ram_percent'] > self.ram_threshold:
            logger.warning(f"⚠️ RAM YÜKSEK: {stats['ram_percent']:.1f}% - THROTTLING BAŞLATIYOR")
            return True
        
        return False
    
    def apply_throttle(self):
        """Pause resource-heavy operations"""
        logger.info("🔻 CPU Guardian: İşlemler yavaşlatılıyor...")
        self.throttled = True
        time.sleep(5)  # Pause for 5 seconds
        self.throttled = False
        logger.info("🔼 CPU Guardian: İşlemlere devam")
    
    def register_process(self, process_id: str, process_name: str):
        """Track active process"""
        self.active_processes[process_id] = {
            'name': process_name,
            'started_at': datetime.now().isoformat(),
            'status': 'running'
        }
        logger.info(f"📝 Süreç kaydedildi: {process_name} ({process_id})")
    
    def unregister_process(self, process_id: str):
        """Stop tracking process"""
        if process_id in self.active_processes:
            del self.active_processes[process_id]
            logger.info(f"✓ Süreç kaydı silindi: {process_id}")
    
    def get_status_report(self) -> Dict:
        """Generate current status"""
        stats = self.get_system_stats()
        return {
            'guardian_status': 'monitoring',
            'throttled': self.throttled,
            'system_stats': stats,
            'active_processes': self.active_processes,
            'cpu_threshold': self.cpu_threshold,
            'ram_threshold': self.ram_threshold
        }
    
    def monitor_loop(self):
        """Continuous monitoring loop"""
        logger.info(f"🛡️ CPU Guardian başlatıldı (CPU: {self.cpu_threshold}%, RAM: {self.ram_threshold}%)")
        
        while self.running:
            try:
                stats = self.get_system_stats()
                
                # Log every 30 seconds
                logger.info(f"CPU: {stats['cpu_percent']:.1f}% | RAM: {stats['ram_percent']:.1f}% | Processes: {len(self.active_processes)}")
                
                if self.should_throttle():
                    self.apply_throttle()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                time.sleep(5)
    
    def start(self):
        """Start monitoring in background thread"""
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("✅ CPU Guardian thread başlatıldı")
        return monitor_thread
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        logger.info("⏹️ CPU Guardian durduruldu")


# Global CPU Guardian instance
_guardian = CPUGuardian(cpu_threshold=65, ram_threshold=75)

def get_guardian() -> CPUGuardian:
    """Get global guardian instance"""
    return _guardian

def start_guardian():
    """Start global guardian"""
    return _guardian.start()


if __name__ == "__main__":
    guardian = CPUGuardian(cpu_threshold=65, ram_threshold=75)
    monitor_thread = guardian.start()
    
    try:
        while True:
            report = guardian.get_status_report()
            print(json.dumps(report, indent=2))
            time.sleep(10)
    except KeyboardInterrupt:
        guardian.stop()
        logger.info("👋 Kapatılıyor...")
