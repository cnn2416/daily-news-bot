import requests
import sys

def test_serverchan(sckey):
    """测试Server酱连接和推送"""
    print(f"🔍 测试Server酱SendKey: {sckey}")
    print("-" * 50)
    
    # 测试URL
    url = f"https://sctapi.ftqq.com/{sckey}.send"
    
    # 测试消息
    test_data = {
        "title": "🔧 Server酱连接测试",
        "desp": f"""
## 🚀 测试信息
- 时间: 2026-03-15 18:40
- SendKey: {sckey[:10]}...
- 状态: 正在测试

## 📋 测试结果
请检查微信是否收到此测试消息。

## 💡 如果没收到
1. 确认SendKey是否正确
2. 确认微信已绑定Server酱
3. 检查网络连接
"""
    }
    
    try:
        print("📤 发送测试消息...")
        response = requests.post(url, data=test_data, timeout=10)
        
        print(f"📊 响应状态码: {response.status_code}")
        result = response.json()
        print(f"📝 响应内容: {result}")
        
        if result.get("code") == 0:
            print("✅ Server酱连接测试成功！")
            print("📱 请检查微信是否收到测试消息")
            return True
        else:
            print(f"❌ Server酱返回错误: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sckey = sys.argv[1]
        test_serverchan(sckey)
    else:
        print("⚠️ 用法: python test_serverchan.py <您的SendKey>")
        print("💡 示例: python test_serverchan.py SCU1234567890abcdef")
        print("")
        print("📱 获取SendKey步骤:")
        print("1. 访问 https://sct.ftqq.com/")
        print("2. 微信扫码登录")
        print("3. 在首页获取SendKey（SCU开头）")
        print("4. 绑定微信接收推送")