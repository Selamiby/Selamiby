#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NEXUS REALTIME WORKER - ANLIK OTOMATIK ÇALIŞMA
===================================================
Her anlık olarak workspace'i tarayıp geliştirme yapan sistem!
İZİN SORMADAN, DURMADAN ÇALIŞIR!
"""

import json
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Logging
log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(log_dir / "realtime_worker.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class RealtimeWorker:
    """Anlık otomatik çalışma sistemi"""

    def __init__(self):
        self.workspace = Path(__file__).parent
        self.work_count = 0
        self.files_improved = 0
        self.features_created = 0

        logger.info("🔥 REALTIME WORKER BAŞLATILDI!")
        logger.info("⚡ ANLIK OTOMATIK ÇALIŞMA MODU AKTIF")

    def find_improvement_opportunities(self) -> List[Path]:
        """İyileştirme fırsatları bul"""
        candidates = []

        # Python dosyalarını tara
        for py_file in self.workspace.glob("*.py"):
            if py_file.name in [
                "nexus_continuous_improver.py",
                "nexus_realtime_worker.py",
            ]:
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # İyileştirme fırsatı var mı?
                if any(
                    marker in content
                    for marker in ["TODO", "FIXME", "HACK", "\n\n\n\n"]
                ):
                    candidates.append(py_file)
            except:
                pass

        return candidates[:5]  # İlk 5 dosya

    def improve_file_now(self, filepath: Path) -> bool:
        """Dosyayı HEMEN iyileştir"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            improvements = []

            # 1. Fazla boş satırları temizle
            if "\n\n\n\n" in content:
                content = content.replace("\n\n\n\n", "\n\n\n")
                improvements.append("Fazla boş satır temizlendi")

            # 2. Trailing whitespace temizle
            lines = content.split("\n")
            cleaned = [line.rstrip() for line in lines]
            if cleaned != lines:
                content = "\n".join(cleaned)
                improvements.append("Trailing whitespace temizlendi")

            # 3. Import sıralaması kontrol
            if "import " in content:
                import_lines = [
                    l for l in lines if l.startswith("import ") or l.startswith("from ")
                ]
                if import_lines != sorted(import_lines):
                    improvements.append("Import sırası optimize edilebilir")

            # Değişiklik varsa kaydet
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                logger.info(f"✅ İYİLEŞTİRME: {filepath.name}")
                for imp in improvements:
                    logger.info(f"   - {imp}")

                self.files_improved += 1
                return True

        except Exception as e:
            logger.error(f"❌ Hata ({filepath.name}): {e}")

        return False

    def create_utility_module(self):
        """Yeni utility modülü oluştur"""
        utilities = {
            "time_tracker.py": '''#!/usr/bin/env python3
"""Time Tracker - Zaman takip modülü"""
import time
from functools import wraps
from datetime import datetime

class TimeTracker:
    """Zaman takip sistemi"""

    def __init__(self):
        self.timings = {}

    def track(self, name: str):
        """Zaman takip decorator"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start

                if name not in self.timings:
                    self.timings[name] = []
                self.timings[name].append(elapsed)

                print(f"⏱️ {name}: {elapsed:.3f}s")
                return result
            return wrapper
        return decorator

    def get_average(self, name: str) -> float:
        """Ortalama süre"""
        if name in self.timings:
            return sum(self.timings[name]) / len(self.timings[name])
        return 0.0
''',
            "data_validator.py": '''#!/usr/bin/env python3
"""Data Validator - Veri doğrulama modülü"""
from typing import Any, Dict, List

class DataValidator:
    """Veri doğrulama sistemi"""

    @staticmethod
    def validate_dict(data: Dict, required_keys: List[str]) -> bool:
        """Dictionary doğrula"""
        return all(key in data for key in required_keys)

    @staticmethod
    def validate_type(data: Any, expected_type: type) -> bool:
        """Tip doğrula"""
        return isinstance(data, expected_type)

    @staticmethod
    def validate_range(value: int, min_val: int, max_val: int) -> bool:
        """Aralık doğrula"""
        return min_val <= value <= max_val
''',
            "config_manager.py": '''#!/usr/bin/env python3
"""Config Manager - Konfigürasyon yönetimi"""
import json
from pathlib import Path

class ConfigManager:
    """Konfigürasyon yönetim sistemi"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self.load()

    def load(self) -> dict:
        """Konfigürasyon yükle"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def save(self):
        """Konfigürasyon kaydet"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        """Değer al"""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Değer ayarla"""
        self.config[key] = value
        self.save()
''',
        }

        # Rastgele bir utility seç ve oluştur
        util_name, util_code = random.choice(list(utilities.items()))
        util_path = self.workspace / "generated_utilities" / util_name
        util_path.parent.mkdir(exist_ok=True)

        if not util_path.exists():
            with open(util_path, "w", encoding="utf-8") as f:
                f.write(util_code)

            logger.info(f"✅ YENİ UTILITY: {util_name}")
            self.features_created += 1
            return True

        return False

    def work_cycle(self):
        """Çalışma döngüsü"""
        self.work_count += 1

        logger.info(f"\n{'='*60}")
        logger.info(f"🔥 WORK CYCLE #{self.work_count}")
        logger.info(f"{'='*60}")

        # 1. İyileştirme fırsatları bul
        opportunities = self.find_improvement_opportunities()
        logger.info(f"📊 {len(opportunities)} dosya iyileştirme bekliyor")

        # 2. Dosyaları iyileştir
        if opportunities:
            target = random.choice(opportunities)
            self.improve_file_now(target)

        # 3. Her 3 döngüde bir yeni utility oluştur
        if self.work_count % 3 == 0:
            self.create_utility_module()

        # 4. İstatistikler
        if self.work_count % 5 == 0:
            logger.info(f"\n📊 TOPLAM İSTATİSTİKLER:")
            logger.info(f"   ✅ Döngü: {self.work_count}")
            logger.info(f"   ✅ İyileştirilen dosya: {self.files_improved}")
            logger.info(f"   ✅ Oluşturulan feature: {self.features_created}")

    def run_forever(self):
        """Sonsuza kadar çalış"""
        logger.info("\n" + "🔥" * 40)
        logger.info("🚀 REALTIME WORKER - NON-STOP MODE!")
        logger.info("🔥" * 40 + "\n")

        while True:
            try:
                self.work_cycle()

                # 15 saniye bekle (daha hızlı)
                logger.info(
                    f"⏸️ 15 saniye bekleniyor... (Cycle {self.work_count} tamamlandı)"
                )
                time.sleep(15)

            except KeyboardInterrupt:
                logger.info("\n⚠️ DURDURULDU")
                break
            except Exception as e:
                logger.error(f"❌ Hata: {e}")
                time.sleep(15)
                continue

        logger.info(f"\n✅ REALTIME WORKER DURDURULDU")
        logger.info(f"📊 {self.work_count} döngü tamamlandı")


if __name__ == "__main__":
    worker = RealtimeWorker()
    worker.run_forever()
