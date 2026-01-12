#!/usr/bin/env python3
"""
MASSIVE BATCH ANALYSIS - 100 PYTHON FILES
Hiç soru sormuyor, hiç beklememiyor, sadece çalışıyor
"""

import ast
import subprocess
from pathlib import Path
import logging

LOG_DIR = Path(__file__).parent / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] BATCH100 - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "batch_analysis_100.log", encoding='utf-8'),
    ]
)
logger = logging.getLogger("Batch100")

def get_python_files(start_dir=Path(__file__).parent, limit=100):
    """Get first 100 Python files"""
    exclude = ['node_modules', '.venv', '__pycache__', '.git', 'venv']
    files = []
    
    for path in Path(start_dir).rglob('*.py'):
        if any(ex in str(path) for ex in exclude):
            continue
        files.append(path)
        if len(files) >= limit:
            break
    
    return files

def analyze_file(filepath):
    """Analyze single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        ast.parse(code)
        
        # Try to fix imports
        try:
            subprocess.run(
                ['autopep8', '--in-place', str(filepath)],
                capture_output=True,
                timeout=3
            )
        except:
            pass
        
        return True
    except SyntaxError as e:
        logger.warning(f"SYNTAX: {filepath.name} - {str(e)[:50]}")
        return False
    except:
        return None

def main():
    logger.info("🔥 BATCH 100 ANALYSIS - BAŞLADI")
    
    files = get_python_files(limit=100)
    logger.info(f"📊 Analiz edilecek: {len(files)} dosya")
    
    results = {'ok': 0, 'error': 0, 'unknown': 0}
    
    for i, filepath in enumerate(files, 1):
        if i % 10 == 0:
            logger.info(f"⏳ {i}/100 tamamlandı...")
        
        result = analyze_file(filepath)
        if result is True:
            results['ok'] += 1
        elif result is False:
            results['error'] += 1
        else:
            results['unknown'] += 1
    
    logger.info(f"✅ BATCH 100 COMPLETE: OK={results['ok']}, ERROR={results['error']}, UNKNOWN={results['unknown']}")

if __name__ == "__main__":
    main()
