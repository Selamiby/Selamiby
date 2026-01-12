#!/usr/bin/env python3
"""Performance Tracker - Performans izleme"""
import time
from functools import wraps


def track_performance(func):
    """Performance decorator"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️ {func.__name__}: {elapsed:.3f}s")
        return result

    return wrapper
