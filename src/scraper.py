#!/usr/bin/env python3
"""
日报抓取脚本 - 国际化多源备份 + 高级反爬
AI科技、跨境电商、产品创业、能源、军事、国际热点
重点关注：美国、马斯克、特朗普
"""

import requests
import json
from datetime import datetime
import feedparser
import time
import re
import random
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class NewsScraper:
    def __init__(self):
        # 多 User-Agent 轮换
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        # 创建带重试的 session
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 基础 headers
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        
        self.news_data = {
            'ai': [],        # AI科技
            'ecommerce': [], # 跨境电商
            'startup': [],   # 产品创业
            'energy': [],    # 能源
            'military': [],  # 军事
            'international': [],  # 国际热点
        }
        
        # 关键词过滤
        self.musk_keywords = ['Elon Musk', 'musk', '马斯克', '特斯拉', 'Tesla', 'SpaceX', '星链', 'Starlink', 'X.com', 'Twitter', 'Neuralink', 'xAI', 'Grok']
        self.trump_keywords = ['Trump', 'Trump', '特朗普', '川普', 'MAGA', 'Donald Trump', 'biden', 'Biden', '拜登']
        self.ai_keywords = ['AI', 'artificial intelligence', 'GPT', 'OpenAI', 'ChatGPT', 'Claude', 'Gemini', 'LLM', '大模型', '人工智能', '机器学习']
        
        # 失败源记录
        self.failed_sources = []
    
    def get_random_ua(self):
        """获取随机 User-Agent"""
        return random.choice(self.user_agents)
    
    def smart_delay(self, base_delay=1):
        """智能延迟，随机增加时间"""
        delay = base_delay + random.uniform(0.5, 2)
        time.sleep(delay)
    
    def rotate_ua(self):
        """轮换 User-Agent"""
        self.session.headers.update({'User-Agent': self.get_random_ua()})
    
    def is_musk_related(self, title):
        """检查是否与马斯克相关"""
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in self.musk_keywords)
    
    def is_trump_related(self, title):
        """检查是否与特朗普相关"""
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in self.trump_keywords)
    
    def is_priority_news(self, title):
        """判断是否为高优先级新闻"""
        return self.is_musk_related(title) or self.is_trump_related(title)
    
    def fetch_url(self, url, timeout=15, retries=2):
        """带重试和错误处理的 URL 获取"""
        for attempt in range(retries + 1):
            try:
                self.rotate_ua()
                response = self.session.get(url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"  尝试 {attempt + 1}/{retries + 1} 失败: {e}")
                if attempt < retries:
                    wait_time = 2 ** attempt + random.uniform(0, 1)  # 指数退避
                    print(f"  等待 {wait_time:.1f}s 后重试...")
                    time.sleep(wait_time)
                else:
                    return None
        return None
    
    def fetch_feed(self, url, category, source_name, limit=5):
        """通用RSS抓取方法 - 增强反爬"""
        print(f"抓取 {source_name}...")
        try:
            # 使用 feedparser 但添加 headers
            self.rotate_ua()
            feed = feedparser.parse(url, 
                                   agent=self.session.headers.get('User-Agent'),
                                   request_headers=self.session.headers)
            
            if feed.bozo and feed.bozo_exception:
                print(f"  {source_name} 警告: {feed.bozo_exception}")
            
            count = 0
            entries = feed.entries[:limit*2] if feed.entries else []
            
            for entry in entries:
                if count >= limit:
                    break
                    
                # 获取标题和链接
                title = entry.get('title', '')
                link = entry.get('link', entry.get('id', ''))
                
                if not title or not link:
                    continue
                
                # 去重检查
                if any(item['url'] == link for item in self.news_data[category]):
                    continue
                
                item = {
                    'title': title,
                    'url': link,
                    'source': source_name
                }
                
                # 标记高优先级
                if self.is_priority_news(title):
                    item['priority'] = True
                    item['priority_type'] = 'musk' if self.is_musk_related(title) else 'trump'
                
                self.news_data[category].append(item)
                count += 1
            
            if count == 0:
                print(f"  {source_name} 未获取到数据")
            else:
                print(f"  {source_name} 获取 {count} 条")
            
            return count
            
        except Exception as e:
            print(f"  {source_name} 抓取失败: {e}")
            self.failed_sources.append(source_name)
            return 0
    
    def fetch_hackernews(self, limit=8):
        """抓取 Hacker News 热门（增强版）"""
        print("抓取 Hacker News...")
        try:
            # 获取热门故事ID
            response = self.fetch_url('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
            if not response:
                print("  Hacker News 无法获取列表")
                self.failed_sources.append('Hacker News')
                return 0
            
            top_ids = response.json()[:limit*2]
            count = 0
            
            for story_id in top_ids:
                if count >= limit:
                    break
                    
                try:
                    story_response = self.fetch_url(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=8, retries=1
                    )
                    if not story_response:
                        continue
                    
                    story = story_response.json()
                    if story and story.get('title'):
                        url = story.get('url', f'https://news.ycombinator.com/item?id={story_id}')
                        
                        if any(item['url'] == url for item in self.news_data['ai']):
                            continue
                        
                        item = {
                            'title': story['title'],
                            'url': url,
                            'source': 'Hacker News'
                        }
                        
                        # AI 关键词过滤
                        if any(kw.lower() in story['title'].lower() for kw in self.ai_keywords):
                            item['tag'] = 'AI'
                        
                        # 马斯克/特朗普标记
                        if self.is_priority_news(story['title']):
                            item['priority'] = True
                            item['priority_type'] = 'musk' if self.is_musk_related(story['title']) else 'trump'
                        
                        self.news_data['ai'].append(item)
                        count += 1
                        
                except Exception as e:
                    continue
            
            print(f"  Hacker News 获取 {count} 条")
            return count
            
        except Exception as e:
            print(f"  Hacker News 抓取失败: {e}")
            self.failed_sources.append('Hacker News')
            return 0
    
    def fetch_github_trending(self, limit=5):
        """抓取 GitHub Trending（增强反爬）"""
        print("抓取 GitHub Trending...")
        try:
            url = 'https://github.com/trending?since=daily'
            response = self.fetch_url(url, timeout=12)
            
            if not response:
                print("  GitHub Trending 无法获取页面")
                self.failed_sources.append('GitHub Trending')
                return 0
            
            soup = BeautifulSoup(response.text, 'html.parser')
            repos = soup.select('article.Box-row')
            
            if not repos:
                # 尝试备选选择器
                repos = soup.select('h2 a[href^="/"]')
            
            count = 0
            for repo in repos[:limit]:
                try:
                    if repo.name == 'a':
                        # 备选选择器
                        href = repo['href']
                        title = href.strip('/')
                    else:
                        link = repo.select_one('h2 a')
                        if not link:
                            continue
                        href = link['href']
                        title = link.get_text(strip=True).replace('\n', '').replace(' ', '')
                    
                    if not title or not href:
                        continue
                    
                    full_url = f"https://github.com{href}" if href.startswith('/') else href
                    
                    if any(item['url'] == full_url for item in self.news_data['ai']):
                        continue
                    
                    # 获取描述
                    desc_elem = repo.select_one('p.color-fg-muted') if repo.name != 'a' else None
                    description = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    self.news_data['ai'].append({
                        'title': f"🔥 {title}",
                        'url': full_url,
                        'source': 'GitHub Trending',
                        'description': description
                    })
                    count += 1
                    
                except Exception as e:
                    continue
            
            print(f"  GitHub Trending 获取 {count} 条")
            return count
            
        except Exception as e:
            print(f"  GitHub Trending 抓取失败: {e}")
            self.failed_sources.append('GitHub Trending')
            return 0
    
    def fetch_techcrunch(self, limit=5):
        """抓取 TechCrunch"""
        return self.fetch_feed('https://techcrunch.com/feed/', 'ai', 'TechCrunch', limit)
    
    def fetch_theverge(self, limit=5):
        """抓取 The Verge"""
        return self.fetch_feed('https://www.theverge.com/rss/index.xml', 'ai', 'The Verge', limit)
    
    def fetch_arstechnica(self, limit=4):
        """抓取 Ars Technica"""
        return self.fetch_feed('https://arstechnica.com/feed/', 'ai', 'Ars Technica', limit)
    
    def fetch_bbc_tech(self, limit=5):
        """抓取 BBC Technology"""
        return self.fetch_feed('https://feeds.bbci.co.uk/news/technology/rss.xml', 'ai', 'BBC Tech', limit)
    
    def fetch_reuters(self, limit=6):
        """抓取 Reuters"""
        return self.fetch_feed('https://www.reutersagency.com/feed/?best-topics=tech', 'international', 'Reuters', limit)
    
    def fetch_politico(self, limit=5):
        """抓取 Politico"""
        return self.fetch_feed('https://www.politico.com/rss/politics08.xml', 'international', 'Politico', limit)
    
    def fetch_foxnews(self, limit=4):
        """抓取 Fox News"""
        return self.fetch_feed('https://feeds.foxnews.com/foxnews/latest', 'international', 'Fox News', limit)
    
    def fetch_wsj(self, limit=4):
        """抓取 Wall Street Journal"""
        return self.fetch_feed('https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml', 'international', 'WSJ', limit)
    
    def fetch_tesla_news(self, limit=4):
        """抓取 Tesla / 马斯克相关"""
        print("抓取 Tesla/Musk 相关...")
        sources = [
            ('https://electrek.co/feed/', 'Electrek'),
            ('https://teslarati.com/feed/', 'Teslarati'),
        ]
        count = 0
        for url, source in sources:
            try:
                self.rotate_ua()
                feed = feedparser.parse(url, agent=self.session.headers.get('User-Agent'))
                
                for entry in feed.entries[:limit]:
                    item = {
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'source': source,
                        'priority': True,
                        'priority_type': 'musk'
                    }
                    if item['title'] and item['url']:
                        self.news_data['international'].append(item)
                        count += 1
                        
            except Exception as e:
                print(f"  {source} 抓取失败: {e}")
        return count
    
    def fetch_producthunt(self, limit=4):
        """抓取 Product Hunt"""
        print("抓取 Product Hunt...")
        return self.fetch_feed('https://www.producthunt.com/feed', 'startup', 'Product Hunt', limit)
    
    def fetch_ai_news(self):
        """AI科技 - 国际化多源"""
        print("\n【AI科技】")
        self.fetch_github_trending(5)
        self.smart_delay()
        
        self.fetch_hackernews(6)
        self.smart_delay()
        
        self.fetch_techcrunch(5)
        self.smart_delay()
        
        self.fetch_theverge(4)
        self.smart_delay()
        
        self.fetch_arstechnica(4)
        self.smart_delay()
        
        self.fetch_bbc_tech(4)
        self.smart_delay()
        
        # 国内补充
        self.fetch_feed('https://www.solidot.org/index.rss', 'ai', 'Solidot', 3)
        self.smart_delay()
    
    def fetch_ecommerce_news(self):
        """跨境电商"""
        print("\n【跨境电商】")
        self.fetch_feed('https://www.cifnews.com/rss', 'ecommerce', '雨果网', 3)
        self.smart_delay()
        
        self.fetch_feed('https://www.ebrun.com/rss/', 'ecommerce', '亿邦动力', 3)
        self.smart_delay()
        
        self.fetch_feed('https://techcrunch.com/category/e-commerce/feed/', 'ecommerce', 'TC EC', 3)
        self.smart_delay()
    
    def fetch_startup_news(self):
        """产品创业"""
        print("\n【产品创业】")
        self.fetch_producthunt(4)
        self.smart_delay()
        
        self.fetch_feed('https://36kr.com/feed', 'startup', '36氪', 3)
        self.smart_delay()
        
        self.fetch_feed('https://www.huxiu.com/rss', 'startup', '虎嗅', 3)
        self.smart_delay()
        
        self.fetch_feed('https://techcrunch.com/category/startups/feed/', 'startup', 'TC Startups', 3)
        self.smart_delay()
    
    def fetch_energy_news(self):
        """能源"""
        print("\n【能源】")
        self.fetch_feed('https://www.in-en.com/rss/', 'energy', '能源界', 3)
        self.smart_delay()
        
        self.fetch_feed('https://www.renewableenergyworld.com/feed/', 'energy', 'REWorld', 3)
        self.smart_delay()
        
        self.fetch_feed('https://electrek.co/feed/', 'energy', 'Electrek', 3)
        self.smart_delay()
    
    def fetch_military_news(self):
        """军事"""
        print("\n【军事】")
        self.fetch_feed('https://mil.huanqiu.com/rss/', 'military', '环球网军事', 3)
        self.smart_delay()
        
        self.fetch_feed('https://feeds.bbci.co.uk/news/world/rss.xml', 'military', 'BBC World', 3)
        self.smart_delay()
    
    def fetch_international_hot(self):
        """国际热点"""
        print("\n【国际热点 - 马斯克/特朗普】")
        self.fetch_tesla_news(4)
        self.smart_delay()
        
        self.fetch_politico(4)
        self.smart_delay()
        
        self.fetch_foxnews(4)
        self.smart_delay()
        
        self.fetch_wsj(3)
        self.smart_delay()
        
        self.fetch_reuters(4)
        self.smart_delay()
    
    def prioritize_news(self):
        """重新排序：优先展示马斯克、特朗普相关"""
        for category in self.news_data:
            priority_news = [n for n in self.news_data[category] if n.get('priority')]
            normal_news = [n for n in self.news_data[category] if not n.get('priority')]
            self.news_data[category] = priority_news + normal_news
    
    def run(self):
        """执行所有抓取任务"""
        print(f"\n{'='*60}")
        print(f"📰 开始抓取 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print('='*60)
        
        # 执行抓取
        self.fetch_ai_news()
        self.fetch_ecommerce_news()
        self.fetch_startup_news()
        self.fetch_energy_news()
        self.fetch_military_news()
        self.fetch_international_hot()
        
        # 重新排序
        self.prioritize_news()
        
        # 统计
        total = sum(len(v) for v in self.news_data.values())
        priority = sum(1 for v in self.news_data.values() for i in v if i.get('priority'))
        
        print(f"\n{'='*60}")
        print(f"✅ 抓取完成 - 总计: {total} 条")
        print(f"🔥 高优先级(马斯克/特朗普): {priority} 条")
        print(f"❌ 失败源: {', '.join(self.failed_sources) if self.failed_sources else '无'}")
        print('='*60)
        
        # 分类统计
        for category, items in self.news_data.items():
            priority_count = sum(1 for i in items if i.get('priority'))
            print(f"  • {category}: {len(items)} 条 (优先: {priority_count})")
        
        return self.news_data

if __name__ == '__main__':
    scraper = NewsScraper()
    result = scraper.run()
    print("\n" + "="*60)
    print("JSON 输出:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
