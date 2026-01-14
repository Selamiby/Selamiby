"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import ast
import logging
import os
from pathlib import Path

from nexus_brain import NexusBrain

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] 🛠️ AUTO-HEALER: %(message)s")
logger = logging.getLogger("AutoHealer")

class NexusAutoHealer:
    """
    NEXUS-ONE Self-Healing Katmanı.
    Dosyaları tarar, hataları bulur ve DeepSeek/Claude ile düzeltir.
    """
    def __init__(self):
        self.workspace = Path("c:/Users/selam/NEXUS-ONE")
        self.brain = NexusBrain()

    def scan_and_fix(self):
        """Tüm workspace'i tarar ve hatalı dosyaları onarır."""
        logger.info("🔍 Proje dosyaları taranıyor...")
        files = list(self.workspace.glob("*.py"))
        
        fixed_count = 0
        for file_path in files:
            if self._check_syntax_error(file_path):
                logger.warning(f"❌ Hata tespit edildi: {file_path.name}")
                if self._apply_fix(file_path):
                    fixed_count += 1
        
        return f"Scan tamamlandı. {len(files)} dosya incelendi, {fixed_count} dosya onarıldı."

    def _check_syntax_error(self, file_path):
        try:
            content = self._read_safe(file_path)
            if content is None: return False
            ast.parse(content)
            return False # Hata yok
        except SyntaxError:
            return True # Hata var
        except Exception:
            return False

    def _read_safe(self, file_path):
        """Encoding hatalarına karşı güvenli okuma."""
        for enc in ["utf-8", "cp1254", "latin-1"]:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        return None

    def _apply_fix(self, file_path):
        logger.info(f"🩹 {file_path.name} üzerinde onarım başlatılıyor...")
        
        broken_code = self._read_safe(file_path)
        if not broken_code: return False

        prompt = (
            f"Aşağıdaki Python dosyasında bir SYNTAX ERROR (Yazım Hatası) var.\n"
            f"Dosya Adı: {file_path.name}\n"
            f"Hatalı Kod:\n{broken_code}\n\n"
            f"Lütfen sadece düzeltilmiş halini, hiçbir açıklama yapmadan döndür."
        )

        fixed_code = self.brain.think(prompt, "Sen uzman bir kod onarıcısın.")
        
        if fixed_code and "import" in fixed_code:
            # Markdown temizliği gerekebilir
            if "```python" in fixed_code:
                fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
            elif "```" in fixed_code:
                fixed_code = fixed_code.split("```")[1].split("```")[0].strip()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)
            logger.info(f"✅ {file_path.name} başarıyla onarıldı.")
            return True
        return False

if __name__ == "__main__":
    healer = NexusAutoHealer()
    print(healer.scan_and_fix())
