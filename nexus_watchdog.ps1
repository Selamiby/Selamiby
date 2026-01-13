# NEXUS-ONE Watchdog & Persistence System
# Bu script terminal kapansa bile arka planda NEXUS'u hayatta tutar.

$DashboardCmd = "streamlit run nexus_dashboard_v2.py --server.port 8501 --server.headless true"
$LearnerCmd = "python nexus_infinite_learner.py"

function Start-NexusProcesses {
    Write-Host "[!] NEXUS-ONE Servisleri başlatılıyor..." -ForegroundColor Cyan
    
    # Dashboard'u arka planda başlat (Penceresiz)
    Start-Process powershell -ArgumentList "-Command $DashboardCmd" -WindowStyle Hidden -PassThru
    Write-Host "[+] Dashboard (Port 8501) arka plana itildi." -ForegroundColor Green
    
    # Otonom Öğreniciyi arka planda başlat
    Start-Process powershell -ArgumentList "-Command $LearnerCmd" -WindowStyle Hidden -PassThru
    Write-Host "[+] Otonom Öğrenici (Brain) arka plana itildi." -ForegroundColor Green
}

# Eğer hali hazırda çalışıyorsa temizle
Get-Process | Where-Object { $_.CommandLine -like "*streamlit*" -or $_.CommandLine -like "*nexus_infinite_learner*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Start-NexusProcesses

Write-Host "[✔] NEXUS-ONE bağımsızlığını ilan etti. Terminali kapatabilirsiniz." -ForegroundColor Yellow
Write-Host "[?] Durdurmak isterseniz: Stop-Process -Name powershell (Dikkatli olun)" -ForegroundColor Gray
