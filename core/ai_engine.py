"""
NEXUS-ONE AI Engine - Otonom AI Sistemi
"""

import random
from datetime import datetime
from typing import Any, Dict, List


class AIEngine:
    """AI İşlemler Motoru"""
    
    def __init__(self):
        self.name = "NEXUS-ONE AI"
        self.version = "2.0"
        self.conversation_history = []
        self.knowledge_base = self._init_knowledge()
        
    def _init_knowledge(self) -> Dict:
        """Bilgi tabanını başlat"""
        return {
            "responses": {
                "merhaba": "Merhaba! NEXUS-ONE AI Engine ile sohbet ediyorsunuz. Nasıl yardımcı olabilirim?",
                "nasılsın": "İyiyim, teşekkür ederim! Sistem normal çalışıyor. Siz nasılsınız?",
                "aether": "NEXUS-ONE, otonom bir AI işletim sistemidir. Python ile yazılmış, verimli ve hızlıdır.",
                "python": "Python, NEXUS-ONE'un temelini oluşturan programlama dilidir. Güçlü ve esnek bir dildir.",
                "yardım": "Yardım için şunları yapabilirsiniz:\n1. AI ile sohbet edin\n2. Metinleri analiz edin\n3. Görev planları oluşturun\n4. Metinleri özetleyin",
            },
            "keywords": {
                "merhaba": ["merhaba", "selam", "hey", "çalış mı"],
                "nasılsın": ["nasılsın", "iyimisin", "durumun", "refahın"],
                "aether": ["aether", "sistem", "os", "işletim"],
                "python": ["python", "kod", "program", "dil"],
                "yardım": ["yardım", "ne yapabilirim", "neler yapar", "komut"],
            }
        }
    
    def generate_response(self, prompt: str) -> str:
        """Prompt'a yanıt üret"""
        prompt_lower = prompt.lower()
        
        # Bilgi tabanında arama
        for key, keywords in self.knowledge_base["keywords"].items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    response = self.knowledge_base["responses"].get(key, "Anlayamadım.")
                    self._save_to_history(prompt, response)
                    return response
        
        # Varsayılan yanıtlar
        default_responses = [
            "İlginç bir soru! Bu konu hakkında daha fazla bilgi verebilir misiniz?",
            "Anladığım kadarıyla siz şundan bahsediyorsunuz: " + prompt[:30] + "...",
            "Bu çok iyi bir gözlem! NEXUS-ONE sisteminde bu konuda çalışmalar devam ediyor.",
            "Haklısınız! Bununla ilgili olarak yapabileceğimiz birçok şey var.",
            "Merak ettim, daha da açıklaması var mı?",
        ]
        
        response = random.choice(default_responses)
        self._save_to_history(prompt, response)
        return response
    
    def analyze_text(self, text: str) -> Dict:
        """Metni analiz et"""
        words = text.split()
        sentences = text.split('.')
        
        sentiment = self._analyze_sentiment(text)
        
        result = {
            "analysis": {
                "text_length": len(text),
                "words": len(words),
                "sentences": len([s for s in sentences if s.strip()]),
                "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
                "sentiment": sentiment,
                "complexity": "high" if len(words) > 20 else "medium" if len(words) > 10 else "low"
            }
        }
        
        return result
    
    def _analyze_sentiment(self, text: str) -> str:
        """Duygu analizi yap"""
        positive_words = ["harika", "iyi", "güzel", "müthiş", "başarılı", "mükemmel", "süper"]
        negative_words = ["kötü", "hata", "sorun", "problem", "başarısız", "olumsuz"]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def create_task_plan(self, task: str) -> Dict:
        """Görev planı oluştur"""
        steps = [
            "Görevi analiz et",
            "Kaynakları belirle",
            "Adımları planla",
            "İşleme başla",
            "Sonuçları kontrol et"
        ]
        
        return {
            "task": task,
            "status": "planned",
            "steps": steps,
            "estimated_time": "30 dakika",
            "priority": "normal",
            "created_at": datetime.now().isoformat()
        }
    
    def summarize_text(self, text: str) -> Dict:
        """Metni özetle"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Basit özet: ilk ve son cümleleri al
        if len(sentences) <= 2:
            summary = text
        else:
            summary = sentences[0] + ". " + sentences[-1] + "."
        
        return {
            "original_length": len(text),
            "summary_length": len(summary),
            "compression_ratio": round((1 - len(summary) / len(text)) * 100, 1) if text else 0,
            "summary": summary,
            "sentences_original": len(sentences),
            "sentences_summary": 2
        }
    
    def _save_to_history(self, prompt: str, response: str):
        """Sohbeti geçmişe kaydet"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        }
        self.conversation_history.append(entry)
        
        # Geçmişi sınırla (son 100 konuşma)
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
    
    def get_conversation_history(self) -> List[Dict]:
        """Sohbet geçmişini getir"""
        return self.conversation_history[-20:] if self.conversation_history else []
    
    def get_system_info(self) -> Dict:
        """Sistem bilgilerini getir"""
        return {
            "engine_name": self.name,
            "version": self.version,
            "conversation_count": len(self.conversation_history),
            "knowledge_base_size": len(self.knowledge_base["responses"]),
            "status": "online"
        }
