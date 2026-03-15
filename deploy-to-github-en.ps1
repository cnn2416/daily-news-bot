Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "GitHub Auto Deployment Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Git
Write-Host "1. Checking Git environment..." -ForegroundColor Yellow
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Git version: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Git not installed" -ForegroundColor Red
    Write-Host "  Please install Git from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Get GitHub repository info
Write-Host ""
Write-Host "2. Configuring GitHub repository..." -ForegroundColor Yellow
$repoName = Read-Host "Enter GitHub repository name (e.g. daily-news-bot)"
$githubUsername = Read-Host "Enter your GitHub username"

if ([string]::IsNullOrEmpty($repoName) -or [string]::IsNullOrEmpty($githubUsername)) {
    Write-Host "  [ERROR] Repository name and username are required" -ForegroundColor Red
    exit 1
}

$repoUrl = "https://github.com/$githubUsername/$repoName.git"
Write-Host "  Repository URL: $repoUrl" -ForegroundColor Gray

# Check if already a Git repository
Write-Host ""
Write-Host "3. Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "  [WARNING] Git repository already exists" -ForegroundColor Yellow
    $choice = Read-Host "Reinitialize? (y/n)"
    if ($choice -eq 'y') {
        Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
        Write-Host "  [OK] Removed old .git directory" -ForegroundColor Green
    }
}

if (-not (Test-Path ".git")) {
    git init
    Write-Host "  [OK] Git repository initialized" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "4. Adding files to Git..." -ForegroundColor Yellow
git add .
$fileCount = (git status --porcelain | Measure-Object).Count
Write-Host "  [OK] Added $fileCount files" -ForegroundColor Green

# Commit initial version
Write-Host ""
Write-Host "5. Committing initial version..." -ForegroundColor Yellow
git commit -m "feat: initial commit - Daily News Bot v1.0.0

- Elon Musk and Donald Trump news columns
- English news with Chinese descriptions
- Multi-channel push support
- GitHub Actions automated daily push"
Write-Host "  [OK] Commit completed" -ForegroundColor Green

# Set remote repository
Write-Host ""
Write-Host "6. Setting GitHub remote repository..." -ForegroundColor Yellow
git remote add origin $repoUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [WARNING] Remote may already exist, updating URL" -ForegroundColor Yellow
    git remote set-url origin $repoUrl
}
Write-Host "  [OK] Remote repository set: $repoUrl" -ForegroundColor Green

# Create main branch
Write-Host ""
Write-Host "7. Creating main branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "  [OK] Main branch created" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "8. Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "  Pushing to $repoUrl" -ForegroundColor Gray
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Push successful!" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Push failed" -ForegroundColor Red
    Write-Host "  Possible reasons:" -ForegroundColor Yellow
    Write-Host "  1. Repository doesn't exist, create it on GitHub: $repoName" -ForegroundColor Gray
    Write-Host "  2. Network connection issue" -ForegroundColor Gray
    Write-Host "  3. Authentication issue" -ForegroundColor Gray
    exit 1
}

# Show next steps
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "GitHub repository deployment completed!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps for GitHub Actions automation:" -ForegroundColor Yellow
Write-Host "  1. Go to your GitHub repository: https://github.com/$githubUsername/$repoName" -ForegroundColor Gray
Write-Host "  2. Click Settings -> Secrets and variables -> Actions" -ForegroundColor Gray
Write-Host "  3. Click New repository secret" -ForegroundColor Gray
Write-Host "  4. Add these Secrets:" -ForegroundColor Gray
Write-Host "     - SERVERCHAN_SENDKEY - Your Server酱 SendKey" -ForegroundColor White
Write-Host "  5. GitHub Actions will run automatically at 8:00 AM Beijing time daily" -ForegroundColor Gray

Write-Host ""
Write-Host "GitHub Actions push schedule:" -ForegroundColor Cyan
Write-Host "  - Daily at UTC 0:00 (8:00 AM Beijing time)" -ForegroundColor Gray
Write-Host "  - Can be triggered manually from Actions page" -ForegroundColor Gray

Write-Host ""
Write-Host "Check deployment status:" -ForegroundColor Cyan
Write-Host "  1. Go to Actions page: https://github.com/$githubUsername/$repoName/actions" -ForegroundColor Gray
Write-Host "  2. Click 'Daily News Push' workflow" -ForegroundColor Gray
Write-Host "  3. Click 'Run workflow' to manually test" -ForegroundColor Gray

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Deployment complete! You'll receive first push tomorrow at 8:00 AM" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan