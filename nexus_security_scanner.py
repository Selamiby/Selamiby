#!/usr/bin/env python3
"""
SECURITY SCANNER - Find vulnerabilities
Hiç soru sormuyor, güvenlik taraması yapıyor
"""

import logging
import re
from pathlib import Path

LOG_DIR = Path(__file__).parent / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] SECURITY - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "security_scan.log", encoding='utf-8'),
    ]
)
logger = logging.getLogger("Security")

class SecurityScanner:
    """Scan Python files for security issues"""
    
    def __init__(self):
        self.vulnerabilities = []
        
        # Security patterns to find
        self.patterns = {
            'hardcoded_password': r'(password|passwd|pwd)\s*=\s*["\'].*["\']',
            'sql_injection': r'execute\(.*\+',
            'eval_usage': r'\beval\s*\(',
            'pickle_usage': r'pickle\.(load|loads)',
            'exec_usage': r'\bexec\s*\(',
            'import_star': r'from\s+\w+\s+import\s+\*',
        }
    
    def scan_file(self, filepath):
        """Scan single file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            issues = []
            for vuln_type, pattern in self.patterns.items():
                if re.search(pattern, content):
                    issues.append((filepath.name, vuln_type))
            
            return issues
        except:
            return []
    
    def run(self, limit=100):
        """Run security scan"""
        logger.info("🔍 SECURITY SCAN - Starting...")
        
        workspace = Path(__file__).parent
        exclude = ['node_modules', '.venv', '__pycache__', '.git', 'venv']
        
        count = 0
        for py_file in workspace.rglob('*.py'):
            if any(ex in str(py_file) for ex in exclude):
                continue
            
            issues = self.scan_file(py_file)
            self.vulnerabilities.extend(issues)
            
            count += 1
            if count >= limit:
                break
        
        logger.info(f"✅ Scanned {count} files")
        logger.info(f"🔴 Found {len(self.vulnerabilities)} security issues:")
        
        for filename, vuln_type in self.vulnerabilities[:10]:
            logger.warning(f"   {filename}: {vuln_type}")
        
        return self.vulnerabilities

if __name__ == "__main__":
    scanner = SecurityScanner()
    scanner.run(limit=100)
