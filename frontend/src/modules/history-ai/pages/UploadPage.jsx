import { ArrowRight, BookOpen, FileJson, FileUp, Loader2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { importBookJson, listBooks, uploadBook } from '../api/client'
import { BackLink, ErrorNote } from '../components/ui'

export default function UploadPage({ subject, onBack, isTeacher, onUploaded, onOpenBook }) {
  const [books, setBooks] = useState([])
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [importMsg, setImportMsg] = useState(null)

  useEffect(() => {
    listBooks(subject?.slug).then(setBooks).catch((err) => setError(err.message))
  }, [subject?.slug])

  async function handleImport(e) {
    const f = e.target.files?.[0]
    e.target.value = ''
    if (!f) return
    setImportMsg({ text: 'Import qilinmoqda...' })
    try {
      const r = await importBookJson(f)
      setImportMsg({ ok: true, text: `Import tayyor: ${r.sections} bo'lim, ${r.topics} mavzu, ${r.questions} test savoli.` })
      setBooks(await listBooks(subject?.slug))
    } catch (err) {
      setImportMsg({ text: err.message, errors: err.errors })
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return
    setError('')
    setLoading(true)
    try {
      const data = await uploadBook(file, title)
      onUploaded(data.book, data.topics)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rise">
      <BackLink onClick={onBack}>Barcha fanlar</BackLink>
      <div className="mb-8">
        <p className="eyebrow mb-2">{subject?.title || 'Kurslar'}</p>
        <h1 className="font-display text-4xl font-extrabold text-ink sm:text-5xl">Kurslar</h1>
        <p className="mt-3 max-w-xl font-read text-lg text-ink-2">
          {isTeacher ? 'Kursni tanlang yoki yangisini yuklang.' : "O'qimoqchi bo'lgan kursni tanlang."}
        </p>
      </div>

      <ErrorNote>{error}</ErrorNote>

      <div className="mb-10 grid gap-4 sm:grid-cols-2">
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

      {isTeacher && (
        <div className="grid gap-5 lg:grid-cols-2">
          <div className="card p-6">
            <div className="mb-3 flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold-soft text-gold">
                <FileJson size={20} />
              </span>
              <h2 className="font-display text-lg font-bold text-ink">Tayyor JSON'dan import</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-muted">
              Mavzular, testlar, o'yinlar hammasi tayyor JSON faylda. Qayta yuklasangiz, talabalar progressi saqlanadi.
            </p>
            <label className="btn btn-primary cursor-pointer">
              JSON faylni tanlash
              <input type="file" accept="application/json,.json" className="hidden" onChange={handleImport} />
            </label>
            {importMsg && (
              <div className={`mt-4 text-sm ${importMsg.ok ? 'text-ok' : 'text-bad'}`}>
                <p>{importMsg.text}</p>
                {importMsg.errors?.length > 0 && (
                  <ul className="mt-1 max-h-40 list-disc overflow-auto pl-5 text-xs">
                    {importMsg.errors.map((er, i) => <li key={i}>{er}</li>)}
                  </ul>
                )}
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="card p-6">
            <h2 className="mb-3 font-display text-lg font-bold text-ink">Zaxira: PDF yuklash</h2>
            <label className="mb-4 block text-sm font-medium text-ink-2">
              Kitob nomi (ixtiyoriy)
              <input
                className="field mt-1.5"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Masalan: 8-sinf Jahon tarixi"
              />
            </label>

            <label className="mb-4 flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-line-strong px-4 py-6 text-center transition-colors hover:border-gold">
              <FileUp className="text-gold" size={26} />
              <span className="text-sm text-ink-2">{file ? file.name : 'PDF faylni tanlash uchun bosing'}</span>
              <input type="file" accept="application/pdf" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            </label>

            <button type="submit" disabled={!file || loading} className="btn btn-primary w-full">
              {loading && <Loader2 className="animate-spin" size={16} />}
              {loading ? 'Yuklanmoqda...' : 'Yuklash'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
