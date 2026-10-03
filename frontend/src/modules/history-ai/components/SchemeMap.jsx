import { MapPin } from 'lucide-react'
import { useId, useState } from 'react'
import { MAP_SIZE, PLACES, REGIONS, RIVERS, SEAS, project } from '../utils/gazetteer'

const toPath = (coords) => coords.map(([lon, lat], i) => `${i ? 'L' : 'M'}${project(lon, lat).map((n) => n.toFixed(1)).join(' ')}`).join(' ')

/** Xaritani o'z nuqtalariga qarab qirqadi: bo'sh joy kamayadi, yozuvlar kattaroq ko'rinadi. */
function cropBox(ids, regionIds) {
  const pts = [
    ...ids.map((id) => project(PLACES[id].lon, PLACES[id].lat)),
    ...regionIds.map((id) => project(REGIONS[id].lon, REGIONS[id].lat)),
  ]
  const xs = pts.map((p) => p[0])
  const ys = pts.map((p) => p[1])
  const pad = 90
  let x0 = Math.min(...xs) - pad
  let x1 = Math.max(...xs) + pad
  let y0 = Math.min(...ys) - pad * 0.8
  let y1 = Math.max(...ys) + pad * 0.8
  const minW = 560
  const minH = 340
  if (x1 - x0 < minW) { const m = (x0 + x1) / 2; x0 = m - minW / 2; x1 = m + minW / 2 }
  if (y1 - y0 < minH) { const m = (y0 + y1) / 2; y0 = m - minH / 2; y1 = m + minH / 2 }
  // Kadr chegaradan chiqmasin (siljitamiz), keyin kerak bo'lsa qisqartiramiz
  const shift = (a, b, max) => (a < 0 ? [0, Math.min(max, b - a)] : b > max ? [Math.max(0, a - (b - max)), max] : [a, b])
  ;[x0, x1] = shift(x0, x1, MAP_SIZE.w)
  ;[y0, y1] = shift(y0, y1, MAP_SIZE.h)
  return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 }
}

/** Yozuv nuqtaning o'ng tomonida; o'ngda boshqa nuqta yaqin bo'lsa yoki chekka bo'lsa chap tomonda. */
function labelAnchor(id, ids, box, s) {
  const [x, y] = project(PLACES[id].lon, PLACES[id].lat)
  if (x > box.x + box.w - 170 * s) return 'end'
  const crowded = ids.some((o) => {
    if (o === id) return false
    const [ox, oy] = project(PLACES[o].lon, PLACES[o].lat)
    return ox > x && ox - x < 150 * s && Math.abs(oy - y) < 22 * s
  })
  return crowded ? 'end' : 'start'
}

/**
 * Sxematik xarita: shaharlar (nuqta), daryolar, dengizlar va yo'nalish o'qlari. Davlat chegaralari
 * chizilmaydi. `quiz` ({question, answer}) berilsa, talaba shahar belgisini bosib javob beradi.
 */
