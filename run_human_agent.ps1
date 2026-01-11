# Runs the Human Interface Agent with BelowNormal priority and minimal CPU pressure
[CmdletBinding()]
param(
    [switch]$Demo
)

$ErrorActionPreference = 'Stop'

function Get-CpuUsage {
    (Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue
}

Write-Host "Starting Human Interface Agent..." -ForegroundColor Cyan
$python = "C:\\Users\\selam\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
$script = Join-Path $PWD 'human_interface_agent.py'

$priority = 'BelowNormal'

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = "`"$script`""
$psi.UseShellExecute = $true
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal

$proc = [System.Diagnostics.Process]::Start($psi)
$proc.PriorityClass = $priority

Write-Host "Process started: $($proc.Id) (Priority: $priority)" -ForegroundColor Green

# Light monitoring loop (optional)
for ($i = 0; $i -lt 5; $i++) {
    Start-Sleep -Seconds 1
    try {
        $cpu = [math]::Round((Get-CpuUsage), 1)
        Write-Host "CPU: $cpu%" -ForegroundColor Yellow
    } catch {}
}

Write-Host "Agent launched. Check nexus_logs/human_agent.log" -ForegroundColor Cyan
