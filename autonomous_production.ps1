#Requires -Version 5.1
#Requires -PSEdition Desktop

param(
    [int]$IntervalSeconds = 30,
    [bool]$EnableParallelOps = $true,
    [bool]$EnableSmartCommit = $true,
    [int]$MaxRetries = 3
)

# NEXUS-ONE Advanced Autonomous System - Production Ready v2.3 (FIXED)
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# Logging & Paths
$LogPath = Join-Path $PSScriptRoot "nexus_logs\autonomous_$(Get-Date -Format 'yyyy-MM-dd').log"
$ErrorLogPath = Join-Path $PSScriptRoot "nexus_logs\errors_$(Get-Date -Format 'yyyy-MM-dd').log"

# --- FONKSİYONLAR ---

function Initialize-Logging {
    if (-not (Test-Path (Join-Path $PSScriptRoot "nexus_logs"))) { 
        New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot "nexus_logs") -Force | Out-Null 
    }
    Get-ChildItem (Join-Path $PSScriptRoot "nexus_logs") -Filter "*.log" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | 
    Remove-Item -Force -ErrorAction SilentlyContinue
}

function Write-AdvLog {
    param([string]$Message, [string]$Level = "INFO", [string]$Module = "CORE")
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    $logMsg = "[$time] [$Level] [$Module] $Message"
    
    switch ($Level) {
        "INFO" { Write-Host $logMsg -ForegroundColor Cyan }
        "SUCCESS" { Write-Host $logMsg -ForegroundColor Green }
        "WARNING" { Write-Host $logMsg -ForegroundColor Yellow }
        "ERROR" { Write-Host $logMsg -ForegroundColor Red }
        "DEBUG" { if ($env:NEXUS_DEBUG -eq "true") { Write-Host $logMsg -ForegroundColor DarkGray } }
        default { Write-Host $logMsg -ForegroundColor White }
    }
    Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
}

function Test-SystemHealth {
    $healthStatus = [ordered]@{ "Powershell" = $PSVersionTable.PSVersion.ToString(); "Disk" = 0; "CPU" = 0 }
    try {
        $drive = $PSScriptRoot.Substring(0, 1)
        $driveInfo = Get-PSDrive -Name $drive -ErrorAction SilentlyContinue
        if ($driveInfo) { $healthStatus.Disk = [math]::Round($driveInfo.Free / 1GB, 2) }
        $cpuInfo = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue
        if ($cpuInfo) { $healthStatus.CPU = [math]::Round(($cpuInfo | Measure-Object -Property LoadPercentage -Average).Average, 2) }
    }
    catch { }
    return $healthStatus
}

function Invoke-GitSync {
    $syncScriptPath = Join-Path $PSScriptRoot "autonomous_sync_v2.ps1"
    Write-AdvLog "Gelişmiş Git senkronizasyonu başlatılıyor..." "INFO" "GIT"
    
    if (-not (Test-Path $syncScriptPath)) {
        Write-AdvLog "autonomous_sync_v2.ps1 bulunamadı. Senkronizasyon atlanıyor." "ERROR" "GIT"
        return $false
    }
    
    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "powershell.exe"
        $processInfo.Arguments = "-ExecutionPolicy Bypass -File `"$syncScriptPath`""
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        $process.Start() | Out-Null
        
        $output = $process.StandardOutput.ReadToEnd()
        $errorOutput = $process.StandardError.ReadToEnd()
        
        $process.WaitForExit()
        
        if ($output) { $output.Split("`n") | ForEach-Object { Write-AdvLog $_ "DEBUG" "GIT_SYNC" } }
        
        if ($process.ExitCode -ne 0) {
            throw "Git senkronizasyon betiği hata koduyla ($($process.ExitCode)) sonlandı. Hata: $errorOutput"
        }
        
        Write-AdvLog "Git senkronizasyonu başarıyla tamamlandı." "SUCCESS" "GIT"
        return $true
    }
    catch {
        Write-AdvLog "Git senkronizasyonu sırasında kritik hata: $_" "ERROR" "GIT"
        return $false
    }
}

