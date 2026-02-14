# 🚀 AI News Dashboard - Project Constitution

**Last Updated:** 2026-02-13T11:49:21-05:00

---

## 📋 Project Overview

**North Star:** A beautiful, interactive dashboard displaying the latest AI news articles from multiple sources, with save/favorite functionality and 24-hour auto-refresh.

**Current Phase:** Protocol 0 - Initialization

---

## 🎯 Discovery Answers

### 1. North Star (Desired Outcome)
Interactive web dashboard that:
- Displays latest articles from last 24 hours
- Allows users to save/favorite articles
- Saved articles persist and remain visible
- Auto-refreshes every 24 hours
- Beautiful, modern dark mode UI

### 2. Integrations
**Phase 1 (Current):**
- Ben's Bites (web scraping)
- The AI Rundown (web scraping)

**Phase 2 (Future):**
- Reddit API
- Supabase (database migration)

**API Keys:** None required for Phase 1 (web scraping)

### 3. Source of Truth
**Phase 1:** Local JSON files in `.tmp/` directory
**Phase 2:** Migrate to Supabase database

### 4. Delivery Payload
- **Format:** Standalone HTML/CSS/JavaScript dashboard
- **Hosting:** Local file (open in browser)
- **Refresh:** Every 24 hours
- **Behavior:** Show new articles if available, skip if none

### 5. Behavioral Rules
- **UI Style:** Dark mode, modern, minimalist
- **Brand Colors:** 
  - Primary/Accent: `#BFF549`
  - Background: `#000000`
  - Text: `#000000` (on light backgrounds)
  - Links: `#99A1AF`
- **Typography:** Inter font (96px h1, 48px h2, 24px body)
- **Article Display:** Summary view with "click for more" modal
- **Deduplication:** Remove duplicate articles across sources
- **Error Handling:** Display error messages if source fails

---

## 📊 Data Schema

### Article Object (JSON)
```json
{
  "id": "string (UUID)",
  "title": "string",
  "summary": "string (max 200 chars)",
  "fullContent": "string (optional)",
  "url": "string (source URL)",
  "source": "string (e.g., 'Ben's Bites', 'The AI Rundown')",
  "publishedDate": "string (ISO 8601)",
  "scrapedDate": "string (ISO 8601)",
  "imageUrl": "string (optional)",
  "isSaved": "boolean (default: false)",
  "tags": ["string"] (optional)
}
```

### Storage Structure
```json
{
  "lastUpdated": "string (ISO 8601)",
  "articles": [
    // Array of Article objects
  ],
  "savedArticles": [
    // Array of saved Article IDs
  ]
}
```

**File Location:** `.tmp/articles_data.json`

---

## 🏗️ Architecture Invariants

### Layer 1: Architecture (`architecture/`)
- SOPs written in Markdown
- Define scraping logic, deduplication rules, UI behavior
- **Rule:** Update SOP before updating code

### Layer 2: Navigation (Orchestration)
- Reasoning layer for routing data
- Calls tools in correct sequence
- No complex business logic here

### Layer 3: Tools (`tools/`)
- Deterministic Python scripts
- Atomic, testable functions
- Environment variables in `.env` (if needed)
- Intermediate files in `.tmp/`

---

## 🔒 Constraints & Rules

1. **Data-First Rule:** Schema defined ✅ (see above)
2. **No Guessing:** All scraping logic must be tested and verified
3. **Self-Annealing:** On error, fix tool + update architecture SOP
4. **Deliverables vs. Intermediates:**
   - **Intermediate:** `.tmp/articles_data.json`, scraper logs
   - **Deliverable:** `dashboard.html` (final UI)
5. **Deduplication Logic:** Match by title similarity (>90%) or exact URL match
6. **24h Refresh:** Only fetch articles published in last 24 hours

---

## 📁 File Structure

```
c:\ANTIGRAVITY\Scraperrr\
├── gemini.md                    # This file (Project Constitution)
├── .env                         # API keys (future use)
├── architecture/                # Layer 1: SOPs
│   ├── scraping_strategy.md
│   ├── deduplication_logic.md
│   └── ui_behavior.md
├── tools/                       # Layer 3: Python Scripts
│   ├── scrape_bens_bites.py
│   ├── scrape_ai_rundown.py
│   ├── deduplicate_articles.py
│   └── fetch_all_sources.py
├── .tmp/                        # Temporary data
│   ├── articles_data.json
│   └── scraper_logs/
├── DesignGuidelines/
│   └── brandguidelines          # Brand colors & typography
└── dashboard.html               # Final deliverable
```

---

## 🧪 Testing Requirements

- [ ] Verify scrapers retrieve articles from last 24h
- [ ] Test deduplication with known duplicates
- [ ] Validate JSON schema compliance
- [ ] Test save/favorite persistence
- [ ] Verify modal functionality
- [ ] Test error display when source fails
- [ ] Validate brand color application

---

## 📝 Maintenance Log

**2026-02-13:** Project initialized, schema defined, brand guidelines integrated
