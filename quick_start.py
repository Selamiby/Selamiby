#!/usr/bin/env python3
"""
NEXUS-ONE Quick Start
Minimal version for testing and quick access
"""
import json
import os
import sys
from datetime import datetime


def quick_start():
    """Hızlı başlangıç fonksiyonu"""
    print("\n" + "=" * 60)
    print("🤖 NEXUS-ONE QUICK START")
    print("=" * 60)

    info = {
        "system": sys.platform,
        "python": sys.version.split()[0],
        "directory": os.getcwd(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files_in_dir": len([f for f in os.listdir() if os.path.isfile(f)]),
    }

    print("\n📊 System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    print("\n📁 Files in current directory (first 10):")
    files = [f for f in os.listdir() if os.path.isfile(f)][:10]
    for i, file in enumerate(files, 1):
        size = os.path.getsize(file)
        print(f"  {i:2}. {file[:30]:30} ({size:,} bytes)")

    print("\n💡 Quick Commands:")
    print("  1. Type 'exit' to quit")
    print("  2. Type 'ls' to list files")
    print("  3. Type 'info' for system info")
    print("  4. Type 'create' to make a test file")

    while True:
        try:
            cmd = input("\nquick> ").strip().lower()

            if cmd in ["exit", "quit", "q"]:
                print("\n👋 Goodbye!")
                break

            elif cmd == "ls":
                files = os.listdir()
                for f in files[:20]:
                    if os.path.isfile(f):
                        print(f"  📄 {f}")
                    else:
                        print(f"  📁 {f}/")

            elif cmd == "info":
                print(json.dumps(info, indent=2))

            elif cmd == "create":
                filename = f"nexus_test_{int(datetime.now().timestamp())}.txt"
                with open(filename, "w") as f:
                    f.write(f"NEXUS-ONE Test File\nCreated: {datetime.now()}")
                print(f"✅ Created: {filename}")

            elif cmd == "help":
                print(
                    """
  Available commands:
  - ls: List files
  - info: Show system info
  - create: Create test file
  - exit: Quit NEXUS-ONE
                """
                )

            elif cmd:
                print(f"❌ Unknown command: {cmd}")
                print("   Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    print(
        r"""
    ╔╗╔╦╗╔╦╗╔═╗╦ ╦╔═╗  ╔═╗╔╗╔╔═╗╔╦╗
    ║║║║║ ║║╠═╝║ ║╚═╗  ║ ║║║║╚═╗ ║
    ╝╚╝╩╩═╝╩╩  ╚═╝╚═╝  ╚═╝╝╚╝╚═╝ ╩

    ╔══════════════════════════════════════╗
    ║     NEXUS-ONE Quick Start v1.0      ║
    ║     Minimal AI Interface            ║
    ╚══════════════════════════════════════╝
    """
    )

    quick_start()
