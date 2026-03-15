#!/usr/bin/env python3
"""
极简测试脚本，逐层验证
"""

import sys
import os

print("=" * 60)
print("Step 1: 检查当前目录")
print("=" * 60)
print(f"当前工作目录: {os.getcwd()}")
print(f"Python版本: {sys.version}")

print("\n" + "=" * 60)
print("Step 2: 检查目录结构")
print("=" * 60)
directories = ['src', 'config']
files_to_check = ['daily_tech_news_bot.py', 'requirements.txt', 'src/scraper.py']

for dir_name in directories:
    if os.path.exists(dir_name):
        print(f"✅ 目录存在: {dir_name}")
    else:
        print(f"❌ 目录不存在: {dir_name}")

for file_name in files_to_check:
    if os.path.exists(file_name):
        print(f"✅ 文件存在: {file_name}")
    else:
        print(f"❌ 文件不存在: {file_name}")

print("\n" + "=" * 60)
print("Step 3: 测试Python模块导入")
print("=" * 60)

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

modules_to_test = ['feedparser', 'requests', 'yaml', 'logging']

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module} 可导入")
    except ImportError as e:
        print(f"❌ {module} 导入失败: {e}")

print("\n" + "=" * 60)
print("Step 4: 测试项目模块导入")
print("=" * 60)

# 测试导入scraper模块
try:
    from scraper import NewsScraper
    print("✅ scraper.NewsScraper 导入成功")
    
    # 测试实例化
    scraper = NewsScraper()
    print("✅ NewsScraper 实例化成功")
except ImportError as e:
    print(f"❌ scraper 导入失败: {e}")
except Exception as e:
    print(f"❌ 实例化失败: {e}")

# 测试导入serverchan模块
try:
    from serverchan_sender import ServerChan
    print("✅ serverchan_sender.ServerChan 导入成功")
    
    # 测试实例化
    sender = ServerChan()
    print("✅ ServerChan 实例化成功")
except ImportError as e:
    print(f"❌ serverchan_sender 导入失败: {e}")
except Exception as e:
    print(f"❌ 实例化失败: {e}")

print("\n" + "=" * 60)
print("Step 5: 创建必要目录")
print("=" * 60)

dirs_to_create = ['data', 'logs', 'backup']
for dir_name in dirs_to_create:
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ 创建目录: {dir_name}")
        else:
            print(f"📁 目录已存在: {dir_name}")
    except Exception as e:
        print(f"❌ 创建目录失败 {dir_name}: {e}")

print("\n" + "=" * 60)
print("Step 6: 测试新闻抓取（简化版）")
print("=" * 60)

if 'scraper' in locals() and scraper:
    try:
        print("尝试运行新闻抓取器...")
        # 查看是否有run方法
        if hasattr(scraper, 'run'):
            print("✅ NewsScraper有run方法")
            
            # 尝试运行
            import traceback
            try:
                # 用timeout防止长时间运行
                import signal
                import functools
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("操作超时")
                
                # 设置超时
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(60)  # 60秒超时
                
                result = scraper.run()
                signal.alarm(0)  # 取消超时
                
                if result:
                    print(f"✅ 抓取成功，返回数据格式: {type(result)}")
                    if isinstance(result, dict):
                        print(f"  数据包含 {len(result)} 个分类")
                        for category, items in result.items():
                            if items:
                                print(f"  {category}: {len(items)} 条新闻")
                else:
                    print("⚠️  抓取返回空数据")
                    
            except TimeoutError:
                print("⚠️  抓取操作超时")
            except Exception as e:
                print(f"❌ 抓取过程中出错: {e}")
                traceback.print_exc()
        else:
            print("❌ NewsScraper没有run方法")
    except Exception as e:
        print(f"❌ 测试抓取失败: {e}")
else:
    print("⚠️ 跳过抓取测试（scraper实例不可用）")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)