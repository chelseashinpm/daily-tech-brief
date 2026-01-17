import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export interface Story {
  id: string
  title: string
  url: string
  source: string
  source_domain: string
  summary: string
  topics: string[]
  trust_score: number
  relevance_score: number
  published_at: string
  created_at: string
}

export interface DailyDigest {
  id: string
  digest_date: string
  story_ids: string[]
  status: string
  created_at: string
  stories?: Story[]
}

export async function getTodaysDigest(): Promise<DailyDigest | null> {
  const today = new Date().toISOString().split('T')[0]

  const { data: digest, error } = await supabase
    .from('daily_digests')
    .select('*')
    .eq('digest_date', today)
    .single()

  if (error || !digest) {
    return null
  }

  // Fetch stories
  const { data: stories } = await supabase
    .from('stories')
    .select('*')
    .in('id', digest.story_ids)

  // Sort stories by the order in story_ids
  const sortedStories = digest.story_ids
    .map((id: string) => stories?.find((s: Story) => s.id === id))
    .filter(Boolean) as Story[]

  return {
    ...digest,
    stories: sortedStories,
  }
}

export async function getRecentDigests(limit: number = 7): Promise<DailyDigest[]> {
  const { data, error } = await supabase
    .from('daily_digests')
    .select('*')
    .order('digest_date', { ascending: false })
    .limit(limit)

  if (error || !data) {
    return []
  }

  return data
}
