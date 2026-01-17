# Quick Setup Guide

Follow these steps to get Daily Tech Brief running in 15 minutes.

---

## 1. Get API Keys (5 minutes)

### Gemini API Key (FREE)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key → Save for later

### Supabase Credentials (FREE)
1. Go to: https://supabase.com
2. Click "Start your project" → Sign up
3. Create new project:
   - Name: `daily-tech-brief`
   - Database password: (choose a strong password)
   - Region: (closest to you)
4. Wait 2 minutes for project to initialize
5. Go to Settings → API:
   - Copy "Project URL" → Save for later
   - Copy "anon public" key → Save for later
6. Go to SQL Editor → Click "+ New query"
7. Copy the entire contents of `database/schema.sql` and paste
8. Click "Run" → Database is ready!

---

## 2. Set Up GitHub Repository (3 minutes)

1. Create new repository on GitHub:
   - Repository name: `daily-tech-brief`
   - Private or Public (your choice)
   - Don't initialize with README

2. Push code to GitHub:
   ```bash
   cd daily-tech-brief
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/daily-tech-brief.git
   git push -u origin main
   ```

3. Add secrets to GitHub:
   - Go to your repository
   - Settings → Secrets and variables → Actions
   - Click "New repository secret" for each:

   **Secret 1:**
   - Name: `GEMINI_API_KEY`
   - Value: (paste your Gemini key)

   **Secret 2:**
   - Name: `SUPABASE_URL`
   - Value: (paste your Supabase URL)

   **Secret 3:**
   - Name: `SUPABASE_KEY`
   - Value: (paste your Supabase anon key)

---

## 3. Test Backend Locally (Optional, 5 minutes)

Skip this if you want to go straight to deployment. Otherwise:

```bash
# Set up Python environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials (use nano, vim, or any text editor)

# Run ingestion (this will take 2-3 minutes)
cd src
python ingestion.py

# Generate digest
python generate_digest.py
```

If successful, you'll see:
- ✨ Ingestion complete!
- ✨ Digest generation complete!

---

## 4. Deploy Frontend to Vercel (5 minutes)

### Option A: Via Vercel Dashboard (Recommended)

1. Go to: https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your `daily-tech-brief` repository
5. Configure:
   - Framework Preset: **Next.js**
   - Root Directory: **frontend**
   - Build Command: (leave default)
   - Output Directory: (leave default)
6. Click "Environment Variables" → Add:
   - Name: `NEXT_PUBLIC_SUPABASE_URL`
   - Value: (your Supabase URL)

   - Name: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Value: (your Supabase anon key)

7. Click "Deploy"
8. Wait 2-3 minutes
9. Your site is live! 🎉

### Option B: Via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set root to: frontend
# - Add environment variables when prompted

# Deploy to production
vercel --prod
```

---

## 5. Enable and Test GitHub Actions (2 minutes)

1. Go to your GitHub repository
2. Click "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"
4. Click "Daily Tech Brief" workflow
5. Click "Run workflow" → "Run workflow" (to test immediately)
6. Wait 3-5 minutes
7. Check the logs:
   - ✅ All green = success!
   - ❌ Red = check the error logs

---

## 6. Verify Everything Works

### Check Database
1. Go to Supabase dashboard
2. Table Editor → `stories` table
3. You should see ~15-20 articles

### Check Digest
1. Table Editor → `daily_digests` table
2. You should see 1 row with today's date

### Check Website
1. Go to your Vercel URL (e.g., `https://daily-tech-brief.vercel.app`)
2. You should see 5-8 stories!

---

## Done! 🎉

Your Daily Tech Brief is now:
- ✅ Fully automated
- ✅ Running on free tiers
- ✅ Updating daily at 8 AM UTC
- ✅ Accessible at your Vercel URL

**Bookmark your URL** and check it daily!

---

## What Happens Next?

- **Every day at 8 AM UTC**:
  1. GitHub Actions runs automatically
  2. Fetches latest tech news
  3. Processes with Gemini
  4. Updates your website
  5. You read your digest anytime!

---

## Troubleshooting

### GitHub Actions failing?
- Check that all 3 secrets are set correctly
- View error logs in Actions tab
- Most common: typo in Supabase URL or key

### Website shows "No digest available"?
- Wait until after first GitHub Actions run
- Or manually trigger workflow (Actions → Run workflow)
- Check Supabase has data in `daily_digests` table

### Gemini API errors?
- Verify API key is correct
- Check you haven't exceeded 1500 requests/day (unlikely)
- Try again in a few minutes

---

## Next Steps

### Customize Sources
Edit `backend/src/sources.py` to add/remove RSS feeds

### Change Schedule
Edit `.github/workflows/daily-digest.yml`:
```yaml
schedule:
  - cron: '0 12 * * *'  # Change to 12 PM UTC
```

### Add Email Notifications
See README.md "Future Enhancements" section

---

## Need Help?

Check the main [README.md](./README.md) for:
- Detailed architecture
- Customization options
- Advanced troubleshooting
- Cost breakdown

Enjoy your daily tech brief! 📰
