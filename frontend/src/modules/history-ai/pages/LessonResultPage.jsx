import { AlertTriangle, ChevronLeft, Loader2 } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { getLesson } from '../api/client'
import AssetPanel from '../components/AssetPanel'
import MatchingGame from '../components/MatchingGame'
import PresentationViewer from '../components/PresentationViewer'
import QuizGame from '../components/QuizGame'
import TimelineGame from '../components/TimelineGame'

const POLL_INTERVAL_MS = 2500

export default function LessonResultPage({ lessonId, topicId, topicTitle, onBack }) {
  const [lesson, setLesson] = useState(null)
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => {
    let cancelled = false

    async function poll() {
      try {
        const data = await getLesson(lessonId)
        if (cancelled) return
        setLesson(data)
        if (data.status !== 'pending' && intervalRef.current) {
          clearInterval(intervalRef.current)
        }
      } catch (err) {
        if (!cancelled) setError(err.message)
      }
    }

    poll()
    intervalRef.current = setInterval(poll, POLL_INTERVAL_MS)
    return () => {
      cancelled = true
      clearInterval(intervalRef.current)
    }
  }, [lessonId])

  return (
    <div className="mx-auto max-w-2xl">
      <button
        onClick={onBack}
        className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700"
      >
        <ChevronLeft size={16} /> Mavzular ro'yxatiga qaytish
      </button>

      <h1 className="mb-6 text-2xl font-semibold text-slate-900">{topicTitle}</h1>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {!error && (!lesson || lesson.status === 'pending') && (
        <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-6 text-sm text-slate-600 shadow-sm">
          <Loader2 className="animate-spin" size={18} />
          Dars rejasi va test tayyorlanmoqda... (AI javob bermoqda)
        </div>
      )}

      {lesson?.status === 'failed' && (
        <div className="flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700">
          <AlertTriangle size={18} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-medium">Xatolik yuz berdi</p>
            <p className="mt-1 text-red-600">{lesson.error_message}</p>
          </div>
        </div>
      )}

      {lesson?.status === 'done' && (
        <div className="flex flex-col gap-6">
          <LessonPlanCard plan={lesson.lesson_plan} />
          <QuizCard quiz={lesson.quiz} />

          <h2 className="mt-2 text-lg font-semibold text-slate-900">Taqdimot va o'yinlar</h2>

          <AssetPanel topicId={topicId} kind="presentation" label="Interaktiv taqdimot">
            {(data) => <PresentationViewer slides={data.slides} />}
          </AssetPanel>

          {lesson.quiz?.questions?.length > 0 && (
            <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-slate-900">Viktorina</h2>
              <QuizGame questions={lesson.quiz.questions} />
            </section>
          )}

          <AssetPanel topicId={topicId} kind="game_timeline" label="O'yin: xronologiya tartiblash">
            {(data) => <TimelineGame items={data.items} />}
          </AssetPanel>

          <AssetPanel topicId={topicId} kind="game_matching" label="O'yin: moslashtirish">
            {(data) => <MatchingGame pairs={data.pairs} />}
          </AssetPanel>
        </div>
      )}
    </div>
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
              </li>
            ))}
          </ul>
        </div>
      )}

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
