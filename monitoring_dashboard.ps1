# NEXUS-ONE Real-Time Monitoring & Dashboard
# WebSocket & Real-time stats, alerts, performance tracking

param(
    [int]$RefreshIntervalSeconds = 5,
    [string]$DashboardPort = "8080"
)

function Write-Dashboard {
    Clear-Host
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $uptime = (Get-Uptime -ErrorAction SilentlyContinue).ToString().Split('.')[0]
    
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         NEXUS-ONE ADVANCED AUTONOMOUS SYSTEM DASHBOARD         ║" -ForegroundColor Cyan
    Write-Host "╠════════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
    
    # System Status
    Write-Host "║ 🔷 SYSTEM STATUS" -ForegroundColor Magenta
    Write-Host "║  Timestamp:  $timestamp" -ForegroundColor Gray
    Write-Host "║  Status:     🟢 ACTIVE ($(if ($uptime) { $uptime } else { 'N/A' }))" -ForegroundColor Green
    Write-Host "║" -ForegroundColor Cyan
    
    # Git Repository Stats
    try {
        $commits = (& git rev-list --all --count)
        $branches = (& git branch -r | Measure-Object -Line).Lines
        $lastCommit = (& git log -1 --format=%ci)
        $status = & git status --short
        $changedFiles = ($status | Measure-Object -Line).Lines
        
        Write-Host "║ 📊 GIT REPOSITORY" -ForegroundColor Green
        Write-Host "║  Total Commits:   $commits" -ForegroundColor Gray
        Write-Host "║  Remote Branches: $branches" -ForegroundColor Gray
        Write-Host "║  Last Commit:     $(($lastCommit -split ' ')[0])" -ForegroundColor Gray
        Write-Host "║  Changed Files:   $changedFiles" -ForegroundColor Yellow
        Write-Host "║" -ForegroundColor Cyan
    }
    catch { }
    
    # File System Stats
    try {
        $totalSize = (Get-ChildItem -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
        $pythonCount = (Get-ChildItem -Path . -Filter "*.py" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        $tsCount = (Get-ChildItem -Path . -Filter "*.ts" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        
        Write-Host "║ 📁 PROJECT STRUCTURE" -ForegroundColor Green
        Write-Host "║  Total Size:      $([math]::Round($totalSize, 2)) MB" -ForegroundColor Gray
        Write-Host "║  Python Files:    $pythonCount" -ForegroundColor Gray
        Write-Host "║  TypeScript Files: $tsCount" -ForegroundColor Gray
        Write-Host "║" -ForegroundColor Cyan
    }
    catch { }
    
    # Process Status
    try {
        $syncProcess = Get-Process -Name powershell -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*autonomous*" }
        $pyProcess = Get-Process -Name python -ErrorAction SilentlyContinue | Measure-Object
        $nodeProcess = Get-Process -Name node -ErrorAction SilentlyContinue | Measure-Object
        
        Write-Host "║ ⚙️  PROCESS STATUS" -ForegroundColor Green
        Write-Host "║  Sync Script:     $(if ($syncProcess) { "🟢 Running" } else { "🔴 Stopped" })" -ForegroundColor Gray
        Write-Host "║  Python Procs:    $($pyProcess.Count)" -ForegroundColor Gray
        Write-Host "║  Node Procs:      $($nodeProcess.Count)" -ForegroundColor Gray
        Write-Host "║" -ForegroundColor Cyan
    }
    catch { }
    
    # Network Status
    try {
        $githubTest = Test-Connection github.com -Count 1 -Quiet -ErrorAction SilentlyContinue
        $localRepoCheck = Test-Path .\.git
        
        Write-Host "║ 🌐 NETWORK STATUS" -ForegroundColor Green
        Write-Host "║  GitHub:          $(if ($githubTest) { "🟢 Connected" } else { "🔴 Unreachable" })" -ForegroundColor Gray
        Write-Host "║  Local Repo:      $(if ($localRepoCheck) { "🟢 Initialized" } else { "🔴 Not Found" })" -ForegroundColor Gray
        Write-Host "║" -ForegroundColor Cyan
    }
    catch { }
    
    # Performance Metrics
    try {
        $cpuUsage = (Get-Counter -Counter "\Processor(_Total)\% Processor Time" -ErrorAction SilentlyContinue).CounterSamples[0].CookedValue
        $memUsage = (Get-Counter -Counter "\Memory\% Committed Bytes In Use" -ErrorAction SilentlyContinue).CounterSamples[0].CookedValue
        
        Write-Host "║ 📈 PERFORMANCE METRICS" -ForegroundColor Green
        Write-Host "║  CPU Usage:       $([math]::Round($cpuUsage, 2))%" -ForegroundColor Gray
        Write-Host "║  Memory Usage:    $([math]::Round($memUsage, 2))%" -ForegroundColor Gray
        Write-Host "║" -ForegroundColor Cyan
    }
    catch { }
    
    # Recent Logs
    try {
        $logFile = ".\.nexus_sync.log"
        if (Test-Path $logFile) {
            $recentLogs = Get-Content $logFile -Tail 5 -ErrorAction SilentlyContinue
            Write-Host "║ 📝 RECENT ACTIVITY" -ForegroundColor Green
            foreach ($log in $recentLogs) {
                $logLine = $log.Substring(0, [System.Math]::Min($log.Length, 60))
                Write-Host "║  $logLine" -ForegroundColor Gray
            }
            Write-Host "║" -ForegroundColor Cyan
        }
    }
    catch { }
    
    # Footer
    Write-Host "╠════════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
    Write-Host "║ 🚀 NEXUS-ONE Advanced Autonomous System v2.0" -ForegroundColor Yellow
    Write-Host "║ Auto-refresh her $RefreshIntervalSeconds saniyede | Press Ctrl+C çıkmak için" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
}

# Real-time Dashboard Loop
Write-Host "🔄 NEXUS-ONE Dashboard başlatıldı..." -ForegroundColor Green
Start-Sleep -Seconds 1

while ($true) {
    Write-Dashboard
    Start-Sleep -Seconds $RefreshIntervalSeconds
}
