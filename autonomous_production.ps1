#Requires -Version 5.1
#Requires -PSEdition Desktop
[System.Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
[System.Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUnusedVariable', '')]
[System.Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidDefaultValueSwitchParameter', '')]
param(
    [int]$IntervalSeconds = 30,
    [bool]$EnableParallelOps = $true,
    [bool]$EnableSmartCommit = $true,
    [int]$MaxRetries = 3
)

# NEXUS-ONE Advanced Autonomous System - Production Ready v2.2
# UTF-8 encoding fix and bug fixes

# Encoding fix for PowerShell 5.1
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# Logging System
$LogPath = Join-Path $PSScriptRoot "nexus_logs\autonomous_$(Get-Date -Format 'yyyy-MM-dd').log"
$ErrorLogPath = Join-Path $PSScriptRoot "nexus_logs\errors_$(Get-Date -Format 'yyyy-MM-dd').log"

function Initialize-Logging {
    if (-not (Test-Path (Join-Path $PSScriptRoot "nexus_logs"))) { 
        New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot "nexus_logs") -Force | Out-Null 
    }
    
    # Clear old logs (keep last 7 days)
    Get-ChildItem (Join-Path $PSScriptRoot "nexus_logs") -Filter "*.log" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | 
    Remove-Item -Force -ErrorAction SilentlyContinue
}

function Write-AdvLog {
    param(
        [string]$Message, 
        [string]$Level = "INFO",
        [string]$Module = "CORE"
    )
    
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    
    # Türkçe karakter fix
    $cleanMessage = $Message
    
    $logMsg = "[$time] [$Level] [$Module] $cleanMessage"
    
    # Console output with colors
    switch ($Level) {
        "INFO" { 
            Write-Host $logMsg -ForegroundColor Cyan
            Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        "SUCCESS" { 
            Write-Host $logMsg -ForegroundColor Green
            Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        "WARNING" { 
            Write-Host $logMsg -ForegroundColor Yellow
            Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
            Add-Content -Path $ErrorLogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        "ERROR" { 
            Write-Host $logMsg -ForegroundColor Red
            Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
            Add-Content -Path $ErrorLogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        "DEBUG" { 
            if ($env:NEXUS_DEBUG -eq "true") {
                Write-Host $logMsg -ForegroundColor DarkGray
                Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
            }
        }
        default { 
            Write-Host $logMsg -ForegroundColor White
            Add-Content -Path $LogPath -Value $logMsg -Encoding UTF8 -ErrorAction SilentlyContinue
        }
    }
}

# Health Check System - FIXED
function Test-SystemHealth {
    $healthStatus = [ordered]@{
        "PowershellVersion" = $PSVersionTable.PSVersion.ToString()
        "ExecutionPolicy"   = Get-ExecutionPolicy
        "PythonAvailable"   = $false
        "GitAvailable"      = $false
        "DiskSpace"         = 0
        "MemoryUsage"       = 0
        "CPUUsage"          = 0
    }
    
    try {
        # Disk space - FIXED
        $drive = $PSScriptRoot.Substring(0, 1)
        $driveInfo = Get-PSDrive -Name $drive -ErrorAction SilentlyContinue
        if ($driveInfo) {
            $healthStatus.DiskSpace = [math]::Round($driveInfo.Free / 1GB, 2)
        }
        
        # Memory - FIXED
        $osInfo = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
        if ($osInfo) {
            $healthStatus.MemoryUsage = [math]::Round($osInfo.FreePhysicalMemory / 1MB, 2)
        }
        
        # CPU - FIXED
        $cpuInfo = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue
        if ($cpuInfo) {
            $healthStatus.CPUUsage = [math]::Round(($cpuInfo | Measure-Object -Property LoadPercentage -Average).Average, 2)
        }
        
        # Check Python - FIXED
        try {
            $pythonOutput = & python --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $healthStatus.PythonAvailable = $true
                $healthStatus.PythonVersion = ($pythonOutput -replace 'Python ', '').Trim()
            }
        }
        catch { }
        
        # Check Git - FIXED
        try {
            $gitOutput = & git --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $healthStatus.GitAvailable = $true
                $healthStatus.GitVersion = ($gitOutput -replace 'git version ', '').Trim()
            }
        }
        catch { }
        
    }
    catch {
        Write-AdvLog "Health check error: $_" "WARNING" "SYSTEM"
    }
    
    return $healthStatus
}

# Ana senkronizasyon döngüsü
function Invoke-GitSync {
    param(
        [int]$RetryCount = 0,
        [string]$SyncScript = "autonomous_sync_v2.ps1"
    )
    
    Write-AdvLog "Gelişmiş senkronizasyon (v2) başlatılıyor..." "INFO" "GIT-SYNC"
    
    # Script varlık kontrolü
    if (-not (Test-Path $SyncScript)) {
        Write-AdvLog "Senkronizasyon script'i bulunamadı: $SyncScript" "ERROR" "GIT-SYNC"
        
        # Fallback: Basic git operations
        try {
            Write-AdvLog "Fallback: Temel Git operasyonları başlatılıyor..." "WARNING" "GIT-SYNC"
            
            # Check git status
            $status = & git status --porcelain 2>$null
            if ($LASTEXITCODE -ne 0) {
                throw "Git komutu çalıştırılamadı"
            }
            
            if ($status) {
                # Stage changes
                & git add . 2>$null
                if ($LASTEXITCODE -eq 0) {
                    # Commit with auto message
                    $commitMsg = "NEXUS-AUTO: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Otonom güncelleme"
                    & git commit -m $commitMsg 2>$null
                    
                    if ($LASTEXITCODE -eq 0) {
                        # Push to remote
                        & git push 2>$null
                        if ($LASTEXITCODE -eq 0) {
                            Write-AdvLog "Fallback senkronizasyon başarılı" "SUCCESS" "GIT-SYNC"
                            return $true
                        }
                    }
                }
            }
            else {
                Write-AdvLog "Değişiklik yok, senkronizasyon atlanıyor" "INFO" "GIT-SYNC"
                return $true
            }
            
        }
        catch {
            Write-AdvLog "Fallback senkronizasyon başarısız: $_" "ERROR" "GIT-SYNC"
            return $false
        }
        
        return $false
    }
    
    try {
        # v2 script'i çalıştır
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "powershell.exe"
        $processInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$SyncScript`" -IntervalSeconds 10"
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true
        $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        $process.Start() | Out-Null
        
        $stdout = $process.StandardOutput.ReadToEnd()
        $stderr = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        
        $exitCode = $process.ExitCode
        
        if ($exitCode -eq 0) {
            Write-AdvLog "v2 senkronizasyonu başarıyla tamamlandı." "SUCCESS" "GIT-SYNC"
            if ($stdout) {
                $stdout.Split("`n") | ForEach-Object {
                    if ($_.Trim()) {
                        Write-AdvLog "v2: $($_.Trim())" "DEBUG" "GIT-SYNC"
                    }
                }
            }
            return $true
        }
        else {
            Write-AdvLog "v2 senkronizasyonunda hata oluştu. ExitCode: $exitCode" "ERROR" "GIT-SYNC"
            if ($stderr) {
                $stderr.Split("`n") | ForEach-Object {
                    if ($_.Trim()) {
                        Write-AdvLog "v2 Hata: $($_.Trim())" "ERROR" "GIT-SYNC"
                    }
                }
            }
            
            # Retry logic
            if ($RetryCount -lt $MaxRetries) {
                Write-AdvLog "Tekrar denenecek ($($RetryCount+1)/$MaxRetries)..." "WARNING" "GIT-SYNC"
                Start-Sleep -Seconds (5 * ($RetryCount + 1))
                return Invoke-GitSync -RetryCount ($RetryCount + 1) -SyncScript $SyncScript
            }
            
            return $false
        }
    }
    catch {
        Write-AdvLog "v2 senkronizasyon betiği çalıştırılamadı: $_" "ERROR" "GIT-SYNC"
        
        if ($RetryCount -lt $MaxRetries) {
            Write-AdvLog "Tekrar denenecek ($($RetryCount+1)/$MaxRetries)..." "WARNING" "GIT-SYNC"
            Start-Sleep -Seconds (5 * ($RetryCount + 1))
            return Invoke-GitSync -RetryCount ($RetryCount + 1) -SyncScript $SyncScript
        }
        
        return $false
    }
}

# === NEXUS-ONE AUTO HEALER HOOK ===
function Invoke-NEXUSHealer {
    Write-AdvLog "NEXUS Auto Healer kontrolü..." "INFO" "AUTO-HEALER"
    
    $healerScript = "nexus_auto_healer.py"
    if (Test-Path $healerScript) {
        try {
            Write-AdvLog "NEXUS Auto Healer çalıştırılıyor..." "INFO" "AUTO-HEALER"
            
            # Run with timeout to prevent hanging
            $processInfo = New-Object System.Diagnostics.ProcessStartInfo
            $processInfo.FileName = "python.exe"
            $processInfo.Arguments = "`"$healerScript`""
            $processInfo.RedirectStandardOutput = $true
            $processInfo.RedirectStandardError = $true
            $processInfo.UseShellExecute = $false
            $processInfo.CreateNoWindow = $true
            $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
            $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
            
            $process = New-Object System.Diagnostics.Process
            $process.StartInfo = $processInfo
            $process.Start() | Out-Null
            
            # Timeout after 30 seconds
            if (-not $process.WaitForExit(30000)) {
                $process.Kill()
                Write-AdvLog "Auto Healer timeout (30s) - killed" "WARNING" "AUTO-HEALER"
                return $false
            }
            
            $output = $process.StandardOutput.ReadToEnd()
            $errorOutput = $process.StandardError.ReadToEnd()
            
            if ($process.ExitCode -eq 0) {
                if ($output) {
                    Write-AdvLog "Auto Healer çıktısı: $output" "DEBUG" "AUTO-HEALER"
                }
                Write-AdvLog "Auto Healer başarıyla tamamlandı" "SUCCESS" "AUTO-HEALER"
                return $true
            }
            else {
                Write-AdvLog "Auto Healer hata kodu: $($process.ExitCode)" "ERROR" "AUTO-HEALER"
                if ($errorOutput) {
                    Write-AdvLog "Auto Healer hata: $errorOutput" "ERROR" "AUTO-HEALER"
                }
                return $false
            }
        }
        catch {
            Write-AdvLog "Auto Healer çalıştırılamadı: $_" "ERROR" "AUTO-HEALER"
            return $false
        }
    }
    else {
        Write-AdvLog "Auto Healer script'i bulunamadı: $healerScript" "WARNING" "AUTO-HEALER"
        return $false
    }
}

# === NEXUS-ONE ADVANCED FEATURES HOOK ===
function Invoke-AdvancedFeatures {
    param([int]$CycleCount)
    
    if (($CycleCount % 5) -eq 0 -and $CycleCount -gt 0) {
        Write-AdvLog "Advanced features kontrolü..." "INFO" "ADV-FEATURES"
        
        $featureScript = "nexus_advanced_features.py"
        if (Test-Path $featureScript) {
            try {
                Write-AdvLog "Advanced features çalıştırılıyor..." "INFO" "ADV-FEATURES"
                
                # Python process'i düzgün çalıştırma - FIXED
                $processInfo = New-Object System.Diagnostics.ProcessStartInfo
                $processInfo.FileName = "python.exe"
                $processInfo.Arguments = "`"$featureScript`""
                $processInfo.RedirectStandardOutput = $true
                $processInfo.RedirectStandardError = $true
                $processInfo.UseShellExecute = $false
                $processInfo.CreateNoWindow = $true
                $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
                $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
                
                $process = New-Object System.Diagnostics.Process
                $process.StartInfo = $processInfo
                $process.Start() | Out-Null
                
                # Timeout after 45 seconds
                if (-not $process.WaitForExit(45000)) {
                    $process.Kill()
                    Write-AdvLog "Advanced features timeout (45s)" "WARNING" "ADV-FEATURES"
                    return $false
                }
                
                $output = $process.StandardOutput.ReadToEnd()
                $errorOutput = $process.StandardError.ReadToEnd()
                
                if ($process.ExitCode -eq 0) {
                    Write-AdvLog "Advanced features tamamlandı" "SUCCESS" "ADV-FEATURES"
                    return $true
                }
                else {
                    Write-AdvLog "Advanced features hata kodu: $($process.ExitCode)" "ERROR" "ADV-FEATURES"
                    if ($errorOutput) {
                        $errorOutput.Split("`n") | Select-Object -First 3 | ForEach-Object {
                            if ($_.Trim()) {
                                Write-AdvLog "Feature Error: $_" "ERROR" "ADV-FEATURES"
                            }
                        }
                    }
                    return $false
                }
            }
            catch {
                Write-AdvLog "Advanced features çalıştırılamadı: $_" "ERROR" "ADV-FEATURES"
                return $false
            }
        }
        else {
            Write-AdvLog "Advanced features script'i bulunamadı" "WARNING" "ADV-FEATURES"
            return $false
        }
    }
    return $true
}

