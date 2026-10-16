import { CheckCircle2, ChevronRight, Eye, Lightbulb, RotateCcw, XCircle } from 'lucide-react'
import { useState } from 'react'
import { ProgressBar } from './ui'

/* ---------- javobni tekshirish ---------- */

function normalize(s) {
  return String(s ?? '')
    .toLowerCase()
    .replace(/[−–—]/g, '-')
    .replace(/(\d),(\d)/g, '$1.$2')
    .replace(/\s+/g, '')
}

function toNumber(s) {
  const t = normalize(s)
  const frac = t.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/)
  if (frac) return Number(frac[1]) / Number(frac[2])
  if (/^-?\d+(?:\.\d+)?$/.test(t)) return Number(t)
  return null
}

function sameSingle(a, b) {
  const na = toNumber(a)
  const nb = toNumber(b)
  if (na !== null && nb !== null) return Math.abs(na - nb) < 1e-6
  return normalize(a) === normalize(b)
}

/** answer: matn yoki variantlar ro'yxati. ';' bilan ajratilgan to'plam javoblarda tartib ahamiyatsiz. */
export function checkAnswer(input, answer) {
  const accepted = Array.isArray(answer) ? answer : [answer]
  return accepted.some((acc) => {
    if (String(acc).includes(';')) {
      const a = String(input).split(';').map(normalize).filter(Boolean).sort()
      const b = String(acc).split(';').map(normalize).filter(Boolean).sort()
      return a.length === b.length && a.every((x, i) => x === b[i] || sameSingle(x, b[i]))
    }
    return sameSingle(input, acc)
  })
}

function Result({ score, total, onReset }) {
  return (
    <div className="rise py-4 text-center">
      <p className="eyebrow mb-1">Natija</p>
      <p className="font-display text-5xl font-extrabold text-brand">
        {score} <span className="text-muted">/ {total}</span>
      </p>
      <p className="mt-2 text-sm text-ink-2">
        {score === total ? "Ajoyib! Hammasini o'zingiz yechdingiz." : "Yaxshi urinish! Xatolarni yechimlar bilan solishtirib, yana bir bor yeching."}
      </p>
      <button onClick={onReset} className="btn btn-ghost mt-5">
        <RotateCcw size={14} /> Qaytadan boshlash
      </button>
    </div>
  )
}

/* ---------- formulalar ---------- */

export function FormulaCards({ items }) {
  if (!items?.length) return null
  return (
    <ul className="grid gap-3 sm:grid-cols-2">
      {items.map((f, i) => (
        <li key={i} className="card p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted">{f.name}</p>
          <p className="mt-2 break-words rounded-lg bg-brand/5 px-3 py-2 font-mono text-lg font-semibold text-brand">{f.formula}</p>
          {f.note && <p className="mt-2 text-sm text-ink-2">{f.note}</p>}
        </li>
      ))}
    </ul>
  )
}

/* ---------- yechilgan misollar (qadamma-qadam) ---------- */

function WorkedExample({ item, index }) {
  const [shown, setShown] = useState(0)
  const steps = item.steps || []
  const done = shown >= steps.length
  return (
    <div className="card p-5 sm:p-6">
      <p className="eyebrow mb-1">Misol {index + 1}</p>
      <p className="font-read text-lg font-medium leading-snug text-ink">{item.problem}</p>
      <ol className="mt-4 flex flex-col gap-2">
        {steps.slice(0, shown).map((s, i) => (
          <li key={i} className="rise flex gap-3 rounded-lg border border-line bg-paper px-3 py-2 text-[0.95rem] text-ink-2">
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand text-xs font-bold text-brand-ink">{i + 1}</span>
            <span className="whitespace-pre-wrap font-mono text-sm leading-relaxed">{s}</span>
          </li>
        ))}
      </ol>
      {!done && (
        <button onClick={() => setShown((n) => n + 1)} className="btn btn-ghost btn-sm mt-3">
          <ChevronRight size={14} /> {shown === 0 ? 'Yechimni boshlash' : 'Keyingi qadam'}
        </button>
      )}
      {done && item.answer && (
        <p className="rise mt-4 rounded-lg border border-ok/40 bg-ok-soft px-3 py-2 text-sm font-semibold text-ok">
          Javob: {item.answer}
        </p>
      )}
    </div>
  )
}

