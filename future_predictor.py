# future_predictor.py
import random


class FuturePredictor:
    def predict_tech_trends(self):
        return {
            "1_hafta": ["Python 3.12 performans iyileştirmeleri", "AI kod asistanlarında artış"],
            "1_ay": ["Yeni JavaScript framework'ü çıkacak", "Rust popülerleşecek"],
            "1_yıl": ["AI tarafından yazılan kod %30'a ulaşacak", "Yeni programlama paradigmaları"]
        }
    
    def predict_next_language(self):
        candidates = ["Mojo", "Zig", "V", "Jai", "Carbon"]
        return {
            "next_big_language": random.choice(candidates),
            "confidence": f"%{random.randint(70, 95)}",
            "reason": "Performans ve güvenlik odaklı"
        }
