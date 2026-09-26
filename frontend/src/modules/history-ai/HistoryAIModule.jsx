import { useEffect, useState } from 'react'
import {
  createAsset, createBookExam, downloadCertificate, getAssetByTopic, getBookExam, getBookProgress, getMe,
  getToken, listTopics, submitBookExam, submitTopicTest,
} from './api/client'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import TestPage from './pages/TestPage'
import TopicSelectPage from './pages/TopicSelectPage'
import UploadPage from './pages/UploadPage'

/**
 * Tarixchi AI modulining kirish nuqtasi. ERP'ga qo'shilganda bitta route
 * ostida shu komponent render qilinadi (masalan <Route path="/history-ai" element={<HistoryAIModule />} />).
 */
export default function HistoryAIModule() {
  const [authed, setAuthed] = useState(Boolean(getToken()))
  const [me, setMe] = useState(null)
  const [step, setStep] = useState('upload') // upload | topics | lesson | topicTest | exam
  const [book, setBook] = useState(null)
  const [topics, setTopics] = useState([])
  const [progress, setProgress] = useState(null)
  const [activeTopic, setActiveTopic] = useState(null)

  useEffect(() => {
    if (authed) getMe().then(setMe).catch(() => setAuthed(false))
  }, [authed])

  if (!authed) {
    return <LoginPage onSuccess={() => setAuthed(true)} />
  }
  if (!me) return null

  const isTeacher = me.is_staff

  async function refreshTopics(bookId = book.id) {
    const [freshTopics, freshProgress] = await Promise.all([listTopics(bookId), getBookProgress(bookId)])
    setTopics(freshTopics)
    setProgress(freshProgress)
  }

  async function handleUploaded(newBook, newTopics) {
    setBook(newBook)
    setTopics(newTopics)
    setProgress(await getBookProgress(newBook.id))
    setStep('topics')
  }

  async function backToTopics() {
    await refreshTopics()
    setStep('topics')
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      {step === 'upload' && (
        <UploadPage
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
          isTeacher={isTeacher}
          progress={progress}
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
    </div>
  )
}
