/**
 * Sxematik xarita uchun joylar ro'yxati (taxminiy geografik koordinatalar: uzunlik, kenglik).
 * Xaritada FAQAT shaharlar, daryolar va yo'nalish o'qlari ko'rsatiladi - bahsli davlat chegaralari
 * ataylab chizilmaydi. Joy `id` lari kontent JSON (`explanation.maps`) da ishlatiladi.
 */

export const PLACES = {
  samarqand: { name: 'Samarqand', lon: 66.96, lat: 39.65 },
  buxoro: { name: 'Buxoro', lon: 64.42, lat: 39.77 },
  marv: { name: 'Marv', lon: 62.19, lat: 37.66 },
  balx: { name: 'Balx', lon: 66.9, lat: 36.76 },
  termiz: { name: 'Termiz', lon: 67.28, lat: 37.22 },
  urganch: { name: 'Gurganch (Urganch)', lon: 59.15, lat: 42.32 },
  kat: { name: 'Kat', lon: 60.75, lat: 41.69 },
  xiva: { name: 'Xiva', lon: 60.36, lat: 41.38 },
  toshkent: { name: 'Toshkent (Choch)', lon: 69.24, lat: 41.3 },
  nishopur: { name: 'Nishopur', lon: 58.8, lat: 36.21 },
  hirot: { name: 'Hirot', lon: 62.2, lat: 34.35 },
  gazna: { name: "G'azna", lon: 68.0, lat: 33.55 },
  qoshgar: { name: "Qoshg'ar", lon: 75.99, lat: 39.47 },
  balasogun: { name: "Balasog'un", lon: 75.25, lat: 42.75 },
  otror: { name: "O'tror (Forob)", lon: 68.3, lat: 42.85 },
  taraz: { name: 'Taraz (Talas)', lon: 71.37, lat: 42.9 },
  jurjon: { name: 'Jurjon', lon: 54.4, lat: 36.8 },
  ray: { name: 'Rayy', lon: 51.4, lat: 35.6 },
  quva: { name: 'Quva', lon: 71.98, lat: 40.52 },
  panjikent: { name: 'Panjikent', lon: 67.6, lat: 39.5 },
}

/** Hududlar: nuqtasiz, faqat qiya yozuv bilan. */
export const REGIONS = {
  xorazm: { name: 'Xorazm', lon: 60.2, lat: 43.2 },
  fargona: { name: "Farg'ona vodiysi", lon: 71.2, lat: 40.2 },
  sugd: { name: "Sug'd", lon: 66.6, lat: 40.5 },
  toxariston: { name: 'Toxariston', lon: 68.6, lat: 37.9 },
  xuroson: { name: 'Xuroson', lon: 59.8, lat: 35.4 },
  yettisuv: { name: 'Yettisuv', lon: 77.0, lat: 44.0 },
}

export const SEAS = [
  {
    name: 'Orol dengizi',
    label: [59.6, 45.0],
    coords: [[58.3, 44.2], [59.0, 45.9], [60.6, 46.5], [61.6, 45.7], [61.0, 44.4], [59.8, 43.7]],
  },
  {
    name: 'Kaspiy dengizi',
    label: [51.0, 42.0],
    coords: [[50, 46.8], [50.8, 46.0], [51.7, 44.6], [52.8, 42.7], [52.8, 41.3], [53.0, 40.0], [53.1, 38.6], [54.0, 37.2], [50, 37.2]],
  },
]

export const RIVERS = [
  {
    name: 'Amudaryo',
    label: [62.4, 40.6],
    coords: [[72.5, 37.0], [70.0, 37.3], [67.3, 37.3], [65.5, 38.2], [63.6, 39.1], [62.0, 40.6], [60.9, 41.6], [60.2, 42.7], [59.6, 43.8]],
  },
  {
    name: 'Sirdaryo',
    label: [66.0, 44.6],
    coords: [[72.5, 40.9], [71.2, 40.9], [69.6, 40.3], [68.8, 40.9], [68.3, 41.9], [67.4, 43.5], [65.2, 44.6], [63.5, 45.3], [61.2, 46.0]],
  },
]

export const FRAME = { lon0: 50, lon1: 78, lat0: 32.5, lat1: 47, k: 38 }
const COS = Math.cos((40 * Math.PI) / 180)

export function project(lon, lat) {
  const { lon0, lat1, k } = FRAME
  return [(lon - lon0) * COS * k, (lat1 - lat) * k]
}

export const MAP_SIZE = (() => {
  const [w] = project(FRAME.lon1, FRAME.lat1)
  const [, h] = project(FRAME.lon0, FRAME.lat0)
  return { w: Math.round(w), h: Math.round(h) }
})()
