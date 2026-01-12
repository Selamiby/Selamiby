# 🎯 NEXUS GERÇEK ASSET ÜRETİCİ - KULLANIM KILAVUZU

## ✅ ÇALIŞAN ÖZELLİKLER (Simülasyon YOK!)

### 1. **Sketchfab 3D Modeller** (Ücretsiz, CC0)
```python
generator = RealAssetGenerator()
model = generator.generate_3d_model_sketchfab("sword")
# ✅ GERÇEK model bulur!
# ⚠️ İndirme: OAuth gerektirir (manuel indirme linki verir)
```

### 2. **Freesound Ses Efektleri** (Ücretsiz, CC0)
```python
sfx = generator.generate_sfx_freesound("explosion")
# ✅ GERÇEK ses indirir! (API key gerekli)
```

### 3. **Leonardo.ai Texture** (150/gün ücretsiz)
```python
texture = generator.generate_texture_leonardo("stone wall")
# ✅ GERÇEK texture üretir ve indirir!
```

### 4. **Meshy.ai 3D Model** (20 model/ay ücretsiz)
```python
model = generator.generate_3d_model_meshy("epic warrior")
# ✅ AI ile GERÇEK 3D model üretir! (2-5 dakika)
```

### 5. **ElevenLabs Ses** (10K char/ay ücretsiz)
```python
voice = generator.generate_sfx_elevenlabs("sword slash")
# ✅ AI ile GERÇEK ses üretir!
```

### 6. **Stable Diffusion Texture** (günlük limit)
```python
texture = generator.generate_texture_stable_diffusion("grass")
# ✅ AI ile GERÇEK texture üretir!
```

### 7. **MusicGen Müzik** (Tamamen ücretsiz, local)
```python
music = generator.generate_music_local_musicgen("epic battle")
# ✅ GERÇEK müzik üretir! (transformers gerekli)
```

---

## 📋 API KEY ALMA REHBERİ

### ÜCRETSIZ (Hemen başla!)

#### 1. **Freesound API** (CC0 sesler)
- Git: https://freesound.org/apiv2/apply/
- Kaydol
- "Apply for API key" tıkla
- Email'e gelen key'i .env dosyasına kopyala
- Limit: Sınırsız!

### ÜCRETLİ FREE TIER (Kredi kartı gerekir, ama ücretsiz limit var)

#### 2. **Meshy.ai** (20 model/ay ücretsiz)
- Git: https://www.meshy.ai/
- Sign up (Google/GitHub)
- Dashboard → API Keys
- Create API Key
- .env'ye kopyala
- Limit: 20 model/ay (sonra $20/ay)

#### 3. **Leonardo.ai** (150 image/gün ücretsiz)
- Git: https://leonardo.ai/
- Sign up
- User Settings → API Access
- Generate API Key
- .env'ye kopyala
- Limit: 150 token/gün (~150 görsel)

#### 4. **ElevenLabs** (10K char/ay ücretsiz)
- Git: https://elevenlabs.io/
- Sign up
- Profile → API Keys
- Create
- .env'ye kopyala
- Limit: 10,000 karakter/ay (~10 dakika ses)

#### 5. **Replicate** (günlük $0.10 ücretsiz)
- Git: https://replicate.com/
- Sign up (GitHub)
- Account → API tokens
- Create token
- .env'ye kopyala
- Limit: $0.10/gün (10 görsel)

---

## 🚀 HIZLI BAŞLANGIÇ

### 1. .env Dosyası Oluştur
```bash
cp .env.example .env
```

### 2. API Key'leri Ekle
```env
FREESOUND_API_KEY=abc123...
LEONARDO_API_KEY=xyz789...
```

### 3. Çalıştır
```bash
python nexus_real_asset_generator.py
```

---

## 📊 ÜCRETSİZ LİMİTLER

| Servis | Ücretsiz Limit | Sonrası Fiyat | Kalite |
|--------|----------------|---------------|--------|
| **Freesound** | Sınırsız | $0 | 7/10 (real recordings) |
| **Sketchfab** | Sınırsız | $0 (CC0) | 6/10 (varies) |
| **Meshy.ai** | 20 model/ay | $20/ay | 8/10 |
| **Leonardo.ai** | 150/gün | $12/ay | 9/10 |
| **ElevenLabs** | 10K char/ay | $5/ay | 9/10 |
| **Replicate** | $0.10/gün | $0.002/saniye | 8/10 |
| **MusicGen** | Sınırsız (local) | $0 | 6/10 |

---

## 💰 MALIYET HESABI

### Aylık 10 Oyun Üretimi İçin:

**Senaryö 1: Sadece Ücretsiz**
- Freesound: $0
- Sketchfab: $0
- MusicGen: $0
**Toplam: $0/ay**
**Kalite: 6/10** (hobbyist)

**Senaryö 2: Free Tier'lar**
- Freesound: $0
- Meshy.ai: 20 model ücretsiz
- Leonardo: 150 görsel/gün ücretsiz
- ElevenLabs: 10K char ücretsiz
**Toplam: $0/ay**
**Kalite: 8/10** (indie)
**Limit:** 2 oyun/ay (model limiti)

**Senaryö 3: Ücretli Plan**
- Meshy.ai: $20/ay (200 model)
- Leonardo.ai: $12/ay (unlimited)
- ElevenLabs: $5/ay (30K char)
- Suno: $10/ay (500 şarkı)
**Toplam: $47/ay**
**Kalite: 9/10** (commercial)
**Limit:** 10+ oyun/ay

---

## 🎯 ÖNERİ

**İLK HAFTA:**
1. Freesound API al (ücretsiz) ✅
2. Test et, sesler gerçekten indirilsin ✅
3. Meshy.ai kaydol (20 model ücretsiz) ✅
4. İlk 3D modelini üret ✅

**İKİNCİ HAFTA:**
5. Leonardo.ai kaydol (150/gün ücretsiz) ✅
6. Texture'ları üret ✅
7. İlk DEMO OYUN yap (gerçek assetlerle!) ✅

**ÜÇÜNCÜ HAFTA:**
8. Limitler yetmediyse ücretli planları aç ✅
9. Tam production'a geç ✅

---

## ⚠️ DİKKAT

### Mixamo Sorunu:
- Mixamo artık GitHub'da yok (404 hatası)
- Alternatif: Mixamo.com'dan manuel indir
- Veya Adobe Creative Cloud gerekiyor

### Sketchfab OAuth:
- API ile search çalışıyor ✅
- Download OAuth gerektirir
- Manuel indirme linki veriliyor (browser'da aç)

### MusicGen:
```bash
pip install transformers scipy torch
```
İlk çalıştırmada model indirecek (~500MB)

---

## 📂 ÇIKTI KLASÖRÜ

```
nexus_real_assets/
├── models_3d/          # FBX, OBJ dosyaları
├── textures/           # PNG, JPG texture'lar
├── audio/              # WAV, MP3 sesler
└── music/              # Müzik parçaları
```

**HEPSİ GERÇEK DOSYA! SİMÜLASYON YOK! ✅**
