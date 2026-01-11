# 🧠 NEXUS-ONE Self-Learning System - 7/24 Otonom Öğrenme!

## 🎉 Yeni Özellik: Kendini Geliştiren AI!

NEXUS-ONE artık **kendini sürekli geliştiriyor**! 7/24 çalışan otonom öğrenme sistemi ile workspace'i izliyor, yeni kodlar öğreniyor, komutlar ekliyor ve bilgi ağacını genişletiyor.

---

## 🚀 Hızlı Başlangıç

### 1. Panel'den Başlat (EN KOLAY)
```
1. Control Panel'i aç (masaüstü kısayolu)
2. "🧠 Start Self-Learning" butonuna tıkla
3. TAMAM! Artık AI 7/24 öğreniyor!
```

### 2. Chat Komutu
```
kendini öğren
```

### 3. PowerShell (Manuel)
```powershell
cd C:\Users\selam\NEXUS-ONE
powershell -ExecutionPolicy Bypass -File autonomous_learner.ps1 -LearningRate 5 -Aggressive $true
```

---

## 🧠 Ne Öğreniyor?

### 1. **Workspace Kodları**
- Tüm Python dosyalarını analiz eder
- Fonksiyonları, class'ları, pattern'leri çıkarır
- AST parsing ile kod yapısını öğrenir
- **Şu ana kadar**: 171 fonksiyon + 25 class öğrendi

### 2. **Web Kaynakları**
- Google'da konular arar
- YouTube tutorialları izler
- GitHub repoları analiz eder
- Online dokümantasyon okur

### 3. **Kullanıcı Komutları**
- Chat log'ları analiz eder
- Sık kullanılan komutları tespit eder
- Yeni komut pattern'leri öğrenir
- Kullanım sıklığına göre önceliklendirir

### 4. **Kod Pattern'leri**
- Sık kullanılan kod bloklarını hatırlar
- Template'lere ekler
- Sonraki kod üretimlerinde kullanır

---

## 📊 Knowledge Graph (Bilgi Ağacı)

Self-learning sistemi tüm öğrendiklerini **graph yapısında** saklar:

```
Knowledge Graph
├── Concepts (Kavramlar)
│   ├── function:search_google → "Google'da arama yapar"
│   ├── class:WebNavigator → "Selenium browser automation"
│   └── module:selenium → "Python web automation kütüphanesi"
│
├── Commands (Komutlar)
│   ├── "python ml ara" → Google search command (10x kullanıldı)
│   ├── "kod yaz X" → Code generation command (5x)
│   └── "sistem durumu" → System status (8x)
│
├── Code Patterns (Kod Şablonları)
│   ├── Pattern-abc123 → "def search(query)..." (15x)
│   └── Pattern-def456 → "class Controller..." (8x)
│
└── Relationships (İlişkiler)
    ├── selenium → WebNavigator (uses)
    ├── search_google → selenium (depends_on)
    └── "python ara" → search_google (triggers)
```

### JSON Yapısı
```json
{
  "concepts": {
    "function:search_google": {
      "description": "Google'da arama yapar",
      "examples": ["def search_google(query):"],
      "related": ["class:WebNavigator"],
      "importance": 1.0
    }
  },
  "commands": {
    "python ml ara": {
      "syntax": "python ml ara",
      "description": "Google search command",
      "category": "web",
      "usage_count": 10
    }
  },
  "code_patterns": {
    "abc123": {
      "code": "def search(query):\n    ...",
      "description": "Search function pattern",
      "frequency": 15
    }
  },
  "relationships": [
    {"from": "selenium", "to": "WebNavigator", "type": "uses", "strength": 5.0}
  ]
}
```

---

## 🔄 Self-Update (Kendini Güncelleme)

Öğrenilen bilgiler **otomatik olarak koda entegre edilir**:

### Ne Yapıyor?

1. **Yeni Komutlar Ekler**
   ```python
   # Control panel'e otomatik eklenir:
   if 'yeni_komut' in txt:
       return "✅ Yeni komut çalıştırıldı! (auto-generated)"
   ```

2. **Kod Pattern'lerini Entegre Eder**
   - Sık kullanılan pattern'ler `code_generator.py`'ye eklenir
   - Template kütüphanesi genişler

