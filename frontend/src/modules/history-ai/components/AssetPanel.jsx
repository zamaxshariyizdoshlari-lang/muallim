import { AlertTriangle, Loader2, Sparkles } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createAsset, getAsset } from '../api/client'

const POLL_INTERVAL_MS = 2500

/**
 * Taqdimot/o'yin uchun umumiy panel: "Yaratish" tugmasi -> fon vazifani
 * boshlaydi -> natija tayyor bo'lguncha pollaydi -> children(data) render qiladi.
 */
export default function AssetPanel({ topicId, kind, label, children }) {
  const [asset, setAsset] = useState(null)
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => () => clearInterval(intervalRef.current), [])

  async function handleGenerate() {
    setError('')
    try {
      const created = await createAsset(topicId, kind)
      setAsset(created)
      intervalRef.current = setInterval(async () => {
        try {
          const data = await getAsset(created.id)
          setAsset(data)
          if (data.status !== 'pending') clearInterval(intervalRef.current)
        } catch (err) {
          setError(err.message)
          clearInterval(intervalRef.current)
        }
      }, POLL_INTERVAL_MS)
    } catch (err) {
      setError(err.message)
    }
  }

  if (!asset) {
    return (
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
          <button
            onClick={handleGenerate}
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
          >
            <Sparkles size={16} /> Yaratish
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      </section>
    )
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">{label}</h2>

      {asset.status === 'pending' && (
        <div className="flex items-center gap-2 text-sm text-slate-600">
          <Loader2 className="animate-spin" size={18} />
          Tayyorlanmoqda...
        </div>
      )}

      {asset.status === 'failed' && (
        <div className="flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          <AlertTriangle size={18} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-medium">Xatolik yuz berdi</p>
            <p className="mt-1 text-red-600">{asset.error_message}</p>
          </div>
        </div>
      )}

      {asset.status === 'done' && children(asset.data)}
    </section>
  )
}
