# AetherOS File Manager - API Dokümantasyonu

## 🔥 Tam Hazır ve Çalışır Kod

File Manager sınıfı, dosya ve dizin yönetimi için tüm işlemleri kapsar. Tüm metodlar hata yönetimi ile birlikte gelir ve Her zaman dict döndürür.

---

## 📦 Kurulum ve Kullanım

### Global Instance
```python
from modules.file_manager import file_manager

# Kullan:
result = file_manager.create_file("test.txt", "Hello")
```

### Kendi Instance
```python
from modules.file_manager import FileManager

fm = FileManager()
```

---

## 📋 Tüm Metodlar (Çalışan Kodlar)

### 1. **get_current_directory()**
```python
current = file_manager.get_current_directory()

# Döner:
{
    "path": "C:\\Users\\selam\\AetherOS",
    "exists": True,
    "is_directory": True,
    "created": "2026-01-10T22:45:00.000000",
    "modified": "2026-01-10T22:45:35.000000",
    "size": 4096
}
```

---

### 2. **list_contents(path=".", show_hidden=False)**
```python
contents = file_manager.list_contents(".")
contents = file_manager.list_contents("src", show_hidden=True)

# Döner:
{
    "path": "C:\\Users\\selam\\AetherOS",
    "parent": "C:\\Users\\selam",
    "items_found": 20,
    "directories_count": 11,
    "files_count": 9,
    "total_size": 47431,
    "total_size_human": "46.32 KB",
    "directories": [
        {
            "name": "core",
            "path": "C:\\Users\\selam\\AetherOS\\core",
            "is_file": False,
            "is_dir": True,
            "size": 0,
            "size_human": "DIR",
            "created": "2026-01-10T20:00:00.000000",
            "modified": "2026-01-10T22:45:35.000000",
            "permissions": "755",
            "extension": ""
        }
    ],
    "files": [
        {
            "name": "main.py",
            "path": "C:\\Users\\selam\\AetherOS\\main.py",
            "is_file": True,
            "is_dir": False,
            "size": 6470,
            "size_human": "6.47 KB",
            "created": "2026-01-10T20:00:00.000000",
            "modified": "2026-01-10T22:45:35.000000",
            "permissions": "644",
            "extension": ".py"
        }
    ]
}
```

---

### 3. **create_file(filename, content="", overwrite=False)**
```python
# Basit kullanım
result = file_manager.create_file("test.txt")

# İçerikle oluştur
result = file_manager.create_file("data.txt", "Merhaba Dünya")

# Var olanı üzerine yaz
result = file_manager.create_file("test.txt", "Yeni İçerik", overwrite=True)

# Döner:
{
    "success": True,
    "message": "File created: test.txt",
    "path": "C:\\Users\\selam\\AetherOS\\test.txt",
    "size": 14,
    "size_human": "14.00 B",
    "created": "2026-01-10T22:45:35.000000"
}

# Hata durumu:
{
    "success": False,
    "error": "File already exists: test.txt",
    "suggestion": "Use overwrite=True to replace",
    "filename": "test.txt"
}
```

---

### 4. **read_file(filepath, max_lines=100)**
```python
# Dosyayı oku
result = file_manager.read_file("test.txt")

# İlk 50 satırı oku
result = file_manager.read_file("large_file.txt", max_lines=50)

# Döner:
{
    "success": True,
    "filename": "test.txt",
    "path": "C:\\Users\\selam\\AetherOS\\test.txt",
    "size": 76,
    "size_human": "76.00 B",
    "line_count": 2,
    "encoding": "utf-8",
    "content": "Bu bir test dosyasıdır.\nAetherOS File Manager tarafından oluşturuldu.\n",
    "is_truncated": False,
    "lines_shown": 2
}

# Hata:
{
    "error": "File not found: test.txt"
}
```

---

### 5. **delete_file(filepath)**
```python
result = file_manager.delete_file("test.txt")

# Döner:
{
    "success": True,
    "message": "File deleted: test.txt",
    "path": "C:\\Users\\selam\\AetherOS\\test.txt"
}

# Hata:
{
    "success": False,
    "error": "File not found: test.txt"
}
```

---

### 6. **copy_file(source, destination, overwrite=False)**
```python
# Dosya kopyala
result = file_manager.copy_file("test.txt", "test_copy.txt")

# Üzerine yaz
result = file_manager.copy_file("test.txt", "test_copy.txt", overwrite=True)

# Alt dizine kopyala
result = file_manager.copy_file("test.txt", "backup/test.txt")

# Döner:
{
    "success": True,
    "message": "File copied from test.txt to test_copy.txt",
    "source": "C:\\Users\\selam\\AetherOS\\test.txt",
    "destination": "C:\\Users\\selam\\AetherOS\\test_copy.txt"
}
```

---

### 7. **move_file(source, destination, overwrite=False)**
```python
# Dosya taşı
result = file_manager.move_file("test.txt", "archive/test.txt")

# Farklı isimiyle taşı
result = file_manager.move_file("old.txt", "new.txt")

# Döner:
{
    "success": True,
    "message": "File moved from test.txt to archive/test.txt",
    "source": "C:\\Users\\selam\\AetherOS\\test.txt",
    "destination": "C:\\Users\\selam\\AetherOS\\archive\\test.txt"
}
```

---

### 8. **create_directory(dirpath)**
```python
# Dizin oluştur
result = file_manager.create_directory("my_folder")

# Alt dizinler oluştur
result = file_manager.create_directory("data/processed/results")

# Döner:
{
    "success": True,
    "message": "Directory created: my_folder",
    "path": "C:\\Users\\selam\\AetherOS\\my_folder"
}
```

