import { CheckCircle2, XCircle } from 'lucide-react'
import { useState } from 'react'

/**
 * Bitta tezkor savol: javob berilishi bilan to'g'ri variant ko'rsatiladi. Ball bermaydi va
 * saqlanmaydi (mashq uchun) - bloklar ichida va "oldindan sinash"da ishlatiladi.
 */
export default function MiniCheck({ question, onAnswered }) {
  const [selected, setSelected] = useState(null)
  if (!question?.options?.length) return null
  const answered = selected !== null

  function pick(i) {
    if (answered) return
    setSelected(i)
    onAnswered?.(i === question.correct_index)
  }

  return (
    <div>
      <p className="mb-3 font-read text-base font-medium leading-snug text-ink">{question.question}</p>
      <div className="flex flex-col gap-2">
        {question.options.map((opt, i) => {
          const isCorrect = answered && i === question.correct_index
          const isWrongPick = selected === i && i !== question.correct_index
          return (
            <button
              key={i}
              type="button"
              onClick={() => pick(i)}
              disabled={answered}
              className={`option ${isCorrect ? 'is-ok' : isWrongPick ? 'is-bad shake' : ''}`}
            >
              <span className="option-key">{String.fromCharCode(65 + i)}</span>
              <span className="pt-0.5">{opt}</span>
            </button>
          )
        })}
      </div>
      {answered && (
        <p
          role="status"
          className={`rise mt-3 flex items-center gap-2 text-sm font-semibold ${
            selected === question.correct_index ? 'text-ok' : 'text-bad'
          }`}
        >
          {selected === question.correct_index ? (
            <><CheckCircle2 size={16} /> To'g'ri!</>
          ) : (
            <><XCircle size={16} /> Hali emas. To'g'ri javob belgilandi.</>
          )}
        </p>
      )}
    </div>
  )
}
