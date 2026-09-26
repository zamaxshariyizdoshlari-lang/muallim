import { Flame, GraduationCap, LogOut, Star } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import {
  Link, Navigate, Outlet, Route, Routes, useLocation, useNavigate, useOutletContext, useParams,
} from 'react-router-dom'
import {
  clearToken, createAsset, createBookExam, downloadCertificate, getAssetByTopic, getBookExam, getBookProgress, getMe,
  getProfile, getSectionExam, getSections, getToken, listBooks, listSubjects, listTopics, submitBookExam, submitSectionExam,
  submitTopicTest,
} from './api/client'
import { Spinner, ThemeToggle, useTheme } from './components/ui'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import ReviewPage from './pages/ReviewPage'
import SubjectsPage from './pages/SubjectsPage'
import TestPage from './pages/TestPage'
import TopicSelectPage from './pages/TopicSelectPage'
import UploadPage from './pages/UploadPage'

/**
 * Muallim ta'lim modulining kirish nuqtasi. Router (BrowserRouter) tashqarida beriladi.
 *
 * Manzillar:
 *   /                          fanlar
 *   /fan/:slug                 fan kurslari
 *   /kurs/:bookId              kurs yo'l xaritasi
 *   /kurs/:bookId/mavzu/:id    dars
 *   /kurs/:bookId/mavzu/:id/test
 *   /kurs/:bookId/bolim/:id    bo'lim testi
 *   /kurs/:bookId/imtihon      yakuniy imtihon
 */
