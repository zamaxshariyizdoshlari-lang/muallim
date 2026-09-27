import { GraduationCap, KeyRound, Loader2 } from 'lucide-react'
import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { confirmPasswordReset } from '../api/client'
import { ErrorNote, FontSizeToggle, ThemeToggle } from '../components/ui'

export default function ResetPasswordPage({ dark, onToggleTheme, fontSize, onChangeFontSize }) {
  const [params] = useSearchParams()
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await confirmPasswordReset(params.get('uid') || '', params.get('token') || '', password)
      setDone(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-5">
      <div className="absolute right-4 top-4 flex items-center gap-1.5">
        <FontSizeToggle size={fontSize} onChange={onChangeFontSize} />
        <ThemeToggle dark={dark} onToggle={onToggleTheme} />
      </div>
      <form onSubmit={handleSubmit} className="card rise w-full max-w-md p-7 sm:p-9">
        <span className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-brand text-brand-ink">
          <GraduationCap size={26} />
        </span>
        <h1 className="font-display text-2xl font-bold text-ink">Yangi parol o'rnating</h1>

        {done ? (
          <>
            <p className="mb-6 mt-3 text-sm text-ink-2">Parol yangilandi. Endi yangi parol bilan kirishingiz mumkin.</p>
            <Link to="/" className="btn btn-primary w-full">Kirishga o'tish</Link>
          </>
        ) : (
          <>
            <p className="mb-6 mt-1 text-sm text-muted">Kamida 8 belgidan iborat yangi parol kiriting.</p>
            <label className="mb-5 block text-sm font-medium text-ink-2">
              Yangi parol
              <input
                type="password"
                className="field mt-1.5"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
                required
              />
            </label>
            <ErrorNote>{error}</ErrorNote>
            <button type="submit" disabled={loading} className="btn btn-primary w-full py-3">
              {loading ? <Loader2 className="animate-spin" size={16} /> : <KeyRound size={16} />}
              Parolni yangilash
            </button>
          </>
        )}
      </form>
    </div>
  )
}
