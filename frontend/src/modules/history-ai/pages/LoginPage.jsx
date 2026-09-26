import { GraduationCap, Loader2, LogIn, UserPlus } from 'lucide-react'
import { useState } from 'react'
import { login, register, requestPasswordReset } from '../api/client'
import { ErrorNote, ThemeToggle } from '../components/ui'

export default function LoginPage({ onSuccess, dark, onToggleTheme }) {
  const [mode, setMode] = useState('login') // login | register | forgot
  const [email, setEmail] = useState('')
  const [info, setInfo] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const isRegister = mode === 'register'
  const isForgot = mode === 'forgot'

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)
    try {
      if (isForgot) {
        const r = await requestPasswordReset(email.trim())
        setInfo(r.detail)
        return
      }
      if (isRegister) await register(username.trim(), password, firstName.trim(), email.trim())
      else await login(username.trim(), password)
      onSuccess()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function switchMode(next) {
    setMode(next)
    setError('')
    setInfo('')
  }

  return (
    <div className="relative min-h-screen">
      <div className="absolute right-4 top-4 z-10">
        <ThemeToggle dark={dark} onToggle={onToggleTheme} />
      </div>

      <div className="mx-auto grid min-h-screen max-w-6xl items-center gap-10 px-5 py-10 lg:grid-cols-2 lg:gap-16">
        {/* Chap: g'oya */}
        <div className="rise">
          <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-brand text-brand-ink shadow-lg">
            <GraduationCap size={30} />
          </div>
          <p className="eyebrow mb-3">Onlayn ta'lim platformasi</p>
          <h1 className="font-display text-5xl font-extrabold leading-[1.05] text-ink sm:text-6xl">
            Muallim
          </h1>
          <p className="mt-5 max-w-md font-read text-lg leading-relaxed text-ink-2">
            Tarix, til va boshqa fanlarni mavzu-mavzu o'rganing. Har mavzuda tushuntirish, o'yinlar va test; oxirida
            sertifikat.
          </p>
          <div className="meander mt-8 max-w-xs" />
          <ul className="mt-6 flex flex-wrap gap-2 text-xs font-semibold text-ink-2">
            <li className="chip chip-gold">Bepul ro'yxatdan o'tish</li>
            <li className="chip chip-gold">Mavzu-mavzu dars</li>
            <li className="chip chip-gold">O'yinlar va testlar</li>
            <li className="chip chip-gold">Sertifikat</li>
          </ul>
        </div>

        {/* O'ng: forma */}
        <form onSubmit={handleSubmit} className="card rise mx-auto w-full max-w-md p-7 sm:p-9" style={{ animationDelay: '0.1s' }}>
          {!isForgot && (
          <div className="mb-6 grid grid-cols-2 rounded-xl bg-paper-2 p-1 text-sm font-semibold">
            {[['login', 'Kirish'], ['register', "Ro'yxatdan o'tish"]].map(([m, label]) => (
              <button
                key={m}
                type="button"
                onClick={() => switchMode(m)}
                className={`rounded-lg px-3 py-2 transition-colors ${
                  mode === m ? 'bg-surface text-ink shadow' : 'text-muted hover:text-ink'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
          )}

          <h2 className="font-display text-2xl font-bold text-ink">
            {isForgot ? 'Parolni tiklash' : isRegister ? 'Yangi hisob yarating' : 'Xush kelibsiz'}
          </h2>
          <p className="mb-6 mt-1 text-sm text-muted">
            {isForgot
              ? "Ro'yxatdan o'tishda kiritgan elektron pochtangizni yozing — tiklash havolasini yuboramiz."
              : isRegister
                ? "Bir daqiqada ro'yxatdan o'ting va o'qishni boshlang"
                : 'Davom etish uchun tizimga kiring'}
          </p>

          {isRegister && (
            <label className="mb-4 block text-sm font-medium text-ink-2">
              Ismingiz
              <input
                className="field mt-1.5"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                autoComplete="given-name"
                maxLength={60}
                placeholder="Masalan: Ali"
              />
            </label>
          )}

          {isForgot && (
            <label className="mb-5 block text-sm font-medium text-ink-2">
              Elektron pochta
              <input
                type="email"
                className="field mt-1.5"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />
            </label>
          )}

          {!isForgot && (
          <>
          <label className="mb-4 block text-sm font-medium text-ink-2">
            Foydalanuvchi nomi
            <input
              className="field mt-1.5"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </label>

          <label className="mb-5 block text-sm font-medium text-ink-2">
            Parol
            <input
              type="password"
              className="field mt-1.5"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={isRegister ? 'new-password' : 'current-password'}
              required
            />
            {isRegister && <span className="mt-1.5 block text-xs font-normal text-muted">Kamida 8 belgi.</span>}
          </label>

          {isRegister && (
            <label className="mb-5 block text-sm font-medium text-ink-2">
              Elektron pochta <span className="font-normal text-muted">(ixtiyoriy — parolni tiklash uchun)</span>
              <input
                type="email"
                className="field mt-1.5"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
              />
            </label>
          )}
          </>
          )}

          <ErrorNote>{error}</ErrorNote>
          {info && <p className="mb-4 rounded-xl border border-ok/40 bg-ok-soft px-4 py-2.5 text-sm text-ok">{info}</p>}

          <button type="submit" disabled={loading} className="btn btn-primary w-full py-3">
            {loading ? <Loader2 className="animate-spin" size={16} /> : isRegister ? <UserPlus size={16} /> : <LogIn size={16} />}
            {loading ? 'Iltimos, kuting...' : isForgot ? 'Havola yuborish' : isRegister ? "Ro'yxatdan o'tish" : 'Kirish'}
          </button>

          {mode === 'login' && (
            <button type="button" onClick={() => switchMode('forgot')} className="mt-4 w-full text-center text-sm text-muted hover:text-brand">
              Parolni unutdingizmi?
            </button>
          )}
          {isForgot && (
            <button type="button" onClick={() => switchMode('login')} className="mt-4 w-full text-center text-sm text-muted hover:text-brand">
              ← Kirishga qaytish
            </button>
          )}
        </form>
      </div>
    </div>
  )
}
