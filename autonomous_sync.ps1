#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
# NEXUS-ONE Otonom Senkronizasyon Sistemi
# Projeyi sürekli otomatik olarak günceller, entegre eder ve GitHub'a sync eder

param(
    [int]$IntervalSeconds = 60,  # Her 1 dakikada çalış
    [int]$MaxRetries = 3         # Başarısızlıkta 3 kez yeniden dene
)

function Write-AutoLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $colors = @{ INFO = "Cyan"; SUCCESS = "Green"; WARNING = "Yellow"; ERROR = "Red" }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $colors[$Level]
}

function Invoke-GitPull {
    Write-AutoLog "Remote repo'dan en son değişiklikler çekiliyor..." "INFO"
    try {
        & git fetch origin main 2>$null
        & git merge origin/main --allow-unrelated-histories --no-edit 2>$null
        Write-AutoLog "Git pull başarılı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Git pull hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-GitCommit {
    try {
        $status = & git status --porcelain
        if ($status) {
            Write-AutoLog "Değişiklikler commit ediliyor..." "INFO"
            & git add . 2>$null
            $message = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Otonom entegrasyon"
            & git commit -m $message 2>$null
            Write-AutoLog "Commit başarılı" "SUCCESS"
            return $true
        }
        else {
            Write-AutoLog "Yeni değişiklik yok" "WARNING"
            return $false
        }
    }
    catch {
        Write-AutoLog "Commit hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-GitPush {
    Write-AutoLog "GitHub'a push ediliyor..." "INFO"
    try {
        & git push origin main --force 2>$null
        Write-AutoLog "Push başarılı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Push hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-AutonomousSync {
    Write-AutoLog "=== NEXUS-ONE OTONOM SENKRONIZASYON BAŞLADI ===" "INFO"
    
    $retryCount = 0
    $success = $false
    
    while ($retryCount -lt $MaxRetries -and -not $success) {
        $retryCount++
        Write-AutoLog "Deneme $retryCount/$MaxRetries" "INFO"
        
        # 1. Pull (upstream'den çek)
        if (-not (Invoke-GitPull)) {
            Write-AutoLog "Pull başarısız, sonraki döngüde tekrar denenecek" "WARNING"
            continue
        }
        
        # 2. Commit (değişiklikleri kaydet)
        if (-not (Invoke-GitCommit)) {
            Write-AutoLog "Commit başarısız, sonraki döngüde tekrar denenecek" "WARNING"
            continue
        }
        if (-not (Invoke-GitPush)) {
            Write-AutoLog "Push başarısız, sonraki döngüde tekrar denenecek" "WARNING"
            continue
        }
        
        $success = $true
        Write-AutoLog "=== SENKRONIZASYON TAMAMLANDI ===" "SUCCESS"
    }
    
    if (-not $success) {
        Write-AutoLog "Senkronizasyon başarısız oldu, sonraki döngüde yeniden denecek" "ERROR"
    }
}

# Ana döngü
Write-AutoLog "NEXUS-ONE Otonom Senkronizasyon Sistemi başlatıldı" "INFO"
Write-AutoLog "Interval: $IntervalSeconds saniye, Max Retry: $MaxRetries" "INFO"

while ($true) {
    try {
        Invoke-AutonomousSync
    }
    catch {
        Write-AutoLog "Kritik hata: $_" "ERROR"
    }
    
    Write-AutoLog "Sonraki senkronizasyon $IntervalSeconds saniye içinde yapılacak..." "INFO"
    Write-Host ""
    Start-Sleep -Seconds $IntervalSeconds
}
