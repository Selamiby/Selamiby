# 🔥 NEXUS-ONE LIVE MONITOR - CANLI İZLEME PANELİ
# Durmadan güncellenecek, çalışmaları göreceksiniz!

$Host.UI.RawUI.WindowTitle = "🔥 NEXUS-ONE LIVE MONITOR - AUTONOMOUS WORK"

function Get-ColoredText {
    param($Text, $Color)
    Write-Host $Text -ForegroundColor $Color -NoNewline
}

function Show-Dashboard {
    Clear-Host
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    # Header
    Write-Host "`n" -NoNewline
    Get-ColoredText "╔════════════════════════════════════════════════════════════════════════╗`n" "Cyan"
    Get-ColoredText "║  " "Cyan"
    Get-ColoredText "🔥 NEXUS-ONE AUTONOMOUS WORK - LIVE MONITOR" "Yellow"
    Get-ColoredText "                   ║`n" "Cyan"
    Get-ColoredText "║  " "Cyan"
    Get-ColoredText "⏰ $timestamp" "White"
    Get-ColoredText "                                                          ║`n" "Cyan"
    Get-ColoredText "╚════════════════════════════════════════════════════════════════════════╝`n" "Cyan"
    
    Write-Host ""
    
    # RUNNING JOBS
    Get-ColoredText "┌─ " "Cyan"
    Get-ColoredText "🚀 ACTIVE BACKGROUND JOBS" "Green"
    Get-ColoredText " ─────────────────────────────────────────┐`n" "Cyan"
    
    $jobs = Get-Job
    if ($jobs) {
        foreach ($job in $jobs) {
            $jobName = $job.Name
            $jobId = $job.Id
            $state = $job.State
            $color = if ($state -eq 'Running') { 'Green' } elseif ($state -eq 'Completed') { 'Yellow' } else { 'Red' }
            $icon = if ($state -eq 'Running') { '✓' } elseif ($state -eq 'Completed') { '■' } else { '⚠' }
            Get-ColoredText "│  " "Cyan"
            Get-ColoredText "$icon " $color
            Get-ColoredText "Job $jobId ($jobName)" "White"
            Get-ColoredText " - $state" $color
            Write-Host ""
        }
    }
    else {
        Get-ColoredText "│  " "Cyan"
        Get-ColoredText "⚠ Hiç job çalışmıyor!" "Red"
        Write-Host ""
    }
    Get-ColoredText "└───────────────────────────────────────────────────────────────────────┘`n" "Cyan"
    
    Write-Host ""
    
    # LATEST ACTIVITY
    Get-ColoredText "┌─ " "Cyan"
    Get-ColoredText "📊 SON AKTİVİTELER" "Yellow"
    Get-ColoredText " ──────────────────────────────────────────────┐`n" "Cyan"
    
    # Infinite Learner Log
    $infiniteLog = "nexus_logs/job_infinite.log"
    if (Test-Path $infiniteLog) {
        $lastLines = Get-Content $infiniteLog -Tail 3 -ErrorAction SilentlyContinue
        if ($lastLines) {
            Get-ColoredText "│  " "Cyan"
            Get-ColoredText "🧠 INFINITE LEARNER:" "Magenta"
            Write-Host ""
            foreach ($line in $lastLines) {
                Get-ColoredText "│    " "Cyan"
                Write-Host $line.Substring(0, [Math]::Min(65, $line.Length))
            }
        }
    }
    
    # Realtime Worker Log
    $workerLog = "nexus_logs/job_worker.log"
    if (Test-Path $workerLog) {
        $lastLines = Get-Content $workerLog -Tail 3 -ErrorAction SilentlyContinue
        if ($lastLines) {
            Get-ColoredText "│  " "Cyan"
            Get-ColoredText "⚡ REALTIME WORKER:" "Yellow"
            Write-Host ""
            foreach ($line in $lastLines) {
                Get-ColoredText "│    " "Cyan"
                Write-Host $line.Substring(0, [Math]::Min(65, $line.Length))
            }
        }
    }
    
    Get-ColoredText "└───────────────────────────────────────────────────────────────────────┘`n" "Cyan"
    
    Write-Host ""
    
    # FILE STATISTICS
    Get-ColoredText "┌─ " "Cyan"
    Get-ColoredText "📁 WORKSPACE İSTATİSTİKLERİ" "Green"
    Get-ColoredText " ──────────────────────────────────────┐`n" "Cyan"
    
    $pyFiles = (Get-ChildItem -Path . -Filter "*.py" -File).Count
    $logSize = if (Test-Path "nexus_logs") { 
        [math]::Round((Get-ChildItem -Path "nexus_logs" -File | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    }
    else { 0 }
    
    $knowledgeCount = 0
    if (Test-Path "infinite_knowledge") {
        $knowledgeCount = (Get-ChildItem -Path "infinite_knowledge" -Filter "*.json" -Recurse).Count
    }
    
    Get-ColoredText "│  " "Cyan"
    Get-ColoredText "🐍 Python Dosyaları: " "White"
    Get-ColoredText "$pyFiles" "Green"
    Write-Host ""
    
    Get-ColoredText "│  " "Cyan"
    Get-ColoredText "📝 Log Boyutu: " "White"
    Get-ColoredText "$logSize MB" "Yellow"
    Write-Host ""
    
    Get-ColoredText "│  " "Cyan"
    Get-ColoredText "🧠 Öğrenilen Topic: " "White"
    Get-ColoredText "$knowledgeCount" "Magenta"
    Write-Host ""

    # Learner metrics (JSON)
    $metricsPath = "nexus_logs/learner_metrics.json"
    if (Test-Path $metricsPath) {
        try {
            $metrics = Get-Content $metricsPath -Raw | ConvertFrom-Json
            $cycles = $metrics.learning_cycles
            $topics = $metrics.total_topics_learned
            $rate = $metrics.learning_rate_per_hour
            $topDom = $metrics.top_domains | Select-Object -First 3

            Get-ColoredText "│  " "Cyan"
            Get-ColoredText "🔄 Learner Cycle: " "White"
            Get-ColoredText "$cycles" "Yellow"
            Write-Host ""

            Get-ColoredText "│  " "Cyan"
            Get-ColoredText "📚 Topics: " "White"
            Get-ColoredText "$topics" "Magenta"
            Get-ColoredText "  (" "Cyan"
            Get-ColoredText "$rate" "Yellow"
            Get-ColoredText " /saat)" "Cyan"
            Write-Host ""

            if ($topDom) {
                $topText = ($topDom | ForEach-Object { "$($_.psobject.Properties['0'].Value): $($_.psobject.Properties['1'].Value)" }) -join ", "
                Get-ColoredText "│  " "Cyan"
                Get-ColoredText "🏆 Top Domains: " "White"
                Get-ColoredText "$topText" "Green"
                Write-Host ""
            }
        }
        catch {
            # ignore parse errors
        }
    }

    # Heartbeat göstergesi
    $heartbeatPath = "nexus_logs/learner_heartbeat.txt"
    if (Test-Path $heartbeatPath) {
        $lastHb = Get-Item $heartbeatPath | Select-Object -ExpandProperty LastWriteTime
        $age = (New-TimeSpan -Start $lastHb -End (Get-Date)).TotalSeconds
        $hbColor = if ($age -lt 90) { 'Green' } elseif ($age -lt 180) { 'Yellow' } else { 'Red' }
        Get-ColoredText "│  " "Cyan"
        Get-ColoredText "🩺 Heartbeat: " "White"
        Get-ColoredText "$([math]::Round($age,0)) sn önce" $hbColor
        Write-Host ""
    }
    
    Get-ColoredText "└───────────────────────────────────────────────────────────────────────┘`n" "Cyan"
    
    Write-Host ""
    
    # SYSTEM STATUS
    $cpu = Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
    $ram = Get-WmiObject Win32_OperatingSystem
    $ramUsed = [math]::Round(($ram.TotalVisibleMemorySize - $ram.FreePhysicalMemory) / 1MB, 1)
    $ramTotal = [math]::Round($ram.TotalVisibleMemorySize / 1MB, 1)
    
    Get-ColoredText "┌─ " "Cyan"
    Get-ColoredText "💻 SİSTEM DURUMU" "Cyan"
    Get-ColoredText " ───────────────────────────────────────────────┐`n" "Cyan"
    
    Get-ColoredText "│  " "Cyan"
    Get-ColoredText "CPU: " "White"
    Get-ColoredText "$cpu%" "Yellow"
    Get-ColoredText "  |  " "Cyan"
    Get-ColoredText "RAM: " "White"
    Get-ColoredText "$ramUsed GB / $ramTotal GB" "Yellow"
    Write-Host ""
    
    Get-ColoredText "└───────────────────────────────────────────────────────────────────────┘`n" "Cyan"
    
    Write-Host ""
    Get-ColoredText "⏸️  Güncelleniyor her 3 saniyede... (CTRL+C ile durdurun)" "DarkGray"
    Write-Host "`n"
}

# Ana döngü - HER 3 SANİYEDE GÜNCELLE
Write-Host "`n🔥 NEXUS-ONE LIVE MONITOR BAŞLATILIYOR...`n" -ForegroundColor Green
Start-Sleep -Seconds 2

while ($true) {
    Show-Dashboard
    Start-Sleep -Seconds 3
}
