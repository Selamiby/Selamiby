# NEXUS-ONE Autonomous Learner - 24/7 Background Service
# =======================================================
# Continuously runs self-learning engine in background
# Auto-restarts on crash, monitors resources, logs everything

param(
    [int]$LearningRate = 5,
    [switch]$Aggressive = $true,
    [int]$CycleDuration = 3600,  # 1 hour per cycle (then restart)
    [switch]$EnableSelfUpdate = $true,
    [int]$UpdateInterval = 86400,  # Self-update every 24 hours
    [string]$LogLevel = "INFO"
)

$ErrorActionPreference = "Continue"
$WorkspaceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = "python"  # Assumes python in PATH

# Logging
$LogDir = Join-Path $WorkspaceRoot "nexus_logs"
$LogFile = Join-Path $LogDir "autonomous_learner.log"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogLine = "$Timestamp - $Level - $Message"
    Add-Content -Path $LogFile -Value $LogLine
    Write-Host $LogLine
}

function Test-ProcessRunning {
    param([string]$ProcessName)
    return (Get-Process -Name $ProcessName -ErrorAction SilentlyContinue) -ne $null
}

function Get-SystemResources {
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    $mem = (Get-Counter '\Memory\% Committed Bytes In Use').CounterSamples.CookedValue
    return @{
        CPU    = [math]::Round($cpu, 1)
        Memory = [math]::Round($mem, 1)
    }
}

Write-Log "=== NEXUS-ONE Autonomous Learner Started ===" "INFO"
Write-Log "Learning Rate: ${LearningRate}x | Aggressive: $Aggressive | Update: $EnableSelfUpdate" "INFO"

# Track last self-update time
$LastSelfUpdateTime = Get-Date

# Main loop
$CycleCount = 0
while ($true) {
    $CycleCount++
    $CycleStart = Get-Date
    
    Write-Log "=== Learning Cycle $CycleCount ===" "INFO"
    
    # Check system resources
    $resources = Get-SystemResources
    Write-Log "System: CPU ${resources.CPU}% | RAM ${resources.Memory}%" "DEBUG"
    
    # Resource throttling (pause if system is overloaded)
    if ($resources.CPU -gt 90 -or $resources.Memory -gt 85) {
        Write-Log "System overloaded (CPU: ${resources.CPU}%, RAM: ${resources.Memory}%) - pausing 60s" "WARN"
        Start-Sleep -Seconds 60
        continue
    }
    
    try {
        # === RUN SELF-LEARNER ===
        Write-Log "Starting self-learner (rate: ${LearningRate}x, duration: ${CycleDuration}s)..." "INFO"
        
        $learnerArgs = @(
            "nexus_self_learner.py",
            "--rate", $LearningRate,
            "--duration", $CycleDuration
        )
        
        if ($Aggressive) {
            $learnerArgs += "--aggressive"
        }
        
        $learnerProcess = Start-Process -FilePath $PythonExe -ArgumentList $learnerArgs `
            -WorkingDirectory $WorkspaceRoot -NoNewWindow -PassThru -Wait
        
        $exitCode = $learnerProcess.ExitCode
        
        if ($exitCode -eq 0) {
            Write-Log "✅ Learning cycle completed successfully" "INFO"
        }
        else {
            Write-Log "⚠️ Learning cycle exited with code $exitCode" "WARN"
        }
        
        # === SELF-UPDATE (periodic) ===
        $timeSinceUpdate = (Get-Date) - $LastSelfUpdateTime
        
        if ($EnableSelfUpdate -and $timeSinceUpdate.TotalSeconds -ge $UpdateInterval) {
            Write-Log "Running self-update (last update: $($timeSinceUpdate.Hours) hours ago)..." "INFO"
            
            $updateArgs = @("nexus_self_updater.py")
            $updateProcess = Start-Process -FilePath $PythonExe -ArgumentList $updateArgs `
                -WorkingDirectory $WorkspaceRoot -NoNewWindow -PassThru -Wait
            
            if ($updateProcess.ExitCode -eq 0) {
                Write-Log "✅ Self-update completed" "INFO"
                $LastSelfUpdateTime = Get-Date
            }
            else {
                Write-Log "⚠️ Self-update failed (code: $($updateProcess.ExitCode))" "WARN"
            }
        }
        
    }
    catch {
        Write-Log "❌ Error in learning cycle: $_" "ERROR"
        Write-Log "Stack trace: $($_.ScriptStackTrace)" "ERROR"
        
        # Wait before retry
        Start-Sleep -Seconds 30
    }
    
    $cycleElapsed = ((Get-Date) - $CycleStart).TotalSeconds
    Write-Log "Cycle $CycleCount completed in ${cycleElapsed}s" "INFO"
    
    # Brief pause between cycles
    Start-Sleep -Seconds 10
}

Write-Log "Autonomous learner stopped" "INFO"
