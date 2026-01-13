#Requires -Version 5.1
#Requires -PSEdition Desktop

# NEXUS-ONE Autonomous Production System
# Version 2.3 - Structural Fix

# --- CONFIGURATION ---
$Global:IntervalSeconds = 15
$Global:MaxRetries = 5
$Global:PythonExecutable = "python.exe"
$Global:LogDirectory = Join-Path $PSScriptRoot "nexus_logs"
$Global:NexusScripts = @(
    "nexus_advanced_features.py",
    "nexus_auto_healer.py",
    "nexus_super_learner.py"
)

# --- SCRIPT-LEVEL STATE ---
$script:StartTime = $null
$script:LoopCounter = 0
$script:IsShuttingDown = $false

# --- INITIALIZATION & LOGGING ---

function Initialize-Logging {
    if (-not (Test-Path $Global:LogDirectory)) {
        try {
            New-Item -Path $Global:LogDirectory -ItemType Directory -ErrorAction Stop | Out-Null
        }
        catch {
            Write-Host "[ERROR] Log dizini oluşturulamadı: $Global:LogDirectory. Betik durduruluyor." -ForegroundColor Red
            exit 1
        }
    }
}

function Write-AdvLog {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$Component = "CORE"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logFile = Join-Path $Global:LogDirectory "prod_$(Get-Date -f 'yyyy-MM-dd').log"
    
    $logEntry = "[$timestamp] [$Level] [$Component] :: $Message"
    
    $color = switch ($Level) {
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "SUCCESS" { "Green" }
        "DEBUG" { "Gray" }
        default { "White" }
    }
    
    Write-Host $logEntry -ForegroundColor $color
    
    try {
        Add-Content -Path $logFile -Value $logEntry -Encoding UTF8 -ErrorAction Stop
    }
    catch {
        Write-Host "[$timestamp] [ERROR] [LOGGING] :: Log dosyasına yazılamadı: $logFile. Hata: $_" -ForegroundColor Red
    }
}

# --- SYSTEM & HEALTH CHECKS ---

