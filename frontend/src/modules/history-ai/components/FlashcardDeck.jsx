import { ChevronLeft, ChevronRight, Volume2 } from 'lucide-react'
import { useState } from 'react'
import { speak } from '../utils/speech'

/** So'z kartochkalari: old tomonda turkcha so'z, orqasida o'zbekcha tarjima + misol gap. */
export default function FlashcardDeck({ words }) {
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)

  if (!words?.length) return <p className="text-sm text-muted">Kartochkalar topilmadi.</p>

  const w = words[index]

  function go(delta) {
    setFlipped(false)
    setIndex((i) => Math.max(0, Math.min(words.length - 1, i + delta)))
  }

  return (
    <div className="mx-auto max-w-md">
      <div className="mb-4 flex items-center justify-center gap-3">
        <span className="chip">{index + 1} / {words.length}</span>
      </div>

      <button
        type="button"
        onClick={() => setFlipped((f) => !f)}
        className="card flex min-h-52 w-full flex-col items-center justify-center gap-3 p-8 text-center"
        aria-label={flipped ? "Old tomonni ko'rish" : "Tarjimani ko'rish uchun bosing"}
      >
        {!flipped ? (
          <>
            <p className="font-display text-3xl font-extrabold text-ink">{w.tr}</p>
            <span
              role="button"
              tabIndex={0}
              onClick={(e) => { e.stopPropagation(); speak(w.tr) }}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.stopPropagation(); speak(w.tr) } }}
              className="mt-1 flex items-center gap-1.5 text-sm font-semibold text-brand"
            >
              <Volume2 size={16} /> Tinglash
            </span>
          </>
        ) : (
          <>
            <p className="font-display text-2xl font-bold text-brand">{w.uz}</p>
            {w.example_tr && (
              <div className="mt-2 border-t border-line pt-3 text-sm">
                <p className="font-medium text-ink">{w.example_tr}</p>
                <p className="mt-1 text-muted">{w.example_uz}</p>
              </div>
            )}
          </>
        )}
        <p className="mt-2 text-xs text-muted">Kartani aylantirish uchun bosing</p>
      </button>

      <div className="mt-4 flex items-center justify-between gap-3">
        <button onClick={() => go(-1)} disabled={index === 0} className="btn btn-ghost btn-sm">
          <ChevronLeft size={16} /> Oldingi
        </button>
        <button onClick={() => go(1)} disabled={index === words.length - 1} className="btn btn-ghost btn-sm">
          Keyingi <ChevronRight size={16} />
        </button>
      </div>
    </div>
  )
}
