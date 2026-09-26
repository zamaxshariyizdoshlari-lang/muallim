import { AlertTriangle, CheckCircle2, ChevronLeft, Loader2, RotateCcw, Sparkles, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'

/**
 * Rasmiy test (mavzu testi yoki yakuniy imtihon). Barcha savollar birdaniga ko'rsatiladi,
 * 100% to'g'ri bo'lsa o'tiladi. To'g'ri javob ko'rsatilmaydi - faqat qaysi savol xato
 * va qaysi betdan qayta o'qish kerakligi.
 */
export default function TestPage({ title, load, create, submit, isTeacher, onBack, onPassed, passedLabel }) {
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
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
  const answeredCount = Object.keys(answers).length
  const detailByIndex = Object.fromEntries((result?.details || []).map((d) => [d.index, d]))

  return (
    <div className="mx-auto max-w-2xl">
      <button onClick={onBack} className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700">
        <ChevronLeft size={16} /> Orqaga
      </button>
      <h1 className="mb-1 text-2xl font-semibold text-slate-900">{title}</h1>
      <p className="mb-6 text-sm text-slate-500">
        Barcha savollarga to'g'ri javob (100%) berilganda o'tilgan hisoblanadi.
      </p>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
      {loading && <Loader2 className="animate-spin text-slate-400" size={20} />}

      {!loading && !test && (
        <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-6 shadow-sm">
          <p className="text-sm text-slate-600">Test hali yaratilmagan.</p>
          {isTeacher && (
            <button onClick={handleCreate} className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700">
              <Sparkles size={16} /> Yaratish
            </button>
          )}
        </div>
      )}

      {test?.status === 'failed' && (
        <div className="flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700">
          <AlertTriangle size={18} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-medium">Test tuzib bo'lmadi</p>
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
            <button onClick={handleCreate} className="mb-4 text-xs text-slate-500 underline">
              Testni qayta yaratish
            </button>
          )}

          {result && (
            <div className={`mb-6 rounded-lg border px-4 py-4 text-sm ${result.passed ? 'border-green-300 bg-green-50 text-green-800' : 'border-amber-300 bg-amber-50 text-amber-800'}`}>
              <p className="text-base font-semibold">
                Natija: {result.score} / {result.total}
              </p>
              {result.passed ? (
                <>
                  <p className="mt-1">{passedLabel || "Tabriklaymiz, test to'liq topshirildi!"}</p>
                  <button onClick={() => onPassed(result)} className="mt-3 rounded-lg bg-green-600 px-4 py-1.5 font-medium text-white hover:bg-green-700">
                    Davom etish
                  </button>
                </>
              ) : (
                <>
                  <p className="mt-1">
                    Hali hammasi to'g'ri emas. Xato savollarning yonidagi betlarni qayta o'qib chiqing va yana urinib ko'ring.
                  </p>
                  <button onClick={retry} className="mt-3 flex items-center gap-1 rounded-lg border border-amber-400 px-3 py-1.5 font-medium hover:bg-amber-100">
                    <RotateCcw size={14} /> Qayta urinish
                  </button>
                </>
              )}
            </div>
          )}

          <ol className="flex flex-col gap-4">
            {questions.map((q, i) => {
              const d = detailByIndex[i]
              return (
                <li key={i} className={`rounded-xl border bg-white p-4 shadow-sm ${d ? (d.correct ? 'border-green-300' : 'border-red-300') : 'border-slate-200'}`}>
                  <p className="mb-2 flex items-start gap-2 text-sm font-medium text-slate-800">
                    <span className="flex-1">{i + 1}. {q.question}</span>
                    {d && (d.correct ? <CheckCircle2 className="shrink-0 text-green-600" size={18} /> : <XCircle className="shrink-0 text-red-600" size={18} />)}
                  </p>
                  <div className="flex flex-col gap-1">
                    {q.options.map((opt, j) => (
                      <label key={j} className={`flex cursor-pointer items-center gap-2 rounded px-2 py-1 text-sm ${answers[i] === j ? 'bg-indigo-50 text-indigo-800' : 'text-slate-700 hover:bg-slate-50'}`}>
                        <input type="radio" name={`q${i}`} disabled={Boolean(result)} checked={answers[i] === j} onChange={() => setAnswers((a) => ({ ...a, [i]: j }))} />
                        {opt}
                      </label>
                    ))}
                  </div>
                  {d && !d.correct && d.page && (
                    <p className="mt-2 text-xs text-red-600">Qayta o'qing: darslikning {d.page}-beti</p>
                  )}
                </li>
              )
            })}
          </ol>

          {!result && (
            <div className="sticky bottom-4 mt-6 flex items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-3 shadow">
              <span className="text-sm text-slate-500">Javob berildi: {answeredCount} / {questions.length}</span>
              <button
                onClick={handleSubmit}
                disabled={submitting || answeredCount < questions.length}
                className="rounded-lg bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
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
