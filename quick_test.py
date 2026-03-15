#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

print("测试1: 导入scraper模块")
try:
    from scraper import NewsScraper
    print("  OK - NewsScraper")
except Exception as e:
    print(f"  FAIL - {e}")

print("\n测试2: 导入serverchan模块")
try:
    from serverchan_sender import ServerChan
    print("  OK - ServerChan")
except Exception as e:
    print(f"  FAIL - {e}")

print("\n测试3: 创建NewsScraper实例")
try:
    scraper = NewsScraper()
    print("  OK - 实例创建成功")
except Exception as e:
    print(f"  FAIL - {e}")

print("\n测试4: 测试抓取功能")
try:
    news_data = scraper.run()
    if news_data:
        print(f"  OK - 抓取到 {len(news_data)} 条新闻")
    else:
        print("  WARNING - 没有抓到新闻")
except Exception as e:
    print(f"  FAIL - {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成!")
