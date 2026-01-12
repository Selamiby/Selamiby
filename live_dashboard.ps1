# ⚡ NEXUS LIVE DASHBOARD - GERÇEK ZAMANLI GÖRÜNÜR PANEL
# Her 2 saniyede güncellenir - HAREKET GÖRECEKSİNİZ!

$Host.UI.RawUI.WindowTitle = "⚡ NEXUS-ONE LIVE DASHBOARD - ANLIK"

function Show-LiveStats {
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Clear-Host
    
    # HEADER
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  ⚡ NEXUS-ONE LIVE DASHBOARD - GERÇEK ZAMANLI               ║" -ForegroundColor Yellow
    Write-Host "║  🕐 $timestamp                                               ║" -ForegroundColor White
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    # JOBS
    Write-Host "🚀 ÇALIŞAN SİSTEMLER:" -ForegroundColor Green
    $jobs = Get-Job | Where-Object { $_.State -eq 'Running' }
    if ($jobs) {
        foreach ($j in $jobs) {
            Write-Host "   ✓ Job$($j.Id) - AKTIF ÇALIŞIYOR" -ForegroundColor Green
        }
    }
    else {
        Write-Host "   ⚠ Hiç job çalışmıyor!" -ForegroundColor Red
    }
    Write-Host ""
    
    # FILES
    $pyCount = (Get-ChildItem -Filter "*.py").Count
    $logCount = if (Test-Path "nexus_logs") { (Get-ChildItem "nexus_logs" -Filter "*.log").Count } else { 0 }
    
    Write-Host "📁 WORKSPACE:" -ForegroundColor Cyan
    Write-Host "   📝 Python dosyaları: $pyCount" -ForegroundColor White
    Write-Host "   📋 Log dosyaları: $logCount" -ForegroundColor White
    Write-Host ""
    
    # LATEST LOG ACTIVITY
    Write-Host "📊 SON AKTİVİTE:" -ForegroundColor Yellow
    
    if (Test-Path "nexus_logs/job_worker.log") {
        $lastLine = Get-Content "nexus_logs/job_worker.log" -Tail 1 -ErrorAction SilentlyContinue
        if ($lastLine) {
            Write-Host "   ⚡ Worker: $($lastLine.Substring(0, [Math]::Min(50, $lastLine.Length)))" -ForegroundColor Magenta
        }
    }
    
    if (Test-Path "nexus_logs/job_infinite.log") {
        $lastLine = Get-Content "nexus_logs/job_infinite.log" -Tail 1 -ErrorAction SilentlyContinue
        if ($lastLine) {
            Write-Host "   🧠 Learner: $($lastLine.Substring(0, [Math]::Min(50, $lastLine.Length)))" -ForegroundColor Cyan
        }
    }
    
    Write-Host ""
    Write-Host "⏱️  Güncelleniyor her 2 saniyede... [CTRL+C ile durdur]" -ForegroundColor DarkGray
    Write-Host ""
}

Write-Host "`n⚡ LIVE DASHBOARD BAŞLATILIYOR...`n" -ForegroundColor Green
Start-Sleep -Seconds 1

# ANA DÖNGÜ - Her 2 saniye
while ($true) {
    Show-LiveStats
    Start-Sleep -Seconds 2
}