function Invoke-PythonScript {
    param(
        [string]$ScriptName,
        [string]$Arguments,
        [int]$TimeoutSeconds = 120
    )
    $scriptPath = Join-Path $PSScriptRoot $ScriptName
    $componentName = ($ScriptName -split '\.')[0].ToUpper()
    
    if (-not (Test-Path $scriptPath)) {
        Write-AdvLog "$ScriptName bulunamadı." "ERROR" $componentName
        return $false
    }
    
    Write-AdvLog "$ScriptName başlatılıyor... Argümanlar: $Arguments" "INFO" $componentName
    
    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "python.exe" # Assuming python is in PATH
        $processInfo.Arguments = "`"$scriptPath`" $Arguments"
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true
        $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        $process.Start() | Out-Null
        
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            $process.Kill()
            throw "$ScriptName zaman aşımına uğradı ($($TimeoutSeconds)s). Sonlandırıldı."
        }
        
        $output = $process.StandardOutput.ReadToEnd()
        $errorOutput = $process.StandardError.ReadToEnd()
        
        if ($output) { $output.Split("`n") | ForEach-Object { if ($_.Trim()) { Write-AdvLog $_ "DEBUG" $componentName } } }
        
        if ($process.ExitCode -ne 0) {
            throw "$ScriptName hata koduyla ($($process.ExitCode)) sonlandı. Hata: $errorOutput"
        }
        
        Write-AdvLog "$ScriptName başarıyla tamamlandı." "SUCCESS" $componentName
        return $true
    }
    catch {
        Write-AdvLog "$ScriptName çalıştırılırken kritik hata: $_" "ERROR" $componentName
        return $false
    }
}

function Invoke-AutonomousTasks {
    param([int]$CycleCount)
    
    Write-AdvLog "Gerçek otonom görevler yürütülüyor..." "INFO" "TASK_RUNNER"
    $results = [ordered]@{}
    
    # Her döngüde çalışır
    $results['AdvancedFeatures'] = Invoke-PythonScript -ScriptName "nexus_advanced_features.py"
    
    # Her 3 döngüde bir çalışır
    if (($CycleCount % 3) -eq 0) {
        $results['AutoHealer'] = Invoke-PythonScript -ScriptName "nexus_auto_healer.py"
    }
    
    # Her 5 döngüde bir çalışır
    if (($CycleCount % 5) -eq 0) {
        $results['SuperLearner'] = Invoke-PythonScript -ScriptName "nexus_super_learner.py" -Arguments "--mode=aggressive --include-nexus"
    }
    
    Write-AdvLog "Tüm otonom görevler tamamlandı." "INFO" "TASK_RUNNER"
    return $results
}

function Register-ShutdownHandler {
    $cleanup = { Write-AdvLog "Sistem kapatılıyor..." "WARNING" "SHUTDOWN"; exit 0 }
    try { Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $cleanup -ErrorAction SilentlyContinue } catch {}
}

# --- ANA KONTROL DÖNGÜSÜ (TAMİRLİ KISIM) ---

try {
    Initialize-Logging
    $script:LoopCounter = 0
    $script:StartTime = Get-Date
    
    Write-AdvLog "NEXUS-ONE Başlatıldı. Döngü başlıyor..." "SUCCESS" "SYSTEM"
    Register-ShutdownHandler

    while ($true) {
        $script:LoopCounter++
        Write-AdvLog "Döngü #$($script:LoopCounter) aktif." "INFO" "CYCLE"

        try {
            $syncResult = Invoke-GitSync
            $taskResults = Invoke-AutonomousTasks -CycleCount $script:LoopCounter

            # Hata Sayısı Kontrolü
            $errorCount = ($taskResults.Values | Where-Object { $_ -eq $false }).Count
            
            if ($errorCount -gt 1) {
                # HATALI SATIRIN DÜZELTİLMİŞ HALİ:
                # [math]::Min her iki argümanı da aynı tipte (double) bekler.
                $val1 = [double]($IntervalSeconds * 2)
                $val2 = [double]300
                $wait = [int][math]::Min($val1, $val2)
                
                Write-AdvLog "Çok fazla hata! Bekleme süresi artırıldı: $wait sn" "WARNING" "CYCLE"
                Start-Sleep -Seconds $wait
            }
            else {
                Start-Sleep -Seconds $IntervalSeconds
            }
        }
        catch {
            # DÜZELTİLMİŞ ÜSTEL BEKLEME (Backoff):
            # Satır 358'deki hata buradaydı. Tip dönüşümleri eklendi.
            $exponent = [math]::Min([double]$script:LoopCounter, [double]5)
            $backoffRaw = [math]::Pow([double]2, $exponent)
            $backoffTime = [int][math]::Min($backoffRaw, [double]60)
            
            Write-AdvLog "Kritik döngü hatası: $($_.Exception.Message)" "ERROR" "CYCLE"
            Write-AdvLog "$backoffTime saniye bekleniyor..." "WARNING" "RECOVERY"
            Start-Sleep -Seconds $backoffTime
        }
    }
}
catch {
    Write-AdvLog "Sistem tamamen durdu: $_" "ERROR" "FATAL"
    exit 1
}