import psutil

from config.config import get_config, setup_directories

# import requests # Henüz kullanılmıyor

def check_system():
    """Sistem kaynak kullanımını kontrol eder."""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    return f"CPU: {cpu}%, RAM: {memory}%"

def main():
    """
    Nexus-One Real ana çalışma fonksiyonu.
    """
    print("🚀 Nexus-One Real Başlatılıyor...")
    
    # 1. Gerekli klasör yapısını hazırla
    setup_directories()
    
    # 2. Sistem durumunu göster
    status = check_system()
    print(f"📊 Sistem Durumu: {status}")
    
    # 3. Yapılandırmayı yükle ve doğrula
    config = get_config()
    print(f"⚙️  Config Yüklendi: {config['APP_NAME']}")
    
    print("\n✅ Nexus-One hazır!")

if __name__ == "__main__":
    main()

