#!/usr/bin/env python3
"""
serverchan_sender.py - Server酱推送器（兼容版本）
提供与serverchan_enhanced.py兼容的接口
"""

from serverchan_enhanced import EnhancedServerChan

# 兼容性：提供与原版相同的ServerChan类
class ServerChan(EnhancedServerChan):
    """Server酱推送器（兼容EnhancedServerChan）"""
    pass

# 导出相同的接口
__all__ = ['ServerChan', 'EnhancedServerChan']

if __name__ == "__main__":
    print("✅ ServerChan 类可用（兼容EnhancedServerChan）")
    
    # 测试兼容性
    sender = ServerChan()
    print("✅ ServerChan 实例创建成功")
    
    # 测试方法
    title, content = sender.format_news("测试消息")
    print(f"✅ format_news测试成功: 标题='{title}', 内容长度={len(content)}")
    
    result = sender.send("测试消息")
    print(f"✅ send方法测试: {'成功' if result else '失败'}")