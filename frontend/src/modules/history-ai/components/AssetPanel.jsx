import { AlertTriangle, Loader2, RefreshCw, Sparkles } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { createAsset, getAsset, getAssetByTopic } from '../api/client'

const POLL_INTERVAL_MS = 2500

/**
 * Taqdimot/o'yin uchun umumiy panel.
 * Avval mavjud natijani tekshiradi (bor bo'lsa AI qayta chaqirilmaydi),
 * bo'lmasa "Yaratish" tugmasini ko'rsatadi. "Qayta yaratish" alohida amal.
 */
export default function AssetPanel({ topicId, kind, label, icon: Icon, isTeacher, children }) {
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

  const heading = (
    <h3 className="flex items-center gap-2.5 font-display text-lg font-bold text-ink">
      {Icon && (
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-soft text-brand">
          <Icon size={17} />
        </span>
      )}
      {label}
    </h3>
  )

  if (loading) {
    return <section className="card p-5 sm:p-6">{heading}</section>
  }

  if (!asset) {
    return (
      <section className="card p-5 sm:p-6">
        <div className="flex items-center justify-between gap-3">
          {heading}
          {isTeacher ? (
            <button onClick={() => handleGenerate(false)} className="btn btn-primary btn-sm">
              <Sparkles size={15} /> Yaratish
            </button>
          ) : (
            <span className="chip">Hali tayyorlanmagan</span>
          )}
        </div>
        {error && <p className="mt-3 text-sm text-bad">{error}</p>}
      </section>
    )
  }

  return (
    <section className="card p-5 sm:p-6">
      <div className="mb-5 flex items-center justify-between gap-3">
        {heading}
        {isTeacher && asset.status !== 'pending' && (
          <button onClick={() => handleGenerate(true)} className="btn btn-ghost btn-sm">
            <RefreshCw size={13} /> Qayta yaratish
          </button>
        )}
      </div>

      {error && <p className="mb-3 text-sm text-bad">{error}</p>}

      {asset.status === 'pending' && (
        <div className="flex items-center gap-2 text-sm text-ink-2">
          <Loader2 className="animate-spin text-gold" size={18} />
          Tayyorlanmoqda...
        </div>
      )}

      {asset.status === 'failed' && (
        <div className="flex items-start gap-2 rounded-xl border border-bad/40 bg-bad-soft px-4 py-3 text-sm text-bad">
          <AlertTriangle size={18} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold">Xatolik yuz berdi</p>
            <p className="mt-1">{asset.error_message}</p>
          </div>
        </div>
      )}

      {asset.status === 'done' && children(asset.data)}
    </section>
  )
}
