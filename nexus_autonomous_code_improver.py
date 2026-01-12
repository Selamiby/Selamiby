#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 NEXUS AUTONOMOUS CODE IMPROVER
Workspace'teki Python dosyalarını otomatik iyileştirir
"""

import ast
import logging
import os
from datetime import datetime
from pathlib import Path

import autopep8

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

class CodeImprover:
    def __init__(self):
        self.improved_count = 0
        self.workspace = Path("C:/Users/selam/NEXUS-ONE")
        
    def improve_file(self, file_path: Path):
        """Dosyayı iyileştir"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # Syntax check
            try:
                ast.parse(original)
            except SyntaxError:
                logger.warning(f"⚠️ Syntax error: {file_path.name}")
                return False
            
            # Auto-format
            improved = autopep8.fix_code(original, options={'aggressive': 2})
            
            if improved != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(improved)
                self.improved_count += 1
                logger.info(f"✅ Improved: {file_path.name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error: {file_path.name} - {e}")
            return False
    
    def run(self, max_files=50):
        """Workspace'te code improvement yap"""
        logger.info("🔧 CODE IMPROVER BAŞLADI")
        
        py_files = list(self.workspace.glob("*.py"))[:max_files]
        
        for file in py_files:
            if file.name.startswith("nexus_") or file.name in ["quick_start.py", "code_generator.py"]:
                self.improve_file(file)
        
        logger.info(f"✅ {self.improved_count}/{len(py_files)} dosya iyileştirildi")

if __name__ == "__main__":
    improver = CodeImprover()
    improver.run()
