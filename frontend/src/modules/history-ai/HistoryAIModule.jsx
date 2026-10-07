import { Flame, GraduationCap, Home, LayoutDashboard, LogOut, Menu, Star, UserRound, WifiOff, X } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import {
  Link, Navigate, Outlet, Route, Routes, useLocation, useNavigate, useOutletContext, useParams,
} from 'react-router-dom'
import {
  clearToken, createAsset, createBookExam, downloadCertificate, getAssetByTopic, getBookExam, getBookProgress, getMe,
  getProfile, getSectionExam, getSections, getToken, listBooks, listSubjects, listTopics, sendHeartbeat, submitBookExam,
  submitSectionExam, getTopicTestHint,
  submitTopicTest,
} from './api/client'
import AdminShell from './components/admin/AdminShell'
import Sidebar from './components/Sidebar'
import { FontSizeToggle, Spinner, ThemeToggle, useFontSize, useTheme } from './components/ui'
import AdminBookEditorPage from './pages/admin/AdminBookEditorPage'
import AdminContentPage from './pages/admin/AdminContentPage'
import { AdminCourseDetailPage, AdminCoursesPage } from './pages/admin/AdminCoursesPage'
import AdminOverviewPage from './pages/admin/AdminOverviewPage'
import AdminStudentsPage from './pages/admin/AdminStudentsPage'
import AdminStudentDetailPage from './pages/admin/AdminStudentDetailPage'
import AdminTopicEditorPage from './pages/admin/AdminTopicEditorPage'
import CertificateVerifyPage from './pages/CertificateVerifyPage'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import PlacementPage from './pages/PlacementPage'
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
        path="boshqaruv"
        element={
          me.is_staff
            ? <AdminShell me={me} dark={dark} onToggleTheme={toggleTheme} onLogout={handleLogout} />
            : <Navigate to="/" replace />
        }
      >
        <Route index element={<AdminOverviewPage />} />
        <Route path="talabalar" element={<AdminStudentsPage />} />
        <Route path="talaba/:userId" element={<AdminStudentDetailRoute />} />
        <Route path="kurslar" element={<AdminCoursesPage />} />
        <Route path="kurslar/:bookId" element={<AdminCourseDetailPage />} />
        <Route path="kontent" element={<AdminContentRoute />} />
        <Route path="kontent/kitob/:bookId" element={<AdminBookEditorRoute />} />
        <Route path="kontent/kitob/:bookId/mavzu/:topicId" element={<AdminTopicEditorRoute />} />
      </Route>
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
        <Route path="daraja/:slug" element={<PlacementPage />} />
        <Route path="fan/:slug" element={<CoursesRoute />} />
        <Route path="kurs/:bookId" element={<BookLayout />}>
          <Route index element={<TopicsRoute />} />
          <Route path="mavzu/:topicId" element={<LessonRoute />} />
          <Route path="mavzu/:topicId/test" element={<TopicTestRoute />} />
          <Route path="bolim/:sectionId" element={<SectionExamRoute />} />
          <Route path="imtihon" element={<ExamRoute />} />
          <Route path="takrorlash" element={<ReviewRoute />} />
          <Route path="aralash" element={<ReviewRoute mixed />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

function Shell({ me, dark, onToggleTheme, fontSize, onChangeFontSize, onLogout }) {
  const [stats, setStats] = useState(null)
  const [online, setOnline] = useState(navigator.onLine)
  const [subjects, setSubjects] = useState([])
  const [course, setCourse] = useState(null)  // ochiq kurs ma'lumoti (BookLayout to'ldiradi) - yon menyu uchun
  const [drawer, setDrawer] = useState(false)
  const location = useLocation()

  useEffect(() => {
    listSubjects().then(setSubjects).catch(() => {})
  }, [])

  // Sahifa almashganda yoki Esc bosilganda kichik ekrandagi menyu yopiladi.
  useEffect(() => { setDrawer(false) }, [location.pathname])
  useEffect(() => {
    if (!drawer) return undefined
    const onKey = (e) => { if (e.key === 'Escape') setDrawer(false) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [drawer])

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
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3">
          <button
            type="button"
            onClick={() => setDrawer(true)}
            className="btn btn-ghost btn-sm !px-2 lg:hidden"
            aria-label="Menyuni ochish"
            aria-expanded={drawer}
          >
            <Menu size={18} />
          </button>
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

      <div className="mx-auto flex max-w-7xl gap-8 px-4">
        <aside className="sticky top-[76px] hidden h-[calc(100vh-76px)] w-64 shrink-0 overflow-y-auto py-6 pr-1 lg:block">
          <Sidebar me={me} subjects={subjects} course={course} stats={stats} />
        </aside>
        <main id="main-content" className="min-w-0 flex-1 pb-24 pt-8">
          <Outlet context={{ me, isTeacher: me.is_staff, setCourse }} />
        </main>
      </div>

      {drawer && (
        <div className="fixed inset-0 z-40 lg:hidden" role="dialog" aria-modal="true" aria-label="Menyu">
          <button type="button" className="absolute inset-0 bg-black/50" onClick={() => setDrawer(false)} aria-label="Menyuni yopish" />
          <div className="rise absolute inset-y-0 left-0 flex w-72 max-w-[85vw] flex-col overflow-y-auto bg-paper p-4 shadow-xl">
            <div className="mb-4 flex items-center justify-between">
              <span className="font-display text-lg font-bold text-ink">Menyu</span>
              <button type="button" onClick={() => setDrawer(false)} className="btn btn-ghost btn-sm !px-2" aria-label="Yopish">
                <X size={18} />
              </button>
            </div>
            <Sidebar me={me} subjects={subjects} course={course} stats={stats} />
            <button type="button" onClick={onLogout} className="btn btn-ghost btn-sm mt-auto w-full justify-start">
              <LogOut size={14} /> Chiqish
            </button>
          </div>
        </div>
      )}

      <MobileNav stats={stats} />
    </div>
  )
}

const NAV_ITEMS = [
  { to: '/', label: 'Bosh sahifa', icon: Home, end: true },
  { to: '/profil', label: 'Profil', icon: UserRound },
]
const ADMIN_NAV_ITEM = { to: '/boshqaruv', label: 'Boshqaruv', icon: LayoutDashboard }

/** Katta ekranda header ichidagi gorizontal menyu. */
function NavMenu({ isTeacher }) {
  const location = useLocation()
  const items = isTeacher ? [...NAV_ITEMS, ADMIN_NAV_ITEM] : NAV_ITEMS
  return (
    <nav aria-label="Asosiy menyu" className="hidden items-center gap-1 sm:flex lg:hidden">
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

  // Yon menyu ochiq kursning bo'limlari/mavzularini ko'rsatishi uchun ma'lumotni Shell'ga uzatamiz.
  const { setCourse } = outer
  useEffect(() => {
    setCourse(data && data.book ? data : null)
    return () => setCourse(null)
  }, [data, setCourse])

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
      onOpenMixed={() => navigate(`/kurs/${bookId}/aralash`)}
      onOpenTopic={(id) => navigate(`/kurs/${bookId}/mavzu/${id}`)}
      onDownloadCertificate={() => downloadCertificate(bookId)}
    />
  )
}

function ReviewRoute({ mixed = false }) {
  const { bookId, refresh } = useOutletContext()
  const navigate = useNavigate()
  return (
    <ReviewPage
      key={mixed ? 'mixed' : 'review'}
      mixed={mixed}
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
      bookId={bookId}
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
      hint={(index, level) => getTopicTestHint(topic.id, index, level)}
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

/* ───────── Boshqaruv paneli (faqat is_staff) ───────── */

function AdminStudentDetailRoute() {
  const { userId } = useParams()
  const navigate = useNavigate()
  return <AdminStudentDetailPage userId={Number(userId)} onBack={() => navigate('/boshqaruv/talabalar')} />
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
