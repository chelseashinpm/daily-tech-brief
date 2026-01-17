export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900">
              Daily Tech Brief
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Curated tech news for founders and product people
            </p>
          </div>
          <div className="text-sm text-gray-500">
            Updated daily at 8 AM UTC
          </div>
        </div>
      </div>
    </header>
  )
}
