import { RotateCcw, Undo2 } from 'lucide-react'
import { useMemo, useState } from 'react'
import { ProgressBar } from './ui'

/** Gap mashqlari: ikki turi bo'ladi -
 *  - "choice": to'g'ri variantni tanlash (o'zbekcha so'rov -> turkcha javob yoki aksincha)
 *  - "order": so'zlarni to'g'ri tartibda bosib, gap tuzish (aralashtirilgan holda ko'rsatiladi)
 */
export default function SentencePractice({ items }) {
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [result, setResult] = useState(null) // true/false - joriy savol javobi

  if (!items?.length) return <p className="text-sm text-muted">Mashqlar topilmadi.</p>

  const item = items[index]
  const finished = index >= items.length

  function answered(correct) {
    setResult(correct)
    if (correct) setScore((s) => s + 1)
  }

  function next() {
    setResult(null)
    setIndex((i) => i + 1)
  }

  function reset() {
    setIndex(0)
    setScore(0)
    setResult(null)
  }

  if (finished) {
    return (
      <div className="rise py-4 text-center">
        <p className="eyebrow mb-1">Natija</p>
        <p className="font-display text-5xl font-extrabold text-brand">
          {score} <span className="text-muted">/ {items.length}</span>
        </p>
        <p className="mt-2 text-sm text-ink-2">
          {score === items.length ? "Ajoyib! Hammasi to'g'ri." : 'Yaxshi urinish! Yana bir bor sinab ko\'ring.'}
        </p>
        <button onClick={reset} className="btn btn-ghost mt-5">
          <RotateCcw size={14} /> Qaytadan boshlash
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <span className="chip">Mashq {index + 1} / {items.length}</span>
        <ProgressBar value={index} max={items.length} />
      </div>
      {item.type === 'order' ? (
        <OrderItem key={index} item={item} onAnswered={answered} result={result} />
      ) : (
        <ChoiceItem key={index} item={item} onAnswered={answered} result={result} />
      )}
      {result !== null && (
        <button onClick={next} className="btn btn-primary mt-5">
          {index + 1 === items.length ? 'Yakunlash' : 'Keyingi mashq'}
        </button>
      )}
    </div>
  )
}

function ChoiceItem({ item, onAnswered, result }) {
  const [selected, setSelected] = useState(null)

  function pick(i) {
    if (selected !== null) return
    setSelected(i)
    onAnswered(i === item.correct_index)
  }

  return (
    <div>
      <p className="mb-4 font-read text-lg font-medium leading-snug text-ink">{item.prompt}</p>
      <div className="flex flex-col gap-2">
        {item.options.map((opt, i) => {
          const isCorrect = selected !== null && i === item.correct_index
          const isWrongPick = selected === i && i !== item.correct_index
          return (
            <button
              key={i}
              onClick={() => pick(i)}
              disabled={selected !== null}
              className={`option ${isCorrect ? 'is-ok' : isWrongPick ? 'is-bad shake' : ''}`}
            >
              <span className="option-key">{String.fromCharCode(65 + i)}</span>
              <span className="pt-0.5">{opt}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

function OrderItem({ item, onAnswered }) {
  const shuffled = useMemo(() => {
    const arr = item.words.map((w, i) => ({ w, i }))
    for (let k = arr.length - 1; k > 0; k--) {
      const j = Math.floor(Math.random() * (k + 1))
      ;[arr[k], arr[j]] = [arr[j], arr[k]]
    }
    return arr
  }, [item])

  const [picked, setPicked] = useState([])
  const [checked, setChecked] = useState(false)
  const remaining = shuffled.filter((t) => !picked.some((p) => p.i === t.i))

  function pick(tok) {
    if (checked) return
    setPicked((p) => [...p, tok])
  }

  function undo() {
    if (checked) return
    setPicked((p) => p.slice(0, -1))
  }

  function check() {
    const ok = picked.every((t, idx) => t.i === idx) && picked.length === item.words.length
    setChecked(true)
    onAnswered(ok)
  }

  return (
    <div>
      {item.prompt && <p className="mb-3 text-sm text-muted">{item.prompt}</p>}
      <div
        className={`mb-4 flex min-h-14 flex-wrap items-center gap-2 rounded-xl border-2 border-dashed px-3 py-3 ${
          checked ? (picked.every((t, i) => t.i === i) ? 'border-ok bg-ok-soft' : 'border-bad bg-bad-soft') : 'border-line-strong'
        }`}
      >
        {picked.length === 0 && <span className="text-sm text-muted">So'zlarni pastdan tartib bilan bosing...</span>}
        {picked.map((t, i) => (
          <span key={i} className="chip chip-gold !text-sm">{t.w}</span>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {remaining.map((t) => (
          <button key={t.i} onClick={() => pick(t)} disabled={checked} className="option !w-auto px-4 py-2">
            {t.w}
          </button>
        ))}
      </div>
      {!checked && (
        <div className="mt-4 flex gap-2">
          <button onClick={undo} disabled={picked.length === 0} className="btn btn-ghost btn-sm">
            <Undo2 size={14} /> Ortga
          </button>
          <button onClick={check} disabled={picked.length !== item.words.length} className="btn btn-primary btn-sm">
            Tekshirish
          </button>
        </div>
      )}
      {checked && !picked.every((t, i) => t.i === i) && (
        <p className="mt-3 text-sm text-ink-2">To'g'ri javob: <b>{item.words.join(' ')}</b></p>
      )}
    </div>
  )
}
