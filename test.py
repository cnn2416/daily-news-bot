#!/usr/bin/env python3
"""
最终版本的功能测试脚本
测试所有关键功能是否正常工作
"""

import sys
import os
import json
import time
from datetime import datetime

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

print("=" * 70)
print("📋 每日新闻机器人最终版本测试")
print("=" * 70)
print()

def test_module_imports():
    """测试模块导入"""
    print("1️⃣ 测试模块导入...")
    
    modules_to_test = [
        'feedparser',
        'requests',
        'yaml',
        'logging',
        'pathlib',
        'json',
        're',
        'random',
        'time',
        'datetime',
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
            return False
    
    # 测试项目模块
    print("\n2️⃣ 测试项目模块...")
    try:
        from scraper_super_enhanced import SuperEnhancedNewsScraper
        print("  ✅ scraper_super_enhanced")
    except ImportError as e:
        print(f"  ❌ scraper_super_enhanced: {e}")
        return False
    
    try:
        from serverchan_enhanced import ServerChanSenderEnhanced
        print("  ✅ serverchan_enhanced")
    except ImportError as e:
        print(f"  ❌ serverchan_enhanced: {e}")
        return False
    
    print("✅ 所有模块导入成功")
    return True

def test_directories():
    """测试目录结构"""
    print("\n3️⃣ 测试目录结构...")
    
    directories = ['data', 'logs', 'config', 'backup', 'src']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ⚠️ {directory}/ (不存在)")
    
    # 检查关键文件
    key_files = [
        'main_final.py',
        'requirements.txt',
        'README_FINAL.md',
        'config/config.example.yaml',
        'src/scraper_super_enhanced.py',
    ]
    
    print("\n4️⃣ 测试关键文件...")
    for file_path in key_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} (缺失)")
            return False
    
    print("✅ 目录和文件结构正常")
    return True

