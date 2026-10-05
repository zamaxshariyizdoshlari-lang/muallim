import {
  BarChart3, BookOpen, ExternalLink, GraduationCap, LayoutDashboard, LogOut, Menu, Settings2, ShieldCheck, Users, X,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { sendHeartbeat } from '../../api/client'
import { ThemeToggle } from '../ui'

const NAV = [
  { group: 'Nazorat', items: [
    { to: '/boshqaruv', label: "Umumiy ko'rinish", icon: LayoutDashboard, end: true },
    { to: '/boshqaruv/talabalar', label: 'Talabalar', icon: Users, match: ['/boshqaruv/talabalar', '/boshqaruv/talaba/'] },
  ] },
  { group: 'Tahlil', items: [
    { to: '/boshqaruv/kurslar', label: 'Kurslar tahlili', icon: BarChart3, match: ['/boshqaruv/kurslar'] },
  ] },
  { group: 'Kontent', items: [
    { to: '/boshqaruv/kontent', label: 'Kurslarni tahrirlash', icon: Settings2, match: ['/boshqaruv/kontent'] },
  ] },
]

function NavList({ pathname }) {
  return (
    <nav aria-label="Admin menyusi" className="flex flex-col gap-5">
      {NAV.map((g) => (
        <div key={g.group}>
          <p className="mb-1.5 px-3 text-[0.68rem] font-bold uppercase tracking-widest text-chalk-ink/50">{g.group}</p>
          <div className="flex flex-col gap-0.5">
            {g.items.map(({ to, label, icon: Icon, end, match }) => {
              const active = end ? pathname === to : (match || [to]).some((m) => pathname.startsWith(m))
              return (
                <Link
                  key={to} to={to} aria-current={active ? 'page' : undefined}
                  className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-semibold transition-colors ${
                    active ? 'bg-white/12 text-white' : 'text-chalk-ink/70 hover:bg-white/8 hover:text-white'
                  }`}
                >
                  <Icon size={16} className="shrink-0" /> {label}
                </Link>
              )
            })}
          </div>
        </div>
      ))}
    </nav>
  )
}

/** Admin paneli: talaba ko'rinishidan alohida, qorong'i yon menyuli ish stoli. */
export default function AdminShell({ me, dark, onToggleTheme, onLogout }) {
  const [drawer, setDrawer] = useState(false)
  const { pathname } = useLocation()
  useEffect(() => { setDrawer(false) }, [pathname])
  useEffect(() => {
    const ping = () => { if (document.visibilityState === 'visible') sendHeartbeat().catch(() => {}) }
    ping()
    const id = setInterval(ping, 30000)
    return () => clearInterval(id)
  }, [])

  const side = (
    <div className="flex h-full flex-col">
      <Link to="/boshqaruv" className="mb-6 flex items-center gap-2.5 px-2">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/15 text-white"><ShieldCheck size={18} /></span>
        <span>
          <span className="block font-display text-lg font-bold leading-none text-white">Muallim</span>
          <span className="mt-1 inline-block rounded bg-gold px-1.5 py-px text-[0.62rem] font-extrabold uppercase tracking-widest text-white">Admin</span>
        </span>
      </Link>
      <NavList pathname={pathname} />
      <div className="mt-auto flex flex-col gap-1 border-t border-white/10 pt-4">
        <Link to="/" className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-semibold text-chalk-ink/70 hover:bg-white/8 hover:text-white">
          <GraduationCap size={16} /> Talaba ko'rinishi <ExternalLink size={12} className="ml-auto" />
        </Link>
        <button type="button" onClick={onLogout} className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-left text-sm font-semibold text-chalk-ink/70 hover:bg-white/8 hover:text-white">
          <LogOut size={16} /> Chiqish
        </button>
        <p className="px-3 pt-2 text-xs text-chalk-ink/50">@{me.username}</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen lg:flex">
      <aside className="sticky top-0 hidden h-screen w-64 shrink-0 overflow-y-auto bg-chalk p-4 lg:block">{side}</aside>

      <div className="min-w-0 flex-1">
        <header className="sticky top-0 z-30 flex items-center justify-between gap-3 border-b border-line bg-paper/90 px-4 py-2.5 backdrop-blur">
          <button type="button" onClick={() => setDrawer(true)} className="btn btn-ghost btn-sm !px-2 lg:hidden" aria-label="Menyuni ochish">
            <Menu size={18} />
          </button>
          <p className="flex items-center gap-2 text-sm font-semibold text-ink-2">
            <BookOpen size={15} className="text-brand" /> Boshqaruv paneli
          </p>
          <ThemeToggle dark={dark} onToggle={onToggleTheme} />
        </header>
        <main id="main-content" className="mx-auto w-full max-w-6xl px-4 pb-20 pt-6 sm:px-6">
          <Outlet context={{ me, isTeacher: true }} />
        </main>
      </div>

      {drawer && (
        <div className="fixed inset-0 z-40 lg:hidden" role="dialog" aria-modal="true" aria-label="Menyu">
          <button type="button" className="absolute inset-0 bg-black/50" onClick={() => setDrawer(false)} aria-label="Yopish" />
          <div className="rise absolute inset-y-0 left-0 w-72 max-w-[85vw] overflow-y-auto bg-chalk p-4 shadow-xl">
            <button type="button" onClick={() => setDrawer(false)} className="mb-2 ml-auto flex text-white" aria-label="Yopish"><X size={18} /></button>
            {side}
          </div>
        </div>
      )}
    </div>
  )
}
