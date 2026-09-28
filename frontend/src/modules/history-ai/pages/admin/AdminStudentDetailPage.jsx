import { Award, BookOpenCheck, Flame, Star } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getAdminStudent } from '../../api/client'
import { BackLink, ErrorNote, Spinner, formatDateUz } from '../../components/ui'

export default function AdminStudentDetailPage({ userId, onBack }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    setData(null)
    getAdminStudent(userId).then(setData).catch((err) => setError(err.message))
  }, [userId])

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Talabalar ro'yxatiga qaytish</BackLink>
      <ErrorNote>{error}</ErrorNote>
      {!data ? (
        <Spinner>Yuklanmoqda...</Spinner>
      ) : (
        <>
          <header className="mb-6">
            <p className="eyebrow mb-2">Talaba</p>
            <h1 className="font-display text-3xl font-extrabold text-ink">{data.first_name || data.username}</h1>
            <p className="mt-1 text-sm text-muted">
              @{data.username} · {data.email || 'email yo\'q'} · ro'yxatdan o'tgan: {formatDateUz(data.date_joined)}
              {!data.is_active && <span className="chip ml-2 !border-bad/40 !bg-bad-soft !text-bad">Bloklangan</span>}
            </p>
          </header>

          <div className="mb-8 grid gap-4 sm:grid-cols-3">
            <Stat icon={Star} label="Jami ball" value={data.profile.xp} />
            <Stat icon={Flame} label="Ketma-ketlik" value={`${data.profile.streak.current} kun`} />
            <Stat icon={Award} label="Sertifikat" value={data.certificates.length} />
          </div>

          <section className="card mb-8 p-5 sm:p-6">
            <h2 className="mb-4 font-display text-lg font-bold text-ink">So'nggi 30 kunlik faollik (daqiqa)</h2>
            <div className="flex h-24 items-end gap-1">
              {data.activity.map((d) => {
                const max = Math.max(...data.activity.map((x) => x.minutes), 1)
                return (
                  <div
                    key={d.date}
                    title={`${d.date}: ${d.minutes} daqiqa`}
                    className="flex-1 rounded-t bg-brand-soft"
                    style={{ height: `${Math.max(4, (d.minutes / max) * 100)}%`, backgroundColor: d.minutes > 0 ? 'var(--brand)' : undefined }}
                  />
                )
              })}
            </div>
          </section>

          <section className="card mb-8 p-5 sm:p-6">
            <h2 className="mb-4 flex items-center gap-2 font-display text-lg font-bold text-ink">
              <BookOpenCheck size={18} className="text-brand" /> O'zlashtirgan mavzular
            </h2>
            {data.completed_topics.length === 0 ? (
              <p className="text-sm text-muted">Hali birorta mavzu o'zlashtirilmagan.</p>
            ) : (
              <ol className="flex flex-col gap-2">
                {data.completed_topics.map((t, i) => (
                  <li key={i} className="flex items-center justify-between gap-3 text-sm">
                    <span className="text-ink-2">
                      {t.topic__title} <span className="text-muted">({t.topic__book__title})</span>
                    </span>
                    <span className="shrink-0 text-xs text-muted">{formatDateUz(t.completed_at)}</span>
                  </li>
                ))}
              </ol>
            )}
          </section>

          <section className="card p-5 sm:p-6">
            <h2 className="mb-4 flex items-center gap-2 font-display text-lg font-bold text-ink">
              <Award size={18} className="text-gold" /> Sertifikatlar
            </h2>
            {data.certificates.length === 0 ? (
              <p className="text-sm text-muted">Hali sertifikat yo'q.</p>
            ) : (
              <ul className="flex flex-col gap-2">
                {data.certificates.map((c) => (
                  <li key={c.code} className="flex items-center justify-between text-sm">
                    <span className="text-ink-2">{c.book__title}</span>
                    <span className="text-xs text-muted">{c.code} · {formatDateUz(c.issued_at)}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}
    </div>
  )
}

function Stat({ icon: Icon, label, value }) {
  return (
    <div className="card p-5 text-center">
      <Icon size={20} className="mx-auto mb-2 text-brand" />
      <p className="font-display text-xl font-extrabold text-ink">{value}</p>
      <p className="text-xs font-medium text-muted">{label}</p>
    </div>
  )
}
