#!/usr/bin/env python3
"""
File Manager Test - Tam Çalışan Test
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.file_manager import file_manager


def test_file_manager():
    """File Manager'ı test et"""

    print("\n" + "=" * 70)
    print("📁 AetherOS FILE MANAGER - TEST")
    print("=" * 70)

    # Test 1: Mevcut dizin
    print("\n[1/8] Mevcut Dizin Bilgisi")
    print("-" * 70)
    current = file_manager.get_current_directory()
    print(f"✅ Dizin: {current['path']}")
    print(f"✅ Var: {current['exists']}")

    # Test 2: Dizin içeriğini listele
    print("\n[2/8] Dizin İçeriğini Listele")
    print("-" * 70)
    contents = file_manager.list_contents(".")
    if "error" not in contents:
        print(f"✅ Toplam Dosya: {contents['files_count']}")
        print(f"✅ Toplam Dizin: {contents['directories_count']}")
        print(f"✅ Toplam Boyut: {contents['total_size_human']}")
        if contents["files"]:
            print(f"✅ İlk Dosya: {contents['files'][0]['name']}")
    else:
        print(f"⚠️ {contents['error']}")

    # Test 3: Dosya oluştur
    print("\n[3/8] Dosya Oluştur")
    print("-" * 70)
    result = file_manager.create_file(
        "test_file.txt",
        "Bu bir test dosyasıdır.\nAetherOS File Manager tarafından oluşturuldu.\n",
    )
    if result["success"]:
        print(f"✅ Dosya: {result['path']}")
        print(f"✅ Boyut: {result['size_human']}")
    else:
        print(f"❌ {result['error']}")

    # Test 4: Dosya oku
    print("\n[4/8] Dosya Oku")
    print("-" * 70)
    read_result = file_manager.read_file("test_file.txt")
    if read_result["success"]:
        print(f"✅ Dosya: {read_result['filename']}")
        print(f"✅ Satır Sayısı: {read_result['line_count']}")
        print(f"✅ İçerik:\n{read_result['content']}")
    else:
        print(f"❌ {read_result['error']}")

    # Test 5: Dosya İstatistikleri
    print("\n[5/8] Dosya İstatistikleri")
    print("-" * 70)
    stats = file_manager.get_file_stats("test_file.txt")
    if "error" not in stats:
        print(f"✅ Dosya: {stats['name']}")
        print(f"✅ Boyut: {stats['size_human']}")
        print(f"✅ MD5: {stats['hash_md5']}")
        print(f"✅ Değiştirme: {stats['modified']}")
    else:
        print(f"❌ {stats['error']}")

    # Test 6: Dosya Kopyala
    print("\n[6/8] Dosya Kopyala")
    print("-" * 70)
    copy_result = file_manager.copy_file("test_file.txt", "test_file_copy.txt")
    if copy_result["success"]:
        print(f"✅ Kaynак: {copy_result['source']}")
        print(f"✅ Hedef: {copy_result['destination']}")
    else:
        print(f"❌ {copy_result['error']}")

    # Test 7: Dizin Oluştur
    print("\n[7/8] Dizin Oluştur")
    print("-" * 70)
    dir_result = file_manager.create_directory("test_directory/sub_directory")
    if dir_result["success"]:
        print(f"✅ Dizin: {dir_result['path']}")
    else:
        print(f"❌ {dir_result['error']}")

    # Test 8: Sistem İstatistikleri
    print("\n[8/8] Sistem İstatistikleri")
    print("-" * 70)
    system_stats = file_manager.get_system_stats()
    print(f"✅ Oluşturulan Dosya: {system_stats['file_manager']['files_created']}")
    print(f"✅ Silinen Dosya: {system_stats['file_manager']['files_deleted']}")
    print(f"✅ Taşınan Dosya: {system_stats['file_manager']['files_moved']}")
    print(f"✅ Toplam İşlem: {system_stats['file_manager']['total_operations']}")
    print(f"✅ İşlem Geçmişi: {system_stats['history_count']}")

    # İşlem Geçmişi
    print("\n[BONUS] İşlem Geçmişi (Son 5)")
    print("-" * 70)
    history = file_manager.get_operation_history(5)
    for i, op in enumerate(history, 1):
        print(f"{i}. {op['action']} - {op['timestamp']}")

    print("\n" + "=" * 70)
    print("✅ TÜM TESTLER TAMAMLANDI")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        test_file_manager()
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback

        traceback.print_exc()
