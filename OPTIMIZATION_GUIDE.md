"""
AetherOS - Optimizasyon Kılavuzu
CPU Kullanımını Düşük Tutma ve Hızlı İşlem
"""

# ============================================================================
# 1. ASYNC İŞLEMLER - CPU DOSTU İŞLEM
# ============================================================================

"""
✅ ASYNC KULLANIMı:
- Blocking I/O işlemleri async/await ile yapılır
- Aynı anda birçok bağlantı açılabilir
- CPU hiç blocking olmaz

Örnek:
"""

import asyncio
from core.async_utils import AsyncBatchProcessor, AsyncHTTPClient

async def example_async():
    # Batch işleme
    processor = AsyncBatchProcessor(batch_size=10, delay=0.01)
    
    async def fetch_item(item):
        # I/O işlem (bellek içi veya ağ)
        await asyncio.sleep(0.01)
        return item * 2
    
    items = list(range(100))
    results = await processor.process(items, fetch_item)
    
    # HTTP istekleri (paralel)
    async with AsyncHTTPClient(max_connections=5) as client:
        tasks = [client.get(f"https://api.example.com/item/{i}") for i in range(10)]
        results = await asyncio.gather(*tasks)


# ============================================================================
# 2. CACHE SİSTEMİ - HIZLI ERIŞIM
# ============================================================================

"""
✅ CACHE KULLANIMI:
- Sık kullanılan verileri RAM'de tut
- TTL (Time To Live) ile eski verileri temizle
- CPU zamanını hesaplama yerine memory'den oku

Örnek:
"""

from core.performance import cache

def example_cache():
    # Veri cache'le
    cache.set('user_data', {'id': 1, 'name': 'Ahmet'})
    
    # Cache'den oku (çok hızlı)
    user = cache.get('user_data')
    
    # Cache boşsa, hesapla ve cache'le
    if not user:
        user = expensive_calculation()
        cache.set('user_data', user)


# ============================================================================
# 3. BELLEK VERİMLİ VERI İŞLEME
# ============================================================================

"""
✅ STREAM İŞLEME (Büyük dosyalar):
- Tüm dosyayı belleğe yüklemek yerine, satır satır oku
- Batch işleme ile bellek kullanımı kontrolü altında

Örnek:
"""

from core.data_processor import StreamProcessor, BatchProcessor
from pathlib import Path

def example_stream_processing():
    # Büyük JSON Lines dosyasını stream et
    for item in StreamProcessor.read_large_json(Path('data/large_file.jsonl')):
        # Her item için işlem yap (bellek verimli)
        process_item(item)
    
    # Batch işleme
    processor = BatchProcessor(batch_size=1000)
    
    def batch_processor_func(batch):
        # 1000 item'i birlikte işle
        return [process_item(item) for item in batch]
    
    items = StreamProcessor.read_large_json(Path('data/large_file.jsonl'))
    results = list(processor.process(items, batch_processor_func))


# ============================================================================
# 4. CPU MONITORING - PERFORMANS TAKİBİ
# ============================================================================

"""
✅ MONITORING:
- CPU kullanımını gerçek zamanlı izle
- Sorunları erken tespit et
- Optimizasyon kararlarını veri ile al

Örnek:
"""

from core.performance import cpu_monitor

def example_monitoring():
    # Anlık istatistikler
    stats = cpu_monitor.get_stats()
    print(f"CPU: {stats['cpu_percent']}%")
    print(f"Bellek: {stats['memory_mb']} MB")
    
    # Ortalama CPU
    avg_cpu = cpu_monitor.get_average_cpu()
    print(f"Ort. CPU: {avg_cpu}%")
    
    # Rapor yazdır
    cpu_monitor.print_report()


# ============================================================================
# 5. OPTİMİZASYON TIPLERİ
# ============================================================================

"""
⚡ HIZLI VERI YAPILARI:
"""

# ❌ Yavaş (CPU ve bellek harcar)
def slow_processing(items):
    result = []
    for item in items:
        if item > 5:  # Her seferinde kontrol
            result.append(item * 2)  # Her seferinde kopya
    return result

# ✅ Hızlı (CPU ve bellek verimli)
def fast_processing(items):
    return [item * 2 for item in items if item > 5]  # List comprehension

