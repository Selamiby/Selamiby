
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
    ```bash
    git clone https://github.com/your-username/aetheros.git
    cd aetheros
    ```

2.  **Python bağımlılıklarını kurun:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ortam değişkenlerini ayarlayın:**
    `.env.example` dosyasını kopyalayarak `.env` adında yeni bir dosya oluşturun ve gerekirse içindeki değişkenleri düzenleyin.

### Başlatma
Sistemi başlatmak için `api_server.py` dosyasını çalıştırın:
```bash
python backend/api_server.py
```
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
