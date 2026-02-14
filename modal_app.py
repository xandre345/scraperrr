"""
Modal scheduled scraper for the AI News Dashboard.
Runs every 24 hours, fetches articles from all sources,
and serves them via a web endpoint.
"""

import modal

app = modal.App("ai-news-scraper")

# Persistent key-value store for cached articles
article_dict = modal.Dict.from_name("article-cache", create_if_missing=True)

# Container image with all scraping dependencies + project source
scraper_image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "feedparser==6.0.11",
        "beautifulsoup4==4.12.3",
        "requests==2.31.0",
        "fastapi[standard]",
    )
    .add_local_python_source("app")
)


@app.function(image=scraper_image, schedule=modal.Period(hours=24))
def scrape_all_sources():
    """Scheduled function: fetches articles from all sources every 24 hours."""
    from datetime import datetime

    print(f"[{datetime.utcnow().isoformat()}] Starting scheduled scrape...")

    all_articles = []
    errors = []

    # --- The AI Rundown ---
    try:
        from app.backend.fetchers.fetch_ai_rundown import fetch_ai_rundown
        articles = fetch_ai_rundown()
        all_articles.extend(articles)
        print(f"  AI Rundown: {len(articles)} articles")
    except Exception as e:
        errors.append(f"AI Rundown: {e}")
        print(f"  AI Rundown ERROR: {e}")

    # --- Reddit ---
    try:
        from app.backend.fetchers.fetch_reddit import fetch_all_reddit
        articles = fetch_all_reddit()
        all_articles.extend(articles)
        print(f"  Reddit: {len(articles)} articles")
    except Exception as e:
        errors.append(f"Reddit: {e}")
        print(f"  Reddit ERROR: {e}")

    # --- Ben's Bites ---
    try:
        from app.backend.fetchers.scrape_bensbites import scrape_bensbites
        articles = scrape_bensbites()
        all_articles.extend(articles)
        print(f"  Ben's Bites: {len(articles)} articles")
    except Exception as e:
        errors.append(f"Ben's Bites: {e}")
        print(f"  Ben's Bites ERROR: {e}")

    # Sort by published date (newest first)
    try:
        all_articles.sort(
            key=lambda x: datetime.fromisoformat(x["published"].split(".")[0]),
            reverse=True,
        )
    except Exception:
        all_articles.sort(key=lambda x: x.get("published", ""), reverse=True)

    # Store in Modal Dict
    article_dict["articles"] = all_articles
    article_dict["last_updated"] = datetime.utcnow().isoformat()

    summary = (
        f"Scrape complete: {len(all_articles)} articles. "
        f"Errors: {len(errors)}. "
        f"Last updated: {article_dict['last_updated']}"
    )
    print(summary)
    return summary


@app.function(image=scraper_image)
@modal.fastapi_endpoint(method="GET")
def get_articles():
    """Web endpoint that serves the cached articles."""
    try:
        articles = article_dict["articles"]
        last_updated = article_dict.get("last_updated", "unknown")
    except KeyError:
        # No cached data yet — trigger a fresh scrape
        print("No cached data found. Running initial scrape...")
        scrape_all_sources.remote()
        try:
            articles = article_dict["articles"]
            last_updated = article_dict.get("last_updated", "unknown")
        except KeyError:
            return {"articles": [], "last_updated": None, "error": "Initial scrape in progress. Try again shortly."}

    return {
        "articles": articles,
        "last_updated": last_updated,
        "count": len(articles),
    }
