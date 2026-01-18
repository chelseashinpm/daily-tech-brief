"""
Daily Tech Brief - Email Delivery Script
Sends the daily digest via email using Resend
"""

import os
from datetime import date
from typing import List, Dict

from supabase import create_client, Client
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Resend configuration
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_API_URL = "https://api.resend.com/emails"


def get_todays_digest() -> Dict:
    """Get today's digest with stories"""
    try:
        today = date.today()

        # Get today's digest
        digest_result = supabase.table("daily_digests") \
            .select("*") \
            .eq("digest_date", today.isoformat()) \
            .single() \
            .execute()

        if not digest_result.data:
            return None

        digest = digest_result.data

        # Get stories
        stories_result = supabase.table("stories") \
            .select("*") \
            .in_("id", digest["story_ids"]) \
            .execute()

        # Sort stories by the order in story_ids
        stories_dict = {story["id"]: story for story in stories_result.data}
        sorted_stories = [stories_dict[story_id] for story_id in digest["story_ids"] if story_id in stories_dict]

        digest["stories"] = sorted_stories
        return digest

    except Exception as e:
        print(f"Error fetching digest: {e}")
        return None


def generate_html_email(digest: Dict) -> str:
    """Generate HTML email content"""

    stories_html = ""
    for i, story in enumerate(digest["stories"], 1):
        topics_html = " ".join([
            f'<span style="display: inline-block; padding: 4px 8px; margin: 2px; background-color: #e5e7eb; border-radius: 4px; font-size: 12px;">{topic}</span>'
            for topic in story.get("topics", [])
        ])

        stories_html += f"""
        <div style="margin-bottom: 30px; padding-bottom: 30px; border-bottom: 1px solid #e5e7eb;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 32px; height: 32px; background-color: #111827; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">
                    {i}
                </div>
                <div>
                    <div style="margin-bottom: 5px;">{topics_html}</div>
                </div>
            </div>
            <h2 style="font-size: 20px; font-weight: 600; margin: 10px 0; color: #111827;">
                <a href="{story['url']}" style="color: #111827; text-decoration: none;">{story['title']}</a>
            </h2>
            <p style="font-size: 14px; color: #6b7280; margin: 5px 0;">{story['source']}</p>
            <p style="font-size: 16px; line-height: 1.6; color: #374151; margin: 15px 0;">{story['summary']}</p>
            <a href="{story['url']}" style="color: #2563eb; text-decoration: none; font-weight: 500; font-size: 14px;">
                Read full article →
            </a>
        </div>
        """

    formatted_date = date.today().strftime("%A, %B %d, %Y")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; margin: 0; padding: 0; background-color: #f9fafb;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
            <!-- Header -->
            <div style="background-color: #ffffff; border-bottom: 1px solid #e5e7eb; padding: 30px 30px;">
                <h1 style="font-size: 28px; font-weight: 700; margin: 0; color: #111827;">Daily Tech Brief</h1>
                <p style="font-size: 16px; color: #6b7280; margin: 10px 0 0 0;">{formatted_date}</p>
            </div>

            <!-- Content -->
            <div style="padding: 30px;">
                {stories_html}
            </div>

            <!-- Footer -->
            <div style="background-color: #f9fafb; padding: 20px 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                <p style="font-size: 12px; color: #6b7280; margin: 0;">
                    Daily Tech Brief • Curated with AI • Powered by Gemini
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def send_email(to_email: str, digest: Dict) -> bool:
    """Send email via Resend"""
    try:
        html_content = generate_html_email(digest)
        formatted_date = date.today().strftime("%B %d, %Y")

        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "from": "Daily Tech Brief <onboarding@resend.dev>",
            "to": [to_email],
            "subject": f"Daily Tech Brief - {formatted_date}",
            "html": html_content
        }

        response = requests.post(RESEND_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"[OK] Email sent successfully to {to_email}")
            return True
        else:
            print(f"[ERROR] Failed to send email: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"[ERROR] Error sending email: {e}")
        return False


def main():
    """Main email sending workflow"""
    print("=" * 60)
    print("Daily Tech Brief - Email Delivery")
    print("=" * 60)
    print()

    # Get today's digest
    print("Fetching today's digest...")
    digest = get_todays_digest()

    if not digest:
        print("[WARNING] No digest found for today. Exiting.")
        return

    print(f"   Found digest with {len(digest.get('stories', []))} stories")

    # Send email
    recipient = "chelseashin@gmail.com"
    print(f"\nSending email to {recipient}...")

    if send_email(recipient, digest):
        print(f"\n{'=' * 60}")
        print("Email delivery complete!")
        print(f"{'=' * 60}")
    else:
        print("\n[ERROR] Failed to send email")


if __name__ == "__main__":
    main()