# ✅ Çok hızlı (Generator - bellek verimli)
def very_fast_processing(items):
    return (item * 2 for item in items if item > 5)  # Lazy evaluation


# ============================================================================
# 6. THREAD POOL - I/O İŞLEMLERİ İÇİN
# ============================================================================

"""
✅ THREAD POOL:
- I/O işlemleri için thread pool kullan
- CPU işlemleri için multiprocessing kullan
- AsyncIO tercih et (daha verimli)

Örnek:
"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio

def example_thread_pool():
    # I/O işlemleri için (dosya okuma, ağ, vb.)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(read_file, f) for f in file_list]
        results = [f.result() for f in futures]


# ============================================================================
# 7. GARBAGE COLLECTION AYARI
# ============================================================================

"""
✅ GARBAGE COLLECTION:
- GC'yi manuel kontrol et
- Yoğun işlemler sırasında GC'yi devre dışı bırak
- İşlem bitince GC'yi çalıştır

Örnek:
"""

import gc

def example_gc():
    # GC devre dışı (yoğun işlem öncesi)
    gc.disable()
    
    try:
        # Yoğun işlemler
        for i in range(1000000):
            data = process_item(i)
    finally:
        # GC etkinleştir (işlem sonrası)
        gc.enable()
        gc.collect()  # Şimdi bellek temizle


# ============================================================================
# 8. BEST PRACTICES
# ============================================================================

"""
✅ EN İYİ UYGULAMALAR:

1. ASYNC TERCIH ET:
   - asyncio > threading > multiprocessing
   - AsyncIO daha hafif ve CPU dostu

2. BATCH İŞLEME KULLAN:
   - Bir seferde birçok item işle
   - Overhead'i azalt

3. CACHE KULL:
   - Sık kullanılan veriler RAM'de
   - Hesaplama zamanı ve CPU kaydedilir

4. STREAM İŞLEME KULLAN:
   - Büyük dosyalar için
   - Bellek sınırını aşmaz

5. CPU MONITOR:
   - Optimizasyonun etkisini ölç
   - Veri-tabanlı kararlar al

6. LAZY EVALUATION:
   - Generator kullan
   - Gerekli olduğunda hesapla

7. PROFILING YAP:
   - py-spy kullan
   -병목noktasını tespit et

8. BATCH SIZE OPTİMİZE ET:
   - Çok küçük = overhead fazla
   - Çok büyük = bellek problem
   - Test et ve ayar yap
"""


# ============================================================================
# 9. PRATIK ÖRNEKLER
# ============================================================================

async def realistic_example():
    """Gerçekçi bir örnek"""
    
    # 1. Cache kontrol et
    from core.performance import cache
    cached = cache.get('expensive_data')
    if cached:
        return cached
    
    # 2. Async batch işleme
    from core.async_utils import AsyncBatchProcessor
    processor = AsyncBatchProcessor(batch_size=20, delay=0.01)
    
    async def fetch_and_process(item_id):
        # Async I/O işlem
        data = await fetch_from_api(item_id)
        return process_data(data)
    
    # 3. İşleri paralel yap
    item_ids = range(100)
    results = await processor.process(item_ids, fetch_and_process)
    
    # 4. Sonuçları cache'le (sonraki çağrılar hızlı olur)
    cache.set('expensive_data', results)
    
    # 5. Monitoring
    stats = cpu_monitor.get_stats()
    if stats['cpu_percent'] > 80:
        print("⚠️ CPU yüksek, işlemi yavaşlat")
        await asyncio.sleep(1)
    
    return results


# ============================================================================
# QUICK START
# ============================================================================

"""
Hızlı Başlangıç:

1. Requirements yükle:
   pip install -r requirements.txt

2. Ana dosya çalıştır:
   python main.py

3. CPU monitoring ekle:
   from core.performance import cpu_monitor
   cpu_monitor.print_report()

4. Async işlem yap:
   from core.async_utils import AsyncBatchProcessor
   processor = AsyncBatchProcessor()
   results = await processor.process(items, func)

5. Cache kullan:
   from core.performance import cache
   cache.set('key', value)
   value = cache.get('key')

Daha fazla bilgi için README.md dosyasını oku.
"""