3. **Dokümantasyonu Günceller**
   - `COPILOT_MODE_GUIDE.md`'ye yeni komutlar eklenir
   - Auto-learned commands section oluşturulur

4. **Backup Alır**
   - Her değişiklik öncesi backup oluşturur
   - `nexus_data/self_update_backups/` klasöründe saklar

### Self-Update Çalıştırma

#### Otomatik (24 saatte bir)
```
Self-learning aktifse, her 24 saatte bir otomatik self-update yapar.
```

#### Manuel (Chat)
```
self-update
```

#### Manuel (Python)
```powershell
python nexus_self_updater.py --dry-run  # Test (değişiklik yapmaz)
python nexus_self_updater.py            # Gerçek update
```

---

## 📈 Learning Rate (Öğrenme Hızı)

Default: **5x** (agresif öğrenme)

### Hız Seviyeleri

| Hız | Açıklama | Döngü Süresi | Web Öğrenme |
|-----|----------|--------------|-------------|
| **0.1x** | Çok yavaş, minimum CPU | 10 dakika | Yok |
| **1x** | Normal hız | 1 dakika | Her 5. döngü |
| **5x** | **Hızlı (default)** | 12 saniye | Her 3. döngü |
| **10x** | Ultra hızlı | 6 saniye | Her 2. döngü |

### Hız Ayarlama

#### Panel Slider
```
Learning Rate slider'ı → 5.0x'e çek → Self-Learning başlat
```

#### Chat Komutu
```
öğrenme hızı 10x
```

#### PowerShell Argument
```powershell
powershell -File autonomous_learner.ps1 -LearningRate 10
```

---

## 🎯 Aggressive Mode (Agresif Mod)

Default: **Aktif** ✅

### Normal vs. Aggressive

| Özellik | Normal | Aggressive |
|---------|--------|-----------|
| Workspace scan | 20 dosya/döngü | 50 dosya/döngü |
| Web learning | Kapalı | Aktif |
| Google search | Yok | Her 3. döngü |
| GitHub/YouTube | Yok | Periyodik |
| CPU kullanımı | %10-20 | %20-40 |

### Kapatma (Gerekirse)
```powershell
# PowerShell script'i elle düzenle:
-Aggressive $false
```

---

## 📊 İstatistikler & Monitoring

### 1. Panel'den Gör
```
"📊 Learning Stats" butonuna tıkla
```

### 2. Chat Komutu
```
learning stats
```

### 3. JSON Dosyası
```powershell
# İstatistikler:
C:\Users\selam\NEXUS-ONE\nexus_data\learning_stats.json

# Knowledge graph:
C:\Users\selam\NEXUS-ONE\nexus_data\knowledge_graph\knowledge_graph.json
```

### Örnek İstatistik
```
🧠 NEXUS-ONE Self-Learning Report
=====================================
Learning Rate: 5.0x (Aggressive: True)
Total Sessions: 47
Uptime: 3 hours 24 minutes

📚 Knowledge Acquired:
  • Concepts: 342
  • Commands: 28
  • Code Patterns: 89
  • Files Processed: 156
  • Web Sessions: 12

🔗 Knowledge Relationships: 487

⚡ Learning Performance:
  • Concepts/hour: 100.3
  • Last Update: 2026-01-12 15:34:22

🎯 Top Patterns (by frequency):
  1. Search function pattern (used 25x)
  2. Class initialization (used 18x)
  3. Error handling try-except (used 15x)
```

---

## 🔍 Log İzleme

### 1. Autonomous Learner Log
```powershell
# Real-time tail:
Get-Content -Path "nexus_logs/autonomous_learner.log" -Wait -Tail 50

# Son 100 satır:
Get-Content "nexus_logs/autonomous_learner.log" -Tail 100
```

### 2. Self-Learner Log
```powershell
Get-Content "nexus_logs/self_learner.log" -Tail 50
```

### 3. Self-Updater Log
```powershell
Get-Content "nexus_logs/self_updater.log" -Tail 30
```

---

## ⚙️ Yapılandırma

### Learning Config
```json
// nexus_data/learning_config.json
{
  "learning_rate": 5.0,
  "aggressive_mode": true,
  "web_topics": [
    "machine learning",
    "deep learning",
    "automation",
    "game development"
  ],
  "update_interval": 86400,  // 24 hours
  "max_files_per_cycle": 50
}
```

