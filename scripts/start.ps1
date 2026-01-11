<#
.SYNOPSIS
    AETHEROS başlatma betiği.
#>

# Betiğin bulunduğu dizine geç
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $Color = @{
        "INFO"    = "Cyan";
        "SUCCESS" = "Green";
        "ERROR"   = "Red"
    }
    Write-Host "[$Level] $Message" -ForegroundColor $Color[$Level]
}

# Zaten çalışıp çalışmadığını kontrol et
$pidFile = "..\data\pid.txt"
if (Test-Path $pidFile) {
    $procId = Get-Content $pidFile
    if (Get-Process -Id $procId -ErrorAction SilentlyContinue) {
        Write-Log "AETHEROS zaten çalışıyor (PID: $procId)" "ERROR"
        exit 1
    }
}

# Gerekli klasörleri oluştur
New-Item -ItemType Directory -Path "..\logs", "..\data", "..\backups" -ErrorAction SilentlyContinue | Out-Null

Write-Log "AETHEROS başlatılıyor..." "INFO"

# API sunucusunu arka planda başlat
$pythonExecutable = "C:/Users/selam/AppData/Local/Programs/Python/Python311/python.exe"
$scriptPath = "..\backend\api_server.py"
$process = Start-Process -FilePath $pythonExecutable -ArgumentList $scriptPath -PassThru -WindowStyle Hidden

# PID'yi kaydet
$process.Id | Out-File -FilePath $pidFile

# Sunucunun başlamasını bekle
Start-Sleep -Seconds 5

# Sunucunun çalışıp çalışmadığını kontrol et
if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
    Write-Log "AETHEROS başarıyla başlatıldı (PID: $($process.Id))" "SUCCESS"
    Write-Log "API Sunucusu: http://localhost:8000" "INFO"
    Write-Log "Dashboard: http://localhost:8000" "INFO"
    Write-Log "API Dokümanları: http://localhost:8000/api/docs" "INFO"
    Write-Log "Loglar: tail -f ..\logs\api_server.log" "INFO"
}
else {
    Write-Log "AETHEROS başlatılamadı." "ERROR"
    if (Test-Path "..\logs\startup.log") {
        Get-Content "..\logs\startup.log"
    }
    exit 1
}