# === NEXUS-ONE SUPER LEARNER HOOK ===
function Invoke-SuperLearner {
    param([int]$CycleCount)
    
    if (($CycleCount % 10) -eq 0 -and $CycleCount -gt 0) {
        Write-AdvLog "Super Learner kontrolü..." "INFO" "SUPER-LEARNER"
        
        $learnerScript = "nexus_super_learner.py"
        if (Test-Path $learnerScript) {
            try {
                Write-AdvLog "Super Learner çalıştırılıyor..." "INFO" "SUPER-LEARNER"
                
                # Process with proper arguments
                $processInfo = New-Object System.Diagnostics.ProcessStartInfo
                $processInfo.FileName = "python.exe"
                $processInfo.Arguments = "`"$learnerScript`" --include-nexus"
                $processInfo.RedirectStandardOutput = $true
                $processInfo.RedirectStandardError = $true
                $processInfo.UseShellExecute = $false
                $processInfo.CreateNoWindow = $true
                $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
                $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
                
                $process = New-Object System.Diagnostics.Process
                $process.StartInfo = $processInfo
                $process.Start() | Out-Null
                
                # Timeout after 60 seconds
                if (-not $process.WaitForExit(60000)) {
                    $process.Kill()
                    Write-AdvLog "Super Learner timeout (60s)" "WARNING" "SUPER-LEARNER"
                    return $false
                }
                
                $output = $process.StandardOutput.ReadToEnd()
                $errorOutput = $process.StandardError.ReadToEnd()
                
                if ($process.ExitCode -eq 0) {
                    if ($output) {
                        Write-AdvLog "Enhanced learning tamamlandı" "SUCCESS" "SUPER-LEARNER"
                        # Log first few lines
                        $output.Split("`n")[0..2] | ForEach-Object {
                            if ($_.Trim()) {
                                Write-AdvLog "Learning: $($_.Trim())" "DEBUG" "SUPER-LEARNER"
                            }
                        }
                    }
                    return $true
                }
                else {
                    Write-AdvLog "Super Learner hata kodu: $($process.ExitCode)" "ERROR" "SUPER-LEARNER"
                    if ($errorOutput) {
                        $errorOutput.Split("`n") | Select-Object -First 3 | ForEach-Object {
                            if ($_.Trim()) {
                                Write-AdvLog "Learning Error: $_" "ERROR" "SUPER-LEARNER"
                            }
                        }
                    }
                    return $false
                }
            }
            catch {
                Write-AdvLog "Super Learner çalıştırılamadı: $_" "ERROR" "SUPER-LEARNER"
                return $false
            }
        }
        else {
            Write-AdvLog "Super Learner script'i bulunamadı" "WARNING" "SUPER-LEARNER"
            return $false
        }
    }
    return $true
}

