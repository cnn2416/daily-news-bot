#!/usr/bin/env python3
"""
测试主脚本运行
"""

import subprocess
import sys

print("🚀 测试主脚本运行...")
print("=" * 60)

# 运行主脚本的测试模式
try:
    result = subprocess.run(
        [sys.executable, "daily_tech_news_bot.py", "--test"],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    print("📋 标准输出:")
    print(result.stdout)
    
    if result.stderr:
        print("\n❌ 错误输出:")
        print(result.stderr)
    
    print(f"\n退出代码: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("⏰ 程序运行超时")
except Exception as e:
    print(f"❌ 运行失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)