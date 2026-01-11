"""
backend/utils.py - Yardımcı fonksiyonlar
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def load_config(config_path: str) -> Dict:
    """Config dosyasını yükle (JSON veya YAML)"""
    path = Path(config_path)
    if not path.exists():
        return {}
    
    if path.suffix.lower() in ['.yaml', '.yml']:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

def save_config(config: Dict, config_path: str):
    """Config dosyasını kaydet"""
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if path.suffix.lower() in ['.yaml', '.yml']:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

from typing import Optional


def setup_logger(name: str, log_file: Optional[str] = None, level=logging.INFO):
    """Logger kurulumu"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def calculate_sha256(filepath: str) -> str:
    """Dosyanın SHA256 hash'ini hesapla"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def format_bytes(size: int) -> str:
    """Byte'ları okunabilir formata çevir"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size = int(size / 1024.0)
    return f"{size:.2f} PB"

def humanize_time(seconds: int) -> str:
    """Saniyeyi insan dostu formata çevir"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minutes"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hours"
    else:
        days = seconds // 86400
        return f"{days} days"

def get_system_info() -> Dict:
    """Temel sistem bilgilerini getir"""
    import platform

    import psutil
    
    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        },
        "hardware": {
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "total_memory": psutil.virtual_memory().total,
            "total_disk": psutil.disk_usage('/').total
        }
    }

def ensure_directories(directories: List[str]):
    """Dizinleri oluştur"""
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def validate_email(email: str) -> bool:
    """Email adresini doğrula"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def retry(func, max_retries=3, delay=1, exceptions=(Exception,)):
    """Retry decorator"""
    import time
    
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise last_exception
        if last_exception:
            raise last_exception
        else:
            raise Exception("Bilinmeyen hata")
    
    return wrapper

class Singleton(type):
    """Singleton metaclass"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
