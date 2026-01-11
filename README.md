
# 🤖 NEXUS-ONE AI Copilot
## Masaüstü Yapay Zeka Asistanı - Kopyala-Yapıştır YOK!

### ⚡ Özellikler
- 💬 **Copilot Chat Mode**: Chat'te komut ver, direkt sonuç gör!
- 🔍 **Web Learning**: Google ara, YouTube izle, GitHub öğren
- 💻 **Code Generation**: AI workspace'i öğrenir, kod yazar (171 fonksiyon bilir)
- 🎮 **Game Engine**: Unity/Unreal proje oluştur
- 🛡️ **Security**: Autonomous güvenlik duvarı, Windows Defender entegrasyonu
- 📊 **System Monitor**: CPU, RAM, AI becerileri canlı takip
- ⚡ **Learning Rate**: 0.1x - 10x öğrenme hızı kontrolü
- 🧵 **Threading**: Panel donmaz, her şey arka planda

### 🚀 Hızlı Başlangıç

#### 1. Masaüstü Kısayol (EN KOLAY)
```
Masaüstünde "NEXUS-ONE AI" simgesi → Çift tıkla!
```

#### 2. PowerShell
```powershell
cd C:\Users\selam\NEXUS-ONE
python ui/human_control_panel.py
```

#### 3. İlk Komut (Chat'te yaz!)
```
help
```
→ Tüm komutlar görünür

---

## 🎯 Copilot Mode Örnekleri

### Google Arama (5 saniye)
```
python machine learning ara
```
**Sonuç**: İlk 5 Google sonucu chat'te!

### Kod Yaz (3 saniye)
```
kod yaz calculator
```
**Sonuç**: ✅ calculator.py oluşturuldu, test edildi!

### Sistem Durumu
```
sistem durumu
```
**Sonuç**: 
```
CPU: 45.2%
RAM: 68.3% (16GB / 32GB)
🧠 AI Becerileri:
  Kod yazma: 85/100
  Web gezinme: 72/100
```

---

## 📚 Dokümantasyon

### Başlangıç Kılavuzları
- **[🚀 QUICK_START_COPILOT.md](QUICK_START_COPILOT.md)** - İlk kullanım, hızlı başlangıç
- **[🤖 COPILOT_MODE_GUIDE.md](COPILOT_MODE_GUIDE.md)** - Tüm komutlar, örnekler, teknik detaylar

### Özellik Detayları
- **[🧠 AI_LEARNING_GUIDE.md](AI_LEARNING_GUIDE.md)** - Web learning, code generation, game engine
- **[🛡️ SECURITY_AND_CHAT_GUIDE.md](SECURITY_AND_CHAT_GUIDE.md)** - Güvenlik özellikleri, chat komutları

---

## 🔧 Kurulum

### Gereksinimler
- **Python 3.11+** (zorunlu)
- **Windows 10/11** (PowerShell, Windows Defender API kullanır)
- **Chrome** (Web learning için)

### Paket Kurulumu
```powershell
pip install -r requirements.txt
pip install selenium pillow opencv-python
```

### Unity (Opsiyonel - Oyun geliştirme için)
```
Unity Hub → Editor Yükle → 2022.3.0f1+
```

---

## 💬 Tüm Chat Komutları

| Kategori | Komut | Açıklama |
|----------|-------|----------|
| **Web** | `X ara` | Google'da ara, 5 sonuç getir |
| | `youtube.com/... öğren` | Video izle, screenshot al |
| | `github.com/... öğren` | Repo analiz et |
| **Code** | `kod yaz X` | Script oluştur, test et |
| | `workspace öğren` | 50+ dosyadan öğren |
| **Security** | `güvenlik başlat` | Monitoring başlat |
| | `defender tara` | Virüs taraması |
| **System** | `sistem durumu` | CPU/RAM/AI becerileri |
| **Learning** | `öğrenme hızı Xx` | Hız ayarla (0.1x-10x) |
| **Game** | `unity proje X` | Unity projesi oluştur |
| **Help** | `help` | Komut listesi + örnekler |

---

## 🎮 Masaüstü Kısayol

Panel'i hızlıca açmak için masaüstünde **"NEXUS-ONE AI"** kısayolu var:
```
Hedef: C:\Users\selam\NEXUS-ONE\ui\human_control_panel.py
Python: C:\Users\selam\AppData\Local\Programs\Python\Python311\python.exe
```

**Çift tıkla → Panel açılır → Chat'e komut yaz!**

---

## 🧠 AI Becerileri

NEXUS-ONE gerçek zamanlı öğrenir ve becerilerini chat'te gösterir:

```
sistem durumu
```

**Çıktı**:
```
🧠 AI Becerileri:
  Kod yazma: 0-100 (workspace'ten öğrendikçe artar)
  Web gezinme: 0-100 (Google/YouTube/GitHub gezinceleri)
  Oyun geliştirme: 0-100 (Unity proje sayısı)
```

Her işlem sonrası beceriler güncellenir!

---

## 📊 Teknik Mimari

### Modüler Yapı
```
NEXUS-ONE/
├── ui/
│   └── human_control_panel.py   # 🎛️ Copilot Panel (Tkinter)
├── web_navigator.py              # 🌐 Selenium browser automation
├── code_generator.py             # 💻 AST-based code generation
├── game_engine_controller.py     # 🎮 Unity/Unreal automation
├── accelerated_learning.py       # ⚡ Multi-modal learning system
├── nexus_security.py             # 🛡️ Defensive security agent
└── requirements.txt              # 📦 Dependencies
```

### Threading Model
- **Main Thread**: Tkinter UI (chat display, buttons)
- **Worker Threads**: AI operations (web search, code gen) → panel donmaz
- **Background Processes**: Security agent, monitoring daemon

### AI Modules
| Modül | Dil | LOC | Bağımlılık |
|-------|-----|-----|------------|
| Web Navigator | Python | ~400 | selenium |
| Code Generator | Python | ~350 | ast, pathlib |
| Game Engine | Python | ~300 | Unity CLI |
| Accelerated Learning | Python | ~400 | multi-modal |
| Security | Python | ~600 | Windows API |

---

## 🎉 Sonuç

**NEXUS-ONE AI Copilot** = Masaüstü Yapay Zeka Asistanı!

✅ Kopyala-yapıştır YOK
✅ Her şey chat'te
✅ 171 fonksiyon bilir
✅ Web'i öğrenir
✅ Kod yazar
✅ Oyun geliştirir
✅ Güvenlik izler

**İlk adım**:
```
Masaüstü → NEXUS-ONE AI → Çift tıkla → "help" yaz
```

**Hoş geldin!** 🚀
Sunucu varsayılan olarak `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

- **Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Dokümantasyonu (Swagger):** [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

## 🔧 Modüller
Proje, aşağıdaki ana modüllerden oluşur:
- **Nexus Core:** Sistemin merkezi orkestratörü.
- **System Monitor:** Kaynak izleme modülü.
- **Backup Manager:** Yedekleme ve geri yükleme modülü.
- **File Organizer:** Otomatik dosya düzenleme modülü.
- **Task Scheduler:** Görev zamanlama modülü.

Daha fazla bilgi için `docs/MODULES.md` dosyasına bakın.
