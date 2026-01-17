-- Daily Tech Brief - Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Stories table: stores all processed articles
CREATE TABLE stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source VARCHAR(255) NOT NULL,
    source_domain VARCHAR(255),
    raw_content TEXT,
    summary TEXT,
    topics TEXT[],
    trust_score FLOAT DEFAULT 0.0,
    relevance_score FLOAT DEFAULT 0.0,
    published_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_stories_published_at ON stories(published_at DESC);
CREATE INDEX idx_stories_status ON stories(status);
CREATE INDEX idx_stories_relevance ON stories(relevance_score DESC);
CREATE INDEX idx_stories_url ON stories(url);

-- Daily digests table: stores curated daily selections
CREATE TABLE daily_digests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    digest_date DATE UNIQUE NOT NULL,
    story_ids UUID[] NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for date lookups
CREATE INDEX idx_daily_digests_date ON daily_digests(digest_date DESC);

-- Function to get today's digest with stories
CREATE OR REPLACE FUNCTION get_todays_digest()
RETURNS JSON AS $$
DECLARE
    digest_record RECORD;
    stories_json JSON;
BEGIN
    -- Get today's digest
    SELECT * INTO digest_record
    FROM daily_digests
    WHERE digest_date = CURRENT_DATE;

    -- If no digest found, return null
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    -- Get stories for this digest
    SELECT json_agg(s.*)
    INTO stories_json
    FROM stories s
    WHERE s.id = ANY(digest_record.story_ids);

    -- Return combined result
    RETURN json_build_object(
        'digest_date', digest_record.digest_date,
        'status', digest_record.status,
        'stories', stories_json
    );
END;
$$ LANGUAGE plpgsql;

-- Optional: Function to clean up old stories (keep last 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_stories()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM stories
    WHERE created_at < NOW() - INTERVAL '30 days'
    AND status != 'published';

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE stories IS 'Stores all fetched and processed articles';
COMMENT ON TABLE daily_digests IS 'Stores daily curated digest selections';
COMMENT ON COLUMN stories.topics IS 'Array of topic tags for categorization';
COMMENT ON COLUMN stories.relevance_score IS 'AI-generated relevance score (0.0-1.0)';
COMMENT ON COLUMN stories.trust_score IS 'Source credibility score (0.0-1.0)';
