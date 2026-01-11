#!/usr/bin/env python3
"""
Build NEXUS-ONE as standalone executable
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller  # noqa: F401
        return True
    except ImportError:
        return False

def build_executable():
    """Build standalone executable"""
    print("="*60)
    print("🛠️  Building NEXUS-ONE Executable")
    print("="*60)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=False)
    
    # Clean previous builds
    build_dir = Path("dist")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Create spec file content
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

a = Analysis(
    ['nexus_one.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'psutil',
        'rich',
        'json',
        'datetime',
        'subprocess',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NexusOne',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='brand/logos/nexus_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NexusOne',
)
'''
    
    # Create .spec file
    with open("nexus_one.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # Build executable
    print("🔨 Building executable...")
    result = subprocess.run([
        "pyinstaller", 
        "--clean",
        "--onefile",
        "--name", "NexusOne",
        "--icon", "brand/logos/nexus_icon.ico",
        "nexus_one.py"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build successful!")
        
        # Check output
        exe_path = Path("dist/NexusOne.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executable size: {size_mb:.1f} MB")
            print(f"📍 Location: {exe_path.absolute()}")
            
            # Create README
            readme_content = f"""
# NEXUS-ONE Standalone Executable

## 📋 About
NEXUS-ONE Autonomous AI Operating System
Version: 1.0.0
Build Date: {Path(__file__).stat().st_mtime}

## 🚀 Usage
Simply run `NexusOne.exe` to start the AI system.

## 🛠️ Features
- System monitoring and analysis
- File management operations
- Intelligent text analysis
- Command execution
- Session export

## 📁 Files Included
- NexusOne.exe: Main executable
- nexus_session.json: Example session export

## ⚙️ Requirements
- Windows 7/8/10/11
- No Python installation required
- 50MB free disk space

## 🔧 Troubleshooting
If the executable doesn't run:
1. Try running as Administrator
2. Check Windows Defender/Firewall settings
3. Ensure .NET Framework is updated

## 📞 Support
For issues and feature requests, visit the project repository.

## ⚠️ Disclaimer
This software is provided "as is". Use at your own risk.
"""
            
            with open("dist/README.txt", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            print("\n" + "="*60)
            print("🎉 BUILD COMPLETE!")
            print("="*60)
            print("\n📋 Next steps:")
            print("   1. Find your executable in: dist/NexusOne.exe")
            print("   2. Copy it anywhere you want to use it")
            print("   3. Double-click to run")
            print("   4. No Python installation required!")
            print("\n💡 Tip: You can distribute this .exe file to others")
            print("="*60)
            
            return True
        else:
            print("❌ Executable not found after build")
            return False
    else:
        print("❌ Build failed!")
        print(f"Error: {result.stderr}")
        return False


def create_portable_package():
    """Create portable package with all dependencies"""
    print("\n📦 Creating portable package...")
    
    # Create portable directory
    portable_dir = Path("NexusOne_Portable")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # Copy files
    files_to_copy = [
        "nexus_one.py",
        "requirements.txt",
        "install.py",
        "run_nexus.bat",
        "run_nexus.ps1",
        "config/nexus_config.yaml",
        "brand/logos/nexus_logo.svg",
    ]
    
    for file_path in files_to_copy:
        src = Path(file_path)
        if src.exists():
            dst = portable_dir / src.name
            if src.is_file():
                shutil.copy2(src, dst)
            else:
                shutil.copytree(src, dst)
    
    # Create launcher
    launcher_content = '''@echo off
chcp 65001 >nul
title NEXUS-ONE Portable
echo.
echo ╔══════════════════════════════════════════╗
echo ║       NEXUS-ONE Portable Edition        ║
echo ╚══════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo ✅ Python detected
echo 📍 Running from portable directory...
echo.

REM Install dependencies if needed
if not exist "venv" (
    echo ⚙️ Setting up portable environment...
    python install.py
)

echo 🚀 Starting NEXUS-ONE...
echo.
call venv\Scripts\activate.bat
python nexus_one.py

pause
'''
    
    with open(portable_dir / "Start_NexusOne.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Create README
    readme_content = '''# NEXUS-ONE Portable Edition

## 📦 What's Included
This portable package contains everything needed to run NEXUS-ONE:

- `nexus_one.py`: Main application
- `Start_NexusOne.bat`: Windows launcher
- `install.py`: Auto-installer for dependencies
- Configuration files and logos

## 🚀 How to Use
1. Extract this folder anywhere
2. Run `Start_NexusOne.bat`
3. The installer will set up everything automatically
4. Enjoy NEXUS-ONE!

## 🔧 Requirements
- Windows OS
- Python 3.8+ installed (python.org)
- Internet connection (for first-time setup)

## 💾 Portable Features
- No installation needed
- Can run from USB drive
- Self-contained environment
- Easy to update

## 📞 Support
For help, check the documentation or contact support.
'''
    
    with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Zip the package
    import zipfile
    zip_path = "NexusOne_Portable.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in portable_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(portable_dir)
                zipf.write(file, arcname)
    
    size_mb = Path(zip_path).stat().st_size / (1024 * 1024)
    print(f"✅ Portable package created: {zip_path} ({size_mb:.1f} MB)")
    
    return True


if __name__ == "__main__":
    try:
        print("Choose build option:")
        print("  1. Standalone .exe (Windows only)")
        print("  2. Portable package (requires Python)")
        print("  3. Both")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        success = True
        
        if choice in ["1", "3"]:
            success = build_executable() and success
        
        if choice in ["2", "3"]:
            success = create_portable_package() and success
        
        if success:
            print("\n🎊 All builds completed successfully!")
        else:
            print("\n⚠️ Some builds may have failed")
            
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelled")
    except Exception as e:
        print(f"\n❌ Build error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
