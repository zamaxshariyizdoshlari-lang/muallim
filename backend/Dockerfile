FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DB kerak emas - faqat statik fayllarni yig'adi. DEBUG default True bo'lgani uchun
# (build vaqtida .env / DEBUG env o'rnatilmagan), settings.py'dagi kuchli SECRET_KEY talabi ishga
# tushmaydi.
RUN python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh

EXPOSE 8080
CMD ["./entrypoint.sh"]
