#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()
param(
    [int]$IntervalSeconds = 5
)
$ErrorActionPreference = 'Stop'

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $workspace
$script = Join-Path $root 'nexus_security.py'

if (-not (Test-Path $script)) {
    Write-Host "nexus_security.py not found at $script" -ForegroundColor Yellow
    exit 1
}

$python = $env:LOCALAPPDATA + '\\Programs\\Python\\Python311\\python.exe'
if (-not (Test-Path $python)) {
    $python = 'python'
}

Write-Host "Starting Defensive Security Agent..." -ForegroundColor Cyan
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = '"' + $script + '"'
$psi.WorkingDirectory = $root
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$proc = [System.Diagnostics.Process]::Start($psi)
if ($proc -ne $null) {
    $proc.PriorityClass = 'BelowNormal'
    Write-Host "Security Agent started (PID: $($proc.Id))" -ForegroundColor Green
}
else {
    Write-Host "Failed to start Security Agent" -ForegroundColor Red
}
