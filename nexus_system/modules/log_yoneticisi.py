import json
import os
from datetime import datetime


class LogYoneticisi:
    def __init__(self):
        self.log_dir = "nexus_system/logs"
        self.log_dosyasi = os.path.join(self.log_dir, "system.log")
        # Log klasörünün varlığını kontrol et, yoksa oluştur
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def calis(self, mesaj=""):
        """Log dosyasına yeni bir kayıt ekler."""
        kayit = {
            "zaman": datetime.now().isoformat(),
            "mesaj": mesaj if mesaj else "Sistem periyodik kontrol.",
            "tip": "bilgi"
        }
        
        try:
            with open(self.log_dosyasi, "a", encoding="utf-8") as f:
                f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
            
            return f"📝 Log kaydedildi: {mesaj}"
        except Exception as e:
            return f"❌ Log kaydedilemedi: {e}"
    
    def temizle(self):
        """Log dosyasının içeriğini temizler."""
        try:
            open(self.log_dosyasi, "w").close()
            self.calis("Log dosyası temizlendi.")
            return "🗑️ Loglar temizlendi"
        except Exception as e:
            return f"❌ Log temizlenemedi: {e}"