# Gerçekçi otonom görevler
function Invoke-AutonomousTasks {
    param([int]$CycleCount)
    
    Write-AdvLog "Otonom görevler başlıyor (Cycle: $CycleCount)..." "INFO" "TASK-RUNNER"
    
    $taskResults = @{
        "AutoHealer"       = $false
        "AdvancedFeatures" = $false
        "SuperLearner"     = $false
    }
    
    # Görev 1: NEXUS-ONE Auto Healer
    $taskResults.AutoHealer = Invoke-NEXUSHealer
    
    # Görev 2: Gelişmiş Özellikler
    $taskResults.AdvancedFeatures = Invoke-AdvancedFeatures -CycleCount $CycleCount
    
    # Görev 3: Süper Öğrenici
    $taskResults.SuperLearner = Invoke-SuperLearner -CycleCount $CycleCount
    
    # Rapor
    $successCount = ($taskResults.Values | Where-Object { $_ -eq $true }).Count
    $totalCount = $taskResults.Values.Count
    
    Write-AdvLog "Görev sonuçları: $successCount/$totalCount başarılı" "INFO" "TASK-RUNNER"
    
    return $taskResults
}

# Performans Monitor - FIXED VERSION
function Get-PerformanceMetrics {
    $metrics = @{
        "Cycle"     = $script:LoopCounter
        "Timestamp" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "Memory_MB" = 0
        "CPU_Time"  = 0
        "Threads"   = 1
        "Uptime"    = 0
    }
    
    try {
        # Get current process
        $currentProcess = Get-Process -Id $PID -ErrorAction SilentlyContinue
        
        if ($currentProcess) {
            # Memory in MB - FIXED Round method
            $memoryMB = $currentProcess.WorkingSet64 / 1MB
            $metrics.Memory_MB = [math]::Round($memoryMB, 2)
            
            # CPU Time - FIXED
            $metrics.CPU_Time = [math]::Round($currentProcess.TotalProcessorTime.TotalSeconds, 2)
            
            # Threads
            $metrics.Threads = $currentProcess.Threads.Count
        }
        
        # Uptime - FIXED
        $uptimeMinutes = 0
        if ($script:StartTime) {
            $uptimeMinutes = [math]::Round(((Get-Date) - $script:StartTime).TotalMinutes, 2)
        }
        $metrics.Uptime = $uptimeMinutes
        
    }
    catch {
        Write-AdvLog "Performance metrics error: $_" "WARNING" "PERFORMANCE"
    }
    
    return $metrics
}

