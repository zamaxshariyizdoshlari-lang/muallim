import { CheckCircle2, ListChecks, Plus, Save, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getAdminTopicLesson, getAdminTopicTest, saveAdminTopicLesson, saveAdminTopicTest } from '../../api/client'
import { BackLink, ErrorNote, Spinner } from '../../components/ui'

const TABS = [
  { id: 'lesson', label: 'Dars (tushuntirish)', icon: ListChecks },
  { id: 'test', label: 'Mavzu testi', icon: CheckCircle2 },
]

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

  useEffect(() => {
    setPlan(null)
    getAdminTopicLesson(topicId).then((data) => setPlan(data?.lesson_plan || EMPTY_LESSON)).catch((err) => setError(err.message))
  }, [topicId])

  function updateBlock(i, patch) {
    setPlan((p) => ({ ...p, blocks: p.blocks.map((b, bi) => (bi === i ? { ...b, ...patch } : b)) }))
  }

  async function handleSave() {
    setSaving(true)
    setError('')
    setSaved(false)
    try {
      const clean = { ...plan, blocks: plan.blocks.filter((b) => b.text.trim()) }
      const result = await saveAdminTopicLesson(topicId, clean)
      setPlan(result.lesson_plan)
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
      <p className="-mb-1 text-xs text-muted">
        Matn ichida <code className="rounded bg-surface-2 px-1">**muhim so'z**</code> - qalin qilib,{' '}
        <code className="rounded bg-surface-2 px-1">==testda chiqishi mumkin==</code> - sariq belgilab ko'rsatiladi.
      </p>

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

      <div className="flex items-center gap-3">
        <button onClick={handleSave} disabled={saving} className="btn btn-primary w-fit">
          <Save size={15} /> {saving ? 'Saqlanmoqda...' : 'Saqlash'}
        </button>
        {saved && <span className="text-sm text-ok">Saqlandi</span>}
      </div>
    </div>
  )
}

const QUESTION_TYPES = [
  { id: 'mcq', label: 'Bitta tanlov' },
  { id: 'fill_blank', label: "Bo'sh joy to'ldirish" },
  { id: 'ordering', label: 'Tartiblash' },
]

function emptyQuestion(type = 'mcq') {
  if (type === 'fill_blank') return { type, question: '', answer: '', page: '' }
  if (type === 'ordering') return { type, question: '', items: ['', ''], page: '' }
  return { type: 'mcq', question: '', options: ['', ''], correct_index: 0, page: '' }
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

  function updateItem(qi, ii, value) {
    setQuestions((qs) => qs.map((q, i) => (i !== qi ? q : { ...q, items: q.items.map((v, j) => (j === ii ? value : v)) })))
  }

  function changeType(qi, newType) {
    setQuestions((qs) => qs.map((q, i) => (i === qi ? { ...emptyQuestion(newType), question: q.question, page: q.page } : q)))
  }

  async function handleSave() {
    setSaving(true)
    setError('')
    setSaved(false)
    try {
      const clean = questions.map((q) => {
        const type = q.type || 'mcq'
        const base = { type, question: q.question.trim(), ...(q.page ? { page: Number(q.page) } : {}) }
        if (type === 'fill_blank') return { ...base, answer: (q.answer || '').trim() }
        if (type === 'ordering') return { ...base, items: q.items.map((v) => v.trim()).filter(Boolean) }
        return { ...base, options: q.options.map((o) => o.trim()), correct_index: q.correct_index }
      })
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
      <p className="text-sm text-muted">
        3 xil savol turi mavjud: bitta tanlov (2-6 variant), bo'sh joy to'ldirish (erkin matn javobi)
        va tartiblash (elementlarni to'g'ri tartibda joylashtirish).
      </p>

      {questions.map((q, qi) => {
        const qtype = q.type || 'mcq'
        return (
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

            <div className="ml-10 mb-3 flex gap-1.5">
              {QUESTION_TYPES.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => changeType(qi, t.id)}
                  className={`btn btn-sm !rounded-full !text-xs ${qtype === t.id ? 'btn-primary' : 'btn-ghost'}`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            <div className="ml-10 flex flex-col gap-2">
              {qtype === 'mcq' && (
                <>
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
                </>
              )}

              {qtype === 'fill_blank' && (
                <label className="block text-xs font-medium text-muted">
                  To'g'ri javob (katta-kichik harf va bo'shliqqa sezgir emas)
                  <input
                    className="field mt-1"
                    placeholder="Masalan: 1991"
                    value={q.answer}
                    onChange={(e) => updateQuestion(qi, { answer: e.target.value })}
                  />
                </label>
              )}

              {qtype === 'ordering' && (
                <>
                  <p className="text-xs font-medium text-muted">Elementlarni to'g'ri (kutilgan) tartibda kiriting</p>
                  {q.items.map((item, ii) => (
                    <div key={ii} className="flex items-center gap-2.5">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-paper-2 text-xs font-bold text-ink-2">
                        {ii + 1}
                      </span>
                      <input
                        className="field flex-1"
                        placeholder={`${ii + 1}-element`}
                        value={item}
                        onChange={(e) => updateItem(qi, ii, e.target.value)}
                      />
                      {q.items.length > 2 && (
                        <button
                          onClick={() => updateQuestion(qi, { items: q.items.filter((_, i) => i !== ii) })}
                          className="btn btn-ghost btn-sm !px-2 text-bad"
                        >
                          <Trash2 size={12} />
                        </button>
                      )}
                    </div>
                  ))}
                  {q.items.length < 8 && (
                    <button
                      onClick={() => updateQuestion(qi, { items: [...q.items, ''] })}
                      className="btn btn-ghost btn-sm w-fit !text-xs"
                    >
                      <Plus size={12} /> Element qo'shish
                    </button>
                  )}
                </>
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
        )
      })}

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
