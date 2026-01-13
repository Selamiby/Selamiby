#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()

$ErrorActionPreference = "Continue"
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   NEXUS-ONE PERSISTENT LEARNING TERMINAL          " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Gerçek kod öğrenme motoru başlatılıyor..." -ForegroundColor Green

$ScriptPath = "c:\Users\selam\NEXUS-ONE\nexus_infinite_learner.py"

while ($true) {
    Write-Host "[$(Get-Date)] NEXUS-ONE Öğrenme Motoru Çalıştırılıyor..." -ForegroundColor Yellow
    python $ScriptPath
    
    Write-Host "[$(Get-Date)] Uyarı: Öğrenme motoru durdu veya çöktü! 5 saniye içinde yeniden başlatılacak..." -ForegroundColor Red
    Start-Sleep -Seconds 5
}
