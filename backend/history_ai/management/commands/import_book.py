import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from history_ai.services.book_import import import_book_json


class Command(BaseCommand):
    help = "Tayyor JSON (format_version 1) dan kitobni import qiladi: import_book kitob.json [--user teacher]"

    def add_arguments(self, parser):
        parser.add_argument('path')
        parser.add_argument('--user', default='teacher')

    def handle(self, *args, path, user, **options):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        try:
            owner = get_user_model().objects.get(username=user)
        except get_user_model().DoesNotExist:
            raise CommandError(f"Foydalanuvchi topilmadi: {user}")
        bank_path = Path(path).with_name('exam_bank.json')
        if bank_path.exists():
            bank = json.loads(bank_path.read_text(encoding='utf-8'))
            for sec in data['sections']:
                for t in sec['topics']:
                    if t['key'] in bank:
                        t['exam_bank'] = bank[t['key']]
        try:
            summary = import_book_json(data, owner)
        except ValueError as exc:
            for err in exc.args[0]:
                self.stderr.write(f"  - {err}")
            raise CommandError(f"JSON noto'g'ri ({len(exc.args[0])} ta xato)")
        self.stdout.write(self.style.SUCCESS(f"Import tayyor: {summary}"))
