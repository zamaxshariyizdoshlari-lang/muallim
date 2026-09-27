/** Brauzerning o'z ovozi orqali talaffuz (bepul, server kerak emas). Http bo'lmagan yoki
 * qo'llab-quvvatlamaydigan muhitda jim ishlamay qoladi - xato tashlamaydi. */
export function isSpeechSupported() {
  return typeof window !== 'undefined' && 'speechSynthesis' in window
}

export function speak(text, lang = 'tr-TR', rate = 0.9) {
  if (!isSpeechSupported() || !text) return
  try {
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(text)
    u.lang = lang
    u.rate = rate
    const voice = window.speechSynthesis.getVoices().find((v) => v.lang === lang || v.lang?.startsWith('tr'))
    if (voice) u.voice = voice
    window.speechSynthesis.speak(u)
  } catch {
    /* ovoz mavjud emas - jim o'tkazib yuboriladi */
  }
}

/** Bir nechta jumlani ketma-ket, biri tugagach ikkinchisi boshlanadigan qilib o'qiydi (dialog uchun). */
export function speakSequence(texts, lang = 'tr-TR', rate = 0.9) {
  if (!isSpeechSupported() || !texts?.length) return
  window.speechSynthesis.cancel()
  let i = 0
  function next() {
    if (i >= texts.length) return
    const u = new SpeechSynthesisUtterance(texts[i])
    u.lang = lang
    u.rate = rate
    const voice = window.speechSynthesis.getVoices().find((v) => v.lang === lang || v.lang?.startsWith('tr'))
    if (voice) u.voice = voice
    u.onend = () => {
      i += 1
      next()
    }
    window.speechSynthesis.speak(u)
  }
  next()
}
