"""
Trusted news sources for Daily Tech Brief
"""

TRUSTED_SOURCES = [
    # Big Tech & Product Strategy
    {
        "name": "TechCrunch",
        "domain": "techcrunch.com",
        "rss_url": "https://techcrunch.com/feed/",
        "trust_score": 0.9,
    },
    {
        "name": "The Verge",
        "domain": "theverge.com",
        "rss_url": "https://www.theverge.com/rss/index.xml",
        "trust_score": 0.9,
    },
    {
        "name": "Ars Technica",
        "domain": "arstechnica.com",
        "rss_url": "https://feeds.arstechnica.com/arstechnica/index",
        "trust_score": 0.95,
    },
    {
        "name": "Hacker News",
        "domain": "news.ycombinator.com",
        "rss_url": "https://hnrss.org/frontpage",
        "trust_score": 0.85,
    },

    # Startups & Ecosystem
    {
        "name": "Y Combinator",
        "domain": "ycombinator.com",
        "rss_url": "https://www.ycombinator.com/blog/feed",
        "trust_score": 0.95,
    },

    # AI & Research
    {
        "name": "OpenAI Blog",
        "domain": "openai.com",
        "rss_url": "https://openai.com/blog/rss.xml",
        "trust_score": 1.0,
    },
    {
        "name": "Anthropic",
        "domain": "anthropic.com",
        "rss_url": "https://www.anthropic.com/news/rss.xml",
        "trust_score": 1.0,
    },
    {
        "name": "Google AI Blog",
        "domain": "ai.googleblog.com",
        "rss_url": "http://ai.googleblog.com/feeds/posts/default",
        "trust_score": 0.95,
    },

    # Regulation & Policy
    {
        "name": "FTC Tech Blog",
        "domain": "ftc.gov",
        "rss_url": "https://www.ftc.gov/news-events/news/rss",
        "trust_score": 1.0,
    },
]

# Keywords for filtering relevant content
RELEVANT_KEYWORDS = [
    # Big Tech
    "google", "apple", "microsoft", "amazon", "meta", "facebook",
    "netflix", "tesla", "twitter", "x.com", "spacex",

    # AI & ML
    "ai", "artificial intelligence", "machine learning", "gpt", "llm",
    "chatgpt", "claude", "gemini", "chatbot", "neural network",
    "deep learning", "generative", "openai", "anthropic",

    # Product & Strategy
    "product", "launch", "announce", "release", "feature",
    "partnership", "acquisition", "merger", "funding",

    # Regulation
    "regulation", "policy", "ftc", "sec", "antitrust",
    "privacy", "gdpr", "compliance", "lawsuit", "senate",

    # Startups
    "startup", "venture", "series a", "series b", "ipo",
    "founder", "vc", "y combinator",

    # Security & Safety
    "security", "breach", "vulnerability", "hack", "safety",
    "encryption", "authentication", "cybersecurity",
]

# Topics for classification
TOPICS = [
    "Big Tech & Product Strategy",
    "Startups & Ecosystem",
    "Government Regulation & Policy",
    "AI Security, Safety, and Privacy",
]
