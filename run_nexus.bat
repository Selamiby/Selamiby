@echo off
chcp 65001 >nul
cls

echo.
echo ==========================================
echo        NEXUS-ONE AI System
echo ==========================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://python.org
    pause
    exit /b 1
)

REM Hangi dosyayı çalıştıracağız?
if exist "nexus_simple.py" (
    set TARGET=nexus_simple.py
) else if exist "main.py" (
    set TARGET=main.py
) else if exist "nexus_one.py" (
    set TARGET=nexus_one.py
) else (
    echo No Python file found. Creating simple version...
    echo print^("NEXUS-ONE System"^) > nexus_simple.py
    echo print^("Hello World!"^) >> nexus_simple.py
    echo input^("Press Enter to exit..."^) >> nexus_simple.py
    set TARGET=nexus_simple.py
)

echo.
echo Starting: %TARGET%
echo ------------------------------------------
echo.

REM Çalıştır
python "%TARGET%"

if errorlevel 1 (
    echo ------------------------------------------
    echo NEXUS-ONE exited with error!
) else (
    echo ------------------------------------------
    echo NEXUS-ONE completed successfully!
)

echo.
echo ==========================================
echo Press any key to exit...
pause >nul
