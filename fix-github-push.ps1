Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "GitHub Push Fix Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Problem detected: Remote repository already has files" -ForegroundColor Yellow
Write-Host "Repository: https://github.com/cnn2416/daily-news-bot" -ForegroundColor Gray
Write-Host ""

Write-Host "Choose solution:" -ForegroundColor Cyan
Write-Host "1. Force push (overwrite remote repository)" -ForegroundColor Gray
Write-Host "   - Recommended: You want to replace remote files with local ones" -ForegroundColor Gray
Write-Host "2. Pull first then push (merge changes)" -ForegroundColor Gray
Write-Host "   - If remote has files you want to keep" -ForegroundColor Gray
Write-Host "3. Create new repository" -ForegroundColor Gray
Write-Host "   - Use a different repository name" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter choice (1, 2, or 3)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Executing force push..." -ForegroundColor Yellow
    git push -u origin main --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Force push successful!" -ForegroundColor Green
        Write-Host "  Remote repository has been overwritten with your local files" -ForegroundColor Gray
    } else {
        Write-Host "  [ERROR] Force push failed" -ForegroundColor Red
    }
}
elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "Pulling remote changes first..." -ForegroundColor Yellow
    git pull origin main --allow-unrelated-histories
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Pull successful" -ForegroundColor Green
        Write-Host ""
        Write-Host "Now pushing your changes..." -ForegroundColor Yellow
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Push successful!" -ForegroundColor Green
            Write-Host "  Local and remote changes have been merged" -ForegroundColor Gray
        } else {
            Write-Host "  [ERROR] Push failed after pull" -ForegroundColor Red
        }
    } else {
        Write-Host "  [ERROR] Pull failed" -ForegroundColor Red
    }
}
elseif ($choice -eq "3") {
    Write-Host ""
    Write-Host "Creating new repository..." -ForegroundColor Yellow
    $newRepoName = Read-Host "Enter new repository name (e.g. daily-news-bot-v2)"
    
    if (-not [string]::IsNullOrEmpty($newRepoName)) {
        $newRepoUrl = "https://github.com/cnn2416/$newRepoName.git"
        Write-Host "  New repository URL: $newRepoUrl" -ForegroundColor Gray
        
        git remote set-url origin $newRepoUrl
        Write-Host "  [OK] Remote URL updated" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Pushing to new repository..." -ForegroundColor Yellow
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Push to new repository successful!" -ForegroundColor Green
        } else {
            Write-Host "  [ERROR] Push to new repository failed" -ForegroundColor Red
            Write-Host "  You may need to create the repository on GitHub first" -ForegroundColor Yellow
        }
    }
}
else {
    Write-Host "  [ERROR] Invalid choice" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Fix completed" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure GitHub Secrets:" -ForegroundColor Gray
Write-Host "   - SERVERCHAN_SENDKEY with your Server酱 Key" -ForegroundColor Gray
Write-Host "2. Test the workflow manually from GitHub Actions" -ForegroundColor Gray
Write-Host "3. You'll receive daily push at 8:00 AM Beijing time" -ForegroundColor Gray