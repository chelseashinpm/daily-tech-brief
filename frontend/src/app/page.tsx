import { getTodaysDigest } from '@/lib/supabase'
import StoryCard from '@/components/StoryCard'
import Header from '@/components/Header'

export const revalidate = 300 // Revalidate every 5 minutes

export default async function Home() {
  const digest = await getTodaysDigest()

  if (!digest || !digest.stories || digest.stories.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              No digest available yet
            </h2>
            <p className="text-gray-600">
              Check back later for today's tech brief!
            </p>
          </div>
        </main>
      </div>
    )
  }

  const formattedDate = new Date(digest.digest_date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-4xl mx-auto px-4 py-12">
        {/* Date Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Daily Tech Brief
          </h1>
          <p className="text-lg text-gray-600">{formattedDate}</p>
        </div>

        {/* Stories */}
        <div className="space-y-6">
          {digest.stories.map((story, index) => (
            <StoryCard key={story.id} story={story} index={index + 1} />
          ))}
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>
            Daily Tech Brief • Curated with AI • Sources from trusted tech publications
          </p>
        </footer>
      </main>
    </div>
  )
}
