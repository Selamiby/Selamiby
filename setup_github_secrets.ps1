#Requires -Version 5.0
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVars', '')]
param()
# ============================================================================
# GitHub Secrets Setup Script
# Automatically adds required secrets to GitHub repository
# ============================================================================

param(
    [string]$RepoOwner = "Selamiby",
    [string]$RepoName = "Selamiby"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "GitHub Secrets Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if GitHub CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue

if (-not $ghInstalled) {
    Write-Host "[ERROR] GitHub CLI (gh) not installed!" -ForegroundColor Red
    Write-Host "`nInstall GitHub CLI:" -ForegroundColor Yellow
    Write-Host "  winget install --id GitHub.cli" -ForegroundColor White
    Write-Host "  or download from: https://cli.github.com/`n"
    exit 1
}

# Check authentication
Write-Host "[1] Checking GitHub authentication..." -ForegroundColor Cyan
$authStatus = & gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[INFO] Not authenticated. Running 'gh auth login'..." -ForegroundColor Yellow
    & gh auth login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Authentication failed!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] Authenticated with GitHub" -ForegroundColor Green

# Secret values (will prompt user for real values)
Write-Host "`n[2] Setting up secrets..." -ForegroundColor Cyan
Write-Host "    Repository: $RepoOwner/$RepoName`n"

# VERCEL_TOKEN
Write-Host "[SECRET 1/2] VERCEL_TOKEN" -ForegroundColor Yellow
Write-Host "  Purpose: Deploy to Vercel (optional)"
Write-Host "  Get it from: https://vercel.com/account/tokens"
$vercelToken = Read-Host "  Enter VERCEL_TOKEN (or press Enter to skip)"

if ($vercelToken) {
    Write-Host "  Adding VERCEL_TOKEN..." -ForegroundColor Gray
    $vercelToken | & gh secret set VERCEL_TOKEN -R "$RepoOwner/$RepoName"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] VERCEL_TOKEN added" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] Failed to add VERCEL_TOKEN" -ForegroundColor Red
    }
} else {
    Write-Host "  [SKIPPED] VERCEL_TOKEN" -ForegroundColor Gray
}

# DEPLOY_KEY
Write-Host "`n[SECRET 2/2] DEPLOY_KEY" -ForegroundColor Yellow
Write-Host "  Purpose: SSH deployment key (optional)"
Write-Host "  Generate with: ssh-keygen -t ed25519 -C 'deploy@nexus-one'"
$deployKey = Read-Host "  Enter DEPLOY_KEY (or press Enter to skip)"

if ($deployKey) {
    Write-Host "  Adding DEPLOY_KEY..." -ForegroundColor Gray
    $deployKey | & gh secret set DEPLOY_KEY -R "$RepoOwner/$RepoName"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] DEPLOY_KEY added" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] Failed to add DEPLOY_KEY" -ForegroundColor Red
    }
} else {
    Write-Host "  [SKIPPED] DEPLOY_KEY" -ForegroundColor Gray
}

# List all secrets
Write-Host "`n[3] Current secrets in repository:" -ForegroundColor Cyan
& gh secret list -R "$RepoOwner/$RepoName"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[COMPLETE] GitHub Secrets Setup Done!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Note: Secrets are encrypted and cannot be viewed after setting." -ForegroundColor Gray
Write-Host "If you need to change them, run this script again.`n"
