"""
Daily Tech Brief - Digest Generation Script
Selects top 5-8 stories from processed articles and creates daily digest
"""

import os
from datetime import datetime, date, timedelta
from typing import List, Dict
from collections import Counter

from supabase import create_client, Client
from dotenv import load_dotenv

from sources import TOPICS

# Load environment variables
load_dotenv()

# Configure Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def get_previously_used_story_ids(days: int = 7) -> List[str]:
    """Get story IDs that were already used in previous digests"""
    try:
        cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        result = supabase.table("daily_digests") \
            .select("story_ids") \
            .gte("digest_date", cutoff_date) \
            .execute()

        # Flatten all story_ids from all digests
        used_ids = []
        for digest in result.data:
            used_ids.extend(digest.get("story_ids", []))

        return used_ids
    except Exception as e:
        print(f"Error fetching previous digests: {e}")
        return []


def get_processed_stories(days: int = 2, exclude_story_ids: List[str] = None) -> List[Dict]:
    """Get all processed stories from the last N days, excluding previously used ones"""
    try:
        # Get stories created in the last N days (not published_at, which might be older)
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        result = supabase.table("stories") \
            .select("*") \
            .eq("status", "processed") \
            .gte("created_at", cutoff_date) \
            .order("relevance_score", desc=True) \
            .execute()

        # Filter out previously used stories
        if exclude_story_ids:
            filtered_stories = [
                story for story in result.data
                if story["id"] not in exclude_story_ids
            ]
            return filtered_stories

        return result.data
    except Exception as e:
        print(f"Error fetching stories: {e}")
        return []


def check_topic_distribution(selected_stories: List[Dict]) -> Dict[str, int]:
    """Check topic distribution in selected stories"""
    topic_counts = Counter()

    for story in selected_stories:
        for topic in story.get("topics", []):
            topic_counts[topic] += 1

    return dict(topic_counts)


def ensure_topic_coverage(stories: List[Dict]) -> List[Dict]:
    """
    Ensure minimum coverage requirements:
    - At least 1 Regulation/Policy
    - At least 1 AI Security/Safety
    - At least 1 Startup/Product Strategy
    """

    required_topics = {
        "Government Regulation & Policy": 1,
        "AI Security, Safety, and Privacy": 1,
        "Startups & Ecosystem": 1,
    }

    selected = []
    topic_coverage = {topic: 0 for topic in required_topics}

    # First pass: Select stories to meet minimum requirements
    for story in stories:
        story_topics = story.get("topics", [])

        # Check if this story helps meet requirements
        for req_topic in required_topics:
            if req_topic in story_topics and topic_coverage[req_topic] < required_topics[req_topic]:
                if story not in selected:
                    selected.append(story)
                topic_coverage[req_topic] += 1
                break

        # Stop if we've met all requirements
        if all(count >= req for req, count in zip(required_topics.values(), topic_coverage.values())):
            break

    # Second pass: Fill remaining slots with highest relevance stories
    remaining_slots = 8 - len(selected)

    for story in stories:
        if story not in selected and len(selected) < 8:
            selected.append(story)

    return selected


def create_daily_digest(stories: List[Dict]) -> bool:
    """Create daily digest entry in database"""
    try:
        today = date.today()

        # Check if digest already exists for today
        existing = supabase.table("daily_digests") \
            .select("id") \
            .eq("digest_date", today.isoformat()) \
            .execute()

        story_ids = [story["id"] for story in stories]

        if existing.data:
            # Update existing digest
            supabase.table("daily_digests") \
                .update({"story_ids": story_ids}) \
                .eq("digest_date", today.isoformat()) \
                .execute()
            print(f"[OK] Updated existing digest for {today}")
        else:
            # Create new digest
            supabase.table("daily_digests").insert({
                "digest_date": today.isoformat(),
                "story_ids": story_ids,
                "status": "ready",
            }).execute()
            print(f"[OK] Created new digest for {today}")

        return True

    except Exception as e:
        print(f"[ERROR] Error creating digest: {e}")
        return False


def main():
    """Main digest generation workflow"""
    print("=" * 60)
    print("Daily Tech Brief - Digest Generation")
    print("=" * 60)
    print()

    # Step 1: Get previously used story IDs
    print("Checking previously used stories...")
    used_story_ids = get_previously_used_story_ids(days=7)
    print(f"   Excluding {len(used_story_ids)} previously used stories")

    # Step 2: Get processed stories (excluding previously used)
    print("\nFetching fresh processed stories...")
    stories = get_processed_stories(days=2, exclude_story_ids=used_story_ids)

    if not stories:
        print("[WARNING] No fresh stories found. Run ingestion or extend search window.")
        return

    print(f"   Found {len(stories)} fresh processed stories")

    # Step 3: Select top stories with topic distribution
    print("\nSelecting stories for digest...")

    # Ensure topic coverage
    selected_stories = ensure_topic_coverage(stories)

    # Limit to 5-8 stories
    if len(selected_stories) > 8:
        selected_stories = selected_stories[:8]

    if len(selected_stories) < 5:
        print(f"[WARNING] Only {len(selected_stories)} stories available (need at least 5)")
        # Continue anyway with what we have

    # Step 4: Display selection
    print(f"\n   Selected {len(selected_stories)} stories:")
    for i, story in enumerate(selected_stories, 1):
        print(f"     {i}. {story['title'][:60]}...")
        print(f"        Topics: {', '.join(story.get('topics', []))}")
        print(f"        Relevance: {story.get('relevance_score', 0):.2f}")
        print()

    # Check topic distribution
    distribution = check_topic_distribution(selected_stories)
    print("   Topic Distribution:")
    for topic, count in distribution.items():
        print(f"     - {topic}: {count}")

    # Step 5: Create digest
    print(f"\nCreating daily digest...")
    if create_daily_digest(selected_stories):
        print(f"\n{'=' * 60}")
        print("Digest generation complete!")
        print(f"{'=' * 60}")
    else:
        print("\n[ERROR] Failed to create digest")


if __name__ == "__main__":
    main()
