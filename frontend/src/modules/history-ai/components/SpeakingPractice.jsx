import { Mic, Volume2 } from 'lucide-react'
import { speak } from '../utils/speech'

/** Gapirish mashqi: nutqni tanish/baholash yo'q (qimmat va murakkab) - talaba brauzer ovozini
 * tinglab, ovoz chiqarib takrorlaydi. Odat hosil qilish uchun, baholanmaydi. */
export default function SpeakingPractice({ sentences }) {
  if (!sentences?.length) return null
  return (
    <div className="flex flex-col gap-2.5">
      <p className="mb-1 flex items-center gap-2 text-sm text-muted">
        <Mic size={15} /> Har jumlani tinglang, keyin ovoz chiqarib takrorlang. Baholanmaydi - mashq uchun.
      </p>
      {sentences.map((s, i) => (
        <div key={i} className="flex items-center justify-between gap-3 rounded-xl bg-surface-2 px-4 py-3">
          <span className="font-read text-base text-ink">{s}</span>
          <button onClick={() => speak(s)} className="btn btn-ghost btn-sm shrink-0" aria-label={`"${s}" ni tinglash`}>
            <Volume2 size={16} />
          </button>
        </div>
      ))}
    </div>
  )
}
