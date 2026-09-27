import { Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'

/** Erkin yozish mashqi: baholanmaydi (avtomatik tekshirish yo'q) - talaba o'zi yozib,
 * keyin namunaviy javob bilan solishtiradi. Milliy sertifikat/TYS'dagi yozma qismga tayyorgarlik. */
export default function WritingPractice({ instruction, sample_answer: sample }) {
  const [text, setText] = useState('')
  const [showSample, setShowSample] = useState(false)

  return (
    <div>
      <p className="mb-3 font-read text-base leading-relaxed text-ink">{instruction}</p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        placeholder="Shu yerga turkcha yozing..."
        className="field font-read"
      />
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <button onClick={() => setShowSample((s) => !s)} className="btn btn-ghost btn-sm">
          {showSample ? <EyeOff size={14} /> : <Eye size={14} />}
          {showSample ? 'Namunani yashirish' : "Namunaviy javobni ko'rish"}
        </button>
        <p className="text-xs text-muted">Bu mashq baholanmaydi - o'zingizni sinab ko'ring.</p>
      </div>
      {showSample && (
        <p className="rise mt-3 rounded-xl border border-ok/40 bg-ok-soft px-4 py-3 font-read text-sm leading-relaxed text-ink">
          {sample}
        </p>
      )}
    </div>
  )
}
