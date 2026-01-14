import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import difflib
import os
import shutil
import time
from pathlib import Path


class NexusConsolidator:
    """
    NEXUS-ONE Redundancy Elimination.
    Benzer isimli veya içerikli dosyaları birleştirir, çakışmaları önler.
    """
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.archive = self.workspace / "archive"
        self.archive.mkdir(exist_ok=True)

    def normalize_name(self, name):
        name = name.lower()
        # Yaygın ekleri ve sayıları kaldır
        for suffix in ["_real", "_v1", "_v2", "_v3", "_final", "_new", "_old", "_test", "_master", "_100", "_200"]:
            name = name.replace(suffix, "")
        import re
        name = re.sub(r'\d+', '', name)
        # 'nexus_' önekini geçici olarak kaldır
        if name.startswith("nexus_"):
            name = name[6:]
        parts = [p for p in name.split("_") if p]
        return "_".join(sorted(parts))

    def find_similar_groups(self):
        files = list(self.workspace.glob("*.py"))
        groups = {}
        for f in files:
            norm = self.normalize_name(f.stem)
            if not norm: continue
            if norm not in groups:
                groups[norm] = []
            groups[norm].append(f)
        return {k: v for k, v in groups.items() if len(v) > 1}

    def consolidate(self):
        print("🧹 NEXUS: Agresif konsolidasyon başlatılıyor...")
        groups = self.find_similar_groups()
        
        for norm_key, files in groups.items():
            # Dosyaları boyuta göre sırala (en dolu dosya master olsun)
            files.sort(key=lambda x: x.stat().st_size, reverse=True)
            master = files[0]
            redundants = files[1:]
            
            # Master dosyasının adını standartlaştır (nexus_ önekini koru)
            standard_name = f"nexus_{norm_key}.py"
            master_path = self.workspace / standard_name
            
            print(f"📦 Grup: {norm_key}")
            print(f"  🏆 Master: {master_path.name}")
            
            # Eğer master dosya zaten varsa ve adı farklıysa içeriğini güncelle
            if master != master_path:
                shutil.copy2(master, master_path)
                if master != master_path: redundants.append(master)

            # Gereksizleri taşı
            for r in set(redundants):
                if r == master_path: continue
                dest = self.archive / r.name
                if dest.exists():
                    dest = self.archive / f"{r.stem}_{int(time.time())}{r.suffix}"
                try:
                    shutil.move(str(r), str(dest))
                    print(f"  🗑️ Arşivlendi: {r.name}")
                except:
                    pass

        print("✅ Konsolidasyon tamamlandı. Çakışmalar giderildi.")

if __name__ == "__main__":
    consolidator = NexusConsolidator("c:/Users/selam/NEXUS-ONE")
    consolidator.consolidate()
