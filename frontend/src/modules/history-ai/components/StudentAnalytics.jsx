import { TrendingUp } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getStudentAnalytics } from '../api/client'

/** Talabaning shaxsiy tahlili: zaif mavzular, imtihon dinamikasi, taxminiy daraja. */
export default function StudentAnalytics({ bookId, onOpenTopic }) {
  const [data, setData] = useState(null)
  useEffect(() => {
    getStudentAnalytics(bookId).then(setData).catch(() => {})
  }, [bookId])
  if (!data || (!data.topics.length && !data.exams.length)) return null
  const max = 100
  return (
    <div className="card mt-6 px-5 py-5">
      <h2 className="font-display text-xl font-bold text-ink inline-flex items-center gap-2">
        <TrendingUp size={20} className="text-gold" /> Mening natijalarim
      </h2>
      {data.forecast !== null && (
        <p className="mt-2 text-sm text-ink-2">
          Taxminiy natija: <b>{data.forecast}%</b> (daraja <b>{data.forecast_level}</b>) — oxirgi imtihonlar o'rtachasi.
        </p>
      )}
      {data.exams.length > 0 && (
        <div className="mt-3 flex h-16 items-end gap-1" aria-label="Imtihon dinamikasi">
          {data.exams.slice(-12).map((e, i) => (
            <div key={i} title={`${e.date}: ${e.percent}%`} style={{ height: `${(e.percent / max) * 100}%` }}
              className={`w-4 rounded-t ${e.passed ? 'bg-ok' : 'bg-gold'}`} />
          ))}
        </div>
      )}
      {data.weak.length > 0 && (
        <div className="mt-4">
          <p className="eyebrow mb-2">Takrorlash kerak</p>
          <ul className="space-y-1 text-sm">
            {data.weak.map((t) => (
              <li key={t.topic_id}>
                <button onClick={() => onOpenTopic?.(t.topic_id)} className="text-left underline decoration-dotted">
                  {t.title}
                </button>
                <span className="ml-2 text-muted">{t.last}% (eng yaxshi {t.best}%)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {data.untouched.length > 0 && (
        <p className="mt-3 text-xs text-muted">Hali boshlanmagan mavzular: {data.untouched.length} ta.</p>
      )}
    </div>
  )
}
