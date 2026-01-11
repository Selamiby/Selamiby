"""
Örnek Araçlar - CPU Optimized Tools
"""

from typing import List, Dict, Any
from pathlib import Path
import json
from core.data_processor import StreamProcessor, BatchProcessor, TextProcessor
from core.performance import cpu_monitor


class FileTools:
    """Dosya işleme araçları"""
    
    @staticmethod
    def read_large_json_safely(filepath: str, max_memory_mb: int = 100) -> List[Dict]:
        """Büyük JSON dosyasını güvenli oku"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {filepath}")
        
        items = []
        current_memory = 0
        
        for item in StreamProcessor.read_large_json(path):
            items.append(item)
            
            # Bellek kontrolü
            stats = cpu_monitor.get_stats()
            if stats.get('memory_mb', 0) > max_memory_mb:
                print(f"⚠️ Bellek limiti yaklaştı: {stats['memory_mb']:.2f} MB")
                break
        
        return items
    
    @staticmethod
    def export_to_jsonl(data: List[Dict], filepath: str):
        """Veriyi JSONL formatında kaydet"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"✅ {len(data)} item kaydedildi: {filepath}")
    
    @staticmethod
    def get_file_stats(filepath: str) -> Dict:
        """Dosya istatistikleri"""
        path = Path(filepath)
        return {
            'name': path.name,
            'size_mb': path.stat().st_size / (1024*1024),
            'exists': path.exists(),
            'is_file': path.is_file(),
            'is_dir': path.is_dir()
        }


class TextTools:
    """Metin işleme araçları"""
    
    @staticmethod
    def process_large_text(text: str, operation: str = 'chunk') -> List[str]:
        """Büyük metni işle"""
        
        if operation == 'chunk':
            return TextProcessor.chunk_text(text, chunk_size=512)
        
        elif operation == 'deduplicate':
            lines = text.split('\n')
            unique_lines = TextProcessor.deduplicate(lines)
            return unique_lines
        
        elif operation == 'normalize':
            return [TextProcessor.normalize(line) for line in text.split('\n')]
        
        return []
    
    @staticmethod
    def analyze_text_stats(text: str) -> Dict:
        """Metin istatistikleri"""
        lines = text.split('\n')
        words = text.split()
        
        return {
            'total_length': len(text),
            'line_count': len(lines),
            'word_count': len(words),
            'average_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'unique_words': len(set(words)),
            'complexity': 'high' if len(set(words)) / len(words) > 0.5 else 'low'
        }


class PerformanceTools:
    """Performans araçları"""
    
    @staticmethod
    def check_system_health() -> Dict:
        """Sistem sağlığını kontrol et"""
        stats = cpu_monitor.get_stats()
        
        health = {
            'cpu_usage': stats.get('cpu_percent', 0),
            'memory_usage_mb': stats.get('memory_mb', 0),
            'thread_count': stats.get('num_threads', 0),
            'system_cpu': stats.get('system_cpu', 0),
            'status': 'healthy' if stats.get('cpu_percent', 0) < 60 else 'warning',
            'recommendations': []
        }
        
        # Tavsiyeler
        if stats.get('cpu_percent', 0) > 60:
            health['recommendations'].append('CPU kullanımı yüksek, işlemleri yavaşlat')
        
        if stats.get('memory_mb', 0) > 300:
            health['recommendations'].append('Bellek kullanımı yüksek, GC çalıştır')
        
        if stats.get('num_threads', 0) > 100:
            health['recommendations'].append('Thread sayısı fazla, az thread kullan')
        
        return health
    
    @staticmethod
    def get_performance_report() -> str:
        """Performans raporu (metin)"""
        cpu_monitor.print_report()
        
        report = "Performans analizi tamamlandı.\n"
        report += f"Ort. CPU: {cpu_monitor.get_average_cpu():.2f}%\n"
        report += f"En yüksek CPU: {cpu_monitor.get_peak_cpu():.2f}%\n"
        
        return report
    
    @staticmethod
    def optimize_gc():
        """Garbage collection optimizasyonu"""
        import gc
        
        # GC istatistikleri
        stats = gc.get_stats()
        
        # Belleği temizle
        collected = gc.collect()
        
        return {
            'objects_collected': collected,
            'total_objects': len(gc.get_objects()),
            'optimization_applied': True
        }


class DataValidationTools:
    """Veri doğrulama araçları"""
    
    @staticmethod
    def validate_json(data: str) -> tuple[bool, str]:
        """JSON geçerliğini kontrol et"""
        try:
            json.loads(data)
            return True, "Geçerli JSON"
        except json.JSONDecodeError as e:
            return False, f"JSON hatası: {e}"
    
    @staticmethod
    def validate_dict_structure(data: Dict, required_keys: List[str]) -> tuple[bool, List[str]]:
        """Dict yapısını doğrula"""
        missing_keys = [k for k in required_keys if k not in data]
        
        if missing_keys:
            return False, missing_keys
        
        return True, []
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Metni temizle"""
        # Boşlukları kaldır
        text = text.strip()
        
        # Çoklu satırları tek satıra çevir
        text = ' '.join(text.split())
        
        # Özel karakterleri kaldır (opsiyonel)
        # text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        return text
