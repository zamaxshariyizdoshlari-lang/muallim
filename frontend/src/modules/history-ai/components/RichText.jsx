/**
 * Dars matnida oddiy belgilash: `**muhim so'z**` qalin qilib, `==testda chiqishi mumkin=='
 * esa sariq belgilagich (highlight) bilan ko'rsatiladi. Til tashuvchi kontent (admin qo'lda
 * yozgan yoki AI import qilgan) shu ikki sintaksisdan foydalanishi mumkin - alohida
 * formatlash vositasi (rich text editor) shart emas.
 */
const PATTERN = /(\*\*(.+?)\*\*|==(.+?)==)/g

export default function RichText({ text, className }) {
  if (!text) return null
  const nodes = []
  let lastIndex = 0
  let match
  let key = 0
  PATTERN.lastIndex = 0
  while ((match = PATTERN.exec(text))) {
    if (match.index > lastIndex) nodes.push(text.slice(lastIndex, match.index))
    if (match[2] !== undefined) {
      nodes.push(<strong key={key++} className="font-bold text-ink">{match[2]}</strong>)
    } else {
      nodes.push(
        <mark key={key++} className="rounded bg-gold-soft px-1 py-0.5 font-semibold text-ink">
          {match[3]}
        </mark>,
      )
    }
    lastIndex = PATTERN.lastIndex
  }
  if (lastIndex < text.length) nodes.push(text.slice(lastIndex))
  return className ? <span className={className}>{nodes}</span> : nodes
}
