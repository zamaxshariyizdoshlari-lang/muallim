import { RotateCcw } from 'lucide-react'
import { useMemo, useState } from 'react'

function shuffle(array) {
  const copy = [...array]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

export default function TimelineGame({ items }) {
  const indexed = useMemo(
    () => items.map((item, originalIndex) => ({ ...item, originalIndex })),
    [items]
  )
  const [pool, setPool] = useState(() => shuffle(indexed))
  const [placed, setPlaced] = useState([])
  const [checked, setChecked] = useState(false)

  if (!items?.length) return <p className="text-sm text-muted">Voqealar topilmadi.</p>

  function pick(item) {
    if (checked) return
    setPool((p) => p.filter((x) => x.originalIndex !== item.originalIndex))
    setPlaced((p) => [...p, item])
  }

  function reset() {
    setPool(shuffle(indexed))
    setPlaced([])
    setChecked(false)
  }

  const correctCount = placed.filter((item, i) => item.originalIndex === i).length

  return (
    <div>
      <p className="mb-4 text-sm text-ink-2">
        Voqealarni sodir bo'lish tartibida bosing (birinchi bo'lgani birinchi).
      </p>

      {pool.length > 0 && (
        <div className="mb-5 flex flex-col gap-2">
          {pool.map((item) => (
            <button key={item.originalIndex} onClick={() => pick(item)} className="option">
              {item.label}
            </button>
          ))}
        </div>
      )}

      {placed.length > 0 && (
        <ol className="relative mb-5 ml-4 flex flex-col gap-2 border-l-2 border-dashed border-line-strong pl-6">
          {placed.map((item, i) => {
            const isCorrect = checked && item.originalIndex === i
            const isWrong = checked && item.originalIndex !== i
            return (
              <li key={item.originalIndex} className="relative">
                <span className="absolute -left-[2.35rem] top-2 flex h-7 w-7 items-center justify-center rounded-full border-2 border-gold bg-surface text-xs font-bold text-gold">
                  {i + 1}
                </span>
                <div className={`option !cursor-default ${isCorrect ? 'is-ok' : isWrong ? 'is-bad' : ''}`}>
                  <span className="pt-0.5">
                    {item.label}
                    {item.page && <span className="chip ml-2">bet {item.page}</span>}
                  </span>
                </div>
              </li>
            )
          })}
        </ol>
      )}

      <div className="flex flex-wrap items-center gap-3">
        {!checked && placed.length === items.length && (
          <button onClick={() => setChecked(true)} className="btn btn-primary">
            Tekshirish
          </button>
        )}
        {checked && <span className="chip chip-gold">To'g'ri: {correctCount} / {items.length}</span>}
        <button onClick={reset} className="btn btn-ghost btn-sm">
          <RotateCcw size={14} /> Qayta boshlash
        </button>
      </div>
    </div>
  )
}
