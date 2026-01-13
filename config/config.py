import os
from pathlib import Path


def get_config():
    """Basit proje yapılandırması."""
    return {
        "version": "4.0.0-AUTONOMOUS",
        "author": "GitHub Copilot & Nexus",
        "cpu_gentle_mode": True,
        "sync_interval_mins": 5,
        "backup_enabled": True
    }

def setup_directories():
    """Gerekli klasörleri oluşturur."""
    dirs = [
        "nexus_logs",
        "infinite_knowledge",
        "nexus_backups",
        "nexus_data"
    ]
    base = Path(__file__).parent.parent
    for d in dirs:
        (base / d).mkdir(exist_ok=True)