---

### 9. **delete_directory(dirpath, recursive=False)**
```python
# Boş dizini sil
result = file_manager.delete_directory("empty_folder")

# İçeriyle birlikte sil
result = file_manager.delete_directory("my_folder", recursive=True)

# Döner:
{
    "success": True,
    "message": "Directory deleted: my_folder"
}

# Hata:
{
    "success": False,
    "error": "Directory not empty: my_folder"
}
```

---

### 10. **search_files(pattern, search_path=".", search_content=False, case_sensitive=False)**
```python
# İsimde ara
result = file_manager.search_files("*.py", ".")

# Tüm .txt dosyalarını ara
result = file_manager.search_files(".txt", ".")

# İçerikle ara
result = file_manager.search_files("TODO", ".", search_content=True)

# Case-sensitive ara
result = file_manager.search_files("MyClass", ".", case_sensitive=True)

# Döner:
{
    "search": {
        "pattern": "*.py",
        "path": "C:\\Users\\selam\\AetherOS",
        "search_content": False,
        "case_sensitive": False
    },
    "results": {
        "found": 3,
        "files": [
            {
                "name": "main.py",
                "path": "C:\\Users\\selam\\AetherOS\\main.py",
                "size": 6470,
                "size_human": "6.47 KB",
                "modified": "2026-01-10T22:45:35.000000",
                "extension": ".py",
                "directory": "C:\\Users\\selam\\AetherOS"
            }
        ]
    },
    "scanned": 123
}
```

---

### 11. **get_file_stats(filepath)**
```python
stats = file_manager.get_file_stats("test.txt")

# Döner:
{
    "name": "test.txt",
    "path": "C:\\Users\\selam\\AetherOS\\test.txt",
    "size": 76,
    "size_human": "76.00 B",
    "created": "2026-01-10T22:45:35.000000",
    "modified": "2026-01-10T22:45:35.000000",
    "accessed": "2026-01-10T22:45:35.000000",
    "permissions": "644",
    "hash_md5": "30a4cc4f694caaecfba6b878b9aab95f",
    "is_readonly": False
}
```

---

### 12. **get_operation_history(limit=20)**
```python
history = file_manager.get_operation_history()
history = file_manager.get_operation_history(limit=10)

# Döner:
[
    {
        "action": "create_file",
        "timestamp": "2026-01-10T22:45:35.074218",
        "details": {
            "filename": "test.txt",
            "size": 76,
            "overwrite": False
        }
    },
    {
        "action": "read_file",
        "timestamp": "2026-01-10T22:45:35.104137",
        "details": {
            "filename": "test.txt",
            "lines_read": 2
        }
    }
]
```

---

### 13. **get_system_stats()**
```python
stats = file_manager.get_system_stats()

# Döner:
{
    "file_manager": {
        "files_created": 1,
        "files_deleted": 0,
        "files_moved": 0,
        "total_operations": 5
    },
    "history_count": 5,
    "current_directory": {
        "path": "C:\\Users\\selam\\AetherOS",
        "exists": True,
        "is_directory": True,
        "created": "2026-01-10T20:00:00.000000",
        "modified": "2026-01-10T22:45:35.000000",
        "size": 40960
    }
}
```

---

## 💻 Gerçek Kullanım Örnekleri

### Proje Analizi
```python
# Projede kaç Python dosyası var?
result = file_manager.search_files(".py", ".")
print(f"Python dosyaları: {result['results']['found']}")

# Tüm .log dosyalarını sil
result = file_manager.search_files(".log", "logs")
for file in result['results']['files']:
    file_manager.delete_file(file['path'])
```

### Yedekleme
```python
# Dosyaları backup'a kopyala
result = file_manager.copy_file("main.py", "backup/main.py.bak")
if result['success']:
    print("✅ Yedek oluşturuldu")
```

### Batch İşlem
```python
# Tüm .txt dosyalarını oku
result = file_manager.search_files(".txt", ".")
for file in result['results']['files']:
    content = file_manager.read_file(file['path'])
    if content['success']:
        print(f"📄 {file['name']}: {content['line_count']} satır")
```

### Dizin Taraması
```python
# Tüm Python dosyalarını listele
contents = file_manager.list_contents(".")
py_files = [f for f in contents['files'] if f['extension'] == '.py']
print(f"Python dosyaları: {len(py_files)}")

for py_file in py_files:
    print(f"  - {py_file['name']} ({py_file['size_human']})")
```

---

## ⚡ Performans Özellikleri

- ✅ **Non-blocking**: Tüm işlemler hızlı
- ✅ **UTF-8 Support**: Türkçe karakter desteği
- ✅ **Error Handling**: Tüm hatalar otomatik yönetilir
- ✅ **History Tracking**: Son 100 işlem kaydedilir
- ✅ **Large Files**: Büyük dosyalar sorun olmaz
- ✅ **Windows/Linux**: Cross-platform uyumlu

---

## 🔒 Güvenlik

- Dosya silinmeden önce onay al
- Recursive delete için `recursive=True` kullan
- MD5 hash ile dosya bütünlüğü kontrol et

---

## 📝 Not

Tüm metodlar dict döndürür. Hata durumunda `"error"` key'i döner.

```python
# Başarı kontrolü
result = file_manager.create_file("test.txt")
if result['success']:
    print("✅ Başarılı")
else:
    print(f"❌ Hata: {result['error']}")
```

---

**Versiyon**: 1.0  
**Status**: ✅ Production Ready  
**Tarih**: 10 Ocak 2026
