"""
Örnek Modüller - CPU Dostu Uygulamalar
"""

from typing import List, Dict, Any, Callable
from core.async_utils import AsyncBatchProcessor, RateLimiter
from core.performance import cache, cpu_monitor
from core.data_processor import StreamProcessor, TextProcessor, BatchProcessor
import asyncio


class DataProcessor:
    """Veri işleme modülü"""
    
    def __init__(self):
        self.processor = AsyncBatchProcessor(batch_size=20, delay=0.01)
        self.cache = cache
    
    async def process_items(self, items: List[Dict]) -> List[Dict]:
        """Async olarak items'ları işle"""
        cache_key = f"items_{len(items)}"
        
        # Cache kontrol et
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Async işleme
        async def process(item):
            return {**item, 'processed': True, 'timestamp': str(asyncio.get_event_loop().time())}
        
        results = await self.processor.process(items, process)
        
        # Sonucu cache'le
        self.cache.set(cache_key, results)
        
        return results


class APIClient:
    """API istemci - Rate limiting ile"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(max_calls=10, time_window=1.0)
        self.session = None
    
    async def fetch(self, url: str, **kwargs) -> Dict:
        """Rate-limited fetch"""
        await self.rate_limiter.wait()
        
        # Cache kontrol
        cache_key = f"api_{url}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Simülasyon (gerçek kodda HTTP isteği yapılır)
        result = {'url': url, 'status': 'ok', 'data': {}}
        
        # Cache'le
        cache.set(cache_key, result)
        
        return result


class TextAnalyzer:
    """Metin analiz modülü"""
    
    @staticmethod
    def analyze_text(text: str) -> Dict:
        """Metni analiz et"""
        # Cache kontrol
        cache_key = f"analysis_{hash(text)}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Analiz
        chunks = TextProcessor.chunk_text(text, chunk_size=256)
        normalized = TextProcessor.normalize(text)
        
        result = {
            'original_length': len(text),
            'normalized_length': len(normalized),
            'chunk_count': len(chunks),
            'word_count': len(normalized.split()),
            'chunks': chunks[:3]  # İlk 3 chunk
        }
        
        # Cache'le
        cache.set(cache_key, result)
        
        return result


class ReportGenerator:
    """Rapor oluşturucu"""
    
    @staticmethod
    def generate_performance_report() -> Dict:
        """Performans raporu oluştur"""
        stats = cpu_monitor.get_stats()
        
        report = {
            'title': 'Performans Raporu',
            'timestamp': stats.get('timestamp'),
            'cpu_percent': stats.get('cpu_percent', 0),
            'memory_mb': stats.get('memory_mb', 0),
            'average_cpu': cpu_monitor.get_average_cpu(),
            'peak_cpu': cpu_monitor.get_peak_cpu(),
            'status': 'optimal' if stats.get('cpu_percent', 0) < 50 else 'high'
        }
        
        return report
    
    @staticmethod
    def generate_system_report() -> Dict:
        """Sistem raporu"""
        import os
        import sys
        import platform
        
        return {
            'python_version': sys.version.split()[0],
            'platform': platform.platform(),
            'cpu_count': os.cpu_count(),
            'current_directory': os.getcwd(),
            'cache_size': len(cache.cache),
        }
