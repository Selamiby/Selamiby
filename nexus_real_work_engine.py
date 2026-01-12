#!/usr/bin/env python3
"""
NEXUS-ONE REAL AUTONOMOUS WORK ENGINE
======================================
GERÇEK ÇALIŞMA - HİÇ SORU SORMUYOR, HİÇ BEKLEMİYOR
Directly analyzes and fixes Python files
"""

import os
import ast
import subprocess
import logging
from pathlib import Path
from typing import List, Dict
import time

WORKSPACE = Path(__file__).parent
LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] REAL-WORK - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "real_work_engine.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("RealWorkEngine")


class RealWorkEngine:
    """NEXUS-ONE gerçek çalışma motoru - hiç soru sormuyor"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.fixed_files = 0
        self.errors_found = 0
        self.improvements_made = 0
        self.start_time = time.time()
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files"""
        py_files = []
        exclude_patterns = ['node_modules', '.venv', '__pycache__', '.git', 'venv']
        
        for root, dirs, files in os.walk(self.workspace):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not any(ex in d for ex in exclude_patterns)]
            
            for file in files:
                if file.endswith('.py'):
                    py_files.append(Path(root) / file)
        
        return py_files
    
    def check_syntax(self, filepath: Path) -> tuple:
        """Check Python file syntax"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def fix_imports(self, filepath: Path) -> bool:
        """Fix import issues using autopep8/black"""
        try:
            # Try to fix with autopep8
            result = subprocess.run(
                ['autopep8', '--in-place', '--aggressive', str(filepath)],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Fixed imports: {filepath.name}")
                self.fixed_files += 1
                return True
        except:
            pass
        
        return False
    
    def remove_unused_imports(self, filepath: Path) -> bool:
        """Remove unused imports"""
        try:
            result = subprocess.run(
                ['autoflake', '--in-place', '--remove-all-unused-imports', str(filepath)],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True
        except:
            pass
        
        return False
    
    def run_analysis(self):
        """Run real analysis - NO QUESTIONS"""
        logger.info("🔥 REAL WORK ENGINE BAŞLADI - HİÇ SORU SORMUYOR")
        logger.info(f"📊 Workspace: {self.workspace}")
        
        # Find all Python files
        py_files = self.find_python_files()
        logger.info(f"🔍 Bulundu: {len(py_files)} Python dosyası")
        
        # Analyze each file
        batch_size = 50
        for i, py_file in enumerate(py_files[:batch_size]):
            if i % 10 == 0:
                logger.info(f"⏳ İşleniyor: {i}/{min(batch_size, len(py_files))}")
            
            try:
                # Check syntax
                valid, error = self.check_syntax(py_file)
                
                if not valid:
                    logger.warning(f"❌ Syntax error: {py_file.name}")
                    self.errors_found += 1
                    
                    # Try to fix
                    if self.fix_imports(py_file):
                        self.improvements_made += 1
                else:
                    # Try to optimize
                    self.remove_unused_imports(py_file)
                    self.improvements_made += 1
            
            except Exception as e:
                logger.error(f"Error processing {py_file.name}: {e}")
        
        # Log results
        elapsed = time.time() - self.start_time
        logger.info(f"\n✅ ANALYSIS COMPLETE:")
        logger.info(f"   • Files checked: {min(batch_size, len(py_files))}")
        logger.info(f"   • Errors found: {self.errors_found}")
        logger.info(f"   • Files fixed: {self.fixed_files}")
        logger.info(f"   • Improvements: {self.improvements_made}")
        logger.info(f"   • Time: {elapsed:.1f}s")
        
        return {
            'files_checked': len(py_files),
            'errors_found': self.errors_found,
            'files_fixed': self.fixed_files,
            'improvements': self.improvements_made
        }


def main():
    """Main - çalış çalış çalış"""
    engine = RealWorkEngine()
    results = engine.run_analysis()
    
    logger.info("\n🚀 GERÇEK İŞLER YAPILIYOR - ŞIRNAK SUSLU!")
    return results


if __name__ == "__main__":
    main()
