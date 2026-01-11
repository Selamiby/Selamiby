#!/usr/bin/env python3
"""
NEXUS-ONE Installation Script
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run shell command"""
    print(f"🚀 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    return True


def install_nexus():
    """Install NEXUS-ONE"""
    print("=" * 60)
    print("🛠️  NEXUS-ONE Installation")
    print("=" * 60)
    
    # Check Python
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment
    print("\n🏗️  Creating virtual environment...")
    if not os.path.exists("venv"):
        if not run_command(f"{sys.executable} -m venv venv"):
            return False
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Activate and install packages
    print("\n📦 Installing packages...")
    
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Upgrade pip
    run_command(f"{pip_path} install --upgrade pip", check=False)
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        if not run_command(f"{pip_path} install -r requirements.txt"):
            print("⚠️  Some packages failed, continuing...")
    else:
        # Install core packages
        packages = ["rich", "psutil", "requests", "aiohttp", "pyyaml", "python-dotenv"]
        for pkg in packages:
            run_command(f"{pip_path} install {pkg}", check=False)
    
    # Create shortcut/launcher
    print("\n🔗 Creating launcher...")
    
    if platform.system() == "Windows":
        # Windows batch file
        bat_content = '''@echo off
chcp 65001 >nul
call "%~dp0venv\\Scripts\\activate.bat"
python "%~dp0main.py"
pause
'''
        with open("run_nexus.bat", "w", encoding="utf-8") as f:
            f.write(bat_content)
        
        # PowerShell script
        ps_content = '''# NEXUS-ONE Launcher
& "$PSScriptRoot\\venv\\Scripts\\Activate.ps1"
python "$PSScriptRoot\\main.py"
'''
        with open("run_nexus.ps1", "w", encoding="utf-8") as f:
            f.write(ps_content)
        
        print("✅ Created run_nexus.bat and run_nexus.ps1")
    
    else:
        # Linux/Mac shell script
        sh_content = '''#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
'''
        with open("run_nexus.sh", "w", encoding="utf-8") as f:
            f.write(sh_content)
        os.chmod("run_nexus.sh", 0o755)
        print("✅ Created run_nexus.sh")
    
    # Test installation
    print("\n🧪 Testing installation...")
    test_result = run_command(f"{python_path} -c \"import rich, psutil; print('✅ Core packages loaded successfully')\"", check=False)
    
    if test_result:
        print("=" * 60)
        print("🎉 NEXUS-ONE INSTALLATION COMPLETE!")
        print("=" * 60)
        print("\n📋 Next steps:")
        print("   1. Run: run_nexus.bat (Windows) or ./run_nexus.sh (Linux/Mac)")
        print("   2. Explore the AI-powered features")
        print("   3. Check config/nexus_config.yaml for customization")
        print("\n💡 Tip: Add your API keys to .env file for enhanced features")
        print("=" * 60)
        return True
    else:
        print("❌ Installation test failed")
        return False


if __name__ == "__main__":
    try:
        success = install_nexus()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled")
        sys.exit(1)
