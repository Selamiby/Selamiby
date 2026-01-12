#!/usr/bin/env python3
"""Auto Optimizer - Otomatik optimizasyon"""
import psutil


class AutoOptimizer:
    """Sistem optimizasyonu"""

    def optimize_memory(self):
        """Bellek optimizasyonu"""
        import gc

        gc.collect()
        return True

    def check_cpu(self) -> float:
        """CPU kullanımı"""
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self) -> float:
        """RAM kullanımı"""
        return psutil.virtual_memory().percent
