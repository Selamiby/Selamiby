"""
CPU ve Performans Optimizasyonu
Hafif, hızlı ve düşük CPU kullanım
"""

import os
import psutil
import threading
from typing import Optional, Callable
from datetime import datetime
from collections import deque
import json


class CPUMonitor:
    """CPU kullanımını gerçek zamanlı takip et"""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.cpu_history = deque(maxlen=max_history)
        self.memory_history = deque(maxlen=max_history)
        self.is_monitoring = False
        self.process = psutil.Process()
        
    def get_stats(self) -> dict:
        """Anlık CPU ve bellek istatistikleri"""
        try:
            cpu_percent = self.process.cpu_percent(interval=0.01)
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_mb': memory_info.rss / 1024 / 1024,
                'memory_percent': memory_percent,
                'num_threads': self.process.num_threads(),
                'system_cpu': psutil.cpu_percent(interval=0.01)
            }
            
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory_info.rss / 1024 / 1024)
            
            return stats
        except Exception as e:
            return {'error': str(e)}
    
    def get_average_cpu(self) -> float:
        """Ortalama CPU kullanımı"""
        if not self.cpu_history:
            return 0.0
        return sum(self.cpu_history) / len(self.cpu_history)
    
    def get_peak_cpu(self) -> float:
        """En yüksek CPU kullanımı"""
        if not self.cpu_history:
            return 0.0
        return max(self.cpu_history)
    
    def print_report(self):
        """Kullanım raporu yazdır"""
        stats = self.get_stats()
        if 'error' not in stats:
            print("\n" + "="*50)
            print("📊 PERFORMANS RAPORU")
            print("="*50)
            print(f"CPU Kullanımı: {stats['cpu_percent']:.2f}%")
            print(f"Sistem CPU: {stats['system_cpu']:.2f}%")
            print(f"Bellek: {stats['memory_mb']:.2f} MB ({stats['memory_percent']:.2f}%)")
            print(f"Thread Sayısı: {stats['num_threads']}")
            print(f"Ort. CPU (son {len(self.cpu_history)}): {self.get_average_cpu():.2f}%")
            print(f"En Yüksek CPU: {self.get_peak_cpu():.2f}%")
            print("="*50 + "\n")


class TaskScheduler:
    """Hafif task scheduler - CPU dostu"""
    
    def __init__(self, num_workers: int = 2):
        self.num_workers = min(num_workers, os.cpu_count() or 1)
        self.tasks = deque()
        self.is_running = False
        self.workers = []
    
    def add_task(self, func: Callable, *args, **kwargs):
        """Task ekle"""
        self.tasks.append((func, args, kwargs))
    
    def start(self):
        """Task scheduler'ı başlat"""
        self.is_running = True
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _worker_loop(self):
        """Worker thread döngüsü"""
        while self.is_running:
            if self.tasks:
                try:
                    func, args, kwargs = self.tasks.popleft()
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"❌ Task hatası: {e}")
            else:
                threading.Event().wait(0.1)  # CPU relax
    
    def stop(self):
        """Scheduler'ı durdur"""
        self.is_running = False
        for worker in self.workers:
            worker.join(timeout=1)


class OptimizedCache:
    """Hafif, hızlı cache sistemi"""
    
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.cache = {}
        self.timestamps = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key: str):
        """Cache'den al"""
        if key in self.cache:
            if self._is_valid(key):
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key: str, value):
        """Cache'e ekle"""
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.timestamps, key=self.timestamps.get)
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now().timestamp()
    
    def _is_valid(self, key: str) -> bool:
        """Cache geçerli mi kontrol et"""
        if key not in self.timestamps:
            return False
        age = datetime.now().timestamp() - self.timestamps[key]
        return age < self.ttl
    
    def clear(self):
        """Cache temizle"""
        self.cache.clear()
        self.timestamps.clear()


def optimize_event_loop():
    """Event loop optimizasyonu"""
    import sys
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Global monitor ve scheduler
cpu_monitor = CPUMonitor()
task_scheduler = TaskScheduler(num_workers=2)
cache = OptimizedCache(max_size=500, ttl=1800)
