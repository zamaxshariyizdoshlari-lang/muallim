# Muallim — serverga joylashtirish

Minimal tavsiya: bitta Linux server (Ubuntu), Nginx, Gunicorn, PostgreSQL, HTTPS (Let's Encrypt).

## 1. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt gunicorn "psycopg[binary]"
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
