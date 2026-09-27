import { Award, BookOpen, Check, ClipboardCheck, Lock, RotateCcw, Trophy } from 'lucide-react'
import SearchBox from '../components/SearchBox'
import { BackLink, ProgressBar, ProgressRing } from '../components/ui'

const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

/** "I BO'LIM. Sarlavha" -> { num: 'I', name: 'Sarlavha' } */
function splitSectionTitle(title = '', fallbackIndex = 0) {
  const m = title.match(/^\s*([IVXLC]+)\s*[- ]*BO['‘’`ʻ]?LIM\.?\s*(.*)$/i)
  if (m) return { num: m[1].toUpperCase(), name: m[2] || title }
  return { num: ROMAN[fallbackIndex] || String(fallbackIndex + 1), name: title }
}

export default function TopicSelectPage({
  book, topics, sections = [], onOpenSectionExam, isTeacher, progress, onSelect, onBack, onOpenExam, onDownloadCertificate,
  onOpenReview, onOpenTopic,
}) {
  const completedCount = topics.filter((t) => t.completed).length
  const sectionIds = [...new Set(topics.map((t) => t.section))]
  const groups = sectionIds.map((id) => ({
    section: sections.find((s) => s.id === id) || null,
    topics: topics.filter((t) => t.section === id),
  }))
  const nextTopic = topics.find((t) => t.unlocked && !t.completed)

  return (
    <div className="rise mx-auto max-w-3xl">
      <BackLink onClick={onBack}>Darsliklar ro'yxati</BackLink>

      {/* Sarlavha kartasi */}
      <div className="card relative mb-10 overflow-hidden p-6 sm:p-8">
        <div className="pointer-events-none absolute -right-10 -top-10 h-44 w-44 rounded-full bg-gold/10" aria-hidden />
        <div className="relative flex flex-wrap items-center gap-6">
          {!isTeacher && <ProgressRing value={completedCount} max={topics.length} />}
          <div className="min-w-0 flex-1">
            <p className="eyebrow mb-1">Yo'l xaritasi</p>
            <h1 className="font-display text-3xl font-extrabold leading-tight text-ink sm:text-4xl">{book.title}</h1>
            <p className="mt-2 text-sm text-muted">
              {topics.length} ta mavzu
              {!isTeacher && ` · o'tildi: ${completedCount} / ${topics.length}`}
            </p>
            {!isTeacher && <ProgressBar value={completedCount} max={topics.length} className="mt-4 max-w-sm" />}
          </div>
          {!isTeacher && nextTopic && (
            <button onClick={() => onSelect(nextTopic)} className="btn btn-primary">
              <BookOpen size={16} /> {completedCount ? 'Davom etish' : 'Boshlash'}
            </button>
          )}
        </div>
      </div>

      <div className="mb-10 space-y-4">
        <SearchBox bookId={book.id} onOpenTopic={onOpenTopic} />
        {!isTeacher && progress?.weak_count > 0 && (
          <button
            onClick={onOpenReview}
            className="card card-hover flex w-full items-center gap-4 !border-gold/60 bg-gold-soft/50 px-5 py-4 text-left"
          >
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gold text-white">
              <RotateCcw size={20} />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block font-display text-lg font-bold text-ink">Xatolarni takrorlash</span>
              <span className="text-sm text-muted">{progress.weak_count} ta savol takrorlashni kutmoqda</span>
            </span>
            <span className="chip chip-gold">Boshlash →</span>
          </button>
        )}
      </div>

      {/* Bo'limlar */}
      {groups.map((group, gi) => {
        const { num, name } = splitSectionTitle(group.section?.title, gi)
        const done = group.topics.filter((t) => t.completed).length
        const sec = group.section
        const examEnabled = isTeacher || sec?.exam_available
        return (
          <section key={sec?.id ?? 'none'} className="mb-10">
            <div className="mb-4 flex items-center gap-4">
              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-brand font-display text-xl font-extrabold text-brand-ink shadow">
                {num}
              </div>
              <div className="min-w-0 flex-1">
                <p className="eyebrow">{num} bo'lim</p>
                <h2 className="font-display text-xl font-bold leading-snug text-ink sm:text-2xl">{name}</h2>
              </div>
              <span className="chip hidden sm:inline-flex">{done} / {group.topics.length}</span>
            </div>

            {/* Mavzular yo'li */}
            <ol className="relative ml-7 border-l-2 border-dashed border-line-strong pl-8">
              {group.topics.map((topic) => {
                const locked = !topic.unlocked
                const current = nextTopic?.id === topic.id
                return (
                  <li key={topic.id} className="relative pb-3">
                    <span
                      className={`absolute -left-[3.05rem] top-3 flex h-9 w-9 items-center justify-center rounded-full border-2 ${
                        topic.completed
                          ? 'border-ok bg-ok text-white'
                          : locked
                            ? 'border-line-strong bg-paper-2 text-muted'
                            : current
                              ? 'border-brand bg-brand text-brand-ink ring-4 ring-brand/20'
                              : 'border-gold bg-surface text-gold'
                      }`}
                      aria-hidden
                    >
                      {topic.completed ? <Check size={17} strokeWidth={3} /> : locked ? <Lock size={15} /> : <BookOpen size={16} />}
                    </span>
                    <button
                      onClick={() => onSelect(topic)}
                      disabled={locked}
                      title={locked ? "Avval oldingi mavzu (yoki bo'lim) testini 100% topshiring" : undefined}
                      className={`card card-hover flex w-full items-center justify-between gap-3 px-4 py-3.5 text-left ${
                        locked ? '!bg-paper-2 !shadow-none' : ''
                      } ${current ? '!border-brand' : ''}`}
                    >
                      <span className={`text-[0.95rem] font-semibold leading-snug ${locked ? 'text-muted' : 'text-ink'}`}>
                        {topic.title}
                      </span>
                      <span className="chip shrink-0">
                        {topic.start_page === topic.end_page ? `bet ${topic.start_page}` : `bet ${topic.start_page}–${topic.end_page}`}
                      </span>
                    </button>
                  </li>
                )
              })}

              {/* Bo'lim testi */}
              {sec && (isTeacher || sec.has_exam) && (
                <li className="relative">
                  <span
                    className={`absolute -left-[3.05rem] top-3 flex h-9 w-9 items-center justify-center rounded-full border-2 ${
                      sec.completed ? 'border-ok bg-ok text-white' : examEnabled ? 'border-gold bg-gold text-white' : 'border-line-strong bg-paper-2 text-muted'
                    }`}
                    aria-hidden
                  >
                    {sec.completed ? <Check size={17} strokeWidth={3} /> : examEnabled ? <ClipboardCheck size={16} /> : <Lock size={15} />}
                  </span>
                  <button
                    onClick={() => onOpenSectionExam(sec)}
                    disabled={!examEnabled}
                    title={!examEnabled ? "Bo'limdagi barcha mavzularni tugatgach ochiladi" : undefined}
                    className={`flex w-full items-center justify-between gap-3 rounded-2xl border px-4 py-3.5 text-left transition-colors ${
                      sec.completed
                        ? 'border-ok/40 bg-ok-soft text-ok'
                        : examEnabled
                          ? 'border-gold bg-gold-soft text-ink hover:brightness-105'
                          : 'cursor-not-allowed border-line bg-paper-2 text-muted'
                    }`}
                  >
                    <span className="flex items-center gap-2 font-display text-base font-bold">
                      <ClipboardCheck size={18} />
                      {sec.completed ? "Bo'lim testi o'tildi" : `${num} bo'lim testi`}
                    </span>
                    <span className="text-xs font-medium">
                      {sec.completed ? 'Yakunlandi' : examEnabled ? 'Boshlash →' : 'Qulflangan'}
                    </span>
                  </button>
                </li>
              )}
            </ol>
          </section>
        )
      })}

      {/* Yakuniy imtihon */}
      <section className="card relative overflow-hidden p-6 sm:p-8">
        <div className="meander absolute inset-x-0 top-0" />
        <div className="flex flex-wrap items-center gap-5 pt-2">
          <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gold-soft text-gold">
            <Trophy size={28} />
          </span>
          <div className="min-w-0 flex-1">
            <h2 className="font-display text-2xl font-bold text-ink">Kitob yakuniy imtihoni</h2>
            <p className="mt-1 text-sm text-muted">
              {isTeacher
                ? "Imtihonni ko'rish yoki yaratish mumkin."
                : progress?.all_topics_completed
                  ? 'Barcha mavzular o\'tildi — imtihonga tayyorsiz!'
                  : "Barcha mavzu testlarini topshirgach ochiladi."}
            </p>
          </div>
          {isTeacher ? (
            <button onClick={onOpenExam} className="btn btn-ghost">Ko'rish / yaratish</button>
          ) : progress?.all_topics_completed ? (
            <button onClick={onOpenExam} className="btn btn-primary">Imtihonni topshirish</button>
          ) : (
            <span className="chip"><Lock size={12} /> Qulflangan</span>
          )}
        </div>

        {progress?.certificate && (
          <button onClick={onDownloadCertificate} className="btn btn-gold mt-5">
            <Award size={16} /> Sertifikatni yuklab olish (PDF)
          </button>
        )}
      </section>
    </div>
  )
}