function Get-PerformanceMetrics {
    $cpu = Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
    $mem = Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object @{Name = "Used"; Expression = { (($_.TotalVisibleMemorySize - $_.FreePhysicalMemory) * 100) / $_.TotalVisibleMemorySize } }
    $uptime = (Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
    
    return @{
        CPU_Load     = [math]::Round($cpu, 2)
        Memory_Usage = [math]::Round($mem.Used, 2)
        Uptime_Hours = [math]::Round($uptime.TotalHours, 1)
    }
}

function Test-SystemHealth {
    Write-AdvLog "Sistem sağlık kontrolü yapılıyor..." "DEBUG" "HEALTH"
    $perf = Get-PerformanceMetrics
    
    $status = "SAĞLIKLI"
    $level = "SUCCESS"
    
    if ($perf.CPU_Load -gt 90) {
        $status = "UYARI: Yüksek CPU kullanımı"
        $level = "WARNING"
    }
    if ($perf.Memory_Usage -gt 85) {
        $status = "UYARI: Yüksek Bellek kullanımı"
        $level = "WARNING"
    }
    
    Write-AdvLog "Sağlık durumu: $status (CPU: $($perf.CPU_Load)%, Bellek: $($perf.Memory_Usage)%)" $level "HEALTH"
    return $perf # Return performance data for logging
}

# --- CORE TASK INVOCATION ---

function Invoke-GitSync {
    $syncScriptPath = Join-Path $PSScriptRoot "autonomous_sync_v2.ps1"
    Write-AdvLog "Git senkronizasyonu başlatılıyor..." "INFO" "GIT"
    
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
        $processInfo.FileName = $Global:PythonExecutable
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
    
    Write-AdvLog "Otonom görevler yürütülüyor..." "INFO" "TASK_RUNNER"
    $results = [ordered]@{
    }
    
    # Nexus Advanced Features
    $results['AdvancedFeatures'] = Invoke-PythonScript -ScriptName "nexus_advanced_features.py"
    
    # Nexus Auto Healer (every 3 cycles)
    if (($CycleCount % 3) -eq 0) {
        $results['AutoHealer'] = Invoke-PythonScript -ScriptName "nexus_auto_healer.py"
    }
    
    # Nexus Super Learner (every 5 cycles, with special args)
    if (($CycleCount % 5) -eq 0) {
        $results['SuperLearner'] = Invoke-PythonScript -ScriptName "nexus_super_learner.py" -Arguments "--mode=aggressive --include-nexus"
    }
    
    Write-AdvLog "Tüm otonom görevler tamamlandı." "INFO" "TASK_RUNNER"
    return $results
}

# --- SHUTDOWN HANDLING ---

function Register-ShutdownHandler {
    $action = {
        if (-not $script:IsShuttingDown) {
            $script:IsShuttingDown = $true
            Write-AdvLog "KAPATMA SİNYALİ ALINDI. Sistem nazikçe durduruluyor..." "WARNING" "SYSTEM"
            $elapsed = (Get-Date) - $script:StartTime
            Write-AdvLog "Oturum süresi: $([math]::Round($elapsed.TotalMinutes, 2)) dakika. Toplam döngü: $script:LoopCounter" "INFO" "SYSTEM"
            Write-AdvLog "================================================" "INFO" "SYSTEM"
        }
    }
    
    # Register for Ctrl+C only in an interactive console
    if (-not [System.Console]::IsInputRedirected) {
        try {
            [Console]::TreatControlCAsInput = $false
            [Console]::CancelKeyPress += {
                param([object]$sender, [System.ConsoleCancelEventArgs]$eventArgs)
                $eventArgs.Cancel = $true # Prevent immediate termination
                & $action
            }
            Write-AdvLog "Etkileşimli kapatma (Ctrl+C) işleyicisi kaydedildi." "DEBUG" "SYSTEM"
        }
        catch {
            Write-AdvLog "Etkileşimli kapatma işleyicisi kaydedilemedi: $_" "WARNING" "SYSTEM"
        }
    }
    else {
        Write-AdvLog "Etkileşimli olmayan oturum, Ctrl+C işleyicisi atlanıyor." "DEBUG" "SYSTEM"
    }
    
    # Register for process termination (more reliable)
    Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $action | Out-Null
    Write-AdvLog "Motor 'Exiting' olayı işleyicisi kaydedildi." "DEBUG" "SYSTEM"
}

# --- MAIN CONTROL LOOP ---
try {
    # Initialization
    Initialize-Logging
    $script:StartTime = Get-Date
    $script:LoopCounter = 0
    
    Write-AdvLog "================================================" "INFO" "SYSTEM"
    Write-AdvLog "NEXUS-ONE Otonom Üretim Sistemi v2.3 Başlatıldı" "SUCCESS" "SYSTEM"
    Write-AdvLog "================================================" "INFO" "SYSTEM"
    
    Register-ShutdownHandler
    
    while ($true) {
        if ($script:IsShuttingDown) { break }
        
        $script:LoopCounter++
        Write-AdvLog "`n--- Döngü #$($script:LoopCounter) [$($(Get-Date).ToString('HH:mm:ss'))] ---" "INFO" "CYCLE"
        
        try {
            $perf = Test-SystemHealth
            $syncResult = Invoke-GitSync
            
            if (-not $syncResult) {
                Write-AdvLog "Senkronizasyon başarısız, görevler atlanıyor" "WARNING" "CYCLE"
                Start-Sleep -Seconds $Global:IntervalSeconds
                continue
            }
            
            $taskResults = Invoke-AutonomousTasks -CycleCount $script:LoopCounter
            
            $errorCount = ($taskResults.Values | Where-Object { $_ -eq $false }).Count
            if ($errorCount -gt 1) {
                # [math]::Min kullanımı için iki değerin de double/decimal olması güvenlidir
                $val1 = [double]($Global:IntervalSeconds * 2)
                $val2 = [double]300
                $adjustedInterval = [int][math]::Min($val1, $val2)
                
                Write-AdvLog "Çok sayıda hata, interval $adjustedInterval saniyeye ayarlandı" "WARNING" "CYCLE"
                Start-Sleep -Seconds $adjustedInterval
            }
            else {
                Start-Sleep -Seconds $Global:IntervalSeconds
            }
        }
        catch {
            Write-AdvLog "Ana döngüde beklenmedik hata: $_" "ERROR" "CYCLE"
            
            # Üstel backoff hesaplaması: 2^n. n değeri MaxRetries'i geçmesin.
            $exponent = [math]::Min([double]$script:LoopCounter, [double]$Global:MaxRetries)
            $backoffRaw = [math]::Pow([double]2, [double]$exponent)
            $backoffTime = [int][math]::Min($backoffRaw, [double]60) # Max 60s
            
            Write-AdvLog "Kritik hata sonrası toparlanma için $backoffTime saniye bekleniyor..." "WARNING" "CYCLE"
            Start-Sleep -Seconds $backoffTime
        }
    }
}
catch {
    # This top-level catch is for catastrophic startup failures
    # The Write-AdvLog might not be available if initialization failed, so we have a fallback.
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $fallbackMessage = "[$timestamp] [FATAL] [SYSTEM] :: Betik başlatılamadı. Kritik hata: $_"
    Write-Host $fallbackMessage -ForegroundColor Red
    
    # Try to log to a file as a last resort
    try {
        $logDir = Join-Path $PSScriptRoot "nexus_logs"
        if (-not (Test-Path $logDir)) { New-Item -Path $logDir -ItemType Directory | Out-Null }
        $logFile = Join-Path $logDir "fatal_error.log"
        Add-Content -Path $logFile -Value $fallbackMessage -Encoding UTF8
    }
    catch {}
    
    exit 1
}
finally {
    if ($script:IsShuttingDown) {
        Write-AdvLog "NEXUS-ONE başarıyla durduruldu." "SUCCESS" "SYSTEM"
    }
}