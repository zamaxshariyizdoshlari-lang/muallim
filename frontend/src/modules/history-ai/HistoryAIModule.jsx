import { useState } from 'react'
import { getToken } from './api/client'
import LessonResultPage from './pages/LessonResultPage'
import LoginPage from './pages/LoginPage'
import TopicSelectPage from './pages/TopicSelectPage'
import UploadPage from './pages/UploadPage'

/**
 * Tarixchi AI modulining kirish nuqtasi. ERP'ga qo'shilganda bitta route
 * ostida shu komponent render qilinadi (masalan <Route path="/history-ai" element={<HistoryAIModule />} />).
 */
export default function HistoryAIModule() {
  const [authed, setAuthed] = useState(Boolean(getToken()))
  const [step, setStep] = useState('upload') // upload | topics | lesson
  const [book, setBook] = useState(null)
  const [topics, setTopics] = useState([])
  const [activeTopic, setActiveTopic] = useState(null)

  if (!authed) {
    return <LoginPage onSuccess={() => setAuthed(true)} />
  }

  function handleUploaded(newBook, newTopics) {
    setBook(newBook)
    setTopics(newTopics)
    setStep('topics')
  }

  function handleSelectTopic(topic) {
    setActiveTopic(topic)
    setStep('lesson')
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      {step === 'upload' && <UploadPage onUploaded={handleUploaded} />}

      {step === 'topics' && (
        <TopicSelectPage
          book={book}
          topics={topics}
          onSelect={handleSelectTopic}
          onBack={() => setStep('upload')}
        />
      )}

      {step === 'lesson' && (
        <LessonResultPage
          topicId={activeTopic?.id}
          topicTitle={activeTopic?.title}
          onBack={() => setStep('topics')}
        />
      )}
    </div>
  )
}
