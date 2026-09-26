import { ArrowRight, BookOpen, Clock, Landmark, Languages, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { listSubjects } from '../api/client'
import { ErrorNote } from '../components/ui'

const ICONS = { landmark: Landmark, languages: Languages, book: BookOpen }

export default function SubjectsPage({ me, onOpenSubject }) {
  const [subjects, setSubjects] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    listSubjects().then(setSubjects).catch((err) => setError(err.message))
  }, [])

  const name = me?.first_name || me?.username

  return (
    <div className="rise">
      <div className="mb-10">
        <p className="eyebrow mb-2">Xush kelibsiz{name ? `, ${name}` : ''}</p>
        <h1 className="font-display text-4xl font-extrabold leading-tight text-ink sm:text-5xl">
          Bugun nimani o'rganamiz?
        </h1>
        <p className="mt-3 max-w-xl font-read text-lg text-ink-2">
          Fanni tanlang, mavzu-mavzu o'ting, o'yinlar va testlar bilan mustahkamlang, oxirida sertifikat oling.
        </p>
      </div>

      <ErrorNote>{error}</ErrorNote>

      <div className="grid gap-5 sm:grid-cols-2">
        {subjects?.map((s, i) => {
          const Icon = ICONS[s.icon] || BookOpen
          return (
            <button
              key={s.id}
              onClick={() => onOpenSubject(s)}
              className="card card-hover group relative overflow-hidden p-6 text-left"
              style={{ animation: 'rise 0.45s ease both', animationDelay: `${i * 0.06}s` }}
            >
              <div className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gold/10" aria-hidden />
              <span className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-brand text-brand-ink shadow">
                <Icon size={28} />
              </span>
              <h2 className="font-display text-2xl font-bold text-ink">{s.title}</h2>
              <p className="mt-1 text-sm leading-relaxed text-muted">{s.description}</p>
              <div className="mt-5 flex items-center justify-between">
                <span className="chip chip-gold">{s.book_count} ta kurs</span>
                <ArrowRight className="text-gold transition-transform group-hover:translate-x-1" size={20} />
              </div>
            </button>
          )
        })}

        {subjects && (
          <div className="card flex flex-col justify-center border-dashed p-6 text-left opacity-90">
            <span className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gold-soft text-gold">
              <Sparkles size={26} />
            </span>
            <h2 className="font-display text-2xl font-bold text-ink">Yangi fanlar</h2>
            <p className="mt-1 flex items-center gap-1.5 text-sm text-muted">
              <Clock size={14} /> Tez orada: Turk tili va boshqalar
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
