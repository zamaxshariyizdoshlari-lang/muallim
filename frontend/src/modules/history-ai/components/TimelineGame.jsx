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

  if (!items?.length) return <p className="text-sm text-slate-500">Voqealar topilmadi.</p>

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
      <p className="mb-3 text-sm text-slate-600">
        Voqealarni sodir bo'lish tartibida bosing (birinchi bo'lgani birinchi).
      </p>

      {pool.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2">
          {pool.map((item) => (
            <button
              key={item.originalIndex}
              onClick={() => pick(item)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm text-slate-700 hover:border-indigo-400 hover:bg-indigo-50"
            >
              {item.label}
            </button>
          ))}
        </div>
      )}

      <ol className="mb-4 flex flex-col gap-2">
        {placed.map((item, i) => {
          const isCorrect = checked && item.originalIndex === i
          const isWrong = checked && item.originalIndex !== i
          return (
            <li
              key={item.originalIndex}
              className={`rounded-lg border px-3 py-2 text-sm ${
                isCorrect
                  ? 'border-green-300 bg-green-50 text-green-700'
                  : isWrong
                    ? 'border-red-300 bg-red-50 text-red-700'
                    : 'border-slate-200 bg-slate-50 text-slate-700'
              }`}
            >
              {i + 1}. {item.label}
              {item.page && <span className="ml-2 text-xs text-slate-400">bet {item.page}</span>}
            </li>
          )
        })}
      </ol>

      <div className="flex items-center gap-3">
        {!checked && placed.length === items.length && (
          <button
            onClick={() => setChecked(true)}
            className="rounded-lg bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
          >
            Tekshirish
          </button>
        )}
        {checked && (
          <p className="text-sm text-slate-600">
            To'g'ri: {correctCount} / {items.length}
          </p>
        )}
        <button
          onClick={reset}
          className="flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          <RotateCcw size={14} /> Qayta boshlash
        </button>
      </div>
    </div>
  )
}
