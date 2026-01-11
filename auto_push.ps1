# Otomatik Git Commit ve Push Scripti
# Her 5 dakikada bir değişiklikleri commit ve push eder
# PSScriptAnalyzer: Function uses approved verbs

param(
    [int]$IntervalSeconds = 300  # Varsayılan: 5 dakika
)

function Invoke-GitAutoPush {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    try {
        # Değişiklikleri kontrol et
        $status = & git status --porcelain
        
        if ($status) {
            Write-Host "[$timestamp] Değişiklikler bulundu. Commit ediliyor..." -ForegroundColor Green
            
            # Değişiklikleri ekle
            & git add .
            
            # Commit et
            & git commit -m "Auto-commit: $timestamp - Değişiklikler otomatik kaydedildi"
            
            # Fetch et (güncel repo'yu çek)
            & git fetch origin
            
            # Push et
            & git push origin main --force
            
            Write-Host "[$timestamp] Başarıyla push edildi!" -ForegroundColor Green
        }
        else {
            Write-Host "[$timestamp] Yeni değişiklik yok." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[$timestamp] Hata: $_" -ForegroundColor Red
    }
}

# Sürekli loop
Write-Host "Otomatik Git Sync başladı. Interval: $IntervalSeconds saniye" -ForegroundColor Cyan
while ($true) {
    Invoke-GitAutoPush
    Start-Sleep -Seconds $IntervalSeconds
}
