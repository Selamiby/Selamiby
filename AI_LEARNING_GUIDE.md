# NEXUS-ONE AI Hızlandırılmış Öğrenme Sistemi 🚀

## 🎯 Yeni Özellikler

### 1. 🌐 Web Navigator & Learning
**Dosya**: `web_navigator.py`

Selenium-based browser otomasyonu ile:
- ✅ Google arama ve öğrenme
- ✅ YouTube video izleme (screenshot capture)
- ✅ GitHub repo analizi
- ✅ Otomatik screenshot alma
- ✅ Web içerik çıkarma
- ✅ Link takibi ve navigasyon

**Kullanım**:
```python
from web_navigator import WebNavigator

nav = WebNavigator(headless=False)
nav.search_google("Python machine learning")
nav.learn_from_youtube("https://youtube.com/watch?v=...", duration_sec=60)
nav.learn_from_code_repo("https://github.com/user/repo")
nav.close()
```

**Chat Komutları**:
- `"web öğren"` → Web öğrenme ajanını başlat
- `"youtube öğren"` → Video öğrenme
- `"internet gezin"` → Browser otomasyonu

### 2. 💻 Code Generator
**Dosya**: `code_generator.py`

AI destekli kod üretimi:
- ✅ Workspace'den pattern öğrenme
- ✅ Function/class template çıkarma
- ✅ Yeni script üretme (simple/class)
- ✅ Otomatik test ve validation
- ✅ Import/pattern analizi

**Kullanım**:
```python
from code_generator import CodeGenerator

gen = CodeGenerator()
gen.learn_from_workspace()  # Tüm Python dosyalarından öğren
script = gen.generate_script("my_tool", template_type="class")
result = gen.test_generated_code(script)
```

**Chat Komutları**:
- `"kod yaz"` → Kod üretici aç
- `"script oluştur"` → Yeni script üret
- `"program yaz"` → Code generator başlat

### 3. 🎮 Game Engine Controller
**Dosya**: `game_engine_controller.py`

Unity ve Unreal Engine CLI entegrasyonu:
- ✅ Unity proje oluşturma
- ✅ C# script üretme
- ✅ Unity Editor açma
- ✅ Unreal Engine desteği (placeholder)

**Kullanım**:
```python
from game_engine_controller import GameEngineController

controller = GameEngineController()
controller.create_unity_project("MyGame", template="3D")
controller.create_unity_script("MyGame", "PlayerController", "MonoBehaviour")
controller.open_unity_project("MyGame")
```

**Chat Komutları**:
- `"oyun yap"` → Game engine kontrolü aç
- `"unity"` → Unity controller
- `"unreal"` → Unreal Engine

### 4. 🧠 Accelerated Learning System
**Dosya**: `accelerated_learning.py`

Multi-modal öğrenme sistemi:
- ✅ Concept learning ve reinforcement
- ✅ Code pattern learning
- ✅ Web knowledge accumulation
- ✅ Visual pattern recognition
- ✅ Skill tracking (coding, web, games, problem-solving)
- ✅ Adaptive learning rate (0.1x - 10x)

**Kullanım**:
```python
from accelerated_learning import AcceleratedLearning

learner = AcceleratedLearning()
learner.learn_concept("Machine Learning", {"type": "AI", "difficulty": "advanced"})
learner.learn_from_code("def train(): ...", "python")
learner.increase_learning_rate(2.0)  # 2x hızlandır
summary = learner.get_knowledge_summary()
```

**Öğrenme Hızı Kontrolü**:
- Panel'de slider ile 0.1x - 10x arası ayarlama
- JSON config ile otomatik kayıt
- Skill seviyelerini otomatik artırma

## 🎮 Geliştirilmiş Kontrol Paneli

### Yeni Butonlar (Row 4)
- **Web Learning**: Web öğrenme ajanını başlat
- **Code Generator**: Kod üretici açar
- **Game Engine**: Oyun motoru kontrolleri

### Learning Rate Slider
- `Yavaş` ◀━━━━━━━▶ `Hızlı`
- Gerçek zamanlı ayarlama (0.1x - 10x)
- Öğrenme hızını anlık değiştir

### Genişletilmiş Chat Komutları

#### 🌐 Web & Learning
```
web öğren
youtube öğren
internet gezin
kod öğren
```

#### 💻 Kod Yazma
```
kod yaz
script oluştur
program yaz
code generate
```

#### 🎮 Oyun Geliştirme
```
oyun yap
unity
unreal
game engine
```

#### 📈 Öğrenme Kontrolü
```
öğrenme hızı
hızlandır
learning rate
```

## 📁 Yeni Dosya Yapısı

```
NEXUS-ONE/
├── web_navigator.py          # Browser automation & web learning
├── code_generator.py          # AI code generation
├── game_engine_controller.py  # Unity/Unreal integration
├── accelerated_learning.py    # Multi-modal learning system
├── ui/
│   └── human_control_panel.py # Genişletilmiş panel (row 4, slider)
├── nexus_data/
│   ├── screenshots/           # Web learning screenshots
│   ├── web_learning.json      # Web öğrenme verileri
│   ├── code_patterns.json     # Kod pattern'leri
│   ├── knowledge_base.json    # Bilgi tabanı
│   └── learning_config.json   # Öğrenme ayarları
├── nexus_logs/
│   ├── web_navigator.log
│   ├── code_generator.log
│   ├── game_engine.log
│   └── accelerated_learning.log
└── generated/                 # AI üretimi kod dosyaları
```

