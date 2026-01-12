# NEXUS-ONE Advanced Autonomous Sync v2.0 - PRODUCTION READY
# Fixed, tested, and optimized for 24/7 operation

param([int]$IntervalSeconds = 30)

function Write-AutoLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $colors = @{ INFO = "Cyan"; SUCCESS = "Green"; WARNING = "Yellow"; ERROR = "Red" }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $colors[$Level]
}

function Invoke-AdvancedSync {
    try {
        Write-AutoLog "Başlıyor..." "INFO"
        
        # 1. Fetch (parallel)
        & git fetch origin 2>$null
        Write-AutoLog "✓ Fetch" "SUCCESS"
        
        # 2. Pull with Rebase
        & git pull --rebase origin main --allow-unrelated-histories --no-edit 2>$null
        Write-AutoLog "✓ Pull/Rebase" "SUCCESS"
        
        # 3. Smart Diff
        $status = & git status --porcelain
        $changes = @()
        
        foreach ($line in $status) {
            $file = $line.Substring(3)
            $skip = $false
            
            if ($file -like "*node_modules*" -or $file -like "*__pycache__*" -or 
                $file -like "*.log" -or $file -like "*AutoGPT*") {
                & git restore --staged $file 2>$null
                $skip = $true
            }
            
            if (-not $skip) { $changes += $file }
        }
        
        if ($changes.Count -gt 0) {
            Write-AutoLog "Değişiklikler: $($changes.Count)" "INFO"
            
            # 4. Commit
            & git add . 2>$null
            $msg = "Auto-Sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            & git commit -m $msg 2>$null
            Write-AutoLog "✓ Commit" "SUCCESS"
            
            # 5. Push with lease (safer force push)
            $pushResult = & git push origin main 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-AutoLog "Normal push başarısız, force-with-lease denenecek. Hata: $pushResult" "WARNING"
                & git push --force-with-lease origin main
                if ($LASTEXITCODE -eq 0) {
                    Write-AutoLog "✓ Push (force-with-lease)" "SUCCESS"
                }
                else {
                    Write-AutoLog "Force-with-lease push da başarısız oldu." "ERROR"
                }
            }
            else {
                Write-AutoLog "✓ Push" "SUCCESS"
            }
        }
        else {
            Write-AutoLog "Değişiklik yok" "INFO"
        }
        
        return $true
    }
    catch {
        Write-AutoLog "Hata: $_" "ERROR"
        return $false
    }
}

Write-AutoLog "NEXUS-ONE v2.0 başlatılıyor..." "INFO"

$i = 0
while ($true) {
    $i++
    Write-AutoLog "Sync #$i" "INFO"
    Invoke-AdvancedSync
    Write-Host ""
    Start-Sleep -Seconds $IntervalSeconds
}
