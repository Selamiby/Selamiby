# 🔥 AetherOS File Manager - Hızlı Referans

## ⚡ 30 Saniyede Başlangıç

```python
from modules.file_manager import file_manager

# Dosya oluştur
file_manager.create_file("test.txt", "Merhaba")

# Dosya oku
content = file_manager.read_file("test.txt")

# Dosya kopyala
file_manager.copy_file("test.txt", "backup.txt")

# Dosya sil
file_manager.delete_file("test.txt")

# Ara
results = file_manager.search_files(".py", ".")
```

---

## 📌 En Çok Kullanılanlar

| İşlem | Kod |
|-------|-----|
| **Dosya Oluştur** | `file_manager.create_file("file.txt", "content")` |
| **Dosya Oku** | `file_manager.read_file("file.txt")` |
| **Dosya Sil** | `file_manager.delete_file("file.txt")` |
| **Dosya Kopyala** | `file_manager.copy_file("src.txt", "dst.txt")` |
| **Dosya Taşı** | `file_manager.move_file("old.txt", "new.txt")` |
| **Dizin Oluştur** | `file_manager.create_directory("folder")` |
| **Dosya Ara** | `file_manager.search_files(".py", ".")` |
| **Dosya Bilgi** | `file_manager.get_file_stats("file.txt")` |
| **Dizin Listele** | `file_manager.list_contents(".")` |
| **İstatistikler** | `file_manager.get_system_stats()` |

---

## 🎯 Hata Yönetimi (Built-in)

```python
result = file_manager.create_file("test.txt")

if result['success']:
    print("✅ Başarılı")
else:
    print(f"❌ Hata: {result['error']}")
```

---

## 💾 Dosya İşlemi Örnekleri

### Okuma/Yazma
```python
# Yaz
fm.create_file("data.txt", "Hello World")

# Oku
data = fm.read_file("data.txt")
print(data['content'])

# Üzerine yaz
fm.create_file("data.txt", "Updated", overwrite=True)
```

### Kopyalama/Taşıma
```python
# Kopyala
fm.copy_file("original.txt", "copy.txt")

# Taşı
fm.move_file("file.txt", "archive/file.txt")
```

### Silme
```python
# Dosya sil
fm.delete_file("temp.txt")

# Dizin sil (boş ise)
fm.delete_directory("empty_folder")

# Dizin sil (içeriyle birlikte)
fm.delete_directory("folder", recursive=True)
```

---

## 🔍 Arama

```python
# İsim ile ara
fm.search_files(".py")

# İçerikte ara
fm.search_files("TODO", search_content=True)

# Case-sensitive ara
fm.search_files("MyClass", case_sensitive=True)
```

---

## 📊 Batch İşlem

```python
# Tüm Python dosyalarını bul
result = fm.search_files(".py", ".")

# Hepsini işle
for file in result['results']['files']:
    content = fm.read_file(file['path'])
    print(f"{file['name']}: {content['line_count']} satır")
```

---

## 🎓 Gerçek Dünya Örnekleri

### Projekt Analizi
```python
# Tüm .py dosya sayısı
py_files = fm.search_files(".py", ".")
print(f"Toplam Python dosyaları: {py_files['results']['found']}")
```

### Yedekleme
```python
# Tüm .txt dosyalarını backup'a kopyala
txt_files = fm.search_files(".txt", ".")
for f in txt_files['results']['files']:
    fm.copy_file(f['path'], f"backup/{f['name']}")
```

### Log Temizleme
```python
# Tüm log dosyalarını sil
logs = fm.search_files(".log", "logs")
for log in logs['results']['files']:
    fm.delete_file(log['path'])
```

---

## ✅ Başarı Kontrolü

Tüm metodlar dict döndürür:

```python
# Başarı
{'success': True, 'message': '...', ...}

# Hata
{'success': False, 'error': '...'}
```

---

## 🚀 Performans

- **Dosya Oluştur**: <1ms
- **Dosya Oku**: <5ms (100 satır)
- **Arama**: <100ms (100 dosya)
- **Kopyala**: <10ms (1MB)

---

**Daha fazla bilgi**: `FILE_MANAGER_API.md`  
**Test script**: `python test_file_manager.py`
