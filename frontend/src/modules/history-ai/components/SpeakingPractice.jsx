import { Mic, Square, Volume2 } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { speak } from '../utils/speech'

const canRecord = () =>
  typeof navigator !== 'undefined' && Boolean(navigator.mediaDevices?.getUserMedia) && typeof MediaRecorder !== 'undefined'

/** Gapirish mashqi: nutqni tanish/baholash yo'q (qimmat va murakkab). Talaba jumlani tinglaydi,
 * ovoz chiqarib takrorlaydi va ixtiyoriy ravishda o'z ovozini yozib, original bilan solishtiradi.
 * Yozuv faqat brauzer xotirasida qoladi - serverga yuborilmaydi. */
export default function SpeakingPractice({ sentences }) {
  if (!sentences?.length) return null
  const recordable = canRecord()
  return (
    <div className="flex flex-col gap-2.5">
      <p className="mb-1 flex items-center gap-2 text-sm text-muted">
        <Mic size={15} />
        {recordable
          ? " Jumlani tinglang, so'ng mikrofon tugmasi bilan o'z ovozingizni yozib, eshitib ko'ring. Yozuv telefoningizda qoladi."
          : " Har jumlani tinglang, keyin ovoz chiqarib takrorlang. Baholanmaydi - mashq uchun."}
      </p>
      {sentences.map((s, i) => (
        <SentenceRow key={i} sentence={s} recordable={recordable} />
      ))}
    </div>
  )
}

function SentenceRow({ sentence, recordable }) {
  const [recording, setRecording] = useState(false)
  const [clipUrl, setClipUrl] = useState(null)
  const [error, setError] = useState('')
  const recorderRef = useRef(null)
  const audioRef = useRef(null)

  // Sahifadan chiqqanda mikrofon va vaqtinchalik havolani bo'shatish
  useEffect(() => () => {
    recorderRef.current?.stream?.getTracks().forEach((t) => t.stop())
    if (clipUrl) URL.revokeObjectURL(clipUrl)
  }, [clipUrl])

  async function toggleRecord() {
    setError('')
    if (recording) {
      recorderRef.current?.stop()
      return
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const rec = new MediaRecorder(stream)
      const chunks = []
      rec.ondataavailable = (e) => chunks.push(e.data)
      rec.onstop = () => {
        stream.getTracks().forEach((t) => t.stop())
        setClipUrl(URL.createObjectURL(new Blob(chunks, { type: rec.mimeType || 'audio/webm' })))
        setRecording(false)
      }
      recorderRef.current = rec
      rec.start()
      setRecording(true)
    } catch {
      setError("Mikrofonga ruxsat berilmadi.")
    }
  }

  return (
    <div className="rounded-xl bg-surface-2 px-4 py-3">
      <div className="flex items-center justify-between gap-3">
        <span className="font-read text-base text-ink">{sentence}</span>
        <div className="flex shrink-0 items-center gap-1">
          <button onClick={() => speak(sentence)} className="btn btn-ghost btn-sm" aria-label={`"${sentence}" ni tinglash`}>
            <Volume2 size={16} />
          </button>
          {recordable && (
            <button
              onClick={toggleRecord}
              className={`btn btn-sm ${recording ? 'btn-primary' : 'btn-ghost'}`}
              aria-label={recording ? "Yozishni to'xtatish" : "O'z ovozimni yozish"}
              aria-pressed={recording}
            >
              {recording ? <Square size={14} /> : <Mic size={16} />}
            </button>
          )}
        </div>
      </div>
      {clipUrl && (
        <audio ref={audioRef} src={clipUrl} controls className="mt-2 h-9 w-full" aria-label="Sizning yozuvingiz" />
      )}
      {error && <p className="mt-2 text-xs text-bad">{error}</p>}
    </div>
  )
}
