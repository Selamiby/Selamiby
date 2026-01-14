"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

import json
import os

base_path = r"C:\Users\selam\NEXUS-ONE"
files_info = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".py"):
            if "nexus" in file.lower() or "core\\modules\\nexus_modules" in root.lower():
                path = os.path.join(root, file)
                try:
                    size = os.path.getsize(path)
                    files_info.append({"FullName": path, "Length": size})
                except OSError:
                    pass

with open("nexus_files_info.json", "w", encoding="utf-8") as f:
    json.dump(files_info, f, indent=4)

print(f"Generated info for {len(files_info)} files.")
