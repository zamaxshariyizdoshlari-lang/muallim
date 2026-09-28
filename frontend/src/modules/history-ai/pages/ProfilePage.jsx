import { Award, BookOpen, Diamond, Flag, Flame, Footprints, Gem, Library, Lock, Medal, Target, Trophy, Zap } from 'lucide-react'
import { useEffect, useState } from 'react'
import { changePassword, getLeaderboard, getMe, getProfile, updateMe } from '../api/client'
import DailyGoalCard from '../components/DailyGoalCard'
import { ErrorNote, ProgressBar, Spinner } from '../components/ui'

const BADGE_ICONS = {
  footprints: Footprints, 'book-open': BookOpen, library: Library, target: Target, flag: Flag,
  flame: Flame, zap: Zap, award: Award,
}

const LEAGUE_ICONS = { award: Award, medal: Medal, trophy: Trophy, gem: Gem, diamond: Diamond }
const LEAGUE_COLORS = {
  bronze: '!text-[#b08d57]', silver: '!text-slate-400', gold: '!text-gold',
  platinum: '!text-cyan-500', diamond: '!text-brand',
}

export default function ProfilePage({ me }) {
  const [account, setAccount] = useState({
    first_name: me.first_name || '', email: me.email || '', email_reminders: me.email_reminders !== false,
  })
  const [accMsg, setAccMsg] = useState(null)
  const [pw, setPw] = useState({ old: '', next: '' })
  const [pwMsg, setPwMsg] = useState(null)

  useEffect(() => {
    getMe()
      .then((m) => setAccount({ first_name: m.first_name || '', email: m.email || '', email_reminders: m.email_reminders !== false }))
      .catch(() => {})
  }, [])

  async function saveAccount(e) {
    e.preventDefault()
    setAccMsg(null)
    try {
      await updateMe(account)
      setAccMsg({ ok: true, text: 'Saqlandi.' })
    } catch (err) {
      setAccMsg({ text: err.message })
    }
  }

  async function savePassword(e) {
    e.preventDefault()
    setPwMsg(null)
    try {
      await changePassword(pw.old, pw.next)
      setPw({ old: '', next: '' })
      setPwMsg({ ok: true, text: 'Parol yangilandi.' })
    } catch (err) {
      setPwMsg({ text: err.message })
    }
  }

  const [p, setP] = useState(null)
  const [board, setBoard] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getProfile().then(setP).catch((err) => setError(err.message))
    getLeaderboard().then(setBoard).catch(() => {})
  }, [])

  async function changeSetting(patch) {
    try {
      await updateMe(patch)
      const [np, nb] = await Promise.all([getProfile(), getLeaderboard()])
      setP(np)
      setBoard(nb)
    } catch (err) {
      setError(err.message)
    }
  }

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
            <div className="mt-1 flex flex-wrap items-center gap-3">
              <p className="text-sm font-semibold text-brand">{p.title}</p>
              {p.league && (() => {
                const LeagueIcon = LEAGUE_ICONS[p.league.icon] || Award
                return (
                  <span className={`chip ${LEAGUE_COLORS[p.league.key] || 'text-ink-2'}`}>
                    <LeagueIcon size={14} /> {p.league.title} ligasi
                  </span>
                )
              })()}
            </div>
            {p.league?.next_title && (
              <p className="mt-1 text-xs text-muted">
                {p.league.xp_to_next} ball qoldi - {p.league.next_title} ligasiga o'tasiz
              </p>
            )}
            <ProgressBar value={p.xp_in_level} max={p.xp_for_next} className="mt-4" />
            <p className="mt-1.5 text-xs text-muted">
              {p.xp_in_level} / {p.xp_for_next} ball — keyingi darajagacha
            </p>
          </div>
        </div>
      </section>

      {/* Raqamlar */}
      <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Stat icon={Trophy} label="Jami ball" value={p.xp} />
        <Stat icon={Flame} label="Joriy ketma-ketlik" value={`${p.streak.current} kun`} hot={p.streak.current > 0} />
        <Stat icon={Zap} label="Eng uzun" value={`${p.streak.best} kun`} />
        <Stat icon={BookOpen} label="O'zlashtirilgan mavzu" value={p.stats.topics_done} />
      </div>

      <div className="mb-8">
        <DailyGoalCard daily={p.daily} streak={p.streak} />
        <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-muted">
          Kunlik maqsad:
          {[20, 50, 100].map((g) => (
            <button
              key={g}
              onClick={() => changeSetting({ daily_goal: g })}
              aria-pressed={p.daily.goal === g}
              className={`chip cursor-pointer ${p.daily.goal === g ? 'chip-gold' : ''}`}
            >
              {g} ball
            </button>
          ))}
        </div>
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
                  b.earned ? 'bg-gold text-white' : 'bg-paper-2 text-muted'
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

      {/* Haftalik reyting */}
      {board && (
        <section className="mt-12" aria-label="Haftalik reyting">
          <div className="mb-4 flex items-end justify-between gap-3">
            <div>
              <h2 className="font-display text-2xl font-bold text-ink">
                Haftalik reyting {board.league && <span className="text-muted">- {board.league.title} ligasi</span>}
              </h2>
              <p className="text-sm text-muted">
                Shu hafta (dushanbadan) to'plangan ball bo'yicha, o'zingiz bilan bir xil ligadagilar orasida
              </p>
            </div>
            <label className="flex cursor-pointer items-center gap-2 text-xs text-muted">
              <input
                type="checkbox"
                checked={board.opted_in}
                onChange={(e) => changeSetting({ show_in_leaderboard: e.target.checked })}
              />
              Reytingda ko'rinish
            </label>
          </div>
          {board.top.length === 0 ? (
            <p className="card p-6 text-sm text-muted">Bu hafta hali hech kim ball to'plamagan. Birinchi bo'ling!</p>
          ) : (
            <ol className="card divide-y divide-line overflow-hidden">
              {board.top.map((r) => (
                <li key={r.rank} className={`flex items-center gap-4 px-4 py-3 ${r.me ? 'bg-brand-soft' : ''}`}>
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-paper-2 text-sm font-bold text-ink-2">
                    {r.rank <= 3 ? <Medal size={16} className="text-gold" /> : r.rank}
                  </span>
                  <span className="min-w-0 flex-1 truncate font-semibold text-ink">
                    {r.name} {r.me && <span className="chip chip-gold ml-1">siz</span>}
                  </span>
                  <span className="font-display font-bold text-ink">{r.points} ball</span>
                </li>
              ))}
            </ol>
          )}
          {board.me && board.me.rank > board.top.length && (
            <p className="mt-2 text-sm text-muted">Sizning o'rningiz: {board.me.rank} ({board.me.points} ball)</p>
          )}
        </section>
      )}

      {/* Hisob sozlamalari */}
      <h2 className="mb-4 mt-12 font-display text-2xl font-bold text-ink">Hisob sozlamalari</h2>
      <div className="grid gap-5 sm:grid-cols-2">
        <form onSubmit={saveAccount} className="card p-5">
          <h3 className="mb-4 font-display text-lg font-bold text-ink">Shaxsiy ma'lumot</h3>
          <label className="mb-3 block text-sm font-medium text-ink-2">
            Ism
            <input className="field mt-1.5" value={account.first_name} maxLength={60}
              onChange={(e) => setAccount((a) => ({ ...a, first_name: e.target.value }))} />
          </label>
          <label className="mb-4 block text-sm font-medium text-ink-2">
            Elektron pochta <span className="font-normal text-muted">(parolni tiklash uchun)</span>
            <input type="email" className="field mt-1.5" value={account.email}
              onChange={(e) => setAccount((a) => ({ ...a, email: e.target.value }))} />
          </label>
          <label className="mb-4 flex cursor-pointer items-center gap-2 text-sm text-ink-2">
            <input
              type="checkbox"
              checked={account.email_reminders}
              onChange={(e) => setAccount((a) => ({ ...a, email_reminders: e.target.checked }))}
            />
            Streak uzilishi arafasida eslatma email yuborilsin
          </label>
          {accMsg && <p className={`mb-3 text-sm ${accMsg.ok ? 'text-ok' : 'text-bad'}`}>{accMsg.text}</p>}
          <button className="btn btn-primary btn-sm">Saqlash</button>
        </form>

        <form onSubmit={savePassword} className="card p-5">
          <h3 className="mb-4 font-display text-lg font-bold text-ink">Parolni o'zgartirish</h3>
          <label className="mb-3 block text-sm font-medium text-ink-2">
            Joriy parol
            <input type="password" className="field mt-1.5" value={pw.old} autoComplete="current-password" required
              onChange={(e) => setPw((v) => ({ ...v, old: e.target.value }))} />
          </label>
          <label className="mb-4 block text-sm font-medium text-ink-2">
            Yangi parol
            <input type="password" className="field mt-1.5" value={pw.next} autoComplete="new-password" required
              onChange={(e) => setPw((v) => ({ ...v, next: e.target.value }))} />
          </label>
          {pwMsg && <p className={`mb-3 text-sm ${pwMsg.ok ? 'text-ok' : 'text-bad'}`}>{pwMsg.text}</p>}
          <button className="btn btn-primary btn-sm">Yangilash</button>
        </form>
      </div>
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
