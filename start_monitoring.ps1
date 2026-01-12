# 🎯 NEXUS-ONE MONITORING STARTER
# Tüm monitoring panellerini başlatır

Write-Host "`n🚀 NEXUS-ONE MONITORING BAŞLATILIYOR...`n" -ForegroundColor Green

# 1. Live Monitor (Dashboard)
Write-Host "📊 Live Monitor başlatılıyor..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File live_monitor.ps1" -WindowStyle Normal
Start-Sleep -Seconds 1

# 2. Activity Viewer (Log Takip)
Write-Host "🎬 Activity Viewer başlatılıyor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File activity_viewer.ps1" -WindowStyle Normal
Start-Sleep -Seconds 1

Write-Host "`n✅ 2 MONITORING PANEL BAŞLATILDI!" -ForegroundColor Green
Write-Host "`n📺 Şimdi:" -ForegroundColor White
Write-Host "  → Live Monitor panelinde sistem durumunu göreceksiniz (her 3 saniye)" -ForegroundColor Cyan
Write-Host "  → Activity Viewer panelinde canlı aktiviteleri göreceksiniz" -ForegroundColor Yellow
Write-Host "`n💡 Her iki terminalde de HAREKETLER göreceksiniz!`n" -ForegroundColor Green
