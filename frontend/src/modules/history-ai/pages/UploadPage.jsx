import { FileUp, Loader2 } from 'lucide-react'
import { useState } from 'react'
import { uploadBook } from '../api/client'

export default function UploadPage({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

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
    <div className="mx-auto max-w-xl">
      <h1 className="mb-1 text-2xl font-semibold text-slate-900">Darslik PDF yuklash</h1>
      <p className="mb-6 text-sm text-slate-500">
        Tarix darsligini PDF shaklida yuklang. Tizim betlarni ajratib, mavzularni aniqlaydi.
      </p>

      <form onSubmit={handleSubmit} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <label className="mb-4 block text-sm text-slate-700">
          Kitob nomi (ixtiyoriy)
          <input
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Masalan: 8-sinf Jahon tarixi"
          />
        </label>

        <label className="mb-4 flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-slate-300 px-4 py-8 text-center hover:border-indigo-400">
          <FileUp className="text-slate-400" size={28} />
          <span className="text-sm text-slate-600">
            {file ? file.name : 'PDF faylni tanlash uchun bosing'}
          </span>
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </label>

        {error && <p className="mb-3 text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={!file || loading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
        >
          {loading && <Loader2 className="animate-spin" size={16} />}
          {loading ? 'Yuklanmoqda...' : 'Yuklash'}
        </button>
      </form>
    </div>
  )
}
