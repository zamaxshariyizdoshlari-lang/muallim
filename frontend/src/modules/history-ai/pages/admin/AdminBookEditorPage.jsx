import { ChevronRight, ListChecks, Plus, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import {
  createAdminSection, createAdminTopic, deleteAdminSection, deleteAdminTopic, getSections, listTopics,
  updateAdminSection, updateAdminTopic,
} from '../../api/client'
import { BackLink, ErrorNote, Spinner } from '../../components/ui'
import AdminQualityPanel from './AdminQualityPanel'

export default function AdminBookEditorPage({ bookId, onBack, onOpenTopic }) {
  const [sections, setSections] = useState(null)
  const [topics, setTopics] = useState(null)
  const [error, setError] = useState('')
  const [newSectionTitle, setNewSectionTitle] = useState('')
  const [view, setView] = useState('structure')

  function refresh() {
    Promise.all([getSections(bookId), listTopics(bookId)])
      .then(([s, t]) => { setSections(s); setTopics(t) })
      .catch((err) => setError(err.message))
  }

  useEffect(refresh, [bookId])

  async function handleAddSection(e) {
    e.preventDefault()
    if (!newSectionTitle.trim()) return
    setError('')
    try {
      await createAdminSection(bookId, {
        title: newSectionTitle, key: `s${(sections?.length || 0) + 1}`, order: (sections?.length || 0) + 1,
      })
      setNewSectionTitle('')
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleRenameSection(section, title) {
    try {
      await updateAdminSection(section.id, { title })
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteSection(section) {
    if (!confirm(`"${section.title}" bo'limi va undagi barcha mavzular o'chiriladi. Davom etasizmi?`)) return
    try {
      await deleteAdminSection(section.id)
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleAddTopic(section) {
    const title = prompt("Yangi mavzu nomi:")
    if (!title?.trim()) return
    const startPage = Number(prompt('Boshlanish beti:', '1')) || 1
    const endPage = Number(prompt('Tugash beti:', String(startPage))) || startPage
    try {
      await createAdminTopic(section.id, {
        title, key: `t${Date.now()}`, start_page: startPage, end_page: endPage,
        order: (topics?.filter((t) => t.section === section.id).length || 0) + 1,
      })
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleRenameTopic(topic, title) {
    try {
      await updateAdminTopic(topic.id, { title })
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteTopic(topic) {
    if (!confirm(`"${topic.title}" mavzusi o'chiriladi (dars va testi bilan). Davom etasizmi?`)) return
    try {
      await deleteAdminTopic(topic.id)
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Fanlar va kurslarga qaytish</BackLink>
      <ErrorNote>{error}</ErrorNote>

      <div className="mb-5 flex gap-2">
        {[['structure', 'Tuzilma'], ['quality', 'Sifat nazorati']].map(([id, label]) => (
          <button
            key={id}
            onClick={() => setView(id)}
            className={`btn btn-sm !rounded-full ${view === id ? 'btn-primary' : 'btn-ghost'}`}
          >
            {label}
          </button>
        ))}
      </div>

      {view === 'quality' ? (
        <AdminQualityPanel bookId={bookId} onOpenTopic={onOpenTopic} />
      ) : !sections || !topics ? (
        <Spinner>Yuklanmoqda...</Spinner>
      ) : (
        <div className="flex flex-col gap-5">
          {sections.map((section) => (
            <section key={section.id} className="card p-5 sm:p-6">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <input
                  className="field !w-auto flex-1 !border-transparent !bg-transparent !px-0 font-display text-lg font-bold text-ink focus:!border-line-strong focus:!bg-surface focus:!px-3"
                  defaultValue={section.title}
                  onBlur={(e) => e.target.value !== section.title && handleRenameSection(section, e.target.value)}
                />
                <div className="flex items-center gap-2">
                  <button onClick={() => handleAddTopic(section)} className="btn btn-ghost btn-sm">
                    <Plus size={14} /> Mavzu
                  </button>
                  <button onClick={() => handleDeleteSection(section)} className="btn btn-ghost btn-sm !px-2 text-bad">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              <ul className="flex flex-col gap-2">
                {topics.filter((t) => t.section === section.id).map((topic) => (
                  <li key={topic.id} className="flex items-center gap-3 rounded-xl border border-line px-3 py-2.5">
                    <ListChecks size={16} className="shrink-0 text-brand" />
                    <input
                      className="field !w-auto flex-1 !border-transparent !bg-transparent !px-0 text-sm font-semibold text-ink focus:!border-line-strong focus:!bg-surface focus:!px-3"
                      defaultValue={topic.title}
                      onBlur={(e) => e.target.value !== topic.title && handleRenameTopic(topic, e.target.value)}
                    />
                    <span className="chip">bet {topic.start_page}–{topic.end_page}</span>
                    <button onClick={() => onOpenTopic(topic.id)} className="btn btn-ghost btn-sm">
                      Dars/test <ChevronRight size={14} />
                    </button>
                    <button onClick={() => handleDeleteTopic(topic)} className="btn btn-ghost btn-sm !px-2 text-bad">
                      <Trash2 size={14} />
                    </button>
                  </li>
                ))}
                {topics.filter((t) => t.section === section.id).length === 0 && (
                  <p className="text-sm text-muted">Bu bo'limda hali mavzu yo'q.</p>
                )}
              </ul>
            </section>
          ))}

          <form onSubmit={handleAddSection} className="card flex flex-wrap items-end gap-3 p-5">
            <label className="flex-1 text-sm font-medium text-ink-2">
              Yangi bo'lim nomi
              <input className="field mt-1.5" value={newSectionTitle} onChange={(e) => setNewSectionTitle(e.target.value)} />
            </label>
            <button className="btn btn-primary btn-sm">
              <Plus size={15} /> Bo'lim qo'shish
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
