# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimler
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Gerekli klasörleri oluştur
RUN mkdir -p logs backups data state

# Portu aç
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Uygulamayı başlat
CMD ["python", "backend/api_server.py"]
