# Creates a desktop shortcut to the NEXUS-ONE Control Panel
$ErrorActionPreference = 'Stop'

$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'NEXUS Control Panel.lnk'
$target = 'powershell.exe'
$arguments = '-ExecutionPolicy Bypass -File "' + (Join-Path $PWD 'scripts/run_control_panel.ps1') + '"'
$icon = (Join-Path $PWD 'brand/icons/nexus.ico')

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $target
$Shortcut.Arguments = $arguments
$Shortcut.WorkingDirectory = $PWD
if (Test-Path $icon) { $Shortcut.IconLocation = $icon }
$Shortcut.Save()

Write-Host "Desktop shortcut created: $shortcutPath" -ForegroundColor Green
