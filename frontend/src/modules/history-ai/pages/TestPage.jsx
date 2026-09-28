import { AlertTriangle, CheckCircle2, Loader2, PartyPopper, RotateCcw, Sparkles, X, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import Confetti from '../components/Confetti'
import { BackLink, ErrorNote, ProgressBar } from '../components/ui'

/** Bir tanlovli (mcq) savol: variant tugmalari, javob matn bo'yicha saqlanadi (indeks emas). */
function McqBody({ q, answer, onChange, disabled, detail: d }) {
  return (
    <div className="flex flex-col gap-2">
      {q.options.map((opt, j) => {
        const isChosen = answer === opt
        const isCorrectOption = d && opt === d.correct_answer
        const isWrongChosen = d && isChosen && !d.correct
        return (
          <button
            key={j}
            type="button"
            disabled={disabled}
            onClick={() => onChange(opt)}
            className={`option ${isChosen && !d ? 'is-selected' : ''} ${isCorrectOption ? 'is-ok' : ''} ${isWrongChosen ? 'is-bad' : ''}`}
            aria-pressed={isChosen}
          >
            <span className="option-key">{String.fromCharCode(65 + j)}</span>
            <span className="pt-0.5">{opt}</span>
            {isCorrectOption && <CheckCircle2 className="ml-auto shrink-0 text-ok" size={18} />}
            {isWrongChosen && <XCircle className="ml-auto shrink-0 text-bad" size={18} />}
          </button>
        )
      })}
    </div>
  )
}

/** Bo'sh joy to'ldirish: erkin matn javobi (katta-kichik harf/bo'shliqqa sezgir emas). */
function FillBlankBody({ answer, onChange, disabled, detail: d }) {
  return (
    <input
      type="text"
      className={`field ${d ? (d.correct ? '!border-ok' : '!border-bad') : ''}`}
      placeholder="Javobingizni shu yerga yozing..."
      value={answer || ''}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}

/** Tartiblash: talaba elementlarni to'g'ri tartibda bosib chiqadi. */
function OrderingBody({ items, answer, onChange, disabled }) {
  const value = answer || []
  const remaining = [...items]
  value.forEach((v) => {
    const idx = remaining.indexOf(v)
    if (idx !== -1) remaining.splice(idx, 1)
  })
  return (
    <div>
      <div className="mb-3 flex min-h-[3rem] flex-wrap gap-2 rounded-lg border border-dashed border-line p-2.5">
        {value.length === 0 && <span className="self-center text-xs text-muted">Pastdagi elementlarni to'g'ri tartibda bosing</span>}
        {value.map((v, idx) => (
          <button
            key={idx}
            type="button"
            disabled={disabled}
            onClick={() => onChange(value.filter((_, j) => j !== idx))}
            className="chip chip-gold"
          >
            {idx + 1}. {v} {!disabled && <X size={12} />}
          </button>
        ))}
      </div>
      {remaining.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {remaining.map((v, idx) => (
            <button key={idx} type="button" disabled={disabled} onClick={() => onChange([...value, v])} className="chip">
              {v}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

/**
 * Rasmiy test (mavzu testi, bo'lim testi yoki yakuniy imtihon). Barcha savollar birdaniga
 * ko'rsatiladi. Topshirilgandan keyin har bir xato savolda to'g'ri javob va tushuntirish
 * ko'rsatiladi (variantlar tartibi har yuklashda aralashtiriladi, shuning uchun bu pozitsiyani
 * yodlab qayta urinishni osonlashtirmaydi).
 */
export default function TestPage({ title, load, create, submit, isTeacher, onBack, onPassed, passedLabel, passThreshold = 1 }) {
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    window.scrollTo({ top: 0 })
    load()
      .then(setTest)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate() {
    setError('')
    try {
      await create()
      setTest(await load())
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSubmit() {
    setError('')
    setSubmitting(true)
    try {
      setResult(await submit(answers))
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  function retry() {
    setAnswers({})
    setResult(null)
    window.scrollTo({ top: 0 })
  }

  const questions = test?.status === 'done' ? test.data?.questions || [] : []
  const isAnswered = (q, i) => {
    const a = answers[i]
    if (q.type === 'ordering') return Array.isArray(a) && a.length === q.items.length
    if (q.type === 'fill_blank') return typeof a === 'string' && a.trim().length > 0
    return a !== undefined
  }
  const answeredCount = questions.filter((q, i) => isAnswered(q, i)).length
  const detailByIndex = Object.fromEntries((result?.details || []).map((d) => [d.index, d]))

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Orqaga</BackLink>

      <header className="mb-8">
        <p className="eyebrow mb-2">Bilimni sinash</p>
        <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">{title}</h1>
        <p className="mt-3 text-sm text-muted">
          {passThreshold >= 1
            ? "Barcha savollarga to'g'ri javob (100%) berilganda o'tilgan hisoblanadi."
            : `Savollarning kamida ${Math.round(passThreshold * 100)}% i to'g'ri bo'lsa o'tilgan hisoblanadi.`}
          {questions.length > 0 && ` Jami ${questions.length} ta savol.`}
        </p>
      </header>

      <ErrorNote>{error}</ErrorNote>
      {loading && <Loader2 className="animate-spin text-gold" size={22} />}

      {!loading && !test && (
        <div className="card flex flex-wrap items-center justify-between gap-4 px-5 py-6">
          <p className="text-sm text-ink-2">Test hali yaratilmagan.</p>
          {isTeacher && (
            <button onClick={handleCreate} className="btn btn-primary btn-sm">
              <Sparkles size={16} /> Yaratish
            </button>
          )}
        </div>
      )}

      {test?.status === 'failed' && (
        <div className="flex items-start gap-2 rounded-xl border border-bad/40 bg-bad-soft px-4 py-4 text-sm text-bad">
          <AlertTriangle size={18} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold">Test tuzib bo'lmadi</p>
            <p className="mt-1">{test.error_message}</p>
            {isTeacher && (
              <button onClick={handleCreate} className="mt-2 underline">Qayta urinish</button>
            )}
          </div>
        </div>
      )}

      {questions.length > 0 && (
        <>
          {isTeacher && !result && (
            <button onClick={handleCreate} className="mb-4 text-xs text-muted underline hover:text-brand">
              Testni qayta yaratish
            </button>
          )}

          {result?.passed && <Confetti />}

          {result && (
            <div
              role="status"
              aria-live="polite"
              className={`rise card mb-8 overflow-hidden p-6 sm:p-8 ${
                result.passed ? '!border-ok' : '!border-gold'
              }`}
            >
              <div className="flex flex-wrap items-center gap-5">
                <div
                  className={`flex h-20 w-20 shrink-0 items-center justify-center rounded-full font-display text-2xl font-extrabold ${
                    result.passed ? 'bg-ok-soft text-ok' : 'bg-gold-soft text-gold'
                  }`}
                >
                  {result.score}/{result.total}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-display text-2xl font-bold text-ink">
                    {result.passed ? (
                      <span className="inline-flex items-center gap-2"><PartyPopper className="text-ok" size={24} /> Tabriklaymiz!</span>
                    ) : (
                      'Yana bir urinib ko\'ring'
                    )}
                  </p>
                  {result.passed && result.xp_gained > 0 && (
                    <p className="xp-pop chip chip-gold mt-2 !text-sm">+{result.xp_gained} ball olindi</p>
                  )}
                  <p className="mt-1 text-sm leading-relaxed text-ink-2">
                    {result.passed
                      ? passedLabel || "Test to'liq topshirildi!"
                      : "Hali yetarlicha emas. Xato savollarning tagida to'g'ri javob va tushuntirish berilgan - shularni o'qib, yana urinib ko'ring."}
                  </p>
                </div>
                {result.passed ? (
                  <button onClick={() => onPassed(result)} className="btn btn-primary">Davom etish</button>
                ) : (
                  <button onClick={retry} className="btn btn-gold">
                    <RotateCcw size={14} /> Qayta urinish
                  </button>
                )}
              </div>
            </div>
          )}

          <ol className="flex flex-col gap-5">
            {questions.map((q, i) => {
              const d = detailByIndex[i]
              return (
                <li
                  key={i}
                  className={`card p-5 sm:p-6 ${d ? (d.correct ? '!border-ok' : '!border-bad') : ''}`}
                >
                  <p className="mb-4 flex items-start gap-3">
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-soft text-sm font-bold text-brand">
                      {i + 1}
                    </span>
                    <span className="flex-1 pt-0.5 font-read text-lg font-medium leading-snug text-ink">{q.question}</span>
                    {d && (d.correct ? <CheckCircle2 className="shrink-0 text-ok" size={22} /> : <XCircle className="shrink-0 text-bad" size={22} />)}
                  </p>
                  {q.type === 'fill_blank' ? (
                    <FillBlankBody
                      answer={answers[i]}
                      disabled={Boolean(result)}
                      detail={d}
                      onChange={(v) => setAnswers((a) => ({ ...a, [i]: v }))}
                    />
                  ) : q.type === 'ordering' ? (
                    <OrderingBody
                      items={q.items}
                      answer={answers[i]}
                      disabled={Boolean(result)}
                      onChange={(v) => setAnswers((a) => ({ ...a, [i]: v }))}
                    />
                  ) : (
                    <McqBody
                      q={q}
                      answer={answers[i]}
                      disabled={Boolean(result)}
                      detail={d}
                      onChange={(v) => setAnswers((a) => ({ ...a, [i]: v }))}
                    />
                  )}
                  {d && !d.correct && (
                    <div className="mt-3 rounded-lg bg-bad-soft px-3 py-2 text-sm text-bad">
                      <p className="font-medium">
                        To'g'ri javob: {Array.isArray(d.correct_answer) ? d.correct_answer.join(' → ') : d.correct_answer}
                      </p>
                      {d.page && <p className="mt-1">Qayta o'qing: darslikning {d.page}-beti</p>}
                      {d.explain && (
                        <p className="mt-1 text-ink-2">
                          {d.explain.heading && <span className="font-semibold">{d.explain.heading}: </span>}
                          {d.explain.snippet}
                        </p>
                      )}
                    </div>
                  )}
                </li>
              )
            })}
          </ol>

          {!result && (
            <div className="card sticky bottom-4 z-20 mt-8 flex items-center gap-4 px-4 py-3 sm:px-5">
              <div className="min-w-0 flex-1">
                <p className="mb-1.5 text-xs font-semibold text-muted">
                  Javob berildi: {answeredCount} / {questions.length}
                </p>
                <ProgressBar value={answeredCount} max={questions.length} />
              </div>
              <button
                onClick={handleSubmit}
                disabled={submitting || answeredCount < questions.length}
                className="btn btn-primary"
              >
                {submitting ? 'Tekshirilmoqda...' : 'Topshirish'}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
