# NEXUS-ONE Keep Awake Script
# Prevents computer from sleeping during 3-hour development session

param(
    [int]$DurationMinutes = 180,  # 3 hours default
    [int]$CheckIntervalSeconds = 30
)

Write-Host "🚀 NEXUS-ONE Keep Awake Active - Duration: $DurationMinutes minutes" -ForegroundColor Cyan
Write-Host "⏰ Started at: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Green

# Prevent sleep using SetThreadExecutionState
Add-Type @'
using System;
using System.Runtime.InteropServices;

public class SleepUtil {
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
    
    public const uint ES_CONTINUOUS = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED = 0x00000001;
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;
    public const uint ES_AWAYMODE_REQUIRED = 0x00000040;
}
'@

# Keep system awake
$result = [SleepUtil]::SetThreadExecutionState(
    [SleepUtil]::ES_CONTINUOUS -bor 
    [SleepUtil]::ES_SYSTEM_REQUIRED -bor 
    [SleepUtil]::ES_DISPLAY_REQUIRED
)

if ($result -eq 0) {
    Write-Host "⚠️  Warning: Could not set execution state" -ForegroundColor Yellow
}
else {
    Write-Host "✅ Sleep mode prevention activated" -ForegroundColor Green
}

$endTime = (Get-Date).AddMinutes($DurationMinutes)
$iterations = 0

try {
    while ((Get-Date) -lt $endTime) {
        $iterations++
        $remaining = ($endTime - (Get-Date)).TotalMinutes
        
        # Send key event to keep system active (invisible)
        $wsh = New-Object -ComObject WScript.Shell
        $wsh.SendKeys('+{F15}')  # Shift+F15 - doesn't do anything visible
        
        # Display status every 10 iterations (5 minutes)
        if ($iterations % 10 -eq 0) {
            Write-Host "⚡ Active - Remaining: $([math]::Round($remaining, 1)) minutes - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
        }
        
        Start-Sleep -Seconds $CheckIntervalSeconds
    }
    
    Write-Host "`n✅ Session completed successfully at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
}
finally {
    # Restore normal power settings
    [SleepUtil]::SetThreadExecutionState([SleepUtil]::ES_CONTINUOUS)
    Write-Host "🔄 Normal power settings restored" -ForegroundColor Yellow
}
