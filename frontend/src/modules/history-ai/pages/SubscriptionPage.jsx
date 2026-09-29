import { Check, Crown, Loader2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { createSubscriptionCheckout, getSubscriptionStatus } from '../api/client'
import { BackLink, ErrorNote, SectionTitle } from '../components/ui'

const BENEFITS = [
  'Barcha fanlarning BARCHA bo\'limlariga cheksiz kirish',
  "Yangi qo'shiladigan har qanday kurs va mavzu",
  "Obuna istalgan vaqt to'xtatilishi mumkin - avtomatik yangilanmaydi",
]

export default function SubscriptionPage({ onBack }) {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState('')
  const [paying, setPaying] = useState('')

  useEffect(() => {
    getSubscriptionStatus().then(setStatus).catch((err) => setError(err.message))
  }, [])

  async function pay(gateway) {
    setError('')
    setPaying(gateway)
    try {
      const { checkout_url: url } = await createSubscriptionCheckout(gateway)
      window.location.href = url
    } catch (err) {
      setError(err.message)
      setPaying('')
    }
  }

  return (
    <div className="rise mx-auto max-w-xl">
      <BackLink onClick={onBack}>Orqaga</BackLink>
      <SectionTitle eyebrow="Obuna">Barcha fanlarga kirish</SectionTitle>

      {!status ? (
        <Loader2 className="animate-spin text-gold" size={22} />
      ) : status.active ? (
        <div className="card !border-ok/40 bg-ok-soft p-6 text-center">
          <Check className="mx-auto mb-2 text-ok" size={28} />
          <p className="font-display text-lg font-bold text-ink">Obunangiz faol!</p>
          {status.current_period_end && (
            <p className="mt-1 text-sm text-muted">
              Amal qilish muddati: {new Date(status.current_period_end).toLocaleDateString('uz-UZ')} gacha
            </p>
          )}
        </div>
      ) : (
        <>
          <div className="card relative mb-6 overflow-hidden p-6 sm:p-8">
            <div className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gold/10" aria-hidden />
            <div className="relative flex items-center gap-4">
              <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gold-soft text-gold">
                <Crown size={26} />
              </span>
              <div>
                <p className="font-display text-3xl font-extrabold text-ink">
                  {status.price?.toLocaleString('uz-UZ')} <span className="text-lg font-semibold text-muted">so'm / oy</span>
                </p>
                <p className="text-sm text-muted">Har bir fanning birinchi bo'limi hamon bepul qoladi</p>
              </div>
            </div>
            <ul className="relative mt-6 flex flex-col gap-2">
              {BENEFITS.map((b) => (
                <li key={b} className="flex items-start gap-2 text-sm text-ink-2">
                  <Check size={16} className="mt-0.5 shrink-0 text-ok" /> {b}
                </li>
              ))}
            </ul>
          </div>

          <ErrorNote>{error}</ErrorNote>

          <div className="flex flex-col gap-3">
            {status.payme_available && (
              <button
                onClick={() => pay('payme')}
                disabled={!!paying}
                className="btn btn-primary w-full justify-center !bg-[#00c8b3] !text-white hover:!brightness-95"
              >
                {paying === 'payme' ? <Loader2 className="animate-spin" size={16} /> : null} Payme orqali to'lash
              </button>
            )}
            {status.click_available && (
              <button
                onClick={() => pay('click')}
                disabled={!!paying}
                className="btn btn-primary w-full justify-center !bg-[#0077ff] !text-white hover:!brightness-95"
              >
                {paying === 'click' ? <Loader2 className="animate-spin" size={16} /> : null} Click orqali to'lash
              </button>
            )}
            {!status.payme_available && !status.click_available && (
              <p className="card p-4 text-center text-sm text-muted">
                To'lov tizimlari hozircha sozlanmagan - tez orada ishga tushadi.
              </p>
            )}
          </div>
        </>
      )}
    </div>
  )
}
