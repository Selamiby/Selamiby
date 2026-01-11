# AetherOS - Hızlı Başlangıç Rehberi

## ⚡ 5 Dakikada Başlangıç

### 1. Kurulum (Windows)

```powershell
# Proje dizinine git
cd C:\Users\selam\AetherOS

# Launcher'ı çalıştır (otomatik setup yapar)
.\run_aether.bat
```

**Alternatif Manuel Kurulum:**

```powershell
# Virtual environment oluştur
python -m venv venv

# Aktivet
venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Çalıştır
python main.py
```

### 2. İlk Çalışma

Program başladığında şu komutları deneyin:

```
Seçim: 1  → Performans istatistikleri
Seçim: 2  → Async işlem örneği
Seçim: 3  → Cache sistemi
Seçim: 6  → CPU raporu
Seçim: 7  → Tüm testler
```

### 3. Python Kodunda Kullanım

#### CPU Monitoring:
```python
from core.performance import cpu_monitor

stats = cpu_monitor.get_stats()
print(f"CPU: {stats['cpu_percent']}%")
print(f"Bellek: {stats['memory_mb']} MB")
```

#### Async İşlem:
```python
import asyncio
from core.async_utils import AsyncBatchProcessor

async def main():
    processor = AsyncBatchProcessor(batch_size=10)
    
    async def process(item):
        return item * 2
    
    results = await processor.process(range(100), process)
    return results

asyncio.run(main())
```

#### Cache:
```python
from core.performance import cache

# Veri kaydet
cache.set('user_1', {'name': 'Ahmet', 'age': 30})

# Veri oku
user = cache.get('user_1')
```

#### Veri İşleme:
```python
from core.data_processor import StreamProcessor, TextProcessor

# Büyük JSON dosyasını stream et
for item in StreamProcessor.read_large_json('data/large_file.jsonl'):
    process(item)

# Metni chunk'lara böl
chunks = TextProcessor.chunk_text(text, chunk_size=512)
```

### 4. Modülleri Kullanma

```python
from modules.example_modules import DataProcessor, TextAnalyzer

# Veri işleme
processor = DataProcessor()
results = await processor.process_items(items)

# Metin analizi
analyzer = TextAnalyzer()
analysis = analyzer.analyze_text(text)
```

### 5. Tools Kullanma

```python
from tools.utility_tools import FileTools, PerformanceTools, TextTools

# Dosya işlemleri
FileTools.export_to_jsonl(data, 'output.jsonl')

# Performans kontrolü
health = PerformanceTools.check_system_health()

# Metin işleme
chunks = TextTools.process_large_text(text, operation='chunk')
```

## 🎯 Sık Yapılan İşlemler

### Async İşlem Yapmak

```python
import asyncio
from core.async_utils import AsyncBatchProcessor

async def batch_process_items():
    processor = AsyncBatchProcessor(batch_size=50, delay=0.01)
    
    items = range(1000)
    
    async def process(item):
        # I/O işlem (network, database, vb.)
        await asyncio.sleep(0.01)
        return item * 2
    
    results = await processor.process(items, process)
    return results
```

### Büyük Dosyayı Okumak

```python
from pathlib import Path
from core.data_processor import StreamProcessor

# Bellek verimli okuma
for item in StreamProcessor.read_large_json(Path('data/huge.jsonl')):
    process_item(item)
    # Bellek otomatik kontrol altında
```

### CPU Monitoring

```python
from core.performance import cpu_monitor

# Anlık istatistikler
stats = cpu_monitor.get_stats()

# İstatistik raporu
cpu_monitor.print_report()

# Ortalama CPU
avg = cpu_monitor.get_average_cpu()
```

### Cache İle Performans İyileştirme

```python
from core.performance import cache

def expensive_operation():
    cache_key = 'my_result'
    
    # Cache kontrol
    result = cache.get(cache_key)
    if result:
        return result  # Hızlı dönüş
    
    # Pahalı işlem
    result = do_expensive_calculation()
    
    # Cache'le
    cache.set(cache_key, result)
    return result
```

### Sistem Sağlığını Kontrol

```python
from tools.utility_tools import PerformanceTools

health = PerformanceTools.check_system_health()
print(f"Status: {health['status']}")
print(f"CPU: {health['cpu_usage']}%")
print(f"Bellek: {health['memory_usage_mb']} MB")

if health['recommendations']:
    print("Öneriler:")
    for rec in health['recommendations']:
        print(f"  - {rec}")
```

## 📁 Dosya Yapısı

```
AetherOS/
├── main.py                 # Ana uygulama
├── requirements.txt        # Bağımlılıklar
├── run_aether.bat         # Windows launcher
├── QUICK_START.md         # Bu dosya
├── README.md              # Tam dokumentasyon
├── OPTIMIZATION_GUIDE.md  # Optimizasyon rehberi
├── config/
│   ├── settings.yaml      # Ayarlar
│   └── api_keys.yaml      # API anahtarları
├── core/
│   ├── performance.py     # CPU monitoring, cache
│   ├── async_utils.py     # Async işlemler
│   └── data_processor.py  # Veri işleme
├── modules/
│   └── example_modules.py # Örnek modüller
├── tools/
│   └── utility_tools.py   # Yardımcı araçlar
├── data/                  # Veri dosyaları
├── logs/                  # Log dosyaları
└── web/                   # Web arayüzü (gelecek)
```

## 🐛 Sorun Giderme

### ImportError: No module named 'core'

Çözüm: `main.py` dosyasının proje köküne olduğundan emin olun.

```powershell
# Virtual environment'ı activate et
venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### psutil Kurulum Hatası

```powershell
# Visual C++ Build Tools gerekebilir
pip install --upgrade setuptools wheel
pip install psutil==5.9.6
```

### CPU Monitoring Çalışmıyor

```python
# psutil'in doğru yüklendiğini kontrol et
import psutil
print(psutil.__version__)
```

## 💡 İpuçları

1. **Async Tercih Et**: ThreadPool yerine AsyncIO kullan
2. **Cache Kulllan**: Sık erişilen veriler RAM'de tutulur
3. **Batch İşleme**: Birçok işi batch'ler halinde yap
4. **Monitoring Yap**: CPU/Bellek istatistikleri izle
5. **Lazy Loading**: Generator ile gerektiğinde yükle

## 📚 Daha Fazla Bilgi

- **Detaylı Rehber**: `README.md`
- **Optimizasyon İpuçları**: `OPTIMIZATION_GUIDE.md`
- **API Dokümantasyonu**: Kod içi docstring'leri oku

## 🚀 Sonraki Adımlar

1. Modülleri özelleştir (`modules/`)
2. Tools'u genişlet (`tools/`)
3. Web arayüzü ekle (`web/`)
4. AI modelleri entegre et

---

**Sorular mı var?** Kod içindeki docstring'leri oku veya GitHub Issues açıl.
