# 🚀 GitHub自动化部署指南

## 📋 前提条件

1. **GitHub账号** - 已有或注册新账号
2. **Server酱SendKey** - 用于微信推送
3. **Git已安装** - 本地需要Git客户端

## 🔧 部署步骤

### 第1步：获取Server酱SendKey

1. 访问 https://sct.ftqq.com/
2. 微信扫码登录
3. 在"发送消息"页面获取SendKey
   - 格式：`SCUxxxxxxxxxxxxx`

### 第2步：部署到GitHub

#### 方法A：使用自动部署脚本（推荐）

运行一键部署脚本：

```powershell
cd "C:\Users\JiaHe\.openclaw\workspace\daily-news-bot"
.\deploy-to-github.ps1
```

按照提示输入：
- **GitHub用户名**：您的GitHub账号
- **仓库名称**：例如 `daily-news-bot`

#### 方法B：手动部署

```bash
# 1. 进入项目目录
cd "C:\Users\JiaHe\.openclaw\workspace\daily-news-bot"

# 2. 初始化Git仓库
git init
git add .
git commit -m "feat: 初始提交 - 每日新闻机器人"

# 3. 连接到GitHub仓库
git remote add origin https://github.com/您的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 第3步：配置GitHub Secrets

推送成功后，配置推送密钥：

1. 访问您的GitHub仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 添加：

| Secret名称 | 说明 | 是否必须 |
|------------|------|----------|
| `SERVERCHAN_SENDKEY` | Server酱SendKey | ✅ 必须 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | ❌ 可选 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | ❌ 可选 |

### 第4步：测试工作流

1. 访问仓库的 **Actions** 页面
2. 点击 **"每日科技日报推送"** 工作流
3. 点击 **"Run workflow"** 手动触发测试
4. 等待运行完成，检查是否收到推送

## ⏰ 推送时间安排

- **自动推送**：每天北京时间 8:00
- **手动触发**：随时在Actions页面手动运行
- **推送内容**：
  - 🚀 马斯克专栏（15条新闻）
  - 🎯 特朗普专栏（15条新闻）
  - 🌍 其他科技新闻（70+条）
  - 📊 每日统计信息

## 📱 接收推送

### Server酱（微信推送）
1. 绑定微信后，每天早上8点自动收到推送
2. 消息包含所有新闻摘要和链接

### Telegram（可选）
1. 创建Telegram Bot
2. 获取Bot Token和Chat ID
3. 配置到GitHub Secrets

## 🔍 监控和维护

### 查看运行状态
1. **Actions日志**：查看每次运行的详细日志
2. **数据文件**：每次运行生成的JSON和Markdown文件
3. **错误通知**：如果运行失败会有标记

### 常见问题处理

#### 问题1：收不到推送
- 检查Server酱SendKey是否正确
- 查看Actions日志是否有错误
- 确认Server酱已绑定微信

#### 问题2：新闻抓取失败
- 可能是网络问题，会自动重试
- 检查新闻源是否可用
- 查看生成的错误日志

#### 问题3：运行时间过长
- 默认超时时间30分钟
- 可以调整超时设置
- 优化新闻源数量

## 🔄 更新项目

如果您修改了脚本，需要更新到GitHub：

```bash
# 提交更改
git add .
git commit -m "fix: 更新配置/功能"
git push origin main

# GitHub Actions会自动使用最新代码
```

## 📊 数据保存

每次运行会自动保存：
- **原始数据**：`data/news_raw_YYYYMMDD_HHMMSS.json`
- **摘要报告**：`data/news_summary_YYYYMMDD_HHMMSS.md`
- **运行日志**：`logs/daily_news_bot.log`

## 🔗 相关链接

- **GitHub仓库**：`https://github.com/您的用户名/仓库名`
- **Server酱官网**：https://sct.ftqq.com/
- **Telegram Bot创建**：https://core.telegram.org/bots
- **GitHub Actions文档**：https://docs.github.com/actions

## ✅ 部署完成验证

1. ✅ 代码已推送到GitHub
2. ✅ GitHub Secrets已配置
3. ✅ 手动运行工作流成功
4. ✅ 收到测试推送消息

**恭喜！部署完成！明天早上8点您将收到第一条自动推送。**