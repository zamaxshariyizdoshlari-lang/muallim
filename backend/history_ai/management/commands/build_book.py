"""Mavzu fayllaridan (content/<kitob>/topics/*.json + meta.json) bitta import JSON yig'adi.

Ishlatish: manage.py build_book content/qd6            -> content/qd6/book.json
           manage.py build_book content/qd6 --verify 4  (kitob matni bazadagi Book id=4 betlaridan)
"""

import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from history_ai.models import Page
from history_ai.services.book_import import validate_book_json

APOS = re.compile(r"[‘’ʻʼ`´]")
YEAR = re.compile(r'(?<!\d)(\d{3,4})(?!\d)')
CAP = re.compile(r"\b[A-ZА-Я][A-Za-zʻʼ'‘’]{3,}")


def norm(text):
    text = text.replace('-\n', '').replace('­', '')
    text = APOS.sub("'", text).lower()
    return re.sub(r'\s+', ' ', text)


def tokens(text):
    text = APOS.sub("'", text)
    years = set(YEAR.findall(text))
    words = set()
    for m in CAP.finditer(text):
        before = text[:m.start()].rstrip()
        if not before or before[-1] in '.?!:(-"“':  # gap boshidagi oddiy so'z - ism emas
            continue
        words.add(m.group(0).lower()[:4])
    return years, words


def iter_claims(topic):
    """(joy, matn, bet) — kitob matni bilan solishtiriladigan har bir da'vo."""
    for i, f in enumerate(topic['explanation'].get('key_facts', [])):
        yield f'key_facts[{i}]', f['fact'], f.get('page')
    for i, q in enumerate(topic['test']):
        yield f'test[{i}]', q['question'] + ' ' + q['options'][q['correct_index']], q.get('page')
    for i, q in enumerate((topic.get('practice') or {}).get('quiz', [])):
        yield f'quiz[{i}]', q['question'] + ' ' + q['options'][q['correct_index']], q.get('page')
    games = topic.get('games') or {}
    for i, it in enumerate((games.get('timeline') or {}).get('items', [])):
        yield f'timeline[{i}]', it['label'], it.get('page')
    for i, p in enumerate((games.get('matching') or {}).get('pairs', [])):
        yield f'matching[{i}]', p['left'] + ' ' + p['right'], p.get('page')
    for i, q in enumerate((games.get('fill_blank') or {}).get('questions', [])):
        yield f'fill_blank[{i}]', q['question'] + ' ' + q['options'][q['correct_index']], q.get('page')
    for i, q in enumerate((topic.get('practice') or {}).get('book_questions', [])):
        yield f'book_questions[{i}]', q['answer'], q.get('page')


class Command(BaseCommand):
    help = "Mavzu fayllarini bitta JSON'ga yig'adi va (ixtiyoriy) kitob matni bilan tekshiradi."

    def add_arguments(self, parser):
        parser.add_argument('folder')
        parser.add_argument('--verify', type=int, help="Matn manbai: bazadagi Book id (Page qatorlari)")

    def handle(self, *args, folder, verify, **options):
        root = Path(folder)
        meta = json.loads((root / 'meta.json').read_text(encoding='utf-8'))
        topics = {}
        for f in sorted((root / 'topics').glob('*.json')):
            t = json.loads(f.read_text(encoding='utf-8'))
            topics[t['key']] = t

        sections, missing = [], []
        for s in meta['sections']:
            ts = []
            for key in s['topics']:
                if key in topics:
                    ts.append(topics[key])
                else:
                    missing.append(key)
            if ts:
                sections.append({'key': s['key'], 'title': s['title'], 'topics': ts})
        data = {'format_version': 1, 'book': meta['book'], 'sections': sections}
        if 'appendix' in meta:
            data['appendix'] = meta['appendix']

        (root / 'book.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        total = sum(len(s['topics']) for s in sections)
        self.stdout.write(f"Yig'ildi: {total} mavzu tayyor" + (f", hali yozilmagan: {', '.join(missing)}" if missing else ''))

        errors = validate_book_json(data)
        for e in errors:
            self.stderr.write(f'  SXEMA: {e}')

        if verify:
            self.verify(data, verify)
        if errors:
            raise CommandError(f"{len(errors)} ta sxema xatosi")

    def verify(self, data, book_id):
        pages = {p.page_number: norm(p.text) for p in Page.objects.filter(book_id=book_id)}
        if not pages:
            raise CommandError(f'Book {book_id} uchun matn (Page) topilmadi')
        issues = 0
        for section in data['sections']:
            for t in section['topics']:
                lo, hi = t['start_page'], t['end_page']
                in_range = ' '.join(pages.get(n, '') for n in range(lo, hi + 1))
                for where, text, page in iter_claims(t):
                    if page is not None and not (lo - 1 <= page <= hi + 1):
                        issues += 1
                        self.stderr.write(f"  [{t['key']}] {where}: bet {page} mavzu oralig'ida emas ({lo}-{hi})")
                    haystack = ' '.join(pages.get(n, '') for n in (page - 1, page, page + 1)) if page else in_range
                    years, words = tokens(text)
                    bad = [y for y in years if y not in haystack] + [w for w in words if norm(w) not in haystack]
                    if bad:
                        issues += 1
                        self.stderr.write(f"  [{t['key']}] {where}: kitobda topilmadi {bad} -> {text[:70]}")
        self.stdout.write(f"Tekshiruv: {issues} ta e'tiroz")
