# Muallim — serverga joylashtirish

Ikki yo'l bor: **bepul sinov** (Render + Vercel, domensiz) yoki **o'z serveringiz** (domen bilan,
to'liq nazorat). Sinov uchun 0-bo'limni, haqiqiy foydalanish uchun 1–6 bo'limlarni o'qing.

## 0. Bepul sinov: Render (backend) + Vercel (frontend)

Domen sotib olmasdan, boshqa odamlar sinab ko'rishi uchun bepul manzil bilan joylashtirish.

**Backend (Render):**
1. [render.com](https://render.com) da ro'yxatdan o'ting (GitHub hisobingiz bilan kirsangiz qulay).
2. **New +** → **Blueprint** → ushbu GitHub repo (`muallim`) ni tanlang. Render repo ildizidagi
   `render.yaml` faylini o'qib, backend xizmati va bepul PostgreSQL bazasini avtomatik taklif qiladi.
3. **Apply** bosing. Render sizga manzil beradi, masalan `https://muallim-api-a1b2.onrender.com`.
4. Agar manzil `render.yaml` dagi `muallim-api.onrender.com` dan farq qilsa (odatda farq qiladi),
   Render paneli → xizmatingiz → **Environment** ga kirib, `ALLOWED_HOSTS` qiymatini haqiqiy
   manzilga almashtiring va qayta joylashtiring (**Manual Deploy**).
5. Tekshirish: `https://<manzilingiz>/api/health/` — `{"status":"ok"}` qaytarishi kerak.
6. **Bepul rejada Shell yo'q** (faqat pullik Starter rejada bor), shuning uchun admin hisobi va
   kontent build buyrug'i orqali avtomatik yaratiladi. Render paneli → xizmatingiz →
   **Environment** ga quyidagi 3 tasini qo'shing (qiymatlarni o'zingiz tanlang):
   - `DJANGO_SUPERUSER_USERNAME` = masalan `admin`
   - `DJANGO_SUPERUSER_EMAIL` = sizning emailingiz
   - `DJANGO_SUPERUSER_PASSWORD` = kuchli parol
   Saqlab, qayta joylashtirilganda `render.yaml`dagi build buyrug'i `createsuperuser --noinput`
   va ikkala kursni (`content/qd6/book.json`, `content/turk_a1/book.json`) shu foydalanuvchi
   nomidan avtomatik import qiladi (loglar orqali tekshirib bo'ladi). `createsuperuser`
   `|| true` bilan himoyalangan (keyingi deploylarda hisob allaqachon bor bo'lsa xato bermaydi),
   lekin kontent import buyruqlari himoyalanmagan - shu sabab agar import muvaffaqiyatsiz
   tugasa (masalan JSON noto'g'ri bo'lsa), build xato bilan to'xtaydi va loglarda sababi ko'rinadi,
   aks holda kontent jim-jit import qilinmay qolib, sayt bo'sh (testlar yo'q) holda ishga tushardi.

**Frontend (Vercel):**
1. [vercel.com](https://vercel.com) da GitHub hisobingiz bilan kiring.
2. **Add New** → **Project** → `muallim` repo'ni tanlang.
3. **Root Directory** ni `frontend` qilib belgilang (Vercel Vite'ni avtomatik aniqlaydi).
4. **Environment Variables** bo'limiga (Render'dan olgan haqiqiy manzilingiz bilan) qo'shing:
   - `VITE_HISTORY_API_BASE_URL` = `https://<render-manzilingiz>/api/history`
   - `VITE_AUTH_TOKEN_URL` = `https://<render-manzilingiz>/api/auth/token/`
   - `VITE_AUTH_REGISTER_URL` = `https://<render-manzilingiz>/api/auth/register/`
5. **Deploy** bosing. Bir necha daqiqada `https://muallim.vercel.app` (yoki shunga o'xshash) tayyor bo'ladi.
6. Render paneliga qaytib, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `FRONTEND_URL`
   qiymatlarini haqiqiy Vercel manzilingizga yangilang va qayta joylashtiring.

**Bepul rejaning cheklovlari (bilib qo'ying):**
- Render'ning bepul veb-xizmati ~15 daqiqa harakatsizlikdan keyin "uxlab qoladi" — birinchi so'rov
  10-30 soniya sekinroq bo'lishi mumkin, keyingilari tez ishlaydi.
- Bepul PostgreSQL 90 kundan keyin avtomatik o'chadi (Render ogohlantiradi) — sinov muddati tugagach
  yangi baza yaratib, kerak bo'lsa ma'lumotni ko'chirish kerak bo'ladi.
- Sertifikat fayllari (`media/`) doimiy diskda saqlanmaydi — qayta joylashtirilganda yo'qolishi mumkin
  (baza yozuvi qoladi, lekin fayl yo'qolsa qayta yuklab bo'lmaydi). Uzoq muddatli foydalanish uchun
  1-bo'limdagi haqiqiy serverga o'ting.

## 1. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # DEBUG=False, SECRET_KEY, ALLOWED_HOSTS, DB_*, SMTP, FRONTEND_URL ni to'ldiring
python manage.py migrate
python manage.py createcachetable   # USE_DB_CACHE=1 bo'lsa
python manage.py collectstatic --noinput
python manage.py createsuperuser    # sizning admin hisobingiz - /admin/ ga shu bilan kirasiz
python manage.py import_book content/qd6/book.json --user <admin_foydalanuvchi_nomi>
gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000
```
Tekshirish: `python manage.py check --deploy` — ogohlantirishsiz bo'lishi kerak.

## 2. Frontend
```bash
cd frontend
cat > .env.production <<'ENV'
VITE_HISTORY_API_BASE_URL=https://muallim.uz/api/history
VITE_AUTH_TOKEN_URL=https://muallim.uz/api/auth/token/
VITE_AUTH_REGISTER_URL=https://muallim.uz/api/auth/register/
ENV
npm ci && npm run build        # dist/ ni Nginx beradi
```

## Admin panel

Ilovaning o'zida "o'qituvchi" yoki boshqaruv ekrani yo'q - platforma ikkita alohida qismdan iborat:
- **Foydalanuvchi ilovasi** (`muallim.uz`) - istalgan kishi ro'yxatdan o'tib o'qiydi.
- **Admin panel** (`muallim.uz/admin/`) - faqat `createsuperuser` bilan yaratilgan hisob kira oladi.
  - Bosh sahifadagi "📊 Platforma statistikasi" - talabalar soni, bugungi faollik, mashhur kurs.
  - **Users** - har bir talabaning ball/mavzu/sertifikat soni ko'rinadi; bloklash, faollashtirish,
    admin huquqi berish shu yerdan.
  - **Certificates** - berilgan sertifikatlarni ko'rish, kerak bo'lsa bekor qilish (o'chirish).
  - **Books/Subjects/Topics** va boshqa hammasi - to'liq ko'rish/tahrirlash.
  - Yangi kurs qo'shish JSON orqali (`manage.py import_book`) qilinadi, admin panelning o'zidan emas.

## 3. Nginx (qisqacha)
- `/` -> `frontend/dist` (SPA: `try_files $uri /index.html`), `sw.js` uchun `Cache-Control: no-cache`.
- `/api/` va `/admin/` -> `http://127.0.0.1:8000` (`X-Forwarded-Proto` ni uzating).
- `/static/` -> `backend/staticfiles`, `/media/` -> `backend/media` (sertifikatlar).
- HTTPS: `certbot --nginx`.

## 4. Zaxira nusxa
`backend/scripts/backup.sh` — bazani va `media/` ni sana bilan saqlaydi. Cron:
```
0 3 * * * /srv/muallim/backend/scripts/backup.sh >> /var/log/muallim-backup.log 2>&1
```
Zaxirani boshqa serverga/ombor (S3, Backblaze) ga nusxalashni unutmang, tiklashni vaqti-vaqti bilan sinang.

## 5. Monitoring
- `GET /api/health/` -> `{"status":"ok"}` (UptimeRobot / Better Stack kabi bepul xizmat bilan tekshiring).
- Xatolar Gunicorn/journal logiga tushadi (`journalctl -u muallim`). Ixtiyoriy: Sentry.

## 6. Elektron pochta
`.env` da SMTP (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`) ni kiriting.
Domen uchun SPF/DKIM sozlanmasa xatlar spamga tushadi.
