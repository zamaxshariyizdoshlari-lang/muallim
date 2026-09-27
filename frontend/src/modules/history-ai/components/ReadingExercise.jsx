import QuizGame from './QuizGame'

/** Qisqa matnni o'qib tushunish: audio yo'q (o'qish ko'nikmasi), keyin savollar. */
export default function ReadingExercise({ title, text, questions }) {
  if (!text) return null
  return (
    <div className="flex flex-col gap-5">
      <section className="card p-5 sm:p-6">
        {title && <h3 className="mb-3 font-display text-lg font-bold text-ink">{title}</h3>}
        <div className="read">
          {text.split(/\n{2,}/).map((para, i) => (
            <p key={i}>{para}</p>
          ))}
        </div>
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
