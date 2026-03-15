# 📰 每日新闻超级增强版机器人

一个专为科技爱好者设计的每日新闻推送机器人，特别关注**马斯克**和**特朗普**的相关新闻，并自动为英文新闻添加中文描述。

## 🎯 核心功能

1. **🤖 马斯克专栏** - 专门收集特斯拉、SpaceX、Neuralink等马斯克相关新闻（最多15条）
2. **🎯 特朗普专栏** - 专门收集特朗普及其相关政治新闻（最多15条）
3. **🌍 英文新闻中文描述** - 自动为英文新闻生成中文翻译/描述
4. **📊 智能分类** - 自动将新闻分为10个类别
5. **🚀 多渠道推送** - 支持多种推送方式
6. **⏰ 自动化运行** - 支持GitHub Actions定时任务

## 📋 功能特性

### 新闻抓取
- **100+ 新闻源** - 覆盖全球主流科技、政治、财经媒体
- **智能去重** - 自动识别重复新闻
- **分类管理** - 10个精心设计的新闻类别
- **优先级排序** - 马斯克和特朗普新闻优先处理

### 翻译功能
- **关键词翻译** - 自动翻译常见英文词汇
- **中文描述** - 为英文新闻提供中文概述
- **双语显示** - 原始标题 + 中文描述

### 推送系统
- **Server酱推送** - 微信推送支持
- **Telegram推送** - Telegram频道/群组支持
- **企业微信推送** - 企业微信机器人支持
- **多格式输出** - 支持文本、Markdown格式

## 🏗️ 系统架构

```
daily-news-bot/
├── main_final.py              # 主程序
├── requirements.txt           # 依赖包
├── .github/workflows/         # GitHub Actions工作流
│   ├── daily-push.yml         # 每日推送工作流
│   └── manual-run.yml         # 手动运行工作流
├── src/                       # 源代码目录
│   ├── scraper_final.py       # 新闻抓取器
│   ├── serverchan_final.py    # Server酱推送
│   └── utils.py              # 工具函数
├── data/                      # 数据目录（自动生成）
├── config/                    # 配置目录
└── logs/                      # 日志目录
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置推送
复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```

编辑 `config/config.yaml`，填写：
- Server酱的 SCKEY
- Telegram Bot Token 和 Chat ID
- 企业微信的 Webhook URL

### 3. 测试运行
```bash
# 测试模式（不推送）
python main_final.py --test

# 完整运行
python main_final.py

# 显示帮助
python main_final.py --help
```

### 4. 设置定时任务（可选）
```bash
# Windows 定时任务
schtasks /create /tn "DailyNewsBot" /tr "python C:\path\to\main_final.py" /sc daily /st 08:00

# Linux/Mac crontab
0 8 * * * cd /path/to/daily-news-bot && python main_final.py
```

## 🔧 配置说明

### 新闻分类
系统自动将新闻分为以下10个类别：
1. **🚀 马斯克专栏** - Elon Musk相关
2. **🎯 特朗普专栏** - Donald Trump相关  
3. **🤖 AI科技前沿** - 人工智能相关
4. **🇺🇸 美国政治** - 美国政治新闻
5. **🌍 国际热点** - 国际新闻
6. **💼 科技商业** - 科技商业新闻
7. **🇨🇳 中国科技** - 中国科技新闻
8. **💰 财经金融** - 财经金融新闻
9. **🛡️ 国防军事** - 国防军事新闻
10. **🚀 能源太空** - 能源和太空新闻

### 推送配置示例
```yaml
serverchan:
  sckey: "SCU1234567890abcdefg"
  enable: true
  
telegram:
  bot_token: "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  chat_id: "-1001234567890"
  enable: false
  
wecom:
  webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=abcdefg"
  enable: false

# 新闻源配置
sources:
  max_per_category: 20
  retry_times: 3
  timeout: 30
```

## ⚙️ GitHub Actions 自动化

