# NEXUS-ONE Watchdog & Persistence System
$DashboardCmd = "streamlit run nexus_dashboard_v2.py --server.port 8501 --server.headless true"
$LearnerCmd = "python nexus_infinite_learner.py"

Write-Host "[!] Servisler hazirlaniyor..." -ForegroundColor Cyan

# Dashboard baslat
Start-Process powershell -ArgumentList "-NoProfile -Command $DashboardCmd" -WindowStyle Hidden
Write-Host "[+] Localhost:8501 Arka Planda Aktif." -ForegroundColor Green

# Learner baslat
Start-Process powershell -ArgumentList "-NoProfile -Command $LearnerCmd" -WindowStyle Hidden
Write-Host "[+] Otonom Brain Arka Planda Aktif." -ForegroundColor Green

Write-Host "=========================================================" -ForegroundColor Yellow
Write-Host " NEXUS-ONE ARTIK BAGIMSIZ " -ForegroundColor Yellow
Write-Host "=========================================================" -ForegroundColor Yellow
Write-Host "Terminali kapatabilirsiniz. Localhost acik kalacaktir."