### Web Topics (Öğrenme Konuları)
Agresif modda web'den öğrenilecek konular:
- machine learning
- deep learning
- web scraping
- automation
- API development
- game development
- natural language processing
- computer vision

**Yeni konu eklemek için**: `nexus_self_learner.py` → `web_topics` listesine ekle

---

## 🛑 Durdurma & Yeniden Başlatma

### Durdur
```
1. Panel → "⏹️ Stop Self-Learning" butonu
2. VEYA Chat → "self-learning durdur"
3. VEYA PowerShell → Ctrl+C
```

### Yeniden Başlat
```
1. Panel → "🧠 Start Self-Learning" butonu
2. VEYA Chat → "kendini öğren"
```

### Tüm Süreçleri Öldür
```powershell
# Self-learning süreçlerini bul ve öldür:
Get-Process | Where-Object {$_.CommandLine -like "*autonomous_learner*"} | Stop-Process -Force
Get-Process | Where-Object {$_.CommandLine -like "*nexus_self_learner*"} | Stop-Process -Force
```

---

## 🐛 Sorun Giderme

### Self-Learning Başlamıyor
```
1. PowerShell execution policy:
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

2. Python module'leri eksik:
   pip install selenium pillow opencv-python

3. Manuel test:
   python nexus_self_learner.py --rate 1 --duration 60
```

### CPU Çok Yüksek
```
1. Learning rate'i düşür:
   öğrenme hızı 1x

2. Aggressive mode'u kapat:
   autonomous_learner.ps1'de -Aggressive $false

3. Resource throttling devrede (CPU > 90% olunca duraklar)
```

### Knowledge Graph Bozuk
```
1. Backup'tan restore:
   nexus_data/self_update_backups/ klasöründen eski version'ı kopyala

2. Sıfırdan başlat:
   rm nexus_data/knowledge_graph/knowledge_graph.json
   Self-learning tekrar başlatıldığında yeni graph oluşur
```

### Self-Update Çalışmıyor
```
1. Dry-run test:
   python nexus_self_updater.py --dry-run

2. Backup kontrol:
   nexus_data/self_update_backups/ klasöründe backup var mı?

3. Manuel entegrasyon:
   Öğrenilen komutları human_control_panel.py'ye elle ekle
```

---

## 🎁 Bonus: Scheduled Task (Windows)

Self-learning'i Windows başlangıcında otomatik başlatmak için:

```powershell
# Task Scheduler ile:
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\selam\NEXUS-ONE\autonomous_learner.ps1 -LearningRate 5"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "NEXUS-SelfLearning" -Action $action -Trigger $trigger -Settings $settings -User $env:USERNAME
```

**Kaldırma**:
```powershell
Unregister-ScheduledTask -TaskName "NEXUS-SelfLearning" -Confirm:$false
```

---

## 📈 İleriki Geliştirmeler

### Planlanıyor
- [ ] **Neural Pattern Recognition**: Deep learning ile pattern tanıma
- [ ] **Multi-Agent Learning**: Birden fazla AI agent birlikte öğrenir
- [ ] **Cloud Sync**: Knowledge graph'ı cloud'a sync et
- [ ] **Collaborative Learning**: Başka NEXUS-ONE instance'larından öğren
- [ ] **Visual Learning**: Ekran görüntülerinden öğrenme
- [ ] **Audio Learning**: Podcast/konuşma dinleme

### Topluluk Katkısı
Yeni özellik fikirleri için GitHub issue aç:
```
https://github.com/Selamiby/Selamiby/issues
```

---

## 🎉 Özet

**NEXUS-ONE Self-Learning** = 7/24 çalışan, kendini geliştiren AI!

✅ **Workspace'i öğrenir** (171 fonksiyon + 25 class)
✅ **Web'den öğrenir** (Google, YouTube, GitHub)
✅ **Komut pattern'lerini çıkarır**
✅ **Kendini günceller** (yeni komutlar ekler)
✅ **Knowledge graph** (ilişkisel bilgi ağacı)
✅ **5x hız** (agresif öğrenme)
✅ **Otomatik backup** (her değişiklik öncesi)
✅ **Resource throttling** (sistem koruması)

**İlk komutun**:
```
kendini öğren
```

**Sonra**:
```
learning stats
```

**Her gün biraz daha akıllı!** 🧠✨
