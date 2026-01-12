"""
AetherOS File Manager - Akıllı Dosya Yöneticisi
"""

import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class FileManager:
    def __init__(self):
        self.history = []
        self.stats = {
            "files_created": 0,
            "files_deleted": 0,
            "files_moved": 0,
            "total_operations": 0,
        }

    def log_operation(self, action: str, details: Dict):
        """İşlem geçmişine kaydet"""
        log_entry = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "details": details,
        }
        self.history.append(log_entry)
        self.stats["total_operations"] += 1

        if len(self.history) > 100:
            self.history = self.history[-100:]

    def get_current_directory(self) -> Dict:
        """Mevcut dizin bilgilerini getir"""
        current_path = Path.cwd()

        try:
            stat = current_path.stat()
            return {
                "path": str(current_path),
                "exists": True,
                "is_directory": True,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size,
            }
        except Exception as e:
            return {"path": str(current_path), "exists": False, "error": str(e)}

    def list_contents(self, path: str = ".", show_hidden: bool = False) -> Dict:
        """Dizin içeriğini listele"""
        try:
            target_path = Path(path).absolute()

            if not target_path.exists():
                return {"error": f"Path not found: {path}"}

            if not target_path.is_dir():
                return {"error": f"Not a directory: {path}"}

            files = []
            directories = []

            for item in target_path.iterdir():
                if not show_hidden and item.name.startswith("."):
                    continue

                try:
                    stat = item.stat()
                    info = {
                        "name": item.name,
                        "path": str(item),
                        "is_file": item.is_file(),
                        "is_dir": item.is_dir(),
                        "size": stat.st_size if item.is_file() else 0,
                        "size_human": (
                            self._format_size(stat.st_size) if item.is_file() else "DIR"
                        ),
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "permissions": oct(stat.st_mode)[-3:],
                        "extension": item.suffix.lower() if item.is_file() else "",
                    }

                    if item.is_file():
                        files.append(info)
                    else:
                        directories.append(info)
                except Exception:
                    continue

            directories.sort(key=lambda x: x["name"].lower())
            files.sort(key=lambda x: x["name"].lower())

            result = {
                "path": str(target_path),
                "parent": str(target_path.parent),
                "items_found": len(directories) + len(files),
                "directories_count": len(directories),
                "files_count": len(files),
                "total_size": sum(f["size"] for f in files),
                "total_size_human": self._format_size(sum(f["size"] for f in files)),
                "directories": directories[:50],
                "files": files[:100],
            }

            self.log_operation(
                "list_contents", {"path": path, "items_found": result["items_found"]}
            )

            return result

        except Exception as e:
            return {"error": f"Error listing directory: {str(e)}"}

    def create_file(
        self, filename: str, content: str = "", overwrite: bool = False
    ) -> Dict:
        """Dosya oluştur"""
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            if filepath.exists() and not overwrite:
                return {
                    "success": False,
                    "error": f"File already exists: {filename}",
                    "suggestion": "Use overwrite=True to replace",
                }

            if not content:
                content = f"""# AetherOS Generated File
# Created: {datetime.now().isoformat()}
# File: {filename}
"""

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            self.stats["files_created"] += 1

            self.log_operation(
                "create_file",
                {"filename": filename, "size": len(content), "overwrite": overwrite},
            )

            return {
                "success": True,
                "message": f"File created: {filename}",
                "filename": filename,
                "path": str(filepath.absolute()),
                "size": len(content),
                "size_human": self._format_size(len(content)),
                "created": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating file: {str(e)}",
                "filename": filename,
            }

    def read_file(self, filepath: str, max_lines: int = 100) -> Dict:
        """Dosyayı oku"""
        try:
            path = Path(filepath)

            if not path.exists():
                return {"error": f"File not found: {filepath}"}

            if not path.is_file():
                return {"error": f"Not a file: {filepath}"}

            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            content = "".join(lines)

            result = {
                "success": True,
                "filename": path.name,
                "path": str(path.absolute()),
                "size": len(content),
                "size_human": self._format_size(len(content)),
                "line_count": len(lines),
                "encoding": "utf-8",
                "content": (
                    content
                    if len(lines) <= max_lines
                    else "".join(lines[:max_lines]) + "\n... [truncated]"
                ),
                "is_truncated": len(lines) > max_lines,
                "lines_shown": min(len(lines), max_lines),
            }

            self.log_operation(
                "read_file", {"filename": filepath, "lines_read": result["lines_shown"]}
            )

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading file: {str(e)}",
                "filename": filepath,
            }

    def delete_file(self, filepath: str) -> Dict:
        """Dosyayı sil"""
        try:
            path = Path(filepath)

            if not path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}

            if not path.is_file():
                return {"success": False, "error": f"Not a file: {filepath}"}

            path.unlink()
            self.stats["files_deleted"] += 1

            self.log_operation("delete_file", {"filename": filepath})

            return {
                "success": True,
                "message": f"File deleted: {filepath}",
                "path": str(path.absolute()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error deleting file: {str(e)}",
                "filename": filepath,
            }

    def move_file(self, source: str, destination: str, overwrite: bool = False) -> Dict:
        """Dosyayı taşı"""
        try:
            src_path = Path(source)
            dst_path = Path(destination)

            if not src_path.exists():
                return {"success": False, "error": f"Source file not found: {source}"}

            if not src_path.is_file():
                return {"success": False, "error": f"Not a file: {source}"}

            if dst_path.exists() and not overwrite:
                return {
                    "success": False,
                    "error": f"Destination already exists: {destination}",
                }

            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))

            self.stats["files_moved"] += 1

            self.log_operation(
                "move_file", {"source": source, "destination": destination}
            )

            return {
                "success": True,
                "message": f"File moved from {source} to {destination}",
                "source": str(src_path.absolute()),
                "destination": str(dst_path.absolute()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error moving file: {str(e)}",
                "source": source,
                "destination": destination,
            }

    def copy_file(self, source: str, destination: str, overwrite: bool = False) -> Dict:
        """Dosyayı kopyala"""
        try:
            src_path = Path(source)
            dst_path = Path(destination)

            if not src_path.exists():
                return {"success": False, "error": f"Source file not found: {source}"}

            if not src_path.is_file():
                return {"success": False, "error": f"Not a file: {source}"}

            if dst_path.exists() and not overwrite:
                return {
                    "success": False,
                    "error": f"Destination already exists: {destination}",
                }

            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src_path), str(dst_path))

            self.log_operation(
                "copy_file", {"source": source, "destination": destination}
            )

            return {
                "success": True,
                "message": f"File copied from {source} to {destination}",
                "source": str(src_path.absolute()),
                "destination": str(dst_path.absolute()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error copying file: {str(e)}",
                "source": source,
                "destination": destination,
            }

    def search_files(
        self,
        pattern: str,
        search_path: str = ".",
        search_content: bool = False,
        case_sensitive: bool = False,
    ) -> Dict:
        """Dosyalarda arama yap"""
        try:
            base_path = Path(search_path).absolute()

            if not base_path.exists():
                return {"error": f"Search path not found: {search_path}"}

            results = []
            pattern_check = pattern if case_sensitive else pattern.lower()
            scanned_count = 0
            max_scan = 500

            for file_path in base_path.rglob("*"):
                if scanned_count >= max_scan:
                    break

                if file_path.is_file():
                    scanned_count += 1
                    filename = file_path.name
                    filename_check = filename if case_sensitive else filename.lower()

                    if pattern_check in filename_check:
                        results.append(self._get_file_info(file_path))
                    elif search_content:
                        try:
                            with open(
                                file_path, "r", encoding="utf-8", errors="ignore"
                            ) as f:
                                content = f.read()
                                content_check = (
                                    content if case_sensitive else content.lower()
                                )
                                if pattern_check in content_check:
                                    results.append(self._get_file_info(file_path))
                        except Exception:
                            continue

                    if len(results) >= 100:
                        break

            return {
                "search": {
                    "pattern": pattern,
                    "path": str(base_path),
                    "search_content": search_content,
                    "case_sensitive": case_sensitive,
                },
                "results": {"found": len(results), "files": results},
                "scanned": scanned_count,
            }

        except Exception as e:
            return {"error": f"Search error: {str(e)}"}

    def get_file_stats(self, filepath: str) -> Dict:
        """Dosya istatistiklerini getir"""
        try:
            path = Path(filepath)

            if not path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}

            stat = path.stat()

            try:
                with open(path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
            except Exception:
                file_hash = "unavailable"

            return {
                "success": True,
                "name": path.name,
                "filename": path.name,
                "path": str(path.absolute()),
                "size": stat.st_size,
                "size_human": self._format_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:],
                "hash_md5": file_hash,
                "is_readonly": not os.access(path, os.W_OK),
            }

        except Exception as e:
            return {"success": False, "error": f"Error getting file stats: {str(e)}"}

    def create_directory(self, dirpath: str) -> Dict:
        """Dizin oluştur"""
        try:
            path = Path(dirpath)
            path.mkdir(parents=True, exist_ok=True)

            self.log_operation("create_directory", {"path": dirpath})

            return {
                "success": True,
                "message": f"Directory created: {dirpath}",
                "path": str(path.absolute()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating directory: {str(e)}",
                "path": dirpath,
            }

    def delete_directory(self, dirpath: str, recursive: bool = False) -> Dict:
        """Dizini sil"""
        try:
            path = Path(dirpath)

            if not path.exists():
                return {"success": False, "error": f"Directory not found: {dirpath}"}

            if not path.is_dir():
                return {"success": False, "error": f"Not a directory: {dirpath}"}

            if recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()

            self.log_operation(
                "delete_directory", {"path": dirpath, "recursive": recursive}
            )

            return {"success": True, "message": f"Directory deleted: {dirpath}"}

        except Exception as e:
            return {
                "success": False,
                "error": f"Error deleting directory: {str(e)}",
                "path": dirpath,
            }

    def _get_file_info(self, filepath: Path) -> Dict:
        """Dosya bilgilerini getir (internal)"""
        try:
            stat = filepath.stat()
            return {
                "name": filepath.name,
                "path": str(filepath),
                "size": stat.st_size,
                "size_human": self._format_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "extension": filepath.suffix.lower(),
                "directory": str(filepath.parent),
            }
        except Exception:
            return {
                "name": filepath.name,
                "path": str(filepath),
                "error": "Unable to get file info",
            }

    def _format_size(self, size_bytes: int) -> str:
        """Byte boyutunu okunabilir formata çevir"""
        if size_bytes == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)

        while size >= 1024 and i < len(units) - 1:
            size /= 1024
            i += 1

        return f"{size:.2f} {units[i]}"

    def get_operation_history(self, limit: int = 20) -> List[Dict]:
        """İşlem geçmişini getir"""
        return self.history[-limit:] if self.history else []

    def get_system_stats(self) -> Dict:
        """Sistem istatistiklerini getir"""
        return {
            "file_manager": self.stats,
            "history_count": len(self.history),
            "current_directory": self.get_current_directory(),
        }


# Global instance
file_manager = FileManager()
