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

  if (!pairs?.length) return <p className="text-sm text-muted">Juftliklar topilmadi.</p>

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
      <p className="mb-4 text-sm text-ink-2">
        Avval chap tomondan bittasini, keyin unga mos o'ng tomondagisini bosing.
      </p>

      <div className="mb-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="flex flex-col gap-2">
          {left.map((item) => (
            <button
              key={item.index}
              onClick={() => pickLeft(item.index)}
              disabled={matched.has(item.index)}
              className={`option ${matched.has(item.index) ? 'is-ok' : selectedLeft === item.index ? 'is-selected' : ''}`}
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
              className={`option ${matched.has(item.index) ? 'is-ok' : wrongPair === item.index ? 'is-bad shake' : ''}`}
            >
              {item.text}
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <span className="chip chip-gold">Topildi: {matched.size} / {pairs.length}</span>
        {matched.size === pairs.length && <span className="text-sm font-semibold text-ok">Barakalla! Hammasi topildi.</span>}
        <button onClick={reset} className="btn btn-ghost btn-sm">
          <RotateCcw size={14} /> Qayta boshlash
        </button>
      </div>
    </div>
  )
}
