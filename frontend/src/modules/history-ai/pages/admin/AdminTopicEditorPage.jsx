import { CheckCircle2, ListChecks, Plus, Save, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getAdminTopicLesson, getAdminTopicTest, saveAdminTopicLesson, saveAdminTopicTest } from '../../api/client'
import { BackLink, ErrorNote, Spinner } from '../../components/ui'

const TABS = [
  { id: 'lesson', label: 'Dars (tushuntirish)', icon: ListChecks },
  { id: 'test', label: 'Mavzu testi', icon: CheckCircle2 },
]

// Dars sifatini oshiruvchi ixtiyoriy qismlar: JSON ko'rinishida tahrirlanadi
const EXTRA_KEYS = ['pretest', 'why', 'source_work', 'images']
const EXTRAS_HINT = `{
  "pretest": [{ "question": "...", "options": ["A", "B"], "correct_index": 0 }],
  "why": { "causes": ["Sabab 1"], "effects": ["Natija 1"] },
  "source_work": { "quote": "Manba matni", "attribution": "Muallif", "question": "...", "options": ["A", "B"], "correct_index": 0 },
  "images": [{ "src": "/maps/misr.svg", "caption": "Qadimgi Misr xaritasi" }]
}`
const pickExtras = (plan) => Object.fromEntries(EXTRA_KEYS.filter((k) => plan?.[k]).map((k) => [k, plan[k]]))

const EMPTY_LESSON = { goals: [], blocks: [{ heading: '', text: '', pages: [] }], key_facts: [], summary: '' }

export default function AdminTopicEditorPage({ topicId, topicTitle, onBack }) {
  const [tab, setTab] = useState('lesson')

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Bo'lim/mavzularga qaytish</BackLink>
      <header className="mb-6">
        <p className="eyebrow mb-2">Mavzu tahriri</p>
        <h1 className="font-display text-3xl font-extrabold text-ink">{topicTitle}</h1>
      </header>

      <div className="mb-6 flex gap-2">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setTab(id)}
            className={`btn btn-sm !rounded-full ${tab === id ? 'btn-primary' : 'btn-ghost'}`}
          >
            <Icon size={14} /> {label}
          </button>
        ))}
      </div>

      {tab === 'lesson' ? <LessonEditor topicId={topicId} /> : <TestEditor topicId={topicId} />}
    </div>
  )
}

