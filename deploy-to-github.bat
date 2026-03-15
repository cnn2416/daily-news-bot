@echo off
echo ======================================================================
echo 🚀 GitHub自动化部署脚本 - Windows批处理版
echo ======================================================================
echo.

REM 检查Git是否安装
echo 1️⃣ 检查Git环境...
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Git已安装
) else (
    echo   ❌ Git未安装
    echo   请从 https://git-scm.com/downloads 安装Git
    pause
    exit /b 1
)

REM 获取GitHub仓库信息
echo.
echo 2️⃣ 配置GitHub仓库...
set /p repoName="请输入GitHub仓库名称 (例如: daily-news-bot): "
set /p githubUsername="请输入您的GitHub用户名: "

if "%repoName%"=="" (
    echo   ❌ 必须提供仓库名称
    pause
    exit /b 1
)
if "%githubUsername%"=="" (
    echo   ❌ 必须提供GitHub用户名
    pause
    exit /b 1
)

set repoUrl=https://github.com/%githubUsername%/%repoName%.git
echo   仓库URL: %repoUrl%

REM 初始化Git仓库
echo.
echo 3️⃣ 初始化Git仓库...
if exist ".git" (
    echo   ⚠️  Git仓库已存在
    set /p choice="是否重新初始化? (y/n): "
    if /i "%choice%"=="y" (
        rmdir /s /q .git >nul 2>&1
        echo   ✅ 已删除旧的.git目录
    )
)

if not exist ".git" (
    git init
    echo   ✅ Git仓库初始化完成
)

REM 添加文件
echo.
echo 4️⃣ 添加文件到Git...
git add .
echo   ✅ 文件已添加到暂存区

REM 提交
echo.
echo 5️⃣ 提交初始版本...
git commit -m "feat: 初始提交 - 每日新闻机器人 v1.0.0

- 马斯克和特朗普单独新闻专栏
- 英文新闻自动添加中文描述
- 多渠道推送支持 (ServerChan/Telegram/WeCom)
- GitHub Actions自动化每日推送"
if %errorlevel% equ 0 (
    echo   ✅ 提交完成
) else (
    echo   ⚠️  提交时遇到问题，但继续...
)

REM 设置远程仓库
echo.
echo 6️⃣ 设置GitHub远程仓库...
git remote add origin %repoUrl% >nul 2>&1
if %errorlevel% neq 0 (
    echo   ⚠️  远程仓库可能已存在，更新URL
    git remote set-url origin %repoUrl%
)
echo   ✅ 远程仓库已设置: %repoUrl%

REM 创建主分支
echo.
echo 7️⃣ 创建主分支...
git branch -M main >nul 2>&1
echo   ✅ 主分支已创建

REM 推送到GitHub
echo.
echo 8️⃣ 推送到GitHub...
echo   正在推送到 %repoUrl%
git push -u origin main

if %errorlevel% equ 0 (
    echo   ✅ 推送成功!
) else (
    echo   ❌ 推送失败
    echo   可能是以下原因：
    echo   1. 仓库不存在，请在GitHub创建仓库: %repoName%
    echo   2. 网络连接问题
    echo   3. 认证问题
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo 🎉 GitHub仓库部署完成!
echo ======================================================================
echo.
echo 🚀 下一步配置GitHub Actions自动化：
echo   1. 访问您的GitHub仓库: https://github.com/%githubUsername%/%repoName%
echo   2. 点击 Settings → Secrets and variables → Actions
echo   3. 点击 New repository secret
echo   4. 添加以下Secrets:
echo      • SERVERCHAN_SENDKEY - 您的Server酱SendKey
echo   5. GitHub Actions会自动在每天8:00(北京时间)运行
echo.
echo 📅 GitHub Actions推送时间：
echo   • 每天 UTC 0:00 (北京时间 8:00)
echo   • 可手动在Actions页面触发
echo.
echo 🔍 检查部署状态：
echo   1. 访问Actions页面: https://github.com/%githubUsername%/%repoName%/actions
echo   2. 点击 '每日科技日报推送' 工作流
echo   3. 点击 'Run workflow' 手动测试
echo.
echo ======================================================================
echo ✨ 部署完成！明天早上8点您将收到第一条推送
echo ======================================================================
pause