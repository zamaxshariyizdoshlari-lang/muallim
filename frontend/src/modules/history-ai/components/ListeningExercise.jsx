import { Play, Volume2 } from 'lucide-react'
import QuizGame from './QuizGame'
import { speak, speakSequence } from '../utils/speech'

/** Qisqa dialogni tinglab tushunish: avval butun dialog o'qib eshittiriladi (yoki qatorma-qator),
 * keyin tushunganini tekshiruvchi savollar (variant tanlash). */
export default function ListeningExercise({ dialogue, questions }) {
  if (!dialogue?.length) return null

  return (
    <div className="flex flex-col gap-5">
      <section className="card p-5 sm:p-6">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="font-display text-lg font-bold text-ink">Dialogni tinglang</h3>
          <button
            onClick={() => speakSequence(dialogue.map((l) => l.text))}
            className="btn btn-primary btn-sm"
          >
            <Play size={14} /> Hammasini tinglash
          </button>
        </div>
        <ol className="flex flex-col gap-2.5">
          {dialogue.map((line, i) => (
            <li key={i} className="flex items-start gap-3 rounded-xl bg-surface-2 px-4 py-2.5">
              <span className="w-20 shrink-0 font-display text-sm font-bold text-brand">{line.speaker}</span>
              <span className="min-w-0 flex-1 font-read text-base text-ink">{line.text}</span>
              <button
                onClick={() => speak(line.text)}
                aria-label={`"${line.text}" so'zini tinglash`}
                className="shrink-0 text-muted hover:text-brand"
              >
                <Volume2 size={16} />
              </button>
            </li>
          ))}
        </ol>
      </section>

      {questions?.length > 0 && (
        <section className="card p-5 sm:p-6">
          <h3 className="mb-4 font-display text-lg font-bold text-ink">Tushundingizmi?</h3>
          <QuizGame questions={questions} />
        </section>
      )}
    </div>
  )
}
