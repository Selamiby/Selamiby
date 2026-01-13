#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()
#Requires -Version 5.1
#Requires -PSEdition Desktop

# Learned Languages Reporter for NEXUS-ONE

$ErrorActionPreference = 'SilentlyContinue'

$jsonPath = Join-Path $PSScriptRoot "learned_languages.json"

if (-not (Test-Path $jsonPath)) {
    Write-Host "Öğrenme kayıt defteri ($jsonPath) henüz oluşturulmamış." -ForegroundColor Yellow
    exit 1
}

$content = Get-Content -Path $jsonPath -Raw
if ([string]::IsNullOrWhiteSpace($content)) {
    $languages = @()
}
else {
    $languages = $content | ConvertFrom-Json
}

if ($languages.Count -eq 0) {
    Write-Host "NEXUS-ONE henüz yeni bir dil öğrenmedi. Öğrenme süreci devam ediyor..." -ForegroundColor Cyan
}
else {
    Write-Host "NEXUS-ONE Tarafından Öğrenilen Diller:" -ForegroundColor Green
    Write-Host "------------------------------------"
    
    $i = 1
    foreach ($lang in $languages) {
        $learnDate = Get-Date $lang.learned_at
        Write-Host "$i. $($lang.name) - (Öğrenilme Tarihi: $($learnDate.ToString('yyyy-MM-dd HH:mm')))"
        $i++
    }
    Write-Host "------------------------------------"
    Write-Host "Toplam Öğrenilen Dil Sayısı: $($languages.Count)" -ForegroundColor Green
}
