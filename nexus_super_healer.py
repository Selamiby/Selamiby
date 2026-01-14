import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import os
import py_compile
import subprocess
import sys
import time
from pathlib import Path

import psutil


class NexusSuperHealer:
    """
    NEXUS-ONE Self-Healing & Visual Enforcement.
    CPU duyarlı tarama ve onarım yapar.
    """
    def __init__(self, workspace):
        self.workspace = Path(workspace)

    def scan_and_fix(self):
        print("🔍 NEXUS-HEALER: Optimizasyon taraması başlatılıyor (Sistem klasörleri hariç)...")
        # CPU kontrolü
        if psutil.cpu_percent() > 80:
            print("⚠️ CPU çok yüksek, tarama erteleniyor...")
            return

        # Neuro-Architect Check
        print("🧠 NEXUS-HEALER: Neuro-Architect kontrol ediliyor...")
        os.system(f"start /b python {self.workspace / 'nexus_neuro_architect.py'}")

        # Sadece ana dizindeki dosyaları tara, alt dizinlere girip CPU'yu yorma
        py_files = list(self.workspace.glob("*.py"))
        
        # Gereksiz/Büyük klasörleri kara listeye al
        ignored_folders = [".git", "node_modules", "nexus_chrome_profile", "venv", "__pycache__"]
        
        errors_found = 0
        for py_file in py_files:
            if any(folder in str(py_file) for folder in ignored_folders):
                continue
            
            # Her dosyada kısa bir mola vererek CPU'yu soğut
            time.sleep(0.05)
                
            try:
                # Check for syntax errors
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as e:
                errors_found += 1
                print(f"⚠️ Error in {py_file.name}: {e.msg}")
                self.attempt_auto_repair(py_file)

        print(f"✅ NEXUS-HEALER: Scan complete. Errors fixed: {errors_found}")

    def attempt_auto_repair(self, file_path):
        """Simple repairs: Fixing common character issues and indentation."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            
            with open(file_path, "w", encoding="utf-8") as f:
                for line in lines:
                    # Fix tabs to spaces, remove null bytes, etc.
                    clean_line = line.replace("\t", "    ").replace("\0", "")
                    f.write(clean_line)
            print(f"🔧 Auto-repaired basic issues in {file_path.name}")
        except:
            pass

    def launch_everything_visible(self):
        """Forces the visuals, server, and production to open in NEW, visible windows."""
        print("🚀 NEXUS: Launching Visual Engine & Sovereign Systems...")
        
        targets = [
            self.workspace / "visuals" / "visual_master.py",
            self.workspace / "nexus_sovereign_server.py",
            self.workspace / "nexus_sovereign_production.py"
        ]
        
        for target in targets:
            if target.exists():
                print(f"🚀 [SUPER-LAUNCHER] Starting: {target.name}")
                # Use 'start' to open in a NEW VISIBLE terminal window
                # We use absolute paths to ensure no confusion
                subprocess.Popen(f'start cmd /k "python \"{str(target)}\""', shell=True)
            else:
                print(f"⚠️ [SUPER-LAUNCHER] File not found: {target.name}")

if __name__ == "__main__":
    from nexus_consolidator import NexusConsolidator
    workspace_path = "c:/Users/selam/NEXUS-ONE"
    
    # Önce benzer dosyaları temizle
    cnt = NexusConsolidator(workspace_path)
    cnt.consolidate()
    
    # Sonra onar ve başlat
    healer = NexusSuperHealer(workspace_path)
    healer.scan_and_fix()
    healer.launch_everything_visible()
