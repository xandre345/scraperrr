# 🗞️ AI News Dashboard

A modern, responsive dashboard that aggregates the latest AI news from various sources (The AI Rundown, Reddit, and Ben's Bites).

## ✨ Features
- **Multi-source Aggregation:** Fetches data from RSS feeds and JSON endpoints.
- **Smart Sorting:** Articles are interleaved chronologically (newest first).
- **Save for Later:** Bookmark articles to your local browser storage.
- **Responsive Design:** Beautiful dark-mode UI that works on mobile and desktop.
- **Clean Content:** Automatically strips HTML and truncates summaries for a unified look.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Node.js (optional, for some build tools if added later)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend
```bash
python -m app.backend.main
```
The API will be available at `http://127.0.0.1:8000`.

### 4. View the Dashboard
Simply open `app/frontend/index.html` in your favorite browser.

## 🏗️ Architecture
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/CSS/JS
- **Data Scraping:** BeautifulSoup4, Feedparser
