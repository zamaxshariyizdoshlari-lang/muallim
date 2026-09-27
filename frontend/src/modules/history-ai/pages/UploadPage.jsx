import { ArrowRight, BookOpen } from 'lucide-react'
import { useEffect, useState } from 'react'
import { listBooks } from '../api/client'
import { BackLink, ErrorNote } from '../components/ui'

/** Fan ichidagi kurslar ro'yxati. Kurs qo'shish/yangilash admin panel (Django admin) va
 * `manage.py import_book` buyrug'i orqali amalga oshiriladi - bu sahifa faqat ko'rish uchun. */
export default function UploadPage({ subject, onBack, onOpenBook }) {
  const [books, setBooks] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    listBooks(subject?.slug).then(setBooks).catch((err) => setError(err.message))
  }, [subject?.slug])

  return (
    <div className="rise">
      <BackLink onClick={onBack}>Barcha fanlar</BackLink>
      <div className="mb-8">
        <p className="eyebrow mb-2">{subject?.title || 'Kurslar'}</p>
        <h1 className="font-display text-4xl font-extrabold text-ink sm:text-5xl">Kurslar</h1>
        <p className="mt-3 max-w-xl font-read text-lg text-ink-2">O'qimoqchi bo'lgan kursni tanlang.</p>
      </div>

      <ErrorNote>{error}</ErrorNote>

      <div className="grid gap-4 sm:grid-cols-2">
        {books.length === 0 && <p className="text-sm text-muted">Bu fanda hozircha kurslar yo'q.</p>}
        {books.map((b, i) => (
          <button
            key={b.id}
            onClick={() => onOpenBook(b)}
            className="card card-hover group relative flex items-stretch overflow-hidden text-left"
            style={{ animation: 'rise 0.45s ease both', animationDelay: `${i * 0.05}s` }}
          >
            <span className="w-3 shrink-0 bg-gradient-to-b from-brand to-gold" aria-hidden />
            <span className="flex flex-1 items-center gap-4 p-5">
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand-soft text-brand">
                <BookOpen size={22} />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block font-display text-lg font-bold leading-snug text-ink">{b.title}</span>
                <span className="mt-1 block text-xs font-medium text-muted">{b.description || "O'qishni boshlash"}</span>
              </span>
              <ArrowRight className="shrink-0 text-gold transition-transform group-hover:translate-x-1" size={20} />
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
