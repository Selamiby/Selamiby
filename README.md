
# 🚀 AETHEROS / NEXUS-ONE
## Autonomous System Management Platform

### 📋 Özellikler
- 🔄 **Otonom Backup Management**
- 📊 **Real-time System Monitoring**
- 🗂️ **Smart File Organization**
- 🌐 **REST API + Web Dashboard**
- ⚡ **Modüler Mimari**
- 🔧 **Kolay Kurulum**

### 🚀 Hızlı Başlangıç

#### Kurulum
```bash
# 1. Kurulum script'ini çalıştır
curl -sSL https://raw.githubusercontent.com/your-repo/install.sh | bash

# 2. Proje dizinine git
cd ~/aetheros

# 3. Başlat
./scripts/start.sh
```

---

**AETHEROS, otonom bir sistem yönetimi ve görev otomasyon platformudur.**

Bu proje, `NEXUS-ONE` kod adıyla geliştirilen, modüler ve genişletilebilir bir yapıya sahip akıllı bir backend sistemidir. Sistem kaynaklarını izler, otomatik yedeklemeler yapar, görevleri zamanlar ve bir API aracılığıyla yönetilebilir.

## ✨ Temel Özellikler

- **Modüler Mimari:** `NexusCore` etrafında şekillenen, kolayca yeni yetenekler eklenebilen bir yapı.
- **Sistem İzleme:** CPU, bellek, disk, ağ ve GPU kullanımını gerçek zamanlı olarak izler ve anormal durumlarda uyarılar oluşturur.
- **Otomatik Yedekleme:** Belirlenen dosya ve klasörleri zamanlanmış görevlerle sıkıştırarak yedekler ve eski yedekleri temizler.
- **Görev Zamanlama:** Tekrarlayan veya tek seferlik görevleri (örn. sistem temizliği, raporlama) otomatize eder.
- **Dosya Organizasyonu:** Klasörleri izleyerek dosyaları türlerine göre otomatik olarak düzenler.
- **RESTful API:** Sistemin tüm fonksiyonlarını kontrol etmek için `FastAPI` tabanlı modern bir API sunar.
- **Basit Web Arayüzü:** Sistemin genel durumunu gösteren ve temel işlemleri yapmaya olanak tanıyan bir dashboard.

## 🚀 Kurulum ve Başlatma

### Gereksinimler
- Python 3.9+
- pip

### Kurulum
1.  **Projeyi klonlayın (veya indirin):**
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
