#!/bin/bash
# deploy.sh - GERÇEK KURULUM SCRIPT'I

set -e

echo "🚀 AETHEROS/NEXUS-ONE Deployment Started"
echo "========================================="

# 1. Bağımlılıkları kontrol et
echo "🔍 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing..."
    sudo apt-get install -y git
fi

# 2. Proje klasörünü oluştur
echo "📁 Creating project structure..."
PROJECT_DIR="$HOME/aetheros"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

mkdir -p {backend,frontend,modules,config,logs,backups,data,state}

# 3. Python bağımlılıklarını kur
echo "📦 Installing Python dependencies..."
cat > requirements.txt << 'EOF'
psutil>=5.8.0
schedule>=1.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
GPUtil>=1.4.0
python-dotenv>=1.0.0
EOF

pip3 install -r requirements.txt

# 4. Backend dosyalarını oluştur
echo "🔧 Creating backend files..."

# backup_manager.py (yukarıdaki kodu buraya kopyala)
cat > backend/backup_manager.py << 'EOF'
# Yukarıdaki backup_manager.py kodu buraya
EOF

# system_monitor.py (yukarıdaki kodu buraya kopyala)
cat > backend/system_monitor.py << 'EOF'
# Yukarıdaki system_monitor.py kodu buraya
EOF

# nexus_core.py (yukarıdaki kodu buraya kopyala)
cat > backend/nexus_core.py << 'EOF'
# Yukarıdaki nexus_core.py kodu buraya
EOF

# 5. File organizer modülü
cat > modules/file_organizer.py << 'EOF'
# Yukarıdaki file_organizer.py kodu buraya
EOF

# 6. Config dosyalarını oluştur
echo "⚙️ Creating configuration files..."

# Ana config
cat > config/nexus_config.json << 'EOF'
{
    "modules": {
        "backup_manager": {
            "enabled": true,
            "config_file": "config/backup_config.json",
            "auto_start": true
        },
        "system_monitor": {
            "enabled": true,
            "log_interval": 60,
            "auto_start": true
        },
        "file_organizer": {
            "enabled": true,
            "auto_organize": true,
            "organize_interval": 300
        }
    },
    "system": {
        "heartbeat_interval": 30,
        "auto_recover": true,
        "max_errors": 10,
        "log_level": "INFO"
    }
}
EOF

# Backup config
cat > config/backup_config.json << 'EOF'
{
    "backup_paths": [
        "$HOME/Documents",
        "$HOME
EOF
