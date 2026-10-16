# -*- coding: utf-8 -*-
"""Informatika kursi: units/s*.py dan book.json va exam_bank.json quradi."""
import importlib.util
import json
import os

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SECTION_TITLES = {
    's1': "1-bo'lim. Axborot va kompyuter asoslari",
    's2': "2-bo'lim. Dasturiy ta'minot va operatsion tizimlar",
    's3': "3-bo'lim. Mantiq va algoritmlar",
    's4': "4-bo'lim. Python dasturlash tili",
    's5': "5-bo'lim. Ofis dasturlari va multimedia",
    's6': "6-bo'lim. Kompyuter tarmoqlari va Internet",
    's7': "7-bo'lim. Ma'lumotlar bazasi va SQL",
    's8': "8-bo'lim. Axborot xavfsizligi",
    's9': "9-bo'lim. Zamonaviy axborot texnologiyalari",
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
        'key': 'informatika', 'title': "Informatika (to'liq kurs)",
        'description': "Informatika bo'yicha to'liq kurs: kompyuter asoslari, algoritmlar, Python, ofis dasturlari, "
                       "tarmoq, ma'lumotlar bazasi, xavfsizlik va zamonaviy texnologiyalar.",
        'subject': 'informatika', 'subject_title': "Informatika",
    },
    'sections': sections,
}
with open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8') as f:
    json.dump(book, f, ensure_ascii=False, indent=1)
with open(os.path.join(HERE, 'exam_bank.json'), 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)
nt = sum(len(t['test']) for s in sections for t in s['topics'])
print(f"{len(sections)} bo'lim, {sum(len(s['topics']) for s in sections)} mavzu, test {nt}, bank {sum(len(v) for v in bank.values())}")
