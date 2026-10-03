"""Kitob JSON (content/<kitob>/book.json) savollarini sifat bo'yicha tekshiradi.

Ishlatish: manage.py lint_questions content/ozb7 [--max 40]
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from history_ai.services.question_lint import lint_questions


class Command(BaseCommand):
    help = "Kitob savollarini tekshiradi (uzun to'g'ri javob, takrorlar, daraja va izoh qamrovi)."

    def add_arguments(self, parser):
        parser.add_argument('path', help='content/<kitob> papkasi')
        parser.add_argument('--max', type=int, default=40, help="Ko'rsatiladigan ogohlantirishlar soni")

    def handle(self, *args, **opts):
        book = Path(opts['path']) / 'book.json'
        if not book.exists():
            raise CommandError(f'{book} topilmadi (avval build_book ishga tushiring)')
        data = json.loads(book.read_text(encoding='utf8'))
        topics = [
            (t['key'], t['title'], t['test'])
            for sec in data['sections'] for t in sec['topics']
        ]
        result = lint_questions(topics)
        s = result['summary']
        self.stdout.write(f"Savollar: {s['questions']}")
        self.stdout.write(f"To'g'ri javob eng uzun variant: {s['longest_correct_share']:.0%} (tasodifiy ~25-30%)")
        self.stdout.write(f"Javob o'rinlari (0=A..): {s['answer_positions']}")
        self.stdout.write(f"Darajalar: {s['levels']}")
        self.stdout.write(f"'Nega?' izohi bor: {s['explanation_share']:.0%}")
        self.stdout.write(f"Ogohlantirishlar: {len(result['warnings'])}")
        for where, msg in result['warnings'][:opts['max']]:
            self.stdout.write(f"  {where}: {msg}")
