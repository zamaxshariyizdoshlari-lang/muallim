import { AlertTriangle, Loader2, RefreshCw, Sparkles } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createAsset, getAsset, getAssetByTopic } from '../api/client'

const POLL_INTERVAL_MS = 2500

/**
 * Taqdimot/o'yin uchun umumiy panel.
 * Avval mavjud natijani tekshiradi (bor bo'lsa AI qayta chaqirilmaydi),
 * bo'lmasa "Yaratish" tugmasini ko'rsatadi. "Qayta yaratish" alohida amal.
 */
export default function AssetPanel({ topicId, kind, label, isTeacher, children }) {
  const [asset, setAsset] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    getAssetByTopic(topicId, kind)
      .then((data) => {
        if (cancelled) return
        setAsset(data)
        if (data?.status === 'pending') startPolling(data.id)
      })
      .catch((err) => !cancelled && setError(err.message))
      .finally(() => !cancelled && setLoading(false))

    return () => {
      cancelled = true
      clearInterval(intervalRef.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId, kind])

  function startPolling(assetId) {
    clearInterval(intervalRef.current)
    intervalRef.current = setInterval(async () => {
      try {
        const data = await getAsset(assetId)
        setAsset(data)
        if (data.status !== 'pending') clearInterval(intervalRef.current)
      } catch (err) {
        setError(err.message)
        clearInterval(intervalRef.current)
      }
    }, POLL_INTERVAL_MS)
  }

  async function handleGenerate(regenerate) {
    setError('')
    try {
      const created = await createAsset(topicId, kind, { regenerate })
      setAsset(created)
      if (created.status === 'pending') startPolling(created.id)
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) {
    return (
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
      </section>
    )
  }

  if (!asset) {
    return (
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
          {isTeacher ? (
            <button
              onClick={() => handleGenerate(false)}
              className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
            >
              <Sparkles size={16} /> Yaratish
            </button>
          ) : (
            <span className="text-xs text-slate-400">Hali tayyorlanmagan</span>
          )}
        </div>
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      </section>
    )
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
        {isTeacher && asset.status !== 'pending' && (
          <button
            onClick={() => handleGenerate(true)}
            className="flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-50"
          >
            <RefreshCw size={13} /> Qayta yaratish
          </button>
        )}
      </div>

      {error && <p className="mb-3 text-sm text-red-600">{error}</p>}

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
