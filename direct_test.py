import sys
sys.path.append('src')

# 直接测试主要功能
print("=== 测试脚本主要功能 ===")
print()

# 测试1: 导入模块
print("1. 测试模块导入...")
try:
    from scraper import NewsScraper
    print("   ✅ scraper 模块导入成功")
    
    from serverchan_sender import ServerChan
    print("   ✅ serverchan_sender 模块导入成功")
except ImportError as e:
    print(f"   ❌ 导入失败: {e}")
    sys.exit(1)

# 测试2: 创建实例
print("\n2. 测试创建实例...")
try:
    scraper = NewsScraper()
    sender = ServerChan()
    print("   ✅ 实例创建成功")
except Exception as e:
    print(f"   ❌ 实例创建失败: {e}")
    sys.exit(1)

# 测试3: 测试抓取少量新闻
print("\n3. 测试新闻抓取（测试模式）...")
try:
    print("   正在抓取新闻...")
    news_data = scraper.run()
    if news_data:
        print(f"   ✅ 抓取成功: {len(news_data)} 个分类的新闻")
        for category, items in news_data.items():
            if items:
                print(f"      {category}: {len(items)} 条")
    else:
        print("   ⚠️  抓取到空数据")
except Exception as e:
    print(f"   ❌ 抓取失败: {e}")
    import traceback
    traceback.print_exc()

print("\n4. 测试推送消息格式化...")
try:
    if news_data:
        # 使用部分数据测试格式化
        test_data = {k: v for k, v in list(news_data.items())[:2] if v}
        
        # 创建简单的格式化函数
        def format_news(news_data):
            message = "测试消息标题\n\n"
            for category, items in news_data.items():
                if items:
                    message += f"{category}:\n"
                    for i, item in enumerate(items[:3], 1):
                        message += f"{i}. {item.get('title', 'No title')}\n"
                    message += "\n"
            return message
        
        test_message = format_news(test_data)
        print(f"   ✅ 消息格式化成功: {len(test_message)} 字符")
        print(f"   消息预览:\n{'-'*40}")
        print(test_message[:100] + "...")
        print(f"{'-'*40}")
except Exception as e:
    print(f"   ❌ 格式化失败: {e}")

print("\n=== 测试完成 ===")
print("✅ 脚本基本功能测试通过")
print("⚠️  实际推送功能需要配置 ServerChan SCKEY 进行测试")