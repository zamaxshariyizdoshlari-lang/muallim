import { useEffect, useState } from 'react'

const COLORS = ['var(--brand)', 'var(--gold)', 'var(--ok)', '#e879f9', '#38bdf8']

/** Tabriklash effekti: test/imtihon o'tilganda yoki sertifikat olinganda bir martalik
 * "konfetti" animatsiyasi. Ekranni bloklamaydi, ~2 soniyadan keyin o'zini tozalaydi. */
export default function Confetti() {
  const [pieces] = useState(() =>
    Array.from({ length: 46 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 0.3,
      duration: 1.6 + Math.random() * 0.9,
      size: 6 + Math.random() * 6,
      color: COLORS[i % COLORS.length],
      rotate: Math.random() * 360,
      drift: (Math.random() - 0.5) * 120,
    }))
  )
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const t = setTimeout(() => setVisible(false), 2600)
    return () => clearTimeout(t)
  }, [])

  const reduceMotion = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  if (!visible || reduceMotion) return null

  return (
    <div className="pointer-events-none fixed inset-0 z-[999] overflow-hidden" aria-hidden>
      {pieces.map((p) => (
        <span
          key={p.id}
          style={{
            position: 'absolute',
            top: '-5%',
            left: `${p.left}%`,
            width: p.size,
            height: p.size * 0.4,
            background: p.color,
            borderRadius: 2,
            opacity: 0.9,
            '--drift': `${p.drift}px`,
            '--rotate': `${p.rotate}deg`,
            animation: `confetti-fall ${p.duration}s ${p.delay}s ease-in forwards`,
          }}
        />
      ))}
    </div>
  )
}
