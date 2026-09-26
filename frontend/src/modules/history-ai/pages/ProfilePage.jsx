import { Award, BookOpen, Flag, Flame, Footprints, Library, Lock, Target, Trophy, Zap } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getProfile } from '../api/client'
import { ErrorNote, ProgressBar, Spinner } from '../components/ui'

const BADGE_ICONS = {
  footprints: Footprints, 'book-open': BookOpen, library: Library, target: Target, flag: Flag,
  flame: Flame, zap: Zap, award: Award,
}

export default function ProfilePage({ me }) {
  const [p, setP] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getProfile().then(setP).catch((err) => setError(err.message))
  }, [])

  if (error) return <ErrorNote>{error}</ErrorNote>
  if (!p) return <Spinner>Profil yuklanmoqda...</Spinner>

  const earned = p.badges.filter((b) => b.earned).length
  const name = me.first_name || me.username

  return (
    <div className="rise mx-auto max-w-3xl">
      {/* Daraja kartasi */}
      <section className="card relative mb-6 overflow-hidden p-6 sm:p-8">
        <div className="pointer-events-none absolute -right-10 -top-10 h-44 w-44 rounded-full bg-gold/10" aria-hidden />
        <div className="relative flex flex-wrap items-center gap-6">
          <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-brand font-display text-3xl font-extrabold text-brand-ink shadow">
            {name.slice(0, 1).toUpperCase()}
          </div>
          <div className="min-w-0 flex-1">
            <p className="eyebrow mb-1">{p.level}-daraja</p>
            <h1 className="font-display text-3xl font-extrabold text-ink">{name}</h1>
            <p className="mt-1 text-sm font-semibold text-brand">{p.title}</p>
            <ProgressBar value={p.xp_in_level} max={p.xp_for_next} className="mt-4" />
            <p className="mt-1.5 text-xs text-muted">
              {p.xp_in_level} / {p.xp_for_next} XP — keyingi darajagacha
            </p>
          </div>
        </div>
      </section>

      {/* Raqamlar */}
      <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Stat icon={Trophy} label="Jami XP" value={p.xp} />
        <Stat icon={Flame} label="Joriy ketma-ketlik" value={`${p.streak.current} kun`} hot={p.streak.current > 0} />
        <Stat icon={Zap} label="Eng uzun" value={`${p.streak.best} kun`} />
        <Stat icon={BookOpen} label="O'zlashtirilgan mavzu" value={p.stats.topics_done} />
      </div>

      {!p.streak.active_today && (
        <p className="mb-8 rounded-xl border border-gold/40 bg-gold-soft px-4 py-3 text-sm text-ink-2">
          <Flame size={15} className="mr-1.5 inline text-gold" />
          Bugun hali o'qimadingiz. Ketma-ketlikni saqlash uchun bitta test topshiring!
        </p>
      )}

      {/* Nishonlar */}
      <div className="mb-4 flex items-end justify-between">
        <h2 className="font-display text-2xl font-bold text-ink">Nishonlar</h2>
        <span className="chip chip-gold">{earned} / {p.badges.length}</span>
      </div>
      <ul className="grid gap-4 sm:grid-cols-2">
        {p.badges.map((b) => {
          const Icon = BADGE_ICONS[b.icon] || Award
          return (
            <li key={b.key} className={`card flex items-center gap-4 p-4 ${b.earned ? '' : 'opacity-60'}`}>
              <span
                className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl ${
                  b.earned ? 'bg-gold text-[#241a08]' : 'bg-paper-2 text-muted'
                }`}
              >
                {b.earned ? <Icon size={22} /> : <Lock size={18} />}
              </span>
              <div className="min-w-0">
                <p className="font-display text-base font-bold text-ink">{b.title}</p>
                <p className="text-xs leading-relaxed text-muted">{b.description}</p>
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}

function Stat({ icon: Icon, label, value, hot }) {
  return (
    <div className="card p-4">
      <Icon size={18} className={hot ? 'text-brand' : 'text-gold'} />
      <p className="mt-2 font-display text-2xl font-extrabold text-ink">{value}</p>
      <p className="text-xs text-muted">{label}</p>
    </div>
  )
}
