import { Award, Target, TrendingUp, Users } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getAnalytics } from '../api/client'
import { BackLink, ErrorNote, ProgressBar, Spinner } from '../components/ui'

function fmtDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('uz-UZ', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

export default function TeacherPanelPage({ book, onBack }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getAnalytics(book.id).then(setData).catch((err) => setError(err.message))
  }, [book.id])

  if (error) return <ErrorNote>{error}</ErrorNote>
  if (!data) return <Spinner>Yuklanmoqda...</Spinner>

  const { summary, students, hard_questions: hard } = data

  return (
    <div className="rise mx-auto max-w-4xl">
      <BackLink onClick={onBack}>Kursga qaytish</BackLink>
      <header className="mb-8">
        <p className="eyebrow mb-2">O'qituvchi paneli</p>
        <h1 className="font-display text-3xl font-extrabold text-ink sm:text-4xl">{book.title}</h1>
      </header>

      <div className="mb-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Kpi icon={Users} label="Talabalar" value={summary.students} />
        <Kpi icon={TrendingUp} label="O'rtacha o'zlashtirish" value={`${summary.avg_progress}%`} />
        <Kpi icon={Award} label="Sertifikat olganlar" value={summary.certificates} />
        <Kpi icon={Target} label="Jami mavzu" value={summary.total_topics} />
      </div>

      <h2 className="mb-4 font-display text-2xl font-bold text-ink">Talabalar</h2>
      {students.length === 0 ? (
        <p className="card mb-10 p-6 text-sm text-muted">Hali hech kim test topshirmagan.</p>
      ) : (
        <div className="card mb-10 overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs uppercase tracking-wider text-muted">
                <th className="px-4 py-3">Talaba</th>
                <th className="px-4 py-3">O'zlashtirish</th>
                <th className="px-4 py-3">Urinishlar</th>
                <th className="px-4 py-3">Oxirgi faollik</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">
                    <p className="font-semibold text-ink">{s.name || s.username}</p>
                    <p className="text-xs text-muted">
                      @{s.username} {s.certificate && <span className="chip chip-gold ml-1">sertifikat</span>}
                    </p>
                  </td>
                  <td className="w-48 px-4 py-3">
                    <ProgressBar value={s.topics_done} max={summary.total_topics} />
                    <p className="mt-1 text-xs text-muted">
                      {s.topics_done} / {summary.total_topics} mavzu · {s.sections_done} bo'lim
                    </p>
                  </td>
                  <td className="px-4 py-3 text-ink-2">{s.attempts}</td>
                  <td className="px-4 py-3 text-ink-2">{fmtDate(s.last_active)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2 className="mb-1 font-display text-2xl font-bold text-ink">Eng qiyin savollar</h2>
      <p className="mb-4 text-sm text-muted">Kamida 3 marta javob berilgan va eng ko'p xato qilingan savollar.</p>
      {hard.length === 0 ? (
        <p className="card p-6 text-sm text-muted">Hozircha yetarli ma'lumot yo'q.</p>
      ) : (
        <ol className="flex flex-col gap-3">
          {hard.map((h, i) => (
            <li key={i} className="card flex items-start gap-4 p-4">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-bad-soft text-sm font-bold text-bad">
                {h.error_rate}%
              </span>
              <div className="min-w-0 flex-1">
                <p className="font-read text-base font-medium leading-snug text-ink">{h.question}</p>
                <p className="mt-1 text-xs text-muted">
                  {h.topic_title} {h.page && `· bet ${h.page}`} · {h.wrong}/{h.seen} xato
                </p>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}

function Kpi({ icon: Icon, label, value }) {
  return (
    <div className="card p-4">
      <Icon size={18} className="text-gold" />
      <p className="mt-2 font-display text-2xl font-extrabold text-ink">{value}</p>
      <p className="text-xs text-muted">{label}</p>
    </div>
  )
}
