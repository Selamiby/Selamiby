@echo off
title NEXUS GUARDIAN - SERVER PERSISTENCE
:start
echo [%date% %time%] Launching NEXUS Sovereign Server...
python c:\Users\selam\NEXUS-ONE\nexus_sovereign_server.py
echo [%date% %time%] Server crashed or stopped. Restarting in 5 seconds...
timeout /t 5
goto start
