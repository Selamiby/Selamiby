#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 NEXUS WORKSPACE ANALYZER
Workspace'i analiz edip rapor oluşturur
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

class WorkspaceAnalyzer:
    def __init__(self):
        self.workspace = Path("C:/Users/selam/NEXUS-ONE")
        self.stats = {
            "analyzed_at": datetime.now().isoformat(),
            "total_files": 0,
            "python_files": 0,
            "powershell_files": 0,
            "json_files": 0,
            "markdown_files": 0,
            "directories": 0,
            "largest_files": [],
            "recent_files": []
        }
    
    def analyze(self):
        """Workspace'i analiz et"""
        logger.info("📊 WORKSPACE ANALYZER BAŞLADI")
        
        all_files = []
        
        for item in self.workspace.rglob("*"):
            if item.is_file():
                self.stats["total_files"] += 1
                
                if item.suffix == ".py":
                    self.stats["python_files"] += 1
                elif item.suffix == ".ps1":
                    self.stats["powershell_files"] += 1
                elif item.suffix == ".json":
                    self.stats["json_files"] += 1
                elif item.suffix == ".md":
                    self.stats["markdown_files"] += 1
                
                try:
                    size = item.stat().st_size
                    mtime = item.stat().st_mtime
                    all_files.append({
                        "name": item.name,
                        "path": str(item.relative_to(self.workspace)),
                        "size": size,
                        "mtime": mtime
                    })
                except:
                    pass
            elif item.is_dir():
                self.stats["directories"] += 1
        
        # Largest files
        all_files.sort(key=lambda x: x["size"], reverse=True)
        self.stats["largest_files"] = [
            {"name": f["name"], "size": f"{f['size']/1024:.2f} KB"}
            for f in all_files[:10]
        ]
        
        # Recent files
        all_files.sort(key=lambda x: x["mtime"], reverse=True)
        self.stats["recent_files"] = [f["name"] for f in all_files[:10]]
        
        logger.info(f"✅ Total files: {self.stats['total_files']}")
        logger.info(f"✅ Python files: {self.stats['python_files']}")
        logger.info(f"✅ PowerShell files: {self.stats['powershell_files']}")
        logger.info(f"✅ Directories: {self.stats['directories']}")
        
        # Save report
        report_path = Path("workspace_analysis.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Report saved: {report_path}")

if __name__ == "__main__":
    analyzer = WorkspaceAnalyzer()
    analyzer.analyze()
