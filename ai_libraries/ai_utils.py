"""
AI Utilities from LangChain
"""
import json
from typing import Any, Dict, List, Optional


class AITools:
    """AI araçları koleksiyonu"""
    
    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        """Metinden varlıkları çıkar (basit versiyon)"""
        entities = {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": [],
            "urls": []
        }
        
        # Basit keyword matching (gerçekte NER modeli kullanılmalı)
        people_keywords = ["Mr.", "Ms.", "Dr.", "said", "told", "according to"]
        org_keywords = ["Inc.", "Corp.", "Ltd.", "Company", "Organization"]
        
        words = text.split()
        for i, word in enumerate(words):
            if word in people_keywords and i + 1 < len(words):
                entities["people"].append(words[i + 1])
            elif word in org_keywords and i - 1 >= 0:
                entities["organizations"].append(words[i - 1])
            elif "http" in word or "www." in word:
                entities["urls"].append(word)
                
        return entities
    
    @staticmethod
    def summarize_text(text: str, max_sentences: int = 3) -> str:
        """Metni özetle (basit algoritma)"""
        sentences = text.split('. ')
        if len(sentences) <= max_sentences:
            return text
        
        # En uzun cümleleri seç (basit özetleme)
        sorted_sentences = sorted(sentences, key=len, reverse=True)
        summary = '. '.join(sorted_sentences[:max_sentences]) + '.'
        return summary
    
    @staticmethod
    def classify_text(text: str, categories: List[str]) -> Dict[str, float]:
        """Metni kategorilere göre sınıflandır"""
        text_lower = text.lower()
        scores = {}
        
        for category in categories:
            category_lower = category.lower()
            # Basit keyword matching
            if category_lower in text_lower:
                score = 0.8
            else:
                # Category kelimeleri metinde var mı?
                category_words = category_lower.split()
                matches = sum(1 for word in category_words if word in text_lower)
                score = matches / len(category_words) * 0.6
            scores[category] = min(score, 1.0)
            
        return scores
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """Metinden anahtar kelimeleri çıkar"""
        # Stop words (gerçekte daha kapsamlı liste kullan)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        words = text.lower().split()
        # Noktalama işaretlerini temizle
        words = [word.strip('.,!?;:"()[]{}') for word in words]
        
        # Stop words'leri filtrele ve frekans say
        word_freq = {}
        for word in words:
            if word and word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # En sık kullanılanları sırala
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