export function WorkedExamples({ items }) {
  if (!items?.length) return null
  return (
    <div className="flex flex-col gap-4">
      {items.map((it, i) => <WorkedExample key={i} item={it} index={i} />)}
    </div>
  )
}

/* ---------- mustaqil masalalar: javob kiritiladi ---------- */

function ProblemItem({ item, onDone }) {
  const [value, setValue] = useState('')
  const [status, setStatus] = useState(null) // null | 'ok' | 'bad'
  const [hint, setHint] = useState(false)
  const [solution, setSolution] = useState(false)

  function submit(e) {
    e.preventDefault()
    if (!value.trim() || status) return
    const ok = checkAnswer(value, item.answer)
    setStatus(ok ? 'ok' : 'bad')
    if (ok) onDone(true)
  }

  function giveUp() {
    setSolution(true)
    if (!status) { setStatus('bad'); onDone(false) }
  }

  const shownAnswer = Array.isArray(item.answer) ? item.answer[0] : item.answer

  return (
    <div>
      <p className="mb-4 font-read text-lg font-medium leading-snug text-ink">{item.question}</p>
      <form onSubmit={submit} className="flex flex-wrap items-center gap-2">
        <input
          value={value}
          onChange={(e) => { setValue(e.target.value); if (status === 'bad' && !solution) setStatus(null) }}
          disabled={status === 'ok'}
          placeholder="Javobingizni yozing..."
          className="field min-w-0 flex-1 font-mono"
          autoComplete="off"
        />
        {item.unit && <span className="text-sm text-muted">{item.unit}</span>}
        <button type="submit" disabled={!value.trim() || status === 'ok'} className="btn btn-primary btn-sm">Tekshirish</button>
      </form>
      {item.format && <p className="mt-2 text-xs text-muted">Javob shakli: {item.format}</p>}
      {status === 'ok' && (
        <p className="rise mt-3 flex items-center gap-2 text-sm font-semibold text-ok"><CheckCircle2 size={16} /> To'g'ri!</p>
      )}
      {status === 'bad' && !solution && (
        <p className="rise mt-3 flex items-center gap-2 text-sm font-semibold text-bad"><XCircle size={16} /> Hali to'g'ri emas. Qayta urinib ko'ring yoki maslahatni oching.</p>
      )}
      <div className="mt-3 flex flex-wrap gap-2">
        {item.hint && status !== 'ok' && (
          <button type="button" onClick={() => setHint(true)} className="btn btn-ghost btn-sm"><Lightbulb size={14} /> Maslahat</button>
        )}
        {!solution && (
          <button type="button" onClick={giveUp} className="btn btn-ghost btn-sm"><Eye size={14} /> {status === 'ok' ? "Yechimni ko'rish" : "Yechimni ko'rsat"}</button>
        )}
      </div>
      {hint && item.hint && status !== 'ok' && <p className="rise mt-3 rounded-lg bg-gold-soft/50 px-3 py-2 text-sm text-ink-2">{item.hint}</p>}
      {solution && (
        <div className="rise mt-3 rounded-lg border border-line bg-paper px-3 py-3 text-sm text-ink-2">
          <p className="font-semibold text-ink">Javob: {shownAnswer}</p>
          {item.solution && <p className="mt-1 whitespace-pre-wrap font-mono leading-relaxed">{item.solution}</p>}
        </div>
      )}
    </div>
  )
}

