"""
Veri işleme optimizasyonları - CPU verimli
"""

from typing import List, Dict, Any, Iterator
import json
import csv
from pathlib import Path
import gc


class StreamProcessor:
    """Bellek verimli stream işleme"""
    
    @staticmethod
    def read_large_json(filepath: Path, chunk_size: int = 1000) -> Iterator[Dict]:
        """Büyük JSON dosyasını stream et"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if filepath.suffix == '.jsonl':  # JSON Lines format
                    for line in f:
                        if line.strip():
                            yield json.loads(line)
                else:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            yield item
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    @staticmethod
    def read_csv_stream(filepath: Path, chunk_size: int = 1000) -> Iterator[Dict]:
        """CSV dosyasını stream et"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield row
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    @staticmethod
    def write_jsonl(filepath: Path, data: Iterator[Dict]):
        """JSONL formatında yaz (bellek verimli)"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"❌ Hata: {e}")


class DataAggregator:
    """Veri toplama - CPU dostu"""
    
    @staticmethod
    def aggregate_dicts(data: List[Dict], key: str, agg_func=sum) -> Dict:
        """Sözlükleri anahtara göre topla"""
        result = {}
        for item in data:
            if key in item:
                k = item[key]
                result[k] = agg_func([d[key] for d in data if d.get(key) == k])
        return result
    
    @staticmethod
    def group_by(data: List[Dict], key: str) -> Dict[str, List[Dict]]:
        """Verileri grupla"""
        result = {}
        for item in data:
            k = item.get(key, 'unknown')
            if k not in result:
                result[k] = []
            result[k].append(item)
        return result
    
    @staticmethod
    def filter_and_map(data: Iterator[Dict], filter_func, map_func) -> Iterator[Dict]:
        """Filter ve map - pipeline işlemi"""
        for item in data:
            if filter_func(item):
                yield map_func(item)


class BatchProcessor:
    """Batch işleme - RAM dostu"""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    def process(self, data: Iterator[Any], processor_func) -> Iterator[Any]:
        """Batch'ler halinde işle"""
        batch = []
        for item in data:
            batch.append(item)
            if len(batch) >= self.batch_size:
                result = processor_func(batch)
                yield from result if isinstance(result, list) else [result]
                batch = []
                gc.collect()  # Bellek temizle
        
        if batch:
            result = processor_func(batch)
            yield from result if isinstance(result, list) else [result]


class TextProcessor:
    """Metin işleme optimizasyonları"""
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """Metni parçalara böl"""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks
    
    @staticmethod
    def deduplicate(items: List[str]) -> List[str]:
        """Duplikaları kaldır (sıra koruyarak)"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def normalize(text: str) -> str:
        """Metni normalize et"""
        return text.strip().lower().replace('\n', ' ')


def memory_efficient_sort(data: Iterator[Any], key=None, chunk_size: int = 10000):
    """Bellek verimli sıralama"""
    chunks = []
    chunk = []
    
    for item in data:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            chunk.sort(key=key)
            chunks.append(chunk)
            chunk = []
    
    if chunk:
        chunk.sort(key=key)
        chunks.append(chunk)
    
    # Merge sort
    import heapq
    return heapq.merge(*chunks, key=key)