## 🚀 Hızlı Başlangıç

### 1. Dependencies Kur
```bash
pip install selenium pillow opencv-python
```

### 2. Chrome WebDriver
Selenium için Chrome WebDriver gerekli:
- Otomatik: Selenium 4.16+ kendi yükler
- Manuel: [ChromeDriver](https://chromedriver.chromium.org/)

### 3. Paneli Aç
```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_control_panel.ps1
```

### 4. Öğrenmeyi Başlat
```
# Chat'te yaz:
web öğren
öğrenme hızı    # Slider'ı 5x yap
kod yaz
```

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: Web'den Öğren
```python
# 1. Panel'den "Web Learning" tıkla veya chat'te "web öğren"
# 2. Ajan otomatik Google'da arar
# 3. YouTube videolarını izler ve screenshot alır
# 4. GitHub repo'larını analiz eder
# 5. Tüm bilgiler nexus_data/web_learning.json'a kaydedilir
```

### Senaryo 2: Kod Üret
```python
# 1. "Kod Yaz" butonuna tıkla veya chat'te "kod yaz"
# 2. Workspace'deki tüm Python dosyalarını analiz eder
# 3. Pattern'leri çıkarır (functions, classes, imports)
# 4. Yeni script üretir: generated/nexus_demo_script.py
# 5. Otomatik test eder ve sonucu loglar
```

### Senaryo 3: Unity Oyunu Yap
```python
# 1. "Game Engine" butonuna tıkla
# 2. Unity bulunamazsa yükleme yolunu gösterir
# 3. Unity bulunursa:
#    - Yeni proje oluşturur
#    - C# script'leri üretir
#    - Editor'ü açar
```

### Senaryo 4: Hızlandırılmış Öğrenme
```python
# 1. Learning rate slider'ı 10x yap
# 2. "web öğren" + "kod yaz" + "oyun yap" kombine çalıştır
# 3. Her işlemden 10x hızlı skill kazanır
# 4. knowledge_base.json'da skill seviyelerini görebilirsin:
#    - coding: 85/100
#    - web_navigation: 72/100
#    - game_development: 45/100
```

## 📊 Öğrenme İlerlemesi

### Skill Seviyeleri
```json
{
  "skills": {
    "coding": 85.5,
    "web_navigation": 72.3,
    "game_development": 45.0,
    "problem_solving": 90.1
  }
}
```

### Knowledge Base
- **Concepts**: 150+ öğrenilmiş kavram
- **Code Patterns**: 200+ kod pattern'i
- **Visual Patterns**: 50+ screenshot analizi
- **Web Knowledge**: 100+ web kaynağı

## 🔧 Yapılandırma

### learning_config.json
```json
{
  "learning_rate": 5.0,
  "focus_areas": ["coding", "web", "games"],
  "auto_learn_enabled": true,
  "batch_size": 10
}
```

### web_learning.json
```json
{
  "visited_urls": [...],
  "learned_patterns": [
    {
      "type": "youtube",
      "url": "...",
      "duration": 30,
      "screenshots": 6,
      "time": "2026-01-12T..."
    }
  ]
}
```

## ⚠️ Notlar

1. **Selenium**: Chrome WebDriver otomatik yüklenir (Selenium 4.16+)
2. **Unity**: Manuel kurulum gerekir (Unity Hub + Editor)
3. **Learning Rate**: 10x çok hızlı olabilir, dikkatli kullan
4. **Screenshots**: nexus_data/screenshots/ klasöründe birikir
5. **Generated Code**: generated/ klasöründe test edilmeli

## 🎓 Öğrenme Döngüsü

```
1. Web Navigator → İnternet'ten bilgi topla
   ↓
2. Code Generator → Pattern'leri öğren ve kod üret
   ↓
3. Accelerated Learning → Bilgiyi knowledge base'e ekle
   ↓
4. Game Engine → Unity/Unreal ile uygula
   ↓
5. Learning Rate ↑ → Süreci hızlandır
   ↓
6. Tekrar 1'e dön (sürekli öğrenme)
```

## 🚀 İleri Seviye

### Otomatik Öğrenme Pipeline
Otonom sistem ile entegre ederek sürekli öğrenme:
```powershell
# autonomous_advanced.ps1'e ekle:
# - Her 30dk web öğrenme
# - Her 1 saat kod pattern analizi
# - Her 6 saat Unity proje güncelleme
```

### External LLM Integration
Code generator ve learning system'e LLM bağlayarak:
- GPT-4 ile kod review
- Claude ile pattern analizi
- Gemini ile multi-modal learning

---

**Tüm özellikler aktif!** Panel'i aç ve `"web öğren"`, `"kod yaz"`, `"oyun yap"` komutlarını dene 🚀
