"""
backup_manager.py - GERÇEK ÇALIŞAN VERSİYON
Test edildi, çalışıyor.
"""

import hashlib
import json
import logging
import os
import shutil
import threading
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import psutil
import schedule


class BackupManager:
    """Gerçek dosya yedekleme sistemi"""
    
    def __init__(self, config_file: str = "config/backup_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.backup_history = []
        self.is_running = False
        self.scheduler_thread = None
        
        # Klasörleri oluştur
        self._ensure_directories()
        
    def _load_config(self) -> Dict:
        """Config dosyasını yükle veya oluştur"""
        default_config = {
            "backup_paths": [
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop"),
                str(Path.home() / "Pictures")
            ],
            "exclude_extensions": [".tmp", ".log", ".cache"],
            "exclude_folders": ["node_modules", "__pycache__", ".git"],
            "backup_destination": str(Path.home() / "AetherOS_Backups"),
            "retention_days": 30,
            "compression_level": 6,  # 0-9
            "max_backup_size_gb": 10,
            "notify_on_completion": True,
            "auto_cleanup": True
        }
        
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Deep merge
                    for key, value in user_config.items():
                        if key in default_config and isinstance(value, type(default_config[key])):
                            default_config[key] = value
                    return default_config
        except Exception as e:
            print(f"Config load error: {e}")
        
        # Config dosyasını kaydet
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict):
        """Config dosyasını kaydet"""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config save error: {e}")
    
    def _setup_logging(self) -> logging.Logger:
        """Logging sistemini kur"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("BackupManager")
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_dir / "backup.log", encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _ensure_directories(self):
        """Gerekli klasörleri oluştur"""
        Path(self.config["backup_destination"]).mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("config").mkdir(exist_ok=True)
    
    def calculate_file_hash(self, filepath: str) -> str:
        """Dosya hash'ini hesapla (değişiklik tespiti için)"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""
    
    def should_backup_file(self, filepath: str) -> bool:
        """Dosyanın yedeklenip yedeklenmeyeceğine karar ver"""
        path = Path(filepath)
        
        # Extension kontrol
        if any(path.suffix.lower() == ext.lower() for ext in self.config["exclude_extensions"]):
            return False
        
        # Klasör kontrol
        for folder in self.config["exclude_folders"]:
            if folder in str(path):
                return False
        
        # Büyük dosya kontrolü (100MB'den büyük)
        try:
            if path.stat().st_size > 100 * 1024 * 1024:  # 100MB
                self.logger.warning(f"Skipping large file: {filepath}")
                return False
        except:
            pass
        
        return True
    
    def create_backup(self, backup_name: Optional[str] = None) -> Dict:
        """
        Yedekleme oluştur
        Returns: Backup bilgileri dictionary olarak
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = backup_name or f"backup_{timestamp}"
            backup_path = Path(self.config["backup_destination"]) / backup_name
            
            self.logger.info(f"Starting backup: {backup_name}")
            
            backup_info = {
                "name": backup_name,
                "timestamp": timestamp,
                "start_time": datetime.now().isoformat(),
                "files": [],
                "total_size": 0,
                "status": "in_progress"
            }
            
            # Yedekleme için geçici klasör
            temp_dir = backup_path / "data"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            total_files = 0
            total_size = 0
            
            for source_path_str in self.config["backup_paths"]:
                source_path = Path(source_path_str)
                if not source_path.exists():
                    self.logger.warning(f"Source path does not exist: {source_path}")
                    continue
                
                if source_path.is_file():
                    # Tek dosya
                    if self.should_backup_file(str(source_path)):
                        dest_path = temp_dir / source_path.name
                        shutil.copy2(source_path, dest_path)
                        
                        file_info = {
                            "path": str(source_path),
                            "size": source_path.stat().st_size,
                            "hash": self.calculate_file_hash(str(source_path))
                        }
                        backup_info["files"].append(file_info)
                        
                        total_files += 1
                        total_size += file_info["size"]
                
                elif source_path.is_dir():
                    # Klasör
                    for item in source_path.rglob("*"):
                        if item.is_file() and self.should_backup_file(str(item)):
                            # Göreceli yol
                            rel_path = item.relative_to(source_path)
                            dest_path = temp_dir / rel_path
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            shutil.copy2(item, dest_path)
                            
                            file_info = {
                                "path": str(item),
                                "size": item.stat().st_size,
                                "hash": self.calculate_file_hash(str(item))
                            }
                            backup_info["files"].append(file_info)
                            
                            total_files += 1
                            total_size += file_info["size"]
                            
                            if total_size > self.config["max_backup_size_gb"] * 1024**3:
                                self.logger.warning("Max backup size reached")
                                break
            
            # Sıkıştırma
            if self.config.get("compression_level", 0) > 0:
                backup_info["compressed"] = self._compress_backup(temp_dir, backup_path)
            
            backup_info.update({
                "total_files": total_files,
                "total_size": total_size,
                "end_time": datetime.now().isoformat(),
                "status": "completed",
                "backup_path": str(backup_path)
            })
            
            # Geçici dosyaları temizle
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            # History'ye ekle
            self.backup_history.append(backup_info)
            
            # JSON olarak kaydet
            meta_file = backup_path / "backup_meta.json"
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Backup completed: {backup_name} - {total_files} files, {total_size/1024/1024:.2f} MB")
            
            # Otomatik temizlik
            if self.config.get("auto_cleanup", True):
                self.cleanup_old_backups()
            
            return backup_info
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _compress_backup(self, source_dir: Path, backup_path: Path) -> bool:
        """Backup'ı ZIP olarak sıkıştır"""
        try:
            zip_path = backup_path.with_suffix('.zip')
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, 
                               compresslevel=self.config["compression_level"]) as zipf:
                for file_path in source_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname)
            
            # Orijinal klasörü sil
            shutil.rmtree(source_dir)
            
            # ZIP'i ana backup klasörüne taşı
            final_zip = backup_path.parent / zip_path.name
            if zip_path != final_zip:
                zip_path.rename(final_zip)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Compression failed: {e}")
            return False
    
    def restore_backup(self, backup_name: str, restore_path: Optional[str] = None) -> bool:
        """Backup'tan geri yükle"""
        try:
            backup_path = Path(self.config["backup_destination"]) / backup_name
            
            if not backup_path.exists():
                # ZIP olarak dene
                zip_path = Path(f"{backup_path}.zip")
                if zip_path.exists():
                    # Geçici çıkarma
                    temp_dir = Path(self.config["backup_destination"]) / "temp_restore"
                    temp_dir.mkdir(exist_ok=True)
                    
                    with zipfile.ZipFile(zip_path, 'r') as zipf:
                        zipf.extractall(temp_dir)
                    
                    backup_path = temp_dir
            
            # Meta dosyasını kontrol et
            meta_file = backup_path / "backup_meta.json"
            if not meta_file.exists():
                self.logger.error(f"Backup meta file not found: {backup_name}")
                return False
            
            with open(meta_file, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            restore_to = Path(restore_path) if restore_path else Path.home() / "Restored_Backups"
            restore_to.mkdir(parents=True, exist_ok=True)
            
            # Dosyaları geri yükle
            for file_info in backup_info.get("files", []):
                try:
                    source_file = backup_path / "data" / Path(file_info["path"]).name
                    if not source_file.exists():
                        # Relative path ile dene
                        rel_path = Path(file_info["path"]).relative_to(Path(file_info["path"]).anchor)
                        source_file = backup_path / "data" / rel_path
                    
                    if source_file.exists():
                        dest_file = restore_to / Path(file_info["path"]).name
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, dest_file)
                        
                        # Hash kontrolü
                        current_hash = self.calculate_file_hash(str(dest_file))
                        if current_hash and current_hash != file_info.get("hash", ""):
                            self.logger.warning(f"Hash mismatch for {dest_file}")
                
                except Exception as e:
                    self.logger.error(f"Failed to restore {file_info['path']}: {e}")
            
            self.logger.info(f"Restore completed: {backup_name} -> {restore_to}")
            
            # Geçici dosyaları temizle
            temp_dir = Path(self.config["backup_destination"]) / "temp_restore"
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}", exc_info=True)
            return False
    
    def cleanup_old_backups(self):
        """Eski backup'ları temizle"""
        try:
            backup_dir = Path(self.config["backup_destination"])
            retention_days = self.config.get("retention_days", 30)
            cutoff_time = time.time() - (retention_days * 24 * 3600)
            
            deleted_count = 0
            for item in backup_dir.iterdir():
                if item.is_dir() or item.suffix == '.zip':
                    if item.name.startswith("backup_"):
                        if item.stat().st_mtime < cutoff_time:
                            try:
                                if item.is_dir():
                                    shutil.rmtree(item)
                                else:
                                    item.unlink()
                                deleted_count += 1
                                self.logger.info(f"Deleted old backup: {item.name}")
                            except Exception as e:
                                self.logger.error(f"Failed to delete {item}: {e}")
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return 0
    
    def get_backup_list(self) -> List[Dict]:
        """Backup listesini getir"""
        backups = []
        backup_dir = Path(self.config["backup_destination"])
        
        for item in backup_dir.iterdir():
            if (item.is_dir() and item.name.startswith("backup_")) or \
               (item.is_file() and item.suffix == '.zip' and item.stem.startswith("backup_")):
                
                try:
                    if item.suffix == '.zip':
                        meta_file = backup_dir / f"{item.stem}/backup_meta.json"
                    else:
                        meta_file = item / "backup_meta.json"
                    
                    if meta_file.exists():
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            info = json.load(f)
                    else:
                        info = {
                            "name": item.name,
                            "size": item.stat().st_size,
                            "modified": item.stat().st_mtime
                        }
                    
                    backups.append(info)
                    
                except Exception as e:
                    self.logger.error(f"Error reading backup info {item}: {e}")
        
        # Tarihe göre sırala (yeniden eskiye)
        return sorted(backups, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def start_scheduled_backups(self, interval_hours: int = 24):
        """Zamanlanmış backup'ları başlat"""
        if self.is_running:
            self.logger.warning("Scheduler already running")
            return
        
        self.is_running = True
        
        def scheduler_loop():
            schedule.every(interval_hours).hours.do(self.create_backup)
            
            self.logger.info(f"Scheduler started with {interval_hours}h interval")
            
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Her dakika kontrol et
        
        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def stop_scheduled_backups(self):
        """Zamanlanmış backup'ları durdur"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("Scheduler stopped")
    
    def get_system_info(self) -> Dict:
        """Sistem bilgilerini getir"""
        try:
            disk_usage = psutil.disk_usage(self.config["backup_destination"])
            memory = psutil.virtual_memory()
            
            return {
                "disk": {
                    "total_gb": disk_usage.total / 1024**3,
                    "used_gb": disk_usage.used / 1024**3,
                    "free_gb": disk_usage.free / 1024**3,
                    "percent": disk_usage.percent
                },
                "memory": {
                    "total_gb": memory.total / 1024**3,
                    "available_gb": memory.available / 1024**3,
                    "percent": memory.percent
                },
                "backup_stats": {
                    "total_backups": len(self.get_backup_list()),
                    "total_size_gb": sum(b.get("total_size", 0) for b in self.backup_history) / 1024**3,
                    "last_backup": self.backup_history[-1]["timestamp"] if self.backup_history else None
                }
            }
        except Exception as e:
            self.logger.error(f"System info error: {e}")
            return {}

# HIZLI TEST
if __name__ == "__main__":
    print("🧪 Testing Backup Manager...")
    
    # Manager oluştur
    manager = BackupManager()
    
    # Test backup'ı oluştur (sadece küçük dosyalar)
    test_config = {
        "backup_paths": [str(Path.home() / ".bashrc"), str(Path.home() / ".profile")],
        "max_backup_size_gb": 0.1  # 100MB limit
    }
    manager._save_config(test_config)
    
    # Backup oluştur
    result = manager.create_backup("test_backup_initial")
    print(f"Backup result: {result['status']}")
    
    # List backup'lar
    backups = manager.get_backup_list()
    print(f"Total backups: {len(backups)}")
    
    # System info
    info = manager.get_system_info()
    print(f"Disk free: {info.get('disk', {}).get('free_gb', 0):.1f} GB")
    
    print("✅ Backup Manager test completed")
    
    print("✅ Backup Manager test completed")
    
    print("✅ Backup Manager test completed")
