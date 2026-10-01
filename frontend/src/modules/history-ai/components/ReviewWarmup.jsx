import { RotateCw } from 'lucide-react'
import { useEffect, useState } from 'react'
import { answerReview, getReview } from '../api/client'

const WARMUP_SIZE = 2

/**
 * Yangi mavzu boshida eski xatolardan 2 ta savol (oraliq takrorlash tizimidan): yangi bilim
 * eskisining ustiga quriladi. To'g'ri javob takrorlash kartochkasini ilgarilatadi (+ball).
 * Takrorlash kerak bo'lgan savol bo'lmasa, hech narsa ko'rsatilmaydi.
 */
export default function ReviewWarmup({ bookId }) {
  const [items, setItems] = useState([])
  const [index, setIndex] = useState(0)
  const [answered, setAnswered] = useState(false)

  useEffect(() => {
    if (!bookId) return
    let cancelled = false
    getReview(bookId).then((d) => !cancelled && setItems(d.items.slice(0, WARMUP_SIZE))).catch(() => {})
    return () => { cancelled = true }
  }, [bookId])

  if (!items.length || index >= items.length) return null
  const q = items[index]

  return (
    <section className="card border-gold/40 bg-gold-soft/30 p-5 sm:p-6" aria-label="Eski mavzuni eslash">
      <p className="eyebrow mb-3 flex items-center gap-2">
        <RotateCw size={14} /> Avval o'tganlarni eslang ({index + 1} / {items.length})
      </p>
      <ServerCheck key={q.key} bookId={bookId} item={q} onDone={() => setAnswered(true)} />
      {answered && (
        <button onClick={() => { setAnswered(false); setIndex((i) => i + 1) }} className="btn btn-primary btn-sm mt-4">
          {index + 1 === items.length ? 'Tayyor' : 'Keyingisi'}
        </button>
      )}
    </section>
  )
}

// To'g'ri javobni server bermaydi: javob serverga yuboriladi va natija (to'g'ri/xato) qaytadi.
function ServerCheck({ bookId, item, onDone }) {
  const [result, setResult] = useState(null)
  const [choice, setChoice] = useState(null)

  async function pick(i) {
    if (choice !== null) return
    setChoice(i)
    try {
      setResult(await answerReview(bookId, item.key, i))
    } catch {
      setResult({ correct: false, page: item.page })
    }
    onDone()
  }

  return (
    <div>
      <p className="mb-3 font-read text-base font-medium leading-snug text-ink">{item.question}</p>
      <div className="flex flex-col gap-2">
        {item.options.map((opt, i) => (
          <button
            key={i}
            type="button"
            disabled={choice !== null}
            onClick={() => pick(i)}
            className={`option ${choice === i ? (result ? (result.correct ? 'is-ok' : 'is-bad shake') : 'is-selected') : ''}`}
          >
            <span className="option-key">{String.fromCharCode(65 + i)}</span>
            <span className="pt-0.5">{opt}</span>
          </button>
        ))}
      </div>
      {result && (
        <p role="status" className={`rise mt-3 text-sm font-semibold ${result.correct ? 'text-ok' : 'text-bad'}`}>
          {result.correct
            ? `To'g'ri!${result.xp_gained ? ` +${result.xp_gained} ball` : ''}`
            : `Hali emas.${result.page ? ` Darslikning ${result.page}-betini qayta o'qing.` : ''}`}
        </p>
      )}
    </div>
  )
}
