"""
File Organizer testleri
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.file_organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_organizer_dir")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "a.txt").write_text("A")
        (self.test_dir / "b.log").write_text("B")
        (self.test_dir / "c").write_text("C")

    def test_organize(self):
        organizer = FileOrganizer()
        result = organizer.organize(str(self.test_dir))
        self.assertTrue(result)
        # Dosyalar uzantı klasörlerine taşınmalı
        self.assertTrue((self.test_dir / "txt" / "a.txt").exists())
        self.assertTrue((self.test_dir / "log" / "b.log").exists())
        self.assertTrue((self.test_dir / "other" / "c").exists())

    def tearDown(self):
        for child in self.test_dir.rglob("*"):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                try:
                    child.rmdir()
                except Exception:
                    pass
        try:
            self.test_dir.rmdir()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
    unittest.main()
    unittest.main()
