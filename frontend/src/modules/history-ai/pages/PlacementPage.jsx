import { ArrowLeft, ArrowRight, Check, Compass, RotateCcw, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getPlacementTest, listPlacements, submitPlacement } from '../api/client'
import { ErrorNote, Spinner } from '../components/ui'

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']

/** Daraja aniqlash testi: savollar ketma-ket, natijada tavsiya etilgan kurs. */
export default function PlacementPage() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [info, setInfo] = useState(null)
  const [questions, setQuestions] = useState(null)
  const [answers, setAnswers] = useState({})
  const [index, setIndex] = useState(0)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    listPlacements().then((list) => setInfo(list.find((p) => p.subject_slug === slug) || false)).catch((e) => setError(e.message))
  }, [slug])

  async function start() {
    setError('')
    setBusy(true)
    try {
      const data = await getPlacementTest(slug)
      setQuestions(data.questions)
      setAnswers({})
      setIndex(0)
      setResult(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  async function finish() {
    setBusy(true)
    setError('')
    try {
      const full = Object.fromEntries(questions.map((x) => [x.id, answers[x.id] ?? -1]))
      setResult(await submitPlacement(slug, full))
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  if (info === null && !error) return <Spinner>Yuklanmoqda...</Spinner>
  if (info === false) {
    return (
      <div className="card p-6">
        <p className="text-ink-2">Bu fan uchun daraja testi hali tayyor emas.</p>
        <Link to="/" className="btn btn-ghost btn-sm mt-3">Bosh sahifa</Link>
      </div>
    )
  }

  // Natija
  if (result) {
    const stages = Object.entries(result.per_stage)
    return (
      <div className="rise mx-auto max-w-2xl">
        <p className="eyebrow mb-1">{info?.subject_title} · daraja natijasi</p>
        <h1 className="mb-5 font-display text-3xl font-extrabold text-ink">Sizning darajangiz: {result.level_label}</h1>
        <div className="card mb-5 p-5">
          <p className="mb-3 text-sm text-muted">Umumiy natija: {result.score} / {result.total} ({result.percent}%)</p>
          <ul className="flex flex-col gap-3">
            {info?.stages.map((label, i) => {
              const [key, p] = stages[i] || []
              const pct = p && p.total ? Math.round((p.right / p.total) * 100) : 0
              return (
                <li key={key || label}>
                  <div className="mb-1 flex justify-between text-sm"><span className="font-semibold text-ink">{label}</span><span className="text-muted">{p ? `${p.right}/${p.total}` : '—'}</span></div>
                  <div className="h-2 overflow-hidden rounded-full bg-paper-2"><div className={`h-full rounded-full ${pct >= 60 ? 'bg-ok' : 'bg-gold'}`} style={{ width: `${pct}%` }} /></div>
                </li>
              )
            })}
          </ul>
        </div>
        {result.recommended && (
          <div className="mb-5 rounded-2xl bg-chalk p-6 text-chalk-ink">
            <p className="mb-1 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-chalk-ink/60"><Sparkles size={14} /> Sizga tavsiya</p>
            <p className="mb-4 font-display text-xl font-bold">{result.recommended.title}</p>
            <button onClick={() => navigate(`/kurs/${result.recommended.book_id}`)} className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-chalk">
              Kursni boshlash <ArrowRight size={16} />
            </button>
          </div>
        )}
        <p className="mb-4 text-xs text-muted">Bu test taxminiy yo'naltirish uchun. Xohlasangiz istalgan kursni o'zingiz tanlashingiz mumkin.</p>
        <div className="flex gap-2">
          <button onClick={start} className="btn btn-ghost btn-sm"><RotateCcw size={14} /> Qayta topshirish</button>
          <Link to="/" className="btn btn-ghost btn-sm">Bosh sahifa</Link>
        </div>
      </div>
    )
  }

  // Kirish
  if (!questions) {
    return (
      <div className="rise mx-auto max-w-xl">
        <ErrorNote>{error}</ErrorNote>
        <span className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-brand text-brand-ink"><Compass size={26} /></span>
        <h1 className="font-display text-3xl font-extrabold text-ink">{info?.subject_title}: darajangizni aniqlang</h1>
        <p className="mb-5 mt-2 font-read text-lg text-ink-2">
          {info?.questions} ta savol, taxminan {Math.ceil((info?.questions || 16) * 0.75)} daqiqa. Natijaga ko'ra sizga mos kursni tavsiya qilamiz. Bilmagan savolni o'tkazib yuborsangiz ham bo'ladi.
        </p>
        {info?.result && (
          <p className="mb-4 rounded-xl border border-line bg-surface-2 px-4 py-2.5 text-sm text-ink-2">
            Oldingi natijangiz: <b>{info.result.level_label}</b> ({info.result.percent}%)
          </p>
        )}
        <div className="flex gap-2">
          <button onClick={start} disabled={busy} className="btn btn-primary">{busy ? 'Tayyorlanmoqda...' : 'Testni boshlash'}</button>
          <Link to="/" className="btn btn-ghost">Keyinroq</Link>
        </div>
      </div>
    )
  }

  // Savollar
  const q = questions[index]
  const last = index === questions.length - 1
  const answered = Object.keys(answers).length
  return (
    <div className="rise mx-auto max-w-2xl">
      <ErrorNote>{error}</ErrorNote>
      <div className="mb-4 flex items-center gap-3">
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-paper-2" role="progressbar" aria-valuenow={index + 1} aria-valuemax={questions.length}>
          <div className="h-full rounded-full bg-brand transition-all" style={{ width: `${((index + 1) / questions.length) * 100}%` }} />
        </div>
        <span className="text-sm font-semibold text-muted">{index + 1} / {questions.length}</span>
      </div>
      <section className="card p-5 sm:p-6">
        <h2 className="mb-4 font-read text-xl font-medium leading-snug text-ink">{q.question}</h2>
        <div className="flex flex-col gap-2" role="radiogroup" aria-label="Variantlar">
          {q.options.map((opt, i) => {
            const picked = answers[q.id] === i
            return (
              <button
                key={i} type="button" role="radio" aria-checked={picked}
                onClick={() => setAnswers((a) => ({ ...a, [q.id]: i }))}
                className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-left transition-colors ${picked ? 'border-brand bg-brand-soft text-ink' : 'border-line bg-surface hover:bg-paper-2'}`}
              >
                <span className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-sm font-bold ${picked ? 'bg-brand text-brand-ink' : 'bg-paper-2 text-ink-2'}`}>
                  {picked ? <Check size={15} /> : LETTERS[i]}
                </span>
                <span className="font-read text-base">{opt}</span>
              </button>
            )
          })}
        </div>
      </section>
      <div className="mt-4 flex items-center justify-between">
        <button onClick={() => setIndex((i) => Math.max(0, i - 1))} disabled={index === 0} className="btn btn-ghost btn-sm"><ArrowLeft size={14} /> Orqaga</button>
        {last ? (
          <button onClick={finish} disabled={busy || answered === 0} className="btn btn-primary">{busy ? 'Hisoblanmoqda...' : `Yakunlash (${answered}/${questions.length})`}</button>
        ) : (
          <button onClick={() => setIndex((i) => i + 1)} className="btn btn-primary btn-sm">
            {answers[q.id] === undefined ? "O'tkazib yuborish" : 'Keyingisi'} <ArrowRight size={14} />
          </button>
        )}
      </div>
    </div>
  )
}
