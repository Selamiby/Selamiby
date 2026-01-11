# NEXUS-ONE Distribution Creator
Write-Host "`n"
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       NEXUS-ONE Distribution Builder     ║" -ForegroundColor Yellow
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Create distribution folder
$distFolder = "NexusOne_Distribution_$(Get-Date -Format 'yyyyMMdd_HHmm')"
New-Item -ItemType Directory -Path $distFolder -Force | Out-Null

Write-Host "📁 Creating distribution in: $distFolder" -ForegroundColor Green

# Essential files to include
$essentialFiles = @(
    "nexus_one.py",
    "requirements.txt",
    "install.py",
    "run_nexus.bat",
    "run_nexus.ps1",
    "config\nexus_config.yaml",
    "brand\logos\nexus_logo.svg",
    "brand\logos\nexus_icon.svg"
)

# Copy essential files
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        $destDir = "$distFolder\$(Split-Path $file -Parent)"
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Copy-Item $file -Destination "$distFolder\$file" -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠️  Missing: $file" -ForegroundColor Yellow
    }
}

# Create quick start guide
$guideContent = @'
# 🚀 NEXUS-ONE Quick Start Guide

## 📦 What is NEXUS-ONE?
NEXUS-ONE is an Autonomous AI Operating System that converges multiple intelligences into a single, powerful interface.

## 🛠️ Installation Options

### Option 1: Quick Start (Recommended)
1. Run `install.py`
2. Follow the prompts
3. Run `run_nexus.bat`

### Option 2: Manual Setup
1. Ensure Python 3.8+ is installed
2. Run: `python -m venv venv`
3. Run: `venv\Scripts\activate`
4. Run: `pip install -r requirements.txt`
5. Run: `python nexus_one.py`

### Option 3: Portable Use
Just run `nexus_one.py` directly (some features may require additional packages)

## 🎯 Quick Features

### System Monitoring
- Real-time CPU, memory, disk usage
- Process management
- Network information

### File Operations
- Intelligent file listing
- File creation and management
- Pattern searching

### AI Capabilities
- Text analysis and sentiment detection
- Intelligent command processing
- Session management

## ⚡ Quick Commands
- `info` - System information
- `files` - List files
- `create` - Create new file
- `analyze` - Analyze text
- `run` - Execute system command
- `export` - Save session data

## 🔧 Configuration
Edit `config\nexus_config.yaml` to customize:
- System settings
- AI behavior
- Interface preferences

## 🆘 Need Help?
- Check the console for error messages
- Ensure all requirements are installed
- Run with administrator privileges if needed

## 📄 License
NEXUS-ONE is provided under open-source license. See LICENSE file for details.

## 🌐 Connect
Visit our repository for updates and community support.

---
*Where All Intelligence Converges*
'@

Set-Content -Path "$distFolder\QUICK_START.md" -Value $guideContent -Encoding UTF8
Write-Host "  ✅ Created QUICK_START.md" -ForegroundColor Green

# Create batch file for easy distribution
$distroBat = @'
@echo off
chcp 65001 >nul
title NEXUS-ONE Distribution Setup
cls

echo.
echo ╔══════════════════════════════════════════╗
echo ║       NEXUS-ONE Distribution Setup       ║
echo ╚══════════════════════════════════════════╝
echo.

echo 📋 This will set up NEXUS-ONE on your system.
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Run installer
echo 🛠️  Running NEXUS-ONE installer...
echo.
python install.py

if errorlevel 1 (
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo.
echo 🎉 Installation complete!
echo.
echo 📋 Next steps:
echo    1. Run: run_nexus.bat
echo    2. Or: python nexus_one.py
echo.
echo 📚 Read QUICK_START.md for more information.
echo.
pause
'@

Set-Content -Path "$distFolder\Setup_NexusOne.bat" -Value $distroBat -Encoding UTF8
Write-Host "  ✅ Created Setup_NexusOne.bat" -ForegroundColor Green

# Create zip file
$zipFile = "$distFolder.zip"
Compress-Archive -Path "$distFolder\*" -DestinationPath $zipFile -Force
$zipSize = [math]::Round((Get-Item $zipFile).Length / 1MB, 2)

Write-Host "`n"
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        DISTRIBUTION CREATED!            ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

Write-Host "📦 Distribution package: $zipFile" -ForegroundColor Cyan
Write-Host "📏 Size: $zipSize MB" -ForegroundColor Cyan
Write-Host "📁 Contents extracted to: $distFolder"