#!/usr/bin/env python3
"""Memory Manager - Bellek yönetimi"""
import gc
import sys


class MemoryManager:
    """Bellek yönetim sistemi"""

    def cleanup(self):
        """Bellek temizliği"""
        gc.collect()
        return sys.getsizeof(gc.garbage)

    def get_object_count(self) -> int:
        """Obje sayısı"""
        return len(gc.get_objects())
