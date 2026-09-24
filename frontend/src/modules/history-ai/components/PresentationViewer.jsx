import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useState } from 'react'

export default function PresentationViewer({ slides }) {
  const [index, setIndex] = useState(0)

  if (!slides?.length) return <p className="text-sm text-slate-500">Slaydlar topilmadi.</p>

  const slide = slides[index]

  return (
    <div>
      <div className="flex min-h-[220px] flex-col justify-center rounded-lg border border-slate-200 bg-slate-50 p-8 text-center">
        <h3 className="mb-4 text-xl font-semibold text-slate-900">{slide.title}</h3>
        {slide.bullets?.length > 0 && (
          <ul className="mx-auto flex max-w-md flex-col gap-2 text-left text-sm text-slate-700">
            {slide.bullets.map((bullet, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-indigo-500">•</span>
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        )}
        {slide.page && (
          <span className="mt-4 self-center rounded bg-slate-200 px-2 py-0.5 text-xs text-slate-500">
            bet {slide.page}
          </span>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between">
        <button
          onClick={() => setIndex((i) => Math.max(0, i - 1))}
          disabled={index === 0}
          className="flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-700 disabled:opacity-40"
        >
          <ChevronLeft size={16} /> Oldingi
        </button>
        <span className="text-sm text-slate-500">
          {index + 1} / {slides.length}
        </span>
        <button
          onClick={() => setIndex((i) => Math.min(slides.length - 1, i + 1))}
          disabled={index === slides.length - 1}
          className="flex items-center gap-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-700 disabled:opacity-40"
        >
          Keyingi <ChevronRight size={16} />
        </button>
      </div>
    </div>
  )
}
