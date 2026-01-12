#!/usr/bin/env python3
"""Time Tracker - Zaman takip modülü"""
import time
from functools import wraps
from datetime import datetime


class TimeTracker:
    """Zaman takip sistemi"""

    def __init__(self):
        self.timings = {}

    def track(self, name: str):
        """Zaman takip decorator"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start

                if name not in self.timings:
                    self.timings[name] = []
                self.timings[name].append(elapsed)

                print(f"⏱️ {name}: {elapsed:.3f}s")
                return result

            return wrapper

        return decorator

    def get_average(self, name: str) -> float:
        """Ortalama süre"""
        if name in self.timings:
            return sum(self.timings[name]) / len(self.timings[name])
        return 0.0
