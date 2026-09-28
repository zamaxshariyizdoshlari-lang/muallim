import { BookOpen, ChevronRight, Plus, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import {
  createAdminSubject, deleteAdminBook, deleteAdminSubject, listAdminBooks, listAdminSubjects,
  updateAdminBook, updateAdminSubject,
} from '../../api/client'
import { BackLink, ErrorNote, Spinner } from '../../components/ui'

export default function AdminContentPage({ onOpenBook, onBack }) {
  const [subjects, setSubjects] = useState(null)
  const [books, setBooks] = useState(null)
  const [error, setError] = useState('')
  const [newSubject, setNewSubject] = useState({ slug: '', title: '' })

  function refresh() {
    Promise.all([listAdminSubjects(), listAdminBooks()])
      .then(([s, b]) => { setSubjects(s); setBooks(b) })
      .catch((err) => setError(err.message))
  }

  useEffect(refresh, [])

  async function handleAddSubject(e) {
    e.preventDefault()
    setError('')
    try {
      const created = await createAdminSubject(newSubject)
      setSubjects((list) => [...list, created])
      setNewSubject({ slug: '', title: '' })
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleRenameSubject(subject, title) {
    try {
      const updated = await updateAdminSubject(subject.id, { title })
      setSubjects((list) => list.map((s) => (s.id === subject.id ? updated : s)))
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteSubject(subject) {
    if (!confirm(`"${subject.title}" fanini o'chirasizmi? Unga tegishli kurslar boshqa fansiz qoladi.`)) return
    try {
      await deleteAdminSubject(subject.id)
      setSubjects((list) => list.filter((s) => s.id !== subject.id))
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleRenameBook(book, title) {
    try {
      const updated = await updateAdminBook(book.id, { title })
      setBooks((list) => list.map((b) => (b.id === book.id ? updated : b)))
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteBook(book) {
    if (!confirm(`"${book.title}" kursini butunlay o'chirasizmi? Bu amalni qaytarib bo'lmaydi.`)) return
    try {
      await deleteAdminBook(book.id)
      setBooks((list) => list.filter((b) => b.id !== book.id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="rise">
      <BackLink onClick={onBack}>Statistikaga qaytish</BackLink>
      <header className="mb-6">
        <p className="eyebrow mb-2">Boshqaruv paneli</p>
        <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">Fanlar va kurslar</h1>
        <p className="mt-2 text-sm text-muted">
          Yangi kurs (kitob) qo'shish uchun JSON import hali kerak; bu yerda mavjud fan/kurs/bo'lim/mavzularni
          tahrirlash va o'chirish mumkin.
        </p>
      </header>

      <ErrorNote>{error}</ErrorNote>

      {!subjects || !books ? (
        <Spinner>Yuklanmoqda...</Spinner>
      ) : (
        <div className="flex flex-col gap-6">
          {subjects.map((subject) => (
            <section key={subject.id} className="card p-5 sm:p-6">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <input
                  className="field !w-auto flex-1 !border-transparent !bg-transparent !px-0 font-display text-lg font-bold text-ink focus:!border-line-strong focus:!bg-surface focus:!px-3"
                  defaultValue={subject.title}
                  onBlur={(e) => e.target.value !== subject.title && handleRenameSubject(subject, e.target.value)}
                />
                <div className="flex items-center gap-2">
                  <span className="chip">{subject.slug}</span>
                  <button onClick={() => handleDeleteSubject(subject)} className="btn btn-ghost btn-sm !px-2 text-bad">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              <ul className="flex flex-col gap-2">
                {books.filter((b) => b.subject === subject.id).map((book) => (
                  <li key={book.id} className="flex items-center gap-3 rounded-xl border border-line px-3 py-2.5">
                    <BookOpen size={16} className="shrink-0 text-brand" />
                    <input
                      className="field !w-auto flex-1 !border-transparent !bg-transparent !px-0 text-sm font-semibold text-ink focus:!border-line-strong focus:!bg-surface focus:!px-3"
                      defaultValue={book.title}
                      onBlur={(e) => e.target.value !== book.title && handleRenameBook(book, e.target.value)}
                    />
                    <button onClick={() => onOpenBook(book.id)} className="btn btn-ghost btn-sm">
                      Bo'lim/mavzular <ChevronRight size={14} />
                    </button>
                    <button onClick={() => handleDeleteBook(book)} className="btn btn-ghost btn-sm !px-2 text-bad">
                      <Trash2 size={14} />
                    </button>
                  </li>
                ))}
                {books.filter((b) => b.subject === subject.id).length === 0 && (
                  <p className="text-sm text-muted">Bu fanda hali kurs yo'q (JSON import orqali qo'shiladi).</p>
                )}
              </ul>
            </section>
          ))}

          <form onSubmit={handleAddSubject} className="card flex flex-wrap items-end gap-3 p-5">
            <label className="text-sm font-medium text-ink-2">
              Yangi fan nomi
              <input
                className="field mt-1.5"
                required
                value={newSubject.title}
                onChange={(e) => setNewSubject((v) => ({ ...v, title: e.target.value }))}
              />
            </label>
            <label className="text-sm font-medium text-ink-2">
              Slug (masalan "biologiya")
              <input
                className="field mt-1.5"
                required
                pattern="[a-z0-9-]+"
                value={newSubject.slug}
                onChange={(e) => setNewSubject((v) => ({ ...v, slug: e.target.value }))}
              />
            </label>
            <button className="btn btn-primary btn-sm">
              <Plus size={15} /> Fan qo'shish
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
