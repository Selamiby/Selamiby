# 📱 NEXUS: MOBILE (APK) YAYINLAMA REHBERİ

NEXUS-ONE tarafından üretilen Idle RPG oyununu bir APK'ya dönüştürmek için şu adımları izleyeceğiz:

## 1. Yöntem: Python Buildozer (Hızlı Test)
Eğer mevcut Python kodunu doğrudan APK yapmak istersen:
1. Windows Subsystem for Linux (WSL) kurulur.
2. `pip install buildozer` çalıştırılır.
3. `buildozer init` ve `buildozer android debug` komutlarıyla APK üretilir.

## 2. Yöntem: Godot Engine (Profesyonel/Ticari)
Trend olan ve "eşiz" bir mobil deneyim için Godot önerilir:
- Proje boyutu: <50MB (Senin 200MB sınırının çok altında).
- Tek tıkla Android Export.
- NEXUS, Godot için `nexus_sdk.gd` üzerinden tüm oyun dengesini (ekonomi, level) yönetebilir.

## 3. Ticari Yayınlama (Google Play & App Store)
- **Kişisel:** 25$ Google Play Developer ücreti.
- **Şirket:** Eğer gelir belli bir sınırı aşarsa şirketleşme önerilir. NEXUS tüm finansal raporları otonom hazırlayabilir.

---
**NEXUS:** Şu an masaüstü prototipi (`nexus_idle_rpg.py`) hazır. Onu çalıştırdığında karşına dikey, mobil formatta bir pencere açılacak. Bu oyunun "beyni" ve "kalbi"dir.
