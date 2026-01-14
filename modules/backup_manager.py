import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:17
🚀 Status: ACTIVE / PRODUCTION
"""

"""
Seviye 1: Otonom Backup Sistemi
Kritik dosyaları otomatik yedekleme, backup schedule management, bütünlük kontrolü
"""

import hashlib
import json
import os
import shutil
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class BackupManager:
    """Otonom yedekleme sistemi"""

    def __init__(self, backup_dir: str = "data/backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backup_manifest = self.backup_dir / "manifest.json"
        self.backups = self._load_manifest()

    def create_backup(
        self, source_path: str, name: Optional[str] = None, backup_type: str = "full"
    ) -> Dict:
        """Yedek oluştur"""
        source = Path(source_path)
        if not source.exists():
            return {"success": False, "error": f"Path not found: {source_path}"}

        backup_name = name or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_name

        try:
            if source.is_file():
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, backup_path)
            else:
                shutil.copytree(source, backup_path, dirs_exist_ok=True)

            # Manifest'e ekle
            backup_info = {
                "name": backup_name,
                "source": str(source),
                "type": backup_type,
                "created": datetime.now().isoformat(),
                "path": str(backup_path),
                "hash": self._calculate_dir_hash(backup_path),
            }

            self.backups[backup_name] = backup_info
            self._save_manifest()

            return {
                "success": True,
                "backup": backup_name,
                "path": str(backup_path),
                "size": self._get_dir_size(backup_path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def restore_backup(self, backup_name: str, restore_path: str) -> Dict:
        """Yedekten geri yükle"""
        if backup_name not in self.backups:
            return {"success": False, "error": f"Backup not found: {backup_name}"}

        backup_path = Path(self.backups[backup_name]["path"])

        try:
            restore_target = Path(restore_path)

            if backup_path.is_file():
                restore_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_path, restore_target)
            else:
                if restore_target.exists():
                    shutil.rmtree(restore_target)
                shutil.copytree(backup_path, restore_target)

            return {
                "success": True,
                "restored_to": str(restore_target),
                "backup_name": backup_name,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_backup(self, backup_name: str) -> Dict:
        """Yedek bütünlüğünü kontrol et"""
        if backup_name not in self.backups:
            return {"success": False, "error": f"Backup not found: {backup_name}"}

        backup_info = self.backups[backup_name]
        backup_path = Path(backup_info["path"])

        if not backup_path.exists():
            return {
                "success": False,
                "status": "MISSING",
                "error": "Backup path not found",
            }

        # Hash kontrol et
        current_hash = self._calculate_dir_hash(backup_path)
        original_hash = backup_info.get("hash", "")

        return {
            "success": True,
            "backup_name": backup_name,
            "status": "VALID" if current_hash == original_hash else "CORRUPTED",
            "path": str(backup_path),
            "size": self._get_dir_size(backup_path),
            "created": backup_info["created"],
        }

    def schedule_backup(
        self, source_path: str, interval_hours: int = 24, max_backups: int = 5
    ) -> Dict:
        """Periyodik yedek zamanla"""
        backup_name = f"scheduled_{Path(source_path).name}_{int(time.time())}"

        def backup_thread():
            while True:
                self.create_backup(
                    source_path, name=backup_name, backup_type="incremental"
                )

                # Eski yedekleri sil
                self._cleanup_old_backups(max_backups)

                time.sleep(interval_hours * 3600)

        thread = threading.Thread(target=backup_thread, daemon=True)
        thread.start()

        return {
            "success": True,
            "scheduled": backup_name,
            "interval_hours": interval_hours,
            "max_backups": max_backups,
        }

    def list_backups(self) -> Dict:
        """Tüm yedekleri listele"""
        backups_list = []

        for name, info in self.backups.items():
            backup_path = Path(info["path"])
            backups_list.append(
                {
                    "name": name,
                    "source": info["source"],
                    "type": info["type"],
                    "created": info["created"],
                    "size": (
                        self._get_dir_size(backup_path) if backup_path.exists() else 0
                    ),
                    "status": "OK" if backup_path.exists() else "MISSING",
                }
            )

        return {
            "total_backups": len(backups_list),
            "backups": sorted(backups_list, key=lambda x: x["created"], reverse=True),
        }

    def cleanup_old_backups(self, days: int = 30) -> Dict:
        """Belirtilen günden eski yedekleri sil"""
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted = []

        for name, info in list(self.backups.items()):
            created = datetime.fromisoformat(info["created"])

            if created < cutoff_date:
                backup_path = Path(info["path"])
                try:
                    if backup_path.is_file():
                        backup_path.unlink()
                    else:
                        shutil.rmtree(backup_path)
                    del self.backups[name]
                    deleted.append(name)
                except Exception:
                    pass

        self._save_manifest()

        return {"deleted": len(deleted), "deleted_backups": deleted}

    def _cleanup_old_backups(self, max_count: int):
        """Yedek sayısını sınırla"""
        if len(self.backups) > max_count:
            sorted_backups = sorted(self.backups.items(), key=lambda x: x[1]["created"])

            to_delete = len(self.backups) - max_count
            for name, info in sorted_backups[:to_delete]:
                backup_path = Path(info["path"])
                try:
                    if backup_path.is_file():
                        backup_path.unlink()
                    else:
                        shutil.rmtree(backup_path)
                    del self.backups[name]
                except Exception:
                    pass

            self._save_manifest()

    def _calculate_dir_hash(self, path: Path) -> str:
        """Dizin hash'ini hesapla"""
        hash_obj = hashlib.md5()

        for file_path in sorted(path.rglob("*")):
            if file_path.is_file():
                try:
                    with open(file_path, "rb") as f:
                        hash_obj.update(f.read())
                except Exception:
                    pass

        return hash_obj.hexdigest()

    def _get_dir_size(self, path: Path) -> int:
        """Dizin boyutunu hesapla"""
        total = 0

        try:
            if path.is_file():
                return path.stat().st_size

            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
        except Exception:
            pass

        return total

    def _load_manifest(self) -> Dict:
        """Manifest dosyasını yükle"""
        if self.backup_manifest.exists():
            try:
                with open(self.backup_manifest, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_manifest(self):
        """Manifest dosyasını kaydet"""
        with open(self.backup_manifest, "w") as f:
            json.dump(self.backups, f, indent=2)


# Global instance
backup_manager = BackupManager()
