#!/usr/bin/env python3
"""
Server 酱消息推送增强版 - 支持10大分类，优化显示格式
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class EnhancedServerChan:
    def __init__(self, sendkey=None):
        self.sendkey = sendkey or os.getenv('SERVERCHAN_SENDKEY')
        # if not self.sendkey:
        #     raise ValueError("需要提供 Server 酱 SendKey")
        # self.api_url = f"https://sctapi.ftqq.com/{self.sendkey}.send"
        
        # 分类配置
        self.category_config = {
            'ai_tech': {
                'emoji': '🤖',
                'name': 'AI科技前沿',
                'limit': 8,
                'description': '最新AI研究、模型发布、技术突破'
            },
            'musk_trump': {
                'emoji': '⭐',
                'name': '焦点人物追踪',
                'limit': 10,
                'description': '马斯克、特朗普及相关重要动态'
            },
            'us_politics': {
                'emoji': '🏛️',
                'name': '美国政治',
                'limit': 6,
                'description': '白宫动态、国会选举、政策变化'
            },
            'international': {
                'emoji': '🌍',
                'name': '国际热点',
                'limit': 8,
                'description': '全球重大事件、地缘政治、国际关系'
            },
            'tech_business': {
                'emoji': '💼',
                'name': '科技商业',
                'limit': 6,
                'description': '科技公司动态、商业并购、市场趋势'
            },
            'chinese_tech': {
                'emoji': '🇨🇳',
                'name': '中国科技',
                'limit': 6,
                'description': '中国科技公司、政策、创新动态'
            },
            'financial': {
                'emoji': '💰',
                'name': '财经金融',
                'limit': 6,
                'description': '股市、经济、投资、货币政策'
            },
            'defense': {
                'emoji': '🛡️',
                'name': '国防军事',
                'limit': 5,
                'description': '军事动态、国防政策、武器装备'
            },
            'energy_space': {
                'emoji': '🚀',
                'name': '能源太空',
                'limit': 5,
                'description': '能源政策、太空探索、可再生能源'
            },
            'emerging_tech': {
                'emoji': '🔬',
                'name': '新兴科技',
                'limit': 5,
                'description': '前沿科学研究、技术创新'
            }
        }
    
    def format_priority_mark(self, item: Dict[str, Any]) -> str:
        """格式化优先级标记"""
        if item.get('priority'):
            priority_type = item.get('priority_type', '')
            if priority_type == 'musk':
                return ' ⚡'
            elif priority_type == 'trump':
                return ' 🎯'
        return ''
    
    def format_section(self, category: str, items: List[Dict[str, Any]]) -> str:
        """格式化单个板块"""
        config = self.category_config.get(category, {
            'emoji': '📰',
            'name': category,
            'limit': 5,
            'description': ''
        })
        
        lines = []
        
        # 标题
        lines.append(f"### {config['emoji']} **{config['name']}**")
        
        # 描述
        if config['description']:
            lines.append(f"*{config['description']}*")
        lines.append("")
        
        # 新闻列表
        if items:
            displayed_items = items[:config['limit']]
            for i, item in enumerate(displayed_items, 1):
                priority_mark = self.format_priority_mark(item)
                
                # 标题（带链接）
                title = item.get('title', '')
                url = item.get('url', '#')
                source = item.get('source', '未知')
                
                # 简短的描述
                description = item.get('description', '')
                short_desc = description[:100] if len(description) > 100 else description
                
                lines.append(f"**{i}.{priority_mark} {title}**")
                lines.append(f"   🔗 [阅读原文]({url})")
                lines.append(f"   📰 {source}")
                if short_desc:
                    lines.append(f"   📝 {short_desc}")
                lines.append("")
        else:
            lines.append("*暂无可显示内容*")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)
    
    def format_statistics(self, news_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """生成统计信息"""
        total_news = sum(len(items) for items in news_data.values())
        
        musk_count = sum(1 for items in news_data.values() for item in items 
                        if item.get('priority_type') == 'musk')
        trump_count = sum(1 for items in news_data.values() for item in items 
                         if item.get('priority_type') == 'trump')
        
        lines = []
        lines.append("### 📊 今日新闻统计")
        lines.append("")
        lines.append(f"• **总计新闻**: {total_news} 条")
        lines.append(f"• **马斯克相关**: {musk_count} 条")
        lines.append(f"• **特朗普相关**: {trump_count} 条")
        lines.append("")
        
        # 分类统计
        lines.append("**分类统计:**")
        for category in self.category_config.keys():
            items = news_data.get(category, [])
            if items:
                musk_in_category = sum(1 for item in items if item.get('priority_type') == 'musk')
                trump_in_category = sum(1 for item in items if item.get('priority_type') == 'trump')
                config = self.category_config[category]
                lines.append(f"  - {config['emoji']} {config['name']}: {len(items)} 条 (M:{musk_in_category}, T:{trump_in_category})")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)
    
    def format_news(self, news_data: Dict[str, List[Dict[str, Any]]]) -> tuple:
        """格式化所有新闻为 Markdown 消息"""
        today = datetime.now()
        date_str = today.strftime('%Y年%m月%d日')
        weekday = today.strftime('%A')
        
        # 标题
        title = f"📰 每日全球新闻简报 - {date_str} ({weekday})"
        
        # 内容
        sections = []
        
        # 头部信息
        sections.append(f"# 🌍 全球新闻简报")
        sections.append(f"**📅 {date_str} ({weekday})**")
        sections.append("")
        sections.append("为您精选今日全球重要新闻，重点关注AI科技、马斯克/特朗普动态、国际热点。")
        sections.append("")
        sections.append("---")
        sections.append("")
        
        # 特别提醒：马斯克/特朗普相关新闻
        musk_trump_items = news_data.get('musk_trump', [])
        if musk_trump_items:
            sections.append("### ⭐ **今日焦点人物新闻**")
            sections.append("")
            for i, item in enumerate(musk_trump_items[:3], 1):
                priority_mark = self.format_priority_mark(item)
                sections.append(f"**{i}.{priority_mark} {item['title']}**")
                sections.append(f"   📰 {item['source']}")
                sections.append("")
            sections.append("---")
            sections.append("")
        
        # 按顺序显示所有分类
        for category in self.category_config.keys():
            items = news_data.get(category, [])
            if items:  # 只显示有内容的分类
                sections.append(self.format_section(category, items))
        
        # 统计信息
        sections.append(self.format_statistics(news_data))
        
        # 底部信息
        sections.append("### ℹ️ 使用说明")
        sections.append("")
        sections.append("• **点击链接**阅读原文")
        sections.append("• **⚡ 标记**: 马斯克相关新闻")
        sections.append("• **🎯 标记**: 特朗普相关新闻")
        sections.append("• 数据来源: 50+国际权威媒体")
        sections.append("")
        sections.append("---")
        sections.append("")
        sections.append("_🤖 由 OpenClaw 增强版每日新闻机器人自动生成_")
        sections.append(f"_⏰ 更新时间: {today.strftime('%H:%M:%S')}_")
        
        content = "\n".join(sections)
        return title, content
    
    def send(self, news_data: Dict[str, List[Dict[str, Any]]]) -> bool:
        """发送消息"""
        title, content = self.format_news(news_data)
        
        # 如果内容太长，进行适当截断
        max_length = 60000  # Server酱限制
        if len(content) > max_length:
            print(f"⚠️  内容过长 ({len(content)} 字符)，进行截断...")
            content = content[:max_length-100] + "\n\n...（内容已截断，完整版请查看日志）"
        
        payload = {
            "title": title[:32],  # 标题限制32字符
            "desp": content,
            "channel": "9"
        }
        
        try:
            print(f"📤 正在发送到 Server 酱...")
            resp = requests.post(self.api_url, data=payload, timeout=45)
            result = resp.json()
            
            if result.get('code') == 0:
                print(f"✅ [{datetime.now()}] Server 酱推送成功")
                print(f"   推送ID: {result.get('data', {}).get('pushid', 'N/A')}")
                print(f"   阅读链接: {result.get('data', {}).get('readkey', 'N/A')}")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"⏰ 发送超时")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 发送出错: {e}")
            return False
    
    def test_format(self, news_data: Dict[str, List[Dict[str, Any]]]) -> None:
        """测试格式，不实际发送"""
        title, content = self.format_news(news_data)
        
        print(f"\n{'='*70}")
        print("📄 格式预览")
        print(f"{'='*70}")
        print(f"标题: {title}")
        print(f"内容长度: {len(content)} 字符")
        print(f"{'='*70}")
        print("\n内容预览（前1000字符）:")
        print("=" * 50)
        print(content[:1000])
        print("..." if len(content) > 1000 else "")
        print("=" * 50)
        
        # 分类统计
        print("\n📊 分类统计:")
        for category in self.category_config.keys():
            items = news_data.get(category, [])
            if items:
                config = self.category_config[category]
                print(f"  {config['emoji']} {config['name']}: {len(items)} 条")


def main():
    """主函数"""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    
    print("""
    ============================================================
    📰 Server 酱推送增强版
    ============================================================
    """)
    
    # 检查环境变量
    sendkey = os.getenv('SERVERCHAN_SENDKEY')
    if not sendkey:
        print("❌ 请设置 SERVERCHAN_SENDKEY 环境变量")
        print("   或在命令行提供: python serverchan_enhanced.py --sendkey YOUR_KEY")
        return False
    
    # 测试模式还是实际发送
    test_mode = '--test' in sys.argv
    
    try:
        # 导入抓取器
        from scraper_enhanced import EnhancedNewsScraper
        
        print("🔄 开始抓取新闻...")
        scraper = EnhancedNewsScraper()
        news_data = scraper.run()
        
        # 创建推送器
        sender = EnhancedServerChan(sendkey)
        
        if test_mode:
            print("\n🧪 测试模式（不实际发送）")
            sender.test_format(news_data)
            return True
        else:
            print("\n🚀 开始推送...")
            success = sender.send(news_data)
            return success
            
    except ImportError as e:
        print(f"❌ 无法导入模块: {e}")
        print("请确保 scraper_enhanced.py 存在")
        return False
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("用法:")
        print("  python serverchan_enhanced.py           # 实际发送")
        print("  python serverchan_enhanced.py --test    # 测试模式")
        print("  python serverchan_enhanced.py --help    # 显示帮助")
        sys.exit(0)
    
    success = main()
    sys.exit(0 if success else 1)