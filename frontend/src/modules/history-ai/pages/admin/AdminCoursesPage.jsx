import { ArrowLeft, Pencil } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getAdminCourse, getAdminCourses } from '../../api/client'
import { Meter, toneFor } from '../../components/admin/Charts'
import { ErrorNote, Spinner } from '../../components/ui'

export function AdminCoursesPage() {
  const [courses, setCourses] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => { getAdminCourses().then(setCourses).catch((e) => setError(e.message)) }, [])
  return (
    <div className="rise">
      <header className="mb-5">
        <p className="eyebrow mb-1">Tahlil</p>
        <h1 className="font-display text-3xl font-extrabold text-ink">Kurslar tahlili</h1>
      </header>
      <ErrorNote>{error}</ErrorNote>
      {!courses ? <Spinner>Yuklanmoqda...</Spinner> : (
        <div className="grid gap-4 md:grid-cols-2">
          {courses.map((c) => (
            <Link key={c.id} to={`/boshqaruv/kurslar/${c.id}`} className="card p-5 transition-shadow hover:shadow-lg">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted">{c.subject}</p>
              <h2 className="mb-3 font-display text-lg font-bold leading-snug text-ink">{c.title}</h2>
              <Meter value={c.avg_progress} tone={toneFor(c.avg_progress)} />
              <dl className="mt-3 grid grid-cols-4 gap-2 text-center">
                {[['Mavzu', c.topics_total], ['Talaba', c.students], ['Urinish', c.attempts], ["O'tish", c.pass_rate === null ? '—' : `${c.pass_rate}%`]].map(([l, v]) => (
                  <div key={l} className="rounded-lg bg-paper-2 py-2">
                    <dd className="font-display text-lg font-extrabold text-ink">{v}</dd>
                    <dt className="text-[0.68rem] text-muted">{l}</dt>
                  </div>
                ))}
              </dl>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export function AdminCourseDetailPage() {
  const { bookId } = useParams()
  const [d, setD] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => { getAdminCourse(bookId).then(setD).catch((e) => setError(e.message)) }, [bookId])

  return (
    <div className="rise">
      <Link to="/boshqaruv/kurslar" className="mb-3 inline-flex items-center gap-1.5 text-sm font-semibold text-brand hover:underline">
        <ArrowLeft size={14} /> Barcha kurslar
      </Link>
      <ErrorNote>{error}</ErrorNote>
      {!d ? <Spinner>Yuklanmoqda...</Spinner> : (
        <>
          <header className="mb-5 flex flex-wrap items-end justify-between gap-3">
            <h1 className="font-display text-2xl font-extrabold text-ink sm:text-3xl">{d.book.title}</h1>
            <Link to={`/boshqaruv/kontent/kitob/${d.book.id}`} className="btn btn-ghost btn-sm"><Pencil size={14} /> Tahrirlash</Link>
          </header>

          <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
            {[['Talabalar', d.summary.students], ["O'rtacha progress", `${d.summary.avg_progress}%`], ['Sertifikat', d.summary.certificates], ["Testdan o'tish", d.summary.pass_rate === null ? '—' : `${d.summary.pass_rate}%`]].map(([l, v]) => (
              <div key={l} className="card p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-muted">{l}</p>
                <p className="font-display text-2xl font-extrabold text-ink">{v}</p>
              </div>
            ))}
          </div>

          <section className="card mb-6 overflow-x-auto p-5">
            <h2 className="mb-1 font-display text-lg font-bold text-ink">Mavzular voronkasi</h2>
            <p className="mb-3 text-xs text-muted">Qaysi mavzuda talabalar to'xtab qolayotganini ko'rsatadi: o'tish foizi past yoki urinishlar soni ko'p bo'lsa — mavzu qiyin.</p>
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead>
                <tr className="border-b border-line text-xs uppercase tracking-wide text-muted">
                  <th className="py-2 pr-3 font-semibold">Mavzu</th>
                  <th className="px-3 py-2 font-semibold">Talaba</th>
                  <th className="px-3 py-2 font-semibold">Urinish / talaba</th>
                  <th className="px-3 py-2 font-semibold">O'rtacha ball</th>
                  <th className="w-44 px-3 py-2 font-semibold">Tugatish</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {d.funnel.map((t) => (
                  <tr key={t.id}>
                    <td className="max-w-xs truncate py-2 pr-3 font-medium text-ink" title={t.title}>{t.title}</td>
                    <td className="px-3 py-2 tabular-nums text-ink-2">{t.students}</td>
                    <td className={`px-3 py-2 tabular-nums ${t.attempts_per_student >= 2.5 ? 'font-semibold text-bad' : 'text-ink-2'}`}>{t.attempts_per_student ?? '—'}</td>
                    <td className="px-3 py-2 tabular-nums text-ink-2">{t.avg_score === null ? '—' : `${t.avg_score}%`}</td>
                    <td className="px-3 py-2"><Meter value={t.completion_rate} tone={toneFor(t.completion_rate)} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <div className="grid gap-4 lg:grid-cols-2">
            <section className="card p-5">
              <h2 className="mb-3 font-display text-lg font-bold text-ink">Eng qiyin savollar</h2>
              {(d.hard_questions || []).length === 0 ? <p className="text-sm text-muted">Hali yetarli ma'lumot yo'q.</p> : (
                <ul className="flex flex-col gap-3">
                  {d.hard_questions.slice(0, 8).map((h, i) => (
                    <li key={i} className="text-sm">
                      <p className="font-medium leading-snug text-ink">{h.question}</p>
                      <p className="mt-0.5 text-xs text-muted">
                        {h.topic_title} · xato {h.error_rate}% ({h.wrong}/{h.seen})
                        {h.suspicious && <span className="ml-1 font-semibold text-gold">· savolni tekshiring</span>}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </section>
            <section className="card p-5">
              <h2 className="mb-3 font-display text-lg font-bold text-ink">Talabalar</h2>
              {(d.students || []).length === 0 ? <p className="text-sm text-muted">Hali talaba yo'q.</p> : (
                <ul className="divide-y divide-line">
                  {d.students.slice(0, 12).map((s) => (
                    <li key={s.id} className="flex items-center justify-between gap-2 py-2 text-sm">
                      <Link to={`/boshqaruv/talaba/${s.id}`} className="truncate font-semibold text-ink hover:text-brand">{s.name || s.username}</Link>
                      <span className="shrink-0 text-xs text-muted">{s.topics_done}/{d.summary.topics_total} mavzu{s.certificate ? ' · sertifikat' : ''}</span>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        </>
      )}
    </div>
  )
}
