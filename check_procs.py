"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:21
🚀 Status: ACTIVE / PRODUCTION
"""

import os

import psutil

print(f"{'PID':<10} {'CommandLine'}")
print("-" * 50)
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'pythonw.exe':
            cmdline = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else "N/A"
            print(f"{proc.info['pid']:<10} {cmdline}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
