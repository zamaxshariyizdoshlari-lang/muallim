import { Check, Flame, Snowflake } from 'lucide-react'
import { ProgressRing } from './ui'

/** Kunlik maqsad (ball) va ketma-ketlik: bosh sahifa va profilda ko'rsatiladi. */
export default function DailyGoalCard({ daily, streak }) {
  const left = Math.max(0, daily.goal - daily.today)
  return (
    <section className="card flex flex-wrap items-center gap-5 p-5" aria-label="Kunlik maqsad">
      <div className="relative">
        <ProgressRing value={Math.min(daily.today, daily.goal)} max={daily.goal} size={72} />
        {daily.met && (
          <span className="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-ok text-white">
            <Check size={14} />
          </span>
        )}
      </div>
      <div className="min-w-0 flex-1">
        <p className="eyebrow mb-0.5">Kunlik maqsad</p>
        <p className="font-display text-xl font-bold text-ink">
          {daily.met ? 'Bugungi maqsad bajarildi!' : `Yana ${left} ball kerak`}
        </p>
        <p className="text-sm text-muted">
          {daily.today} / {daily.goal} ball · mavzu testini topshiring yoki xatolarni takrorlang
        </p>
      </div>
      <div className="flex gap-2">
        <span className={`chip ${streak.current > 0 ? 'chip-gold' : ''}`} title="Ketma-ket faol kunlar">
          <Flame size={13} /> {streak.current} kun
        </span>
        {streak.freezes > 0 && (
          <span className="chip" title="Bitta o'tkazilgan kunni kechiradi: har 7 faol kunda 1 ta beriladi">
            <Snowflake size={13} /> {streak.freezes}
          </span>
        )}
      </div>
    </section>
  )
}
