$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$ShortcutFile = [System.IO.Path]::Combine($DesktopPath, "NEXUS-ONE.lnk")
$Shortcut = $WshShell.CreateShortcut($ShortcutFile)

# Pythonw.exe (Konsol açılmadan çalıştıran exe)
$PythonPath = "C:\Users\selam\AppData\Local\Programs\Python\Python311\pythonw.exe"
$ScriptPath = "C:\Users\selam\NEXUS-ONE\nexus_app_wrapper.py"

$Shortcut.TargetPath = $PythonPath
$Shortcut.Arguments = $ScriptPath
$Shortcut.WorkingDirectory = "C:\Users\selam\NEXUS-ONE"
$Shortcut.IconLocation = "shell32.dll,130"
$Shortcut.Description = "NEXUS-ONE Advanced AI Operating System"
$Shortcut.Save()

Write-Host "✅ Masaüstü kısayolu başarıyla oluşturuldu!" -ForegroundColor Green
