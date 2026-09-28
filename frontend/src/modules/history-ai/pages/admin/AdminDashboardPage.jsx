import { Ban, BookOpen, CheckCircle2, Flame, Search, ShieldCheck, ShieldOff, Users } from 'lucide-react'
import { useEffect, useState } from 'react'
import { adminStudentAction, getAdminStats, getAdminStudents } from '../../api/client'
import { ErrorNote, Spinner } from '../../components/ui'

export default function AdminDashboardPage({ onOpenStudent, onOpenContent }) {
  const [stats, setStats] = useState(null)
  const [students, setStudents] = useState(null)
  const [q, setQ] = useState('')
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  useEffect(() => {
    getAdminStats().then(setStats).catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    const id = setTimeout(() => {
      getAdminStudents(q).then(setStudents).catch((err) => setError(err.message))
    }, 250)
    return () => clearTimeout(id)
  }, [q])

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

  return (
    <div className="rise">
      <header className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="eyebrow mb-2">Boshqaruv paneli</p>
          <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">
            Platforma statistikasi
          </h1>
        </div>
        <button onClick={onOpenContent} className="btn btn-ghost btn-sm">
          <BookOpen size={15} /> Fanlar va kurslar
        </button>
      </header>

      <ErrorNote>{error}</ErrorNote>

      {!stats ? (
        <Spinner>Yuklanmoqda...</Spinner>
      ) : (
        <div className="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard icon={Users} label="Talabalar" value={stats.students_total} hint={`Bugun faol: ${stats.students_active_today}`} />
          <StatCard icon={Flame} label="So'nggi 7 kun" value={stats.new_registrations_7d} hint="yangi ro'yxatdan o'tgan" />
          <StatCard icon={ShieldCheck} label="Fanlar / kurslar" value={`${stats.subjects_total} / ${stats.books_total}`} hint={stats.most_popular_book ? `Mashhur: ${stats.most_popular_book}` : ''} />
          <StatCard icon={CheckCircle2} label="Sertifikatlar" value={stats.certificates_total} hint={`${stats.test_attempts_total} ta urinish`} />
        </div>
      )}

      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-display text-xl font-bold text-ink">Talabalar nazorati</h2>
        <div className="relative w-full max-w-xs">
          <Search size={15} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input
            className="field pl-9"
            placeholder="Ism, login yoki email bo'yicha qidirish"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
      </div>

      {!students ? (
        <Spinner>Yuklanmoqda...</Spinner>
      ) : students.length === 0 ? (
        <p className="card p-6 text-sm text-muted">Hech kim topilmadi.</p>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs uppercase tracking-wide text-muted">
                <th className="px-4 py-3 font-semibold">Talaba</th>
                <th className="px-4 py-3 font-semibold">Ball</th>
                <th className="px-4 py-3 font-semibold">Mavzu</th>
                <th className="px-4 py-3 font-semibold">Sertifikat</th>
                <th className="px-4 py-3 font-semibold">Oxirgi faollik</th>
                <th className="px-4 py-3 font-semibold">Holat</th>
                <th className="px-4 py-3 font-semibold">Amal</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {students.map((s) => (
                <tr key={s.id} className={!s.is_active ? 'opacity-50' : ''}>
                  <td className="px-4 py-3">
                    <button onClick={() => onOpenStudent(s.id)} className="font-semibold text-ink hover:text-brand hover:underline">
                      {s.first_name || s.username}
                    </button>
                    <p className="text-xs text-muted">@{s.username}{s.is_staff && ' · admin'}</p>
                  </td>
                  <td className="px-4 py-3 font-semibold text-ink">{s.xp}</td>
                  <td className="px-4 py-3 text-ink-2">{s.topics_done}</td>
                  <td className="px-4 py-3 text-ink-2">{s.certs_count}</td>
                  <td className="px-4 py-3 text-ink-2">{s.last_activity || '—'}</td>
                  <td className="px-4 py-3">
                    {s.is_active ? (
                      <span className="chip !border-ok/40 !bg-ok-soft !text-ok">Faol</span>
                    ) : (
                      <span className="chip !border-bad/40 !bg-bad-soft !text-bad">Bloklangan</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1.5">
                      <button
                        title={s.is_active ? 'Bloklash' : 'Faollashtirish'}
                        disabled={busyId === s.id}
                        onClick={() => handleAction(s.id, s.is_active ? 'deactivate' : 'activate')}
                        className="btn btn-ghost btn-sm !px-2"
                      >
                        {s.is_active ? <Ban size={15} className="text-bad" /> : <CheckCircle2 size={15} className="text-ok" />}
                      </button>
                      <button
                        title={s.is_staff ? "Admin huquqini olib qo'yish" : 'Admin huquqi berish'}
                        disabled={busyId === s.id}
                        onClick={() => handleAction(s.id, s.is_staff ? 'revoke_staff' : 'grant_staff')}
                        className="btn btn-ghost btn-sm !px-2"
                      >
                        {s.is_staff ? <ShieldOff size={15} /> : <ShieldCheck size={15} />}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon: Icon, label, value, hint }) {
  return (
    <div className="card p-5">
      <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-xl bg-brand-soft text-brand">
        <Icon size={18} />
      </div>
      <p className="font-display text-2xl font-extrabold text-ink">{value}</p>
      <p className="text-sm font-medium text-ink-2">{label}</p>
      {hint && <p className="mt-1 text-xs text-muted">{hint}</p>}
    </div>
  )
}