function LessonEditor({ topicId }) {
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [saving, setSaving] = useState(false)
  const [extrasText, setExtrasText] = useState('')

  useEffect(() => {
    setPlan(null)
    getAdminTopicLesson(topicId)
      .then((data) => {
        const loaded = data?.lesson_plan || EMPTY_LESSON
        setPlan(loaded)
        const extras = pickExtras(loaded)
        setExtrasText(Object.keys(extras).length ? JSON.stringify(extras, null, 2) : '')
      })
      .catch((err) => setError(err.message))
  }, [topicId])

  function updateBlock(i, patch) {
    setPlan((p) => ({ ...p, blocks: p.blocks.map((b, bi) => (bi === i ? { ...b, ...patch } : b)) }))
  }

  async function handleSave() {
    setSaving(true)
    setError('')
    setSaved(false)
    try {
      let extras = {}
      if (extrasText.trim()) {
        try {
          extras = JSON.parse(extrasText)
        } catch {
          throw new Error("Boyituvchi qismlar to'g'ri JSON emas")
        }
      }
      const base = { ...plan }
      EXTRA_KEYS.forEach((k) => delete base[k])  // o'chirilgan qism bo'sh yuboriladi
      const clean = { ...base, ...Object.fromEntries(EXTRA_KEYS.map((k) => [k, extras[k] ?? null])), blocks: plan.blocks.filter((b) => b.text.trim()) }
      const result = await saveAdminTopicLesson(topicId, clean)
      setPlan(result.lesson_plan)
      setExtrasText(Object.keys(pickExtras(result.lesson_plan)).length ? JSON.stringify(pickExtras(result.lesson_plan), null, 2) : '')
      setSaved(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (!plan) return error ? <ErrorNote>{error}</ErrorNote> : <Spinner>Yuklanmoqda...</Spinner>

  return (
    <div className="flex flex-col gap-5">
      <ErrorNote>{error}</ErrorNote>

      <div className="card p-5 sm:p-6">
        <label className="mb-2 block text-sm font-semibold text-ink-2">
          Maqsadlar (har biri alohida qatorda)
        </label>
        <textarea
          className="field min-h-[80px]"
          value={plan.goals.join('\n')}
          onChange={(e) => setPlan((p) => ({ ...p, goals: e.target.value.split('\n') }))}
        />
      </div>

      {plan.blocks.map((block, i) => (
        <div key={i} className="card p-5 sm:p-6">
          <div className="mb-3 flex items-center justify-between gap-3">
            <input
              className="field flex-1"
              placeholder="Blok sarlavhasi (ixtiyoriy)"
              value={block.heading}
              onChange={(e) => updateBlock(i, { heading: e.target.value })}
            />
            <button
              onClick={() => setPlan((p) => ({ ...p, blocks: p.blocks.filter((_, bi) => bi !== i) }))}
              className="btn btn-ghost btn-sm !px-2 text-bad"
            >
              <Trash2 size={14} />
            </button>
          </div>
          <textarea
            className="field mb-3 min-h-[120px]"
            placeholder="Matn"
            value={block.text}
            onChange={(e) => updateBlock(i, { text: e.target.value })}
          />
          <label className="block text-xs font-medium text-muted">
            Manba betlari (vergul bilan, masalan: 5, 6)
            <input
              className="field mt-1"
              value={(block.pages || []).join(', ')}
              onChange={(e) => updateBlock(i, {
                pages: e.target.value.split(',').map((v) => parseInt(v.trim(), 10)).filter(Number.isFinite),
              })}
            />
          </label>
        </div>
      ))}

      <button
        onClick={() => setPlan((p) => ({ ...p, blocks: [...p.blocks, { heading: '', text: '', pages: [] }] }))}
        className="btn btn-ghost btn-sm w-fit"
      >
        <Plus size={14} /> Blok qo'shish
      </button>

      <div className="card p-5 sm:p-6">
        <label className="mb-2 block text-sm font-semibold text-ink-2">Xulosa (ixtiyoriy)</label>
        <textarea
          className="field min-h-[80px]"
          value={plan.summary}
          onChange={(e) => setPlan((p) => ({ ...p, summary: e.target.value }))}
        />
      </div>

      <details className="card p-5 sm:p-6" open={Boolean(extrasText)}>
        <summary className="cursor-pointer text-sm font-semibold text-ink-2">
          Boyituvchi qismlar (ixtiyoriy, JSON): oldindan sinash, "Nega?", manba, rasm/xarita
        </summary>
        <textarea
          className="field mt-3 min-h-[160px] font-mono text-xs"
          placeholder={EXTRAS_HINT}
          value={extrasText}
          onChange={(e) => setExtrasText(e.target.value)}
          spellCheck={false}
        />
        <p className="mt-2 text-xs text-muted">
          Bo'sh qoldirsangiz, bu qismlar ko'rsatilmaydi. Blok ichidagi mini-savol bo'lmasa, mini-viktorinadan avtomatik olinadi.
        </p>
      </details>

      <div className="flex items-center gap-3">
        <button onClick={handleSave} disabled={saving} className="btn btn-primary w-fit">
          <Save size={15} /> {saving ? 'Saqlanmoqda...' : 'Saqlash'}
        </button>
        {saved && <span className="text-sm text-ok">Saqlandi</span>}
      </div>
    </div>
  )
}

function emptyQuestion() {
  return { question: '', options: ['', ''], correct_index: 0, page: '' }
}

function TestEditor({ topicId }) {
  const [questions, setQuestions] = useState(null)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    setQuestions(null)
    getAdminTopicTest(topicId).then((data) => setQuestions(data?.questions?.length ? data.questions : [emptyQuestion()]))
      .catch((err) => setError(err.message))
  }, [topicId])

  function updateQuestion(i, patch) {
    setQuestions((qs) => qs.map((q, qi) => (qi === i ? { ...q, ...patch } : q)))
  }

  function updateOption(qi, oi, value) {
    setQuestions((qs) => qs.map((q, i) => (i !== qi ? q : { ...q, options: q.options.map((o, j) => (j === oi ? value : o)) })))
  }

  async function handleSave() {
    setSaving(true)
    setError('')
    setSaved(false)
    try {
      const clean = questions.map((q) => ({
        question: q.question.trim(),
        options: q.options.map((o) => o.trim()),
        correct_index: q.correct_index,
        ...(q.page ? { page: Number(q.page) } : {}),
      }))
      const result = await saveAdminTopicTest(topicId, clean)
      setQuestions(result.questions)
      setSaved(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (!questions) return error ? <ErrorNote>{error}</ErrorNote> : <Spinner>Yuklanmoqda...</Spinner>

  return (
    <div className="flex flex-col gap-5">
      <ErrorNote>{error}</ErrorNote>
      <p className="text-sm text-muted">Har bir savolda 2–6 variant bo'lishi va to'g'ri javob belgilanishi shart.</p>

      {questions.map((q, qi) => (
        <div key={qi} className="card p-5 sm:p-6">
          <div className="mb-3 flex items-start justify-between gap-3">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-soft text-sm font-bold text-brand">
              {qi + 1}
            </span>
            <textarea
              className="field flex-1"
              placeholder="Savol matni"
              value={q.question}
              onChange={(e) => updateQuestion(qi, { question: e.target.value })}
            />
            <button
              onClick={() => setQuestions((qs) => qs.filter((_, i) => i !== qi))}
              className="btn btn-ghost btn-sm !px-2 text-bad"
            >
              <Trash2 size={14} />
            </button>
          </div>

          <div className="ml-10 flex flex-col gap-2">
            {q.options.map((opt, oi) => (
              <label key={oi} className="flex items-center gap-2.5">
                <input
                  type="radio"
                  name={`correct-${qi}`}
                  checked={q.correct_index === oi}
                  onChange={() => updateQuestion(qi, { correct_index: oi })}
                />
                <input
                  className="field flex-1"
                  placeholder={`Variant ${String.fromCharCode(65 + oi)}`}
                  value={opt}
                  onChange={(e) => updateOption(qi, oi, e.target.value)}
                />
                {q.options.length > 2 && (
                  <button
                    onClick={() => updateQuestion(qi, {
                      options: q.options.filter((_, i) => i !== oi),
                      correct_index: q.correct_index >= oi && q.correct_index > 0 ? q.correct_index - 1 : q.correct_index,
                    })}
                    className="btn btn-ghost btn-sm !px-2 text-bad"
                  >
                    <Trash2 size={12} />
                  </button>
                )}
              </label>
            ))}
            {q.options.length < 6 && (
              <button
                onClick={() => updateQuestion(qi, { options: [...q.options, ''] })}
                className="btn btn-ghost btn-sm w-fit !text-xs"
              >
                <Plus size={12} /> Variant qo'shish
              </button>
            )}
            <label className="mt-1 block w-40 text-xs font-medium text-muted">
              Bet (ixtiyoriy)
              <input
                type="number"
                className="field mt-1"
                value={q.page}
                onChange={(e) => updateQuestion(qi, { page: e.target.value })}
              />
            </label>
          </div>
        </div>
      ))}

      <button onClick={() => setQuestions((qs) => [...qs, emptyQuestion()])} className="btn btn-ghost btn-sm w-fit">
        <Plus size={14} /> Savol qo'shish
      </button>

      <div className="flex items-center gap-3">
        <button onClick={handleSave} disabled={saving} className="btn btn-primary w-fit">
          <Save size={15} /> {saving ? 'Saqlanmoqda...' : 'Saqlash'}
        </button>
        {saved && <span className="text-sm text-ok">Saqlandi</span>}
      </div>
    </div>
  )
}
