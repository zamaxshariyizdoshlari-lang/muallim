import { ArrowDownRight, ArrowUpRight, Minus } from 'lucide-react'
import { useState } from 'react'

const fmtDay = (iso) => {
  const d = new Date(iso)
  return `${d.getDate()}.${String(d.getMonth() + 1).padStart(2, '0')}`
}

/** O'zgarish (%) belgisi: o'sish yashil, pasayish qizil. `inverse` - pasayish yaxshi bo'lgan ko'rsatkichlar uchun. */
export function Delta({ value }) {
  if (value === null || value === undefined) return <span className="text-xs text-muted">—</span>
  const Icon = value > 0 ? ArrowUpRight : value < 0 ? ArrowDownRight : Minus
  const tone = value > 0 ? 'text-ok' : value < 0 ? 'text-bad' : 'text-muted'
  return (
    <span className={`inline-flex items-center gap-0.5 text-xs font-semibold ${tone}`} title="Oldingi 7 kunga nisbatan">
      <Icon size={13} /> {Math.abs(value)}%
    </span>
  )
}

/** Kichik chiziqli grafik (KPI kartalar ichida). */
export function Sparkline({ data, className = 'text-brand', height = 36 }) {
  const w = 120
  const max = Math.max(1, ...data.map((p) => p.value))
  const step = w / Math.max(1, data.length - 1)
  const pts = data.map((p, i) => [i * step, height - 3 - (p.value / max) * (height - 8)])
  const line = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ')
  return (
    <svg viewBox={`0 0 ${w} ${height}`} className={`h-9 w-full ${className}`} preserveAspectRatio="none" aria-hidden="true">
      <path d={`${line} L${w} ${height} L0 ${height} Z`} fill="currentColor" opacity="0.12" />
      <path d={line} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
    </svg>
  )
}

/**
 * Ustunli grafik: kunlik qiymatlar. `overlay` berilsa (masalan, o'tganlar) shu qiymat ustunning
 * ichida to'q rangda chiziladi. Ustiga sichqoncha olib borilganda aniq qiymat ko'rinadi.
 */
export function BarChart({ data, overlay, label = 'ta', height = 160, tone = 'bg-brand' }) {
  const [hover, setHover] = useState(null)
  const max = Math.max(1, ...data.map((p) => p.value))
  const tick = Math.max(1, Math.ceil(data.length / 6))
  const cur = hover === null ? null : data[hover]
  return (
    <div>
      <p className="mb-2 h-5 text-xs text-muted" aria-live="polite">
        {cur ? (
          <>
            <b className="text-ink">{fmtDay(cur.date)}</b>: {cur.value} {label}
            {overlay ? ` (o'tgan: ${overlay[hover].value})` : ''}
          </>
        ) : (
          `Oxirgi ${data.length} kun`
        )}
      </p>
      <div className="flex items-end gap-[3px]" style={{ height }} role="img" aria-label={`Kunlik grafik, oxirgi ${data.length} kun`}>
        {data.map((p, i) => (
          <div
            key={p.date}
            className="relative flex h-full flex-1 items-end"
            onMouseEnter={() => setHover(i)}
            onMouseLeave={() => setHover(null)}
          >
            <div
              className={`w-full rounded-t ${tone} ${hover === i ? 'opacity-100' : 'opacity-75'} transition-opacity`}
              style={{ height: `${Math.max(p.value ? 3 : 1, (p.value / max) * 100)}%` }}
            >
              {overlay && overlay[i].value > 0 && (
                <div className="absolute bottom-0 w-full rounded-t bg-ok" style={{ height: `${(overlay[i].value / max) * 100}%` }} />
              )}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-1 flex gap-[3px] text-[0.65rem] text-muted">
        {data.map((p, i) => (
          <span key={p.date} className="flex-1 overflow-visible whitespace-nowrap">{i % tick === 0 ? fmtDay(p.date) : ''}</span>
        ))}
      </div>
    </div>
  )
}

/** Gorizontal progress chizig'i, foiz yozuvi bilan. */
export function Meter({ value, tone = 'bg-brand', className = '' }) {
  const v = Math.max(0, Math.min(100, value ?? 0))
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="h-2 flex-1 overflow-hidden rounded-full bg-paper-2">
        <div className={`h-full rounded-full ${tone}`} style={{ width: `${v}%` }} />
      </div>
      <span className="w-9 text-right text-xs font-semibold tabular-nums text-ink-2">{value === null || value === undefined ? '—' : `${v}%`}</span>
    </div>
  )
}

/** Foiz bo'yicha rang: past - qizil, o'rta - sariq, yuqori - yashil. */
export const toneFor = (v) => (v === null || v === undefined ? 'bg-line-strong' : v >= 75 ? 'bg-ok' : v >= 50 ? 'bg-gold' : 'bg-bad')
