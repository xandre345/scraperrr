"""
Ben's Bites Web Scraper
Scrapes articles from Ben's Bites posts page
"""

import requests
import json
from typing import List, Dict
from datetime import datetime

def scrape_bensbites() -> List[Dict]:
    """
    Fetch articles from Ben's Bites posts page (which returns JSON)
    Returns list of article dictionaries matching our schema
    """
    url = "https://bensbites.beehiiv.com/posts"
    
    print(f"Fetching Ben's Bites data from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response
        try:
            data = response.json()
        except json.JSONDecodeError:
            # Fallback if it returns HTML but we want to be sure
            print("Response was not valid JSON. Content might be HTML.")
            return []

        articles = []
        
        # The JSON structure seems to be {"posts": [...], "pagination": {...}}
        posts = data.get('posts', [])
        
        for post in posts[:20]:  # Limit to 20 most recent
            try:
                slug = post.get('slug', '')
                link = f"https://bensbites.beehiiv.com/p/{slug}" if slug else ""
                
                if not link:
                    continue
                    
                # Normalize date
                created_at = post.get('created_at', '')
                if created_at:
                    try:
                        # Beehiiv date often has Z and milliseconds, normalize to YYYY-MM-DDTHH:MM:SS
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        published = dt.strftime('%Y-%m-%dT%H:%M:%S')
                    except Exception:
                        published = datetime.now().isoformat()
                else:
                    published = datetime.now().isoformat()

                from bs4 import BeautifulSoup
                summary_raw = post.get('web_subtitle', '')
                summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else ""
                summary = (summary[:250] + '...') if len(summary) > 250 else summary

                article = {
                    "id": post.get('id', link),
                    "title": post.get('web_title', 'No Title'),
                    "summary": summary,
                    "link": link,
                    "published": published,
                    "source": "Ben's Bites",
                    "tags": ["bensbites"],
                    "saved": False
                }
                articles.append(article)
                    
            except Exception as e:
                print(f"Error parsing post: {e}")
                continue
        
        print(f"Successfully fetched {len(articles)} articles from Ben's Bites")
        return articles
        
    except requests.RequestException as e:
        print(f"Error fetching Ben's Bites: {e}")
        return []

def save_to_json(articles: List[Dict], filename: str = "bensbites_articles.json"):
    """Save articles to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filename}")

if __name__ == "__main__":
    # Test the scraper
    articles = scrape_bensbites()
    
    # Display first article as sample
    if articles:
        print("\n--- Sample Article ---")
        print(json.dumps(articles[0], indent=2))
    else:
        print("\nNo articles found.")
    
    # Save to file
    save_to_json(articles)
