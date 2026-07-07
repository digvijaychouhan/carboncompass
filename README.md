# 🧭 CarbonCompass

> Your daily climate & carbon consultancy knowledge hub — auto-updated, zero hosting cost.

**Live at:** `https://digvijaychouhan.github.io/carboncompass`

---

## 📁 File Structure

```
carboncompass/
├── index.html              ← The website (never edit directly)
├── fetch_news.py           ← Auto news fetcher (runs via GitHub Actions)
├── data/
│   ├── news.json           ← Auto-updated daily ← DO NOT manually edit
│   ├── guides.json         ← YOUR topic guides (CBAM, GHG, ISO etc.)
│   ├── certifications.json ← Certifications to track
│   ├── startups.json       ← Climate startups to watch
│   └── articles.json       ← Your knowledge articles
└── .github/
    └── workflows/
        └── update.yml      ← Daily automation config
```

---

## ✏️ How to Add/Edit Content

### Add a News Item (manual)
Open `data/news.json` and add at the top:
```json
{
  "id": 999,
  "title": "Your news headline here",
  "source": "Source Name",
  "date": "2026-06-07",
  "url": "https://link-to-article.com",
  "tag": "CBAM",
  "summary": "Brief summary of the news item.",
  "manual": true
}
```
> Set `"manual": true` so the auto-updater doesn't remove it.

**Available tags:** `CBAM`, `GHG`, `ISO 14064`, `BRSR`, `Carbon Credits`, `Carbon Markets`, `Net Zero`, `India Policy`, `ESG`, `SBTi`, `Energy`, `Startups`, `Climate`

---

### Add a Knowledge Article
Open `data/articles.json` and add:
```json
{
  "id": 3,
  "title": "Your Article Title",
  "date": "2026-06-07",
  "author": "Your Name",
  "tags": ["CBAM", "Export"],
  "readTime": "5 min",
  "summary": "One-line summary shown in the card.",
  "content": "Full article text goes here. Can be long."
}
```

---

### Add a Topic Guide
Open `data/guides.json` and add:
```json
{
  "id": "yourtopic",
  "title": "Topic Name",
  "icon": "🌱",
  "tag": "Category",
  "level": "Beginner / Intermediate / Advanced",
  "summary": "What this guide covers.",
  "keyPoints": [
    "Point one",
    "Point two",
    "Point three"
  ],
  "resources": [
    { "label": "Official Website", "url": "https://example.com" }
  ]
}
```

---

### Add a Startup
Open `data/startups.json` and add:
```json
{
  "id": 6,
  "name": "StartupName",
  "country": "🇮🇳 India",
  "focus": "What they do",
  "stage": "Seed / Series A / Growth",
  "raise": "$5M",
  "year": 2024,
  "url": "https://startup.com",
  "description": "Brief description of the startup."
}
```

---

### Add a Certification
Open `data/certifications.json` and add:
```json
{
  "id": 7,
  "name": "Certification Name",
  "provider": "Issuing Body",
  "status": "recommended",
  "level": "Foundation / Professional / Specialist",
  "duration": "3 months",
  "cost": "₹15,000",
  "url": "https://cert-url.com",
  "description": "What this certification covers and who it is for.",
  "tags": ["GHG", "ISO"]
}
```
> `status` options: `recommended` (green) or `explore` (amber)

---

## 🤖 Auto-Update Setup (One Time)

### Step 1 — Get a Free NewsAPI Key
1. Go to [newsapi.org](https://newsapi.org) → Get API Key (free)
2. Copy your API key

### Step 2 — Add Secret to GitHub
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `NEWS_API_KEY`  Value: your API key
4. Save

### Step 3 — Enable GitHub Actions
1. Go to **Actions** tab in your repo
2. Click **Enable GitHub Actions**

That's it. News will auto-update every day at 6 AM IST. You can also click **Run workflow** manually anytime.

---

## 🚀 Deployment (One Time)

1. Create GitHub account at [github.com](https://github.com)
2. Create new repo named `carboncompass` (Public)
3. Upload all these files (drag & drop)
4. Go to **Settings → Pages → Source → Deploy from branch → main → Save**
5. Site is live at `https://yourusername.github.io/carboncompass`

---

## 🌐 Custom Domain (Optional)
1. Buy `carboncompass.in` (~₹800/yr)
2. Go to repo **Settings → Pages → Custom domain**
3. Enter `carboncompass.in` and save
4. Add CNAME record at your domain registrar pointing to `yourusername.github.io`

---

*Built for climate consultants. Updated daily. Zero cost.*
