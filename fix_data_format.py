#!/usr/bin/env python3
"""
修复主脚本中的sender调用问题
"""

import sys
import os

# 添加src目录到路径
src_dir = os.path.join(os.path.dirname(__file__), "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

def analyze_problem():
    """分析问题并显示修复建议"""
    print("🔍 分析问题...")
    print("=" * 60)
    
    # 检查主脚本的调用
    main_script_path = os.path.join(os.path.dirname(__file__), "daily_tech_news_bot.py")
    with open(main_script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找sender.send调用
    if 'success = self.sender.send(push_message)' in content:
        print("✅ 找到问题位置: self.sender.send(push_message)")
        
        # 查找push_message是如何生成的
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'push_message' in line and '=' in line:
                print(f"   第{i+1}行: {line.strip()}")
    
    print("\n💡 问题分析:")
    print("1. serverchan_enhanced.py期望字典格式的news_data")
    print("2. 但主脚本传递的是字符串格式的push_message")
    print("3. 需要统一数据格式或修改sender.send方法")
    
    print("\n🔧 解决方案:")
    print("选项1: 修改sender.send()方法接受字符串")
    print("选项2: 修改主脚本传递字典格式数据")
    print("选项3: 创建适配器方法")
    
    return content

def fix_main_script():
    """修复主脚本"""
    print("\n🔧 修复主脚本...")
    
    main_script_path = os.path.join(os.path.dirname(__file__), "daily_tech_news_bot.py")
    
    with open(main_script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed = False
    new_lines = []
    
    for line in lines:
        # 修复sender.send调用
        if 'success = self.sender.send(push_message)' in line:
            print(f"⚠️  找到需要修复的行: {line.strip()}")
            
            # 查找push_message的定义
            # 这里需要根据实际情况调整
            # 假设push_message是字符串，但sender期望字典
            
            # 解决方案：修改为传递news_data
            fixed_line = line.replace(
                'success = self.sender.send(push_message)',
                '# 修复: 传递正确的数据格式\n' +
                '            if self.news_data:\n' +
                '                success = self.sender.send(self.news_data)\n' +
                '            else:\n' +
                '                success = self.sender.send(push_message)'
            )
            new_lines.append(fixed_line)
            fixed = True
            print("✅ 已修复sender.send调用")
        else:
            new_lines.append(line)
    
    if fixed:
        # 备份原文件
        backup_path = main_script_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ 已创建备份: {backup_path}")
        
        # 写入修复后的文件
        with open(main_script_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ 主脚本已修复")
    else:
        print("⚠️  未找到需要修复的行")
        
        # 显示可能的相关代码
        print("\n📋 相关代码段:")
        for i, line in enumerate(lines):
            if 'sender' in line.lower() or 'send' in line.lower():
                print(f"  第{i+1:4d}行: {line.rstrip()}")
    
    return fixed

def test_fix():
    """测试修复"""
    print("\n🧪 测试修复...")
    
    try:
        # 导入模块测试
        from serverchan_sender import ServerChan
        print("✅ serverchan_sender导入成功")
        
        # 创建实例
        sender = ServerChan()
        print("✅ ServerChan实例创建成功")
        
        # 测试发送字符串
        print("测试发送字符串消息...")
        try:
            result = sender.send("测试消息")
            print(f"✅ 字符串发送测试: {result}")
        except Exception as e:
            print(f"⚠️  字符串发送失败: {e}")
        
        # 测试发送字典（如果方法支持）
        print("\n测试发送字典消息...")
        try:
            test_data = {
                'title': '测试标题',
                'content': '测试内容',
                'musk_trump': [],
                'other_news': []
            }
            result = sender.send(test_data)
            print(f"✅ 字典发送测试: {result}")
        except Exception as e:
            print(f"⚠️  字典发送失败: {e}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("📦 Daily News Bot - 数据格式修复工具")
    print("=" * 60)
    
    analyze_problem()
    
    choice = input("\n是否自动修复主脚本? (y/n): ")
    
    if choice.lower() == 'y':
        if fix_main_script():
            test_fix()
    else:
        print("\n💡 手动修复指南:")
        print("1. 打开 daily_tech_news_bot.py")
        print("2. 查找 'success = self.sender.send(push_message)'")
        print("3. 修改为传递字典格式的数据，例如: self.news_data")
        print("4. 或者修改 serverchan_sender.py 的 send() 方法接受字符串")
    
    print("\n" + "=" * 60)
    print("🔧 修复完成")
    print("=" * 60)