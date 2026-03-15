#!/usr/bin/env python3
"""
直接修复主脚本中的数据格式问题
"""

import os
import re

# 主脚本路径
main_script = os.path.join(os.path.dirname(__file__), "daily_tech_news_bot.py")

print(f"🔧 修复主脚本: {main_script}")
print("=" * 60)

# 读取主脚本
with open(main_script, 'r', encoding='utf-8') as f:
    content = f.read()

print("📋 分析问题...")
print("-" * 40)

# 检查当前的sender.send调用
if 'success = self.sender.send(push_message)' in content:
    print("✅ 找到需要修复的行")
    
    # 查找push_message的定义
    push_message_pattern = r'push_message\s*=\s*(.+)'
    push_message_match = re.search(push_message_pattern, content)
    if push_message_match:
        print(f"  push_message定义: {push_message_match.group(0)[:80]}...")
    
    # 检查是否应该传递news_data而不是push_message
    if 'self.news_data' in content and 'self.format_news_summary()' in content:
        print("  📊 脚本同时包含self.news_data和格式化方法")
        
        # 修复方案1：修改send调用传递正确的数据
        # 我们需要确定应该传递什么
        
        # 先备份
        backup_file = main_script + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已创建备份: {backup_file}")
        
        # 分析serverchan_sender.py中的send方法
        sender_file = os.path.join(os.path.dirname(__file__), "src", "serverchan_sender.py")
        if os.path.exists(sender_file):
            with open(sender_file, 'r', encoding='utf-8') as f:
                sender_content = f.read()
            
            # 检查send方法的签名
            if 'def send(self, message:' in sender_content:
                print("  ✅ serverchan_sender.send()期望字符串参数")
                
                # 当前调用是正确的
                print("  💡 当前调用 push_message (字符串) 应该是正确的")
                
                # 检查是否有其他问题
                # 可能serverchan_enhanced.py还在被导入
                import_patterns = [
                    r'from serverchan_enhanced import',
                    r'import serverchan_enhanced',
                    r'from src.serverchan_enhanced import',
                    r'ServerChanSenderEnhanced'
                ]
                
                for pattern in import_patterns:
                    if re.search(pattern, content):
                        print(f"  ⚠️  发现可能的旧导入: {pattern}")
                
                # 修复导入
                fixed_content = content
                
                # 确保导入正确的ServerChan
                if 'from serverchan_sender import ServerChan' not in content:
                    print("  ⚠️  未找到正确的ServerChan导入")
                    # 添加正确的导入
                    import_lines = content.split('\n')
                    new_lines = []
                    added_import = False
                    for line in import_lines:
                        if 'import' in line and ('serverchan_enhanced' in line or 'ServerChanSenderEnhanced' in line):
                            print(f"  🔧 替换导入行: {line}")
                            # 替换为正确的导入
                            new_lines.append('from serverchan_sender import ServerChan')
                            added_import = True
                        else:
                            new_lines.append(line)
                    
                    if not added_import:
                        # 在适当位置添加导入
                        for i, line in enumerate(new_lines):
                            if 'from scraper import' in line:
                                new_lines.insert(i + 1, 'from serverchan_sender import ServerChan')
                                break
                    
                    fixed_content = '\n'.join(new_lines)
                
                # 写入修复后的内容
                with open(main_script, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print("  ✅ 主脚本已修复")
                
                # 测试修复
                print("\n🧪 测试修复...")
                test_script = """
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from serverchan_sender import ServerChan
    print("✅ ServerChan导入成功")
    
    # 检查send方法
    import inspect
    sig = inspect.signature(ServerChan.send)
    print(f"✅ send方法签名: {sig}")
    
    print("\\n🎉 修复成功！")
except Exception as e:
    print(f"❌ 测试失败: {e}")
"""
                
                test_file = os.path.join(os.path.dirname(__file__), "test_fix.py")
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(test_script)
                
                import subprocess
                result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print(f"错误: {result.stderr}")
                
                # 清理测试文件
                os.remove(test_file)
                
            else:
                print("  ❌ 无法确定serverchan_sender.send()的签名")
        else:
            print(f"  ❌ serverchan_sender.py文件不存在: {sender_file}")
    else:
        print("  ⚠️  未找到足够的信息进行自动修复")
else:
    print("✅ 未找到需要修复的sender.send调用")

print("\n" + "=" * 60)
print("🔧 修复完成")
print("=" * 60)

print("\n💡 如果问题仍然存在，请:")
print("1. 检查是否有多个serverchan_*文件冲突")
print("2. 确保导入的是正确的ServerChan类")
print("3. 手动测试: python -c \"from serverchan_sender import ServerChan; s=ServerChan(); s.send('test')\"")