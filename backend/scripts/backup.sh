#!/usr/bin/env bash
# Baza va yuklangan fayllarning sanali zaxira nusxasi. 14 kundan eskisi o'chiriladi.
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a
OUT="${BACKUP_DIR:-./backups}/$(date +%F_%H%M)"
mkdir -p "$OUT"
if [ -n "${DB_NAME:-}" ]; then
  PGPASSWORD="${DB_PASSWORD:-}" pg_dump -h "${DB_HOST:-localhost}" -U "${DB_USER:-}" "$DB_NAME" | gzip > "$OUT/db.sql.gz"
else
  cp db.sqlite3 "$OUT/db.sqlite3"
fi
[ -d media ] && tar czf "$OUT/media.tar.gz" media
find "${BACKUP_DIR:-./backups}" -mindepth 1 -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
echo "Zaxira tayyor: $OUT"
