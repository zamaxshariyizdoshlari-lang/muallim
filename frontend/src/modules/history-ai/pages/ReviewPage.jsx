import { CheckCircle2, RotateCcw, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { answerReview, getReview } from '../api/client'
import { BackLink, ErrorNote, ProgressBar, Spinner } from '../components/ui'

/**
 * Xatolarni takrorlash: oxirgi marta xato qilingan savollar. To'g'ri javob ko'rsatilmaydi -
 * faqat to'g'ri/xato va qaysi betni qayta o'qish kerakligi (rasmiy testdagi kabi).
 * To'g'ri javob berilgan savol ro'yxatdan chiqadi va +5 XP beradi.
 */
export default function ReviewPage({ bookId, onBack, onOpenTopic }) {
  const [items, setItems] = useState(null)
  const [total, setTotal] = useState(0)
  const [index, setIndex] = useState(0)
  const [feedback, setFeedback] = useState(null) // { choice, correct, page, xp }
  const [mastered, setMastered] = useState(0)
  const [error, setError] = useState('')

  useEffect(() => {
    window.scrollTo({ top: 0 })
    getReview(bookId)
      .then((d) => { setItems(d.items); setTotal(d.items.length) })
      .catch((err) => setError(err.message))
  }, [bookId])

  if (error) return <ErrorNote>{error}</ErrorNote>
  if (!items) return <Spinner>Yuklanmoqda...</Spinner>

  const done = index >= items.length
  const q = items[index]

  async function pick(choice) {
    if (feedback) return
    try {
      const r = await answerReview(bookId, q.key, choice)
      setFeedback({ choice, correct: r.correct, page: r.page, xp: r.xp_gained })
      if (r.correct) setMastered((m) => m + 1)
    } catch (err) {
      setError(err.message)
    }
  }

  function next() {
    setFeedback(null)
    setIndex((i) => i + 1)
  }

  function again() {
    setFeedback(null)
    setIndex(0)
    setMastered(0)
    setItems(null)
    getReview(bookId).then((d) => { setItems(d.items); setTotal(d.items.length) })
  }

  return (
    <div className="rise mx-auto max-w-2xl">
      <BackLink onClick={onBack}>Kursga qaytish</BackLink>
      <header className="mb-8">
        <p className="eyebrow mb-2">Takrorlash</p>
        <h1 className="font-display text-3xl font-extrabold text-ink sm:text-4xl">Xatolar ustida ishlash</h1>
        <p className="mt-3 text-sm text-muted">
          Testlarda xato qilgan savollaringiz. To'g'ri javob bergan savol ro'yxatdan chiqadi (+5 XP).
        </p>
      </header>

      {total === 0 && (
        <div className="card p-8 text-center">
          <Sparkles className="mx-auto mb-3 text-gold" size={32} />
          <p className="font-display text-xl font-bold text-ink">Takrorlaydigan xato yo'q!</p>
          <p className="mt-1 text-sm text-muted">Testlarda xato qilsangiz, savollar shu yerga tushadi.</p>
        </div>
      )}

      {total > 0 && !done && (
        <div className="card p-5 sm:p-7">
          <div className="mb-5 flex items-center gap-3">
            <span className="chip">{index + 1} / {items.length}</span>
            <ProgressBar value={index} max={items.length} />
          </div>
          <p className="mb-5 font-read text-xl font-medium leading-snug text-ink">{q.question}</p>
          <div className="flex flex-col gap-2">
            {q.options.map((opt, j) => {
              const picked = feedback?.choice === j
              return (
                <button
                  key={j}
                  onClick={() => pick(j)}
                  disabled={Boolean(feedback)}
                  className={`option ${picked ? (feedback.correct ? 'is-ok' : 'is-bad shake') : ''}`}
                >
                  <span className="option-key">{String.fromCharCode(65 + j)}</span>
                  <span className="pt-0.5">{opt}</span>
                </button>
              )
            })}
          </div>

          {feedback && (
            <div className="rise mt-5">
              {feedback.correct ? (
                <p className="flex items-center gap-2 text-sm font-semibold text-ok">
                  <CheckCircle2 size={18} /> To'g'ri! {feedback.xp > 0 && <span className="chip chip-gold">+{feedback.xp} XP</span>}
                </p>
              ) : (
                <p className="rounded-lg bg-bad-soft px-3 py-2 text-sm font-medium text-bad">
                  Noto'g'ri.{' '}
                  {feedback.page && (
                    <>
                      Qayta o'qing: darslikning {feedback.page}-beti
                      {q.topic_id && (
                        <button onClick={() => onOpenTopic(q.topic_id)} className="ml-2 underline">
                          Mavzuga o'tish
                        </button>
                      )}
                    </>
                  )}
                </p>
              )}
              <button onClick={next} className="btn btn-primary mt-4">
                {index + 1 === items.length ? 'Yakunlash' : 'Keyingi savol'}
              </button>
            </div>
          )}
        </div>
      )}

      {total > 0 && done && (
        <div className="card rise p-8 text-center">
          <p className="eyebrow mb-1">Natija</p>
          <p className="font-display text-5xl font-extrabold text-brand">
            {mastered} <span className="text-muted">/ {total}</span>
          </p>
          <p className="mt-2 text-sm text-ink-2">
            {mastered === total ? "Ajoyib! Barcha xatolar tuzatildi." : "Qolgan savollarni yana bir bor takrorlang."}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            {mastered < total && (
              <button onClick={again} className="btn btn-gold">
                <RotateCcw size={14} /> Qolganlarini takrorlash
              </button>
            )}
            <button onClick={onBack} className="btn btn-ghost">Kursga qaytish</button>
          </div>
        </div>
      )}
    </div>
  )
}