### 每日自动推送
1. Fork 本项目到你的 GitHub 仓库
2. 在仓库设置中添加 Secrets：
   - `SERVERCHAN_KEY` - Server酱的 SCKEY
   - `TELEGRAM_BOT_TOKEN` - Telegram Bot Token
   - `TELEGRAM_CHAT_ID` - Telegram Chat ID
3. Actions会自动在每天指定时间运行

### 手动触发
在 GitHub 仓库的 Actions 页面，可以手动运行工作流进行测试。

## 📊 输出示例

```
📰 2025年03月15日 全球新闻简报
==========================================
🚀 超级增强版 | 马斯克+特朗普单独专栏 | 英文新闻带中文描述
==========================================

📊 今日统计:
• 总计新闻: 108 条
• 马斯克专栏: 12 条
• 特朗普专栏: 10 条
• 分类数量: 9 个

🚀 马斯克专栏:
------------------------------
1. Tesla announces new AI breakthrough
   中文: 特斯拉宣布新的AI突破
   来源: Tech News
   链接: https://example.com/tesla-ai

2. SpaceX Starship launch successful
   中文: SpaceX星舰发射成功
   来源: Space News
   链接: https://example.com/spacex-starship
```

## 🛠️ 高级功能

### 自定义新闻源
编辑 `config/sources_custom.yaml` 添加自定义RSS源：
```yaml
custom_sources:
  your_category:
    - url: "https://your-rss-feed.com/rss"
      name: "Your Source Name"
      weight: 1.0  # 优先级权重
```

### 翻译扩展
要使用更好的翻译，可以启用翻译API：
```yaml
translation:
  enable: false
  api: "google"  # 或 "baidu", "deepl"
  key: "your-api-key"
  secret: "your-api-secret"
```

### 高级过滤
```yaml
filters:
  min_title_length: 10
  max_title_length: 200
  block_keywords:
    - "spam"
    - "advertisement"
  allow_domains:
    - "reuters.com"
    - "techcrunch.com"
```

## 🐛 故障排除

### 常见问题

1. **抓取失败**
   ```
   ✅ 解决方案：检查网络连接，调整超时时间
   ```

2. **推送失败**
   ```
   ✅ 解决方案：检查API密钥配置，确保服务可用
   ```

3. **内存不足**
   ```
   ✅ 解决方案：减少抓取数量，增加内存限制
   ```

### 日志查看
```bash
# 查看最新日志
tail -f logs/news_bot.log

# 查看错误日志
cat logs/error.log
```

## 📈 性能优化

### 缓存机制
系统自动缓存新闻数据，避免重复抓取：
- 内存缓存：保存最近的1000条新闻
- 文件缓存：自动清理7天前的数据

### 并行处理
启用并行抓取加速：
```yaml
performance:
  max_workers: 10
  enable_parallel: true
  batch_size: 5
```

## 🔒 安全注意事项

1. **API密钥保护** - 不要将密钥提交到公共仓库
2. **网络请求限制** - 遵守网站的robots.txt规则
3. **数据存储** - 本地存储的新闻数据定期清理
4. **隐私保护** - 不收集个人信息

## 🤝 贡献指南

欢迎提交Pull Request或Issue：
1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

### 开发环境设置
```bash
# 1. 克隆仓库
git clone https://github.com/your-username/daily-news-bot.git

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements-dev.txt

# 4. 运行测试
pytest tests/
```

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 联系方式

- 问题反馈：[GitHub Issues](https://github.com/your-username/daily-news-bot/issues)
- 功能建议：[Discussions](https://github.com/your-username/daily-news-bot/discussions)

## ✨ 更新日志

### v1.0.0 (2025-03-15)
- ✅ 完成超级增强版开发
- ✅ 马斯克和特朗普单独专栏
- ✅ 英文新闻中文描述
- ✅ 完整的多渠道推送
- ✅ GitHub Actions自动化

---

**🚀 开始使用吧！** 让每日新闻推送变得更加智能和个性化。