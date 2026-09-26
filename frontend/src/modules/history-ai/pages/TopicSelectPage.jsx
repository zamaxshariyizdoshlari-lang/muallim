import { Award, BookOpen, CheckCircle2, ChevronLeft, ClipboardCheck, Lock } from 'lucide-react'

export default function TopicSelectPage({ book, topics, isTeacher, progress, onSelect, onBack, onOpenExam, onDownloadCertificate }) {
  const completedCount = topics.filter((t) => t.completed).length

  return (
    <div className="mx-auto max-w-xl">
      <button onClick={onBack} className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700">
        <ChevronLeft size={16} /> Darsliklar ro'yxati
      </button>

      <h1 className="mb-1 text-2xl font-semibold text-slate-900">Mavzu tanlang</h1>
      <p className="mb-6 text-sm text-slate-500">
        "{book.title}" kitobidan {topics.length} ta mavzu aniqlandi.
        {!isTeacher && ` O'tildi: ${completedCount} / ${topics.length}.`}
      </p>

      <div className="flex flex-col gap-2">
        {topics.map((topic) => {
          const locked = !topic.unlocked
          return (
            <button
              key={topic.id}
              onClick={() => onSelect(topic)}
              disabled={locked}
              title={locked ? "Avval oldingi mavzu testini 100% topshiring" : undefined}
              className={`flex items-center justify-between rounded-lg border px-4 py-3 text-left shadow-sm ${
                locked
                  ? 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
                  : 'border-slate-200 bg-white hover:border-indigo-400 hover:bg-indigo-50'
              }`}
            >
              <span className="flex items-center gap-3">
                {locked ? <Lock size={18} /> : topic.completed ? <CheckCircle2 className="text-green-600" size={18} /> : <BookOpen className="text-indigo-500" size={18} />}
                <span className="text-sm font-medium">{topic.title}</span>
              </span>
              <span className="text-xs text-slate-400">
                {topic.start_page === topic.end_page ? `bet ${topic.start_page}` : `bet ${topic.start_page}-${topic.end_page}`}
              </span>
            </button>
          )
        })}
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-1 flex items-center gap-2 text-sm font-semibold text-slate-900">
          <ClipboardCheck size={16} /> Kitob yakuniy imtihoni
        </h2>
        {isTeacher ? (
          <button onClick={onOpenExam} className="mt-2 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
            Yakuniy imtihonni ko'rish / yaratish
          </button>
        ) : progress?.all_topics_completed ? (
          <button onClick={onOpenExam} className="mt-2 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700">
            Yakuniy imtihonni topshirish
          </button>
        ) : (
          <p className="text-xs text-slate-500">Barcha mavzu testlarini topshirgach ochiladi.</p>
        )}

        {progress?.certificate && (
          <button onClick={onDownloadCertificate} className="mt-3 flex items-center gap-2 rounded-lg bg-green-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-green-700">
            <Award size={16} /> Sertifikatni yuklab olish (PDF)
          </button>
        )}
      </div>
    </div>
  )
}
