SAFETY_RULES = {
    "max_code_length": 1000,  # Üretilecek max kod satırı
    "allowed_actions": ["read", "write_file", "api_call"],  # İzinli eylemler
    "banned_keywords": ["rm -rf", "format c:", "shutdown"],  # Yasaklı komutlar
    "backup_frequency": "hourly"  # Yedekleme sıklığı
}
