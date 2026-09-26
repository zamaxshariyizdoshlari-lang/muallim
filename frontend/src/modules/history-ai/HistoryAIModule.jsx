import { GraduationCap, LogOut } from 'lucide-react'
import { useEffect, useState } from 'react'
import {
  clearToken, createAsset, createBookExam, downloadCertificate, getAssetByTopic, getBookExam, getBookProgress, getMe,
  getSectionExam, getSections, getToken, listTopics, submitBookExam, submitSectionExam, submitTopicTest,
} from './api/client'
import { ThemeToggle, useTheme } from './components/ui'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import TestPage from './pages/TestPage'
import TopicSelectPage from './pages/TopicSelectPage'
import SubjectsPage from './pages/SubjectsPage'
import UploadPage from './pages/UploadPage'

/**
 * Muallim ta'lim modulining kirish nuqtasi. ERP'ga qo'shilganda bitta route
 * ostida shu komponent render qilinadi (masalan <Route path="/history-ai" element={<HistoryAIModule />} />).
 */
export default function HistoryAIModule() {
  const [dark, toggleTheme] = useTheme()
  const [authed, setAuthed] = useState(Boolean(getToken()))
  const [me, setMe] = useState(null)
  const [step, setStep] = useState('subjects') // subjects | upload (kurslar) | topics | lesson | topicTest | sectionExam | exam
  const [book, setBook] = useState(null)
  const [subject, setSubject] = useState(null)
  const [topics, setTopics] = useState([])
  const [sections, setSections] = useState([])
  const [activeSection, setActiveSection] = useState(null)
  const [progress, setProgress] = useState(null)
  const [activeTopic, setActiveTopic] = useState(null)

  useEffect(() => {
    if (authed) getMe().then(setMe).catch(() => setAuthed(false))
  }, [authed])

  if (!authed) {
    return <LoginPage onSuccess={() => setAuthed(true)} dark={dark} onToggleTheme={toggleTheme} />
  }
  if (!me) return null

  const isTeacher = me.is_staff

  function handleLogout() {
    clearToken()
    setMe(null)
    setBook(null)
    setStep('subjects')
    setSubject(null)
    setAuthed(false)
  }

  async function refreshTopics(bookId = book.id) {
    const [freshTopics, freshProgress, freshSections] = await Promise.all([
      listTopics(bookId), getBookProgress(bookId), getSections(bookId),
    ])
    setTopics(freshTopics)
    setProgress(freshProgress)
    setSections(freshSections)
  }

  async function handleUploaded(newBook, newTopics) {
    setBook(newBook)
    await refreshTopics(newBook.id)
    setStep('topics')
  }

  async function backToTopics() {
    await refreshTopics()
    setStep('topics')
  }

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-line bg-paper/85 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-3">
          <button
            type="button"
            onClick={() => setStep('subjects')}
            className="flex items-center gap-2.5 text-left"
            aria-label="Bosh sahifa"
          >
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-brand-ink">
              <GraduationCap size={18} />
            </span>
            <span className="font-display text-lg font-bold leading-none text-ink">
              Muallim
            </span>
          </button>
          <div className="flex items-center gap-2">
            <span className="hidden text-sm text-muted sm:inline">
              {me.username}
              {isTeacher && <span className="chip chip-gold ml-2">o'qituvchi</span>}
            </span>
            <ThemeToggle dark={dark} onToggle={toggleTheme} />
            <button type="button" onClick={handleLogout} className="btn btn-ghost btn-sm">
              <LogOut size={14} /> <span className="hidden sm:inline">Chiqish</span>
            </button>
          </div>
        </div>
        <div className="meander" />
      </header>

      <main className="mx-auto max-w-5xl px-4 pb-24 pt-8">
      {step === 'subjects' && (
        <SubjectsPage me={me} onOpenSubject={(sub) => { setSubject(sub); setStep('upload') }} />
      )}

      {step === 'upload' && (
        <UploadPage
          subject={subject}
          onBack={() => setStep('subjects')}
          isTeacher={isTeacher}
          onUploaded={handleUploaded}
          onOpenBook={async (b) => {
            setBook(b)
            await refreshTopics(b.id)
            setStep('topics')
          }}
        />
      )}

      {step === 'topics' && (
        <TopicSelectPage
          book={book}
          topics={topics}
          sections={sections}
          isTeacher={isTeacher}
          progress={progress}
          onOpenSectionExam={(section) => { setActiveSection(section); setStep('sectionExam') }}
          onSelect={(topic) => { setActiveTopic(topic); setStep('lesson') }}
          onBack={() => setStep('upload')}
          onOpenExam={() => setStep('exam')}
          onDownloadCertificate={() => downloadCertificate(book.id)}
        />
      )}

      {step === 'lesson' && (
        <LessonResultPage
          topicId={activeTopic.id}
          topicTitle={activeTopic.title}
          isTeacher={isTeacher}
          onBack={backToTopics}
          onStartTest={() => setStep('topicTest')}
        />
      )}

      {step === 'topicTest' && (
        <TestPage
          key={`t${activeTopic.id}`}
          title={`Mavzu testi: ${activeTopic.title}`}
          isTeacher={isTeacher}
          load={() => getAssetByTopic(activeTopic.id, 'topic_test')}
          create={() => createAsset(activeTopic.id, 'topic_test', { regenerate: true })}
          submit={(answers) => submitTopicTest(activeTopic.id, answers)}
          passedLabel="Mavzu to'liq o'zlashtirildi. Keyingi mavzu ochildi!"
          onBack={() => setStep('lesson')}
          onPassed={backToTopics}
        />
      )}

      {step === 'sectionExam' && (
        <TestPage
          key={`s${activeSection.id}`}
          title={`Bo'lim testi: ${activeSection.title}`}
          isTeacher={false}
          load={() => getSectionExam(activeSection.id)}
          create={async () => {}}
          submit={(answers) => submitSectionExam(activeSection.id, answers)}
          passedLabel="Bo'lim to'liq o'zlashtirildi. Keyingi bo'lim ochildi!"
          onBack={backToTopics}
          onPassed={backToTopics}
        />
      )}

      {step === 'exam' && (
        <TestPage
          key="exam"
          title={`Yakuniy imtihon: ${book.title}`}
          isTeacher={isTeacher}
          load={() => getBookExam(book.id)}
          create={() => createBookExam(book.id)}
          submit={(answers) => submitBookExam(book.id, answers)}
          passedLabel="Kitob muvaffaqiyatli tugatildi! Sertifikatingiz tayyor."
          onBack={backToTopics}
          onPassed={backToTopics}
        />
      )}
      </main>
    </div>
  )
}
