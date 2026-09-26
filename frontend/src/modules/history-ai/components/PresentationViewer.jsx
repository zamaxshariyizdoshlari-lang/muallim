import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useState } from 'react'

export default function PresentationViewer({ slides }) {
  const [index, setIndex] = useState(0)

  if (!slides?.length) return <p className="text-sm text-muted">Slaydlar topilmadi.</p>

  const slide = slides[index]
  const isTitle = !slide.bullets?.length

  return (
    <div>
      {/* Bo'r doskasi uslubidagi slayd */}
      <div
        key={index}
        className="rise relative flex min-h-[260px] flex-col justify-center overflow-hidden rounded-2xl border-4 border-[#5b4526] px-6 py-8 shadow-inner sm:px-10"
        style={{ background: 'var(--chalk)', color: 'var(--chalk-ink)' }}
      >
        <div className="meander absolute inset-x-0 top-0 opacity-40" />
        <h3
          className={`font-display font-bold text-[#e9c46a] ${isTitle ? 'text-center text-3xl sm:text-4xl' : 'mb-5 text-2xl'}`}
        >
          {slide.title}
        </h3>
        {!isTitle && (
          <ul className="flex flex-col gap-3 font-read text-base leading-relaxed sm:text-lg">
            {slide.bullets.map((bullet, i) => (
              <li key={i} className="flex gap-3">
                <span className="mt-2.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[#e9c46a]" />
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        )}
        {slide.page && (
          <span className="absolute bottom-3 right-4 text-xs font-semibold text-[#e9c46a]/70">bet {slide.page}</span>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between gap-3">
        <button
          onClick={() => setIndex((i) => Math.max(0, i - 1))}
          disabled={index === 0}
          className="btn btn-ghost btn-sm"
        >
          <ChevronLeft size={16} /> Oldingi
        </button>
        <div className="flex flex-wrap items-center justify-center gap-1.5" aria-label={`${index + 1} / ${slides.length}`}>
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              aria-label={`${i + 1}-slayd`}
              className={`h-2 rounded-full transition-all ${i === index ? 'w-6 bg-brand' : 'w-2 bg-line-strong hover:bg-gold'}`}
            />
          ))}
        </div>
        <button
          onClick={() => setIndex((i) => Math.min(slides.length - 1, i + 1))}
          disabled={index === slides.length - 1}
          className="btn btn-ghost btn-sm"
        >
          Keyingi <ChevronRight size={16} />
        </button>
      </div>
    </div>
  )
}
