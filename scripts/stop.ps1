<#
.SYNOPSIS
    AETHEROS durdurma betiği.
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

$pidFile = "..\data\pid.txt"
if (-not (Test-Path $pidFile)) {
    Write-Log "PID dosyası bulunamadı. AETHEROS çalışmıyor olabilir mi?" "ERROR"
    exit 1
}

$aetherosPid = [int](Get-Content $pidFile)

if (Get-Process -Id $aetherosPid -ErrorAction SilentlyContinue) {
    Write-Log "AETHEROS durduruluyor (PID: $aetherosPid)..." "INFO"
    Stop-Process -Id $aetherosPid -Force
    # İşlemin durmasını bekle
    Start-Sleep -Seconds 2
    if (Get-Process -Id $aetherosPid -ErrorAction SilentlyContinue) {
        Write-Log "İşlem düzgün bir şekilde durmadı. Tekrar zorlanıyor..." "ERROR"
        Stop-Process -Id $aetherosPid -Force
    }
    
    Write-Log "AETHEROS durduruldu." "SUCCESS"
}
else {
    Write-Log "İşlem $pid bulunamadı." "ERROR"
}

# Temizlik
Remove-Item -Path $pidFile -ErrorAction SilentlyContinue
<#
.SYNOPSIS
    AETHEROS durdurma betiği.
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

$pidFile = "..\data\pid.txt"
if (-not (Test-Path $pidFile)) {
    Write-Log "PID dosyası bulunamadı. AETHEROS çalışmıyor olabilir mi?" "ERROR"
    exit 1
}

$aetherosPid = [int](Get-Content $pidFile)

if (Get-Process -Id $aetherosPid -ErrorAction SilentlyContinue) {
    Write-Log "AETHEROS durduruluyor (PID: $aetherosPid)..." "INFO"
    Stop-Process -Id $aetherosPid -Force
    
    # İşlemin durmasını bekle
    Start-Sleep -Seconds 2
    
    if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
        Write-Log "İşlem düzgün bir şekilde durmadı. Tekrar zorlanıyor..." "ERROR"
        Stop-Process -Id $pid -Force
    }
    
    Write-Log "AETHEROS durduruldu." "SUCCESS"
}
else {
    Write-Log "İşlem $pid bulunamadı." "ERROR"
}

# Temizlik
Remove-Item -Path $pidFile -ErrorAction SilentlyContinue
