#!/usr/bin/env python3
"""
修复模块导入问题的脚本
确保Python可以找到src目录中的本地模块
"""

import sys
import os

def fix_imports():
    """修复Python导入路径"""
    print("🔧 修复Python导入路径...")
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, "src")
    
    # 将src目录添加到Python路径
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        print(f"✅ 已将src目录添加到Python路径: {src_dir}")
    else:
        print("✅ src目录已在Python路径中")
    
    # 测试导入
    print("\n🧪 测试模块导入...")
    try:
        import scraper
        print("✅ scraper模块导入成功")
        
        from serverchan_sender import ServerChan
        print("✅ serverchan_sender模块导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        
        # 显示当前Python路径
        print("\n📁 当前Python路径:")
        for i, path in enumerate(sys.path[:10]):
            print(f"  {i+1}. {path}")
        
        # 检查src目录是否存在
        print(f"\n🔍 检查src目录: {src_dir}")
        if os.path.exists(src_dir):
            print("✅ src目录存在")
            print("📄 src目录内容:")
            for file in os.listdir(src_dir):
                if file.endswith('.py'):
                    print(f"  - {file}")
        else:
            print("❌ src目录不存在!")
            
        return False

def test_main_script():
    """测试主脚本"""
    print("\n🚀 测试主脚本...")
    try:
        # 导入主脚本需要的模块
        import sys
        import os
        
        # 确保路径正确
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # 导入并测试
        from daily_tech_news_bot import main
        
        print("✅ 主脚本导入成功")
        print("💡 提示: 可以运行 'python daily_tech_news_bot.py --test' 进行完整测试")
        return True
        
    except Exception as e:
        print(f"❌ 主脚本导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📦 Daily News Bot - 模块导入修复工具")
    print("=" * 60)
    
    if fix_imports():
        print("\n✅ 模块导入修复成功!")
        
        # 询问是否测试主脚本
        test = input("\n是否测试主脚本? (y/n): ")
        if test.lower() == 'y':
            test_main_script()
    else:
        print("\n❌ 模块导入修复失败!")
        print("\n💡 解决方案:")
        print("1. 确保src目录包含scraper.py和serverchan_sender.py")
        print("2. 手动运行: python -c \"import sys; sys.path.insert(0, 'src'); import scraper\"")
        print("3. 在脚本开头添加: import sys; sys.path.insert(0, 'src')")
    
    print("\n" + "=" * 60)
    print("🔧 修复完成")
    print("=" * 60)