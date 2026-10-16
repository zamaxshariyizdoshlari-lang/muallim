# -*- coding: utf-8 -*-
"""Matematika kursi: units/m*.py dan book.json va exam_bank.json quradi."""
import importlib.util
import json
import os

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SECTION_TITLES = {
    'm1': "1-bo'lim. Arifmetika asoslari",
    'm2': "2-bo'lim. Algebra asoslari",
    'm3': "3-bo'lim. Tenglamalar va funksiyalar",
    'm4': "4-bo'lim. Planimetriya (tekislikdagi geometriya)",
    'm5': "5-bo'lim. Stereometriya (fazodagi geometriya)",
    'm6': "6-bo'lim. Trigonometriya",
    'm7': "7-bo'lim. Ketma-ketlik, kombinatorika, ehtimol va statistika",
    'm8': "8-bo'lim. Koordinatalar usuli va vektorlar",
    'm9': "9-bo'lim. Matematik analiz asoslari",
    'm10': "10-bo'lim. Oliy matematika elementlari",
}

sections, bank = [], {}
for sk, title in SECTION_TITLES.items():
    path = os.path.join(HERE, 'units', f'{sk}.py')
    if not os.path.exists(path):
        continue
    spec = importlib.util.spec_from_file_location(sk, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    extras = {}
    xpath = os.path.join(HERE, 'units', f'{sk}_x.py')
    if os.path.exists(xpath):
        xspec = importlib.util.spec_from_file_location(sk + '_x', xpath)
        xmod = importlib.util.module_from_spec(xspec)
        xspec.loader.exec_module(xmod)
        extras = xmod.EXTRAS
    topics = []
    for t, b in mod.TOPICS:
        t['explanation'].update(extras.get(t['key'], {}))
        topics.append(t)
        bank[t['key']] = b
    sections.append({'key': sk, 'title': title, 'topics': topics})

book = {
    'format_version': 1,
    'book': {
        'key': 'matematika', 'title': "Matematika (noldan professional darajagacha)",
        'description': "Matematika bo'yicha to'liq kurs: arifmetika, algebra, funksiyalar, geometriya, trigonometriya, kombinatorika va ehtimol, matematik analiz va oliy matematika elementlari.",
        'subject': 'matematika', 'subject_title': "Matematika",
    },
    'sections': sections,
}
with open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8') as f:
    json.dump(book, f, ensure_ascii=False, indent=1)
with open(os.path.join(HERE, 'exam_bank.json'), 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)
nt = sum(len(t['test']) for s in sections for t in s['topics'])
print(f"{len(sections)} bo'lim, {sum(len(s['topics']) for s in sections)} mavzu, test {nt}, bank {sum(len(v) for v in bank.values())}")
