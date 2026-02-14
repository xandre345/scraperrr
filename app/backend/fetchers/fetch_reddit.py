"""
Reddit RSS Feed Fetcher
Fetches and parses posts from r/artificial and r/MachineLearning
"""

import feedparser
import json
from typing import List, Dict

def fetch_reddit_feed(subreddit: str) -> List[Dict]:
    """
    Fetch posts from a subreddit's RSS feed
    Args:
        subreddit: subreddit name (e.g., 'artificial', 'MachineLearning')
    Returns:
        List of article dictionaries
    """
    feed_url = f"https://www.reddit.com/r/{subreddit}/.rss"
    
    print(f"Fetching Reddit RSS feed from r/{subreddit}")
    feed = feedparser.parse(feed_url)
    
    articles = []
    
    for entry in feed.entries:
        # Normalize date
        published_dt = entry.get('published_parsed')
        if published_dt:
            # feedparser.published_parsed returns a time.struct_time
            from datetime import datetime
            published = datetime(*published_dt[:6]).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            from datetime import datetime
            published = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        from bs4 import BeautifulSoup
        summary_raw = entry.get('summary', '')
        summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else ""
        # Truncate aggressively to prevent data blobs
        summary = (summary[:250] + '...') if len(summary) > 250 else summary

        article = {
            "id": entry.get('id', entry.get('link', '')),
            "title": entry.get('title', 'No Title'),
            "summary": summary,
            "link": entry.get('link', ''),
            "published": published,
            "source": f"r/{subreddit}",
            "tags": [subreddit, "reddit"],
            "saved": False
        }
        articles.append(article)
    
    print(f"Successfully fetched {len(articles)} posts from r/{subreddit}")
    return articles

def fetch_all_reddit() -> List[Dict]:
    """Fetch from all configured subreddits"""
    subreddits = ['artificial', 'MachineLearning']
    all_articles = []
    
    for subreddit in subreddits:
        articles = fetch_reddit_feed(subreddit)
        all_articles.extend(articles)
    
    return all_articles

def save_to_json(articles: List[Dict], filename: str = "reddit_articles.json"):
    """Save articles to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filename}")

if __name__ == "__main__":
    # Test the fetcher
    articles = fetch_all_reddit()
    
    # Display first article as sample
    if articles:
        print("\n--- Sample Article ---")
        print(json.dumps(articles[0], indent=2))
    
    # Save to file
    save_to_json(articles)
