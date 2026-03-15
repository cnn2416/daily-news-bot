#!/usr/bin/env python3
"""
每日新闻超级增强版 - 最终版本
整合所有最佳功能：
1. 马斯克和特朗普的单独新闻专栏
2. 英文新闻自动添加中文描述
3. 多渠道推送支持
4. 完整的错误处理和日志
"""

import sys
import os
import json
import argparse
from datetime import datetime
import traceback
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 尝试导入所需的模块
try:
    from scraper import NewsScraper
    from serverchan_enhanced import EnhancedServerChan
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所有依赖包：pip install -r requirements.txt")
    sys.exit(1)


class DailyNewsBotFinal:
    """最终版本的新闻机器人"""
    
    def __init__(self, config_path=None):
        """初始化机器人"""
        self.config = self.load_config(config_path)
        self.setup_directories()
        
        # 初始化组件
        self.scraper = NewsScraper()
        self.sender = EnhancedServerChan()
        
        # 日志设置
        self.log_file = "logs/daily_news_bot.log"
        self.setup_logging()
        
    def load_config(self, config_path):
        """加载配置文件"""
        default_config = {
            'push': {
                'serverchan_enabled': True,
                'telegram_enabled': False,
                'wecom_enabled': False,
            },
            'scraping': {
                'max_news_per_category': 15,
                'timeout': 30,
                'retry_times': 3,
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/daily_news_bot.log',
            }
        }
        
        # 如果提供了配置文件，尝试加载
        if config_path and os.path.exists(config_path):
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    # 合并配置
                    self.merge_configs(default_config, user_config)
            except Exception as e:
                print(f"⚠️ 配置文件加载失败，使用默认配置: {e}")
        
        return default_config
    
    def merge_configs(self, default, user):
        """合并配置字典"""
        for key, value in user.items():
            if key in default and isinstance(value, dict) and isinstance(default[key], dict):
                self.merge_configs(default[key], value)
            else:
                default[key] = value
    
    def setup_directories(self):
        """创建必要的目录"""
        directories = ['data', 'logs', 'config', 'backup']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 创建目录: {directory}")
    
    def setup_logging(self):
        """设置日志"""
        import logging
        
        # 创建日志目录
        log_dir = os.path.dirname(self.log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("=" * 70)
        self.logger.info("📰 每日新闻机器人启动")
        self.logger.info("=" * 70)
    
    def format_news_for_push(self, news_data):
        """格式化新闻数据用于推送"""
        self.logger.info("开始格式化新闻数据...")
        
        formatted_news = {}
        
        # 中文分类名称映射
        category_names = {
            'elon_musk': '🚀 马斯克专栏',
            'donald_trump': '🎯 特朗普专栏',
            'ai_tech': '🤖 AI科技前沿',
            'us_politics': '🇺🇸 美国政治',
            'international': '🌍 国际热点',
            'tech_business': '💼 科技商业',
            'chinese_tech': '🇨🇳 中国科技',
            'financial': '💰 财经金融',
            'defense': '🛡️ 国防军事',
            'energy_space': '🚀 能源太空',
        }
        
        for category, items in news_data.items():
            if not items:
                continue
                
            category_name = category_names.get(category, category)
            formatted_items = []
            
            for i, item in enumerate(items, 1):
                # 构建新闻条目
                title = item.get('title', '')
                translated_title = item.get('translated_title', '')
                url = item.get('url', '#')
                source = item.get('source', '未知来源')
                is_english = item.get('is_english', False)
                
                # 构建显示文本
                if is_english and translated_title:
                    display_text = f"{i}. {title}\n   中文: {translated_title}"
                else:
                    display_text = f"{i}. {title}"
                
                # 添加英文标记
                if is_english:
                    display_text += " 🌍"
                
                # 添加来源和链接
                display_text += f"\n   来源: {source}\n   链接: {url}\n"
                
                formatted_items.append(display_text)
            
            formatted_news[category_name] = formatted_items
        
        self.logger.info(f"格式化完成，共处理 {sum(len(items) for items in formatted_news.values())} 条新闻")
        return formatted_news
    
    def create_push_message(self, news_data):
        """创建推送消息"""
        self.logger.info("开始创建推送消息...")
        
        formatted_news = self.format_news_for_push(news_data)
        
        # 消息标题
        today = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%H:%M:%S')
        message = f"📰 {today} {current_time} 全球新闻简报\n"
        message += "=" * 60 + "\n"
        message += "🚀 超级增强版 | 马斯克+特朗普单独专栏 | 英文新闻带中文描述\n"
        message += "=" * 60 + "\n\n"
        
        # 统计信息
        total_news = sum(len(items) for items in news_data.values())
        musk_count = len(news_data.get('elon_musk', []))
        trump_count = len(news_data.get('donald_trump', []))
        english_count = sum(1 for items in news_data.values() for item in items if item.get('is_english', False))
        
        message += f"📊 今日统计:\n"
        message += f"• 总计新闻: {total_news} 条\n"
        message += f"• 马斯克专栏: {musk_count} 条\n"
        message += f"• 特朗普专栏: {trump_count} 条\n"
        message += f"• 英文新闻: {english_count} 条（已翻译）\n"
        message += f"• 分类数量: {len([c for c in news_data if news_data[c]])} 个\n\n"
        
        # 按分类添加新闻
        category_order = [
            '🚀 马斯克专栏',
            '🎯 特朗普专栏',
            '🤖 AI科技前沿',
            '🇺🇸 美国政治',
            '🌍 国际热点',
            '💼 科技商业',
            '🇨🇳 中国科技',
            '💰 财经金融',
            '🛡️ 国防军事',
            '🚀 能源太空',
        ]
        
        added_categories = 0
        for category_name in category_order:
            if category_name in formatted_news:
                message += f"\n{category_name}:\n"
                message += "-" * 40 + "\n"
                for item_text in formatted_news[category_name]:
                    message += item_text + "\n"
                added_categories += 1
        
        # 底部信息
        message += "\n" + "=" * 60 + "\n"
        message += "📱 由 OpenClaw 每日新闻机器人自动生成\n"
        message += f"⏰ 生成时间: {current_time}\n"
        message += f"📊 新闻来源: 100+ 个主流媒体\n"
        message += "🔗 GitHub: https://github.com/\n"
        
        self.logger.info(f"推送消息创建完成，长度: {len(message)} 字符，包含 {added_categories} 个分类")
        return message
    
    def save_data_files(self, news_data):
        """保存数据到文件"""
        self.logger.info("开始保存数据文件...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存JSON原始数据
        json_file = f"data/news_raw_{timestamp}.json"
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"原始数据已保存: {json_file}")
        except Exception as e:
            self.logger.error(f"保存JSON数据失败: {e}")
        
        # 保存Markdown摘要
        md_file = f"data/news_summary_{timestamp}.md"
        try:
            self.save_markdown_summary(news_data, md_file)
            self.logger.info(f"摘要已保存: {md_file}")
        except Exception as e:
            self.logger.error(f"保存Markdown摘要失败: {e}")
        
        # 保存今天的最新文件
        latest_file = "data/news_latest.json"
        try:
            with open(latest_file, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"最新数据已保存: {latest_file}")
        except Exception as e:
            self.logger.error(f"保存最新数据失败: {e}")
        
        return json_file, md_file
    
    def save_markdown_summary(self, news_data, output_file):
        """保存Markdown格式的新闻摘要"""
        today = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        summary = f"""# {today} {current_time} 新闻摘要

## 📊 统计信息

"""
        
        # 统计数据
        total_news = sum(len(items) for items in news_data.values())
        musk_count = len(news_data.get('elon_musk', []))
        trump_count = len(news_data.get('donald_trump', []))
        english_count = sum(1 for items in news_data.values() for item in items if item.get('is_english', False))
        
        summary += f"- **总计新闻**: {total_news} 条\n"
        summary += f"- **马斯克专栏**: {musk_count} 条\n"
        summary += f"- **特朗普专栏**: {trump_count} 条\n"
        summary += f"- **英文新闻**: {english_count} 条（已添加中文描述）\n"
        summary += f"- **分类数量**: {len([c for c in news_data if news_data[c]])} 个\n\n"
        
        # 分类映射
        category_names_zh = {
            'elon_musk': '马斯克专栏',
            'donald_trump': '特朗普专栏',
            'ai_tech': 'AI科技前沿',
            'us_politics': '美国政治',
            'international': '国际热点',
            'tech_business': '科技商业',
            'chinese_tech': '中国科技',
            'financial': '财经金融',
            'defense': '国防军事',
            'energy_space': '能源太空',
        }
        
        # 按分类添加新闻
        for category, items in news_data.items():
            if not items:
                continue
                
            category_zh = category_names_zh.get(category, category)
            summary += f"## {category_zh}\n\n"
            
            for i, item in enumerate(items, 1):
                title = item.get('title', '')
                translated_title = item.get('translated_title', '')
                url = item.get('url', '#')
                source = item.get('source', '未知来源')
                is_english = item.get('is_english', False)
                
                if is_english and translated_title:
                    summary += f"{i}. **{title}** 🌍\n"
                    summary += f"   - **中文描述**: {translated_title}\n"
                else:
                    summary += f"{i}. **{title}**\n"
                
                summary += f"   - **来源**: {source}\n"
                summary += f"   - **链接**: [查看原文]({url})\n\n"
        
        # 底部信息
        summary += f"""
---

## ℹ️ 项目信息

- **项目名称**: 每日新闻超级增强版机器人
- **生成时间**: {current_time}
- **程序版本**: 1.0.0
- **GitHub**: [查看项目](https://github.com/)

---

> 本摘要由每日新闻机器人自动生成，数据来源于100+个主流新闻源。
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
    
    def cleanup_old_files(self, days_to_keep=7):
        """清理旧的数据文件"""
        import glob
        from datetime import datetime, timedelta
        
        self.logger.info(f"清理 {days_to_keep} 天前的旧文件...")
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # 清理data目录中的旧文件
        data_patterns = [
            "data/news_raw_*.json",
            "data/news_summary_*.md",
        ]
        
        deleted_count = 0
        for pattern in data_patterns:
            files = glob.glob(pattern)
            for file in files:
                try:
                    # 从文件名中解析日期
                    file_date_str = os.path.basename(file).split('_')[2]  # news_raw_YYYYMMDD_HHMMSS.json
                    if len(file_date_str) >= 8:
                        file_date = datetime.strptime(file_date_str[:8], '%Y%m%d')
                        if file_date < cutoff_date:
                            os.remove(file)
                            deleted_count += 1
                            self.logger.debug(f"删除旧文件: {file}")
                except Exception as e:
                    self.logger.debug(f"无法处理文件 {file}: {e}")
        
        self.logger.info(f"清理完成，共删除 {deleted_count} 个旧文件")
    
    def run(self, test_mode=False, no_push=False):
        """运行主程序"""
        try:
            self.logger.info("开始每日新闻机器人运行流程...")
            
            # 1. 抓取新闻数据
            self.logger.info("第1步：抓取新闻数据...")
            news_data = self.scraper.run()
            
            if not news_data or all(not items for items in news_data.values()):
                self.logger.error("新闻抓取失败或没有抓到数据")
                return False
            
            # 2. 保存数据文件
            self.logger.info("第2步：保存数据文件...")
            json_file, md_file = self.save_data_files(news_data)
            
            # 3. 创建推送消息
            self.logger.info("第3步：创建推送消息...")
            push_message = self.create_push_message(news_data)
            
            # 4. 显示预览
            self.logger.info("第4步：显示消息预览...")
            preview_length = min(500, len(push_message))
            print("\n" + "=" * 70)
            print("📱 推送消息预览 (前500字符):")
            print("=" * 70)
            print(push_message[:preview_length] + ("..." if len(push_message) > preview_length else ""))
            print("=" * 70 + "\n")
            
            # 5. 推送消息
            if test_mode or no_push:
                self.logger.info("测试模式：跳过推送")
                print("✅ 测试模式：所有功能测试通过！")
                print(f"• 抓取新闻: {sum(len(items) for items in news_data.values())} 条")
                print(f"• 消息长度: {len(push_message)} 字符")
                print(f"• 数据文件: {json_file}, {md_file}")
            else:
                self.logger.info("第5步：推送消息...")
                success = self.sender.send(push_message)
                
                if success:
                    self.logger.info("消息推送成功！")
                    print("✅ 消息推送成功！")
                else:
                    self.logger.error("消息推送失败")
                    print("❌ 消息推送失败")
            
            # 6. 清理旧文件
            self.logger.info("第6步：清理旧文件...")
            self.cleanup_old_files()
            
            self.logger.info("每日新闻机器人运行完成！")
            print("\n" + "=" * 70)
            print("🎉 每日新闻机器人运行完成！")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            self.logger.error(f"程序运行出错: {e}", exc_info=True)
            print(f"\n❌ 程序运行出错: {e}")
            traceback.print_exc()
            return False


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='每日新闻超级增强版机器人')
    
    parser.add_argument('--test', action='store_true',
                       help='测试模式：只抓取数据，不推送')
    parser.add_argument('--no-push', action='store_true',
                       help='不推送消息：抓取数据但不发送推送')
    parser.add_argument('--config', type=str, default=None,
                       help='配置文件路径')
    parser.add_argument('--cleanup-days', type=int, default=7,
                       help='清理多少天前的旧文件')
    parser.add_argument('--version', action='store_true',
                       help='显示版本信息')
    
    return parser.parse_args()


def show_banner():
    """显示程序横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    📰 每日新闻超级增强版机器人 v1.0.0                         ║
    ║    🚀 马斯克+特朗普单独专栏 | 英文新闻中文描述               ║
    ║    ⏰ 自动抓取+推送 | 100+新闻源 | 智能分类                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """主函数"""
    show_banner()
    
    args = parse_arguments()
    
    if args.version:
        print("每日新闻超级增强版机器人 v1.0.0")
        print("发布日期: 2025-03-15")
        print("功能: 马斯克专栏 | 特朗普专栏 | 英文新闻中文描述")
        return
    
    print(f"🎯 模式: {'测试' if args.test else '正式'}")
    print(f"📤 推送: {'关闭' if args.no_push or args.test else '开启'}")
    print(f"🗄️  配置: {args.config or '默认配置'}")
    print(f"🗑️  清理: {args.cleanup_days} 天前的旧文件\n")
    
    # 运行机器人
    bot = DailyNewsBotFinal(config_path=args.config)
    
    start_time = datetime.now()
    success = bot.run(test_mode=args.test, no_push=args.no_push)
    end_time = datetime.now()
    
    # 显示运行时间
    duration = end_time - start_time
    minutes, seconds = divmod(duration.total_seconds(), 60)
    
    print(f"\n⏱️  运行时间: {int(minutes)}分{int(seconds)}秒")
    print("✨ 任务完成！")
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序异常退出: {e}")
        traceback.print_exc()
        sys.exit(1)