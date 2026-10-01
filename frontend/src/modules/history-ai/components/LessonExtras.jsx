import { Gauge, HelpCircle, Image as ImageIcon, MessageSquareQuote, PenLine, Route } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getLessonFeedback, sendLessonFeedback } from '../api/client'
import MiniCheck from './MiniCheck'

/** "Nega?": sabab va oqibat. Tarixiy voqeani faktlar to'plami emas, zanjir sifatida ko'rsatadi. */
export function WhyCard({ why }) {
  if (!why || !(why.causes?.length || why.effects?.length)) return null
  return (
    <section className="card p-5 sm:p-6">
      <h3 className="mb-4 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <Route size={18} className="text-brand" /> Nega shunday bo'ldi?
      </h3>
      <div className="grid gap-4 sm:grid-cols-2">
        {[['causes', 'Sabablari', 'border-gold/50 bg-gold-soft/40'], ['effects', 'Natijalari', 'border-ok/40 bg-ok-soft/50']].map(
          ([key, title, tone]) =>
            why[key]?.length > 0 && (
              <div key={key} className={`rounded-xl border p-4 ${tone}`}>
                <p className="mb-2 text-sm font-bold uppercase tracking-wide text-ink-2">{title}</p>
                <ul className="flex flex-col gap-2">
                  {why[key].map((item, i) => (
                    <li key={i} className="text-sm leading-relaxed text-ink">{item}</li>
                  ))}
                </ul>
              </div>
            ),
        )}
      </div>
    </section>
  )
}

/** Manba bilan ishlash: qisqa hujjat/ta'rif va u haqida savol. */
export function SourceWork({ work }) {
  if (!work?.quote) return null
  return (
    <section className="card p-5 sm:p-6">
      <h3 className="mb-4 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <MessageSquareQuote size={18} className="text-brand" /> Manba bilan ishlang
      </h3>
      <blockquote className="mb-4 rounded-xl border-l-4 border-gold bg-surface-2 px-4 py-3 font-read text-base italic leading-relaxed text-ink">
        {work.quote}
        {work.attribution && <footer className="mt-2 text-sm not-italic text-muted">— {work.attribution}</footer>}
      </blockquote>
      <MiniCheck question={work} />
    </section>
  )
}

/** Xarita/rasm: src (masalan /maps/misr.svg), izoh va ixtiyoriy savol. */
export function ImageFigure({ image }) {
  if (!image?.src) return null
  return (
    <figure className="card overflow-hidden p-3 sm:p-4">
      <img src={image.src} alt={image.caption} loading="lazy" className="mx-auto max-h-96 w-auto rounded-lg" />
      <figcaption className="mt-3 flex items-center gap-2 text-sm text-muted">
        <ImageIcon size={14} className="shrink-0" /> {image.caption}
      </figcaption>
      {image.question && (
        <div className="mt-4 border-t border-line pt-4">
          <MiniCheck question={image.question} />
        </div>
      )}
    </figure>
  )
}

/** Blok tagidagi mini-savol: o'qigan joyini darrov tekshiradi. */
export function BlockCheck({ question }) {
  if (!question) return null
  return (
    <div className="mt-5 rounded-xl border border-brand/25 bg-brand-soft/40 p-4">
      <p className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-brand">
        <HelpCircle size={14} /> Tushundingizmi?
      </p>
      <MiniCheck question={question} />
    </div>
  )
}

/** Xulosa: avval talaba o'z so'zi bilan 1 gap yozadi (eslab qolishni kuchaytiradi), keyin namuna ochiladi. */
export function SelfSummary({ topicId, summary }) {
  const storageKey = `muallim_summary_${topicId}`
  const [text, setText] = useState(() => {
    try { return localStorage.getItem(storageKey) || '' } catch { return '' }
  })
  const [revealed, setRevealed] = useState(false)

  useEffect(() => {
    try { localStorage.setItem(storageKey, text) } catch { /* xotira yopiq - muhim emas */ }
  }, [storageKey, text])

  if (!summary) return null
  return (
    <div className="rounded-2xl border border-brand/30 bg-brand-soft p-5 sm:p-6">
      <h3 className="mb-2 font-display text-lg font-bold text-brand">Xulosa</h3>
      {!revealed ? (
        <>
          <label className="mb-2 flex items-center gap-2 text-sm font-medium text-ink-2" htmlFor={`summary-${topicId}`}>
            <PenLine size={14} /> Mavzuni 1-2 gap bilan o'z so'zingizda yozing:
          </label>
          <textarea
            id={`summary-${topicId}`}
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={3}
            className="field w-full"
            placeholder="Bu mavzuda eng muhimi..."
          />
          <button onClick={() => setRevealed(true)} className="btn btn-primary btn-sm mt-3">
            {text.trim() ? "Namunaviy xulosani ko'rish" : "O'tkazib, xulosani ko'rish"}
          </button>
        </>
      ) : (
        <>
          {text.trim() && (
            <p className="mb-3 rounded-xl bg-surface px-4 py-3 text-sm text-ink-2">
              <b className="text-ink">Sizning xulosangiz:</b> {text}
            </p>
          )}
          <p className="rise font-read text-base leading-relaxed text-ink">{summary}</p>
        </>
      )}
    </div>
  )
}

const RATINGS = [
  { value: 1, emoji: '😕', label: 'Qiyin edi' },
  { value: 2, emoji: '🙂', label: "O'rtacha" },
  { value: 3, emoji: '😀', label: 'Tushunarli' },
]

/** Dars oxirida o'zini baholash: o'qituvchi panelida qaysi mavzu qiyinligi shundan ko'rinadi. */
export function SelfRating({ topicId }) {
  const [rating, setRating] = useState(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    let cancelled = false
    getLessonFeedback(topicId).then((d) => !cancelled && setRating(d.rating)).catch(() => {})
    return () => { cancelled = true }
  }, [topicId])

  async function choose(value) {
    setRating(value)
    setError(false)
    try {
      await sendLessonFeedback(topicId, value)
    } catch {
      setError(true)
    }
  }

  return (
    <section className="card p-5 sm:p-6" aria-label="Darsni baholash">
      <h3 className="mb-1 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <Gauge size={18} className="text-brand" /> Bu dars sizga qanday bo'ldi?
      </h3>
      <p className="mb-4 text-sm text-muted">Javobingiz mavzuni yaxshilashga yordam beradi.</p>
      <div className="flex flex-wrap gap-2" role="radiogroup">
        {RATINGS.map((r) => (
          <button
            key={r.value}
            role="radio"
            aria-checked={rating === r.value}
            onClick={() => choose(r.value)}
            className={`btn btn-sm !rounded-full ${rating === r.value ? 'btn-primary' : 'btn-ghost'}`}
          >
            <span aria-hidden>{r.emoji}</span> {r.label}
          </button>
        ))}
      </div>
      {error && <p className="mt-2 text-xs text-bad">Saqlab bo'lmadi, keyinroq urinib ko'ring.</p>}
    </section>
  )
}
