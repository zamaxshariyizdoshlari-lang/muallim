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

export default function MatchingGame({ pairs }) {
  const left = useMemo(() => pairs.map((p, i) => ({ text: p.left, index: i })), [pairs])
  const rightShuffled = useMemo(
    () => shuffle(pairs.map((p, i) => ({ text: p.right, index: i }))),
    [pairs]
  )

  const [selectedLeft, setSelectedLeft] = useState(null)
  const [matched, setMatched] = useState(() => new Set())
  const [wrongPair, setWrongPair] = useState(null)

  if (!pairs?.length) return <p className="text-sm text-slate-500">Juftliklar topilmadi.</p>

  function pickLeft(index) {
    if (matched.has(index)) return
    setSelectedLeft(index)
    setWrongPair(null)
  }

  function pickRight(rightIndex) {
    if (selectedLeft === null || matched.has(rightIndex)) return
    if (rightIndex === selectedLeft) {
      setMatched((m) => new Set(m).add(rightIndex))
      setSelectedLeft(null)
    } else {
      setWrongPair(rightIndex)
      setTimeout(() => setWrongPair(null), 500)
      setSelectedLeft(null)
    }
  }

  function reset() {
    setSelectedLeft(null)
    setMatched(new Set())
    setWrongPair(null)
  }

  return (
    <div>
      <p className="mb-3 text-sm text-slate-600">
        Chap tomondan bittasini, keyin unga mos o'ng tomondagisini bosing.
      </p>

      <div className="mb-4 grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-2">
          {left.map((item) => (
            <button
              key={item.index}
              onClick={() => pickLeft(item.index)}
              disabled={matched.has(item.index)}
              className={`rounded-lg border px-3 py-2 text-left text-sm ${
                matched.has(item.index)
                  ? 'border-green-300 bg-green-50 text-green-700'
                  : selectedLeft === item.index
                    ? 'border-indigo-400 bg-indigo-50 text-indigo-700'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-indigo-300'
              }`}
            >
              {item.text}
            </button>
          ))}
        </div>

        <div className="flex flex-col gap-2">
          {rightShuffled.map((item) => (
            <button
              key={item.index}
              onClick={() => pickRight(item.index)}
              disabled={matched.has(item.index)}
              className={`rounded-lg border px-3 py-2 text-left text-sm ${
                matched.has(item.index)
                  ? 'border-green-300 bg-green-50 text-green-700'
                  : wrongPair === item.index
                    ? 'border-red-300 bg-red-50 text-red-700'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-indigo-300'
              }`}
            >
              {item.text}
            </button>
          ))}
        </div>
      </div>

      <div className="flex items-center gap-3">
        <p className="text-sm text-slate-600">
          Topildi: {matched.size} / {pairs.length}
        </p>
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
