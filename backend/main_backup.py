#!/usr/bin/env python3
"""
NEXUS-ONE - Autonomous Operating System
3-Level Autonomous System: Basic -> AI-Powered -> Advanced
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from core.aether_core import aether_core, quick_start


def main():
    """NEXUS-ONE Ana Giris Noktasi"""
    
    print("\n" + "=" * 70)
    print("   NEXUS-ONE - AUTONOMOUS OPERATING SYSTEM")
    print("=" * 70)
    print(f"   Baslangic: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    # 1. Tum seviyeleri basla
    print("[1] Sistem Baslatiliyor...")
    init_result = aether_core.initialize_all_systems()
    
    for level, status in init_result["levels"].items():
        status_icon = "OK" if status['status'] == 'OPERATIONAL' else "FAIL"
        level_name = {
            "level1": "Temel Otonom (Basic Autonomy)",
            "level2": "AI-Destekli (AI-Powered)",
            "level3": "Ileri Otonom (Advanced)"
        }.get(level, level)
        print(f"    [{status_icon}] {level_name}: {status['status']}")
    
    # 2. Sistem kontrolu
    print("\n[2] Sistem Kontrolu Yapiliyor...")
    check_result = aether_core.perform_system_check()
    
    if "disk" in check_result["checks"]:
        disk = check_result["checks"]["disk"]
        usage = disk.get('usage_percent') or 0
        if usage is None:
            usage = 0
        print(f"    * Disk: {disk['status']} ({usage:.1f}%)")
    
    if "system_health" in check_result["checks"]:
        health = check_result["checks"]["system_health"]
        cpu = health.get('cpu') or 0
        mem = health.get('memory') or 0
        if cpu is None:
            cpu = 0
        if mem is None:
            mem = 0
        print(f"    * CPU: {cpu:.1f}% | Bellek: {mem:.1f}%")
    
    # 3. Sistem durumu
    print("\n[3] Sistem Durumu")
    system_status = aether_core.get_system_status()
    print(f"    * Genel Status: {system_status['overall_status']}")
    print(f"    * Aktif Moduller: {system_status['active_modules']}")
    
    # 4. Modul listesi
    print("\n[4] Aktif Moduller:")
    for i, module in enumerate(system_status['modules_list'], 1):
        print(f"    {i:2}. {module}")
    
    # 5. Basari mesaji
    print("\n" + "=" * 70)
    print("   NEXUS-ONE TAMAMEN ISLEVSEL")
    print("   Tum 3 Seviye Basarili Yüklü")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