# Graceful Shutdown Handler
function Register-ShutdownHandler {
    # Cleanup function
    $cleanupScript = {
        Write-AdvLog "Shutdown signal alındı, temizlik yapılıyor..." "WARNING" "SHUTDOWN"
        
        # Save state if needed
        $state = @{
            LastCycle    = $script:LoopCounter
            LastRun      = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            HealthStatus = Test-SystemHealth
        }
        
        $state | ConvertTo-Json | Out-File "nexus_state.json" -Encoding UTF8
        
        Write-AdvLog "NEXUS-ONE güvenli şekilde durduruldu. Toplam döngü: $($script:LoopCounter)" "SUCCESS" "SHUTDOWN"
        exit 0
    }
    
    # Register for termination events
    try {
        Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $cleanupScript
    }
    catch {
        Write-AdvLog "Shutdown handler registration failed: $_" "WARNING" "SYSTEM"
    }
}

# Ana Kontrol Döngüsü
try {
    # Initialization
    Initialize-Logging
    $script:StartTime = Get-Date
    $script:LoopCounter = 0
    
    Write-AdvLog "================================================" "INFO" "SYSTEM"
    Write-AdvLog "NEXUS-ONE Otonom Üretim Sistemi v2.2 Başlatıldı" "SUCCESS" "SYSTEM"
    Write-AdvLog "Başlangıç Zamanı: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "INFO" "SYSTEM"
    Write-AdvLog "Interval: $IntervalSeconds saniye" "INFO" "SYSTEM"
    Write-AdvLog "Max Retries: $MaxRetries" "INFO" "SYSTEM"
    Write-AdvLog "Parallel Ops: $EnableParallelOps" "INFO" "SYSTEM"
    Write-AdvLog "================================================" "INFO" "SYSTEM"
    
    # Health check
    $health = Test-SystemHealth
    Write-AdvLog "Sistem Sağlık Kontrolü:" "INFO" "SYSTEM"
    $health.GetEnumerator() | ForEach-Object {
        Write-AdvLog "  $($_.Key): $($_.Value)" "INFO" "SYSTEM"
    }
    
    # Register shutdown handler
    Register-ShutdownHandler
    
    # Main loop
    while ($true) {
        $script:LoopCounter++
        
        Write-AdvLog "`n--- Döngü #$($script:LoopCounter) [$($(Get-Date).ToString('HH:mm:ss'))] ---" "INFO" "CYCLE"
        
        try {
            # 1. Performance metrics - FIXED
            $perf = Get-PerformanceMetrics
            if ($perf) {
                Write-AdvLog "Performans: Memory=$($perf.Memory_MB)MB, CPU=$($perf.CPU_Time)s, Uptime=$($perf.Uptime)m" "DEBUG" "PERFORMANCE"
            }
            
            # 2. Git Senkronizasyonu
            $syncResult = Invoke-GitSync
            if (-not $syncResult) {
                Write-AdvLog "Senkronizasyon başarısız, görevler atlanıyor" "WARNING" "CYCLE"
                continue
            }
            
            # 3. Otonom Görevler
            $taskResults = Invoke-AutonomousTasks -CycleCount $script:LoopCounter
            
            # 4. Cycle summary
            Write-AdvLog "Döngü #$($script:LoopCounter) tamamlandı. $IntervalSeconds saniye bekleniyor..." "INFO" "CYCLE"
            
            # 5. Adaptive interval (slow down if errors)
            $errorCount = ($taskResults.Values | Where-Object { $_ -eq $false }).Count
            if ($errorCount -gt 1) {
                $adjustedInterval = [math]::Min($IntervalSeconds * 2, 300) # Max 5 minutes
                Write-AdvLog "Çok sayıda hata, interval $adjustedInterval saniyeye ayarlandı" "WARNING" "CYCLE"
                Start-Sleep -Seconds $adjustedInterval
            }
            else {
                Start-Sleep -Seconds $IntervalSeconds
            }
            
        }
        catch {
            Write-AdvLog "Döngü hatası: $_" "ERROR" "CYCLE"
            Write-AdvLog "Stack Trace: $($_.ScriptStackTrace)" "ERROR" "CYCLE"
            
            # Exponential backoff on critical errors - FIXED calculation
            $backoffTime = [math]::Min([math]::Pow(2, [math]::Min($script:LoopCounter, 5)), 60)
            Write-AdvLog "Kritik hata, $backoffTime saniye bekleniyor..." "WARNING" "CYCLE"
            Start-Sleep -Seconds $backoffTime
        }
    }
}
catch {
    Write-AdvLog "Sistem başlatma hatası: $_" "ERROR" "SYSTEM"
    Write-AdvLog "Program sonlandırılıyor..." "ERROR" "SYSTEM"
    exit 1
}