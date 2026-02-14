from typing import List, Dict
import sys
import os

# Add parent directory to path to allow imports if running directly
# catch-all for path issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from .models import Article
from .fetchers import fetch_ai_rundown
from .fetchers import fetch_reddit
from .fetchers import scrape_bensbites

import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataService:
    def __init__(self):
        self.sources = {
            "ai_rundown": fetch_ai_rundown.fetch_ai_rundown,
            "reddit": fetch_reddit.fetch_all_reddit,
            "bens_bites": scrape_bensbites.scrape_bensbites
        }
        self.cache_timeout = 900  # Restore 15-minute cache
        self._cache = None
        self._last_fetch_time = 0

    def fetch_all_articles(self) -> List[Article]:
        import time
        current_time = time.time()

        # Return cached data if valid
        if self._cache and (current_time - self._last_fetch_time < self.cache_timeout):
            logger.info(f"Returning cached data ({len(self._cache)} articles)...")
            return self._cache

        all_articles = []
        errors = []
        
        logger.info("Starting global fetch...")
        
        for source_name, fetcher_func in self.sources.items():
            try:
                logger.info(f"Fetching from {source_name}...")
                raw_articles = fetcher_func()
                
                # Convert to Pydantic models to validate
                for raw in raw_articles:
                    try:
                        article = Article(**raw)
                        all_articles.append(article)
                    except Exception as e:
                        logger.error(f"Validation error for article from {source_name}: {e}")
                        
            except Exception as e:
                error_msg = f"Error fetching from {source_name}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)
                
        # Sort by published date (newest first)
        try:
            from datetime import datetime
            # Robust sort: parse strings to datetime objects for comparison
            all_articles.sort(key=lambda x: datetime.fromisoformat(x.published.split('.')[0]), reverse=True)
            logger.info("Successfully performed rigorous datetime sort.")
        except Exception as e:
            logger.warning(f"Fallback to string sort due to error: {e}")
            all_articles.sort(key=lambda x: x.published, reverse=True)
        
        # Log top 5 with source to verify interleaving
        for a in all_articles[:5]:
            logger.info(f"Top Article: {a.published} | {a.source} | {a.title[:30]}...")
        
        logger.info(f"Global fetch complete. Found {len(all_articles)} articles.")
        
        # Update cache
        if all_articles:
            self._cache = all_articles
            self._last_fetch_time = current_time
            
        return all_articles

if __name__ == "__main__":
    service = DataService()
    articles = service.fetch_all_articles()
    print(f"Fetched {len(articles)} articles")
