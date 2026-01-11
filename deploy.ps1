# deploy.ps1 - GERÇEK KURULUM SCRIPT'I (PowerShell Versiyonu)

# Hata durumunda script'i durdur
$ErrorActionPreference = 'Stop'

Write-Host "🚀 AETHEROS/NEXUS-ONE Deployment Started (PowerShell)" -ForegroundColor Green
Write-Host "========================================="

# 1. Proje ve kaynak dizinlerini ayarla
$ProjectDir = "$HOME\aetheros"
$SourceDir = $PSScriptRoot # Script'in çalıştığı dizin (NEXUS-ONE)

Write-Host "📁 Creating project structure in '$ProjectDir'..."
# -Force parametresi mkdir -p gibi çalışır
New-Item -Path $ProjectDir -ItemType Directory -Force | Out-Null
Set-Location -Path $ProjectDir

# Gerekli alt klasörleri oluştur
$subfolders = @("backend", "modules", "config", "logs", "backups", "data", "state")
foreach ($folder in $subfolders) {
    New-Item -Path (Join-Path $ProjectDir $folder) -ItemType Directory -Force | Out-Null
}
Write-Host "✅ Project structure created."

# 2. Python bağımlılıklarını kur
Write-Host "📦 Installing Python dependencies..."

# requirements.txt dosyasını oluştur
$requirements = @"
psutil>=5.8.0
schedule>=1.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
GPUtil>=1.4.0
python-dotenv>=1.0.0
"@
Set-Content -Path (Join-Path $ProjectDir "requirements.txt") -Value $requirements

# Bağımlılıkları pip ile kur
try {
    Write-Host "Running pip install..."
    python -m pip install -r (Join-Path $ProjectDir "requirements.txt")
    Write-Host "✅ Python dependencies installed."
}
catch {
    Write-Host "❌ Failed to install Python dependencies. Make sure Python and pip are correctly installed and in your PATH." -ForegroundColor Red
    exit 1
}


# 3. Mevcut Python dosyalarını yeni yapıya kopyala
Write-Host "🔧 Copying backend and module files..."
Copy-Item -Path (Join-Path $SourceDir "nexus_core.py") -Destination (Join-Path $ProjectDir "backend\nexus_core.py") -Force
Copy-Item -Path (Join-Path $SourceDir "system_monitor.py") -Destination (Join-Path $ProjectDir "backend\system_monitor.py") -Force
Copy-Item -Path (Join-Path $SourceDir "backup_manager.py") -Destination (Join-Path $ProjectDir "backend\backup_manager.py") -Force
Copy-Item -Path (Join-Path $SourceDir "modules\file_organizer.py") -Destination (Join-Path $ProjectDir "modules\file_organizer.py") -Force
Write-Host "✅ Core Python files copied."


# 4. Config dosyalarını oluştur
Write-Host "⚙️ Creating configuration files..."

# Ana config (nexus_config.json)
$nexusConfig = @"
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
"@
Set-Content -Path (Join-Path $ProjectDir "config\nexus_config.json") -Value $nexusConfig

# Backup config (backup_config.json)
# $HOME'u PowerShell'in anlayacağı şekilde değiştiriyoruz
$backupConfig = @"
{
    "backup_paths": [
        "$HOME\Documents",
        "$HOME\Desktop"
    ],
    "backup_destination": "$ProjectDir\backups",
    "max_backups": 10,
    "compress": true,
    "schedule": {
        "frequency": "daily",
        "time": "02:00"
    }
}
"@
Set-Content -Path (Join-Path $ProjectDir "config\backup_config.json") -Value $backupConfig
Write-Host "✅ Configuration files created."

Write-Host "🎉 Deployment script finished successfully!" -ForegroundColor Green
Write-Host "Your project is set up in: $ProjectDir"
