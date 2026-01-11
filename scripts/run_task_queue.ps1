#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()
# Launches the NEXUS-ONE Task Queue with BelowNormal priority
$ErrorActionPreference = 'Stop'

$python = "C:\\Users\\selam\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
$runner = Join-Path $PWD 'tasks/task_queue.py'

Write-Host "Starting Task Queue..." -ForegroundColor Cyan

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = "`"$runner`""
$psi.UseShellExecute = $true
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal

$proc = [System.Diagnostics.Process]::Start($psi)
$proc.PriorityClass = 'BelowNormal'

Write-Host "Task Queue started (PID: $($proc.Id))" -ForegroundColor Green
