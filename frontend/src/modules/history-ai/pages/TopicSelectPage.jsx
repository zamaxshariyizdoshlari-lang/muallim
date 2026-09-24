import { BookOpen, ChevronLeft } from 'lucide-react'

export default function TopicSelectPage({ book, topics, onSelect, onBack }) {
  return (
    <div className="mx-auto max-w-xl">
      <button
        onClick={onBack}
        className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700"
      >
        <ChevronLeft size={16} /> Boshqa kitob yuklash
      </button>

      <h1 className="mb-1 text-2xl font-semibold text-slate-900">Mavzu tanlang</h1>
      <p className="mb-6 text-sm text-slate-500">
        "{book.title}" kitobidan {topics.length} ta mavzu aniqlandi.
      </p>

      <div className="flex flex-col gap-2">
        {topics.map((topic) => (
          <button
            key={topic.id}
            onClick={() => onSelect(topic)}
            className="flex items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-3 text-left shadow-sm hover:border-indigo-400 hover:bg-indigo-50"
          >
            <span className="flex items-center gap-3">
              <BookOpen className="text-indigo-500" size={18} />
              <span className="text-sm font-medium text-slate-800">{topic.title}</span>
            </span>
            <span className="text-xs text-slate-400">
              {topic.start_page === topic.end_page
                ? `bet ${topic.start_page}`
                : `bet ${topic.start_page}-${topic.end_page}`}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
