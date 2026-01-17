# Daily Tech Brief

An automated daily email product that delivers bite-sized, high-signal summaries of tech news with a focus on:
- Big Tech product and strategy moves
- Government regulation shaping technology decisions
- AI security, safety, and compliance trends
- Startup ecosystem news

**Cost**: $0/month using free tiers of Gemini, Supabase, Vercel, and GitHub Actions

---

## Architecture

```
GitHub Actions (Daily 8 AM UTC)
    ↓
Fetch RSS feeds → Process with Gemini Flash (free)
    ↓
Save to Supabase (PostgreSQL)
    ↓
Display on Next.js site (Vercel)
```

---

## Features

- ✅ Fully automated daily digest generation
- ✅ AI-powered summarization with Gemini Flash
- ✅ Topic classification (Big Tech, Startups, Regulation, AI Security)
- ✅ Curated from trusted sources (TechCrunch, The Verge, OpenAI, etc.)
- ✅ Clean, mobile-friendly reading experience
- ✅ Zero cost using free tiers

---

## Project Structure

```
daily-tech-brief/
├── backend/
│   ├── src/
│   │   ├── ingestion.py         # Fetches RSS feeds & processes with Gemini
│   │   ├── generate_digest.py   # Selects top 5-8 stories for daily digest
│   │   └── sources.py            # Trusted source configuration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Main digest page
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   └── StoryCard.tsx
│   │   └── lib/
│   │       └── supabase.ts       # Supabase client
│   ├── package.json
│   └── .env.local.example
├── database/
│   └── schema.sql                # Supabase database schema
├── .github/
│   └── workflows/
│       └── daily-digest.yml      # Daily automation workflow
└── README.md
```

---

## Setup Instructions

### Prerequisites

1. **Google Gemini API Key** (free tier: 1500 requests/day)
   - Get it at: https://makersuite.google.com/app/apikey

2. **Supabase Account** (free tier: 500MB database)
   - Sign up at: https://supabase.com

3. **Vercel Account** (free tier: unlimited deployments)
   - Sign up at: https://vercel.com

4. **GitHub Account** (free tier: 2000 Actions minutes/month)
   - You already have this!

---

### Step 1: Set Up Supabase Database

1. Create a new project on Supabase
2. Go to SQL Editor and run the schema:
   ```bash
   # Copy contents from database/schema.sql
   ```
3. Note your credentials:
   - Project URL: `https://[project-id].supabase.co`
   - Anon/Public Key: Found in Settings → API

---

### Step 2: Set Up GitHub Repository

1. Create a new GitHub repository
2. Push this code:
   ```bash
   cd daily-tech-brief
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/daily-tech-brief.git
   git push -u origin main
   ```

3. Add GitHub Secrets (Settings → Secrets and variables → Actions):
   - `GEMINI_API_KEY`: Your Gemini API key
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key

---

### Step 3: Test Backend Locally (Optional)

1. Set up Python environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Run ingestion:
   ```bash
   cd src
   python ingestion.py
   ```

4. Generate digest:
   ```bash
   python generate_digest.py
   ```

---

### Step 4: Deploy Frontend to Vercel

1. Install Vercel CLI (optional):
   ```bash
   npm i -g vercel
   ```

2. Deploy via Vercel Dashboard:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Add environment variables:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Deploy!

3. Your site will be live at: `https://your-project.vercel.app`

---

### Step 5: Enable GitHub Actions

1. Go to your repository → Actions tab
2. Enable workflows if prompted
3. The workflow will run daily at 8 AM UTC automatically
4. To test manually:
   - Go to Actions → Daily Tech Brief workflow
   - Click "Run workflow" → Run workflow

---

## Usage

### Daily Automated Workflow

1. **8:00 AM UTC**: GitHub Actions triggers
2. **8:01-8:05 AM**: Ingestion script fetches and processes articles
3. **8:05-8:06 AM**: Digest generation selects top 5-8 stories
4. **8:06 AM+**: Your Vercel site automatically updates (ISR revalidation)
5. **Anytime**: Visit your site to read today's digest

### Manual Trigger

You can manually trigger the workflow anytime:
- Go to GitHub → Actions → Daily Tech Brief
- Click "Run workflow"

---

## Customization

### Adding New Sources

Edit `backend/src/sources.py`:

```python
TRUSTED_SOURCES = [
    {
        "name": "Your Source Name",
        "domain": "example.com",
        "rss_url": "https://example.com/feed",
        "trust_score": 0.9,  # 0.0 to 1.0
    },
    # ... existing sources
]
```

### Adjusting Schedule

Edit `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Change to your preferred time (UTC)
```

### Changing Story Count

Edit `backend/src/generate_digest.py`:

```python
# Change limits in ensure_topic_coverage function
if len(selected_stories) > 8:  # Change 8 to your preferred max
    selected_stories = selected_stories[:8]
```

---

## Cost Breakdown

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| **Gemini Flash** | 1500 req/day | ~25 req/day | $0 |
| **Supabase** | 500MB, 2GB transfer | ~50MB/month | $0 |
| **Vercel** | Unlimited | Static site | $0 |
| **GitHub Actions** | 2000 min/month | ~150 min/month | $0 |
| **Total** | — | — | **$0** |

---

## Troubleshooting

### GitHub Actions Failing

1. Check secrets are set correctly (Actions → Secrets)
2. View logs in Actions tab
3. Common issues:
   - Invalid API keys
   - Supabase connection timeout
   - Rate limits exceeded

### No Digest Showing on Frontend

1. Check if GitHub Actions ran successfully
2. Verify Supabase has data:
   ```sql
   SELECT * FROM daily_digests ORDER BY digest_date DESC LIMIT 1;
   ```
3. Check Vercel deployment logs
4. Ensure environment variables are set in Vercel

### Gemini API Errors

1. Verify API key is correct
2. Check you haven't exceeded 1500 requests/day
3. Try reducing articles processed in `ingestion.py` (line 172)

---

## Monitoring

### View GitHub Actions Logs
- Go to Actions tab in your repository
- Click on latest workflow run
- View detailed logs for each step

### Check Database
- Go to Supabase dashboard
- Table Editor → View `stories` and `daily_digests` tables
- SQL Editor → Run custom queries

### Vercel Analytics
- Go to Vercel dashboard → Your project
- View deployment logs and performance metrics

---

## Future Enhancements

**Low-cost additions**:
- [ ] Email delivery to yourself (Resend free tier: 100/day)
- [ ] Archive page showing past 7 days
- [ ] RSS feed output
- [ ] Topic filtering preferences

**Requires budget**:
- [ ] Subscriber management (if sharing with others)
- [ ] Email delivery at scale (AWS SES: $0.10 per 1K emails)
- [ ] Premium AI models for better quality

---

## License

MIT License - feel free to use and modify for your own projects!

---

## Credits

Built with:
- [Gemini Flash 1.5](https://ai.google.dev/) - AI summarization
- [Supabase](https://supabase.com) - PostgreSQL database
- [Next.js](https://nextjs.org) - React framework
- [Vercel](https://vercel.com) - Deployment
- [GitHub Actions](https://github.com/features/actions) - Automation

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review GitHub Actions logs
3. Open an issue in this repository

Enjoy your daily tech brief! 📰
