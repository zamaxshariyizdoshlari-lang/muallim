import {
  AlertTriangle, BookMarked, CheckCircle2, Clock, Gamepad2, HelpCircle, Layers, Lightbulb, Link2, ListChecks,
  Presentation, RefreshCw, ShieldAlert, Sparkles, Target,
} from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createLesson, getLessonByTopic } from '../api/client'
import AssetPanel from '../components/AssetPanel'
import MatchingGame from '../components/MatchingGame'
import PresentationViewer from '../components/PresentationViewer'
import QuizGame from '../components/QuizGame'
import TimelineGame from '../components/TimelineGame'
import { BackLink, ErrorNote, PageTag, Spinner } from '../components/ui'

const POLL_INTERVAL_MS = 2500

const STAGES = [
  { n: 1, id: 'stage-1', label: 'Tushuntirish', icon: BookMarked },
  { n: 2, id: 'stage-2', label: "O'yinlar", icon: Gamepad2 },
  { n: 3, id: 'stage-3', label: 'Savollar', icon: HelpCircle },
  { n: 4, id: 'stage-4', label: 'Mavzu testi', icon: ListChecks },
]

export default function LessonResultPage({ topicId, topicTitle, isTeacher, onBack, onStartTest }) {
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => {
    window.scrollTo({ top: 0 })
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

  function goTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const ready = lesson?.status === 'done'
  const pageRange = ready ? pageRangeOf(lesson.lesson_plan) : null

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Mavzular ro'yxatiga qaytish</BackLink>

      <header className="mb-6">
        <p className="eyebrow mb-2">Mavzu</p>
        <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">{topicTitle}</h1>
        {pageRange && (
          <p className="mt-3 flex items-center gap-2 text-sm text-muted">
            <Clock size={14} /> Darslikning {pageRange} betlari asosida
          </p>
        )}
      </header>

      {ready && (
        <nav
          aria-label="Bosqichlar"
          className="sticky top-[4.15rem] z-20 -mx-4 mb-8 overflow-x-auto border-b border-line bg-paper/90 px-4 py-2 backdrop-blur"
        >
          <ul className="flex min-w-max gap-2">
            {STAGES.map((s) => (
              <li key={s.id}>
                <button onClick={() => goTo(s.id)} className="btn btn-ghost btn-sm !rounded-full">
                  <span className="flex h-5 w-5 items-center justify-center rounded-full bg-brand text-[0.68rem] text-brand-ink">
                    {s.n}
                  </span>
                  {s.label}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      )}

      <ErrorNote>{error}</ErrorNote>

      {loading && <Spinner>Yuklanmoqda...</Spinner>}

      {!loading && !lesson && (
        <div className="card flex flex-wrap items-center justify-between gap-4 px-5 py-6">
          <p className="text-sm text-ink-2">
            {isTeacher ? 'Bu mavzu uchun dars rejasi va test hali yaratilmagan.' : "Bu mavzu materiallari hali tayyorlanmagan."}
          </p>
          {isTeacher && (
            <button onClick={() => handleGenerate(false)} className="btn btn-primary btn-sm">
              <Sparkles size={16} /> Yaratish
            </button>
          )}
        </div>
      )}

      {lesson?.status === 'pending' && <Spinner>Dars rejasi va test tayyorlanmoqda... (AI javob bermoqda)</Spinner>}

      {lesson?.status === 'failed' && (
        <div className="flex flex-col gap-3">
          <div className="flex items-start gap-2 rounded-xl border border-bad/40 bg-bad-soft px-4 py-4 text-sm text-bad">
            <AlertTriangle size={18} className="mt-0.5 shrink-0" />
            <div>
              <p className="font-semibold">Xatolik yuz berdi</p>
              <p className="mt-1">{lesson.error_message}</p>
            </div>
          </div>
          <button onClick={() => handleGenerate(true)} className="btn btn-ghost btn-sm w-fit">
            <RefreshCw size={14} /> Qayta urinish
          </button>
        </div>
      )}

      {ready && (
        <div className="flex flex-col gap-14">
          {isTeacher && (
            <div className="-mb-8 flex justify-end">
              <button onClick={() => handleGenerate(true)} className="btn btn-ghost btn-sm">
                <RefreshCw size={13} /> Dars rejasini qayta yaratish
              </button>
            </div>
          )}

          <Stage n={1} id="stage-1" title="Mavzu tushuntirilishi">
            <LessonPlanCard plan={lesson.lesson_plan} />
          </Stage>

          <Stage n={2} id="stage-2" title="O'yinlar" hint="Ixtiyoriy mashq — bilimni qiziqarli tarzda mustahkamlang.">
            <div className="flex flex-col gap-5">
              <AssetPanel topicId={topicId} kind="presentation" label="Interaktiv taqdimot" icon={Presentation} isTeacher={isTeacher}>
                {(data) => <PresentationViewer slides={data.slides} />}
              </AssetPanel>
              <AssetPanel topicId={topicId} kind="game_timeline" label="Xronologiya tartiblash" icon={Clock} isTeacher={isTeacher}>
                {(data) => <TimelineGame items={data.items} />}
              </AssetPanel>
              <AssetPanel topicId={topicId} kind="game_matching" label="Moslashtirish" icon={Link2} isTeacher={isTeacher}>
                {(data) => <MatchingGame pairs={data.pairs} />}
              </AssetPanel>
              <AssetPanel topicId={topicId} kind="game_fill_blank" label="Bo'sh joyni to'ldirish" icon={Layers} isTeacher={isTeacher}>
                {(data) => <QuizGame questions={data.questions} />}
              </AssetPanel>
            </div>
          </Stage>

          <Stage n={3} id="stage-3" title="Savollar">
            <div className="flex flex-col gap-5">
              <BookQuestions items={lesson.quiz?.book_questions} />
              <QuizCard quiz={lesson.quiz} />
              {lesson.quiz?.questions?.length > 0 && (
                <section className="card p-5 sm:p-6">
                  <h3 className="mb-4 font-display text-lg font-bold text-ink">Viktorina</h3>
                  <QuizGame questions={lesson.quiz.questions} />
                </section>
              )}
            </div>
          </Stage>

          <Stage n={4} id="stage-4" title="Mavzu testi">
            <section className="card relative overflow-hidden border-brand/40 p-6 sm:p-8">
              <div className="meander absolute inset-x-0 top-0" />
              <div className="flex flex-wrap items-center gap-5 pt-2">
                <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-brand text-brand-ink">
                  <ListChecks size={28} />
                </span>
                <div className="min-w-0 flex-1">
                  <p className="font-read text-base leading-relaxed text-ink-2">
                    Mavzudagi barcha ma'lumotlar bo'yicha to'liq test. Keyingi mavzu faqat testni <b className="text-ink">100%</b> topshirgandan
                    keyin ochiladi.
                  </p>
                </div>
                <button onClick={onStartTest} className="btn btn-primary">
                  {isTeacher ? "Testni ko'rish / yaratish" : 'Testni boshlash'}
                </button>
              </div>
            </section>
          </Stage>
        </div>
      )}
    </div>
  )
}

function pageRangeOf(plan) {
  const pages = (plan?.blocks || []).flatMap((b) => b.pages || []).filter((p) => Number.isFinite(p))
  if (!pages.length) return null
  const min = Math.min(...pages)
  const max = Math.max(...pages)
  return min === max ? String(min) : `${min}–${max}`
}

function Stage({ n, id, title, hint, children }) {
  return (
    <section id={id} className="scroll-mt-32">
      <div className="mb-6">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand font-display text-lg font-bold text-brand-ink shadow">
            {n}
          </span>
          <h2 className="font-display text-2xl font-bold text-ink sm:text-3xl">{title}</h2>
        </div>
        {hint && <p className="ml-13 mt-1 pl-1 text-sm text-muted">{hint}</p>}
      </div>
      {children}
    </section>
  )
}

function UnverifiedTag() {
  return (
    <span
      title="Bu fakt kitob matnida avtomatik tasdiqlanmadi"
      className="chip ml-2 !border-gold/50 !bg-warn-soft !text-gold"
    >
      <ShieldAlert size={12} /> kitobda tasdiqlanmadi
    </span>
  )
}

function LessonPlanCard({ plan }) {
  if (!plan) return null
  return (
    <div className="flex flex-col gap-6">
      {plan.goals?.length > 0 && (
        <div className="card border-gold/40 bg-gold-soft/40 p-5 sm:p-6">
          <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
            <Target size={18} className="text-gold" /> Bu mavzuda nimani o'rganasiz
          </h3>
          <ul className="flex flex-col gap-2">
            {plan.goals.map((goal, i) => (
              <li key={i} className="flex gap-2.5 text-[0.95rem] text-ink-2">
                <CheckCircle2 size={18} className="mt-0.5 shrink-0 text-ok" />
                {goal}
              </li>
            ))}
          </ul>
        </div>
      )}

      {plan.blocks?.length > 0 && (
        <article className="card p-6 sm:p-9">
          {plan.blocks.map((b, i) => (
            <div key={i} className={i > 0 ? 'mt-9' : ''}>
              {b.heading && (
                <h3 className="mb-4 border-b border-line pb-2 font-display text-xl font-bold text-brand sm:text-2xl">{b.heading}</h3>
              )}
              <div className="read">
                {b.text.split(/\n{2,}/).map((para, pi) => (
                  <p key={pi} className={i === 0 && pi === 0 ? 'read-first' : ''}>
                    {para}
                  </p>
                ))}
              </div>
              {b.pages?.length > 0 && (
                <p className="mt-3 flex flex-wrap items-center gap-1 text-xs text-muted">
                  Manba:
                  {b.pages.map((pg) => (
                    <PageTag key={pg} page={pg} />
                  ))}
                </p>
              )}
            </div>
          ))}
        </article>
      )}

      {plan.key_facts?.length > 0 && (
        <div>
          <h3 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
            <Lightbulb size={18} className="text-gold" /> Esda tuting
          </h3>
          <ul className="grid gap-3 sm:grid-cols-2">
            {plan.key_facts.map((f, i) => (
              <li key={i} className="card border-l-4 !border-l-gold p-4 text-sm leading-relaxed text-ink-2">
                {f.fact}
                <PageTag page={f.page} />
                {f.verified === false && <UnverifiedTag />}
              </li>
            ))}
          </ul>
        </div>
      )}

      {plan.explanation && (
        <div className="card p-5 sm:p-6">
          <h3 className="mb-2 font-display text-lg font-bold text-ink">Tushuntirish</h3>
          <p className="read !text-base">{plan.explanation}</p>
        </div>
      )}

      {plan.summary && (
        <div className="rounded-2xl border border-brand/30 bg-brand-soft p-5 sm:p-6">
          <h3 className="mb-2 font-display text-lg font-bold text-brand">Xulosa</h3>
          <p className="font-read text-base leading-relaxed text-ink">{plan.summary}</p>
        </div>
      )}
    </div>
  )
}

function BookQuestions({ items }) {
  const [open, setOpen] = useState({})
  if (!items?.length) return null
  return (
    <section className="card p-5 sm:p-6">
      <h3 className="mb-5 font-display text-lg font-bold text-ink">Darslikdagi savol va topshiriqlar</h3>
      <ol className="flex flex-col gap-5">
        {items.map((q, i) => (
          <li key={i} className="flex gap-3">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-soft text-sm font-bold text-brand">
              {i + 1}
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-read text-base font-medium leading-snug text-ink">{q.question}</p>
              {open[i] ? (
                <p className="rise mt-3 rounded-xl border border-ok/40 bg-ok-soft px-4 py-3 text-sm leading-relaxed text-ink">
                  {q.answer}
                  <PageTag page={q.page} />
                </p>
              ) : (
                <button onClick={() => setOpen((o) => ({ ...o, [i]: true }))} className="btn btn-ghost btn-sm mt-2.5">
                  Javobni ko'rish
                </button>
              )}
            </div>
          </li>
        ))}
      </ol>
    </section>
  )
}

function QuizCard({ quiz }) {
  if (!quiz?.questions?.length) return null
  return (
    <section className="card p-5 sm:p-6">
      <h3 className="mb-5 font-display text-lg font-bold text-ink">Test savollari (javoblari bilan)</h3>
      <ol className="flex flex-col gap-5">
        {quiz.questions.map((q, i) => (
          <li key={i}>
            <p className="font-read text-base font-medium text-ink">
              {i + 1}. {q.question}
              <PageTag page={q.page} />
            </p>
            <ul className="mt-2 flex flex-col gap-1.5">
              {q.options?.map((opt, j) => (
                <li
                  key={j}
                  className={`rounded-lg px-3 py-1.5 text-sm ${
                    j === q.correct_index ? 'bg-ok-soft font-semibold text-ok' : 'text-ink-2'
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
