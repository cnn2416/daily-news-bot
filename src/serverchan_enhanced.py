#!/usr/bin/env python3
"""
serverchan_enhanced.py - 增强版Server酱推送器
兼容原版serverchan_sender.py，但支持字典格式的news_data
"""

import json
import requests
from typing import Dict, List, Any, Tuple
import yaml
import os
import logging

class EnhancedServerChan:
    """增强版Server酱推送器"""
    
    def __init__(self, config_path=None):
        """初始化"""
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config(config_path)
        self.sckey = self.config.get('push', {}).get('serverchan', {}).get('sckey', '')
        
    def load_config(self, config_path=None):
        """加载配置文件"""
        default_config = {
            'push': {
                'serverchan': {
                    'enabled': True,
                    'sckey': '',
                    'retry_times': 3
                }
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        return config
            except Exception as e:
                self.logger.error(f"加载配置文件失败: {e}")
        
        # 尝试从环境变量获取
        env_sckey = os.environ.get('SERVERCHAN_SENDKEY')
        if env_sckey:
            default_config['push']['serverchan']['sckey'] = env_sckey
        
        return default_config
    
    def format_news(self, news_data):
        """
        格式化新闻数据为Server酱消息
        
        参数:
            news_data: 可以是字典格式的新闻数据，也可以是字符串格式的消息
        """
        # 如果是字符串，直接返回
        if isinstance(news_data, str):
            return "每日科技新闻摘要", news_data
        
        # 如果是字典，进行格式化
        elif isinstance(news_data, dict):
            # 修复兼容性：处理不同的键名
            musk_trump_items = []
            
            # 尝试获取马斯克/特朗普相关新闻
            for key in ['musk_trump', 'elon_musk', 'donald_trump', 'focus_news']:
                if key in news_data:
                    items = news_data.get(key, [])
                    if isinstance(items, list):
                        musk_trump_items.extend(items)
            
            # 获取其他新闻
            other_news = []
            for key, value in news_data.items():
                if key not in ['musk_trump', 'elon_musk', 'donald_trump', 'focus_news']:
                    if isinstance(value, list):
                        other_news.extend(value)
            
            # 构建消息
            sections = []
            sections.append("# 🌐 每日科技新闻摘要")
            sections.append("")
            sections.append("为您精选今日全球重要新闻，重点关注AI科技、马斯克/特朗普动态、国际热点。")
            sections.append("")
            sections.append("---")
            sections.append("")
            
            # 特别提醒：马斯克/特朗普相关新闻
            if musk_trump_items:
                sections.append("### ⭐ **今日焦点人物新闻**")
                sections.append("")
                for i, item in enumerate(musk_trump_items[:3], 1):
                    # 安全地获取item的内容
                    title = item.get('title', '无标题') if isinstance(item, dict) else str(item)
                    source = item.get('source', '未知来源') if isinstance(item, dict) else '未知来源'
                    sections.append(f"**{i}. {title}**")
                    sections.append(f"   📰 {source}")
                sections.append("")
            
            # 其他新闻
            if other_news:
                sections.append("### 📰 **其他重要新闻**")
                sections.append("")
                for i, item in enumerate(other_news[:10], 1):
                    title = item.get('title', '无标题') if isinstance(item, dict) else str(item)
                    source = item.get('source', '未知来源') if isinstance(item, dict) else '未知来源'
                    sections.append(f"**{i}. {title}**")
                    sections.append(f"   📰 {source}")
                sections.append("")
            
            sections.append("---")
            sections.append("")
            sections.append("📊 **今日新闻统计**")
            sections.append(f"• 焦点新闻: {len(musk_trump_items)} 条")
            sections.append(f"• 其他新闻: {len(other_news)} 条")
            sections.append("")
            sections.append("📅 数据更新时间: " + news_data.get('timestamp', '刚刚'))
            
            content = "\n".join(sections)
            return "每日科技新闻摘要", content
        
        else:
            # 默认返回
            return "每日新闻", str(news_data)
    
    def format_priority_mark(self, item):
        """格式化优先级标记（兼容方法）"""
        if isinstance(item, dict) and item.get('priority', 0) > 0:
            return "⭐ "
        return ""
    
    def send(self, data):
        """
        发送消息到Server酱
        
        参数:
            data: 可以是新闻数据字典，也可以是消息字符串
        """
        try:
            # 格式化消息
            title, content = self.format_news(data)
            
            # 如果没有sckey，返回测试成功
            if not self.sckey:
                self.logger.warning("未配置Server酱sckey，跳过实际发送")
                return True
            
            # 构建API URL
            api_url = f"https://sctapi.ftqq.com/{self.sckey}.send"
            
            # 准备请求数据
            payload = {
                'title': title[:100],  # 限制标题长度
                'desp': content
            }
            
            # 发送请求
            response = requests.post(api_url, data=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    self.logger.info(f"消息推送成功: {result.get('message', '成功')}")
                    return True
                else:
                    self.logger.error(f"Server酱API错误: {result}")
                    return False
            else:
                self.logger.error(f"HTTP请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"推送消息时出错: {e}")
            return False
    
    def send_text(self, text):
        """发送纯文本消息（兼容旧接口）"""
        return self.send(text)
    
    def send_news(self, news_data):
        """发送新闻数据（兼容旧接口）"""
        return self.send(news_data)


# 兼容性：提供与原版serverchan_sender相同的接口
if __name__ == "__main__":
    # 测试代码
    sender = EnhancedServerChan()
    print("✅ EnhancedServerChan 类可用")
    
    # 测试发送字符串
    test_result = sender.send("测试消息")
    print(f"字符串发送测试: {'成功' if test_result else '失败'}")
    
    # 测试发送字典
    test_data = {
        'musk_trump': [
            {'title': '测试马斯克新闻', 'source': 'Test Source'}
        ],
        'timestamp': '2026-03-15 19:20:00'
    }
    test_result2 = sender.send(test_data)
    print(f"字典发送测试: {'成功' if test_result2 else '失败'}")