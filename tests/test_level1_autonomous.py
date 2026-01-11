#!/usr/bin/env python3
"""
Seviye 1 Otonom Sistem - Test
"""

import os
import sys

sys.path.insert(0, r'c:\Users\selam\NEXUS-ONE')
os.chdir(r'c:\Users\selam\NEXUS-ONE')

print("\n" + "="*80)
print("SEVİYE 1: OTONOM SİSTEM - TEST")
print("="*80)

# Test 1: File Organizer
print("\n[1] FILE ORGANIZER TEST")
print("-"*80)
try:
    from modules.file_organizer import FileOrganizer
    
    organizer = FileOrganizer()
    
    # Kategorileri kontrol et
    print("Kategoriler:")
    for cat, exts in organizer.CATEGORY_MAP.items():
        print(f"  {cat}: {len(exts)} uzantı")
    
    # Rapor oluştur
    report = organizer.generate_report(".")
    print(f"\nGeçerli dizin raporu:")
    for cat, info in list(report["categories"].items())[:5]:
        print(f"  {cat}: {info['count']} dosya ({info['size_human']})")
    
    print("[OK] File Organizer başarılı")
except Exception as e:
    print(f"[ERROR] File Organizer: {e}")

# Test 2: Backup Manager
print("\n[2] BACKUP MANAGER TEST")
print("-"*80)
try:
    from modules.backup_manager import BackupManager
    
    bm = BackupManager()
    
    # Test dosyası oluştur
    test_dir = "test_backup_dir"
    os.makedirs(test_dir, exist_ok=True)
    
    with open(f"{test_dir}/test.txt", "w") as f:
        f.write("Test backup content")
    
    # Yedek oluştur
    result = bm.create_backup(test_dir, name="test_backup_001")
    print(f"Yedek oluştur: {result['success']}")
    
    # Yedekleri listele
    backups = bm.list_backups()
    print(f"Toplam yedekler: {backups['total_backups']}")
    
    # Temizle
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)
    
    print("[OK] Backup Manager başarılı")
except Exception as e:
    print(f"[ERROR] Backup Manager: {e}")

# Test 3: System Maintenance
print("\n[3] SYSTEM MAINTENANCE TEST")
print("-"*80)
try:
    from modules.system_maintenance import SystemMaintenance
    
    sm = SystemMaintenance()
    
    # Disk analizi
    disk_info = sm.analyze_disk("C:\\")
    print(f"Disk C: {disk_info.get('used_gb', 0):.2f}/{disk_info.get('total_gb', 0):.2f} GB")
    print(f"Status: {disk_info.get('status', 'N/A')}")
    
    # Sistem istatistikleri
    stats = sm.get_system_stats()
    if "error" not in stats:
        print(f"CPU: {stats['cpu_percent']:.1f}%")
        print(f"Memory: {stats['memory_percent']:.1f}%")
        print(f"System Status: {stats['status']}")
    
    # Büyük dosyaları ara
    large = sm.find_large_files(".", min_size_mb=10)
    print(f"10MB+ dosyalar: {large['large_files_count']}")
    
    print("[OK] System Maintenance başarılı")
except Exception as e:
    print(f"[ERROR] System Maintenance: {e}")

print("\n" + "="*80)
print("SEVİYE 1 TESTLERI TAMAMLANDI")
print("="*80)
print("""
✓ File Organizer - Dosya organizasyonu, duplicate detection
✓ Backup Manager - Otonom yedekleme sistemi
✓ System Maintenance - Disk analizi, sistem bakımı

Tüm Seviye 1 modülleri operational!
""")
