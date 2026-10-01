import { Brain, ChevronRight } from 'lucide-react'
import { useState } from 'react'
import MiniCheck from './MiniCheck'

/**
 * Oldindan sinash (pre-test): dars o'qilishidan oldin 2-3 savol. Javob noto'g'ri bo'lsa ham zarari
 * yo'q - miya mavzuga "tayyorlanadi" va keyin o'qiganini yaxshiroq eslab qoladi.
 * Ixtiyoriy: o'tkazib yuborish mumkin. Natija saqlanmaydi.
 */
export default function PreTest({ questions }) {
  const [started, setStarted] = useState(false)
  const [dismissed, setDismissed] = useState(false)
  const [index, setIndex] = useState(0)
  const [correct, setCorrect] = useState(0)
  const [answered, setAnswered] = useState(false)

  if (!questions?.length || dismissed) return null
  const finished = index >= questions.length

  if (!started) {
    return (
      <section className="card flex flex-wrap items-center gap-4 border-brand/30 bg-brand-soft/50 p-5">
        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand text-brand-ink">
          <Brain size={22} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="font-display text-base font-bold text-ink">Avval o'zingizni sinab ko'ring</p>
          <p className="text-sm text-ink-2">
            {questions.length} ta savol. Bilmasangiz ham zarari yo'q: shunda dars ma'nosi aniqroq bo'ladi.
          </p>
        </div>
        <button onClick={() => setStarted(true)} className="btn btn-primary btn-sm">Boshlash</button>
        <button onClick={() => setDismissed(true)} className="btn btn-ghost btn-sm">O'tkazib yuborish</button>
      </section>
    )
  }

  return (
    <section className="card border-brand/30 p-5 sm:p-6" aria-label="Oldindan sinash">
      <p className="eyebrow mb-3 flex items-center gap-2"><Brain size={14} /> Oldindan sinash</p>
      {finished ? (
        <div className="rise">
          <p className="font-display text-xl font-bold text-ink">
            {correct} / {questions.length} ta to'g'ri
          </p>
          <p className="mt-1 text-sm text-ink-2">
            {correct === questions.length
              ? "Siz bu mavzuni yaxshi bilar ekansiz! Dars bilimingizni mustahkamlaydi."
              : "Yaxshi, endi dars matnida shu savollar javobini izlang."}
          </p>
          <button onClick={() => setDismissed(true)} className="btn btn-primary btn-sm mt-4">Darsni boshlash</button>
        </div>
      ) : (
        <>
          <p className="mb-3 text-xs font-semibold text-muted">Savol {index + 1} / {questions.length}</p>
          <MiniCheck
            key={index}
            question={questions[index]}
            onAnswered={(ok) => { setAnswered(true); if (ok) setCorrect((c) => c + 1) }}
          />
          {answered && (
            <button
              onClick={() => { setAnswered(false); setIndex((i) => i + 1) }}
              className="btn btn-primary btn-sm mt-4"
            >
              {index + 1 === questions.length ? 'Natijani ko\'rish' : 'Keyingi'} <ChevronRight size={14} />
            </button>
          )}
        </>
      )}
    </section>
  )
}