export default function SchemeMap({ map }) {
  const uid = useId().replace(/:/g, '')
  const [picked, setPicked] = useState(null)
  const points = (map.points || []).filter((id) => PLACES[id])
  const regions = (map.regions || []).filter((id) => REGIONS[id])
  const emphasis = new Set(map.emphasis || [])
  const arrows = (map.arrows || []).filter((a) => PLACES[a.from] && PLACES[a.to])
  const quiz = map.quiz && PLACES[map.quiz.answer] ? map.quiz : null
  const answered = picked !== null
  const box = cropBox(points, regions)
  const s = box.w / 620  // ekrandagi o'lcham doimiy bo'lishi uchun shkala

  return (
    <figure className="card overflow-hidden p-3 sm:p-4">
      <p className="mb-2 flex items-center gap-2 font-display text-base font-bold text-ink">
        <MapPin size={16} className="text-brand" /> {map.title}
      </p>
      <svg
        viewBox={`${box.x.toFixed(0)} ${box.y.toFixed(0)} ${box.w.toFixed(0)} ${box.h.toFixed(0)}`}
        role="img"
        aria-label={`${map.title}. ${map.caption || ''}`}
        className="w-full rounded-lg border border-line bg-surface-2"
      >
        <defs>
          <marker id={`arr${uid}`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth={7} markerHeight={7} orient="auto-start-reverse">
            <path d="M0 0L10 5L0 10z" fill="currentColor" className="text-gold" />
          </marker>
        </defs>

        {SEAS.map((sea) => (
          <g key={sea.name}>
            <path d={`${toPath(sea.coords)}Z`} className="fill-brand/20 stroke-brand/40" strokeWidth="1" />
            <text {...textAt(sea.label)} fontSize={13 * s} className="fill-brand/70 italic">{sea.name}</text>
          </g>
        ))}
        {RIVERS.map((r) => (
          <g key={r.name}>
            <path d={toPath(r.coords)} fill="none" className="stroke-brand/60" strokeWidth={2.2 * s} strokeLinejoin="round" />
            <text {...textAt(r.label)} fontSize={12 * s} className="fill-brand/70 italic">{r.name}</text>
          </g>
        ))}
        {regions.map((id) => (
          <text key={id} {...textAt([REGIONS[id].lon, REGIONS[id].lat])} textAnchor="middle" fontSize={14 * s} className="fill-muted font-semibold uppercase tracking-widest opacity-70">
            {REGIONS[id].name}
          </text>
        ))}

        {arrows.map((a, i) => {
          const [x1, y1] = project(PLACES[a.from].lon, PLACES[a.from].lat)
          const [x2, y2] = project(PLACES[a.to].lon, PLACES[a.to].lat)
          const mx = (x1 + x2) / 2
          const my = (y1 + y2) / 2
          return (
            <g key={i} className="text-gold">
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="currentColor" strokeWidth={2.4 * s} strokeDasharray={`${7 * s} ${4 * s}`} markerEnd={`url(#arr${uid})`} />
              {a.label && (
                <text x={mx} y={my - 7 * s} textAnchor="middle" fontSize={12 * s} className="fill-ink font-semibold" stroke="var(--color-surface-2, #fff)" strokeWidth={3 * s} paintOrder="stroke">
                  {a.label}
                </text>
              )}
            </g>
          )
        })}

        {points.map((id) => {
          const p = PLACES[id]
          const [x, y] = project(p.lon, p.lat)
          const isTarget = answered && quiz?.answer === id
          const isWrong = answered && picked === id && quiz?.answer !== id
          const big = emphasis.has(id) || isTarget
          const anchor = labelAnchor(id, points, box, s)
          return (
            <g
              key={id}
              onClick={quiz && !answered ? () => setPicked(id) : undefined}
              className={quiz && !answered ? 'cursor-pointer' : ''}
              role={quiz && !answered ? 'button' : undefined}
              aria-label={quiz && !answered ? p.name : undefined}
              tabIndex={quiz && !answered ? 0 : undefined}
              onKeyDown={quiz && !answered ? (e) => { if (e.key === 'Enter' || e.key === ' ') setPicked(id) } : undefined}
            >
              {quiz && !answered && <circle cx={x} cy={y} r={18 * s} fill="transparent" />}
              <circle
                cx={x} cy={y} r={(big ? 8 : 5.5) * s}
                className={isTarget ? 'fill-ok stroke-white' : isWrong ? 'fill-bad stroke-white' : big ? 'fill-gold stroke-white' : 'fill-brand stroke-white'}
                strokeWidth={2 * s}
              />
              <text
                x={x + (anchor === 'end' ? -11 * s : 11 * s)} y={y + 4 * s} textAnchor={anchor} fontSize={13 * s}
                className={`${big ? 'font-bold' : 'font-medium'} fill-ink`}
                stroke="var(--color-surface-2, #fff)" strokeWidth={3 * s} paintOrder="stroke"
              >
                {p.name}
              </text>
            </g>
          )
        })}
      </svg>

      {map.caption && <figcaption className="mt-2 text-sm text-muted">{map.caption}</figcaption>}
      <p className="mt-1 text-xs text-muted">Sxema: joylar taxminiy ko'rsatilgan, davlat chegaralari chizilmagan.</p>

      {quiz && (
        <div className="mt-4 border-t border-line pt-4">
          <p className="mb-2 font-read text-base font-medium leading-snug text-ink">{quiz.question}</p>
          {!answered ? (
            <p className="text-sm text-muted">Xaritada shahar belgisini bosing.</p>
          ) : (
            <p role="status" className={`rise text-sm font-semibold ${picked === quiz.answer ? 'text-ok' : 'text-bad'}`}>
              {picked === quiz.answer ? "To'g'ri!" : `Hali emas. To'g'ri javob: ${PLACES[quiz.answer].name} (yashil belgi).`}
              <button type="button" onClick={() => setPicked(null)} className="ml-3 font-normal text-brand underline">Qayta urinish</button>
            </p>
          )}
        </div>
      )}
    </figure>
  )
}

function textAt([lon, lat]) {
  const [x, y] = project(lon, lat)
  return { x, y }
}

