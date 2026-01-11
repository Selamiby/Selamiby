#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()
# Launches the NEXUS-ONE human control panel with BelowNormal priority
$ErrorActionPreference = 'Stop'

$python = "C:\\Users\\selam\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
$panel = Join-Path $PWD 'ui/human_control_panel.py'

Write-Host "Starting Control Panel..." -ForegroundColor Cyan

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = "`"$panel`""
$psi.UseShellExecute = $true
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal

$proc = [System.Diagnostics.Process]::Start($psi)
$proc.PriorityClass = 'BelowNormal'

Write-Host "Control Panel started (PID: $($proc.Id))" -ForegroundColor Green
