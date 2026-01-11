# AETHEROS Modül Dokümantasyonu

Bu dosya, AETHEROS projesinde bulunan ana modüllerin ve eklentilerin açıklamalarını içerir.

## Ana Modüller (Backend)

### 1. Nexus Core (`nexus_core.py`)
- **Sorumluluk:** Sistemin ana beyni ve orkestratörüdür.
- **Özellikler:**
    - Modül yükleme, başlatma, durdurma ve yönetme.
    - Modüller arası iletişim için bir olay (event) sistemi sağlar.
    - Merkezi konfigürasyon yönetimi.
    - Komut satırı arayüzü (CLI) ile etkileşim.
    - Sistem genelinde loglama ve hata yönetimi.

### 2. Backup Manager (`backup_manager.py`)
- **Sorumluluk:** Dosya ve klasörlerin yedeklenmesi ve geri yüklenmesi.
- **Özellikler:**
    - Zamanlanmış (scheduled) yedeklemeler.
    - Tam ve artımlı (incremental) yedekleme stratejileri.
    - Yedekleri sıkıştırma (örn. `.zip`, `.tar.gz`).
    - Yedek bütünlüğünü doğrulama.
    - Eski yedekleri temizlemek için saklama (retention) politikaları.

### 3. System Monitor (`system_monitor.py`)
- **Sorumluluk:** Sistem kaynaklarının (CPU, RAM, disk, ağ) izlenmesi.
- **Özellikler:**
    - Gerçek zamanlı kaynak kullanımı takibi.
    - Belirlenen eşikler aşıldığında uyarı (alert) oluşturma.
    - En çok kaynak tüketen işlemlerin listelenmesi.
    - GPU kullanımı izleme (varsa).

### 4. API Server (`api_server.py`)
- **Sorumluluk:** Sistemin dış dünya ile iletişim kurmasını sağlayan web arayüzü.
- **Özellikler:**
    - FastAPI tabanlı RESTful API.
    - Modülleri kontrol etmek için endpoint'ler (`/api/module/control`).
    - Yedekleme ve geri yükleme işlemleri için endpoint'ler.
    - Sistem metriklerini ve durumunu sunan endpoint'ler.
    - Basit bir web tabanlı dashboard.

## Eklenti Modülleri (Modules)

### 1. File Organizer (`file_organizer.py`)
- **Sorumluluk:** Belirtilen klasörlerdeki dosyaları türlerine, tarihlerine veya diğer kurallara göre otomatik olarak düzenleme.
- **Özellikler:**
    - Kural tabanlı dosya sınıflandırma (resimler, belgeler, videolar vb.).
    - Yinelenen (duplicate) dosyaları tespit etme.
    - Boş klasörleri temizleme.
    - İzleme modunda çalışarak klasörleri periyodik olarak düzenleme.

### 2. Task Scheduler (`task_scheduler.py`)
- **Sorumluluk:** Belirli zamanlarda veya aralıklarda özel görevlerin çalıştırılması.
- **Özellikler:**
    - Cron benzeri görev zamanlama.
    - Tek seferlik veya tekrarlayan görevler tanımlama.
    - Sistem bakımı, rapor oluşturma gibi görevleri otomatize etme.

### 3. AI Assistant (`ai_assistant.py`)
- **Sorumluluk:** Doğal dil komutlarını anlayan ve yürüten bir yapay zeka asistanı.
- **Özellikler:**
    - "Sistemin durumunu raporla" veya "Belgelerimi yedekle" gibi komutları işleme.
    - Harici AI servisleri (OpenAI, vb.) ile entegrasyon.
    - Sistem hakkında bilgi sağlama ve basit görevleri yerine getirme.
