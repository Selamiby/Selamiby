import os
from pathlib import Path

from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Proje yolları
BASE_DIR = Path(__file__).parent.parent # config dizininden bir üste çık
DATA_DIR = BASE_DIR / "nexus_data"
LOGS_DIR = BASE_DIR / "nexus_logs"
BACKUP_DIR = BASE_DIR / "nexus_backups"

# Ana yapılandırma sözlüğü
CONFIG = {
    "APP_NAME": "Nexus-One Real",
    "BASE_DIR": BASE_DIR,
    "DATA_DIR": DATA_DIR,
    "LOGS_DIR": LOGS_DIR,
    "BACKUP_DIR": BACKUP_DIR,
    "API_KEYS": {
        "newsapi": os.getenv("NEWSAPI_KEY", ""),
        "weatherapi": os.getenv("WEATHERAPI_KEY", ""),
        "translate": os.getenv("TRANSLATE_KEY", "")
    },
    "SYSTEM_SETTINGS": {
        "MAX_LOG_FILES": 100,
        "LOG_RETENTION_DAYS": 30,
        "BACKUP_RETENTION_DAYS": 7
    }
}

def setup_directories():
    """Gerekli dizinleri oluşturur."""
    print("📂 Gerekli dizinler kontrol ediliyor/oluşturuluyor...")
    for directory in [DATA_DIR, LOGS_DIR, BACKUP_DIR]:
        directory.mkdir(exist_ok=True)
    print("✅ Dizinler hazır.")

def get_config():
    """Yapılandırma sözlüğünü döndürür."""
    return CONFIG

