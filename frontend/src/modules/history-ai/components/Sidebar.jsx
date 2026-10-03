import {
  Award, BookOpen, Check, ChevronDown, ClipboardCheck, Home, LayoutDashboard, Library, Lock, Map as MapIcon,
  RotateCcw, Settings2, Shuffle, UserRound,
} from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

function ItemLink({ to, icon: Icon, children, active, badge, disabled, title, end }) {
  const cls = `group flex items-center gap-2.5 rounded-xl px-3 py-2 text-sm font-semibold transition-colors ${
    disabled ? 'cursor-not-allowed text-muted/60' : active ? 'bg-brand-soft text-brand' : 'text-ink-2 hover:bg-paper-2 hover:text-ink'
  }`
  const inner = (
    <>
      {Icon && <Icon size={16} className="shrink-0" />}
      <span className="min-w-0 flex-1 truncate">{children}</span>
      {badge > 0 && <span className="chip chip-gold !px-1.5 !py-0 text-[0.68rem]">{badge}</span>}
      {disabled && <Lock size={13} className="shrink-0" />}
    </>
  )
  if (disabled) return <span className={cls} title={title} aria-disabled="true">{inner}</span>
  return (
    <Link to={to} className={cls} title={title} aria-current={active ? 'page' : undefined} data-end={end}>
      {inner}
    </Link>
  )
}

function Group({ title, children }) {
  return (
    <div className="mb-5">
      <p className="mb-1.5 px-3 text-[0.68rem] font-bold uppercase tracking-widest text-muted">{title}</p>
      <div className="flex flex-col gap-0.5">{children}</div>
    </div>
  )
}

/** Kurs daraxti: bo'limlar (yig'iladigan) va ularning mavzulari, holat belgilari bilan. */
function CourseTree({ course, isTeacher, pathname }) {
  const { book, topics, sections } = course
  const activeTopicId = Number((pathname.match(/\/kurs\/\d+\/mavzu\/(\d+)/) || [])[1]) || null
  const activeSectionId = Number((pathname.match(/\/kurs\/\d+\/bolim\/(\d+)/) || [])[1]) || null

  const groups = useMemo(() => {
    const ids = [...new Set(topics.map((t) => t.section))]
    return ids.map((id, i) => ({
      id,
      section: sections.find((s) => s.id === id) || null,
      topics: topics.filter((t) => t.section === id),
      index: i + 1,
    }))
  }, [topics, sections])

  const defaultOpen = useMemo(() => {
    const cur = topics.find((t) => t.id === activeTopicId)
    if (cur) return cur.section
    if (activeSectionId) return activeSectionId
    return topics.find((t) => t.unlocked && !t.completed)?.section ?? groups[0]?.id
  }, [topics, groups, activeTopicId, activeSectionId])

  const [open, setOpen] = useState({})
  useEffect(() => {
    if (defaultOpen != null) setOpen((o) => ({ ...o, [defaultOpen]: true }))
  }, [defaultOpen, book.id])

  return (
    <div className="flex flex-col gap-1">
      {groups.map((g) => {
        const done = g.topics.filter((t) => t.completed).length
        const isOpen = Boolean(open[g.id])
        const sec = g.section
        const examEnabled = isTeacher || sec?.exam_available
        return (
          <div key={g.id}>
            <button
              type="button"
              onClick={() => setOpen((o) => ({ ...o, [g.id]: !o[g.id] }))}
              aria-expanded={isOpen}
              className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-left text-sm font-bold text-ink hover:bg-paper-2"
            >
              <ChevronDown size={14} className={`shrink-0 transition-transform ${isOpen ? '' : '-rotate-90'}`} />
              <span className="min-w-0 flex-1 truncate" title={sec?.title}>{sec?.title || `${g.index}-bo'lim`}</span>
              <span className="text-xs font-semibold text-muted">{done}/{g.topics.length}</span>
            </button>
            {isOpen && (
              <ul className="ml-3 mt-0.5 flex flex-col gap-0.5 border-l border-line pl-2">
                {g.topics.map((t) => {
                  const canOpen = isTeacher || t.unlocked
                  const active = t.id === activeTopicId
                  return (
                    <li key={t.id}>
                      <ItemLink
                        to={`/kurs/${book.id}/mavzu/${t.id}`}
                        active={active}
                        disabled={!canOpen}
                        title={canOpen ? t.title : 'Avval oldingi mavzu testini topshiring'}
                        icon={t.completed ? Check : undefined}
                      >
                        {t.title.replace(/^\d+(-\d+)?-mavzu(lar)?\.\s*/, '')}
                      </ItemLink>
                    </li>
                  )
                })}
                {sec && (isTeacher || sec.has_exam) && (
                  <li>
                    <ItemLink
                      to={`/kurs/${book.id}/bolim/${sec.id}`}
                      icon={ClipboardCheck}
                      active={sec.id === activeSectionId}
                      disabled={!examEnabled}
                      title={examEnabled ? undefined : "Bo'limdagi barcha mavzularni tugatgach ochiladi"}
                    >
                      Bo'lim testi
                    </ItemLink>
                  </li>
                )}
              </ul>
            )}
          </div>
        )
      })}
    </div>
  )
}

