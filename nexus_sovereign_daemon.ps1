# NEXUS-ONE Sovereign Persistence Daemon
# HEDEF: 7/24 Kesintisiz çalışma garantisi.
# Bu script arka planda çalışır ve ölen servisleri diriltir.

$Workspace = "c:\Users\selam\NEXUS-ONE"
Set-Location $Workspace

$LogFile = "$Workspace\nexus_logs\daemon_persistence.log"

function Write-Log {
    param($Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$TimeStamp] $Message" | Out-File -FilePath $LogFile -Append
}

Write-Log "🔥 Sovereign Daemon Başlatıldı. 7/24 İzleme Aktif."

while ($true) {
    try {
        # 1. Dashboard Kontrolü (Port 8501)
        $DashboardActive = netstat -ano | findstr :8501
        if (-not $DashboardActive) {
            Write-Log "⚠️ Dashboard (8501) durmuş! Hiper-Kalıcı modda yeniden başlatılıyor..."
            # Arka planda tam bağımsız süreç olarak başlat
            Start-Process pythonw -ArgumentList "-m streamlit run $Workspace\nexus_dashboard_v2.py --server.port 8501 --server.headless true" -WindowStyle Hidden
        }

        # 1b. Dashboard Donma Kontrolü (Zombi Süreç Temizliği)
        $StreamlitProcs = Get-Process | Where-Object { $_.CommandLine -like "*streamlit*" }
        foreach ($proc in $StreamlitProcs) {
            if ($proc.Responding -eq $false) {
                Write-Log "🚨 Dashboard zombileşmiş! Zorla kapatılıyor..."
                Stop-Process -Id $proc.Id -Force
            }
        }

        # 2. Infinite Learner (Sovereign) Kontrolü
        $LearnerProcess = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*nexus_infinite_learner.py*" }
        if (-not $LearnerProcess) {
            Write-Log "⚠️ Sovereign Learner durmuş! Yeniden başlatılıyor..."
            Start-Process pythonw -ArgumentList "nexus_infinite_learner.py" -WindowStyle Hidden
        }

        # 2a. Keep-Awake Sentinel (Sistemin uyumasını engelle)
        $KeepAwakeProcess = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*keep_awake.ps1*" }
        if (-not $KeepAwakeProcess) {
            Write-Log "🛡️ Keep-Awake aktif değil! Uyku engelleme başlatılıyor..."
            Start-Process powershell -ArgumentList "-File $Workspace\keep_awake.ps1" -WindowStyle Hidden
        }

        # 3. Heartbeat (Nabız) Kontrolü
        if (Test-Path "$Workspace\nexus_logs\learner_heartbeat.txt") {
            $LastHeartbeat = Get-Content "$Workspace\nexus_logs\learner_heartbeat.txt"
            $TimeDiff = (Get-Date) - (Get-Date $LastHeartbeat)
            if ($TimeDiff.TotalMinutes -gt 5) {
                Write-Log "🚨 Nabız donmuş ($($TimeDiff.TotalMinutes) dk)! Süreç zorla sonlandırılıp yeniden başlatılıyor..."
                if ($LearnerProcess) { Stop-Process -Id $LearnerProcess.ProcessId -Force }
                Start-Process pythonw -ArgumentList "nexus_infinite_learner.py" -WindowStyle Hidden
            }
        }

        # 4. Revenue Hunter & Daily Summary (Saatlik Çalıştır)
        $CurrentHour = (Get-Date).Hour
        if (($CurrentHour -ne $LastRevenueHour) -or (-not $LastRevenueHour)) {
            Write-Log "💰 Revenue Hunter tetikleniyor... (Fırsat Taraması)"
            Start-Process pythonw -ArgumentList "nexus_revenue_hunter.py" -WindowStyle Hidden
            
            Write-Log "🎨 Adobe Stock Generator tetikleniyor... (Görsel Üretimi)"
            Start-Process pythonw -ArgumentList "nexus_adobe_stock_generator.py" -WindowStyle Hidden
            
            $LastRevenueHour = $CurrentHour
        }

        # 5. Stable Diffusion Check (Port 7860)
        $SDActive = netstat -ano | findstr :7860
        if (-not $SDActive) {
            Write-Log "🎨 Stable Diffusion kapalı! Arka planda başlatılıyor..."
            # Not: Bu işlem GPU yükü bindirecektir.
            Start-Process cmd -ArgumentList "/c $Workspace\stable-diffusion-webui\webui-user.bat" -WorkingDirectory "$Workspace\stable-diffusion-webui" -WindowStyle Hidden
        }
    }
    catch {
        Write-Log "❌ Daemon hatası: $_"
    }

    # CPU koruması: 1 dakikada bir kontrol et
    Start-Sleep -Seconds 60
}
