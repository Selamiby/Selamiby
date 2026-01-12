"""
Seviye 2: AI-POWERED OTONOM SİSTEM
Akıllı İçerik Analizi - Dosya içeriklerini okuyup kategorize etme
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class SmartContentAnalyzer:
    """Akıllı içerik analiz sistemi"""

    # Dosya türlerine göre analiz stratejileri
    CONTENT_PATTERNS = {
        "code": {
            "patterns": [
                "def ",
                "class ",
                "function ",
                "import ",
                "require(",
                "return ",
            ],
            "extensions": [".py", ".js", ".java", ".cpp", ".c", ".ts"],
        },
        "document": {
            "patterns": ["Introduction", "Summary", "Chapter", "Section", "References"],
            "extensions": [".txt", ".md", ".doc", ".docx", ".pdf"],
        },
        "data": {
            "patterns": ["{", "}", "[", "]", '"', "column", "row"],
            "extensions": [".json", ".csv", ".xml", ".parquet", ".sql"],
        },
        "config": {
            "patterns": ["[", "key", "value", "config", "setting"],
            "extensions": [".yaml", ".yml", ".json", ".ini", ".conf"],
        },
    }

    def __init__(self):
        self.analyzed_files = {}
        self.category_stats = {}

    def analyze_file_content(self, file_path: str) -> Dict:
        """Dosya içeriğini analiz et"""
        path = Path(file_path)

        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        if not path.is_file():
            return {"error": f"Not a file: {file_path}"}

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(10000)  # İlk 10KB'ı oku
        except Exception as e:
            return {"error": f"Cannot read file: {str(e)}"}

        # İçerik analizi
        analysis = {
            "file": str(path),
            "size": path.stat().st_size,
            "lines": len(content.split("\n")),
            "words": len(content.split()),
            "content_type": self._detect_content_type(content, path.suffix),
            "language": self._detect_language(content),
            "key_info": self._extract_key_info(content, path.suffix),
            "sentiment": self._analyze_sentiment(content),
            "importance": self._calculate_importance(content, path.suffix),
            "metadata": {
                "created": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            },
        }

        # Kaydet
        self.analyzed_files[str(path)] = analysis

        return analysis

    def categorize_content(self, content: str, file_type: str = "unknown") -> Dict:
        """İçeriği otomatik kategorize et"""
        categories = {}

        for category, patterns in self.CONTENT_PATTERNS.items():
            match_count = 0
            for pattern in patterns["patterns"]:
                match_count += content.lower().count(pattern.lower())

            if match_count > 0:
                categories[category] = {
                    "matches": match_count,
                    "confidence": min(match_count / 10, 1.0),  # 0-1 arası
                }

        # En yüksek confidence'ı bulunulan
        if categories:
            best_match = max(categories.items(), key=lambda x: x[1]["confidence"])
            return {
                "primary_category": best_match[0],
                "confidence": best_match[1]["confidence"],
                "all_categories": categories,
            }

        return {"primary_category": "unknown", "confidence": 0.0}

    def extract_important_data(self, file_path: str) -> Dict:
        """Dosyadan önemli bilgileri çıkar"""
        path = Path(file_path)

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return {"error": "Cannot read file"}

        extracted = {
            "emails": self._extract_emails(content),
            "urls": self._extract_urls(content),
            "phone_numbers": self._extract_phone_numbers(content),
            "dates": self._extract_dates(content),
            "numbers": self._extract_numbers(content),
            "important_keywords": self._extract_keywords(content),
        }

        # Boş olanları kaldır
        return {k: v for k, v in extracted.items() if v}

    def batch_analyze_directory(self, directory: str = ".") -> Dict:
        """Dizindeki tüm dosyaları analiz et"""
        results = {
            "total_files": 0,
            "analyzed": 0,
            "errors": 0,
            "categories": {},
            "files": [],
        }

        try:
            for file_path in Path(directory).rglob("*"):
                if file_path.is_file() and not file_path.name.startswith("."):
                    results["total_files"] += 1

                    analysis = self.analyze_file_content(str(file_path))

                    if "error" not in analysis:
                        results["analyzed"] += 1

                        content_type = analysis.get("content_type", "unknown")
                        if content_type not in results["categories"]:
                            results["categories"][content_type] = 0
                        results["categories"][content_type] += 1

                        results["files"].append(
                            {
                                "name": file_path.name,
                                "type": analysis["content_type"],
                                "size": analysis["size"],
                                "importance": analysis.get("importance", 0),
                            }
                        )
                    else:
                        results["errors"] += 1
        except Exception as e:
            results["error"] = str(e)

        # Önem sırasına göre sırala
        results["files"].sort(key=lambda x: x["importance"], reverse=True)

        return results

    def _detect_content_type(self, content: str, extension: str) -> str:
        """İçerik türünü tespit et"""
        for category, patterns in self.CONTENT_PATTERNS.items():
            if extension in patterns["extensions"]:
                return category

        # Pattern eşleştirme
        categorization = self.categorize_content(content)
        return categorization.get("primary_category", "unknown")

    def _detect_language(self, content: str) -> str:
        """Yazı dilini tespit et"""
        # Basit heuristic
        turkish_words = ["ve", "de", "da", "bir", "ile", "için"]
        english_words = ["the", "and", "or", "is", "are", "for"]

        turkish_count = sum(1 for word in turkish_words if word in content.lower())
        english_count = sum(1 for word in english_words if word in content.lower())

        if turkish_count > english_count:
            return "Turkish"
        elif english_count > turkish_count:
            return "English"
        else:
            return "Unknown"

    def _extract_key_info(self, content: str, extension: str) -> List[str]:
        """Temel bilgileri çıkar"""
        lines = content.split("\n")
        key_info = []

        for line in lines[:10]:  # İlk 10 satır
            line = line.strip()
            if len(line) > 20 and not line.startswith("#"):
                key_info.append(line[:100])

        return key_info

    def _analyze_sentiment(self, content: str) -> str:
        """İçerik duygusunu analiz et"""
        positive_words = ["good", "great", "excellent", "perfect", "harika", "güzel"]
        negative_words = ["bad", "terrible", "awful", "poor", "kötü", "berbat"]

        pos_count = sum(1 for word in positive_words if word in content.lower())
        neg_count = sum(1 for word in negative_words if word in content.lower())

        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"

    def _calculate_importance(self, content: str, extension: str) -> float:
        """Dosya önemini hesapla (0-1)"""
        score = 0.0

        # Boyut önemli ise daha önemli
        score += min(len(content) / 100000, 0.3)

        # Yapılandırılmış veri (code, data)
        if extension in [".py", ".js", ".json", ".csv"]:
            score += 0.4

        # Config dosyaları önemli
        if extension in [".yaml", ".ini", ".conf"]:
            score += 0.2

        return min(score, 1.0)

    def _extract_emails(self, content: str) -> List[str]:
        """Email adreslerini çıkar"""
        import re

        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return list(set(re.findall(pattern, content)))

    def _extract_urls(self, content: str) -> List[str]:
        """URL'leri çıkar"""
        import re

        pattern = r"https?://[^\s]+"
        return list(set(re.findall(pattern, content)))

    def _extract_phone_numbers(self, content: str) -> List[str]:
        """Telefon numaralarını çıkar"""
        import re

        pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        return list(set(re.findall(pattern, content)))

    def _extract_dates(self, content: str) -> List[str]:
        """Tarihleri çıkar"""
        import re

        pattern = r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}"
        return list(set(re.findall(pattern, content)))

    def _extract_numbers(self, content: str) -> List[str]:
        """Önemli sayıları çıkar"""
        import re

        # Büyük sayıları bul
        pattern = r"\d{3,}"
        matches = re.findall(pattern, content)
        return list(set(matches))[:10]  # İlk 10

    def _extract_keywords(self, content: str) -> List[str]:
        """Anahtar kelimeleri çıkar"""
        # Basit yöntem: sık tekrarlanan kelimeler
        words = content.lower().split()
        # 4+ karakter, sık tekrarlanan
        from collections import Counter

        word_counts = Counter(words)

        keywords = [
            word for word, count in word_counts.most_common(10) if len(word) > 4
        ]
        return keywords


# Global instance
smart_analyzer = SmartContentAnalyzer()
