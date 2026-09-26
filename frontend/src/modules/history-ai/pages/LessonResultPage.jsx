import { AlertTriangle, ChevronLeft, Loader2, RefreshCw, ShieldAlert, Sparkles } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createLesson, getLesson, getLessonByTopic } from '../api/client'
import AssetPanel from '../components/AssetPanel'
import MatchingGame from '../components/MatchingGame'
import PresentationViewer from '../components/PresentationViewer'
import QuizGame from '../components/QuizGame'
import TimelineGame from '../components/TimelineGame'

const POLL_INTERVAL_MS = 2500

export default function LessonResultPage({ topicId, topicTitle, isTeacher, onBack, onStartTest }) {
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    getLessonByTopic(topicId)
      .then((data) => {
        if (cancelled) return
        setLesson(data)
        if (data?.status === 'pending') startPolling()
      })
      .catch((err) => !cancelled && setError(err.message))
      .finally(() => !cancelled && setLoading(false))

    return () => {
      cancelled = true
      clearInterval(intervalRef.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId])

  function startPolling() {
    clearInterval(intervalRef.current)
    intervalRef.current = setInterval(async () => {
      try {
        const data = await getLessonByTopic(topicId)
        setLesson(data)
        if (data?.status !== 'pending') clearInterval(intervalRef.current)
      } catch (err) {
        setError(err.message)
        clearInterval(intervalRef.current)
      }
    }, POLL_INTERVAL_MS)
  }

  async function handleGenerate(regenerate) {
    setError('')
    try {
      const created = await createLesson(topicId, { regenerate })
      setLesson(created)
      if (created.status === 'pending') startPolling()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <button
        onClick={onBack}
        className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700"
      >
        <ChevronLeft size={16} /> Mavzular ro'yxatiga qaytish
      </button>

      <h1 className="mb-6 text-2xl font-semibold text-slate-900">{topicTitle}</h1>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

      {loading && (
        <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-6 text-sm text-slate-600 shadow-sm">
          <Loader2 className="animate-spin" size={18} />
          Yuklanmoqda...
        </div>
      )}

      {!loading && !lesson && (
        <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-6 shadow-sm">
          <p className="text-sm text-slate-600">
            {isTeacher ? 'Bu mavzu uchun dars rejasi va test hali yaratilmagan.' : "Bu mavzu materiallarini o'qituvchi hali tayyorlamagan."}
          </p>
          {isTeacher && (
            <button
              onClick={() => handleGenerate(false)}
              className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
            >
              <Sparkles size={16} /> Yaratish
            </button>
          )}
        </div>
      )}

      {lesson?.status === 'pending' && (
        <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-6 text-sm text-slate-600 shadow-sm">
          <Loader2 className="animate-spin" size={18} />
          Dars rejasi va test tayyorlanmoqda... (AI javob bermoqda)
        </div>
      )}

      {lesson?.status === 'failed' && (
        <div className="flex flex-col gap-3">
          <div className="flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700">
            <AlertTriangle size={18} className="mt-0.5 shrink-0" />
            <div>
              <p className="font-medium">Xatolik yuz berdi</p>
              <p className="mt-1 text-red-600">{lesson.error_message}</p>
            </div>
          </div>
          <button
            onClick={() => handleGenerate(true)}
            className="flex w-fit items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
          >
            <RefreshCw size={14} /> Qayta urinish
          </button>
        </div>
      )}

      {lesson?.status === 'done' && (
        <div className="flex flex-col gap-6">
          {isTeacher && (
            <div className="flex justify-end">
              <button
                onClick={() => handleGenerate(true)}
                className="flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-50"
              >
                <RefreshCw size={13} /> Dars rejasini qayta yaratish
              </button>
            </div>
          )}

          <StageHeading n={1} text="Mavzu tushuntirilishi" />
          <LessonPlanCard plan={lesson.lesson_plan} />

          <StageHeading n={2} text="O'yinlar (ixtiyoriy mashq)" />
          <AssetPanel topicId={topicId} kind="presentation" label="Interaktiv taqdimot" isTeacher={isTeacher}>
            {(data) => <PresentationViewer slides={data.slides} />}
          </AssetPanel>
          <AssetPanel topicId={topicId} kind="game_timeline" label="Xronologiya tartiblash" isTeacher={isTeacher}>
            {(data) => <TimelineGame items={data.items} />}
          </AssetPanel>
          <AssetPanel topicId={topicId} kind="game_matching" label="Moslashtirish" isTeacher={isTeacher}>
            {(data) => <MatchingGame pairs={data.pairs} />}
          </AssetPanel>
          <AssetPanel topicId={topicId} kind="game_fill_blank" label="Bo'sh joyni to'ldirish" isTeacher={isTeacher}>
            {(data) => <QuizGame questions={data.questions} />}
          </AssetPanel>

          <StageHeading n={3} text="Savollar" />
          <BookQuestions items={lesson.quiz?.book_questions} />
          <QuizCard quiz={lesson.quiz} />
          {lesson.quiz?.questions?.length > 0 && (
            <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-slate-900">Viktorina</h2>
              <QuizGame questions={lesson.quiz.questions} />
            </section>
          )}

          <StageHeading n={4} text="Mavzu testi" />
          <section className="rounded-xl border border-indigo-200 bg-indigo-50 p-6 shadow-sm">
            <p className="mb-3 text-sm text-slate-700">
              Mavzudagi barcha ma'lumotlar bo'yicha to'liq test. Keyingi mavzu faqat testni 100% topshirgandan keyin ochiladi.
            </p>
            <button onClick={onStartTest} className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
              {isTeacher ? "Testni ko'rish / yaratish" : 'Testni boshlash'}
            </button>
          </section>
        </div>
      )}
    </div>
  )
}

function StageHeading({ n, text }) {
  return (
    <h2 className="mt-4 flex items-center gap-2 text-lg font-semibold text-slate-900">
      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-indigo-600 text-sm text-white">{n}</span>
      {text}
    </h2>
  )
}

function PageTag({ page }) {
  if (page === undefined || page === null) return null
  return (
    <span className="ml-2 inline-block rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-500">
      bet {page}
    </span>
  )
}

function UnverifiedTag() {
  return (
    <span
      title="Bu fakt kitob matnida avtomatik tasdiqlanmadi"
      className="ml-2 inline-flex items-center gap-1 rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-700"
    >
      <ShieldAlert size={12} /> kitobda tasdiqlanmadi
    </span>
  )
}

function LessonPlanCard({ plan }) {
  if (!plan) return null
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Dars rejasi</h2>

      {plan.goals?.length > 0 && (
        <div className="mb-4">
          <h3 className="mb-1 text-sm font-medium text-slate-700">Maqsadlar</h3>
          <ul className="list-inside list-disc text-sm text-slate-600">
            {plan.goals.map((goal, i) => (
              <li key={i}>{goal}</li>
            ))}
          </ul>
        </div>
      )}

      {plan.key_facts?.length > 0 && (
        <div className="mb-4">
          <h3 className="mb-1 text-sm font-medium text-slate-700">Asosiy faktlar</h3>
          <ul className="flex flex-col gap-1 text-sm text-slate-600">
            {plan.key_facts.map((f, i) => (
              <li key={i}>
                {f.fact}
                <PageTag page={f.page} />
                {f.verified === false && <UnverifiedTag />}
              </li>
            ))}
          </ul>
        </div>
      )}

      {plan.blocks?.map((b, i) => (
        <div key={i} className="mb-4">
          {b.heading && <h3 className="mb-1 text-sm font-semibold text-slate-800">{b.heading}</h3>}
          <p className="whitespace-pre-line text-sm leading-relaxed text-slate-700">
            {b.text}
            {b.pages?.map((pg) => <PageTag key={pg} page={pg} />)}
          </p>
        </div>
      ))}

      {plan.explanation && (
        <div className="mb-4">
          <h3 className="mb-1 text-sm font-medium text-slate-700">Tushuntirish</h3>
          <p className="text-sm text-slate-600">{plan.explanation}</p>
        </div>
      )}

      {plan.summary && (
        <div>
          <h3 className="mb-1 text-sm font-medium text-slate-700">Xulosa</h3>
          <p className="text-sm text-slate-600">{plan.summary}</p>
        </div>
      )}
    </section>
  )
}

