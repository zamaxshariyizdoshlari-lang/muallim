import { ChevronLeft, Loader2, Moon, Sun } from 'lucide-react'
import { useEffect, useState } from 'react'

const THEME_KEY = 'tarixchi_theme'

export function useTheme() {
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'))

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    try {
      localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light')
    } catch {
      /* localStorage mavjud emas */
    }
  }, [dark])

  return [dark, () => setDark((d) => !d)]
}

export function ThemeToggle({ dark, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={dark ? 'Yorug\' rejim' : 'Qorong\'i rejim'}
      title={dark ? 'Yorug\' rejim' : 'Qorong\'i rejim'}
      className="btn btn-ghost btn-sm !px-2.5"
    >
      {dark ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  )
}

export function BackLink({ onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="mb-5 inline-flex items-center gap-1 text-sm font-medium text-muted transition-colors hover:text-brand"
    >
      <ChevronLeft size={16} /> {children}
    </button>
  )
}

export function Spinner({ children }) {
  return (
    <div className="card flex items-center gap-3 px-5 py-6 text-sm text-ink-2">
      <Loader2 className="animate-spin text-gold" size={20} />
      {children}
    </div>
  )
}

export function PageTag({ page }) {
  if (page === undefined || page === null) return null
  return <span className="chip ml-2 align-middle">bet {page}</span>
}

export function ProgressBar({ value, max, className = '' }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0
  return (
    <div
      className={`h-2 w-full overflow-hidden rounded-full bg-line ${className}`}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
    >
      <div
        className="h-full rounded-full bg-gradient-to-r from-gold to-brand transition-all duration-700"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

export function ProgressRing({ value, max, size = 76 }) {
  const stroke = 7
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const pct = max > 0 ? value / max : 0
  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--line)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--gold)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - pct)}
          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center font-display text-lg font-bold text-ink">
        {Math.round(pct * 100)}%
      </div>
    </div>
  )
}

export function ErrorNote({ children }) {
  if (!children) return null
  return (
    <p className="mb-4 rounded-xl border border-bad/40 bg-bad-soft px-4 py-2.5 text-sm text-bad">{children}</p>
  )
}

export function SectionTitle({ eyebrow, children, right }) {
  return (
    <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
      <div>
        {eyebrow && <p className="eyebrow mb-1">{eyebrow}</p>}
        <h2 className="font-display text-2xl font-bold text-ink">{children}</h2>
      </div>
      {right}
    </div>
  )
}

const UZ_MONTHS = [
  'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
  'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr',
]

/** Ba'zi brauzerlarda `toLocaleDateString('uz-UZ', {month:'long'})` oy nomini bilmaydi (ICU
 * ma'lumoti yo'q) - shuning uchun sanani o'zimiz, ishonchli formatlaymiz: "27 sentabr 2026". */
export function formatDateUz(value) {
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return ''
  return `${d.getDate()} ${UZ_MONTHS[d.getMonth()]} ${d.getFullYear()}`
}
