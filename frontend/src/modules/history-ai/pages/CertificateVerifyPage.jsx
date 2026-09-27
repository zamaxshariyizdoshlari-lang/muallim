import { Award, BadgeCheck, GraduationCap, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { verifyCertificate } from '../api/client'
import { formatDateUz, Spinner, ThemeToggle } from '../components/ui'

/**
 * Ochiq (login talab qilmaydigan) sertifikat tekshiruvi: sertifikatdagi havola/kod orqali
 * istalgan kishi (masalan ish beruvchi) sertifikat haqiqiyligini tasdiqlashi mumkin.
 */
export default function CertificateVerifyPage({ dark, onToggleTheme }) {
  const { code } = useParams()
  const [result, setResult] = useState(null)

  useEffect(() => {
    verifyCertificate(code).then(setResult)
  }, [code])

  return (
    <div className="relative flex min-h-screen items-center justify-center px-5">
      <div className="absolute right-4 top-4">
        <ThemeToggle dark={dark} onToggle={onToggleTheme} />
      </div>
      <div className="w-full max-w-md">
        <div className="mb-6 flex items-center justify-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-brand-ink">
            <GraduationCap size={18} />
          </span>
          <span className="font-display text-lg font-bold text-ink">Muallim</span>
        </div>

        {!result ? (
          <div className="card p-8 text-center"><Spinner>Tekshirilmoqda...</Spinner></div>
        ) : result.valid ? (
          <div className="card rise p-8 text-center">
            <span className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-ok-soft text-ok">
              <BadgeCheck size={28} />
            </span>
            <p className="eyebrow mb-1">Sertifikat tasdiqlandi</p>
            <h1 className="font-display text-2xl font-bold text-ink">{result.student_name}</h1>
            <p className="mt-3 flex items-center justify-center gap-2 font-read text-base text-ink-2">
              <Award size={16} className="text-gold" /> "{result.book_title}"
            </p>
            <p className="mt-4 text-sm text-muted">
              {formatDateUz(result.issued_at)} sanasida Muallim platformasida kursni to'liq yakunlagani uchun berilgan.
            </p>
          </div>
        ) : (
          <div className="card rise p-8 text-center">
            <span className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-bad-soft text-bad">
              <XCircle size={28} />
            </span>
            <p className="font-display text-xl font-bold text-ink">Bunday sertifikat topilmadi</p>
            <p className="mt-2 text-sm text-muted">Havola noto'g'ri yoki sertifikat mavjud emas.</p>
          </div>
        )}
        <p className="mt-6 text-center text-sm">
          <Link to="/" className="text-muted hover:text-brand">Muallim platformasiga o'tish</Link>
        </p>
      </div>
    </div>
  )
}
