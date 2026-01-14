"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:19
🚀 Status: ACTIVE / PRODUCTION
"""

"""
Seviye 1: Akıllı Sistem Bakımı
Temp dosyaları temizleme, disk analizi, gereksiz paketleri tespit etme
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import psutil


class SystemMaintenance:
    """Sistem bakım ve optimizasyon"""

    # Temp dosya konumları
    TEMP_LOCATIONS = [
        Path(os.getenv("TEMP", "/tmp")),
        Path(os.getenv("TMP", "/tmp")),
        Path.home() / "AppData" / "Local" / "Temp",
    ]

    # Sisteme kritik klasörler
    CRITICAL_PATHS = [
        Path.home() / "AppData" / "Local" / "Programs",
        Path.home() / "Documents",
        Path.home() / "Desktop",
    ]

    def __init__(self):
        self.disk_stats = {}

    def analyze_disk(self, path: str = "/") -> Dict:
        """Disk kullanımını analiz et"""
        try:
            disk = psutil.disk_usage(path)

            usage_percent = (disk.used / disk.total) * 100

            return {
                "path": path,
                "total_gb": disk.total / (1024**3),
                "used_gb": disk.used / (1024**3),
                "free_gb": disk.free / (1024**3),
                "percent": usage_percent,
                "status": self._get_disk_status(usage_percent),
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze_directory(self, directory: str = ".") -> Dict:
        """Dizin boyutunu ve içeriğini analiz et"""
        dir_path = Path(directory)

        if not dir_path.exists():
            return {"error": f"Directory not found: {directory}"}

        categories = {}
        total_size = 0
        file_count = 0

        try:
            for item in dir_path.rglob("*"):
                if item.is_file():
                    size = item.stat().st_size
                    ext = item.suffix.lower() or "no_extension"

                    if ext not in categories:
                        categories[ext] = {"count": 0, "size": 0}

                    categories[ext]["count"] += 1
                    categories[ext]["size"] += size
                    total_size += size
                    file_count += 1
        except Exception:
            pass

        # Boyuta göre sırala
        sorted_categories = sorted(
            categories.items(), key=lambda x: x[1]["size"], reverse=True
        )

        return {
            "directory": str(dir_path),
            "total_files": file_count,
            "total_size_mb": total_size / (1024**2),
            "total_size_human": self._format_size(total_size),
            "categories": {
                ext: {
                    "count": info["count"],
                    "size_mb": info["size"] / (1024**2),
                    "size_human": self._format_size(info["size"]),
                }
                for ext, info in sorted_categories
            },
        }

    def cleanup_temp_files(self, dry_run: bool = True) -> Dict:
        """Temp dosyaları temizle"""
        deleted = []
        freed_space = 0
        errors = []

        for temp_dir in self.TEMP_LOCATIONS:
            if not temp_dir.exists():
                continue

            try:
                for item in temp_dir.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            if not dry_run:
                                item.unlink()
                            deleted.append(str(item))
                            freed_space += size
                        elif item.is_dir():
                            size = self._get_dir_size(item)
                            if not dry_run:
                                shutil.rmtree(item)
                            deleted.append(str(item))
                            freed_space += size
                    except Exception as e:
                        errors.append(f"{str(item)}: {str(e)}")
            except Exception as e:
                errors.append(f"{str(temp_dir)}: {str(e)}")

        return {
            "dry_run": dry_run,
            "deleted_count": len(deleted),
            "freed_space_mb": freed_space / (1024**2),
            "freed_space_human": self._format_size(freed_space),
            "deleted_items": deleted[:10],  # İlk 10
            "errors": errors,
        }

    def find_large_files(self, directory: str = ".", min_size_mb: int = 50) -> Dict:
        """Belirtilen boyuttan büyük dosyaları bul"""
        large_files = []
        min_bytes = min_size_mb * 1024 * 1024

        try:
            for file_path in Path(directory).rglob("*"):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size >= min_bytes:
                            large_files.append(
                                {
                                    "path": str(file_path),
                                    "size_mb": size / (1024**2),
                                    "size_human": self._format_size(size),
                                }
                            )
                    except Exception:
                        pass
        except Exception:
            pass

        large_files.sort(key=lambda x: x["size_mb"], reverse=True)

        return {
            "large_files_count": len(large_files),
            "files": large_files[:20],  # Top 20
        }

    def get_system_stats(self) -> Dict:
        """Sistem istatistiklerini al"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_mb": memory.used / (1024**2),
                "memory_total_mb": memory.total / (1024**2),
                "disk": self.analyze_disk(),
                "status": self._get_system_health_status(cpu_percent, memory.percent),
            }
        except Exception as e:
            return {"error": str(e)}

    def find_old_files(self, directory: str = ".", days: int = 30) -> Dict:
        """Belirtilen günden eski dosyaları bul"""
        cutoff_date = datetime.now() - timedelta(days=days)
        old_files = []

        try:
            for file_path in Path(directory).rglob("*"):
                if file_path.is_file():
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime < cutoff_date:
                            old_files.append(
                                {
                                    "path": str(file_path),
                                    "last_modified": mtime.isoformat(),
                                    "age_days": (datetime.now() - mtime).days,
                                }
                            )
                    except Exception:
                        pass
        except Exception:
            pass

        old_files.sort(key=lambda x: x["last_modified"])

        return {
            "old_files_count": len(old_files),
            "threshold_days": days,
            "files": old_files[:20],  # Top 20
        }

    def health_report(self) -> Dict:
        """Sistem sağlığı raporu oluştur"""
        return {
            "timestamp": datetime.now().isoformat(),
            "disk": self.analyze_disk(),
            "system": self.get_system_stats(),
            "temp_files": self.cleanup_temp_files(dry_run=True),
            "large_files": self.find_large_files(min_size_mb=100),
        }

    def _get_dir_size(self, path: Path) -> int:
        """Dizin boyutunu hesapla"""
        total = 0
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
        except Exception:
            pass
        return total

    def _format_size(self, size: int) -> str:
        """Boyutu insan okunur formata çevir"""
        size_float = float(size)
        for unit in ["B", "KB", "MB", "GB"]:
            if size_float < 1024:
                return f"{size_float:.2f} {unit}"
            size_float /= 1024
        return f"{size_float:.2f} TB"

    def _get_disk_status(self, percent: float) -> str:
        """Disk durumunu belirle"""
        if percent < 50:
            return "GOOD"
        elif percent < 80:
            return "WARNING"
        elif percent < 90:
            return "CRITICAL"
        else:
            return "FULL"

    def _get_system_health_status(self, cpu: float, memory: float) -> str:
        """Sistem sağlığını belirle"""
        if cpu > 80 or memory > 85:
            return "CRITICAL"
        elif cpu > 60 or memory > 70:
            return "WARNING"
        else:
            return "HEALTHY"


# Global instance
system_maintenance = SystemMaintenance()
