import { Flame, GraduationCap, Home, LayoutDashboard, LogOut, Star, Users, UserRound, WifiOff } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import {
  Link, Navigate, Outlet, Route, Routes, useLocation, useNavigate, useOutletContext, useParams,
} from 'react-router-dom'
import {
  clearToken, createAsset, createBookExam, downloadCertificate, getAssetByTopic, getBookExam, getBookProgress, getMe,
  getProfile, getSectionExam, getSections, getToken, listBooks, listSubjects, listTopics, sendHeartbeat, submitBookExam,
  submitSectionExam, submitTopicTest,
} from './api/client'
import { FontSizeToggle, Spinner, ThemeToggle, useFontSize, useTheme } from './components/ui'
import AdminBookEditorPage from './pages/admin/AdminBookEditorPage'
import AdminContentPage from './pages/admin/AdminContentPage'
import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import AdminStudentDetailPage from './pages/admin/AdminStudentDetailPage'
import AdminTopicEditorPage from './pages/admin/AdminTopicEditorPage'
import CertificateVerifyPage from './pages/CertificateVerifyPage'
import FriendsPage from './pages/FriendsPage'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import ResetPasswordPage from './pages/ResetPasswordPage'
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
  const [fontSize, setFontSize] = useFontSize()
  // Token localStorage'da qolar ekan, kirish doim ochiq bo'ladi: faqat token haqiqatan
  // yaroqsiz (401/403) bo'lsa chiqib ketiladi, tarmoq/server xatosida emas.
  const [authed, setAuthed] = useState(Boolean(getToken()))
  const [me, setMe] = useState(null)
  const [meError, setMeError] = useState('')

  const loadMe = useCallback(() => {
    setMeError('')
    getMe().then(setMe).catch((err) => {
      if (err.status === 401 || err.status === 403) setAuthed(false)
      // `err.status` bo'lsa - backend javob berib, aniq xabar yuborgan (o'zbekcha); aks holda
      // brauzerning o'z tarmoq xatosi (odatda inglizcha) - o'rniga umumiy o'zbekcha xabar ko'rsatiladi.
      else setMeError(err.status ? err.message : "Ulanishda xatolik. Internetni tekshiring.")
    })
  }, [])

  useEffect(() => {
    if (authed) loadMe()
  }, [authed, loadMe])

  useEffect(() => {
    if (!authed || me) return
    const onOnline = () => loadMe()
    window.addEventListener('online', onOnline)
    return () => window.removeEventListener('online', onOnline)
  }, [authed, me, loadMe])

  if (!authed) {
    return (
      <Routes>
        <Route
          path="parolni-tiklash"
          element={<ResetPasswordPage dark={dark} onToggleTheme={toggleTheme} fontSize={fontSize} onChangeFontSize={setFontSize} />}
        />
        <Route
          path="sertifikat/:code"
          element={<CertificateVerifyPage dark={dark} onToggleTheme={toggleTheme} fontSize={fontSize} onChangeFontSize={setFontSize} />}
        />
        <Route
          path="*"
          element={
            <LoginPage
              onSuccess={() => setAuthed(true)} dark={dark} onToggleTheme={toggleTheme}
              fontSize={fontSize} onChangeFontSize={setFontSize}
            />
          }
        />
      </Routes>
    )
  }
  if (!me) {
    return (
      <div className="flex min-h-screen items-center justify-center px-5">
        <div className="card max-w-sm p-6 text-center">
          <Spinner>Yuklanmoqda...</Spinner>
          {meError && (
            <>
              <p className="mt-3 text-sm text-bad">{meError}</p>
              <button onClick={loadMe} className="btn btn-ghost btn-sm mt-3">Qayta urinish</button>
            </>
          )}
        </div>
      </div>
    )
  }

  function handleLogout() {
    clearToken()
    setMe(null)
    setAuthed(false)
  }

  return (
    <Routes>
      <Route
        path="sertifikat/:code"
        element={<CertificateVerifyPage dark={dark} onToggleTheme={toggleTheme} fontSize={fontSize} onChangeFontSize={setFontSize} />}
      />
      <Route
        element={
          <Shell
            me={me} dark={dark} onToggleTheme={toggleTheme} fontSize={fontSize} onChangeFontSize={setFontSize}
            onLogout={handleLogout}
          />
        }
      >
        <Route index element={<SubjectsRoute />} />
        <Route path="profil" element={<ProfileRoute />} />
        <Route path="dostlar" element={<FriendsPage />} />
        <Route path="fan/:slug" element={<CoursesRoute />} />
        <Route path="kurs/:bookId" element={<BookLayout />}>
          <Route index element={<TopicsRoute />} />
          <Route path="mavzu/:topicId" element={<LessonRoute />} />
          <Route path="mavzu/:topicId/test" element={<TopicTestRoute />} />
          <Route path="bolim/:sectionId" element={<SectionExamRoute />} />
          <Route path="imtihon" element={<ExamRoute />} />
          <Route path="takrorlash" element={<ReviewRoute />} />
        </Route>
        <Route path="boshqaruv" element={<AdminGate />}>
          <Route index element={<AdminDashboardRoute />} />
          <Route path="talaba/:userId" element={<AdminStudentDetailRoute />} />
          <Route path="kontent" element={<AdminContentRoute />} />
          <Route path="kontent/kitob/:bookId" element={<AdminBookEditorRoute />} />
          <Route path="kontent/kitob/:bookId/mavzu/:topicId" element={<AdminTopicEditorRoute />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

function Shell({ me, dark, onToggleTheme, fontSize, onChangeFontSize, onLogout }) {
  const [stats, setStats] = useState(null)
  const [online, setOnline] = useState(navigator.onLine)
  const location = useLocation()

  useEffect(() => {
    const up = () => setOnline(true)
    const down = () => setOnline(false)
    window.addEventListener('online', up)
    window.addEventListener('offline', down)
    return () => {
      window.removeEventListener('online', up)
      window.removeEventListener('offline', down)
    }
  }, [])

  // Sahifa almashganda ball/ketma-ketlik yangilanadi (test topshirilgandan keyin ham).
  useEffect(() => {
    getProfile().then(setStats).catch(() => {})
  }, [location.pathname])

  // Admin panelda "kunlik faollik" jadvali uchun: sahifa ochiq va faol paytda har 30s belgi beriladi.
  useEffect(() => {
    const ping = () => { if (document.visibilityState === 'visible') sendHeartbeat().catch(() => {}) }
    ping()
    const id = setInterval(ping, 30000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="min-h-screen">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-xl focus:bg-brand focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-brand-ink"
      >
        Asosiy kontentga o'tish
      </a>
      <header className="sticky top-0 z-30 border-b border-line bg-paper/85 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-3">
          <Link to="/" className="flex items-center gap-2.5 text-left" aria-label="Bosh sahifa">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-brand-ink">
              <GraduationCap size={18} />
            </span>
            <span className="font-display text-lg font-bold leading-none text-ink">Muallim</span>
          </Link>

          <NavMenu isTeacher={me.is_staff} />

          <div className="flex items-center gap-2">
            {stats && (
              <Link to="/profil" className="hidden items-center gap-1.5 sm:flex" title="Profil: ball va ketma-ketlik">
                <span className={`chip ${stats.streak.current > 0 ? 'chip-gold' : ''}`}>
                  <Flame size={13} className={stats.streak.current > 0 ? 'streak-flame' : ''} /> {stats.streak.current}
                </span>
                <span className="chip chip-gold">
                  <Star size={13} /> {stats.xp} ball
                </span>
              </Link>
            )}
            <FontSizeToggle size={fontSize} onChange={onChangeFontSize} />
            <ThemeToggle dark={dark} onToggle={onToggleTheme} />
            <button type="button" onClick={onLogout} className="btn btn-ghost btn-sm">
              <LogOut size={14} /> <span className="hidden sm:inline">Chiqish</span>
            </button>
          </div>
        </div>
        <div className="meander" />
        {!online && (
          <div className="flex items-center justify-center gap-2 bg-gold-soft px-4 py-1.5 text-xs font-semibold text-ink-2">
            <WifiOff size={13} /> Internet yo'q — avval ochilgan darslarni o'qishingiz mumkin, testlar ishlamaydi.
          </div>
        )}
      </header>

      <main id="main-content" className="mx-auto max-w-5xl px-4 pb-24 pt-8">
        <Outlet context={{ me, isTeacher: me.is_staff }} />
      </main>

      <MobileNav stats={stats} />
    </div>
  )
}

const NAV_ITEMS = [
  { to: '/', label: 'Bosh sahifa', icon: Home, end: true },
  { to: '/dostlar', label: "Do'stlar", icon: Users },
  { to: '/profil', label: 'Profil', icon: UserRound },
]
const ADMIN_NAV_ITEM = { to: '/boshqaruv', label: 'Boshqaruv', icon: LayoutDashboard }

/** Katta ekranda header ichidagi gorizontal menyu. */
function NavMenu({ isTeacher }) {
  const location = useLocation()
  const items = isTeacher ? [...NAV_ITEMS, ADMIN_NAV_ITEM] : NAV_ITEMS
  return (
    <nav aria-label="Asosiy menyu" className="hidden items-center gap-1 sm:flex">
      {items.map(({ to, label, icon: Icon, end }) => {
        const active = end ? location.pathname === to : location.pathname.startsWith(to)
        return (
          <Link
            key={to}
            to={to}
            aria-current={active ? 'page' : undefined}
            className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-semibold transition-colors ${
              active ? 'bg-brand-soft text-brand' : 'text-muted hover:text-ink'
            }`}
          >
            <Icon size={15} /> {label}
          </Link>
        )
      })}
    </nav>
  )
}

/** Kichik ekranda pastki qattiq menyu (Duolingo/mobil ilovalar uslubida). */
function MobileNav({ stats }) {
  const location = useLocation()
  return (
    <nav
      aria-label="Asosiy menyu"
      className="fixed inset-x-0 bottom-0 z-30 flex items-stretch justify-around border-t border-line bg-paper/95 backdrop-blur sm:hidden"
    >
      {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => {
        const active = end ? location.pathname === to : location.pathname.startsWith(to)
        return (
          <Link
            key={to}
            to={to}
            aria-current={active ? 'page' : undefined}
            className={`flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[0.68rem] font-semibold ${
              active ? 'text-brand' : 'text-muted'
            }`}
          >
            <span className="relative">
              <Icon size={20} />
              {to === '/profil' && stats?.streak.current > 0 && (
                <span className="absolute -right-2 -top-1.5 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-gold text-[0.55rem] text-white">
                  {stats.streak.current}
                </span>
              )}
            </span>
            {label}
          </Link>
        )
      })}
    </nav>
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
  const { slug } = useParams()
  const navigate = useNavigate()
  const [subject, setSubject] = useState(null)

  useEffect(() => {
    listSubjects().then((list) => setSubject(list.find((s) => s.slug === slug) || { slug, title: slug }))
  }, [slug])

  if (!subject) return <Spinner>Yuklanmoqda...</Spinner>
  return <UploadPage subject={subject} onBack={() => navigate('/')} onOpenBook={(book) => navigate(`/kurs/${book.id}`)} />
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
      passThreshold={0.8}
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
      passThreshold={0.8}
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

/* ───────── Boshqaruv paneli (faqat is_staff) ───────── */

function AdminGate() {
  const outer = useOutletContext()
  if (!outer.isTeacher) return <Navigate to="/" replace />
  return <Outlet context={outer} />
}

function AdminDashboardRoute() {
  const navigate = useNavigate()
  return (
    <AdminDashboardPage
      onOpenStudent={(id) => navigate(`/boshqaruv/talaba/${id}`)}
      onOpenContent={() => navigate('/boshqaruv/kontent')}
    />
  )
}

function AdminStudentDetailRoute() {
  const { userId } = useParams()
  const navigate = useNavigate()
  return <AdminStudentDetailPage userId={Number(userId)} onBack={() => navigate('/boshqaruv')} />
}

function AdminContentRoute() {
  const navigate = useNavigate()
  return (
    <AdminContentPage
      onOpenBook={(id) => navigate(`/boshqaruv/kontent/kitob/${id}`)}
      onBack={() => navigate('/boshqaruv')}
    />
  )
}

function AdminBookEditorRoute() {
  const { bookId } = useParams()
  const navigate = useNavigate()
  return (
    <AdminBookEditorPage
      bookId={Number(bookId)}
      onBack={() => navigate('/boshqaruv/kontent')}
      onOpenTopic={(topicId) => navigate(`/boshqaruv/kontent/kitob/${bookId}/mavzu/${topicId}`)}
    />
  )
}

function AdminTopicEditorRoute() {
  const { bookId, topicId } = useParams()
  const navigate = useNavigate()
  const [title, setTitle] = useState('')

  useEffect(() => {
    listTopics(Number(bookId)).then((topics) => {
      setTitle(topics.find((t) => t.id === Number(topicId))?.title || '')
    })
  }, [bookId, topicId])

  return (
    <AdminTopicEditorPage
      topicId={Number(topicId)}
      topicTitle={title}
      onBack={() => navigate(`/boshqaruv/kontent/kitob/${bookId}`)}
    />
  )
}
