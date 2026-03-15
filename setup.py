from setuptools import setup, find_packages

setup(
    name="daily-tech-news-bot",
    version="1.0.0",
    author="cnn2416",
    description="Daily tech news bot with Elon Musk and Donald Trump columns",
    packages=find_packages(),
    install_requires=[
        "feedparser>=6.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "PyYAML>=6.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "daily-news-bot=daily_tech_news_bot:main",
        ],
    },
)