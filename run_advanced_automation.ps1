# ============================================================================
# NEXUS-ONE Advanced Automation Orchestrator
# Runs all 5 automation features with intelligent scheduling
# ============================================================================

param(
    [switch]$Interactive = $false,
    [int]$IntervalSeconds = 300
)

Write-Host ""
Write-Host "=================================================="
Write-Host "[NEXUS] Advanced Automation Orchestrator"
Write-Host "=================================================="
Write-Host ""

function Run-AdvancedAutomation {
    param([string]$Mode = "full")
    
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Running Advanced Automation..." -ForegroundColor Cyan
    
    # Run Python advanced automation
    $pythonPath = "C:\Users\selam\AppData\Local\Programs\Python\Python311\python.exe"
    
    if (Test-Path $pythonPath) {
        & $pythonPath nexus_advanced_automation.py 2>&1 | ForEach-Object {
            Write-Host $_
        }
        
        # After automation runs, commit changes if any
        if ((git status --porcelain | Measure-Object).Count -gt 0) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Committing automation changes..." -ForegroundColor Green
            git add -A 2>&1 | Out-Null
            git commit -m "chore: advanced automation run $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" 2>&1 | Out-Null
            git push 2>&1 | Out-Null
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Changes committed and pushed" -ForegroundColor Green
        }
    }
    else {
        Write-Host "[ERROR] Python not found at $pythonPath" -ForegroundColor Red
    }
}

# Main loop
if ($Interactive) {
    Run-AdvancedAutomation "interactive"
}
else {
    Write-Host "[INFO] Starting continuous automation (every ${IntervalSeconds}s)..." -ForegroundColor Yellow
    Write-Host "[INFO] Press Ctrl+C to stop`n" -ForegroundColor Yellow
    
    while ($true) {
        Run-AdvancedAutomation "continuous"
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Next run in ${IntervalSeconds}s..." -ForegroundColor Gray
        Start-Sleep -Seconds $IntervalSeconds
    }
}
