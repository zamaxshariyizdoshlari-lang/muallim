import { Loader2, Search, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { searchBook } from '../api/client'

/** Kurs ichida qidiruv: mavzu sarlavhasi, tushuntirish matni va muhim faktlar bo'yicha. */
export default function SearchBox({ bookId, onOpenTopic }) {
  const [q, setQ] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const term = q.trim()
    if (term.length < 2) return undefined
    const timer = setTimeout(async () => {
      setLoading(true)
      try {
        setResults((await searchBook(bookId, term)).results)
      } catch {
        setResults([])
      } finally {
        setLoading(false)
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [q, bookId])

  const active = q.trim().length >= 2

  return (
    <div className="relative">
      <div className="relative">
        <Search size={16} className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
        <input
          className="field !pl-10 !pr-10"
          placeholder="Kursdan qidirish: masalan, piramida"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          aria-label="Kursdan qidirish"
        />
        {q && (
          <button
            type="button"
            onClick={() => { setQ(''); setResults(null) }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-ink"
            aria-label="Tozalash"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <X size={16} />}
          </button>
        )}
      </div>

      {active && results && (
        <ul className="card absolute left-0 right-0 z-20 mt-2 max-h-96 overflow-auto p-2">
          {results.length === 0 && (
            <li className="px-3 py-3 text-sm text-muted">
              Hech narsa topilmadi. (Faqat ochilgan mavzular ichidan qidiriladi.)
            </li>
          )}
          {results.map((r, i) => (
            <li key={i}>
              <button
                type="button"
                onClick={() => onOpenTopic(r.topic_id)}
                className="block w-full rounded-xl px-3 py-2.5 text-left transition-colors hover:bg-surface-2"
              >
                <span className="flex items-center justify-between gap-2">
                  <span className="text-sm font-semibold text-ink">{r.topic_title}</span>
                  {r.page && <span className="chip shrink-0">bet {r.page}</span>}
                </span>
                <span className="mt-0.5 block text-xs leading-relaxed text-muted">{r.snippet}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
