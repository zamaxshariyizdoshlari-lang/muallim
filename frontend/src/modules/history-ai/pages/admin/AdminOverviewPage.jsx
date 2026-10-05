import { AlertTriangle, Award, CheckCircle2, Clock, GraduationCap, UserPlus, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getAdminOverview } from '../../api/client'
import { BarChart, Delta, Meter, Sparkline, toneFor } from '../../components/admin/Charts'
import { ErrorNote, Spinner } from '../../components/ui'

const FEED_ICON = {
  pass: { icon: CheckCircle2, tone: 'text-ok' },
  fail: { icon: XCircle, tone: 'text-bad' },
  certificate: { icon: Award, tone: 'text-gold' },
  signup: { icon: UserPlus, tone: 'text-brand' },
}

function ago(iso) {
  const m = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000))
  if (m < 1) return 'hozir'
  if (m < 60) return `${m} daq oldin`
  if (m < 1440) return `${Math.round(m / 60)} soat oldin`
  return `${Math.round(m / 1440)} kun oldin`
}

function Kpi({ label, value, suffix, delta, spark, hint, tone }) {
  return (
    <div className="card p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">{label}</p>
      <div className="mt-1 flex items-baseline gap-2">
        <p className="font-display text-3xl font-extrabold text-ink">
          {value ?? '—'}<span className="text-lg font-bold text-ink-2">{value !== null && value !== undefined ? suffix : ''}</span>
        </p>
        {delta !== undefined && <Delta value={delta} />}
      </div>
      {spark ? <div className="mt-2"><Sparkline data={spark} className={tone || 'text-brand'} /></div> : <p className="mt-2 text-xs text-muted">{hint}</p>}
    </div>
  )
}

export default function AdminOverviewPage() {
  const [days, setDays] = useState(30)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    setData(null)
    getAdminOverview(days).then(setData).catch((e) => setError(e.message))
  }, [days])

  const k = data?.kpis
  return (
    <div className="rise">
      <header className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="eyebrow mb-1">Boshqaruv paneli</p>
          <h1 className="font-display text-3xl font-extrabold text-ink">Umumiy ko'rinish</h1>
        </div>
        <div className="inline-flex rounded-xl border border-line bg-surface p-0.5" role="group" aria-label="Davr">
          {[7, 30, 90].map((d) => (
            <button
              key={d} type="button" onClick={() => setDays(d)} aria-pressed={days === d}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold ${days === d ? 'bg-chalk text-white' : 'text-ink-2 hover:text-ink'}`}
            >
              {d} kun
            </button>
          ))}
        </div>
      </header>
      <ErrorNote>{error}</ErrorNote>
      {!data ? <Spinner>Yuklanmoqda...</Spinner> : (
        <>
          <div className="mb-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Kpi label="Talabalar" value={k.students_total} hint={`Bugun faol: ${k.active_today}`} spark={data.series.signups} />
            <Kpi label="Faol (7 kun)" value={k.active_7d} delta={k.active_delta} hint={`Jalb etilganlik ${k.engagement_7d}%`} spark={data.series.active} tone="text-ok" />
            <Kpi label="Test urinishlari (7 kun)" value={k.attempts_7d} delta={k.attempts_delta} spark={data.series.attempts} tone="text-gold" />
            <Kpi label="O'tish ulushi (7 kun)" value={k.pass_rate_7d} suffix="%" hint={`${k.completions_total} mavzu tugatilgan, ${k.certificates_total} sertifikat`} />
          </div>

          <div className="mb-6 grid gap-4 lg:grid-cols-3">
            <section className="card p-5 lg:col-span-2">
              <h2 className="mb-1 font-display text-lg font-bold text-ink">Test urinishlari</h2>
              <p className="mb-3 text-xs text-muted"><span className="inline-block h-2 w-2 rounded-sm bg-brand" /> barcha urinishlar · <span className="inline-block h-2 w-2 rounded-sm bg-ok" /> muvaffaqiyatlisi</p>
              <BarChart data={data.series.attempts} overlay={data.series.passed} label="urinish" />
            </section>
            <section className="card p-5">
              <h2 className="mb-1 font-display text-lg font-bold text-ink">Faol talabalar</h2>
              <p className="mb-3 text-xs text-muted">Bir kunda o'rtacha {k.avg_minutes_per_active} daqiqa o'qishgan (7 kun)</p>
              <BarChart data={data.series.active} label="talaba" height={140} tone="bg-ink-2" />
            </section>
          </div>

          <div className="mb-6 grid gap-4 lg:grid-cols-5">
            <section className="card p-5 lg:col-span-3">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="font-display text-lg font-bold text-ink">Kurslar holati</h2>
                <Link to="/boshqaruv/kurslar" className="text-sm font-semibold text-brand hover:underline">Batafsil</Link>
              </div>
              {data.courses.length === 0 ? <p className="text-sm text-muted">Kurslar yo'q.</p> : (
                <ul className="divide-y divide-line">
                  {data.courses.map((c) => (
                    <li key={c.id} className="py-3">
                      <div className="flex flex-wrap items-baseline justify-between gap-2">
                        <Link to={`/boshqaruv/kurslar/${c.id}`} className="font-semibold text-ink hover:text-brand">{c.title}</Link>
                        <span className="text-xs text-muted">{c.students} talaba · {c.certificates} sertifikat · o'tish {c.pass_rate ?? '—'}{c.pass_rate !== null ? '%' : ''}</span>
                      </div>
                      <Meter value={c.avg_progress} tone={toneFor(c.avg_progress)} className="mt-1.5" />
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section className="card p-5 lg:col-span-2">
              <h2 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
                <AlertTriangle size={17} className="text-gold" /> E'tibor kerak
              </h2>
              {data.at_risk.length === 0 ? (
                <p className="text-sm text-muted">Hozircha xavf ostidagi talaba yo'q.</p>
              ) : (
                <ul className="flex flex-col gap-2">
                  {data.at_risk.map((r, i) => (
                    <li key={`${r.id}-${i}`}>
                      <Link to={`/boshqaruv/talaba/${r.id}`} className="flex items-start gap-2.5 rounded-lg p-2 hover:bg-paper-2">
                        <span className={`mt-0.5 ${r.reason === 'stuck' ? 'text-bad' : 'text-gold'}`}>
                          {r.reason === 'stuck' ? <XCircle size={16} /> : <Clock size={16} />}
                        </span>
                        <span className="min-w-0">
                          <span className="block truncate text-sm font-semibold text-ink">{r.name || r.username}</span>
                          <span className="block text-xs text-muted">{r.detail}</span>
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>

          <section className="card p-5">
            <h2 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-ink">
              <GraduationCap size={17} className="text-brand" /> So'nggi voqealar
            </h2>
            {data.feed.length === 0 ? <p className="text-sm text-muted">Hali voqea yo'q.</p> : (
              <ul className="divide-y divide-line">
                {data.feed.map((e, i) => {
                  const { icon: Icon, tone } = FEED_ICON[e.kind]
                  return (
                    <li key={i} className="flex items-center gap-3 py-2 text-sm">
                      <Icon size={16} className={`shrink-0 ${tone}`} />
                      <Link to={`/boshqaruv/talaba/${e.user_id}`} className="shrink-0 font-semibold text-ink hover:text-brand">{e.user}</Link>
                      <span className="min-w-0 flex-1 truncate text-ink-2">{e.text}</span>
                      <span className="shrink-0 text-xs text-muted">{ago(e.at)}</span>
                    </li>
                  )
                })}
              </ul>
            )}
          </section>
        </>
      )}
    </div>
  )
}
