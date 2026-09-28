import { Check, Flame, Search, Trophy, UserMinus, UserPlus, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import {
  acceptFriendRequest, declineFriendRequest, getFriends, removeFriend, searchUsers, sendFriendRequest,
} from '../api/client'
import { ErrorNote, SectionTitle, Spinner } from '../components/ui'

export default function FriendsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [searching, setSearching] = useState(false)
  const [msg, setMsg] = useState(null)

  function load() {
    return getFriends().then(setData).catch((err) => setError(err.message))
  }

  useEffect(() => {
    load()
  }, [])

  useEffect(() => {
    const q = query.trim()
    if (q.length < 2) {
      setResults([])
      return
    }
    setSearching(true)
    const timer = setTimeout(() => {
      searchUsers(q).then((r) => setResults(r.items)).catch(() => {}).finally(() => setSearching(false))
    }, 300)
    return () => clearTimeout(timer)
  }, [query])

  async function act(fn, username, successText) {
    setMsg(null)
    try {
      await fn(username)
      setMsg({ ok: true, text: successText })
      setResults((r) => r.filter((u) => u.username !== username))
      await load()
    } catch (err) {
      setMsg({ text: err.message })
    }
  }

  if (error) return <ErrorNote>{error}</ErrorNote>
  if (!data) return <Spinner>Yuklanmoqda...</Spinner>

  return (
    <div className="rise mx-auto max-w-2xl">
      <SectionTitle eyebrow="Jamoa">Do'stlar</SectionTitle>
      <p className="-mt-2 mb-6 text-sm text-muted">
        Do'stlaringizni qo'shing va haftalik ball bo'yicha kim ko'proq o'rganayotganini ko'ring.
      </p>

      <div className="card mb-6 p-5">
        <h3 className="mb-3 font-display text-lg font-bold text-ink">Foydalanuvchi qidirish</h3>
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted" size={16} />
          <input
            className="field pl-9"
            placeholder="Foydalanuvchi nomi (kamida 2 harf)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        {msg && <p className={`mt-3 text-sm ${msg.ok ? 'text-ok' : 'text-bad'}`}>{msg.text}</p>}
        {searching && <p className="mt-3 text-xs text-muted">Qidirilmoqda...</p>}
        {results.length > 0 && (
          <ul className="mt-3 flex flex-col gap-2">
            {results.map((u) => (
              <li key={u.username} className="flex items-center justify-between rounded-lg bg-surface-2 px-3 py-2">
                <span className="text-sm font-medium text-ink">{u.name}</span>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => act(sendFriendRequest, u.username, `${u.name}ga so'rov yuborildi.`)}
                >
                  <UserPlus size={14} /> Qo'shish
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {data.incoming.length > 0 && (
        <div className="card mb-6 p-5">
          <h3 className="mb-3 font-display text-lg font-bold text-ink">Kiruvchi so'rovlar</h3>
          <ul className="flex flex-col gap-2">
            {data.incoming.map((u) => (
              <li key={u.username} className="flex items-center justify-between rounded-lg bg-surface-2 px-3 py-2">
                <span className="text-sm font-medium text-ink">{u.name}</span>
                <div className="flex gap-2">
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => act(acceptFriendRequest, u.username, `${u.name} bilan do'st bo'ldingiz.`)}
                  >
                    <Check size={14} /> Qabul qilish
                  </button>
                  <button
                    className="btn btn-sm"
                    onClick={() => act(declineFriendRequest, u.username, "So'rov rad etildi.")}
                  >
                    <X size={14} />
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.outgoing.length > 0 && (
        <div className="card mb-6 p-5">
          <h3 className="mb-3 font-display text-lg font-bold text-ink">Yuborilgan so'rovlar</h3>
          <ul className="flex flex-col gap-2">
            {data.outgoing.map((u) => (
              <li key={u.username} className="flex items-center justify-between rounded-lg bg-surface-2 px-3 py-2">
                <span className="text-sm text-ink-2">{u.name}</span>
                <button
                  className="btn btn-sm"
                  onClick={() => act(declineFriendRequest, u.username, "So'rov bekor qilindi.")}
                >
                  Bekor qilish
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="card p-5">
        <h3 className="mb-3 font-display text-lg font-bold text-ink">
          Do'stlaringiz {data.friends.length > 0 && `(${data.friends.length})`}
        </h3>
        {data.friends.length === 0 ? (
          <p className="text-sm text-muted">Hali do'stlaringiz yo'q. Yuqoridan qidirib, taklif yuboring.</p>
        ) : (
          <ol className="flex flex-col gap-2">
            {[data.me, ...data.friends]
              .sort((a, b) => b.weekly_points - a.weekly_points)
              .map((u, i) => (
                <li
                  key={u.username}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2.5 ${u.username === data.me.username ? 'bg-brand-soft' : 'bg-surface-2'}`}
                >
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-paper-2 text-xs font-bold text-ink-2">
                    {i + 1}
                  </span>
                  <span className="min-w-0 flex-1 truncate text-sm font-semibold text-ink">
                    {u.name} {u.username === data.me.username && <span className="chip chip-gold ml-1">siz</span>}
                  </span>
                  {u.streak > 0 && (
                    <span className="flex items-center gap-1 text-xs text-gold"><Flame size={13} /> {u.streak}</span>
                  )}
                  <span className="flex items-center gap-1 font-display text-sm font-bold text-ink">
                    <Trophy size={13} className="text-gold" /> {u.weekly_points}
                  </span>
                  {u.username !== data.me.username && (
                    <button
                      className="text-muted hover:text-bad"
                      title="Do'stlikni bekor qilish"
                      onClick={() => act(removeFriend, u.username, `${u.name} do'stlar ro'yxatidan chiqarildi.`)}
                    >
                      <UserMinus size={16} />
                    </button>
                  )}
                </li>
              ))}
          </ol>
        )}
      </div>
    </div>
  )
}