export function ProblemSolver({ items }) {
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [answered, setAnswered] = useState(false)
  if (!items?.length) return null
  const finished = index >= items.length

  function reset() { setIndex(0); setScore(0); setAnswered(false) }
  if (finished) return <Result score={score} total={items.length} onReset={reset} />

  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <span className="chip">Masala {index + 1} / {items.length}</span>
        <ProgressBar value={index} max={items.length} />
      </div>
      <ProblemItem
        key={index}
        item={items[index]}
        onDone={(ok) => { setAnswered(true); if (ok) setScore((s) => s + 1) }}
      />
      <button
        onClick={() => { setIndex((i) => i + 1); setAnswered(false) }}
        className={`btn mt-5 ${answered ? 'btn-primary' : 'btn-ghost'}`}
      >
        {index + 1 === items.length ? 'Yakunlash' : answered ? 'Keyingi masala' : "O'tkazib yuborish"}
      </button>
    </div>
  )
}

/* ---------- kod: natijani toping ---------- */

function CodeBlock({ code }) {
  return (
    <pre className="overflow-x-auto rounded-xl border border-line bg-ink px-4 py-3 font-mono text-sm leading-relaxed text-paper">
      <code>{code}</code>
    </pre>
  )
}

function TraceItem({ item, onDone }) {
  const [value, setValue] = useState('')
  const [status, setStatus] = useState(null)

  function submit(e) {
    e.preventDefault()
    if (!value.trim() || status) return
    const ok = normalizeOutput(value) === normalizeOutput(Array.isArray(item.answer) ? item.answer[0] : item.answer)
      || (Array.isArray(item.answer) && item.answer.some((a) => normalizeOutput(value) === normalizeOutput(a)))
    setStatus(ok ? 'ok' : 'bad')
    onDone(ok)
  }

  return (
    <div>
      {item.title && <p className="mb-2 text-sm font-semibold text-muted">{item.title}</p>}
      <CodeBlock code={item.code} />
      <p className="mt-4 font-read text-lg font-medium leading-snug text-ink">{item.question}</p>
      <form onSubmit={submit} className="mt-3 flex flex-wrap items-start gap-2">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={Boolean(status)}
          rows={item.lines || 1}
          placeholder="Dastur nimani chiqaradi?"
          className="field min-w-0 flex-1 font-mono"
        />
        <button type="submit" disabled={!value.trim() || Boolean(status)} className="btn btn-primary btn-sm">Tekshirish</button>
      </form>
      {status && (
        <div className={`rise mt-3 rounded-lg border px-3 py-3 text-sm ${status === 'ok' ? 'border-ok/40 bg-ok-soft text-ok' : 'border-bad/40 bg-bad-soft text-bad'}`}>
          <p className="font-semibold">{status === 'ok' ? "To'g'ri!" : "To'g'ri chiqish:"}</p>
          {status === 'bad' && <pre className="mt-1 font-mono text-ink">{Array.isArray(item.answer) ? item.answer[0] : item.answer}</pre>}
          {item.explanation && <p className="mt-2 text-ink-2">{item.explanation}</p>}
        </div>
      )}
    </div>
  )
}

function normalizeOutput(s) {
  return String(s ?? '').split('\n').map((l) => l.trim().replace(/\s+/g, ' ')).filter(Boolean).join('\n').toLowerCase()
}

export function CodeTrace({ items }) {
  const [index, setIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [answered, setAnswered] = useState(false)
  if (!items?.length) return null
  if (index >= items.length) return <Result score={score} total={items.length} onReset={() => { setIndex(0); setScore(0); setAnswered(false) }} />
  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <span className="chip">Kod {index + 1} / {items.length}</span>
        <ProgressBar value={index} max={items.length} />
      </div>
      <TraceItem key={index} item={items[index]} onDone={(ok) => { setAnswered(true); if (ok) setScore((s) => s + 1) }} />
      {answered && (
        <button onClick={() => { setIndex((i) => i + 1); setAnswered(false) }} className="btn btn-primary mt-5">
          {index + 1 === items.length ? 'Yakunlash' : 'Keyingi kod'}
        </button>
      )}
    </div>
  )
}
