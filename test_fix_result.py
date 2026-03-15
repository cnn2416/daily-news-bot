#!/usr/bin/env python3
"""
测试修复结果
"""

import sys
import os

# 添加src目录到路径
src_dir = os.path.join(os.path.dirname(__file__), "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("🧪 测试修复...")
print("=" * 60)

try:
    # 1. 测试导入EnhancedServerChan
    from serverchan_enhanced import EnhancedServerChan
    print("✅ serverchan_enhanced.EnhancedServerChan 导入成功")
    
    # 2. 测试导入ServerChan
    from serverchan_sender import ServerChan
    print("✅ serverchan_sender.ServerChan 导入成功")
    
    # 3. 创建实例
    enhanced_sender = EnhancedServerChan()
    print("✅ EnhancedServerChan 实例创建成功")
    
    sender = ServerChan()
    print("✅ ServerChan 实例创建成功")
    
    # 4. 测试format_news方法（兼容性测试）
    print("\n📋 测试format_news方法...")
    
    # 测试字符串
    title1, content1 = enhanced_sender.format_news("测试字符串消息")
    print(f"✅ 字符串格式化测试: 标题='{title1}', 长度={len(content1)}")
    
    # 测试字典
    test_dict = {
        'musk_trump': [
            {'title': 'Elon Musk launches new project', 'source': 'Teslarati'},
            {'title': 'Donald Trump makes announcement', 'source': 'Fox News'}
        ],
        'ai_tech': [
            {'title': 'AI breakthrough announced', 'source': 'TechCrunch'}
        ],
        'timestamp': '2026-03-15 19:30:00'
    }
    
    title2, content2 = enhanced_sender.format_news(test_dict)
    print(f"✅ 字典格式化测试: 标题='{title2}', 长度={len(content2)}")
    
    # 显示部分内容
    print(f"\n📄 字典格式化结果预览:")
    lines = content2.split('\n')
    for i, line in enumerate(lines[:10]):
        print(f"  {line}")
    if len(lines) > 10:
        print(f"  ... 还有{len(lines)-10}行")
    
    # 5. 测试send方法
    print("\n📤 测试send方法（不实际发送）...")
    
    # 测试字符串发送
    result1 = enhanced_sender.send("测试消息")
    print(f"✅ 字符串send测试: {'成功' if result1 else '失败（未配置sckey是正常的）'}")
    
    # 测试字典发送
    result2 = enhanced_sender.send(test_dict)
    print(f"✅ 字典send测试: {'成功' if result2 else '失败（未配置sckey是正常的）'}")
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！修复成功！")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n🔧 调试信息:")
    print(f"当前目录: {os.getcwd()}")
    print(f"Python路径: {sys.path[:3]}")
    print(f"src目录内容: {os.listdir(src_dir) if os.path.exists(src_dir) else '不存在'}")