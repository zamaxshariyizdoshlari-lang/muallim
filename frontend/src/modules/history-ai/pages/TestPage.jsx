import { AlertTriangle, BookOpen, CheckCircle2, Lightbulb, Loader2, PartyPopper, RotateCcw, Sparkles, XCircle } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import Confetti from '../components/Confetti'
import { BackLink, ErrorNote, ProgressBar } from '../components/ui'

const LEVEL_LABELS = { eslash: 'Eslash', tushunish: 'Tushunish', qollash: "Qo'llash" }

function shuffled(items) {
  const a = [...items]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

/**
 * Har urinishda savollar va variantlar tartibi aralashtiriladi (yodlab olishning oldini olish).
 * Oldingi urinishda xato qilingan savollar oldinga chiqariladi. Server asl indekslar bilan ishlaydi:
 * `qi` - savolning asl o'rni, `oi` - variantning asl o'rni.
 */
function buildOrder(questions, wrongFirst = []) {
  const wrong = new Set(wrongFirst)
  const order = shuffled(questions.map((_, qi) => qi))
  order.sort((a, b) => Number(wrong.has(b)) - Number(wrong.has(a)))  // barqaror: xatolar oldinda
  return order.map((qi) => ({ qi, options: shuffled(questions[qi].options.map((_, oi) => oi)) }))
}

/** Xatolarni mavzu (tag) yoki bet bo'yicha guruhlaydi: "qaysi qismni takrorlash kerak". */
function groupMistakes(details) {
  const groups = new Map()
  for (const d of details) {
    if (d.correct) continue
    const label = d.tag || (d.page ? `Darslikning ${d.page}-beti` : null)
    if (!label) continue
    groups.set(label, (groups.get(label) || 0) + 1)
  }
  return [...groups.entries()].sort((a, b) => b[1] - a[1])
}

/**
 * Rasmiy test (mavzu testi, bo'lim testi yoki yakuniy imtihon). Barcha savollar birdaniga ko'rsatiladi;
 * to'g'ri javoblar foizi o'tish chegarasidan kam bo'lmasa o'tiladi. To'g'ri javob ko'rsatilmaydi -
 * faqat qaysi savol xato va qaysi betdan qayta o'qish kerakligi (o'tilgach "nega?" izohi ham).
 * `hint(index, level)` berilsa, har savolda bosqichli maslahat tugmasi chiqadi.
 */
export default function TestPage({ title, load, create, submit, hint, isTeacher, onBack, onPassed, passedLabel, reloadOnRetry }) {
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [attempt, setAttempt] = useState({ n: 0, wrong: [] })
  // Maslahatlar: {savol_indeksi: {level, page, explain, eliminate}}; urinish almashganda tozalanadi.
  const [hints, setHints] = useState({})
  const [hintBusy, setHintBusy] = useState(false)
  const draftKey = `muallim:test-draft:${title}`
  const [draftLoaded, setDraftLoaded] = useState(false)

  useEffect(() => {
    window.scrollTo({ top: 0 })
    load()
      .then(setTest)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Qoralama: yarim qolgan javoblar brauzerda saqlanadi (savollar soni o'zgargan bo'lsa tashlab yuboriladi).
  useEffect(() => {
    if (draftLoaded || test?.status !== 'done') return
    try {
      const saved = JSON.parse(localStorage.getItem(draftKey) || 'null')
      if (saved && saved.n === (test.data?.questions || []).length && saved.answers) setAnswers(saved.answers)
    } catch { /* localStorage mavjud emas */ }
    setDraftLoaded(true)
  }, [test, draftLoaded, draftKey])

  useEffect(() => {
    if (!draftLoaded || test?.status !== 'done') return
    try {
      if (result?.passed || Object.keys(answers).length === 0) localStorage.removeItem(draftKey)
      else if (!result) localStorage.setItem(draftKey, JSON.stringify({ n: (test.data?.questions || []).length, answers }))
    } catch { /* localStorage mavjud emas */ }
  }, [answers, result, draftLoaded, test, draftKey])

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

  async function askHint(i) {
    const level = (hints[i]?.level || 0) + 1
    if (level > 2 || hintBusy) return
    setHintBusy(true)
    setError('')
    try {
      const h = await hint(i, level)
      setHints((all) => ({ ...all, [i]: { ...all[i], ...h } }))
      if (level === 2 && h.eliminate?.includes(answers[i])) {
        setAnswers((a) => { const { [i]: _drop, ...rest } = a; return rest })
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setHintBusy(false)
    }
  }

  async function retry() {
    if (reloadOnRetry) {
      // Yakuniy imtihon: har urinishda butunlay yangi savollar
      try { localStorage.removeItem(draftKey) } catch { /* ignore */ }
      setLoading(true)
      try {
        setTest(await load())
        setAttempt((a) => ({ n: a.n + 1, wrong: [] }))
        setAnswers({})
        setHints({})
        setResult(null)
        window.scrollTo({ top: 0 })
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
      return
    }
    const wrong = (result?.details || []).filter((d) => !d.correct).map((d) => d.index)
    setAttempt((a) => ({ n: a.n + 1, wrong }))
    setAnswers({})
    setHints({})
    setResult(null)
    window.scrollTo({ top: 0 })
  }

  const questions = test?.status === 'done' ? test.data?.questions || [] : []
  const passPercent = result?.pass_percent ?? test?.data?.pass_percent ?? 100
  // Tartib har urinishda yangilanadi (savollar yuklangach va "qayta urinish"da)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const layout = useMemo(() => buildOrder(questions, attempt.wrong), [test, attempt.n])
  const mistakes = result && !result.passed ? groupMistakes(result.details || []) : []
  const answeredCount = Object.keys(answers).length
  const detailByIndex = Object.fromEntries((result?.details || []).map((d) => [d.index, d]))

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Orqaga</BackLink>

      <header className="mb-8">
        <p className="eyebrow mb-2">Bilimni sinash</p>
        <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">{title}</h1>
        <p className="mt-3 text-sm text-muted">
          {passPercent >= 100
            ? "Barcha savollarga to'g'ri javob (100%) berilganda o'tilgan hisoblanadi."
            : `Kamida ${passPercent}% to'g'ri javob berilganda o'tilgan hisoblanadi. Xato qilganlaringiz keyinroq takrorlash uchun saqlanadi.`}
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
                      : result.fail_reason
                        ? `${result.fail_reason} Zaif mavzularni takrorlab, yangi savollar bilan yana urinib ko'ring.`
                        : `Hali yetarli emas (kamida ${passPercent}% kerak). Xato savollarning tagidagi betlarni qayta o'qib chiqing va yana urinib ko'ring.`}
                  </p>
                  {!result.passed && attempt.n >= 1 && (
                    <p className="mt-2 text-sm text-ink-2">
                      Qiyin bo'layaptimi? Darsga qaytib, tushuntirishni qayta ko'rib chiqing, so'ng yana urinib ko'ring.
                      <button onClick={onBack} className="ml-2 inline-flex items-center gap-1 font-semibold text-brand underline">
                        <BookOpen size={14} /> Darsga qaytish
                      </button>
                    </p>
                  )}
                  {mistakes.length > 0 && (
                    <div className="mt-3 text-sm text-ink-2">
                      <p className="font-semibold text-ink">Quyidagilarni takrorlang:</p>
                      <ul className="mt-1 flex flex-wrap gap-2">
                        {mistakes.map(([label, n]) => (
                          <li key={label} className="chip !border-bad/40 !bg-bad-soft !text-bad">{label} · {n} ta xato</li>
                        ))}
                      </ul>
                    </div>
                  )}
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
            {layout.map(({ qi: i, options }, pos) => {
              const q = questions[i]
              const d = detailByIndex[i]
              return (
                <li
                  key={i}
                  className={`card p-5 sm:p-6 ${d ? (d.correct ? '!border-ok' : '!border-bad') : ''}`}
                >
                  <p className="mb-4 flex items-start gap-3">
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-soft text-sm font-bold text-brand">
                      {pos + 1}
                    </span>
                    <span className="flex-1 pt-0.5 font-read text-lg font-medium leading-snug text-ink">
                      {q.question}
                      {q.level && LEVEL_LABELS[q.level] && (
                        <span className="chip ml-2 align-middle !text-[0.68rem]">{LEVEL_LABELS[q.level]}</span>
                      )}
                    </span>
                    {d && (d.correct ? <CheckCircle2 className="shrink-0 text-ok" size={22} /> : <XCircle className="shrink-0 text-bad" size={22} />)}
                  </p>
                  <div className="flex flex-col gap-2">
                    {options.map((j, k) => {
                      const gone = hints[i]?.eliminate?.includes(j)
                      return (
                        <button
                          key={j}
                          type="button"
                          disabled={Boolean(result) || gone}
                          onClick={() => setAnswers((a) => ({ ...a, [i]: j }))}
                          className={`option ${answers[i] === j ? 'is-selected' : ''} ${gone ? 'opacity-40 line-through' : ''}`}
                          aria-pressed={answers[i] === j}
                        >
                          <span className="option-key">{String.fromCharCode(65 + k)}</span>
                          <span className="pt-0.5">{q.options[j]}</span>
                        </button>
                      )
                    })}
                  </div>
                  {hint && !result && (
                    <div className="mt-3">
                      {hints[i]?.level >= 1 && (
                        <p className="mb-2 flex items-start gap-2 rounded-lg bg-gold-soft px-3 py-2 text-sm text-ink-2">
                          <Lightbulb size={16} className="mt-0.5 shrink-0 text-gold" />
                          <span>
                            {hints[i].page ? `Darslikning ${hints[i].page}-betiga qarang. ` : ''}
                            {hints[i].explain && (
                              <>
                                {hints[i].explain.heading && <span className="font-semibold">{hints[i].explain.heading}: </span>}
                                {hints[i].explain.snippet}
                              </>
                            )}
                            {hints[i].level >= 2 && " Ikkita noto'g'ri variant olib tashlandi."}
                          </span>
                        </p>
                      )}
                      {(hints[i]?.level || 0) < 2 && (
                        <button
                          type="button"
                          onClick={() => askHint(i)}
                          disabled={hintBusy}
                          className="inline-flex items-center gap-1.5 text-sm font-semibold text-brand underline-offset-2 hover:underline"
                        >
                          <Lightbulb size={14} />
                          {hints[i]?.level ? "Yana maslahat (2 ta variantni olib tashlash)" : 'Maslahat'}
                        </button>
                      )}
                    </div>
                  )}
                  {d?.why && (
                    <p className="mt-3 flex items-start gap-2 rounded-lg bg-ok-soft px-3 py-2 text-sm text-ink-2">
                      <Lightbulb size={16} className="mt-0.5 shrink-0 text-ok" />
                      <span><span className="font-semibold text-ink">Nega? </span>{d.why}</span>
                    </p>
                  )}
                  {d && !d.correct && (d.page || d.explain) && (
                    <div className="mt-3 rounded-lg bg-bad-soft px-3 py-2 text-sm text-bad">
                      {d.page && <p className="font-medium">Qayta o'qing: darslikning {d.page}-beti</p>}
                      {d.explain && (
                        <p className={d.page ? 'mt-1 text-ink-2' : 'font-medium text-ink-2'}>
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