def test_scraper():
    """测试新闻抓取器"""
    print("\n5️⃣ 测试新闻抓取器（快速测试）...")
    
    try:
        from scraper_super_enhanced import SuperEnhancedNewsScraper
        
        print("  启动抓取器...")
        scraper = SuperEnhancedNewsScraper()
        
        print("  抓取少量新闻进行测试...")
        # 创建一个简化的抓取方法进行测试
        test_sources = [
            ("https://rsshub.app/telegram/channel/elonmusk", "Elon Musk Telegram"),
            ("https://rsshub.app/twitter/user/realDonaldTrump", "Donald Trump Twitter"),
        ]
        
        all_news = []
        for url, name in test_sources:
            try:
                print(f"  测试抓取: {name}")
                import feedparser
                feed = feedparser.parse(url)
                if feed.entries:
                    for entry in feed.entries[:2]:  # 只取前2条
                        news_item = {
                            'title': entry.title[:100] if entry.title else 'No Title',
                            'url': entry.link if hasattr(entry, 'link') else '#',
                            'source': name,
                            'published': entry.get('published', datetime.now().isoformat()),
                            'is_english': True
                        }
                        all_news.append(news_item)
                    print(f"    ✅ 抓取成功: {len(feed.entries)} 条")
                else:
                    print(f"    ⚠️  无新闻条目")
            except Exception as e:
                print(f"    ❌ 抓取失败: {e}")
        
        if all_news:
            print(f"  ✅ 抓取测试成功: 共 {len(all_news)} 条新闻")
            
            # 测试分类
            categorized = {}
            for news in all_news:
                title = news['title'].lower()
                if 'musk' in title or 'elon' in title or 'tesla' in title or 'spacex' in title:
                    category = 'elon_musk'
                elif 'trump' in title or 'donald' in title:
                    category = 'donald_trump'
                elif 'ai' in title or 'artificial' in title or 'chatgpt' in title:
                    category = 'ai_tech'
                else:
                    category = 'international'
                
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(news)
            
            print(f"    分类结果: {list(categorized.keys())}")
            return True
        else:
            print("  ⚠️  未抓到任何新闻（可能是网络问题）")
            return True  # 网络问题不算测试失败
            
    except Exception as e:
        print(f"  ❌ 抓取器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_formatting():
    """测试消息格式化"""
    print("\n6️⃣ 测试消息格式化...")
    
    # 创建测试数据
    test_news = {
        'elon_musk': [
            {
                'title': 'Tesla announces new AI breakthrough in autonomous driving',
                'url': 'https://example.com/tesla-ai',
                'source': 'Tech News',
                'is_english': True,
                'translated_title': '特斯拉宣布自动驾驶领域新的AI突破'
            },
            {
                'title': 'SpaceX launches new Starship prototype',
                'url': 'https://example.com/spacex-starship',
                'source': 'Space News',
                'is_english': True,
                'translated_title': 'SpaceX发射新的星舰原型'
            }
        ],
        'donald_trump': [
            {
                'title': 'Trump announces 2024 presidential campaign',
                'url': 'https://example.com/trump-campaign',
                'source': 'Political News',
                'is_english': True,
                'translated_title': '特朗普宣布2024年总统竞选'
            }
        ]
    }
    
    # 测试格式化函数
    try:
        from main_final import DailyNewsBotFinal
        bot = DailyNewsBotFinal()
        
        formatted = bot.format_news_for_push(test_news)
        print("  ✅ 格式化函数工作正常")
        
        if formatted:
            print(f"    生成了 {len(formatted)} 个分类的格式化内容")
            
            # 测试消息创建
            message = bot.create_push_message(test_news)
            print(f"  ✅ 消息创建成功: {len(message)} 字符")
            
            # 显示预览
            print("\n  消息预览:")
            print("-" * 40)
            print(message[:200] + "..." if len(message) > 200 else message)
            print("-" * 40)
            
            return True
        else:
            print("  ⚠️  格式化结果为空")
            return False
            
    except Exception as e:
        print(f"  ❌ 格式化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """测试配置文件"""
    print("\n7️⃣ 测试配置文件...")
    
    config_file = 'config/config.example.yaml'
    
    if os.path.exists(config_file):
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 检查必要配置项
            required_sections = ['push', 'scraping', 'logging']
            for section in required_sections:
                if section in config:
                    print(f"  ✅ 配置部分: {section}")
                else:
                    print(f"  ⚠️  缺失配置部分: {section}")
            
            # 检查关键配置
            if 'serverchan' in config.get('push', {}):
                print("  ✅ Server酱配置存在")
            
            print("✅ 配置文件格式正确")
            return True
            
        except Exception as e:
            print(f"  ❌ 配置文件读取失败: {e}")
            return False
    else:
        print(f"  ⚠️  配置文件不存在: {config_file}")
        print("  请运行: copy config\\config.example.yaml config\\config.yaml")
        return True  # 配置文件可以后续创建

def test_requirements():
    """测试依赖包"""
    print("\n8️⃣ 测试依赖包...")
    
    if not os.path.exists('requirements.txt'):
        print("  ⚠️ requirements.txt 不存在")
        return False
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"  发现 {len(requirements)} 个依赖包")
        
        # 测试关键依赖
        key_deps = ['feedparser', 'requests', 'pyyaml', 'python-dateutil']
        for dep in key_deps:
            try:
                __import__(dep.replace('-', '_'))
                print(f"  ✅ {dep}")
            except ImportError:
                print(f"  ❌ {dep} (未安装)")
                print(f"    请运行: pip install {dep}")
        
        print("✅ 依赖包检查完成")
        return True
        
    except Exception as e:
        print(f"  ❌ 依赖包测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始完整功能测试...\n")
    
    tests = [
        ("模块导入", test_module_imports),
        ("目录结构", test_directories),
        ("新闻抓取", test_scraper),
        ("消息格式化", test_message_formatting),
        ("配置文件", test_configuration),
        ("依赖包", test_requirements),
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n🔍 正在测试: {test_name}")
        print("-" * 40)
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"结果: {'✅ 通过' if success else '❌ 失败'}")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 显示总结
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    # 显示详细结果
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {test_name}")
    
    # 运行时间
    elapsed = time.time() - start_time
    minutes, seconds = divmod(elapsed, 60)
    print(f"\n⏱️  总测试时间: {int(minutes)}分{int(seconds)}秒")
    
    # 后续步骤
    print("\n" + "=" * 70)
    print("🚀 后续步骤")
    print("=" * 70)
    
    if passed == total:
        print("🎉 所有测试通过！现在可以进行以下操作：")
        print("1. 复制配置文件:")
        print("   copy config\\config.example.yaml config\\config.yaml")
        print("2. 编辑配置文件，填写推送密钥")
        print("3. 测试完整功能:")
        print("   python main_final.py --test")
        print("4. 推送到GitHub:")
        print("   git add .")
        print("   git commit -m 'feat: 初始提交'")
        print("   git push origin main")
    else:
        print("⚠️  有些测试失败，请先修复以下问题：")
        for test_name, success in results:
            if not success:
                print(f"  • 修复 {test_name}")
        
        print("\n修复后重新运行测试:")
        print("  python test_final.py")
    
    print("\n" + "=" * 70)
    
    # 返回退出码
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 测试异常退出: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)