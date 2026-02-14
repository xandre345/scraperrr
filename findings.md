# 🔍 Findings & Research Log

**Project:** AI News Dashboard  
**Last Updated:** 2026-02-13T11:49:21-05:00

---

## Discovery Phase

### User Requirements
- **Confirmed:** Save/favorite functionality with persistent display
- **Confirmed:** Web scraping approach for Phase 1
- **Confirmed:** Local JSON storage (`.tmp/` directory)
- **Confirmed:** Dark mode, modern UI with brand colors
- **Confirmed:** Summary view with modal for full content
- **Confirmed:** Deduplication across sources
- **Confirmed:** Error display when sources fail

### Brand Guidelines
**File:** `c:\ANTIGRAVITY\Scraperrr\DesignGuidelines\brandguidelines`

**Colors:**
- Primary/Accent: `#BFF549` (bright lime green)
- Background: `#000000` (black)
- Text Primary: `#000000` (black - for light backgrounds)
- Links: `#99A1AF` (gray-blue)

**Typography:**
- Font Family: Inter
- H1: 96px
- H2: 48px
- Body: 24px

### Technical Decisions
- **Tech Stack:** Vanilla HTML/CSS/JavaScript (no framework for simplicity)
- **Storage:** Local JSON files (migrate to Supabase in Phase 2)
- **Scraping:** Python scripts with BeautifulSoup/Selenium (TBD based on site structure)
- **Hosting:** Local file for now (future: Vercel/Netlify)

---

## Research Completed ✅

### The AI Rundown (The Rundown AI)
- **Website:** https://therundown.ai
- **RSS Feed:** https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml ✅
- **Platform:** Beehiiv (newsletter platform)
- **Status:** RSS feed confirmed working
- **Approach:** Use RSS parsing instead of web scraping

### Ben's Bites
- **Website:** https://bensbites.beehiiv.com
- **Platform:** Beehiiv (newsletter platform)
- **RSS Feed:** Likely follows format `https://rss.beehiiv.com/feeds/[ID].xml`
- **Status:** Need to find specific feed ID
- **Approach:** Use RSS parsing instead of web scraping

## Research Needed

### Ben's Bites RSS Feed ID
- [ ] Find the specific Beehiiv feed ID for Ben's Bites
- [ ] Test RSS feed accessibility
- [ ] Verify article structure in RSS

### Deduplication Strategy
- [ ] Research fuzzy string matching libraries (e.g., `fuzzywuzzy`, `difflib`)
- [ ] Define similarity threshold (suggested: 90%)
- [ ] Handle edge cases (same article, different titles)

---

## Constraints & Discoveries

### Known Constraints
- No API keys available for Phase 1
- Must handle scraping failures gracefully
- 24-hour refresh cycle (automation TBD)
- Articles must be from last 24 hours only

### User Decisions (2026-02-13)
- ✅ **Ben's Bites:** Use web scraping (RSS not publicly available)
- ✅ **The AI Rundown:** Use RSS feed (https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml)
- ✅ **Reddit Integration:** Add r/artificial and r/MachineLearning feeds
- ✅ **Design:** Adapt designinspo.png style to news dashboard context
- ✅ **Automation:** Defer to Phase 5 (Windows Task Scheduler)

### Open Questions (Resolved)
- ~~How to automate 24h refresh?~~ → Phase 5 (Task Scheduler)
- Should we cache images locally or hotlink? → TBD during build
- What happens if both sources fail? (Show cached data?) → Display error banner

---

### Phase 2: Link (Connectivity)
- **The AI Rundown**: RSS feed (`https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml`) is working and returns full article data.
- **Ben's Bites**: 
  - RSS feed is private/unavailable.
  - **Discovery**: The `/posts` page (`https://bensbites.beehiiv.com/posts`) returns a JSON response with article data! This is much more reliable than HTML scraping.
  - Implemented a fetcher using this JSON endpoint.
- **Reddit**:
  - `r/artificial` and `r/MachineLearning` RSS feeds are working.
  - Data mapping is straightforward (title -> title, selftext/html -> summary).

## Open Questions
- [x] Can we scrape Ben's Bites? -> Yes, found a JSON endpoint which is even better.
- [x] Are Reddit feeds reliable? -> Yes, standard Reddit RSS works fine.

## Next Steps
- Move to **Phase 3: Architect**.
- Set up the main application structure.
- Combine the fetchers into a unified data service.
- Build the frontend dashboard.
