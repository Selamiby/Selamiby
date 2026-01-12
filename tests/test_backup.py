"""
Backup Manager testleri
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.backup_manager import BackupManager


class TestBackupManager(unittest.TestCase):
    def setUp(self):
        # Test için geçici dizin
        self.test_dir = Path(tempfile.mkdtemp())
        self.backup_dir = self.test_dir / "backups"
        self.source_dir = self.test_dir / "source"

        # Test dosyaları oluştur
        self.source_dir.mkdir()
        (self.source_dir / "test1.txt").write_text("Test content 1")
        (self.source_dir / "test2.txt").write_text("Test content 2")

        # Config
        self.config = {
            "backup": {
                "paths": [str(self.source_dir)],
                "destination": str(self.backup_dir),
                "compression": False,
                "verify_backup": False,
            }
        }

    def test_backup_creation(self):
        """Backup oluşturma testi"""
        manager = BackupManager(str(self.backup_dir))
        result = manager.create_backup(str(self.source_dir))
        self.assertTrue(result["success"], msg=result)
        # Yedek dosyası/dizini oluştu mu?
        backups = list(self.backup_dir.glob("*"))
        self.assertTrue(len(backups) > 0)

    def tearDown(self):
        # Temizlik
        shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
