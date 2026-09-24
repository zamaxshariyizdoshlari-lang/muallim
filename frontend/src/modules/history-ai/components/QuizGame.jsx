import { RotateCcw } from 'lucide-react'
import { useState } from 'react'

export default function QuizGame({ questions }) {
  const [index, setIndex] = useState(0)
  const [selected, setSelected] = useState(null)
  const [score, setScore] = useState(0)

  if (!questions?.length) return <p className="text-sm text-slate-500">Savollar topilmadi.</p>

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
      <div className="text-center">
        <p className="mb-4 text-lg font-medium text-slate-800">
          Natija: {score} / {questions.length}
        </p>
        <button
          onClick={reset}
          className="mx-auto flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          <RotateCcw size={14} /> Qaytadan boshlash
        </button>
      </div>
    )
  }

  return (
    <div>
      <p className="mb-1 text-xs text-slate-400">
        Savol {index + 1} / {questions.length}
      </p>
      <p className="mb-3 text-sm font-medium text-slate-800">{question.question}</p>

      <div className="flex flex-col gap-2">
        {question.options?.map((opt, i) => {
          const isCorrect = selected !== null && i === question.correct_index
          const isWrongPick = selected === i && i !== question.correct_index
          return (
            <button
              key={i}
              onClick={() => pick(i)}
              className={`rounded-lg border px-3 py-2 text-left text-sm ${
                isCorrect
                  ? 'border-green-300 bg-green-50 text-green-700'
                  : isWrongPick
                    ? 'border-red-300 bg-red-50 text-red-700'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-indigo-300'
              }`}
            >
              {String.fromCharCode(65 + i)}. {opt}
            </button>
          )
        })}
      </div>

      {selected !== null && (
        <button
          onClick={next}
          className="mt-4 rounded-lg bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
        >
          {index + 1 === questions.length ? 'Yakunlash' : 'Keyingi savol'}
        </button>
      )}
    </div>
  )
}
