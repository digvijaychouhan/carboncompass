"""
CarbonCompass — Daily News Fetcher
Pulls from RSS feeds (free) + NewsAPI (free tier)
Run by GitHub Actions every day at 6 AM IST
"""

import json, os, feedparser, requests
from datetime import datetime, timezone
from dateutil import parser as dateparser

TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')
NEWS_FILE = 'data/news.json'
MAX_ITEMS = 20  # Max news items to keep

# ── FREE RSS FEEDS (no API key needed) ──
RSS_FEEDS = [
    {
        'url': 'https://www.carbonbrief.org/feed/',
        'source': 'Carbon Brief',
        'default_tag': 'Climate Science'
    },
    {
        'url': 'https://unfccc.int/rss.xml',
        'source': 'UNFCCC',
        'default_tag': 'Policy'
    },
    {
        'url': 'https://www.iea.org/rss/news.xml',
        'source': 'IEA',
        'default_tag': 'Energy'
    },
    {
        'url': 'https://www.climatechangenews.com/feed/',
        'source': 'Climate Home News',
        'default_tag': 'Climate Policy'
    },
]

# ── KEYWORD → TAG MAPPING ──
TAG_MAP = {
    'cbam': 'CBAM',
    'carbon border': 'CBAM',
    'ghg': 'GHG',
    'greenhouse gas': 'GHG',
    'iso 14064': 'ISO 14064',
    'brsr': 'BRSR',
    'carbon credit': 'Carbon Credits',
    'carbon market': 'Carbon Markets',
    'ets': 'Carbon Markets',
    'net zero': 'Net Zero',
    'sbti': 'SBTi',
    'ccts': 'India Policy',
    'india': 'India Policy',
    'scope 3': 'GHG',
    'tcfd': 'ESG',
    'esg': 'ESG',
    'renewable': 'Energy',
    'solar': 'Energy',
    'startup': 'Startups',
}

def guess_tag(title, summary):
    text = (title + ' ' + summary).lower()
    for keyword, tag in TAG_MAP.items():
        if keyword in text:
            return tag
    return 'Climate'

def fetch_rss():
    items = []
    for feed_cfg in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_cfg['url'])
            for entry in feed.entries[:5]:
                title = entry.get('title', '').strip()
                summary = entry.get('summary', entry.get('description', '')).strip()
                # Clean HTML tags from summary
                import re
                summary = re.sub('<[^>]+>', '', summary)[:300]
                link = entry.get('link', '#')
                
                # Parse date
                try:
                    pub = entry.get('published', entry.get('updated', TODAY))
                    date_str = dateparser.parse(pub).strftime('%Y-%m-%d')
                except:
                    date_str = TODAY

                tag = guess_tag(title, summary)

                items.append({
                    'id': abs(hash(title)) % 100000,
                    'title': title,
                    'source': feed_cfg['source'],
                    'date': date_str,
                    'url': link,
                    'tag': tag,
                    'summary': summary[:280] + ('...' if len(summary) > 280 else '')
                })
        except Exception as e:
            print(f"RSS error ({feed_cfg['source']}): {e}")
    return items

def fetch_newsapi():
    """Uses NewsAPI free tier (100 req/day). Add NEWS_API_KEY secret in GitHub."""
    api_key = os.environ.get('NEWS_API_KEY', '')
    if not api_key:
        print("No NEWS_API_KEY found — skipping NewsAPI fetch. RSS only.")
        return []
    
    queries = ['carbon credits', 'CBAM carbon border', 'climate policy india', 'net zero emissions']
    items = []
    
    for q in queries:
        try:
            resp = requests.get('https://newsapi.org/v2/everything', params={
                'q': q, 'sortBy': 'publishedAt', 'pageSize': 3,
                'language': 'en', 'apiKey': api_key
            }, timeout=10)
            for article in resp.json().get('articles', []):
                title = article.get('title', '').strip()
                summary = article.get('description', '').strip() or ''
                if not title or title == '[Removed]':
                    continue
                items.append({
                    'id': abs(hash(title)) % 100000,
                    'title': title,
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'date': article.get('publishedAt', TODAY)[:10],
                    'url': article.get('url', '#'),
                    'tag': guess_tag(title, summary),
                    'summary': summary[:280]
                })
        except Exception as e:
            print(f"NewsAPI error ({q}): {e}")
    return items

def main():
    print(f"🌿 CarbonCompass news fetch — {TODAY}")
    
    # Load existing news (to keep manual entries)
    existing = []
    try:
        with open(NEWS_FILE) as f:
            existing = json.load(f)
            # Keep only manually curated items (no auto-fetched duplicates)
            existing = [e for e in existing if e.get('manual', False)]
    except:
        pass
    
    # Fetch from sources
    rss_items = fetch_rss()
    api_items = fetch_newsapi()
    
    all_items = rss_items + api_items
    print(f"  Fetched: {len(rss_items)} RSS + {len(api_items)} API items")
    
    # Deduplicate by title similarity
    seen_titles = set()
    deduped = []
    for item in sorted(all_items, key=lambda x: x['date'], reverse=True):
        key = item['title'][:60].lower()
        if key not in seen_titles:
            seen_titles.add(key)
            deduped.append(item)
    
    # Merge: manual items first, then auto-fetched
    final = existing + deduped
    final = final[:MAX_ITEMS]
    
    # Re-number IDs
    for i, item in enumerate(final, 1):
        item['id'] = i
    
    with open(NEWS_FILE, 'w') as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Saved {len(final)} items to {NEWS_FILE}")

if __name__ == '__main__':
    main()
