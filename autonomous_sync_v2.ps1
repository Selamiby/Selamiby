#Requires -Version 5.1
#Requires -PSEdition Desktop

# Advanced Git Synchronization Script for NEXUS-ONE
# Version 2.1 - Rebase Strategy with Force-with-Lease

param(
    [string]$Branch = "main",
    [string]$Remote = "origin",
    [int]$IntervalSeconds = 15,
    [switch]$Force,
    [switch]$NoPush
)

# --- CONFIGURATION ---
$CommitMessage = "NEXUS-AUTO: Autonomous sync and self-update"
$GitRetryCount = 2
$GitRetryDelay = 5 # seconds

# --- LOGGING ---
$LogFile = Join-Path $PSScriptRoot "nexus_logs\sync_$(Get-Date -f 'yyyy-MM-dd').log"

function Write-SyncLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    # Write to console
    $color = switch ($Level) {
        "ERROR"   { "Red" }
        "WARNING" { "Yellow" }
        "SUCCESS" { "Green" }
        default   { "Cyan" }
    }
    Write-Host $logEntry -ForegroundColor $color
    
    # Write to log file
    try {
        Add-Content -Path $LogFile -Value $logEntry -Encoding UTF8 -ErrorAction Stop
    }
    catch {
        Write-Host "[$timestamp] [ERROR] Log dosyasına yazılamadı: $LogFile" -ForegroundColor Red
    }
}

# --- CORE FUNCTIONS ---

function Invoke-GitCommand {
    param(
        [scriptblock]$Command,
        [string]$ErrorMessage
    )
    for ($i = 1; $i -le $GitRetryCount; $i++) {
        try {
            $output = & $Command 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-SyncLog "Başarılı: $($Command.ToString())"
                if ($output) {
                    $output | ForEach-Object { Write-SyncLog $_ }
                }
                return $true
            }
            else {
                throw "Komut başarısız oldu. Çıktı: $output"
            }
        }
        catch {
            Write-SyncLog "$ErrorMessage (deneme $i/$GitRetryCount): $_" "ERROR"
            if ($i -lt $GitRetryCount) {
                Start-Sleep -Seconds $GitRetryDelay
            }
        }
    }
    return $false
}

function Invoke-AdvancedSync {
    Write-SyncLog "Gelişmiş senkronizasyon başlatıldı. Uzak: $Remote, Dal: $Branch"
    
    # 1. Fetch latest changes from remote
    if (-not (Invoke-GitCommand -Command { git fetch $Remote } -ErrorMessage "Uzak sunucudan fetch edilemedi")) {
        return $false
    }
    Write-SyncLog "Uzak sunucudaki değişiklikler başarıyla fetch edildi." "SUCCESS"

    # 2. Check for local changes
    $status = git status --porcelain
    if ($status) {
        Write-SyncLog "Yerel değişiklikler tespit edildi. Commit atılıyor..."
        
        # Add all changes
        if (-not (Invoke-GitCommand -Command { git add -A } -ErrorMessage "Değişiklikler 'stage' alanına eklenemedi")) {
            return $false
        }
        
        # Commit changes
        $commitFullMessage = "$CommitMessage - $(Get-Date)"
        if (-not (Invoke-GitCommand -Command { git commit -m $commitFullMessage } -ErrorMessage "Commit atılamadı")) {
            # If commit fails (e.g., nothing to commit after add), it might not be a critical error.
            Write-SyncLog "Commit atma başarısız, muhtemelen commit atılacak yeni değişiklik yok." "WARNING"
        }
        else {
            Write-SyncLog "Yerel değişiklikler başarıyla commit'lendi." "SUCCESS"
        }
    }
    else {
        Write-SyncLog "Yerel değişiklik bulunmuyor."
    }

    # 3. Pull with rebase
    Write-SyncLog "Uzak sunucudaki değişiklikler rebase stratejisi ile pull ediliyor..."
    if (-not (Invoke-GitCommand -Command { git pull --rebase $Remote $Branch } -ErrorMessage "Rebase ile pull işlemi başarısız oldu")) {
        Write-SyncLog "Rebase işlemi sırasında çakışma olabilir. Manuel müdahale gerekebilir." "ERROR"
        # Attempt to abort rebase to return to a clean state
        Invoke-GitCommand -Command { git rebase --abort } -ErrorMessage "Rebase iptal edilemedi"
        return $false
    }
    Write-SyncLog "Rebase ile pull işlemi başarıyla tamamlandı." "SUCCESS"

    # 4. Push changes
    if ($NoPush) {
        Write-SyncLog "NoPush bayrağı aktif, push işlemi atlanıyor." "WARNING"
        return $true
    }
    
    Write-SyncLog "Değişiklikler uzak sunucuya push ediliyor (--force-with-lease)..."
    if (-not (Invoke-GitCommand -Command { git push --force-with-lease $Remote $Branch } -ErrorMessage "Push işlemi başarısız oldu")) {
        return $false
    }
    Write-SyncLog "Tüm işlemler başarıyla tamamlandı. Kod tabanı güncel." "SUCCESS"
    
    return $true
}

# --- MAIN EXECUTION ---
try {
    if (-not (Invoke-AdvancedSync)) {
        Write-SyncLog "Senkronizasyon döngüsü hatalarla sonuçlandı." "ERROR"
        exit 1
    }
    else {
        Write-SyncLog "Senkronizasyon döngüsü başarıyla tamamlandı." "SUCCESS"
        exit 0
    }
}
catch {
    Write-SyncLog "Beklenmedik bir hata oluştu: $_" "ERROR"
    exit 1
}
