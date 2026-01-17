import type { Story } from '@/lib/supabase'

interface StoryCardProps {
  story: Story
  index: number
}

const topicColors: Record<string, string> = {
  'Big Tech & Product Strategy': 'bg-blue-100 text-blue-800',
  'Startups & Ecosystem': 'bg-green-100 text-green-800',
  'Government Regulation & Policy': 'bg-purple-100 text-purple-800',
  'AI Security, Safety, and Privacy': 'bg-orange-100 text-orange-800',
}

export default function StoryCard({ story, index }: StoryCardProps) {
  return (
    <article className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
      {/* Story Number */}
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-sm">
            {index}
          </div>
        </div>

        <div className="flex-1">
          {/* Topics */}
          <div className="flex flex-wrap gap-2 mb-3">
            {story.topics.map((topic) => (
              <span
                key={topic}
                className={`px-2 py-1 rounded-full text-xs font-medium ${
                  topicColors[topic] || 'bg-gray-100 text-gray-800'
                }`}
              >
                {topic}
              </span>
            ))}
          </div>

          {/* Title */}
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            <a
              href={story.url}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-600 transition-colors"
            >
              {story.title}
            </a>
          </h2>

          {/* Source */}
          <p className="text-sm text-gray-500 mb-3">{story.source}</p>

          {/* Summary */}
          <p className="text-gray-700 leading-relaxed mb-4">{story.summary}</p>

          {/* Read More Link */}
          <a
            href={story.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium text-sm"
          >
            Read full article
            <svg
              className="w-4 h-4 ml-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </a>
        </div>
      </div>
    </article>
  )
}
