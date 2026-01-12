"""
File Organizer - Otomatik dosya düzenleyici modül
"""

import os
from pathlib import Path
from typing import List


class FileOrganizer:
    CATEGORY_MAP = {"txt": ["txt"], "log": ["log"], "other": []}

    def generate_report(self, path: str):
        """Belirtilen dizindeki dosyaları kategori bazında raporlar."""
        from collections import defaultdict

        import humanize

        p = Path(path)
        report = {"categories": {}}
        ext_map = {}
        for cat, exts in self.CATEGORY_MAP.items():
            for ext in exts:
                ext_map[ext] = cat
        cat_info = defaultdict(lambda: {"count": 0, "size": 0, "size_human": "0B"})
        for file in p.rglob("*"):
            if file.is_file():
                ext = file.suffix[1:] if file.suffix else "other"
                cat = ext_map.get(ext, "other")
                cat_info[cat]["count"] += 1
                size = file.stat().st_size
                cat_info[cat]["size"] += size
        for cat, info in cat_info.items():
            info["size_human"] = self._human_readable(info["size"])
            report["categories"][cat] = info
        return report

    @staticmethod
    def _human_readable(num, suffix="B"):
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(num) < 1024.0:
                return f"{num:3.2f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.2f}Y{suffix}"

    def __init__(self, watch_paths: List[str] = None):
        self.watch_paths = watch_paths or []

    def organize(self, path: str):
        # Basit örnek: dosyaları uzantısına göre alt klasörlere taşı
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return False
        for file in p.iterdir():
            if file.is_file():
                ext = file.suffix[1:] if file.suffix else "other"
                target_dir = p / ext
                target_dir.mkdir(exist_ok=True)
                file.rename(target_dir / file.name)
        return True

    def organize_all(self):
        for path in self.watch_paths:
            self.organize(path)
            self.organize(path)
            self.organize(path)
            self.organize(path)
            self.organize(path)
