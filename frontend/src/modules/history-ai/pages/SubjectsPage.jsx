import { ArrowRight, BookOpen, Flame, Landmark, Languages, Play, RotateCcw, Star, Trophy } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDashboard, getLeaderboard, getProfile, listSubjects } from '../api/client'
import DailyGoalCard from '../components/DailyGoalCard'
import { ErrorNote, Spinner } from '../components/ui'

const ICONS = { landmark: Landmark, languages: Languages, book: BookOpen }

const greeting = () => {
  const h = new Date().getHours()
  return h < 6 ? 'Xayrli tun' : h < 12 ? 'Xayrli tong' : h < 18 ? 'Xayrli kun' : 'Xayrli kech'
}

function Stat({ icon: Icon, tone, value, label }) {
  return (
    <div className="card flex items-center gap-3 p-4">
      <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${tone}`}><Icon size={19} /></span>
      <div className="min-w-0">
        <p className="font-display text-xl font-extrabold leading-none text-ink">{value}</p>
        <p className="mt-1 truncate text-xs text-muted">{label}</p>
      </div>
    </div>
  )
}

function CourseRow({ c }) {
  return (
    <Link to={`/kurs/${c.id}`} className="card card-hover flex flex-col gap-3 p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted">{c.subject}</p>
          <h3 className="font-display text-base font-bold leading-snug text-ink">{c.title}</h3>
        </div>
        <span className={`chip shrink-0 ${c.percent === 100 ? '!border-ok/40 !bg-ok-soft !text-ok' : ''}`}>{c.percent}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-paper-2" role="progressbar" aria-valuenow={c.percent} aria-valuemin={0} aria-valuemax={100}>
        <div className={`h-full rounded-full ${c.percent === 100 ? 'bg-ok' : 'bg-brand'}`} style={{ width: `${c.percent}%` }} />
      </div>
      <div className="flex items-center justify-between text-xs text-muted">
        <span>{c.topics_done} / {c.topics_total} mavzu</span>
        {c.due_reviews > 0 && <span className="font-semibold text-gold">{c.due_reviews} ta takrorlash</span>}
      </div>
    </Link>
  )
}

export default function SubjectsPage({ me, onOpenSubject }) {
  const [subjects, setSubjects] = useState(null)
  const [dash, setDash] = useState(null)
  const [prof, setProf] = useState(null)
  const [board, setBoard] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    listSubjects().then(setSubjects).catch((err) => setError(err.message))
    getDashboard().then(setDash).catch(() => {})
    getProfile().then(setProf).catch(() => {})
    getLeaderboard().then(setBoard).catch(() => {})
  }, [])

  const name = me?.first_name || me?.username
  const mine = dash?.courses.filter((c) => c.started) || []
  const cont = dash?.continue
  const lvlPct = prof ? Math.round((prof.xp_in_level / prof.xp_for_next) * 100) : 0

  return (
    <div className="rise">
      <header className="mb-6">
        <p className="eyebrow mb-1">{greeting()}{name ? `, ${name}` : ''}</p>
        <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">
          {cont ? 'Davom etamizmi?' : "Bugun nimani o'rganamiz?"}
        </h1>
      </header>

      <ErrorNote>{error}</ErrorNote>

      {/* Davom etish: eng muhim harakat birinchi o'rinda */}
      {cont && (
        <Link
          to={`/kurs/${cont.book_id}/mavzu/${cont.topic.id}`}
          className="group relative mb-5 flex flex-wrap items-center gap-5 overflow-hidden rounded-2xl bg-gradient-to-br from-chalk to-brand-hover/70 p-6 ring-1 ring-brand/40 text-chalk-ink shadow-lg transition-transform hover:-translate-y-0.5"
        >
          <div className="pointer-events-none absolute -right-10 -top-10 h-44 w-44 rounded-full bg-white/5" aria-hidden />
          <span className="hidden h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-white/15 sm:flex"><Play size={26} className="ml-0.5" /></span>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-widest text-chalk-ink/60">{cont.book_title} · {cont.percent}%</p>
            <p className="mt-1 font-display text-xl font-bold leading-snug sm:text-2xl">{cont.topic.title}</p>
          </div>
          <span className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 sm:w-auto text-sm font-bold text-chalk">
            Davom etish <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
          </span>
        </Link>
      )}

      {dash?.due_reviews_total > 0 && (
        <Link
          to={`/kurs/${dash.due_book_id}/takrorlash`}
          className="mb-5 flex items-center gap-3 rounded-2xl border border-gold/40 bg-gold-soft px-5 py-3 text-ink hover:brightness-95"
        >
          <RotateCcw size={18} className="text-gold" />
          <span className="flex-1 text-sm font-semibold">Bugun takrorlash uchun {dash.due_reviews_total} ta savol sizni kutmoqda</span>
          <ArrowRight size={16} className="text-gold" />
        </Link>
      )}

      {prof && (
        <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
          <Stat icon={Flame} tone="bg-gold-soft text-gold" value={`${prof.streak.current} kun`} label="Ketma-ket faol kunlar" />
          <Stat icon={Star} tone="bg-brand-soft text-brand" value={prof.xp} label={`${prof.level}-daraja · ${prof.title}`} />
          <Stat icon={Trophy} tone="bg-ok-soft text-ok" value={prof.stats.topics_done} label="Tugatilgan mavzu" />
          <div className="card flex flex-col justify-center p-4">
            <div className="mb-1.5 flex justify-between text-xs text-muted"><span>Keyingi darajagacha</span><span>{lvlPct}%</span></div>
            <div className="h-2 overflow-hidden rounded-full bg-paper-2"><div className="h-full rounded-full bg-brand" style={{ width: `${lvlPct}%` }} /></div>
          </div>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          {prof && <DailyGoalCard daily={prof.daily} streak={prof.streak} />}

          {dash && mine.length > 0 && (
            <section aria-labelledby="mine-h">
              <h2 id="mine-h" className="mb-3 font-display text-xl font-bold text-ink">Mening kurslarim</h2>
              <div className="grid gap-3 sm:grid-cols-2">{mine.map((c) => <CourseRow key={c.id} c={c} />)}</div>
            </section>
          )}

          <section aria-labelledby="subj-h">
            <h2 id="subj-h" className="mb-3 font-display text-xl font-bold text-ink">{mine.length ? 'Barcha fanlar' : 'Fanni tanlang'}</h2>
            {!subjects ? <Spinner>Yuklanmoqda...</Spinner> : (
              <div className="grid gap-3 sm:grid-cols-2">
                {subjects.map((s) => {
                  const Icon = ICONS[s.icon] || BookOpen
                  return (
                    <button key={s.id} onClick={() => onOpenSubject(s)} className="card card-hover group flex items-center gap-4 p-4 text-left">
                      <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand text-brand-ink"><Icon size={22} /></span>
                      <span className="min-w-0 flex-1">
                        <span className="block font-display text-lg font-bold text-ink">{s.title}</span>
                        <span className="block text-xs text-muted">{s.book_count} ta kurs</span>
                      </span>
                      <ArrowRight size={18} className="text-gold transition-transform group-hover:translate-x-1" />
                    </button>
                  )
                })}
              </div>
            )}
          </section>
        </div>

        <aside className="space-y-6">
          {board && board.opted_in && (
            <section className="card p-5" aria-labelledby="lb-h">
              <h2 id="lb-h" className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
                <Trophy size={17} className="text-gold" /> Haftalik reyting
              </h2>
              {board.top.length === 0 ? (
                <p className="text-sm text-muted">Bu hafta hali ball to'plagan yo'q. Birinchi bo'ling!</p>
              ) : (
                <ol className="flex flex-col gap-1">
                  {board.top.slice(0, 5).map((r) => (
                    <li key={r.rank} className={`flex items-center gap-3 rounded-lg px-2 py-1.5 text-sm ${r.me ? 'bg-brand-soft font-bold text-brand' : 'text-ink-2'}`}>
                      <span className="w-5 text-center font-extrabold">{r.rank}</span>
                      <span className="min-w-0 flex-1 truncate">{r.me ? 'Siz' : r.name}</span>
                      <span className="tabular-nums">{r.points}</span>
                    </li>
                  ))}
                </ol>
              )}
              {board.me && board.me.rank > 5 && (
                <p className="mt-2 border-t border-line pt-2 text-sm text-ink-2">Sizning o'rningiz: <b>{board.me.rank}</b> · {board.me.points} ball</p>
              )}
            </section>
          )}
          <section className="card p-5 text-sm text-ink-2">
            <p className="mb-1 font-display text-base font-bold text-ink">Maslahat</p>
            Har kuni 10–15 daqiqa o'qish haftada bir marta uzoq o'tirishdan samaraliroq: xatolarni takrorlash bo'limi shuning uchun bor.
          </section>
        </aside>
      </div>
    </div>
  )
}
