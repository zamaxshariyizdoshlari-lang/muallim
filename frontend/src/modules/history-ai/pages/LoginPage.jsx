import { Landmark, LogIn, Loader2 } from 'lucide-react'
import { useState } from 'react'
import { login } from '../api/client'
import { ErrorNote, ThemeToggle } from '../components/ui'

export default function LoginPage({ onSuccess, dark, onToggleTheme }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(username, password)
      onSuccess()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
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
            <Landmark size={28} />
          </div>
          <p className="eyebrow mb-3">Qadimgi dunyo tarixi</p>
          <h1 className="font-display text-5xl font-extrabold leading-[1.05] text-ink sm:text-6xl">
            Tarixchi <span className="text-brand">AI</span>
          </h1>
          <p className="mt-5 max-w-md font-read text-lg leading-relaxed text-ink-2">
            Misr piramidalaridan Rim imperiyasigacha — darslikni mavzu-mavzu o'rganing, o'yinlar bilan mustahkamlang va
            sertifikat oling.
          </p>
          <div className="meander mt-8 max-w-xs" />
          <ul className="mt-6 flex flex-wrap gap-2 text-xs font-semibold text-ink-2">
            <li className="chip chip-gold">Mavzu-mavzu dars</li>
            <li className="chip chip-gold">O'yinlar va testlar</li>
            <li className="chip chip-gold">Sertifikat</li>
          </ul>
        </div>

        {/* O'ng: forma */}
        <form onSubmit={handleSubmit} className="card rise mx-auto w-full max-w-md p-7 sm:p-9" style={{ animationDelay: '0.1s' }}>
          <h2 className="font-display text-2xl font-bold text-ink">Xush kelibsiz</h2>
          <p className="mb-6 mt-1 text-sm text-muted">Davom etish uchun tizimga kiring</p>

          <label className="mb-4 block text-sm font-medium text-ink-2">
            Login
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
              autoComplete="current-password"
              required
            />
          </label>

          <ErrorNote>{error}</ErrorNote>

          <button type="submit" disabled={loading} className="btn btn-primary w-full py-3">
            {loading ? <Loader2 className="animate-spin" size={16} /> : <LogIn size={16} />}
            {loading ? 'Kirilmoqda...' : 'Kirish'}
          </button>
        </form>
      </div>
    </div>
  )
}
