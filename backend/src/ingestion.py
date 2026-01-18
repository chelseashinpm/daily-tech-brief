"""
Daily Tech Brief - Content Ingestion Script
Fetches articles from RSS feeds, processes with Gemini, and saves to Supabase
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import feedparser
import google.generativeai as genai
from supabase import create_client, Client
from dotenv import load_dotenv
import dateparser

from sources import TRUSTED_SOURCES, RELEVANT_KEYWORDS, TOPICS

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-flash-latest')

# Configure Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def get_url_hash(url: str) -> str:
    """Generate a hash for URL deduplication"""
    return hashlib.md5(url.encode()).hexdigest()


def is_recent(published_date: str, hours: int = 48) -> bool:
    """Check if article was published within the last N hours"""
    try:
        parsed_date = dateparser.parse(published_date)
        if not parsed_date:
            # If we can't parse the date, assume it's recent
            return True

        cutoff = datetime.now() - timedelta(hours=hours)
        return parsed_date > cutoff
    except:
        # If there's an error, assume it's recent
        return True


def contains_relevant_keywords(text: str) -> bool:
    """Check if text contains any relevant keywords"""
    text_lower = text.lower()
    # For tech sources, we're already filtering by source, so be more permissive
    # Just exclude obviously non-tech content
    excluded = ["sports", "weather", "recipe", "fashion", "celebrity gossip"]
    if any(ex in text_lower for ex in excluded):
        return False
    return True  # Accept all tech content from our trusted sources


def check_duplicate(url: str) -> bool:
    """Check if URL already exists in database"""
    try:
        result = supabase.table("stories").select("id").eq("url", url).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error checking duplicate: {e}")
        return False


def fetch_articles() -> List[Dict]:
    """Fetch articles from all trusted sources"""
    print(f"Fetching articles from {len(TRUSTED_SOURCES)} sources...")

    all_articles = []

    for source in TRUSTED_SOURCES:
        try:
            print(f"  Fetching from {source['name']}...")
            feed = feedparser.parse(source['rss_url'])

            for entry in feed.entries[:15]:  # Top 15 per source
                # Extract data
                article = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": entry.get("published", ""),
                    "source_name": source["name"],
                    "source_domain": source["domain"],
                    "trust_score": source["trust_score"],
                }

                # Filter: Check if recent (7 days for testing)
                if not is_recent(article["published"], hours=168):
                    continue

                # Filter: Check if contains relevant keywords
                combined_text = f"{article['title']} {article['summary']}"
                if not contains_relevant_keywords(combined_text):
                    continue

                # Filter: Check for duplicates
                if check_duplicate(article["url"]):
                    continue

                all_articles.append(article)

            print(f"    [OK] Found {len([a for a in all_articles if a['source_name'] == source['name']])} relevant articles")

        except Exception as e:
            print(f"    [ERROR] Error fetching from {source['name']}: {e}")
            continue

    print(f"\nTotal articles to process: {len(all_articles)}")
    return all_articles


def process_with_gemini(article: Dict) -> Optional[Dict]:
    """Process article with Gemini API to classify and summarize"""

    prompt = f"""You are analyzing a tech news article for a daily brief focused on:
- Big Tech product and strategy moves
- Government regulation shaping technology decisions
- AI security, safety, and compliance trends
- Startup ecosystem news

Article Title: {article['title']}
Article Summary: {article['summary'][:1000]}
Source: {article['source_name']}

Please analyze this article and provide:

1. **Topics** (select ALL that apply from this list):
   - Big Tech & Product Strategy
   - Startups & Ecosystem
   - Government Regulation & Policy
   - AI Security, Safety, and Privacy

2. **Summary** (EXACTLY 3 sentences):
   - Sentence 1: What happened (the key event or announcement)
   - Sentence 2: Why it matters (the implications)
   - Sentence 3: Who it impacts (products, startups, users, or policy)

3. **Relevance Score** (0.0 to 1.0):
   - How relevant is this to product managers, founders, and people interested in tech?
   - 1.0 = extremely relevant (major product launch, regulation change, security incident)
   - 0.5 = moderately relevant (interesting but not critical)
   - 0.0 = not relevant (off-topic, minor update)

Respond in JSON format:
{{
  "topics": ["topic1", "topic2"],
  "summary": "Three sentence summary here.",
  "relevance_score": 0.8
}}
"""

    try:
        response = model.generate_content(prompt)

        # Extract JSON from response
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        return {
            "topics": result.get("topics", []),
            "summary": result.get("summary", ""),
            "relevance_score": result.get("relevance_score", 0.5),
        }

    except Exception as e:
        print(f"    [ERROR] Error processing with Gemini: {e}")
        return None


def save_to_database(article: Dict, analysis: Dict) -> bool:
    """Save processed article to Supabase"""
    try:
        data = {
            "title": article["title"],
            "url": article["url"],
            "source": article["source_name"],
            "source_domain": article["source_domain"],
            "raw_content": article["summary"][:2000],  # Limit size
            "summary": analysis["summary"],
            "topics": analysis["topics"],
            "trust_score": article["trust_score"],
            "relevance_score": analysis["relevance_score"],
            "published_at": article["published"],
            "status": "processed",
        }

        supabase.table("stories").insert(data).execute()
        return True

    except Exception as e:
        print(f"    [ERROR] Error saving to database: {e}")
        return False


def main():
    """Main ingestion workflow"""
    print("=" * 60)
    print("Daily Tech Brief - Content Ingestion")
    print("=" * 60)
    print()

    # Step 1: Fetch articles
    articles = fetch_articles()

    if not articles:
        print("\n[WARNING] No new articles found. Exiting.")
        return

    # Step 2: Process with Gemini (limit to top 25 to stay within free tier)
    print(f"\nProcessing articles with Gemini API...")
    processed_count = 0

    # Sort by source diversity first (to ensure we get articles from different sources)
    # Group by source, then take top articles from each source in round-robin
    from collections import defaultdict
    import random

    articles_by_source = defaultdict(list)
    for article in articles:
        articles_by_source[article["source_name"]].append(article)

    # Sort articles within each source by trust score
    for source in articles_by_source:
        articles_by_source[source].sort(key=lambda x: x["trust_score"], reverse=True)

    # Round-robin selection from sources to ensure diversity
    diverse_articles = []
    max_per_source = 5  # Max 5 articles per source
    sources = list(articles_by_source.keys())
    for i in range(max_per_source):
        for source in sources:
            if i < len(articles_by_source[source]):
                diverse_articles.append(articles_by_source[source][i])

    articles = diverse_articles

    for i, article in enumerate(articles[:25], 1):
        print(f"\n  [{i}/25] Processing: {article['title'][:60]}...")

        # Add delay to respect rate limits (5 requests/minute = 1 request every 12 seconds)
        if i > 1:  # Skip delay for first request
            print("    [WAIT] Waiting 12 seconds for rate limit...")
            time.sleep(12)

        analysis = process_with_gemini(article)

        if not analysis:
            continue

        # Only save articles with relevance score >= 0.6
        if analysis["relevance_score"] < 0.6:
            print(f"    [SKIP] Skipped (relevance: {analysis['relevance_score']:.2f})")
            continue

        # Save to database
        if save_to_database(article, analysis):
            processed_count += 1
            print(f"    [OK] Saved (relevance: {analysis['relevance_score']:.2f})")

    print(f"\n{'=' * 60}")
    print(f"Ingestion complete!")
    print(f"   Fetched: {len(articles)} articles")
    print(f"   Processed: {processed_count} articles")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
