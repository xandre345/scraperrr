"""
The AI Rundown RSS Feed Fetcher
Fetches and parses articles from The AI Rundown RSS feed
"""

import feedparser
import json
from datetime import datetime
from typing import List, Dict

def fetch_ai_rundown() -> List[Dict]:
    """
    Fetch articles from The AI Rundown RSS feed
    Returns list of article dictionaries matching our schema
    """
    feed_url = "https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml"
    
    print(f"Fetching RSS feed from: {feed_url}")
    feed = feedparser.parse(feed_url)
    
    articles = []
    
    for entry in feed.entries:
        # Normalize date
        published_dt = entry.get('published_parsed')
        if published_dt:
            published = datetime(*published_dt[:6]).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            published = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        from bs4 import BeautifulSoup
        summary_raw = entry.get('summary', '')
        summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else ""
        summary = (summary[:250] + '...') if len(summary) > 250 else summary

        article = {
            "id": entry.get('id', entry.get('link', '')),
            "title": entry.get('title', 'No Title'),
            "summary": summary,
            "link": entry.get('link', ''),
            "published": published,
            "source": "The AI Rundown",
            "tags": [tag.term for tag in entry.get('tags', [])],
            "saved": False
        }
        articles.append(article)
    
    print(f"Successfully fetched {len(articles)} articles from The AI Rundown")
    return articles

def save_to_json(articles: List[Dict], filename: str = "ai_rundown_articles.json"):
    """Save articles to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filename}")

if __name__ == "__main__":
    # Test the fetcher
    articles = fetch_ai_rundown()
    
    # Display first article as sample
    if articles:
        print("\n--- Sample Article ---")
        print(json.dumps(articles[0], indent=2))
    
    # Save to file
    save_to_json(articles)
