#!/usr/bin/env python3
"""
PERFORMANCE PROFILER - Find slow files
Yavaş dosyaları bul ve optimize et
"""

import os
from pathlib import Path
import time
import logging

LOG_DIR = Path(__file__).parent / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] PERF - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "performance_profiler.log", encoding='utf-8'),
    ]
)
logger = logging.getLogger("Profiler")

def analyze_performance():
    """Analyze file sizes and complexity"""
    logger.info("🔍 PERFORMANCE ANALYSIS - Yavaş dosyaları buluyorum...")
    
    workspace = Path(__file__).parent
    exclude = ['node_modules', '.venv', '__pycache__', '.git', 'venv']
    
    files_by_size = []
    files_by_complexity = []
    
    for py_file in workspace.rglob('*.py'):
        if any(ex in str(py_file) for ex in exclude):
            continue
        
        try:
            size = py_file.stat().st_size
            
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = len(f.readlines())
            
            # Complexity = lines with imports/classes/functions
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                complexity = content.count('def ') + content.count('class ') + content.count('import ')
            
            files_by_size.append((py_file.name, size, lines))
            files_by_complexity.append((py_file.name, complexity, lines))
        
        except:
            pass
    
    # Sort by size
    files_by_size.sort(key=lambda x: x[1], reverse=True)
    
    logger.info(f"📊 En büyük 5 dosya:")
    for name, size, lines in files_by_size[:5]:
        logger.info(f"   {name}: {size/1024:.1f}KB ({lines} lines)")
    
    logger.info(f"📊 En kompleks 5 dosya:")
    for name, complexity, lines in files_by_complexity[:5]:
        logger.info(f"   {name}: complexity={complexity}, lines={lines}")
    
    logger.info(f"✅ Performance analizi tamamlandı")

if __name__ == "__main__":
    analyze_performance()
