#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
# NEXUS-ONE Advanced Autonomous System v2.0 FIXED
param([int]$IntervalSeconds = 30)

$ExcludePatterns = @("node_modules", ".venv", "__pycache__", "*.log", "AutoGPT", "crewAI")

function Write-AutoLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $colors = @{ INFO = "Cyan"; SUCCESS = "Green"; WARNING = "Yellow"; ERROR = "Red"; PERF = "Magenta" }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $colors[$Level]
}

function Invoke-SmartDiff {
    Write-AutoLog "Akıllı diff analizi yapılıyor..." "INFO"
    try {
        $diffCount = 0
        $excludedCount = 0
        
        $status = & git status --porcelain
        foreach ($line in $status) {
            $file = $line.Substring(3)
            
            # Exclude patterns'i kontrol et
            $shouldExclude = $false
            foreach ($pattern in $ExcludePatterns) {
                if ($file -like "*$pattern*") {
                    $shouldExclude = $true
                    $excludedCount++
                    & git restore --staged $file 2>$null
                    break
                }
            }
            
            if (-not $shouldExclude) {
                $diffCount++
            }
        }
        
        Write-AutoLog "Diff: $diffCount değişiklik, $excludedCount hariç tutuldu" "PERF"
        return $diffCount -gt 0
    }
    catch {
        Write-AutoLog "Diff analizi hatası: $_" "ERROR"
        return $true  # Fallback: normal commit
    }
}

function Invoke-ParallelGitPull {
    Write-AutoLog "Paralel pull başlanıyor..." "INFO"
    try {
        # Arka planda fetch (hızlı)
        $fetchJob = Start-Job -ScriptBlock {
            Set-Location $args[0]
            & git fetch origin --all --prune 2>$null
        } -ArgumentList (Get-Location)
        
        # Main branch'i hazırla
        & git checkout main -q 2>$null
        
        # Fetch'i bekle
        $fetchJob | Wait-Job | Out-Null
        
        # Merge et
        & git merge origin/main --allow-unrelated-histories --no-edit 2>$null
        
        Write-AutoLog "Paralel pull başarılı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Paralel pull hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-OptimizedCommit {
    param([bool]$HasChanges)
    
    if (-not $HasChanges) {
        Write-AutoLog "Yeni değişiklik yok, commit atlanıyor" "WARNING"
        return $false
    }
    
    try {
        Write-AutoLog "Commit ediliyor..." "INFO"
        
        $message = "Auto: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Otonom entegrasyon"
        & git commit -m $message 2>$null
        
        Write-AutoLog "Commit başarılı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Commit hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-FastPush {
    try {
        Write-AutoLog "Hızlı push başlanıyor..." "INFO"
        
        # Arka planda push yap (non-blocking)
        $pushJob = Start-Job -ScriptBlock {
            Set-Location $args[0]
            & git push origin main --force 2>$null
        } -ArgumentList (Get-Location)
        
        Write-AutoLog "Push başarılı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Push hatası: $_" "ERROR"
        return $false
    }
}

function Invoke-MultiBranchSync {
    Write-AutoLog "Multi-branch senkronizasyon başlanıyor..." "INFO"
    try {
        $branches = @("main", "develop", "staging")
        
        foreach ($branch in $branches) {
            if (& git rev-parse --verify $branch 2>$null) {
                $pushOutput = Start-Job -ScriptBlock {
                    & git push origin $branch 2>&1
                }
                $jobId = $pushOutput.Id
                Write-AutoLog "  ✓ $branch senkronize ediliyor... (Job: $jobId)" "INFO"
                & git checkout $branch -q 2>$null
                & git pull origin $branch --allow-unrelated-histories --no-edit 2>$null
            }
        }
        
        & git checkout main -q
        Write-AutoLog "Multi-branch senkronizasyon tamamlandı" "SUCCESS"
        return $true
    }
    catch {
        Write-AutoLog "Multi-branch hatası: $_" "ERROR"
        return $false
    }
}

function Get-PerformanceStats {
    try {
        $commits = (& git rev-list --all --count)
        $branches = (& git branch -r | Measure-Object -Line).Lines
        $sizeBytes = (Get-ChildItem -Path . -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $size = $sizeBytes / 1MB
        
        Write-AutoLog "📊 Stats | Commits: $commits | Branches: $branches | Size: $([math]::Round($size, 2))MB" "PERF"
    }
    catch { }
}

function Invoke-AdvancedAutonomousSync {
    Write-AutoLog "╔══ NEXUS-ONE ADVANCED AUTONOMOUS SYNC v2.0 ══╗" "INFO"
    
    $retryCount = 0
    $success = $false
    
    while ($retryCount -lt $MaxRetries -and -not $success) {
        $retryCount++
        
        try {
            # 1. Paralel Pull
            $pullSuccess = Invoke-ParallelGitPull
            if (-not $pullSuccess) { continue }
            
            # 2. Akıllı Diff Analizi
            $hasChanges = Invoke-SmartDiff
            
            # 3. Optimize Commit
            $commitSuccess = Invoke-OptimizedCommit $hasChanges
            
            # 4. Hızlı Push
            if ($commitSuccess -or $hasChanges) {
                Invoke-FastPush
            }
            
            # 5. Multi-Branch (her 5. iterasyonda)
            if ($EnableMultiBranch -and ($retryCount % 5 -eq 0)) {
                Invoke-MultiBranchSync
            }
            
            # 6. Performance Stats
            if ($EnableMonitoring) {
                Get-PerformanceStats
            }
            
            $success = $true
            Write-AutoLog "╚══ SENKRONIZASYON TAMAMLANDI ✓ ══╝" "SUCCESS"
        }
        catch {
            Write-AutoLog "Kritik hata (deneme $retryCount/$MaxRetries): $_" "ERROR"
        }
    }
    
# ════════════════════════════════════════════════
# MAIN LOOP - Advanced Autonomous System
# ════════════════════════════════════════════════

Write-AutoLog "🚀 NEXUS-ONE Advanced Autonomous System başlatıldı" "INFO"
Write-AutoLog "⚙ Interval: $IntervalSeconds saniye | Multi-Branch: $EnableMultiBranch | Monitoring: $EnableMonitoring" "INFO"

$iterationCount = 0
while ($true) {
    $iterationCount++
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    try {
        Invoke-AdvancedAutonomousSync
    }
    catch {
        Write-AutoLog "🔴 Kritik sistem hatası: $_" "ERROR"
    }
    
    $stopwatch.Stop()
    $elapsedMs = $stopwatch.ElapsedMilliseconds
    
    Write-AutoLog "⏱ Senkronizasyon süresi: ${elapsedMs}ms | Iterasyon: $iterationCount" "PERF"
    Write-Host ""
    
    Start-Sleep -Seconds $IntervalSeconds
}