function BookQuestions({ items }) {
  const [open, setOpen] = useState({})
  if (!items?.length) return null
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Darslikdagi savol va topshiriqlar</h2>
      <ol className="flex flex-col gap-4">
        {items.map((q, i) => (
          <li key={i}>
            <p className="text-sm font-medium text-slate-800">{i + 1}. {q.question}</p>
            {open[i] ? (
              <p className="mt-2 rounded bg-green-50 px-3 py-2 text-sm text-green-800">
                {q.answer}<PageTag page={q.page} />
              </p>
            ) : (
              <button onClick={() => setOpen((o) => ({ ...o, [i]: true }))} className="mt-1 text-xs text-indigo-600 underline">
                Javobni ko'rish
              </button>
            )}
          </li>
        ))}
      </ol>
    </section>
  )
}

function QuizCard({ quiz }) {
  if (!quiz?.questions?.length) return null
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Test savollari</h2>
      <ol className="flex flex-col gap-4">
        {quiz.questions.map((q, i) => (
          <li key={i}>
            <p className="text-sm font-medium text-slate-800">
              {i + 1}. {q.question}
              <PageTag page={q.page} />
            </p>
            <ul className="mt-2 flex flex-col gap-1">
              {q.options?.map((opt, j) => (
                <li
                  key={j}
                  className={`rounded px-2 py-1 text-sm ${
                    j === q.correct_index
                      ? 'bg-green-50 text-green-700'
                      : 'text-slate-600'
                  }`}
                >
                  {String.fromCharCode(65 + j)}. {opt}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ol>
    </section>
  )
}
