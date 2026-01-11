
# AETHEROS güncelleme betiği

# Betiğin bulunduğu dizine geç
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $Color = @{
        "INFO"    = "Cyan"
        "SUCCESS" = "Green"
        "WARNING" = "Yellow"
        "ERROR"   = "Red"
    }
    Write-Host "[$Level] $Message" -ForegroundColor $Color[$Level]
}

# Çalışıyorsa durdur
$pidFile = "..\data\pid.txt"
if (Test-Path $pidFile) {
    $aetherosPid = [int](Get-Content $pidFile)
    if (Get-Process -Id $aetherosPid -ErrorAction SilentlyContinue) {
        Write-Log "AETHEROS durduruluyor. PID: $aetherosPid" "WARNING"
        & .\stop.ps1
    }
}

# Yapılandırmayı yedekle
Write-Log "Yapılandırma yedekleniyor..." "INFO"
$backupPath = "..\backups\config_$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
Copy-Item -Path "..\config\*" -Destination $backupPath -Recurse -Force

# Git'ten güncelle (eğer .git klasörü varsa)
if (Test-Path "..\.git") {
    Write-Log "Git deposundan son değişiklikler çekiliyor..." "INFO"
    git -C ".." pull origin main
}
else {
    Write-Log "Git deposu bulunamadı, pull işlemi atlanıyor." "WARNING"
}

# Bağımlılıkları güncelle
Write-Log "Python bağımlılıkları güncelleniyor..." "INFO"
$pythonExecutable = "C:/Users/selam/AppData/Local/Programs/Python/Python311/python.exe"
& $pythonExecutable -m pip install --upgrade pip
& $pythonExecutable -m pip install -r "..\requirements.txt"

Write-Log "Güncelleme tamamlandı. Sistemi start.ps1 ile başlatabilirsiniz." "SUCCESS"
