#!/usr/bin/env pwsh
<#
.GitHub仓库部署脚本
.自动将每日新闻机器人推送到GitHub并配置自动化推送
#>

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 GitHub自动化部署脚本" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# 检查Git
Write-Host "1️⃣ 检查Git环境..." -ForegroundColor Yellow
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Git版本: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Git未安装" -ForegroundColor Red
    Write-Host "  请从 https://git-scm.com/downloads 安装Git" -ForegroundColor Yellow
    exit 1
}

# 获取GitHub仓库信息
Write-Host "`n2️⃣ 配置GitHub仓库..." -ForegroundColor Yellow
$repoName = Read-Host "请输入GitHub仓库名称 (例如: daily-news-bot)"
$githubUsername = Read-Host "请输入您的GitHub用户名"

if ([string]::IsNullOrEmpty($repoName) -or [string]::IsNullOrEmpty($githubUsername)) {
    Write-Host "  ❌ 必须提供仓库名称和用户名" -ForegroundColor Red
    exit 1
}

$repoUrl = "https://github.com/$githubUsername/$repoName.git"
Write-Host "  仓库URL: $repoUrl" -ForegroundColor Gray

# 检查当前目录是否是Git仓库
Write-Host "`n3️⃣ 初始化Git仓库..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "  ⚠️  Git仓库已存在" -ForegroundColor Yellow
    $choice = Read-Host "是否重新初始化? (y/n)"
    if ($choice -eq 'y') {
        Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
        Write-Host "  ✅ 已删除旧的.git目录" -ForegroundColor Green
    }
}

if (-not (Test-Path ".git")) {
    git init
    Write-Host "  ✅ Git仓库初始化完成" -ForegroundColor Green
}

# 添加所有文件
Write-Host "`n4️⃣ 添加文件到Git..." -ForegroundColor Yellow
git add .
$fileCount = (git status --porcelain | Measure-Object).Count
Write-Host "  ✅ 添加了 $fileCount 个文件" -ForegroundColor Green

# 提交初始版本
Write-Host "`n5️⃣ 提交初始版本..." -ForegroundColor Yellow
git commit -m "feat: 初始提交 - 每日新闻机器人 v1.0.0

- 马斯克和特朗普单独新闻专栏
- 英文新闻自动添加中文描述
- 多渠道推送支持 (ServerChan/Telegram/WeCom)
- GitHub Actions自动化每日推送"
Write-Host "  ✅ 提交完成" -ForegroundColor Green

# 设置远程仓库
Write-Host "`n6️⃣ 设置GitHub远程仓库..." -ForegroundColor Yellow
git remote add origin $repoUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠️  远程仓库可能已存在，更新URL" -ForegroundColor Yellow
    git remote set-url origin $repoUrl
}
Write-Host "  ✅ 远程仓库已设置: $repoUrl" -ForegroundColor Green

# 创建主分支
Write-Host "`n7️⃣ 创建主分支..." -ForegroundColor Yellow
git branch -M main
Write-Host "  ✅ 主分支已创建" -ForegroundColor Green

# 推送到GitHub
Write-Host "`n8️⃣ 推送到GitHub..." -ForegroundColor Yellow
Write-Host "  正在推送到 $repoUrl" -ForegroundColor Gray
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ 推送成功!" -ForegroundColor Green
} else {
    Write-Host "  ❌ 推送失败" -ForegroundColor Red
    Write-Host "  可能是以下原因：" -ForegroundColor Yellow
    Write-Host "  1. 仓库不存在，请在GitHub创建仓库: $repoName" -ForegroundColor Gray
    Write-Host "  2. 网络连接问题" -ForegroundColor Gray
    Write-Host "  3. 认证问题" -ForegroundColor Gray
    exit 1
}

# 显示后续步骤
Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "🎉 GitHub仓库部署完成!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 下一步配置GitHub Actions自动化：" -ForegroundColor Yellow
Write-Host "  1. 访问您的GitHub仓库: https://github.com/$githubUsername/$repoName" -ForegroundColor Gray
Write-Host "  2. 点击 Settings → Secrets and variables → Actions" -ForegroundColor Gray
Write-Host "  3. 点击 New repository secret" -ForegroundColor Gray
Write-Host "  4. 添加以下Secrets:" -ForegroundColor Gray
Write-Host "     • SERVERCHAN_SENDKEY - 您的Server酱SendKey" -ForegroundColor White
Write-Host "     • TELEGRAM_BOT_TOKEN - Telegram Bot Token (可选)" -ForegroundColor White
Write-Host "     • TELEGRAM_CHAT_ID - Telegram Chat ID (可选)" -ForegroundColor White
Write-Host "  5. GitHub Actions会自动在每天8:00(北京时间)运行" -ForegroundColor Gray

Write-Host "`n📅 GitHub Actions推送时间：" -ForegroundColor Cyan
Write-Host "  • 每天 UTC 0:00 (北京时间 8:00)" -ForegroundColor Gray
Write-Host "  • 可手动在Actions页面触发" -ForegroundColor Gray

Write-Host "`n🔍 检查部署状态：" -ForegroundColor Cyan
Write-Host "  1. 访问Actions页面: https://github.com/$githubUsername/$repoName/actions" -ForegroundColor Gray
Write-Host "  2. 点击 '每日科技日报推送' 工作流" -ForegroundColor Gray
Write-Host "  3. 点击 'Run workflow' 手动测试" -ForegroundColor Gray

Write-Host "`n💡 推送内容预览：" -ForegroundColor Cyan
Write-Host "  • 🚀 马斯克专栏 (15条)" -ForegroundColor Gray
Write-Host "  • 🎯 特朗普专栏 (15条)" -ForegroundColor Gray
Write-Host "  • 🌍 英文新闻中文描述" -ForegroundColor Gray
Write-Host "  • 📊 每日统计信息" -ForegroundColor Gray

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "✨ 部署完成！明天早上8点您将收到第一条推送" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan