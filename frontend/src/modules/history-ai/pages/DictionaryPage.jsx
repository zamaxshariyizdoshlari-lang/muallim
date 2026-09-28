import { Loader2, Search, Volume2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getBookDictionary } from '../api/client'
import { BackLink, ErrorNote, SectionTitle } from '../components/ui'
import { isSpeechSupported, speak } from '../utils/speech'

/** Kurs bo'yicha to'plangan lug'at: barcha ochilgan mavzulardagi so'zlar, qidirish bilan.
 * Foydalanuvchi oldingi darslarning so'zlarini alohida Lesson'ni qayta ochmasdan topadi. */
export default function DictionaryPage({ bookId, onBack, onOpenTopic }) {
  const [q, setQ] = useState('')
  const [items, setItems] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    const timer = setTimeout(() => {
      getBookDictionary(bookId, q.trim())
        .then((d) => setItems(d.items))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false))
    }, 250)
    return () => clearTimeout(timer)
  }, [bookId, q])

  return (
    <div className="rise mx-auto max-w-2xl">
      <BackLink onClick={onBack}>Orqaga</BackLink>
      <SectionTitle eyebrow="Lug'at">Kurs lug'ati</SectionTitle>
      <p className="-mt-2 mb-6 text-sm text-muted">
        Hozirgacha o'qigan darslaringizdagi barcha so'zlar - bitta joydan qidiring va takrorlang.
      </p>

      <div className="relative mb-6">
        <Search size={16} className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
        <input
          className="field !pl-10"
          placeholder="So'z qidirish (turkcha yoki o'zbekcha)"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </div>

      <ErrorNote>{error}</ErrorNote>

      {loading && !items ? (
        <Loader2 className="animate-spin text-gold" size={22} />
      ) : !items?.length ? (
        <p className="card p-6 text-sm text-muted">
          {q.trim() ? 'Hech narsa topilmadi.' : "Hali so'z yo'q - darslarni o'qigan sari bu yerda to'planadi."}
        </p>
      ) : (
        <ol className="flex flex-col gap-2">
          {items.map((w, i) => (
            <li key={i} className="card p-4 sm:p-5">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <p className="flex items-center gap-2 font-display text-lg font-bold text-ink">
                    {w.tr}
                    {isSpeechSupported() && (
                      <button
                        type="button"
                        onClick={() => speak(w.tr)}
                        className="text-muted hover:text-brand"
                        aria-label="Tinglash"
                      >
                        <Volume2 size={16} />
                      </button>
                    )}
                  </p>
                  <p className="mt-0.5 text-sm text-ink-2">{w.uz}</p>
                  {w.example_tr && (
                    <p className="mt-2 text-sm italic leading-relaxed text-muted">
                      {w.example_tr}
                      {w.example_uz && <span className="not-italic"> — {w.example_uz}</span>}
                    </p>
                  )}
                </div>
                <button
                  type="button"
                  onClick={() => onOpenTopic(w.topic_id)}
                  className="chip shrink-0 hover:!border-brand/40 hover:!bg-brand-soft hover:!text-brand"
                  title="Shu so'z o'rgatilgan darsga o'tish"
                >
                  {w.topic_title}
                </button>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
