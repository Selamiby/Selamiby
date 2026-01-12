# 🎬 NEXUS-ONE ACTIVITY VIEWER - CANLI AKTİVİTE İZLEYİCİ
# Log dosyalarını canlı olarak takip eder - hareket göreceksiniz!

$Host.UI.RawUI.WindowTitle = "🎬 NEXUS-ONE ACTIVITY VIEWER"

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  " -NoNewline -ForegroundColor Cyan
Write-Host "🎬 NEXUS-ONE ACTIVITY VIEWER - CANLI LOGlar" -NoNewline -ForegroundColor Yellow
Write-Host "          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Log dosyalarını kontrol et
$logFiles = @(
    @{Path="nexus_logs/job_infinite.log"; Name="🧠 INFINITE LEARNER"; Color="Magenta"},
    @{Path="nexus_logs/job_worker.log"; Name="⚡ REALTIME WORKER"; Color="Yellow"},
    @{Path="nexus_logs/job_automation.log"; Name="🔧 AUTOMATION"; Color="Green"},
    @{Path="nexus_logs/job_healer.log"; Name="🏥 AUTO HEALER"; Color="Cyan"}
)

$positions = @{}
foreach ($log in $logFiles) {
    if (Test-Path $log.Path) {
        $positions[$log.Path] = (Get-Content $log.Path).Count
    } else {
        $positions[$log.Path] = 0
    }
}

Write-Host "✅ Monitoring başlatıldı - Yeni aktiviteler HEMEN görünecek!`n" -ForegroundColor Green
Write-Host "─" * 60 -ForegroundColor DarkGray
Write-Host ""

# Sonsuz döngü - yeni satırları göster
$cycleCount = 0
while ($true) {
    $cycleCount++
    $hasNewActivity = $false
    
    foreach ($log in $logFiles) {
        if (Test-Path $log.Path) {
            $currentLines = Get-Content $log.Path
            $currentCount = $currentLines.Count
            $lastPosition = $positions[$log.Path]
            
            if ($currentCount -gt $lastPosition) {
                # Yeni satırlar var!
                $hasNewActivity = $true
                $newLines = $currentLines[$lastPosition..($currentCount-1)]
                
                Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] " -NoNewline -ForegroundColor DarkGray
                Write-Host $log.Name -NoNewline -ForegroundColor $log.Color
                Write-Host " →" -ForegroundColor DarkGray
                
                foreach ($line in $newLines) {
                    if ($line.Trim()) {
                        Write-Host "  $line" -ForegroundColor White
                    }
                }
                Write-Host ""
                
                $positions[$log.Path] = $currentCount
            }
        }
    }
    
    # Her 10 döngüde bir heartbeat göster
    if ($cycleCount % 10 -eq 0 -and -not $hasNewActivity) {
        Write-Host "💓 Heartbeat #$cycleCount - Sistemler çalışıyor... " -NoNewline -ForegroundColor DarkGray
        Write-Host "($(Get-Date -Format 'HH:mm:ss'))" -ForegroundColor DarkGray
    }
    
    Start-Sleep -Milliseconds 1500
}
