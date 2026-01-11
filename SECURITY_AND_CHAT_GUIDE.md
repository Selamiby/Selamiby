# NEXUS-ONE Güvenlik ve Chat Özellikleri

## 🛡️ Savunma Odaklı Güvenlik Sistemi

### Özellikler
- **Süreç İzleme**: Şüpheli süreçler ve ağ bağlantıları (psutil)
- **Otomatik Engelleme**: Windows Firewall ile şüpheli IP'leri engeller
- **Windows Defender Entegrasyonu**: Otomatik imza güncelleme ve QuickScan
- **Akıllı Temizlik**: Temp klasörleri, tarayıcı cache, Prefetch, Recycle Bin
- **Dinamik Öğrenme**: Loglardan tehdit pattern'leri öğrenir ve blocklist günceller
- **Workspace Koruması**: Proje klasörünü otomatik hariç tutar

### Yapılandırma
Dosya: `nexus_data/security_config.json`

```json
{
  "exclude_paths": ["c:/Users/selam/NEXUS-ONE"],
  "auto_block": true,
  "learning_mode": true,
  "cleanup_enabled": true,
  "cleanup_max_age_days": 7,
  "extended_cleanup_enabled": false,
  "browser_cache_cleanup": false,
  "prefetch_cleanup": false,
  "recycle_bin_cleanup": false
}
```

**Genişletilmiş Temizlik (İsteğe Bağlı)**
- `extended_cleanup_enabled: true` - Tüm genişletilmiş temizlik modüllerini aktifleştirir
- `browser_cache_cleanup: true` - Chrome, Edge, Firefox cache temizliği
- `prefetch_cleanup: true` - Windows Prefetch temizliği (admin gerektirir)
- `recycle_bin_cleanup: true` - Geri Dönüşüm Kutusu'nu boşaltır

### Çalıştırma

**Kontrol Panelinden:**
```
"Start Security" butonu
```

**PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_security.ps1
```

**Durdurma:**
- Panel: "Stop Security" butonu
- Chat: "güvenlik durdur"

### Loglar
`nexus_logs/security.log` - Tüm güvenlik olayları ve temizlik işlemleri

---

## 💬 Gelişmiş Chat Sistemi

### Doğal Dil Desteği
Chat artık sizin gibi tüm komutları ve soruları anlayıp tepki veriyor!

### Desteklenen Komutlar

#### 🛡️ Güvenlik Komutları
- `"güvenlik başlat"` / `"security start"` → Güvenlik ajanını başlatır
- `"güvenlik durdur"` / `"stop security"` → Güvenlik ajanını durdurur
- `"defender tara"` / `"virüs tara"` → Windows Defender QuickScan başlatır
- `"tehdit göster"` / `"show threats"` → Son tehditleri listeler

#### 📊 Sistem Komutları
- `"sistem durumu"` / `"system status"` → CPU, RAM, süreç sayısı
- `"bilgi ver"` / `"durum"` → Sistem özeti

#### 🧹 Temizlik Komutları
- `"temizlik yap"` / `"cleanup"` → Temp klasörleri temizler
- `"tarayıcı temizle"` / `"browser cache clean"` → Config'de aktifse tarayıcı cache'i temizler

#### 📝 Log Komutları
- `"log göster"` → Log klasörünü açar
- `"security log göster"` → Güvenlik logunu Notepad'de açar
- `"günlük göster"` → Log görüntüleme

#### 🔧 Geliştirme Komutları
- `"format python"` / `"kod düzenle"` → Black ile Python formatlar
- `"vscode aç"` / `"editör aç"` → VS Code'u workspace ile açar

#### 🌐 Domain Yönetimi
- `"domain add https://example.com"` → Whitelist'e ekler
- `"domain remove https://example.com"` → Whitelist'ten çıkarır
- `"unsafe on"` / `"unsafe off"` → Güvensiz tarama modunu açar/kapatır
- `"open https://example.com"` → URL'yi açar (whitelist kurallarına göre)

### Fuzzy Intent Matching
Chat sistemi tam komutu bilmeseniz de amacınızı anlar:
- ✅ `"güvenliği başlat"` → Çalışır
- ✅ `"sistemin durumunu söyle"` → Çalışır
- ✅ `"temizlik işlemi yap"` → Çalışır
- ✅ `"virüs taraması başlat"` → Çalışır

### Akıllı Öneri Sistemi
Komut algılanamazsa ilgili kategorilerde öneriler sunar:
```
"güvenlik" kelimesi → Güvenlik komutlarını önerir
"log" kelimesi → Log komutlarını önerir
"sistem" kelimesi → Sistem komutlarını önerir
```

---

## 🎮 Kontrol Paneli Butonları

### Güvenlik Kontrolleri
- **Start Security** → Güvenlik ajanını başlatır
- **Stop Security** → Güvenlik ajanını durdurur
- **Open Security Logs** → security.log'u Notepad'de açar

### Diğer Özellikler
- Run Demo, Start/Stop Agent
- Open VS Code, Logs, Workspace
- Format Python (black)
- Start Task Queue
- Safe Browser (Whitelist kontrolü)

---

## 📋 Kullanım Örnekleri

### Örnek 1: Güvenlik Taraması
```
Chat: "defender tara"
Agent: Windows Defender taraması başlatıldı.
```

### Örnek 2: Sistem Durumu
```
Chat: "sistem durumu"
Agent: Sistem:
CPU: 15.2%
RAM: 45.3% (7GB / 16GB)
Süreçler: 234
```

### Örnek 3: Temizlik
```
Chat: "temizlik yap"
Agent: Temizlik başlatıldı (temp klasörleri, 7 gün+). Detaylar security.log'da.
```

### Örnek 4: Whitelist Yönetimi
```
Chat: "domain add https://stackoverflow.com"
Agent: Whitelist'e eklendi: https://stackoverflow.com
```

---

## ⚠️ Önemli Notlar

1. **Saldırı Yapılmaz**: Sistem yalnızca savunma odaklıdır. Karşı saldırı veya offensive işlemler desteklenmez.

2. **Workspace Korumalı**: Proje klasörü (`c:/Users/selam/NEXUS-ONE`) her zaman temizlik ve taramalardan hariçtir.

3. **Admin Gereklilikleri**: Bazı işlemler (Prefetch temizliği, Firewall kuralları) yönetici yetkisi gerektirir.

4. **Unsafe Browsing**: Varsayılan OFF; açarken dikkatli olun.

5. **Genişletilmiş Temizlik**: Varsayılan OFF; aktif etmek için config dosyasını düzenleyin.

---

## 🔄 Otonom Çalışma

Güvenlik ajanı sürekli çalışırken:
- **Her 5 saniye**: Süreç ve ağ izleme
- **Her 30 dakika**: Log analizi ve tehdit öğrenme
- **Her 1 saat**: Temp klasör temizliği (+ genişletilmiş temizlik aktifse)
- **Her 6 saat**: Windows Defender güncelleme ve QuickScan

---

## 📁 Dosya Yapısı

```
nexus_security.py          # Ana güvenlik ajanı
scripts/run_security.ps1   # Başlatıcı script (BelowNormal priority)
ui/human_control_panel.py  # Kontrol paneli (chat + butonlar)
nexus_data/
  security_config.json     # Güvenlik yapılandırması
  domain_whitelist.json    # Domain whitelist
  chat_config.json         # Chat yapılandırması
nexus_logs/
  security.log             # Güvenlik olayları logu
```

---

## 🚀 Hızlı Başlangıç

1. **Paneli Aç**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/run_control_panel.ps1
   ```
   veya masaüstü kısayolu

2. **Güvenliği Başlat**: "Start Security" butonuna tıkla

3. **Chat Kullan**:
   - `"sistem durumu"`
   - `"defender tara"`
   - `"log göster"`

4. **İzle**: Logları "Open Security Logs" ile kontrol et

---

## 🔮 Gelecek Özellikler (İsteğe Bağlı)

- Makine öğrenmesi tabanlı anomali tespiti
- Ağ trafiği analizi ve DPI
- Otomatik güncelleme sistemi
- Dashboard ve görselleştirme
- Email/Telegram bildirimleri

---

**Not**: Bu sistem eğitim ve kişisel koruma amaçlıdır. Profesyonel güvenlik çözümlerinin yerine geçmez.
