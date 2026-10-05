import { Ban, CheckCircle2, ChevronDown, ChevronUp, Search, ShieldCheck, ShieldOff } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { adminStudentAction, getAdminStudents } from '../../api/client'
import { ErrorNote, Spinner } from '../../components/ui'

const DAY = 86400000
const daysSince = (d) => (d ? Math.floor((Date.now() - new Date(d).getTime()) / DAY) : null)

function status(s) {
  if (!s.is_active) return 'blocked'
  const d = daysSince(s.last_activity)
  if (d === null) return 'new'
  return d <= 7 ? 'active' : 'idle'
}

const STATUS = {
  active: { label: 'Faol', cls: '!border-ok/40 !bg-ok-soft !text-ok' },
  idle: { label: 'Faolsiz', cls: '!border-gold/40 !bg-gold-soft !text-gold' },
  new: { label: 'Boshlamagan', cls: '' },
  blocked: { label: 'Bloklangan', cls: '!border-bad/40 !bg-bad-soft !text-bad' },
}

const FILTERS = [['all', 'Hammasi'], ['active', 'Faol'], ['idle', 'Faolsiz'], ['new', 'Boshlamagan'], ['blocked', 'Bloklangan']]

const fmtTime = (sec) => (sec >= 3600 ? `${Math.floor(sec / 3600)} s ${Math.round((sec % 3600) / 60)} d` : `${Math.round(sec / 60)} daq`)

export default function AdminStudentsPage() {
  const navigate = useNavigate()
  const [students, setStudents] = useState(null)
  const [q, setQ] = useState('')
  const [filter, setFilter] = useState('all')
  const [sort, setSort] = useState({ key: 'last_activity', dir: -1 })
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  useEffect(() => {
    const id = setTimeout(() => {
      getAdminStudents(q).then(setStudents).catch((err) => setError(err.message))
    }, 250)
    return () => clearTimeout(id)
  }, [q])

  const rows = useMemo(() => {
    if (!students) return null
    const list = students.filter((s) => filter === 'all' || status(s) === filter)
    const { key, dir } = sort
    return [...list].sort((a, b) => {
      const x = a[key] ?? ''
      const y = b[key] ?? ''
      return (x > y ? 1 : x < y ? -1 : 0) * dir
    })
  }, [students, filter, sort])

  const counts = useMemo(() => {
    const c = { all: students?.length || 0 }
    ;(students || []).forEach((s) => { c[status(s)] = (c[status(s)] || 0) + 1 })
    return c
  }, [students])

  async function handleAction(id, action) {
    setBusyId(id)
    setError('')
    try {
      const result = await adminStudentAction(id, action)
      setStudents((list) => list.map((s) => (s.id === id ? { ...s, ...result } : s)))
    } catch (err) {
      setError(err.message)
    } finally {
      setBusyId(null)
    }
  }

  const Th = ({ k, children }) => (
    <th className="px-4 py-3 font-semibold" aria-sort={sort.key === k ? (sort.dir > 0 ? 'ascending' : 'descending') : 'none'}>
      <button type="button" onClick={() => setSort((s) => ({ key: k, dir: s.key === k ? -s.dir : -1 }))} className="inline-flex items-center gap-1 uppercase hover:text-ink">
        {children}
        {sort.key === k && (sort.dir > 0 ? <ChevronUp size={12} /> : <ChevronDown size={12} />)}
      </button>
    </th>
  )

  return (
    <div className="rise">
      <header className="mb-5">
        <p className="eyebrow mb-1">Nazorat</p>
        <h1 className="font-display text-3xl font-extrabold text-ink">Talabalar</h1>
      </header>
      <ErrorNote>{error}</ErrorNote>

      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap gap-1.5" role="group" aria-label="Holat bo'yicha filtr">
          {FILTERS.map(([k, label]) => (
            <button
              key={k} type="button" onClick={() => setFilter(k)} aria-pressed={filter === k}
              className={`chip ${filter === k ? '!border-chalk !bg-chalk !text-white' : ''}`}
            >
              {label} <span className="opacity-70">{counts[k] || 0}</span>
            </button>
          ))}
        </div>
        <div className="relative w-full max-w-xs">
          <Search size={15} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input className="field pl-9" placeholder="Ism, login yoki email" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
      </div>

      {!rows ? <Spinner>Yuklanmoqda...</Spinner> : rows.length === 0 ? (
        <p className="card p-6 text-sm text-muted">Hech kim topilmadi.</p>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full min-w-[820px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs tracking-wide text-muted">
                <Th k="first_name">Talaba</Th>
                <Th k="xp">Ball</Th>
                <Th k="topics_done">Mavzu</Th>
                <Th k="certs_count">Sertifikat</Th>
                <Th k="total_seconds">Vaqt</Th>
                <Th k="last_activity">Oxirgi faollik</Th>
                <th className="px-4 py-3 font-semibold uppercase">Holat</th>
                <th className="px-4 py-3 font-semibold uppercase">Amal</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {rows.map((s) => {
                const st = STATUS[status(s)]
                return (
                  <tr key={s.id} className={`hover:bg-paper-2/60 ${!s.is_active ? 'opacity-60' : ''}`}>
                    <td className="px-4 py-3">
                      <button onClick={() => navigate(`/boshqaruv/talaba/${s.id}`)} className="font-semibold text-ink hover:text-brand hover:underline">
                        {s.first_name || s.username}
                      </button>
                      <p className="text-xs text-muted">@{s.username}</p>
                    </td>
                    <td className="px-4 py-3 font-semibold tabular-nums text-ink">{s.xp}</td>
                    <td className="px-4 py-3 tabular-nums text-ink-2">{s.topics_done}</td>
                    <td className="px-4 py-3 tabular-nums text-ink-2">{s.certs_count}</td>
                    <td className="px-4 py-3 text-ink-2">{s.total_seconds ? fmtTime(s.total_seconds) : '—'}</td>
                    <td className="px-4 py-3 text-ink-2">{s.last_activity || '—'}</td>
                    <td className="px-4 py-3"><span className={`chip ${st.cls}`}>{st.label}</span></td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-1.5">
                        <button
                          title={s.is_active ? 'Bloklash' : 'Faollashtirish'} disabled={busyId === s.id}
                          onClick={() => handleAction(s.id, s.is_active ? 'deactivate' : 'activate')} className="btn btn-ghost btn-sm !px-2"
                        >
                          {s.is_active ? <Ban size={15} className="text-bad" /> : <CheckCircle2 size={15} className="text-ok" />}
                        </button>
                        <button
                          title={s.is_staff ? "Admin huquqini olib qo'yish" : 'Admin huquqi berish'} disabled={busyId === s.id}
                          onClick={() => handleAction(s.id, s.is_staff ? 'revoke_staff' : 'grant_staff')} className="btn btn-ghost btn-sm !px-2"
                        >
                          {s.is_staff ? <ShieldOff size={15} /> : <ShieldCheck size={15} />}
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
