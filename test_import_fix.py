#!/usr/bin/env python3
"""
验证模块导入修复
"""

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("🔍 测试模块导入...")
print(f"当前目录: {current_dir}")
print(f"Python路径: {sys.path[:3]}")

try:
    # 测试导入scraper
    import scraper
    print("✅ scraper 导入成功")
    
    # 检查scraper模块内容
    print(f"scraper模块内容: {dir(scraper)[:10]}")
    
    # 测试导入serverchan_sender
    from serverchan_sender import ServerChan
    print("✅ serverchan_sender.ServerChan 导入成功")
    
    # 创建实例测试
    print("🧪 创建实例测试...")
    scraper_instance = scraper.NewsScraper()
    print("✅ NewsScraper实例创建成功")
    
    sender_instance = ServerChan()
    print("✅ ServerChan实例创建成功")
    
    print("\n🎉 所有模块导入测试通过!")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("\n📁 检查src目录内容:")
    src_path = os.path.join(current_dir, "src")
    if os.path.exists(src_path):
        for file in os.listdir(src_path):
            print(f"  - {file}")
    else:
        print("  src目录不存在!")
    
    print("\n💡 可能的问题:")
    print("1. 文件名错误 (serverchan_enhanced.py vs serverchan_sender.py)")
    print("2. 类名不匹配")
    print("3. Python路径设置问题")
    
except Exception as e:
    print(f"❌ 其他错误: {e}")
    import traceback
    traceback.print_exc()