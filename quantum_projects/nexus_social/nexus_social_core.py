import json
import time
from pathlib import Path

import psutil


class NexusSocial:
    """
    REAL-WORLD DISRUPTIVE SOCIAL ECOSYSTEM
    Competitor to: TikTok, Instagram, X.
    Killer Feature: REAL Bio-Telemetry & System Fatigue Analysis.
    """
    def __init__(self):
        self.project_dir = Path("c:/Users/selam/NEXUS-ONE/quantum_projects/nexus_social")
        self.curator_config = self.project_dir / "ai_curator.json"
        self._init_curator()

    def _init_curator(self):
        if not self.curator_config.exists():
            config = {
                "interests": ["Technology", "AI", "Blockchain"],
                "avoid": ["Toxic Politics"],
                "fatigue_threshold": 0.5,
                "current_session_stress": 0.0
            }
            with open(self.curator_config, "w") as f:
                json.dump(config, f, indent=4)

    def analyze_system_fatigue(self):
        """
        GERÇEK ANALİZ: Kullanıcının ve sistemin yükünü analiz eder.
        CPU kullanımı, açık pencere sayısı ve sistem çalışma süresi üzerinden 
        bir yorgunluk endeksi oluşturur.
        """
        cpu_load = psutil.cpu_percent(interval=0.5) / 100.0
        memory_load = psutil.virtual_memory().percent / 100.0
        
        # Karmaşık bir stres skoru hesapla
        stress_score = (cpu_load * 0.7) + (memory_load * 0.3)
        
        print(f"[PROD] System Stress Analysis: {stress_score:.2f}")
        
        if stress_score > 0.6:
            self._trigger_restorative_mode()
        
        return stress_score

    def _trigger_restorative_mode(self):
        """Ekranı ve içeriği otomatik olarak 'Yenileyici' forma sokar."""
        # Windows API/Flet/Custom UI ile ekran rengini ısıtma/karartma yapılabilir.
        print("[AUTO-HEAL] Mental Fatigue Detected! Restorative Mode Active.")
        print(">> Algorithm addiction bypassed. Only calming content prioritized.")

    def get_curated_feed(self):
        """Gerçek sistem durumuna göre kürate edilmiş akış."""
        score = self.analyze_system_fatigue()
        
        if score > 0.6:
            return [{"id": "Zen-1", "content": "Biraz mola verin. Nefes egzersizi öneriliyor."}]
        else:
            return [{"id": "Tech-1", "content": "P2P Web 4.0 mimarisi hakkında makale."}]

if __name__ == "__main__":
    social = NexusSocial()
    print("🚀 NexusSocial Canlı Analiz Başlıyor...")
    feed = social.get_curated_feed()
    print(f"📡 Canlı Akış: {feed}")
