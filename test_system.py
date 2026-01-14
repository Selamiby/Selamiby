import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AetherOS System Test Script
"""
import io
import os
import sys

# Unicode çıktı için
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import time

from modules.system_monitor import SystemMonitor


def test_system_monitor():
    """System Monitor testi"""
    print("🚀 Testing System Monitor...")

    monitor = SystemMonitor(update_interval=1)

    # Başlat
    monitor.start_monitoring()

    print("📊 Collecting metrics for 10 seconds...")

    metrics_data = []
    for i in range(10):
        time.sleep(1)
        if monitor.metrics_history:
            latest = monitor.metrics_history[-1]
            metrics_data.append(
                {
                    "time": latest.timestamp.strftime("%H:%M:%S"),
                    "cpu": f"{latest.cpu_percent:.1f}%",
                    "memory": f"{latest.memory_percent:.1f}%",
                    "disk": f"{latest.disk_usage_percent:.1f}%",
                }
            )
            print(
                f"  [{i+1}/10] CPU: {latest.cpu_percent:.1f}%, Mem: {latest.memory_percent:.1f}%"
            )

    # Durdur
    monitor.stop_monitoring()

    print("\n📋 Test Results:")
    print(json.dumps(monitor.get_metrics_summary(hours=1), indent=2))

    print("\n🔥 Top Processes:")
    for i, proc in enumerate(monitor.get_top_processes(3), 1):
        print(
            f"  {i}. {proc.name}: {proc.cpu_percent:.1f}% CPU, {proc.memory_percent:.1f}% MEM"
        )

    print("\n💾 Disk Info:")
    for disk in monitor.get_disk_info():
        print(f"  {disk['mountpoint']}: {disk['percent']:.1f}% used")


def test_file_manager():
    """File Manager testi"""
    print("\n📁 Testing File Manager...")

    try:
        from modules.file_manager import FileManager

        fm = FileManager()

        # Mevcut dizin
        result = fm.list_contents()
        print(f"  Current dir: {result['path']}")
        print(
            f"  Files: {result['files_count']}, Directories: {result['directories_count']}"
        )

        # Test dosyası oluştur
        test_file = "aetheros_test_file.txt"
        create_result = fm.create_file(
            test_file, "This is a test file created by AetherOS"
        )

        if create_result.get("success"):
            print(f"  ✓ Created test file: {test_file}")

            # Dosyayı oku
            read_result = fm.read_file(test_file)
            if read_result.get("success"):
                print(f"  ✓ File read successfully ({read_result['line_count']} lines)")
        else:
            print(f"  ✗ File creation failed: {create_result.get('error')}")

    except ImportError as e:
        print(f"  ✗ File Manager not available: {e}")


def test_ai_engine():
    """AI Engine testi"""
    print("\n🤖 Testing AI Engine...")

    try:
        from core.ai_engine import AIEngine

        ai = AIEngine()

        # Test analizi
        test_text = "AetherOS is an autonomous AI operating system built with Python"
        analysis = ai.analyze_text(test_text)

        print(f"  Text analysis: {analysis['analysis']['words']} words")
        print(f"  Sentiment: {analysis['analysis']['sentiment']}")

        # Test response
        response = ai.generate_response("What can you do?")
        print(f"  AI Response: {response[:80]}...")

        # Task planning
        task_plan = ai.create_task_plan("Organize my documents folder")
        print(f"  Task planning: {task_plan['steps'][0]}")

    except ImportError as e:
        print(f"  ✗ AI Engine not available: {e}")


def main():
    """Ana test fonksiyonu"""
    print("=" * 60)
    print("AETHEROS COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)

    # Tüm testleri çalıştır
    test_system_monitor()
    test_file_manager()
    test_ai_engine()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
