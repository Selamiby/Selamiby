# NEXUS-ONE Basit Launcher
# Sadece Python'u çalıştırır, başka hiçbir şey yapmaz

# 1. Ekranı temizle
Clear-Host

# 2. Banner göster
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        NEXUS-ONE AI System" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 3. Python kontrolü (basit)
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from: https://python.org" -ForegroundColor Yellow
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# 4. Hangi dosyayı çalıştıracağımızı bul
$targetFile = "nexus_simple.py"

# Eğer nexus_simple.py yoksa, main.py dene
if (-not (Test-Path $targetFile)) {
    $targetFile = "main.py"
}

# Eğer main.py de yoksa, nexus_one.py dene
if (-not (Test-Path $targetFile)) {
    $targetFile = "nexus_one.py"
}

# Hala dosya yoksa, oluştur
if (-not (Test-Path $targetFile)) {
    Write-Host "No Python file found. Creating simple version..." -ForegroundColor Yellow
    
    # Basit bir Python dosyası oluştur
    $simpleCode = @'
print("NEXUS-ONE System")
print("Hello World!")
input("Press Enter to exit...")
'@
    
    $simpleCode | Out-File -FilePath "nexus_simple.py" -Encoding UTF8
    $targetFile = "nexus_simple.py"
    Write-Host "Created: $targetFile" -ForegroundColor Green
}

# 5. Dosyayı çalıştır
Write-Host ""
Write-Host "Starting: $targetFile" -ForegroundColor Cyan
Write-Host "------------------------------------------" -ForegroundColor DarkGray

try {
    # Python dosyasını çalıştır
    python $targetFile
    
    # Çıkış kodu
    if ($LASTEXITCODE -eq 0) {
        Write-Host "------------------------------------------" -ForegroundColor DarkGray
        Write-Host "NEXUS-ONE completed successfully!" -ForegroundColor Green
    }
    else {
        Write-Host "------------------------------------------" -ForegroundColor DarkGray
        Write-Host "NEXUS-ONE exited with code: $LASTEXITCODE" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}

# 6. Kapanış
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