export default function HistoryAIModule() {
  const [dark, toggleTheme] = useTheme()
  const [authed, setAuthed] = useState(Boolean(getToken()))
  const [me, setMe] = useState(null)

  useEffect(() => {
    if (authed) getMe().then(setMe).catch(() => setAuthed(false))
  }, [authed])

  if (!authed) {
    return <LoginPage onSuccess={() => setAuthed(true)} dark={dark} onToggleTheme={toggleTheme} />
  }
  if (!me) return null

  function handleLogout() {
    clearToken()
    setMe(null)
    setAuthed(false)
  }

  return (
    <Routes>
      <Route element={<Shell me={me} dark={dark} onToggleTheme={toggleTheme} onLogout={handleLogout} />}>
        <Route index element={<SubjectsRoute />} />
        <Route path="profil" element={<ProfileRoute />} />
        <Route path="fan/:slug" element={<CoursesRoute />} />
        <Route path="kurs/:bookId" element={<BookLayout />}>
          <Route index element={<TopicsRoute />} />
          <Route path="mavzu/:topicId" element={<LessonRoute />} />
          <Route path="mavzu/:topicId/test" element={<TopicTestRoute />} />
          <Route path="bolim/:sectionId" element={<SectionExamRoute />} />
          <Route path="imtihon" element={<ExamRoute />} />
          <Route path="takrorlash" element={<ReviewRoute />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

function Shell({ me, dark, onToggleTheme, onLogout }) {
  const [stats, setStats] = useState(null)
  const location = useLocation()

  // Sahifa almashganda XP/ketma-ketlik yangilanadi (test topshirilgandan keyin ham).
  useEffect(() => {
    getProfile().then(setStats).catch(() => {})
  }, [location.pathname])

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-line bg-paper/85 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-3">
          <Link to="/" className="flex items-center gap-2.5 text-left" aria-label="Bosh sahifa">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-brand-ink">
              <GraduationCap size={18} />
            </span>
            <span className="font-display text-lg font-bold leading-none text-ink">Muallim</span>
          </Link>
          <div className="flex items-center gap-2">
            {stats && (
              <Link to="/profil" className="flex items-center gap-1.5" title="Profil: XP va ketma-ketlik">
                <span className={`chip ${stats.streak.current > 0 ? 'chip-gold' : ''}`}>
                  <Flame size={13} /> {stats.streak.current}
                </span>
                <span className="chip chip-gold">
                  <Star size={13} /> {stats.xp} XP
                </span>
              </Link>
            )}
            <Link to="/profil" className="hidden text-sm text-muted hover:text-brand sm:inline">
              {me.first_name || me.username}
              {me.is_staff && <span className="chip chip-gold ml-2">o'qituvchi</span>}
            </Link>
            <ThemeToggle dark={dark} onToggle={onToggleTheme} />
            <button type="button" onClick={onLogout} className="btn btn-ghost btn-sm">
              <LogOut size={14} /> <span className="hidden sm:inline">Chiqish</span>
            </button>
          </div>
        </div>
        <div className="meander" />
      </header>

      <main className="mx-auto max-w-5xl px-4 pb-24 pt-8">
        <Outlet context={{ me, isTeacher: me.is_staff }} />
      </main>
    </div>
  )
}

/* ───────── Fanlar va kurslar ───────── */

function ProfileRoute() {
  const { me } = useOutletContext()
  return <ProfilePage me={me} />
}

function SubjectsRoute() {
  const { me } = useOutletContext()
  const navigate = useNavigate()
  return <SubjectsPage me={me} onOpenSubject={(s) => navigate(`/fan/${s.slug}`)} />
}

function CoursesRoute() {
  const { isTeacher } = useOutletContext()
  const { slug } = useParams()
  const navigate = useNavigate()
  const [subject, setSubject] = useState(null)

  useEffect(() => {
    listSubjects().then((list) => setSubject(list.find((s) => s.slug === slug) || { slug, title: slug }))
  }, [slug])

  if (!subject) return <Spinner>Yuklanmoqda...</Spinner>
  return (
    <UploadPage
      subject={subject}
      isTeacher={isTeacher}
      onBack={() => navigate('/')}
      onUploaded={(book) => navigate(`/kurs/${book.id}`)}
      onOpenBook={(book) => navigate(`/kurs/${book.id}`)}
    />
  )
}

/* ───────── Kurs (bo'limlar, mavzular, progress) ───────── */

function BookLayout() {
  const outer = useOutletContext()
  const { bookId } = useParams()
  const id = Number(bookId)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  const refresh = useCallback(async () => {
    const [books, topics, progress, sections] = await Promise.all([
      listBooks(), listTopics(id), getBookProgress(id), getSections(id),
    ])
    setData({ book: books.find((b) => b.id === id) || null, topics, progress, sections })
  }, [id])

  useEffect(() => {
    setData(null)
    setError('')
    refresh().catch((err) => setError(err.message))
  }, [refresh])

  if (error) return <p className="text-bad">{error}</p>
  if (!data) return <Spinner>Kurs yuklanmoqda...</Spinner>
  if (!data.book) return <Navigate to="/" replace />

  return <Outlet context={{ ...outer, ...data, bookId: id, refresh }} />
}

function TopicsRoute() {
  const { book, topics, sections, progress, isTeacher, bookId } = useOutletContext()
  const navigate = useNavigate()
  return (
    <TopicSelectPage
      book={book}
      topics={topics}
      sections={sections}
      isTeacher={isTeacher}
      progress={progress}
      onOpenSectionExam={(s) => navigate(`/kurs/${bookId}/bolim/${s.id}`)}
      onSelect={(t) => navigate(`/kurs/${bookId}/mavzu/${t.id}`)}
      onBack={() => navigate(book.subject_slug ? `/fan/${book.subject_slug}` : '/')}
      onOpenExam={() => navigate(`/kurs/${bookId}/imtihon`)}
      onOpenReview={() => navigate(`/kurs/${bookId}/takrorlash`)}
      onOpenTopic={(id) => navigate(`/kurs/${bookId}/mavzu/${id}`)}
      onDownloadCertificate={() => downloadCertificate(bookId)}
    />
  )
}

function ReviewRoute() {
  const { bookId, refresh } = useOutletContext()
  const navigate = useNavigate()
  return (
    <ReviewPage
      bookId={bookId}
      onBack={async () => { await refresh(); navigate(`/kurs/${bookId}`) }}
      onOpenTopic={(id) => navigate(`/kurs/${bookId}/mavzu/${id}`)}
    />
  )
}

function useTopicParam() {
  const { topics } = useOutletContext()
  const { topicId } = useParams()
  return topics.find((t) => t.id === Number(topicId)) || null
}

function LessonRoute() {
  const { isTeacher, bookId, refresh } = useOutletContext()
  const topic = useTopicParam()
  const navigate = useNavigate()
  if (!topic) return <Navigate to={`/kurs/${bookId}`} replace />
  if (!isTeacher && !topic.unlocked) return <Navigate to={`/kurs/${bookId}`} replace />
  return (
    <LessonResultPage
      topicId={topic.id}
      topicTitle={topic.title}
      isTeacher={isTeacher}
      onBack={async () => { await refresh(); navigate(`/kurs/${bookId}`) }}
      onStartTest={() => navigate(`/kurs/${bookId}/mavzu/${topic.id}/test`)}
    />
  )
}

function TopicTestRoute() {
  const { isTeacher, bookId, refresh } = useOutletContext()
  const topic = useTopicParam()
  const navigate = useNavigate()
  if (!topic) return <Navigate to={`/kurs/${bookId}`} replace />
  return (
    <TestPage
      key={`t${topic.id}`}
      title={`Mavzu testi: ${topic.title}`}
      isTeacher={isTeacher}
      load={() => getAssetByTopic(topic.id, 'topic_test')}
      create={() => createAsset(topic.id, 'topic_test', { regenerate: true })}
      submit={(answers) => submitTopicTest(topic.id, answers)}
      passedLabel="Mavzu to'liq o'zlashtirildi. Keyingi mavzu ochildi!"
      onBack={() => navigate(`/kurs/${bookId}/mavzu/${topic.id}`)}
      onPassed={async () => { await refresh(); navigate(`/kurs/${bookId}`) }}
    />
  )
}

function SectionExamRoute() {
  const { sections, bookId, refresh } = useOutletContext()
  const { sectionId } = useParams()
  const navigate = useNavigate()
  const section = sections.find((s) => s.id === Number(sectionId))
  if (!section) return <Navigate to={`/kurs/${bookId}`} replace />
  const back = async () => { await refresh(); navigate(`/kurs/${bookId}`) }
  return (
    <TestPage
      key={`s${section.id}`}
      title={`Bo'lim testi: ${section.title}`}
      isTeacher={false}
      load={() => getSectionExam(section.id)}
      create={async () => {}}
      submit={(answers) => submitSectionExam(section.id, answers)}
      passedLabel="Bo'lim to'liq o'zlashtirildi. Keyingi bo'lim ochildi!"
      onBack={back}
      onPassed={back}
    />
  )
}

function ExamRoute() {
  const { book, isTeacher, bookId, refresh } = useOutletContext()
  const navigate = useNavigate()
  const back = async () => { await refresh(); navigate(`/kurs/${bookId}`) }
  return (
    <TestPage
      key="exam"
      title={`Yakuniy imtihon: ${book.title}`}
      isTeacher={isTeacher}
      load={() => getBookExam(bookId)}
      create={() => createBookExam(bookId)}
      submit={(answers) => submitBookExam(bookId, answers)}
      passedLabel="Kurs muvaffaqiyatli tugatildi! Sertifikatingiz tayyor."
      onBack={back}
      onPassed={back}
    />
  )
}