/**
 * Yon menyu. Bo'limlar: Asosiy, Fanlar, (kursda bo'lsa) Kurs menyusi + mavzular daraxti, (o'qituvchiga) Boshqaruv.
 * Katta ekranda doimiy ustun, kichik ekranda `drawer` sifatida ochiladi.
 */
export default function Sidebar({ me, subjects, course, stats }) {
  const { pathname } = useLocation()
  const isTeacher = me.is_staff
  const bookMatch = pathname.match(/^\/kurs\/(\d+)/)
  const inCourse = Boolean(bookMatch && course && course.book.id === Number(bookMatch[1]))
  const base = inCourse ? `/kurs/${course.book.id}` : null

  const completed = inCourse ? course.topics.filter((t) => t.completed).length : 0
  const total = inCourse ? course.topics.length : 0
  const pct = total ? Math.round((completed / total) * 100) : 0
  const progress = inCourse ? course.progress : null

  return (
    <nav aria-label="Yon menyu" className="text-ink">
      <Group title="Asosiy">
        <ItemLink to="/" icon={Home} active={pathname === '/'}>Bosh sahifa</ItemLink>
        <ItemLink to="/profil" icon={UserRound} active={pathname.startsWith('/profil')} badge={0}>
          Profil{stats ? ` · ${stats.xp} ball` : ''}
        </ItemLink>
      </Group>

      {subjects.length > 0 && (
        <Group title="Fanlar">
          {subjects.map((s) => (
            <ItemLink
              key={s.id}
              to={`/fan/${s.slug}`}
              icon={Library}
              active={pathname === `/fan/${s.slug}` || (inCourse && course.book.subject_slug === s.slug)}
            >
              {s.title}
            </ItemLink>
          ))}
        </Group>
      )}

      {inCourse && (
        <>
          <Group title="Joriy kurs">
            <div className="mb-1 px-3">
              <p className="line-clamp-2 text-sm font-bold leading-snug text-ink" title={course.book.title}>{course.book.title}</p>
              <div className="mt-2 flex items-center gap-2" aria-label={`Kurs bo'yicha ${pct} foiz`}>
                <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-paper-2">
                  <div className="h-full rounded-full bg-brand" style={{ width: `${pct}%` }} />
                </div>
                <span className="text-xs font-semibold text-muted">{completed}/{total}</span>
              </div>
            </div>
            <ItemLink to={base} icon={MapIcon} active={pathname === base}>Yo'l xaritasi</ItemLink>
            {!isTeacher && (
              <>
                <ItemLink to={`${base}/takrorlash`} icon={RotateCcw} active={pathname.startsWith(`${base}/takrorlash`)} badge={progress?.weak_count || 0}>
                  Xatolarni takrorlash
                </ItemLink>
                {progress?.mixed_available && (
                  <ItemLink to={`${base}/aralash`} icon={Shuffle} active={pathname.startsWith(`${base}/aralash`)}>Aralash mashq</ItemLink>
                )}
              </>
            )}
            {(isTeacher || progress?.exam_exists) && (
              <ItemLink
                to={`${base}/imtihon`}
                icon={Award}
                active={pathname.startsWith(`${base}/imtihon`)}
                disabled={!isTeacher && !progress?.all_topics_completed}
                title={!isTeacher && !progress?.all_topics_completed ? 'Barcha mavzularni tugatgach ochiladi' : undefined}
              >
                Yakuniy imtihon
              </ItemLink>
            )}
          </Group>

          <Group title="Mavzular">
            <CourseTree course={course} isTeacher={isTeacher} pathname={pathname} />
          </Group>
        </>
      )}

      {isTeacher && (
        <Group title="Boshqaruv">
          <ItemLink to="/boshqaruv" icon={LayoutDashboard} active={pathname === '/boshqaruv' || pathname.startsWith('/boshqaruv/talaba')}>
            Statistika
          </ItemLink>
          <ItemLink to="/boshqaruv/kontent" icon={Settings2} active={pathname.startsWith('/boshqaruv/kontent')}>Kontent</ItemLink>
        </Group>
      )}

      {!inCourse && (
        <p className="mt-2 flex items-start gap-2 px-3 text-xs leading-relaxed text-muted">
          <BookOpen size={14} className="mt-0.5 shrink-0" />
          Kursni ochsangiz, bu yerda uning bo'limlari va mavzulari ko'rinadi.
        </p>
      )}
    </nav>
  )
}
