import { AlertTriangle, CheckCircle2, ChevronDown, Circle, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getAdminBookQuality, getBookAnalytics } from '../../api/client'
import { ErrorNote, Spinner } from '../../components/ui'

/** Kurs sifati: har mavzuning to'liqlik ro'yxati, talabalarning o'zini baholashi va shubhali savollar. */
export default function AdminQualityPanel({ bookId, onOpenTopic }) {
  const [rows, setRows] = useState(null)
  const [hard, setHard] = useState([])
  const [error, setError] = useState('')
  const [open, setOpen] = useState({})

  useEffect(() => {
    let cancelled = false
    Promise.all([getAdminBookQuality(bookId), getBookAnalytics(bookId)])
      .then(([q, a]) => {
        if (cancelled) return
        setRows(q)
        setHard(a.hard_questions || [])
      })
      .catch((err) => !cancelled && setError(err.message))
    return () => { cancelled = true }
  }, [bookId])

  if (error) return <ErrorNote>{error}</ErrorNote>
  if (!rows) return <Spinner>Yuklanmoqda...</Spinner>

  const incomplete = rows.filter((r) => r.required_ok < r.required_total).length
  const suspicious = hard.filter((h) => h.suspicious)

  return (
    <div className="flex flex-col gap-5">
      <div className="card flex flex-wrap items-center gap-x-6 gap-y-2 p-5">
        <p className="text-sm text-ink-2">
          <b className="text-ink">{rows.length}</b> ta mavzu ·{' '}
          <b className={incomplete ? 'text-bad' : 'text-ok'}>{incomplete}</b> tasida asosiy qismlar yetishmaydi
        </p>
      </div>

      {suspicious.length > 0 && (
        <section className="card border-bad/40 p-5">
          <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-bad">
            <AlertTriangle size={18} /> Qayta ko'rib chiqiladigan savollar
          </h3>
          <p className="mb-3 text-sm text-ink-2">
            Deyarli hamma talaba adashgan savollar: ehtimol savol yoki variantlar noaniq yozilgan.
          </p>
          <ul className="flex flex-col gap-2">
            {suspicious.map((h, i) => (
              <li key={i} className="rounded-lg bg-bad-soft px-3 py-2 text-sm text-ink">
                {h.question}
                <span className="ml-2 text-xs text-muted">
                  {h.topic_title && `${h.topic_title} · `}{h.error_rate}% xato ({h.wrong}/{h.seen})
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <ul className="flex flex-col gap-2">
        {rows.map((r) => {
          const ok = r.required_ok === r.required_total
          return (
            <li key={r.topic_id} className="card p-4">
              <button
                onClick={() => setOpen((o) => ({ ...o, [r.topic_id]: !o[r.topic_id] }))}
                className="flex w-full items-center gap-3 text-left"
                aria-expanded={Boolean(open[r.topic_id])}
              >
                {ok ? <CheckCircle2 size={18} className="shrink-0 text-ok" /> : <AlertTriangle size={18} className="shrink-0 text-gold" />}
                <span className="min-w-0 flex-1 text-sm font-semibold text-ink">{r.title}</span>
                {r.feedback && (
                  <span
                    className={`chip ${r.feedback.hard_percent >= 40 ? '!border-bad/40 !bg-bad-soft !text-bad' : ''}`}
                    title={`${r.feedback.count} ta baho, o'rtacha ${r.feedback.avg}/3`}
                  >
                    {r.feedback.hard_percent}% "qiyin"
                  </span>
                )}
                <span className="chip">{r.required_ok}/{r.required_total}</span>
                {r.bonus_total > 0 && (
                  <span className="chip chip-gold" title="Boyituvchi qismlar">
                    <Sparkles size={11} /> {r.bonus_ok}/{r.bonus_total}
                  </span>
                )}
                <ChevronDown size={16} className={`shrink-0 text-muted transition ${open[r.topic_id] ? 'rotate-180' : ''}`} />
              </button>
              {open[r.topic_id] && (
                <div className="rise mt-3 border-t border-line pt-3">
                  <ul className="grid gap-1.5 sm:grid-cols-2">
                    {r.checks.map((c) => (
                      <li key={c.key} className={`flex items-start gap-2 text-sm ${c.ok ? 'text-ink-2' : c.required ? 'text-bad' : 'text-muted'}`}>
                        {c.ok ? <CheckCircle2 size={15} className="mt-0.5 shrink-0 text-ok" /> : <Circle size={15} className="mt-0.5 shrink-0" />}
                        {c.label}{!c.required && !c.ok && ' (ixtiyoriy)'}
                      </li>
                    ))}
                  </ul>
                  <button onClick={() => onOpenTopic(r.topic_id)} className="btn btn-ghost btn-sm mt-3">Tahrirlash</button>
                </div>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}
