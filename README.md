# Muallim

**Muallim** — ommaviy onlayn ta'lim platformasi: mavzu-mavzu dars, o'yinlar, testlar, ball/reyting va
sertifikat bilan. Har kim bepul ro'yxatdan o'tib o'qiy oladi. Hozircha ikkita yo'nalish bor:

- 📜 **Tarix** — "Qadimgi dunyo tarixi" (6-sinf) va "O'zbekiston tarixi" (7-sinf, IV asrdan XIII asr
  boshigacha) darsliklari asosida, betlarga aniq iqtibos bilan.
- 🇹🇷 **Turk tili (A1)** — "Yedi İklim" darsligi tuzilishi asosida: grammatika, so'z boyligi
  (kartochkalar), tinglash, o'qish, yozish va gapirish mashqlari — TYS va Milliy sertifikat
  imtihonlarining 4 ko'nikmasiga moslab qurilgan.

Loyihaning asosiy tamoyili: **xarajatni minimallashtirish**. Kontent oldindan tayyorlanadi va JSON
sifatida saqlanadi — foydalanuvchi o'qiyotganda hech qanday AI so'rovi yuborilmaydi.

## Xususiyatlar

- **O'rganish yo'li**: tushuntirish → kartochka/o'yinlar → mavzu testi (80%+) → bo'lim testi (80%+) →
  yakuniy imtihon → PDF sertifikat (ochiq havola orqali tekshiriladigan).
- **Gamifikatsiya**: ball, daraja, kunlik ketma-ketlik (streak, "muzlatish" bilan), kunlik maqsad,
  haftalik reyting, nishonlar.
- **Maslahat va izohlar**: testda bosqichli maslahat (darslik joyi → 2 ta noto'g'ri variantni olib tashlash), savollarda ixtiyoriy `explanation` ("Nega?" izohi, o'tilgach ko'rsatiladi), 2 marta o'tolmasa darsga qaytish tavsiyasi.
- **Asosiy fikrlar va eslab qolish**: har mavzuda "Katta rasm" (o'qishdan oldin) va oxirida xulosa uchun 3 ta asosiy fikr (`takeaways`), sanalar va ketma-ketliklar uchun "Eslab qolish usuli" (`mnemonics`).
- **Aralash mashq**: o'tilgan mavzulardan aralash 10 savol (oxirgi hafta ko'proq) - interleaving; xatolar takrorlash kartochkasiga tushadi.
- **Xatolarni takrorlash**: oraliq takrorlash (spaced repetition) — xato javob kartochka sifatida
  saqlanadi va 1→3→7→14→30 kunlik oraliqda qaytadi.
- **Ikki panel**: foydalanuvchi ilovasi (React) va to'liq nazorat uchun Django admin paneli
  (foydalanuvchilar, statistika, sertifikatlar, kontent).
- **PWA**: ko'rilgan darslar offline ochiladi.
- **Qulaylik**: matn o'lchamini o'zgartirish, klaviatura navigatsiyasi, ekran o'quvchi bilan mos.

## Texnologiyalar

| Qism | Texnologiya |
|---|---|
| Backend | Django 6, Django REST Framework, SQLite (yoki PostgreSQL) |
| Frontend | React 19, React Router, Tailwind CSS v4, Vite, Lucide ikonkalar |
| Autentifikatsiya | DRF Token Authentication |
| Sertifikat | fpdf2 (server tomonida PDF yaratish) |

## Loyihani lokal ishga tushirish

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py import_book content/qd6/book.json --user <admin_foydalanuvchi_nomi>
python manage.py import_book content/turk_a1/book.json --user <admin_foydalanuvchi_nomi>
python manage.py import_book content/ozb7/book.json --user <admin_foydalanuvchi_nomi>
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Ilova `http://localhost:5173` da, admin panel esa `http://localhost:8000/admin/` da ochiladi.

## Kontent qo'shish

Yangi kurs (kitob) JSON formatida tayyorlanadi va import qilinadi — batafsil format
`backend/history_ai/services/book_import.py` dagi `validate_book_json` funksiyasida tasvirlangan.
Mavjud namunalar: `backend/content/qd6/book.json` (tarix, betlarga iqtibos bilan) va
`backend/content/turk_a1/book.json` (til kursi: kartochka, tinglash, o'qish, yozish, gapirish).

### Darsni boyituvchi ixtiyoriy maydonlar

Mavzuning `explanation` qismiga qo'shiladi (hammasi ixtiyoriy):

| Maydon | Vazifasi |
|---|---|
| `pretest` | Dars boshidagi "oldindan sinash" savollari (bo'lmasa mini-viktorinadan olinadi) |
| `blocks[].check` | Blok tagidagi mini-savol (bo'lmasa mini-viktorinadan bet bo'yicha olinadi) |
| `why` | `{causes: [...], effects: [...]}` — "Nega shunday bo'ldi?" bloki |
| `source_work` | `{quote, attribution, question, options, correct_index}` — manba bilan ishlash |
| `images` | `[{src, caption, question?}]` — xarita/rasm (fayl `frontend/public/` ichida) |

Test savollariga `level` (`eslash` / `tushunish` / `qollash`) va `tag` (qism nomi) qo'yish mumkin;
berilmasa import paytida taxminiy qiymat qo'yiladi (`services/enrichment.py`).
Test o'tish foizi `PASS_PERCENT` (standart 100) muhit o'zgaruvchisi bilan sozlanadi.
Admin panelda **Sifat nazorati** tabi har mavzuning to'liqligini va talabalar bahosini ko'rsatadi.

## Serverga joylashtirish

To'liq qo'llanma: [DEPLOY.md](DEPLOY.md) — Nginx, Gunicorn, PostgreSQL, HTTPS, zaxira nusxa,
monitoring va admin panel haqida.

## Hissa qo'shish

Xato topsangiz yoki taklifingiz bo'lsa, Issue oching yoki Pull Request yuboring. Loyiha MIT litsenziyasi
ostida tarqatiladi ([LICENSE](LICENSE)).
