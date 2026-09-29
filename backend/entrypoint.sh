#!/bin/sh
set -e

python manage.py migrate --noinput
(python manage.py createsuperuser --noinput || true)
(python manage.py import_book content/qd6/book.json --user "$DJANGO_SUPERUSER_USERNAME" || echo "OGOHLANTIRISH: qd6 import muvaffaqiyatsiz")
(python manage.py import_book content/turk_a1/book.json --user "$DJANGO_SUPERUSER_USERNAME" || echo "OGOHLANTIRISH: turk_a1 import muvaffaqiyatsiz")
(python manage.py import_book content/turk_a2/book.json --user "$DJANGO_SUPERUSER_USERNAME" || echo "OGOHLANTIRISH: turk_a2 import muvaffaqiyatsiz")
(python manage.py import_book content/ai/book.json --user "$DJANGO_SUPERUSER_USERNAME" || echo "OGOHLANTIRISH: ai import muvaffaqiyatsiz")

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8080}" --workers 2 --threads 4 --timeout 60
