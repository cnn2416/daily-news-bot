#!/usr/bin/env pwsh
<#
.每日新闻机器人一键部署脚本
.自动完成所有必要的设置步骤
#>

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 每日新闻机器人 - 一键部署脚本" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# 检查Python
Write-Host "1️⃣ 检查Python环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Python版本: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python未安装或不在PATH中" -ForegroundColor Red
    Write-Host "  请从 https://www.python.org/downloads/ 安装Python 3.8+" -ForegroundColor Yellow
    exit 1
}

# 检查pip
Write-Host "2️⃣ 检查pip..." -ForegroundColor Yellow
$pipVersion = python -m pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ pip可用" -ForegroundColor Green
} else {
    Write-Host "  ❌ pip不可用" -ForegroundColor Red
    Write-Host "  请运行: python -m ensurepip --upgrade" -ForegroundColor Yellow
    exit 1
}

# 安装依赖
Write-Host "3️⃣ 安装依赖包..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  安装依赖包，这可能需要几分钟..." -ForegroundColor Gray
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ 依赖包安装成功" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 依赖包安装失败" -ForegroundColor Red
        Write-Host "  请手动运行: pip install -r requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ requirements.txt 不存在" -ForegroundColor Red
    exit 1
}

# 创建目录结构
Write-Host "4️⃣ 创建目录结构..." -ForegroundColor Yellow
$directories = @("data", "logs", "config", "backup")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ 创建目录: $dir" -ForegroundColor Green
    } else {
        Write-Host "  📁 目录已存在: $dir" -ForegroundColor Gray
    }
}

# 检查配置文件
Write-Host "5️⃣ 检查配置文件..." -ForegroundColor Yellow
$exampleConfig = "config/config.example.yaml"
$userConfig = "config/config.yaml"

if (Test-Path $exampleConfig) {
    Write-Host "  📋 配置文件示例存在" -ForegroundColor Gray
    
    if (-not (Test-Path $userConfig)) {
        Write-Host "  🔧 创建用户配置文件..." -ForegroundColor Yellow
        Copy-Item $exampleConfig $userConfig
        Write-Host "  ✅ 配置文件已创建: $userConfig" -ForegroundColor Green
        Write-Host "    请编辑此文件并填写您的推送密钥" -ForegroundColor Yellow
    } else {
        Write-Host "  📄 用户配置文件已存在: $userConfig" -ForegroundColor Gray
    }
} else {
    Write-Host "  ❌ 配置文件示例不存在: $exampleConfig" -ForegroundColor Red
    exit 1
}

# 运行功能测试
Write-Host "6️⃣ 运行功能测试..." -ForegroundColor Yellow
if (Test-Path "test.py") {
    Write-Host "  运行完整功能测试..." -ForegroundColor Gray
    python test.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ 功能测试通过" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  功能测试未完全通过，请查看上面的输出" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ 测试脚本不存在" -ForegroundColor Red
}

# 显示Git设置指南
Write-Host "7️⃣ Git和GitHub设置..." -ForegroundColor Yellow
Write-Host "  如需推送到GitHub，请按以下步骤操作：" -ForegroundColor Gray
Write-Host "  ==========================================" -ForegroundColor Gray
Write-Host "  1. 初始化Git仓库:" -ForegroundColor Gray
Write-Host "     git init" -ForegroundColor White
Write-Host "     git add ." -ForegroundColor White
Write-Host "     git commit -m 'feat: 初始提交 - 每日新闻机器人'" -ForegroundColor White
Write-Host "  " -ForegroundColor Gray
Write-Host "  2. 连接到GitHub远程仓库:" -ForegroundColor Gray
Write-Host "     git remote add origin https://github.com/你的用户名/仓库名.git" -ForegroundColor White
Write-Host "     git push -u origin main" -ForegroundColor White
Write-Host "  " -ForegroundColor Gray
Write-Host "  3. 在GitHub仓库设置Secrets:" -ForegroundColor Gray
Write-Host "     Settings → Secrets and variables → Actions → New repository secret" -ForegroundColor White
Write-Host "     添加: SERVERCHAN_KEY (你的Server酱SCKEY)" -ForegroundColor White

# 显示下一步操作
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🎉 部署完成！" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 下一步操作:" -ForegroundColor Yellow
Write-Host "  1. 编辑配置文件:" -ForegroundColor White
Write-Host "     notepad config/config.yaml" -ForegroundColor Gray
Write-Host "     填写你的Server酱SCKEY等推送配置" -ForegroundColor Gray
Write-Host "  " -ForegroundColor White
Write-Host "  2. 测试完整功能:" -ForegroundColor White
Write-Host "     python daily_tech_news_bot.py --test" -ForegroundColor Gray
Write-Host "     这会在不推送的情况下测试所有功能" -ForegroundColor Gray
Write-Host "  " -ForegroundColor White
Write-Host "  3. 实际运行（会推送消息）:" -ForegroundColor White
Write-Host "     python daily_tech_news_bot.py" -ForegroundColor Gray
Write-Host "     确保已正确配置推送密钥" -ForegroundColor Gray
Write-Host "  " -ForegroundColor White
Write-Host "  4. 设置定时任务（Windows）:" -ForegroundColor White
Write-Host "     在任务计划程序中创建任务" -ForegroundColor Gray
Write-Host "     每天8点运行: python daily_tech_news_bot.py" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 更多信息请查看:" -ForegroundColor Yellow
Write-Host "  • README.md - 完整功能文档" -ForegroundColor Gray
Write-Host "  • config/config.example.yaml - 配置示例" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 温馨提示:" -ForegroundColor Cyan
Write-Host "  • 确保有稳定的网络连接" -ForegroundColor Gray
Write-Host "  • Server酱SCKEY需要微信扫码绑定" -ForegroundColor Gray
Write-Host "  • 首次运行可能需要较长时间（抓取100+新闻源）" -ForegroundColor Gray
Write-Host "  • 查看日志: data/ 和 logs/ 目录" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✨ 祝您使用愉快！" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# 询问是否要测试
Write-Host ""
$testChoice = Read-Host "是否立即运行测试? (y/n)"
if ($testChoice -eq 'y' -or $testChoice -eq 'Y') {
    Write-Host "运行测试..." -ForegroundColor Yellow
    python daily_tech_news_bot.py --test
}