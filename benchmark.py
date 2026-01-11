#!/usr/bin/env python3
"""
AetherOS Performans Benchmark
CPU, Bellek ve İşlem Hızı Testi
"""

import time
import asyncio
import sys
from pathlib import Path

# Core imports
sys.path.insert(0, str(Path(__file__).parent))

from core.performance import cpu_monitor, cache
from core.async_utils import AsyncBatchProcessor
from core.data_processor import TextProcessor, BatchProcessor


async def benchmark_async_batch():
    """Async batch processing benchmark"""
    print("\n" + "="*60)
    print("🔥 ASYNC BATCH PROCESSING BENCHMARK")
    print("="*60)
    
    processor = AsyncBatchProcessor(batch_size=50, delay=0.01)
    items = list(range(1000))
    
    async def process(item):
        return item * 2
    
    start = time.time()
    results = await processor.process(items, process)
    elapsed = time.time() - start
    
    stats = cpu_monitor.get_stats()
    
    print(f"\n📊 Sonuçlar:")
    print(f"  İşlem Sayısı: {len(results)}")
    print(f"  Süre: {elapsed:.4f} saniye")
    print(f"  İşlem/Saniye: {len(results)/elapsed:.0f}")
    print(f"  CPU Kullanımı: {stats['cpu_percent']:.2f}%")
    print(f"  Bellek: {stats['memory_mb']:.2f} MB")


def benchmark_cache():
    """Cache performance benchmark"""
    print("\n" + "="*60)
    print("💾 CACHE PERFORMANCE BENCHMARK")
    print("="*60)
    
    # Write benchmark
    print("\n📝 Write Benchmark (10,000 items):")
    start = time.time()
    for i in range(10000):
        cache.set(f'key_{i}', {'id': i, 'data': f'value_{i}'})
    write_time = time.time() - start
    
    print(f"  Süre: {write_time:.4f} saniye")
    print(f"  İşlem/Saniye: {10000/write_time:.0f}")
    
    # Read benchmark
    print("\n📖 Read Benchmark (10,000 items):")
    start = time.time()
    for i in range(10000):
        _ = cache.get(f'key_{i}')
    read_time = time.time() - start
    
    print(f"  Süre: {read_time:.4f} saniye")
    print(f"  İşlem/Saniye: {10000/read_time:.0f}")
    
    stats = cpu_monitor.get_stats()
    print(f"\n💻 Sistem:")
    print(f"  CPU: {stats['cpu_percent']:.2f}%")
    print(f"  Bellek: {stats['memory_mb']:.2f} MB")
    print(f"  Cache Size: {len(cache.cache)} items")


def benchmark_text_processing():
    """Text processing benchmark"""
    print("\n" + "="*60)
    print("📝 TEXT PROCESSING BENCHMARK")
    print("="*60)
    
    text = """
    AetherOS, CPU dostu bir otonom yapay zeka sistemidir.
    Hızlı işlem ve düşük bellek kullanımı ile tasarlanmıştır.
    Async işlemler ve batch processing desteği bulunmaktadır.
    """ * 1000  # 1000x tekrar
    
    # Chunking benchmark
    print("\n📂 Chunking Benchmark (1000x 3 paragraf):")
    start = time.time()
    chunks = TextProcessor.chunk_text(text, chunk_size=512)
    chunk_time = time.time() - start
    
    print(f"  Chunk Sayısı: {len(chunks)}")
    print(f"  Süre: {chunk_time:.4f} saniye")
    print(f"  Chunk/Saniye: {len(chunks)/chunk_time:.0f}")
    
    # Normalization benchmark
    print("\n🔤 Normalization Benchmark:")
    start = time.time()
    normalized = TextProcessor.normalize(text)
    norm_time = time.time() - start
    
    print(f"  Original Length: {len(text)}")
    print(f"  Normalized Length: {len(normalized)}")
    print(f"  Süre: {norm_time:.4f} saniye")


def benchmark_batch_processing():
    """Batch processing benchmark"""
    print("\n" + "="*60)
    print("📦 BATCH PROCESSING BENCHMARK")
    print("="*60)
    
    processor = BatchProcessor(batch_size=100)
    items = (i for i in range(10000))
    
    def batch_process(batch):
        return [x * 2 for x in batch]
    
    print(f"\n🔄 Processing 10,000 items in batches of 100:")
    start = time.time()
    results = list(processor.process(items, batch_process))
    elapsed = time.time() - start
    
    print(f"  Sonuç Sayısı: {len(results)}")
    print(f"  Süre: {elapsed:.4f} saniye")
    print(f"  İşlem/Saniye: {len(results)/elapsed:.0f}")
    
    stats = cpu_monitor.get_stats()
    print(f"\n💻 Sistem:")
    print(f"  CPU: {stats['cpu_percent']:.2f}%")
    print(f"  Bellek: {stats['memory_mb']:.2f} MB")


def benchmark_cpu_monitoring():
    """CPU monitoring overhead"""
    print("\n" + "="*60)
    print("📊 CPU MONITORING OVERHEAD")
    print("="*60)
    
    print("\n⏱️ Monitoring Call Overhead (10,000 calls):")
    start = time.time()
    for _ in range(10,000):
        _ = cpu_monitor.get_stats()
    elapsed = time.time() - start
    
    print(f"  Süre: {elapsed:.4f} saniye")
    print(f"  Çağrı/Saniye: {10000/elapsed:.0f}")
    print(f"  Per-call Overhead: {(elapsed/10000)*1000:.4f} ms")


async def main():
    """Benchmark'leri çalıştır"""
    print("\n" + "🔬 AetherOS PERFORMANS BENCHMARK v2.0")
    print("=" * 60)
    
    try:
        await benchmark_async_batch()
        benchmark_cache()
        benchmark_text_processing()
        benchmark_batch_processing()
        benchmark_cpu_monitoring()
        
        # Final report
        print("\n" + "="*60)
        print("📈 FINAL RAPOR")
        print("="*60)
        
        cpu_monitor.print_report()
        
        print("\n✅ Tüm benchmark'ler tamamlandı!")
        print("\nSonuçlar INSTALLATION_SUMMARY.md dosyasına eklenebilir.")
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Benchmark iptal edildi")
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")
        sys.exit(1)
