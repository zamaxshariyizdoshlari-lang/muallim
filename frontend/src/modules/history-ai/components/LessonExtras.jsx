import { Brain, CheckCircle2, Flag, Gauge, HelpCircle, Image as ImageIcon, MessageSquareQuote, PenLine, RotateCcw, Route, UserRound } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getLessonFeedback, sendLessonFeedback } from '../api/client'
import MiniCheck from './MiniCheck'

/** Mavzuning 2-5 ta asosiy fikri: o'qishdan oldin "katta rasm", oxirida xulosa sifatida. */
export function Takeaways({ items, title = 'Mavzuning asosiy fikrlari', closing = false }) {
  if (!items?.length) return null
  return (
    <section className={`card p-5 sm:p-6 ${closing ? '' : 'border-brand/30 bg-brand-soft/40'}`}>
      <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <Flag size={18} className="text-brand" /> {title}
      </h3>
      <ol className="flex flex-col gap-2.5">
        {items.map((t, i) => (
          <li key={i} className="flex gap-3 text-[0.95rem] leading-relaxed text-ink-2">
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand text-xs font-bold text-white">
              {i + 1}
            </span>
            <span className="pt-0.5">{t}</span>
          </li>
        ))}
      </ol>
    </section>
  )
}

/** "Eslab qol": sanalar, ketma-ketliklar uchun qisqa eslab qolish usullari. */
export function Mnemonics({ items }) {
  if (!items?.length) return null
  return (
    <section>
      <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <Brain size={18} className="text-gold" /> Eslab qolish usuli
      </h3>
      <ul className="grid gap-3 sm:grid-cols-2">
        {items.map((m, i) => (
          <li key={i} className="card border-l-4 !border-l-brand p-4 text-sm leading-relaxed text-ink-2">
            <p className="mb-1 font-semibold text-ink">{m.title}</p>
            {m.text}
          </li>
        ))}
      </ul>
    </section>
  )
}

/** "Kim kim?": tarixiy shaxslar kartochkalari (nomi, yillari, vazifasi, asosiy ishlari). */
export function PersonCards({ persons }) {
  if (!persons?.length) return null
  return (
    <section>
      <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <UserRound size={18} className="text-brand" /> Kim kim?
      </h3>
      <ul className="grid gap-3 sm:grid-cols-2">
        {persons.map((p, i) => (
          <li key={i} className="card p-4">
            <p className="font-display text-base font-bold text-ink">{p.name}</p>
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">
              {[p.years, p.role].filter(Boolean).join(' · ')}
            </p>
            <ul className="flex flex-col gap-1.5">
              {p.facts.map((f, j) => (
                <li key={j} className="flex gap-2 text-sm leading-relaxed text-ink-2">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-gold" /> {f}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </section>
  )
}

/**
 * Tasniflash o'yini: elementni tanlab, keyin toifani bosing (sichqoncha va telefonda bir xil ishlaydi).
 * Tekshirilganda noto'g'ri joylashganlari qizil bo'ladi va qayta urinish mumkin.
 */
export function ClassifyGame({ game }) {
  const [placed, setPlaced] = useState({})  // {itemIndex: categoryIndex}
  const [selected, setSelected] = useState(null)
  const [checked, setChecked] = useState(false)
  if (!game?.items?.length || !game.categories?.length) return null

  const unplaced = game.items.map((_, i) => i).filter((i) => placed[i] === undefined)
  const wrong = checked ? game.items.map((_, i) => i).filter((i) => placed[i] !== undefined && placed[i] !== game.items[i].category) : []
  const allCorrect = checked && unplaced.length === 0 && wrong.length === 0

  function place(cat) {
    if (selected === null) return
    setPlaced((p) => ({ ...p, [selected]: cat }))
    setSelected(null)
    setChecked(false)
  }

  function unplace(i) {
    if (allCorrect) return
    setPlaced((p) => { const { [i]: _drop, ...rest } = p; return rest })
    setChecked(false)
  }

  function reset() {
    setPlaced({})
    setSelected(null)
    setChecked(false)
  }

  return (
    <section className="card p-5 sm:p-6">
      <h3 className="mb-1 flex items-center gap-2 font-display text-lg font-bold text-ink">
        <CheckCircle2 size={18} className="text-brand" /> {game.title || 'Tasniflang'}
      </h3>
      <p className="mb-4 text-sm text-muted">{game.instruction || "Elementni tanlang, so'ng u tegishli bo'lgan toifani bosing."}</p>

      {unplaced.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2" aria-label="Joylashtirilmagan elementlar">
          {unplaced.map((i) => (
            <button
              key={i}
              type="button"
              onClick={() => setSelected(selected === i ? null : i)}
              aria-pressed={selected === i}
              className={`option !w-auto !py-2 text-sm ${selected === i ? 'is-selected' : ''}`}
            >
              {game.items[i].text}
            </button>
          ))}
        </div>
      )}

      <div className={`grid gap-3 ${game.categories.length > 2 ? 'sm:grid-cols-3' : 'sm:grid-cols-2'}`}>
        {game.categories.map((c, ci) => (
          <div
            key={ci}
            role="group"
            aria-label={c}
            className={`rounded-xl border p-3 ${selected !== null ? 'border-brand/60 bg-brand-soft/30' : 'border-line bg-surface-2'}`}
          >
            <button
              type="button"
              disabled={selected === null}
              onClick={() => place(ci)}
              className="mb-2 w-full text-left font-display text-sm font-bold text-brand disabled:cursor-default"
            >
              {c}{selected !== null && <span className="ml-2 text-xs font-normal text-muted">(shu yerga qo'yish)</span>}
            </button>
            <ul className="flex flex-col gap-1.5">
              {game.items.map((it, i) => placed[i] === ci && (
                <li key={i}>
                  <button
                    type="button"
                    onClick={() => unplace(i)}
                    className={`w-full rounded-lg border px-2.5 py-1.5 text-left text-sm ${
                      checked ? (it.category === ci ? 'border-ok bg-ok-soft text-ink' : 'border-bad bg-bad-soft text-ink') : 'border-line bg-surface text-ink-2'
                    }`}
                  >
                    {it.text}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <button type="button" onClick={() => setChecked(true)} disabled={unplaced.length > 0 || allCorrect} className="btn btn-primary btn-sm">
          Tekshirish
        </button>
        <button type="button" onClick={reset} className="btn btn-ghost btn-sm"><RotateCcw size={13} /> Boshidan</button>
        {checked && (
          <p role="status" className={`text-sm font-semibold ${allCorrect ? 'text-ok' : 'text-bad'}`}>
            {allCorrect ? "Ajoyib! Hammasi to'g'ri." : `${wrong.length} ta xato. Qizil elementni bosib olib tashlang va qayta joylashtiring.`}
          </p>
        )}
      </div>
    </section>
  )
}

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
