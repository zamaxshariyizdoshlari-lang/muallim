import { RotateCcw } from 'lucide-react'
import { useState } from 'react'
import { ProgressBar } from './ui'

export default function QuizGame({ questions }) {
  const [index, setIndex] = useState(0)
  const [selected, setSelected] = useState(null)
  const [score, setScore] = useState(0)

  if (!questions?.length) return <p className="text-sm text-muted">Savollar topilmadi.</p>

  const question = questions[index]
  const finished = index >= questions.length

  function pick(optionIndex) {
    if (selected !== null) return
    setSelected(optionIndex)
    if (optionIndex === question.correct_index) setScore((s) => s + 1)
  }

  function next() {
    setSelected(null)
    setIndex((i) => i + 1)
  }

  function reset() {
    setIndex(0)
    setSelected(null)
    setScore(0)
  }

  if (finished) {
    return (
      <div className="rise py-4 text-center">
        <p className="eyebrow mb-1">Natija</p>
        <p className="font-display text-5xl font-extrabold text-brand">
          {score} <span className="text-muted">/ {questions.length}</span>
        </p>
        <p className="mt-2 text-sm text-ink-2">
          {score === questions.length ? "Ajoyib! Hammasi to'g'ri." : "Yaxshi urinish! Yana bir bor sinab ko'ring."}
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
        <span className="chip">Savol {index + 1} / {questions.length}</span>
        <ProgressBar value={index} max={questions.length} />
      </div>
      <p className="mb-4 font-read text-lg font-medium leading-snug text-ink">{question.question}</p>

      <div className="flex flex-col gap-2">
        {question.options?.map((opt, i) => {
          const isCorrect = selected !== null && i === question.correct_index
          const isWrongPick = selected === i && i !== question.correct_index
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

      {selected !== null && (
        <button onClick={next} className="btn btn-primary mt-5">
          {index + 1 === questions.length ? 'Yakunlash' : 'Keyingi savol'}
        </button>
      )}
    </div>
  )
}
